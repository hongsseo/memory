# 🔗 쿠팡 제휴링크 자동 생성 가이드

상품 URL만 넣으면 제휴링크를 한 번에 만들어 인포크링크에 붙일 수 있어요.
(쿠팡 API 키는 Meta와 달리 **승인 없이 즉시 발급**)

## 1. API 키 발급 (최초 1회, ~3분)
1. https://partners.coupang.com 로그인
2. 상단 **페이지관리 → OPEN API** (또는 '도구 → API 발급')
3. **AccessKey / SecretKey** 발급 → 복사

## 2. 키 등록
`.env` 파일에 추가(automation/.env — git 제외됨):
```
COUPANG_ACCESS_KEY=발급받은_액세스키
COUPANG_SECRET_KEY=발급받은_시크릿키
```
로드:  `set -a; source .env; set +a`

## 3. 상품 URL 넣기
`urls_예시.txt`(또는 새 파일)에 쿠팡 상품 URL을 한 줄에 하나씩.
쿠팡앱 → 상품 → 공유 → 링크 복사 → 붙여넣기.

## 4. 제휴링크 자동 생성
```bash
cd automation
python3 coupang_deeplink.py --urls-file urls_예시.txt --out links.tsv
```
→ 화면에 제휴링크 출력 + `links.tsv`(원본URL <탭> 제휴URL)에 저장.
→ (테스트) 키 없이 구조만 보려면: `python3 coupang_deeplink.py --dry-run --url "..."`

## 5. 인포크링크에 붙이기
`links.tsv`의 제휴URL을 인포크링크 '살림템 모음'에 카테고리별로 등록.
각 상품에 근거 한 줄(coupang_curation.md) + 페이지 상단에 파트너스 표시 문구.

## ⚠️ 규정
- 제휴링크 게시엔 **"쿠팡파트너스 활동으로 일정액의 수수료를 받을 수 있음"** 문구 필수.
- 자가·가족 구매로 수수료 X(정지 사유). SecretKey는 절대 공개 X(.env·비공개만).

## 검증(2026-07-12)
- HMAC(CEA) 서명 = 독립 손계산과 일치 ✅ / dry-run 요청구조 정상 ✅
