# 🎬 오늘살림 영상 자동화 (생성 + 업로드)

블루세요처럼 **"알아서 올라가는"** 구조 = ①영상 생성기 + ②업로더 + ③스케줄러(형님 기기).
상황극 숏츠(키네틱 자막 밈)를 만들고 → 인스타 릴스·쓰레드·유튜브 쇼츠에 자동 게시합니다.

## 구성
```
shorts/   build_kinetic.py   # ① 생성기: skits.json → 세로 숏츠 mp4 (효과음 포함)
          skits.json          #    상황극 대본(글만 바꾸면 무한 생산)
          out/                #    생성된 mp4 (git 제외)
          videos/             #    게시용 공개 호스팅 mp4 (raw.githubusercontent)
autovideo/ reels-poster.cjs   # ② 인스타 릴스 + 쓰레드 영상 업로더
          youtube-upload.cjs  # ② 유튜브 쇼츠 업로더
          get-youtube-token.cjs
          video-queue.json    #    영상별 캡션·쿠팡링크·유튜브 제목/설명
          config.example.json → config.json (git 제외)
```

## ① 영상 만들기
```bash
cd shorts
python3 build_kinetic.py        # out/ 에 5개 생성 (폰트 자동 다운로드)
```
새 주제 추가 = `skits.json`에 비트만 추가 → 재실행. 끝.

## ② 업로드 준비(토큰)
`config.json` 작성(`cp config.example.json config.json`):
- **ig / threads** : 오늘살림 Meta 토큰 (autopost와 동일 — `autopost/토큰_이어서하기.md` 참고). 릴스·쓰레드 영상용.
- **youtube** : 오늘살림 유튜브 채널 토큰
  1. Google Cloud Console → YouTube Data API v3 사용 설정 → OAuth 데스크톱 클라이언트 생성
  2. `npm install googleapis`
  3. `node get-youtube-token.cjs <clientId> <clientSecret>` → 오늘살림 유튜브 구글계정으로 승인 → refreshToken 저장
- **publicVideoBase** : `shorts/videos/`의 raw URL (릴스·쓰레드가 영상을 긁어감). 영상 교체 시 커밋 SHA만 갱신.

## ③ 업로드 실행
```bash
# 인스타 릴스 + 쓰레드 영상
node autovideo/reels-poster.cjs --dry --id 1전기세   # 미리보기
node autovideo/reels-poster.cjs --due                # 다음 1건
node autovideo/reels-poster.cjs --due --only reels   # 릴스만 / --only threads

# 유튜브 쇼츠
node autovideo/youtube-upload.cjs --dry --id 1전기세
node autovideo/youtube-upload.cjs --due
```

## 무인 운영
- Windows 작업 스케줄러 / cron에 매일 `--due` 3종(릴스·쓰레드·쇼츠) 등록 → 하루 1편 자동.
- 토큰 만료: Meta 60일(autopost/refresh-token.cjs 재사용), 유튜브 refreshToken은 장기 유효.

## 규정
- 제휴(쿠팡) 영상은 **고지문 자동 상단**(릴스·쓰레드·쇼츠 설명). 유튜브는 '유료 프로모션 포함'도 체크 권장.
- 일반 영상은 프로필/설명 인포크 링크로 유도.

## 한계(정직)
- 실사·AI 캐릭터·성우 음성은 이 파이프라인 범위 밖(별도 촬영/AI툴/CapCut TTS 필요).
- 배경음악은 저작권상 미포함 → 업로드 시 트렌드 사운드 1탭 권장(도달↑).
