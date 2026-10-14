#!/usr/bin/env node
/**
 * 오늘살림 영상 자동 포스터 — Instagram 릴스 + Threads 영상
 * autopost/poster.cjs와 같은 패턴(3단계·재시도·고지문 상단·--dry).
 *
 *   Instagram 릴스: POST media(media_type=REELS, video_url) → 상태대기 FINISHED → media_publish
 *   Threads 영상 : POST threads(media_type=VIDEO, video_url) → 처리대기 → threads_publish
 *
 * 전제: 영상(mp4)을 공개 URL로 호스팅(publicVideoBase). 토큰은 config.json(.gitignore).
 *
 * 사용:
 *   node reels-poster.cjs --dry --id 1전기세
 *   node reels-poster.cjs --id 1전기세            # 릴스+쓰레드 둘 다
 *   node reels-poster.cjs --due --only reels      # 다음 1건, 릴스만
 */
const fs = require("fs"), path = require("path");
const DIR = __dirname;
const CFG = JSON.parse(fs.readFileSync(path.join(DIR, "config.json"), "utf8"));
const QUEUE = JSON.parse(fs.readFileSync(path.join(DIR, "video-queue.json"), "utf8")).videos;
const STATE_PATH = path.join(DIR, "posted.json");
const STATE = fs.existsSync(STATE_PATH) ? JSON.parse(fs.readFileSync(STATE_PATH)) : { reels: [], threads: [] };

const ARGS = process.argv.slice(2);
const has = f => ARGS.includes(f);
const val = f => { const i = ARGS.indexOf(f); return i >= 0 ? ARGS[i + 1] : null; };
const DRY = has("--dry"), ONLY = val("--only");
const DISCLOSURE = "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.";

const log = m => console.log(`[${new Date().toISOString().slice(11,19)}] ${m}`);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const saveState = () => fs.writeFileSync(STATE_PATH, JSON.stringify(STATE, null, 2));
const vidUrl = name => CFG.publicVideoBase.replace(/\/$/, "") + "/" + encodeURIComponent(name);

// 캡션: 제휴글이면 고지문 최상단(계정 보호), 쿠팡링크는 쓰레드 본문만
function captionFor(post, platform) {
  let cap = (post.caption || "").trim();
  if (post.coupangLink) {
    cap = `${DISCLOSURE}\n\n${cap}`;
    if (platform === "threads") cap += `\n\n👉 ${post.coupangLink}`;
  }
  return cap;
}
function isTransient(status, body) {
  if (status >= 500 || status === 429) return true;
  const c = body && body.error && body.error.code;
  return [1, 2, 4, 17, 32, 341, 368, 613, -1].includes(c);
}
async function api(url, params) {
  const body = new URLSearchParams(params);
  if (DRY) { log(`[DRY] POST ${url.split("?")[0]} (${[...body.keys()].join(",")})`); return { id: "DRY_" + Math.floor(performance.now()) }; }
  for (let a = 1; a <= 5; a++) {
    let st = 0, j = null;
    try { const r = await fetch(url, { method: "POST", body }); st = r.status; j = await r.json(); if (r.ok && !j.error) return j; }
    catch (e) { j = { error: { code: -1, message: String(e) } }; }
    if (a < 5 && isTransient(st, j)) { const w = Math.min(2 ** a, 16) * 1000; log(`  ↻ 재시도 ${a}/4 (${st}) ${w/1000}s`); await sleep(w); continue; }
    throw new Error(`API 실패(${st}): ${JSON.stringify(j && j.error || j)}`);
  }
}
async function getJSON(url) { if (DRY) return { status_code: "FINISHED", status: "FINISHED" }; return (await fetch(url)).json(); }

// 컨테이너 처리 대기(영상은 길다: 최대 ~5분)
async function waitReady(statusUrl, field) {
  for (let i = 0; i < 60; i++) {
    const s = await getJSON(statusUrl);
    const code = s[field] || s.status_code || s.status;
    if (code === "FINISHED") return;
    if (code === "ERROR" || code === "EXPIRED") throw new Error(`컨테이너 ${code}`);
    log(`  … 영상 처리 대기(${code || "?"})`); await sleep(5000);
  }
  throw new Error("영상 처리 시간초과");
}

// ── Instagram 릴스
async function postReel(post) {
  const v = CFG.apiVersion, uid = CFG.ig.igUserId, tok = CFG.ig.accessToken;
  const base = `https://graph.instagram.com/${v}/${uid}`;
  const c = await api(`${base}/media`, { media_type: "REELS", video_url: vidUrl(post.video), caption: captionFor(post, "reels"), share_to_feed: "true", access_token: tok });
  log(`  릴스 컨테이너 → ${c.id}`);
  await waitReady(`https://graph.instagram.com/${v}/${c.id}?fields=status_code&access_token=${tok}`, "status_code");
  const p = await api(`${base}/media_publish`, { creation_id: c.id, access_token: tok });
  log(`  ✅ 릴스 게시 media_id=${p.id}`); return p.id;
}
// ── Threads 영상
async function postThreadsVideo(post) {
  const uid = CFG.threads.threadsUserId, tok = CFG.threads.accessToken;
  const base = `https://graph.threads.net/v1.0/${uid}`;
  const c = await api(`${base}/threads`, { media_type: "VIDEO", video_url: vidUrl(post.video), text: captionFor(post, "threads"), access_token: tok });
  log(`  쓰레드 영상 컨테이너 → ${c.id}`);
  await waitReady(`https://graph.threads.net/v1.0/${c.id}?fields=status&access_token=${tok}`, "status");
  const p = await api(`${base}/threads_publish`, { creation_id: c.id, access_token: tok });
  log(`  ✅ 쓰레드 게시 id=${p.id}`); return p.id;
}

function pick() {
  if (val("--id")) return QUEUE.find(p => p.id === val("--id"));
  return QUEUE.find(p => !STATE.reels.includes(p.id) || !STATE.threads.includes(p.id));
}
(async () => {
  const post = pick();
  if (!post) { log("게시할 미게시 영상이 없습니다."); process.exit(0); }
  log(`── ${post.id} (${post.video}) ──`);
  const doR = ONLY !== "threads" && !STATE.reels.includes(post.id);
  const doT = ONLY !== "reels" && !STATE.threads.includes(post.id);
  if (doR) { try { await postReel(post); if (!DRY) { STATE.reels.push(post.id); saveState(); } } catch (e) { log(`❌ 릴스 실패: ${e.message}`); } }
  else log("릴스 건너뜀");
  if (doT) { try { await postThreadsVideo(post); if (!DRY) { STATE.threads.push(post.id); saveState(); } } catch (e) { log(`❌ 쓰레드 실패: ${e.message}`); } }
  else log("쓰레드 건너뜀");
  log(`완료. 릴스 ${STATE.reels.length}/${QUEUE.length} · 쓰레드 ${STATE.threads.length}/${QUEUE.length}`);
})();
