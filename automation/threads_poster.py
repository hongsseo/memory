#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
오늘살림 — Threads 자동 발행기
Threads 공식 Graph API(2단계: 컨테이너 생성 → 게시)를 사용해 posts.json의 글을
슬롯 스케줄에 맞춰 자동으로 올립니다.

필요 환경변수 (.env 또는 export):
  THREADS_USER_ID       - Threads 사용자 ID (숫자)
  THREADS_ACCESS_TOKEN  - long-lived access token (threads_basic, threads_content_publish 권한)

사용 예:
  python3 threads_poster.py --dry-run --all        # 실제 발행 없이 API 호출만 미리보기
  python3 threads_poster.py --due                  # 지금 시각의 슬롯에 해당하는 '오늘' 글 1개 발행
  python3 threads_poster.py --id W1                # 특정 글 즉시 발행
  python3 threads_poster.py --day 1 --slot 아침     # 특정 글 즉시 발행

크론 예시(자세한 건 README.md):
  30 7  * * *  cd /path/automation && python3 threads_poster.py --due >> run.log 2>&1
  30 12 * * *  ...
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request, datetime

API_BASE = "https://graph.threads.net/v1.0"
HERE = os.path.dirname(os.path.abspath(__file__))
POSTS_PATH = os.path.join(HERE, "posts.json")
STATE_PATH = os.path.join(HERE, "state.json")   # 발행 이력(중복 방지)

# 슬롯 → 발행 시각(로컬). --due가 현재 시각을 가장 가까운 슬롯에 매핑할 때 사용.
SLOT_HHMM = {"아침": (7, 30), "점심": (12, 30), "저녁": (18, 0), "밤": (21, 0)}


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_posts():
    with open(POSTS_PATH, encoding="utf-8") as f:
        return json.load(f)["posts"]


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"posted": {}}   # id -> {media_id, at}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _post(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def publish_thread(text, user_id, token, dry_run=False):
    """Threads 2단계 발행: 컨테이너 생성 → (권장 대기) → 게시. media_id 반환."""
    # 1) 컨테이너 생성
    create_url = f"{API_BASE}/{user_id}/threads"
    create_params = {"media_type": "TEXT", "text": text, "access_token": token}
    if dry_run:
        log(f"[DRY] POST {create_url}")
        log(f"[DRY]   media_type=TEXT, text=({len(text)}자) '{text[:24]}...'")
        log(f"[DRY] → (권장 30초 대기) → POST {API_BASE}/{user_id}/threads_publish  creation_id=<컨테이너ID>")
        return "DRY_MEDIA_ID"
    resp = _post(create_url, create_params)
    creation_id = resp["id"]
    log(f"컨테이너 생성됨 creation_id={creation_id}")
    # 2) 권장 대기 (Meta 문서: 게시 전 ~30초 처리 시간 권장)
    time.sleep(30)
    # 3) 게시
    publish_url = f"{API_BASE}/{user_id}/threads_publish"
    pub = _post(publish_url, {"creation_id": creation_id, "access_token": token})
    media_id = pub["id"]
    log(f"게시 완료 media_id={media_id}")
    return media_id


def current_slot(now=None):
    """현재 시각을 가장 가까운(그리고 이미 지난) 슬롯으로 매핑."""
    now = now or datetime.datetime.now()
    cur = now.hour * 60 + now.minute
    best, best_delta = None, 10**9
    for slot, (h, m) in SLOT_HHMM.items():
        delta = cur - (h * 60 + m)
        if 0 <= delta < best_delta:   # 이미 지난 슬롯 중 가장 최근
            best, best_delta = slot, delta
    return best


def pick_due(posts, state, now=None):
    """오늘(=1주차 시작 기준 경과일) + 현재 슬롯에 해당하는 미발행 글 1개."""
    now = now or datetime.datetime.now()
    slot = current_slot(now)
    if not slot:
        return None, "현재 시각에 해당하는 발행 슬롯이 없습니다(07:30/12:30/18:00/21:00 이후에 실행)."
    start = os.environ.get("THREADS_WEEK_START")  # YYYY-MM-DD (1일차 날짜)
    if start:
        d0 = datetime.date.fromisoformat(start)
        day = (now.date() - d0).days + 1
    else:
        day = None  # 미설정 시 슬롯만으로 첫 미발행 글 선택
    for p in posts:
        if p["id"] in state["posted"]:
            continue
        if p["slot"] != slot:
            continue
        if day is not None and p["day"] != day:
            continue
        return p, None
    return None, f"슬롯='{slot}'{'/day='+str(day) if day else ''} 에 발행할 미발행 글이 없습니다."


def main():
    ap = argparse.ArgumentParser(description="오늘살림 Threads 자동 발행기")
    ap.add_argument("--dry-run", action="store_true", help="실제 발행 없이 API 호출 미리보기")
    ap.add_argument("--all", action="store_true", help="모든 미발행 글 대상(주로 dry-run 미리보기용)")
    ap.add_argument("--due", action="store_true", help="현재 슬롯에 해당하는 글 1개 발행(크론용)")
    ap.add_argument("--id", help="특정 글 id 발행")
    ap.add_argument("--day", type=int, help="특정 day")
    ap.add_argument("--slot", help="특정 slot(아침/점심/저녁/밤)")
    args = ap.parse_args()

    posts = load_posts()
    state = load_state()
    user_id = os.environ.get("THREADS_USER_ID")
    token = os.environ.get("THREADS_ACCESS_TOKEN")

    if not args.dry_run and (not user_id or not token):
        log("환경변수 THREADS_USER_ID / THREADS_ACCESS_TOKEN 가 필요합니다. (--dry-run 은 없이도 됨)")
        sys.exit(2)

    # 대상 선정
    targets = []
    if args.all:
        targets = [p for p in posts if p["id"] not in state["posted"]]
    elif args.id:
        targets = [p for p in posts if p["id"] == args.id]
    elif args.day and args.slot:
        targets = [p for p in posts if p["day"] == args.day and p["slot"] == args.slot]
    elif args.due:
        p, err = pick_due(posts, state)
        if err:
            log(err); sys.exit(0)
        targets = [p]
    else:
        ap.print_help(); sys.exit(1)

    if not targets:
        log("대상 글이 없습니다."); sys.exit(0)

    for p in targets:
        tag = "🛒상품" if p.get("product") else "무료"
        log(f"── {p['id']} (day{p['day']} {p['slot']}, {tag}) ──")
        try:
            media_id = publish_thread(p["text"], user_id, token, dry_run=args.dry_run)
            if not args.dry_run:
                state["posted"][p["id"]] = {"media_id": media_id,
                                            "at": datetime.datetime.now().isoformat(timespec="seconds")}
                save_state(state)
        except Exception as e:
            log(f"❌ 발행 실패 {p['id']}: {e}")
            if not args.all:
                sys.exit(1)

    log(f"완료. 누적 발행 {len(state['posted'])}/{len(posts)}건.")


if __name__ == "__main__":
    main()
