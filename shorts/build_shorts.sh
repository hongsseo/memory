#!/usr/bin/env bash
# 오늘살림 숏츠 생성기 — 카드 4장(1080x1350) → 세로 숏츠(1080x1920) 무음 모션카드
# 사용: bash build_shorts.sh [출력폴더]   (기본: ./out)
set -euo pipefail
CARDS="$(cd "$(dirname "$0")/../products/cards" && pwd)"
OUT="${1:-$(dirname "$0")/out}"; mkdir -p "$OUT"
BG="0xF4EEE1"; DUR=4; XF=0.5
# 전환 오프셋: k*(DUR-XF)
o1=$(echo "$DUR-$XF"|bc); o2=$(echo "2*($DUR-$XF)"|bc); o3=$(echo "3*($DUR-$XF)"|bc)

declare -a TOPICS=("1전기세:card1" "2설거지:card2" "3냉파:card3" "4절수:card4" "5구독료:card5")
PAD="scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=$BG,setsar=1,fps=30"

for t in "${TOPICS[@]}"; do
  id="${t%%:*}"; pre="${t##*:}"
  ffmpeg -y -loglevel error \
    -loop 1 -t $DUR -i "$CARDS/${pre}-1.png" -loop 1 -t $DUR -i "$CARDS/${pre}-2.png" \
    -loop 1 -t $DUR -i "$CARDS/${pre}-3.png" -loop 1 -t $DUR -i "$CARDS/${pre}-4.png" \
    -filter_complex "[0:v]$PAD[v0];[1:v]$PAD[v1];[2:v]$PAD[v2];[3:v]$PAD[v3];\
[v0][v1]xfade=transition=fade:duration=$XF:offset=$o1[a];\
[a][v2]xfade=transition=fade:duration=$XF:offset=$o2[b];\
[b][v3]xfade=transition=fade:duration=$XF:offset=$o3[v]" \
    -map "[v]" -c:v libx264 -pix_fmt yuv420p -r 30 -movflags +faststart "$OUT/오늘살림_${id}_숏츠.mp4"
  echo "✅ $id"
done
echo "완료: $OUT"
