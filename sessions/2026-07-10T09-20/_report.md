# 📝 CEO 보고서 — 기기 없는 무인 발행(GitHub Actions)

**원 명령:** (사용자) 내가 패드를 켰을 때만 되는 거 아니야? → 기기와 무관한 무인 자동화 요청.

## 핵심 정정
- 패드/아이패드는 백그라운드 크론 불가 → "켰을 때만" 도는 건 사실상 수동.
- **진짜 자동 = 항상 켜진 서버가 대신 발행.** 이미 저장소가 깃허브에 있으므로 **GitHub Actions**가 최적(무료, 기기 불필요).

## ✅ 완료된 작업 (Developer)
- `.github/workflows/threads-autopost.yml` — KST 4슬롯 크론(UTC 환산), TZ=Asia/Seoul,
  `threads_poster.py --due` 실행, 발행 후 `state.json`을 저장소에 다시 커밋해 중복방지.
- 시크릿/변수는 GitHub Secrets·Variables로 주입(토큰 저장소에 노출 X).
- 발행이력(state.json)을 추적 대상으로 전환(.gitignore에서 제외, 초기값 커밋).
- README에 "기기 없이 무인 운영" 세팅 6단계 추가.

## 🔬 검증
- 워크플로 YAML 문법 OK.
- cron 환산 검증: 07:30→"30 22", 12:30→"30 3", 18:00→"0 9", 21:00→"0 12" (UTC) 일치.

## 🚀 다음 액션 (사용자, GitHub 웹에서 5분)
1. Settings→Secrets: `THREADS_USER_ID`, `THREADS_ACCESS_TOKEN` 등록.
2. Settings→Variables: `THREADS_WEEK_START=2026-07-13`.
3. 워크플로를 **main에 병합**(예약은 main에서만 실행).
4. Actions 탭 → Run workflow(dry_run=true)로 테스트 → 실제 가동.

## ⚠️ 한계(솔직)
- 예약 크론 몇 분 지연 가능. long-lived 토큰 ~60일 만료(갱신 자동화는 다음 단계).
- 인포크링크 등록은 여전히 최초 1회 수동(API 없음).
