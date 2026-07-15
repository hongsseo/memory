# -*- coding: utf-8 -*-
"""오늘살림 인스타 카드 v2 — 스크롤 멈추는 디자인. reportlab→PNG."""
import os, fitz
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO, MJ = "HYGothic-Medium", "HYSMyeongJo-Medium"

INK  = colors.HexColor("#1F2A24")
SAGE = colors.HexColor("#5E8468")
SAGED= colors.HexColor("#3D5C48")
SAGEL= colors.HexColor("#E8F0EA")
CREAM= colors.HexColor("#F8F6F0")
WHITE= colors.white
GOLD = colors.HexColor("#C8792E")
BODY = colors.HexColor("#41504A")
LINE = colors.HexColor("#DCDCD2")
S = 1080

def tw(t, f, s): return pdfmetrics.stringWidth(t, f, s)

def make(num, pre, key, post, points, cta, out):
    c = canvas.Canvas(out, pagesize=(S, S))
    c.setFillColor(CREAM); c.rect(0, 0, S, S, fill=1, stroke=0)
    c.setFillColor(SAGED); c.rect(0, S-140, S, 140, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(GO, 34); c.drawString(70, S-90, "오늘살림")
    c.setFillColor(SAGEL); c.setFont(MJ, 21); c.drawRightString(S-70, S-88, "계산해주는 살림")
    c.setFillColor(GOLD); c.roundRect(70, S-240, 155, 62, 31, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(GO, 26); c.drawCentredString(147, S-224, "살림팁 %d" % num)
    y = S-330
    c.setFillColor(INK); c.setFont(GO, 66); c.drawString(70, y, pre); y -= 92
    kw = tw(key, GO, 78)
    c.setFillColor(GOLD); c.roundRect(64, y-16, kw+28, 92, 12, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(GO, 78); c.drawString(78, y, key); y -= 92
    c.setFillColor(INK); c.setFont(GO, 66); c.drawString(70, y, post)
    box_top = y - 55
    ph = 60*len(points) + 70
    c.setFillColor(WHITE); c.roundRect(60, box_top-ph, S-120, ph, 24, fill=1, stroke=0)
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.roundRect(60, box_top-ph, S-120, ph, 24, fill=0, stroke=1)
    py = box_top - 55
    for p in points:
        c.setStrokeColor(SAGE); c.setLineWidth(5)
        c.line(100, py+8, 112, py-4); c.line(112, py-4, 134, py+22)
        c.setFillColor(BODY); c.setFont(MJ, 33); c.drawString(155, py, p); py -= 60
    c.setFillColor(SAGE); c.rect(0, 0, S, 150, fill=1, stroke=0)
    c.setFillColor(WHITE); c.rect(78, 52, 40, 52, fill=1, stroke=0)
    pth=c.beginPath(); pth.moveTo(78,52); pth.lineTo(98,70); pth.lineTo(118,52); pth.close()
    c.setFillColor(SAGE); c.drawPath(pth, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(GO, 38); c.drawString(140, 78, cta)
    c.setFillColor(SAGEL); c.setFont(MJ, 23); c.drawString(140, 42, "프로필 링크 → 살림템 모음에서 확인")
    c.showPage(); c.save()

CARDS = [
 (1,"이거 모르면","1년에 12만원","그냥 샙니다",
  ["안 쓰는 셋톱박스・전자레인지 대기전력","코드만 뽑아도 가구당 월 1만원 절약","'차단 멀티탭'이면 발로 끄면 끝"],
  "저장하고 오늘부터"),
 (2,"설거지 시간","반으로","줄이는 순서",
  ["유리컵 → 수저 → 그릇 → 기름기 순서로","기름때 마지막에 몰면 물・세제 절약","물 받아 '담가두기'가 핵심"],
  "저장 필수, 오늘 저녁부터"),
 (3,"냉장고 3칸으로","일주일","버티는 법",
  ["냉동실 '먼저 먹기' 칸 지정하기","장보기 전 냉장고 사진 찍기","주 1회 '냉파데이' → 장보기 30% 감소"],
  "냉파 같이 할 사람 저장"),
]
os.makedirs("/home/user/memory/products/cards", exist_ok=True)
for num,pre,key,post,pts,cta in CARDS:
    pdf="/home/user/memory/products/cards/_c%d.pdf"%num
    make(num,pre,key,post,pts,cta,pdf)
    d=fitz.open(pdf); pix=d[0].get_pixmap(dpi=72)
    png="/home/user/memory/products/cards/오늘살림_카드%d.png"%num
    pix.save(png); d.close(); os.remove(pdf); print("saved",png)
