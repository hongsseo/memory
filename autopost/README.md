# 🤖 오늘살림 자동 포스터 (Instagram + Threads)

BlueSeyo의 `instagram-poster.cjs` 패턴을 복제해 **이미지 카드 + 캡션을 인스타그램과 쓰레드에 자동 게시**합니다.
캐러셀(여러 장) 지원, 재시도, 플랫폼별 이력 분리, 쿠팡 고지문 강제 삽입.

## 파일
- `poster.cjs` — 메인. IG(자식→CAROUSEL→상태대기→발행) + Threads(자식→CAROUSEL→발행), 재시도, --dry.
- `queue.json` — 게시 큐(캐러셀 5종). `images`/`caption`/`coupangLink`.
- `config.example.json` → `config.json`으로 복사해 자격증명 입력 (git 제외).
- `posted.json` — 게시 이력(IG/Threads 분리, 자동 생성, git 제외).
- `refresh-token.cjs` — 장기 토큰 60일 갱신.
- `run-daily.cmd` — Windows 작업 스케줄러 래퍼.

---

## ⚠️ 핵심 원칙 (문서 규정 반영)
1. **쿠팡 고지문**은 `poster.cjs`의 `DISCLOSURE`에 하드코딩 → 모든 캡션 끝에 자동 삽입(누락 불가).
2. **인스타 캡션 링크는 클릭 안 됨** → 쿠팡 링크는 **Threads 본문**에만 삽입(`coupangLink`). 인스타는 프로필 바이오 링크로 유도.
3. 이미지는 **로컬 업로드 불가** → 공개 URL을 API가 긁어감. 먼저 공개 호스팅에 올려야 함.

---

## 선행 세팅

### 1) 이미지 공개 호스팅 — ✅ 완료 (해결됨)
카드 PNG는 **공개 저장소 `hongsseo/memory`** 에 커밋돼 있고,
`config.example.json`의 `publicMediaBase`가 이미 **검증된 공개 URL**로 박혀 있습니다:
```
https://raw.githubusercontent.com/hongsseo/memory/<커밋SHA>/products/cards
```
- 파일명은 영문(ASCII)로 통일: `card1-1.png` … `card5-4.png` (URL 스크래핑 안정).
- 커밋 SHA로 고정 → 이후 커밋이 쌓여도 이 URL은 불변(인스타가 항상 같은 이미지 획득).
- 실측 검증: `raw.githubusercontent.com` → `HTTP 200 · image/png · 34,694 bytes`.
- 카드를 새로 만들면: `products/cards/`에 커밋 → 새 SHA로 `publicMediaBase`만 갱신.
- (대안) 같은 저장소를 jsDelivr로도 서빙 가능: `https://cdn.jsdelivr.net/gh/hongsseo/memory@<SHA>/products/cards`

### 2) Meta 토큰 (진짜 블로커)
같은 Meta 앱에서 IG·Threads 둘 다 발급:
- **인스타**: 프로페셔널 계정 → `instagram_basic` + `instagram_content_publish` → 장기토큰(60일) + `ig_user_id`
- **쓰레드**: 같은 앱에 Threads 유스케이스 → `threads_basic` + `threads_content_publish` → 장기토큰 + `threads_user_id`
- **BlueSeyo가 쓰는 Meta 앱을 재사용**하고 오늘살림 계정만 추가하면 앱 생성 단계 스킵 가능.

### 3) config.json 작성
```bash
cp config.example.json config.json   # 값 채우기 (git에 안 올라감)
```

---

## 사용
```bash
node poster.cjs --dry --id 1전기세     # 실제 게시 없이 요청 구조 확인
node poster.cjs --id 1전기세           # 특정 캐러셀 IG+Threads 게시
node poster.cjs --due                  # 다음 미게시분 1건 게시(스케줄러용)
node poster.cjs --due --only ig        # IG만 / --only threads = 쓰레드만
```

## 무인 운영 (Windows)
`run-daily.cmd`를 **작업 스케줄러**에 매일 원하는 시각으로 등록 → 매일 1건 자동 게시.
토큰 갱신은 `node refresh-token.cjs`를 주 1회 스케줄에 추가(60일 만료 방어).

## 검증(2026-07-15)
- `--dry`로 IG·Threads 3단계 캐러셀 요청 구조 확인 ✅
- Instagram 캐러셀 API(자식 `is_carousel_item` → 부모 `media_type=CAROUSEL, children` → publish) 최신 문서 대조.
