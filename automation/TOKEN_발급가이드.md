# 🔑 Threads API 토큰 발급 가이드 (오늘살림)

자동 발행에는 **API 액세스 토큰**이 필요합니다. Threads 앱 로그인과는 별개예요.
아래 순서대로 하면 됩니다. (처음 1회, 약 15분)

> 준비물: 오늘살림 Threads 계정 + 그 계정과 연결된 인스타그램/페이스북 로그인.

---

## STEP 1. Meta 개발자 계정 만들기
1. https://developers.facebook.com 접속 → 우측 상단 **로그인**(오늘살림과 연결된 계정으로)
2. 처음이면 **"개발자 등록"** — 휴대폰 인증 1회.

## STEP 2. 앱 만들기
1. 우측 상단 **My Apps → Create App**
2. "무엇을 하려 하나요?" → **"Access the Threads API"**(Threads API 사용) 선택
3. 앱 이름: `오늘살림-autopost` (아무거나) → 생성

## STEP 3. Threads API 권한(스코프) 추가
1. 앱 대시보드 좌측 **Use cases**(사용 사례) → **Access the Threads API** → **Customize**
2. 아래 두 권한을 **Add**:
   - `threads_basic`
   - `threads_content_publish`

## STEP 4. 내 Threads 계정 연결
1. 같은 화면에서 **Threads 계정 연결/추가**(Add or connect account) →
   오늘살림 Threads 계정으로 승인.

## STEP 5. 토큰 생성(짧은 토큰)
1. Use case 화면의 **Generate access token**(액세스 토큰 생성) 클릭 →
   오늘살림 계정 선택 → **짧은 수명 토큰(short-lived)** 이 나옵니다. 복사.

## STEP 6. 긴 수명 토큰으로 변환 + 내 User ID 확인 (도우미 스크립트)
짧은 토큰은 몇 시간이면 만료돼요. 아래 한 줄이면 **60일짜리 긴 토큰 + User ID**를 뽑아줍니다.
```bash
cd automation
python3 get_token.py --app-secret <앱시크릿> --short-token <STEP5에서_복사한_토큰>
```
- `앱시크릿`: 앱 대시보드 → **App settings → Basic → App secret**(Show) 값.
- 출력된 `THREADS_ACCESS_TOKEN`(긴 토큰)과 `THREADS_USER_ID`를 그대로 사용하면 됩니다.

## STEP 7. GitHub에 넣기 (무인 발행 켜기)
저장소 → **Settings → Secrets and variables → Actions**
- **Secrets**: `THREADS_ACCESS_TOKEN`(긴 토큰), `THREADS_USER_ID`
- **Variables**: `THREADS_WEEK_START = 2026-07-13`
→ 워크플로를 main에 병합하면 매일 4번 자동 발행 시작. (README.md 6번 참고)

---

## ⚠️ 주의
- **토큰은 비밀번호입니다.** 채팅·코드·캡처에 붙이지 마세요. GitHub Secrets에만.
- 긴 토큰도 **약 60일 후 만료** → 갱신 필요. `python3 get_token.py --refresh <긴토큰> --app-secret <시크릿>`으로 재발급(만료 전 아무 때나). 자동 갱신은 다음 단계에서 워크플로로 붙일 수 있음.
- Threads API는 **하루 발행 한도**가 있으나(계정당 250건/24h 수준) 우리 4~5건/일엔 여유.

## 막히면
STEP 3~5 화면 이름이 Meta 업데이트로 조금씩 바뀝니다. 화면 캡처를 보여주시면 어디를 눌러야 하는지 짚어드릴게요.
