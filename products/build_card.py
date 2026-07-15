# -*- coding: utf-8 -*-
"""오늘살림 인스타 카드뉴스 생성 (1080x1080 PNG). reportlab→PDF→pymupdf→PNG."""
import sys, fitz
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO, MJ = "HYGothic-Medium", "HYSMyeongJo-Medium"

INK   = colors.HexColor("#22312B")
SAGE  = colors.HexColor("#6B8F71")
SAGED = colors.HexColor("#4E7A5A")
SAGEL = colors.HexColor("#E8F0EA")
CREAM = colors.HexColor("#F7F5EF")
GRAY  = colors.HexColor("#8A8A80")

S = 1080  # px = pt (render at 72dpi)

def wrap(c, text, font, size, maxw):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def make_card(num, hook, body, cta, out):
    c = canvas.Canvas(out, pagesize=(S, S))
    # 배경
    c.setFillColor(CREAM); c.rect(0, 0, S, S, fill=1, stroke=0)
    # 상단 밴드
    c.setFillColor(SAGEL); c.rect(0, S-150, S, 150, fill=1, stroke=0)
    c.setFillColor(SAGED); c.setFont(GO, 30)
    c.drawString(70, S-95, "오늘살림")
    c.setFillColor(SAGE); c.setFont(MJ, 20)
    c.drawRightString(S-70, S-95, "계산해주는 살림")
    # 번호 뱃지
    c.setFillColor(SAGE); c.circle(110, S-260, 42, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont(GO, 34)
    c.drawCentredString(110, S-273, str(num))
    # 후크 (큰 글씨)
    y = S-360
    c.setFillColor(INK)
    for ln in wrap(c, hook, GO, 58, S-140):
        c.setFont(GO, 58); c.drawString(70, y, ln); y -= 74
    # 구분선
    y -= 10
    c.setStrokeColor(SAGE); c.setLineWidth(3); c.line(70, y, 250, y); y -= 60
    # 본문
    c.setFillColor(colors.HexColor("#3C4A42"))
    for ln in wrap(c, body, MJ, 34, S-140):
        c.setFont(MJ, 34); c.drawString(70, y, ln); y -= 50
    # 하단 CTA 바
    c.setFillColor(SAGE); c.rect(0, 0, S, 130, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont(GO, 30)
    c.drawCentredString(S/2, 68, cta)
    c.setFont(MJ, 20)
    c.drawCentredString(S/2, 34, "프로필 링크 → 살림템 모음")
    c.showPage(); c.save()
    # PNG 변환
    doc = fitz.open(out.replace(".png", ".pdf") if out.endswith(".png") else out)
    return out

# 카드 데이터 (num, hook, body, cta)
CARDS = [
    (1, "이거 모르면 1년에 12만원 샙니다",
     "안 쓰는 셋톱박스・전자레인지 대기전력. 코드만 뽑아도 가구당 월 1만원 절약. '차단 멀티탭'이면 발로 끄면 끝.",
     "저장하고 오늘부터 실천하기"),
    (2, "설거지 시간 반으로 줄이는 순서",
     "유리컵 → 수저 → 그릇 → 기름기 순. 기름때를 마지막에 몰면 물・세제 낭비 없음. 물 받아 담가두기가 핵심.",
     "저장 필수 · 오늘 저녁부터"),
    (3, "냉장고 3칸으로 일주일 버티는 법",
     "냉동실 '먼저 먹기' 칸 지정 / 사기 전 사진 찍기 / 주 1회 냉파데이. 장보기 30% 줄어요.",
     "냉파 같이 할 사람 저장하기"),
]
import os
os.makedirs("/home/user/memory/products/cards", exist_ok=True)
for num, hook, body, cta in CARDS:
    pdf = f"/home/user/memory/products/cards/card{num}.pdf"
    make_card(num, hook, body, cta, pdf)
    d = fitz.open(pdf)
    pix = d[0].get_pixmap(dpi=72)
    png = f"/home/user/memory/products/cards/오늘살림_카드{num}.png"
    pix.save(png)
    d.close(); os.remove(pdf)
    print("saved", png, pix.width, "x", pix.height)
