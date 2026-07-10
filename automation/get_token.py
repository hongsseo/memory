#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 토큰 도우미 — 짧은 수명 토큰을 60일짜리 긴 토큰으로 바꾸고, User ID를 확인합니다.

사용:
  # 짧은 토큰 → 긴 토큰(+User ID)
  python3 get_token.py --app-secret <APP_SECRET> --short-token <SHORT_TOKEN>

  # 만료 전 긴 토큰 갱신(다시 60일)
  python3 get_token.py --app-secret <APP_SECRET> --refresh <LONG_TOKEN>

출력된 THREADS_ACCESS_TOKEN / THREADS_USER_ID 를 GitHub Secrets/Variables 에 넣으세요.
(토큰은 화면에만 출력됩니다. 파일로 저장하지 않습니다 — 직접 안전한 곳에 복사하세요.)
"""
import argparse, json, sys, urllib.parse, urllib.request

API = "https://graph.threads.net"


def _get(path, params):
    url = f"{API}{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())


def exchange_short_to_long(short_token, app_secret):
    # 짧은 토큰 → 긴 토큰 (60일)
    return _get("/access_token", {
        "grant_type": "th_exchange_token",
        "client_secret": app_secret,
        "access_token": short_token,
    })


def refresh_long(long_token):
    # 긴 토큰 갱신 (다시 60일). 최소 24시간 이상 사용된 토큰이어야 함.
    return _get("/refresh_access_token", {
        "grant_type": "th_refresh_token",
        "access_token": long_token,
    })


def fetch_user_id(token):
    return _get("/v1.0/me", {"fields": "id,username", "access_token": token})


def main():
    ap = argparse.ArgumentParser(description="Threads 토큰 도우미")
    ap.add_argument("--app-secret", required=True, help="Meta 앱 시크릿(App settings→Basic)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--short-token", help="STEP5에서 복사한 짧은 수명 토큰")
    g.add_argument("--refresh", help="갱신할 기존 긴 수명 토큰")
    args = ap.parse_args()

    try:
        if args.short_token:
            res = exchange_short_to_long(args.short_token, args.app_secret)
        else:
            res = refresh_long(args.refresh)
    except urllib.error.HTTPError as e:
        print("❌ 토큰 발급 실패:", e.read().decode(), file=sys.stderr)
        sys.exit(1)

    long_token = res.get("access_token")
    expires = res.get("expires_in")
    if not long_token:
        print("❌ 응답에 토큰이 없습니다:", res, file=sys.stderr); sys.exit(1)

    print("\n=== 발급 성공 ===")
    print(f"유효기간: 약 {int(expires)//86400}일" if expires else "유효기간: (미제공)")

    try:
        me = fetch_user_id(long_token)
        uid = me.get("id"); uname = me.get("username")
        print(f"계정: @{uname}") if uname else None
    except Exception as e:
        uid = None
        print("(User ID 조회 실패 — 토큰으로 /me 호출 확인 필요:", e, ")", file=sys.stderr)

    print("\n───── GitHub 에 넣을 값 ─────")
    if uid:
        print(f"THREADS_USER_ID      = {uid}")
    print(f"THREADS_ACCESS_TOKEN = {long_token}")
    print("────────────────────────────")
    print("⚠️ 이 토큰은 비밀번호입니다. GitHub Secrets 에만 넣고, 채팅/코드에 붙이지 마세요.\n")


if __name__ == "__main__":
    main()
