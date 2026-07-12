#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
쿠팡파트너스 딥링크 자동 생성기
상품 URL을 넣으면 제휴(파트너스) 링크를 한 번에 만들어 줍니다.
→ 인포크링크 '살림템 모음'에 붙이거나, 상품글 CTA에 사용.

필요 환경변수(쿠팡파트너스 → 페이지관리/도구 → OPEN API 키 발급, 승인 불필요):
  COUPANG_ACCESS_KEY
  COUPANG_SECRET_KEY

사용:
  python3 coupang_deeplink.py --url "https://www.coupang.com/vp/products/1234567"
  python3 coupang_deeplink.py --urls-file urls.txt          # 한 줄에 URL 하나씩
  python3 coupang_deeplink.py --urls-file urls.txt --out links.tsv
  python3 coupang_deeplink.py --dry-run --url "..."         # 실제 호출 없이 서명/요청 확인

주의: 생성된 링크에는 파트너스 표시 문구를 함께 노출해야 합니다(공정위).
"""
import argparse, hashlib, hmac, json, os, ssl, sys, time, urllib.request, datetime


def load_dotenv():
    """스크립트 폴더의 .env 를 읽어 환경변수로 로드 (외부 패키지 불필요, 윈도우 호환)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_dotenv()

DOMAIN = "https://api-gateway.coupang.com"
PATH = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
METHOD = "POST"


def signed_datetime(now=None):
    # 쿠팡 CEA 서명용 시각: GMT, 'yyMMddTHHmmssZ'
    now = now or datetime.datetime.utcnow()
    return now.strftime("%y%m%dT%H%M%SZ")


def make_authorization(access_key, secret_key, dt):
    """CEA HmacSHA256 서명 헤더 생성. message = dt + METHOD + PATH(+query='')."""
    message = dt + METHOD + PATH
    signature = hmac.new(secret_key.encode("utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()
    return ("CEA algorithm=HmacSHA256, "
            f"access-key={access_key}, signed-date={dt}, signature={signature}")


def create_deeplinks(urls, access_key, secret_key, dry_run=False):
    dt = signed_datetime()
    auth = make_authorization(access_key or "DRY_ACCESS", secret_key or "DRY_SECRET", dt)
    body = json.dumps({"coupangUrls": urls}).encode("utf-8")
    full = DOMAIN + PATH
    if dry_run:
        print("[DRY] POST", full)
        print("[DRY] Authorization:", auth)
        print("[DRY] Body:", body.decode())
        return [{"originalUrl": u, "shortenUrl": "(dry-run)"} for u in urls]
    req = urllib.request.Request(full, data=body, method=METHOD)
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "application/json;charset=UTF-8")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        resp = json.loads(r.read().decode())
    return resp.get("data", [])


def main():
    ap = argparse.ArgumentParser(description="쿠팡파트너스 딥링크 자동 생성")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="상품 URL 하나")
    g.add_argument("--urls-file", help="URL 목록 파일(한 줄에 하나)")
    ap.add_argument("--out", help="결과 저장 파일(TSV: 원본URL<tab>제휴URL)")
    ap.add_argument("--dry-run", action="store_true", help="실제 호출 없이 서명/요청 확인")
    args = ap.parse_args()

    if args.url:
        urls = [args.url.strip()]
    else:
        with open(args.urls_file, encoding="utf-8") as f:
            urls = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not urls:
        print("URL이 없습니다."); sys.exit(1)

    access = os.environ.get("COUPANG_ACCESS_KEY")
    secret = os.environ.get("COUPANG_SECRET_KEY")
    if not args.dry_run and (not access or not secret):
        print("환경변수 COUPANG_ACCESS_KEY / COUPANG_SECRET_KEY 필요. (--dry-run 은 없이도 됨)")
        sys.exit(2)

    # 쿠팡 딥링크 API는 한 번에 여러 URL 처리 가능
    try:
        data = create_deeplinks(urls, access, secret, dry_run=args.dry_run)
    except urllib.error.HTTPError as e:
        print("❌ API 오류:", e.code, e.read().decode(), file=sys.stderr); sys.exit(1)

    lines = []
    print("\n=== 제휴 링크 ===")
    for d in data:
        orig = d.get("originalUrl", "")
        short = d.get("shortenUrl") or d.get("landingUrl") or ""
        print(f"- {orig}\n  → {short}")
        lines.append(f"{orig}\t{short}")
    if args.out and not args.dry_run:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\n저장: {args.out}")
    print("\n⚠️ 게시 시 '쿠팡파트너스 활동으로 일정액의 수수료를 받을 수 있음' 문구를 함께 노출하세요.\n")


if __name__ == "__main__":
    main()
