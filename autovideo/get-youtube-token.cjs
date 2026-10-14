#!/usr/bin/env node
/**
 * 유튜브 업로드용 refresh_token 1회 발급기 (오늘살림 채널)
 *
 * 준비(한 번만):
 *  1) Google Cloud Console → 프로젝트 생성 → "YouTube Data API v3" 사용 설정
 *  2) OAuth 동의 화면 구성(외부, 테스트 사용자에 오늘살림 구글계정 추가)
 *  3) 사용자 인증 정보 → OAuth 클라이언트 ID → 유형 "데스크톱 앱" 생성
 *     → clientId, clientSecret 확보
 *
 * 실행:
 *   npm install googleapis
 *   node get-youtube-token.cjs <clientId> <clientSecret>
 *   → 출력된 URL을 '오늘살림 유튜브 채널의 구글 계정'으로 로그인해 승인
 *   → 받은 코드를 터미널에 붙여넣기
 *   → refresh_token 출력 → config.json의 youtube.refreshToken에 저장
 */
const { google } = require("googleapis");
const readline = require("readline");
const [clientId, clientSecret] = process.argv.slice(2);
if (!clientId || !clientSecret) { console.error("사용법: node get-youtube-token.cjs <clientId> <clientSecret>"); process.exit(1); }

const o = new google.auth.OAuth2(clientId, clientSecret, "urn:ietf:wg:oauth:2.0:oob");
const url = o.generateAuthUrl({ access_type: "offline", prompt: "consent", scope: ["https://www.googleapis.com/auth/youtube.upload"] });
console.log("\n1) 아래 URL을 열어 '오늘살림' 유튜브 채널 구글 계정으로 승인하세요:\n\n" + url + "\n");
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
rl.question("2) 받은 코드 붙여넣기: ", async code => {
  rl.close();
  try {
    const { tokens } = await o.getToken(code.trim());
    if (!tokens.refresh_token) { console.error("\n⚠️ refresh_token이 없습니다. prompt=consent 로 다시 시도하세요."); process.exit(1); }
    console.log("\n✅ refresh_token (config.json의 youtube.refreshToken 에 저장):\n\n" + tokens.refresh_token + "\n");
  } catch (e) { console.error("토큰 교환 실패:", e.message); process.exit(1); }
});
