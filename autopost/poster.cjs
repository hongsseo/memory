#!/usr/bin/env node
/**
 * 오늘살림 자동 포스터 — Instagram + Threads (이미지/캐러셀)
 * BlueSeyo의 instagram-poster.cjs 패턴 복제 + 이미지·쓰레드 확장.
 *
 * 3단계(컨테이너 생성 → 처리 대기 → 발행), 재시도(isTransient), 플랫폼별 이력 분리,
 * 캡션에 쿠팡 고지문 하드코딩(누락 불가), --dry 모드.
 *
 * 사용:
 *   node poster.cjs --dry          # 실제 게시 없이 요청 미리보기
 *   node poster.cjs --due          # 다음 미게시분 1건 IG+Threads 게시
 *   node poster.cjs --id 1전기세    # 특정 항목 게시
 *   node poster.cjs --only ig      # IG만 (threads도 가능)
 */
const fs = require("fs");
const path = require("path");

const DIR = __dirname;
const CFG = load("config.json");            // 시크릿(.gitignore)
const QUEUE = load("queue.json").posts;
const STATE_PATH = path.join(DIR, "posted.json");
const STATE = fs.existsSync(STATE_PATH) ? JSON.parse(fs.readFileSync(STATE_PATH)) : { ig: [], threads: [] };

const ARGS = process.argv.slice(2);
const has = (f) => ARGS.includes(f);
const val = (f) => { const i = ARGS.indexOf(f); return i >= 0 ? ARGS[i + 1] : null; };
const DRY = has("--dry");
const ONLY = val("--only");                 // 'ig' | 'threads' | null(둘다)

const DISCLOSURE = "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.";

function load(f) { return JSON.parse(fs.readFileSync(path.join(DIR, f), "utf8")); }
function log(m) { console.log(`[${new Date().toISOString().slice(11,19)}] ${m}`); }
function saveState() { fs.writeFileSync(STATE_PATH, JSON.stringify(STATE, null, 2)); }
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const imgUrl = (name) => CFG.publicMediaBase.replace(/\/$/, "") + "/" + encodeURIComponent(name);

// 캡션 조립
//  - 제휴(대가성) 글: 공정위 고지문을 반드시 '최상단'에 배치(계정 정지 예방 — 영상 규칙)
//  - 순수 정보/공감글(coupangLink 없음): 고지문 불필요 → 넣지 않음
//  - 쿠팡 링크는 Threads 본문에만(클릭 가능), 인스타는 프로필 유도
function captionFor(post, platform) {
  let cap = post.caption.trim();
  if (post.coupangLink) {
    cap = `${DISCLOSURE}\n\n${cap}`;                 // 고지문 최상단
    if (platform === "threads") cap += `\n\n👉 ${post.coupangLink}`;
  }
  return cap;
}

function isTransient(status, body) {
  if (status >= 500) return true;
  if (status === 429) return true;
  const code = body && body.error && body.error.code;
  // 1: unknown, 2: transient, 4/17/32/613: rate/throttle, 368: temporarily blocked, -1: network
  return [1, 2, 4, 17, 32, 341, 368, 613, -1].includes(code);
}

async function api(url, params) {
  const body = new URLSearchParams(params);
  if (DRY) { log(`[DRY] POST ${url.split("?")[0]}  (${[...body.keys()].join(",")})`); return { id: "DRY_" + Math.floor(performance.now()) }; }
  for (let attempt = 1; attempt <= 5; attempt++) {
    let status = 0, json = null;
    try {
      const res = await fetch(url, { method: "POST", body });
      status = res.status; json = await res.json();
      if (res.ok && !json.error) return json;
    } catch (e) { json = { error: { code: -1, message: String(e) } }; }
    if (attempt < 5 && isTransient(status, json)) {
      const wait = Math.min(2 ** attempt, 16) * 1000;
      log(`  ↻ 일시 오류(${status}) 재시도 ${attempt}/4 — ${wait/1000}s 후`); await sleep(wait); continue;
    }
    throw new Error(`API 실패(${status}): ${JSON.stringify(json && json.error || json)}`);
  }
}
async function get(url) {
  if (DRY) return { status_code: "FINISHED" };
  const res = await fetch(url); return res.json();
}

// ── Instagram 캐러셀: 자식 컨테이너 → 부모(CAROUSEL) → 상태대기 → 발행
async function postInstagram(post) {
  const v = CFG.apiVersion, uid = CFG.ig.igUserId, tok = CFG.ig.accessToken;
  const base = `https://graph.instagram.com/${v}/${uid}`;
  const children = [];
  for (const name of post.images) {
    const r = await api(`${base}/media`, { image_url: imgUrl(name), is_carousel_item: "true", access_token: tok });
    children.push(r.id); log(`  IG 자식 컨테이너 ${name} → ${r.id}`);
  }
  const parent = await api(`${base}/media`, { media_type: "CAROUSEL", children: children.join(","), caption: captionFor(post, "ig"), access_token: tok });
  log(`  IG 부모 컨테이너 → ${parent.id}`);
  await waitFinished(`https://graph.instagram.com/${v}/${parent.id}?fields=status_code&access_token=${tok}`);
  const pub = await api(`${base}/media_publish`, { creation_id: parent.id, access_token: tok });
  log(`  ✅ IG 게시 완료 media_id=${pub.id}`); return pub.id;
}

// ── Threads 캐러셀: 자식(IMAGE) → 부모(CAROUSEL) → 발행
async function postThreads(post) {
  const uid = CFG.threads.threadsUserId, tok = CFG.threads.accessToken;
  const base = `https://graph.threads.net/v1.0/${uid}`;
  const children = [];
  for (const name of post.images) {
    const r = await api(`${base}/threads`, { media_type: "IMAGE", image_url: imgUrl(name), is_carousel_item: "true", access_token: tok });
    children.push(r.id); log(`  TH 자식 ${name} → ${r.id}`);
  }
  const parent = await api(`${base}/threads`, { media_type: "CAROUSEL", children: children.join(","), text: captionFor(post, "threads"), access_token: tok });
  log(`  TH 부모 → ${parent.id}`);
  if (!DRY) await sleep(30000);                       // 처리 대기(권장)
  const pub = await api(`${base}/threads_publish`, { creation_id: parent.id, access_token: tok });
  log(`  ✅ Threads 게시 완료 id=${pub.id}`); return pub.id;
}

async function waitFinished(statusUrl) {
  for (let i = 0; i < 20; i++) {
    const s = await get(statusUrl);
    if (s.status_code === "FINISHED") return;
    if (s.status_code === "ERROR") throw new Error("컨테이너 처리 ERROR");
    log(`  … 처리 대기(${s.status_code||"?"})`); await sleep(5000);
  }
  throw new Error("컨테이너 처리 시간초과");
}

function pickPost() {
  if (val("--id")) return QUEUE.find(p => p.id === val("--id"));
  // IG·Threads 둘 중 하나라도 아직 안 올라간 첫 항목
  return QUEUE.find(p => !STATE.ig.includes(p.id) || !STATE.threads.includes(p.id));
}

(async () => {
  const post = pickPost();
  if (!post) { log("게시할 미게시 항목이 없습니다."); process.exit(0); }
  log(`── ${post.id} (${post.images.length}장) ──`);

  const doIG = ONLY !== "threads" && !STATE.ig.includes(post.id);
  const doTH = ONLY !== "ig" && !STATE.threads.includes(post.id);

  if (doIG) {
    try { await postInstagram(post); if (!DRY) { STATE.ig.push(post.id); saveState(); } }
    catch (e) { log(`❌ IG 실패: ${e.message}`); }
  } else log("IG 건너뜀(이미 게시/제외)");

  if (doTH) {
    try { await postThreads(post); if (!DRY) { STATE.threads.push(post.id); saveState(); } }
    catch (e) { log(`❌ Threads 실패: ${e.message}`); }
  } else log("Threads 건너뜀(이미 게시/제외)");

  log(`완료. IG ${STATE.ig.length}/${QUEUE.length} · Threads ${STATE.threads.length}/${QUEUE.length}`);
})();
