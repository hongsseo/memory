#!/usr/bin/env node
/**
 * 오늘살림 유튜브 쇼츠 자동 업로더 (YouTube Data API v3)
 * video-queue.json의 영상을 오늘살림 유튜브 채널에 업로드.
 * - 세로 1080x1920 + 60초 미만 → 유튜브가 자동으로 '쇼츠' 인식(#Shorts 포함)
 * - 토큰: config.json의 youtube {clientId, clientSecret, refreshToken} (get-youtube-token.cjs로 발급)
 *
 * 준비:  npm install googleapis      (autovideo 폴더에서)
 * 사용:
 *   node youtube-upload.cjs --dry --id 1전기세
 *   node youtube-upload.cjs --id 1전기세
 *   node youtube-upload.cjs --due            # 다음 미업로드 1건
 */
const fs = require("fs"), path = require("path");
const { google } = require("googleapis");
const DIR = __dirname;
const CFG = JSON.parse(fs.readFileSync(path.join(DIR, "config.json"), "utf8"));
const QUEUE = JSON.parse(fs.readFileSync(path.join(DIR, "video-queue.json"), "utf8")).videos;
const LOCAL = path.join(DIR, CFG.localVideoDir || "out");          // mp4 로컬 경로
const STATE_PATH = path.join(DIR, "posted-youtube.json");
const STATE = fs.existsSync(STATE_PATH) ? JSON.parse(fs.readFileSync(STATE_PATH)) : { youtube: [] };

const ARGS = process.argv.slice(2);
const has = f => ARGS.includes(f);
const val = f => { const i = ARGS.indexOf(f); return i >= 0 ? ARGS[i + 1] : null; };
const DRY = has("--dry");
const log = m => console.log(`[${new Date().toISOString().slice(11,19)}] ${m}`);
const DISCLOSURE = "이 영상에는 쿠팡 파트너스 활동의 일환으로 수수료를 제공받는 링크가 포함되어 있습니다.";

function oauth() {
  const o = new google.auth.OAuth2(CFG.youtube.clientId, CFG.youtube.clientSecret);
  o.setCredentials({ refresh_token: CFG.youtube.refreshToken });
  return o;
}
function pick() {
  if (val("--id")) return QUEUE.find(p => p.id === val("--id"));
  return QUEUE.find(p => !STATE.youtube.includes(p.id));
}
function descFor(post) {
  const y = post.youtube || {};
  let d = (y.description || post.caption || "").trim();
  if (post.coupangLink) {
    d = `${DISCLOSURE}\n\n${d}\n\n👉 ${post.coupangLink}`;
  }
  if (!/#Shorts/i.test(d)) d += "\n\n#Shorts";
  return d;
}

(async () => {
  const post = pick();
  if (!post) { log("업로드할 미게시 영상이 없습니다."); process.exit(0); }
  const file = path.join(LOCAL, post.video);
  const y = post.youtube || {};
  const title = (y.title || post.id).slice(0, 100);
  const desc = descFor(post);
  const tags = y.tags || ["오늘살림", "살림팁", "절약팁", "Shorts"];
  log(`── 유튜브 업로드: ${post.id} ──`);
  log(`  제목: ${title}`);
  if (DRY) { log(`  [DRY] videos.insert (${file})  설명 ${desc.length}자  태그 ${tags.length}개`); log("DRY 종료"); return; }
  if (!fs.existsSync(file)) { log(`❌ 파일 없음: ${file}`); process.exit(1); }

  const yt = google.youtube({ version: "v3", auth: oauth() });
  try {
    const res = await yt.videos.insert({
      part: ["snippet", "status"],
      requestBody: {
        snippet: { title, description: desc, tags, categoryId: "26" },           // 26 = Howto & Style
        status: { privacyStatus: CFG.youtube.privacy || "public", selfDeclaredMadeForKids: false },
      },
      media: { body: fs.createReadStream(file) },
    });
    log(`  ✅ 업로드 완료 videoId=${res.data.id}  https://youtu.be/${res.data.id}`);
    STATE.youtube.push(post.id);
    fs.writeFileSync(STATE_PATH, JSON.stringify(STATE, null, 2));
  } catch (e) {
    log(`❌ 업로드 실패: ${e.errors ? JSON.stringify(e.errors) : e.message}`);
    process.exit(1);
  }
})();
