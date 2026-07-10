# 📝 CEO 보고서 — Threads 발행 자동화 파이프라인 구축

**원 명령:** (사용자) 나는 자동화를 하려는거야 / 크롬으로는 가능하잖아

## ✅ 완료된 작업 (Developer)
회사 목표 "매주 자동으로 올리는 파이프라인"을 실제 코드로 구현. **Threads 공식 API 자동 발행기** 완성.
- `automation/posts.json` — 1주차 28개 발행 큐(day/slot/text/product)
- `automation/threads_poster.py` — 2단계 API(컨테이너 생성→게시), 슬롯 자동매핑, state.json 중복방지, dry-run
- `automation/README.md` — 토큰 발급법·크론 등록법·검증 결과
- `.env.example` + .gitignore(토큰·상태 제외)

## 🔬 동작 검증 (2026-07-10, 토큰 없이 dry-run)
- API 호출 구조(POST /{uid}/threads → /{uid}/threads_publish) 확인 ✅
- 슬롯 매핑 07:35→아침 / 12:40→점심 / 18:05→저녁 / 21:30→밤 / 06:00→없음 ✅
- --due 주차·슬롯 선택: 수요일 12:40 → day3 점심 W10 정확 ✅
- 중복 방지: state에 있으면 건너뜀 ✅

## 🧭 자동화 범위 (솔직한 정리)
| 항목 | 자동화 |
|---|---|
| 쓰레드 발행 | ✅ 크론 등록 시 완전 무인 |
| 쿠팡 제휴링크 | ✅ 가능(다음 단계, Deep Link API) |
| 인포크링크 상품등록 | ❌ API 없음+SMS로그인 → 최초 1회 수동 |

## 🚀 다음 액션 (Top 3)
1. **(사용자)** Meta 개발자앱에서 Threads 토큰 발급(threads_basic + threads_content_publish) → `.env` 채우기.
2. **(사용자)** `python3 threads_poster.py --dry-run --all`로 미리보고, `--id W1`로 실발행 1건 테스트.
3. **(사용자)** 크론 4줄 등록 → 무인 운영 시작. 2주차부터 posts.json에 글만 추가.

## 💡 인사이트
- 인포크링크는 '매일'이 아니라 '한 번' 세팅이라 자동화 병목이 아님. 진짜 반복노동인 발행을 자동화한 것이 핵심.
- posts.json 분리 설계 → 콘텐츠(Writer)와 발행(Developer)이 독립. 매주 글만 갈아끼우면 파이프라인 재사용.
