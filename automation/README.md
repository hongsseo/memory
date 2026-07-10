# 🤖 오늘살림 — Threads 자동 발행 파이프라인

매일 4개 슬롯(07:30·12:30·18:00·21:00)에 `posts.json`의 글을 **Threads 공식 API로 자동 발행**합니다.
크론에 한 번만 걸어두면 손 안 대고 1주일치가 올라갑니다.

## 무엇이 자동화되고, 무엇이 안 되나 (솔직하게)
| 항목 | 자동화 | 방법 |
|---|---|---|
| **쓰레드 글 발행** | ✅ 완전 자동 | Threads Graph API + 크론 (이 폴더) |
| 쿠팡 제휴링크 생성 | ✅ 가능 | 쿠팡파트너스 Deep Link API (다음 단계) |
| **인포크링크 상품 등록** | ❌ 불가 | 공개 API 없음 + 카카오/SMS 로그인 필요 → **최초 1회 수동**(가이드: `sessions/.../inpock_link.md`) |
| 이미지/카드 첨부 발행 | ⚠️ 가능하나 이미지 URL 필요 | 현재는 TEXT 전용. 이미지 자동화는 2차 |

> 인포크링크는 "매일 반복"이 아니라 "처음 한 번" 세팅이라 자동화 대상에서 빠져도 병목이 아닙니다.
> 진짜 반복 노동인 **발행**을 자동화하는 게 핵심입니다.

---

## 1) Threads API 토큰 발급 (최초 1회, ~15분)
1. https://developers.facebook.com → 앱 만들기 → 유형 **"Threads"** 선택
2. 제품에서 **Threads API** 추가 → 권한(스코프): `threads_basic`, `threads_content_publish`
3. 오늘살림 Threads 계정을 앱에 연결 → **long-lived access token** 발급
4. 내 **Threads User ID**(숫자) 확인 (그래프 API 탐색기 `/me?fields=id`)

## 2) 환경변수 설정
`.env.example`를 복사해 `.env` 만들고 값 채우기:
```bash
cp .env.example .env
# .env 편집:
#   THREADS_USER_ID=1784xxxxxxxxx
#   THREADS_ACCESS_TOKEN=THAAxxxxxxxx...
#   THREADS_WEEK_START=2026-07-13     # 1일차(월요일) 날짜
```
실행 전 로드:  `set -a; source .env; set +a`

## 3) 먼저 미리보기(토큰 없이도 됨)
```bash
python3 threads_poster.py --dry-run --all     # 28개 발행 순서·내용 확인
python3 threads_poster.py --dry-run --id W1    # 한 개만 확인
```

## 4) 실제 발행
```bash
python3 threads_poster.py --id W1        # 특정 글 즉시 발행
python3 threads_poster.py --due          # 지금 슬롯에 해당하는 오늘 글 1개 (크론용)
```
발행 이력은 `state.json`에 기록되어 **중복 발행을 막습니다**.

## 5) 크론에 등록 = 완전 무인 운영
`crontab -e` 에 추가 (경로는 본인 환경에 맞게):
```cron
30 7  * * * cd /home/you/memory/automation && set -a && . ./.env && set +a && python3 threads_poster.py --due >> run.log 2>&1
30 12 * * * cd /home/you/memory/automation && set -a && . ./.env && set +a && python3 threads_poster.py --due >> run.log 2>&1
0  18 * * * cd /home/you/memory/automation && set -a && . ./.env && set +a && python3 threads_poster.py --due >> run.log 2>&1
0  21 * * * cd /home/you/memory/automation && set -a && . ./.env && set +a && python3 threads_poster.py --due >> run.log 2>&1
```
→ 이제 매일 4번, 지정 시각에 오늘 슬롯 글이 자동으로 올라갑니다.
→ 2주차부터는 `posts.json`에 글만 추가하고 `THREADS_WEEK_START`만 바꾸면 됩니다.

## 6) 기기 없이 무인 운영 (권장) — GitHub Actions ⭐
사장님 패드·컴퓨터가 **꺼져 있어도** 깃허브 서버가 대신 발행합니다.
워크플로 파일은 이미 있음: `.github/workflows/threads-autopost.yml`

세팅(최초 1회, GitHub 웹에서):
1. 저장소 → **Settings → Secrets and variables → Actions**
2. **Secrets** 탭 → New repository secret 로 2개 등록
   - `THREADS_USER_ID` = 숫자 유저ID
   - `THREADS_ACCESS_TOKEN` = long-lived 토큰
3. **Variables** 탭 → New variable 로 1개 등록
   - `THREADS_WEEK_START` = `2026-07-13` (1일차 월요일)
4. 이 워크플로를 **기본 브랜치(main)에 병합** ← 예약 실행은 main에서만 켜짐
5. (테스트) 저장소 → **Actions 탭 → "오늘살림 Threads 자동발행" → Run workflow → dry_run=true**

→ 이후 매일 07:30/12:30/18:00/21:00(KST)에 자동 발행. 발행 이력은 `state.json`에
   자동 커밋되어 중복 발행을 막습니다. 사장님은 아무것도 안 켜도 됩니다.

주의:
- 토큰은 **절대 코드/채팅에 붙이지 말고** GitHub Secrets에만 넣으세요(암호화 저장).
- GitHub cron은 몇 분 지연될 수 있음(정확 시각 보장 X) — 발행엔 문제 없음.
- long-lived 토큰은 만료(약 60일)되므로 갱신 필요. 갱신 자동화는 다음 단계.

## 파일
- `posts.json` — 발행 큐(1주차 28개). `day`/`slot`/`text`/`product`.
- `.github/workflows/threads-autopost.yml` — 기기 없는 무인 발행(크론).
- `threads_poster.py` — 발행기(2단계 API: 컨테이너 생성 → 게시, 슬롯 매핑, 중복 방지).
- `state.json` — 발행 이력(자동 생성, git 제외).
- `.env` — 토큰(git 제외).

## 동작 검증(2026-07-10)
- `--dry-run`으로 API 호출 구조(컨테이너→게시) 확인 ✅
- 슬롯 매핑(07:35→아침 … 21:30→밤, 06:00→없음) ✅
- `--due` 주차/슬롯 선택(수요일 12:40 → day3 점심 W10) ✅
- 중복 방지(state에 있으면 건너뜀) ✅

## 다음 자동화(제안)
- 쿠팡파트너스 Deep Link API로 상품글의 링크를 자동 생성/삽입
- 발행 후 텔레그램으로 결과 요약 푸시(youtube/tools/telegram_notify 재사용)
