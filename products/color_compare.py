# -*- coding: utf-8 -*-
"""크림 배경 + 2색 조합 여러 개 비교."""
import os, fitz
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO,MJ="HYGothic-Medium","HYSMyeongJo-Medium"
C=colors.HexColor
CREAM=C("#F4EEE1"); INK=C("#2A2E26"); MUTE=C("#9A9483"); LINE=C("#DED6C4"); BODY=C("#5A5F52")
LT=C("#FBF3E7")  # 박스 위 밝은 글씨
W,H=1080,1350
def tw(t,f,s): return pdfmetrics.stringWidth(t,f,s)
out="/home/user/memory/products/cards"; os.makedirs(out,exist_ok=True)
def cover(c, BRAND, TAGBG, TAGT, BOXBG, BOXT, DOT):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(BRAND); c.setFont(GO,30); c.drawString(80,H-100,"오늘살림")
    c.setFillColor(MUTE); c.setFont(MJ,23); c.drawRightString(W-80,H-98,"계산해주는 살림")
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,H-130,W-80,H-130)
    c.setFillColor(TAGBG); c.roundRect(80,H-250,175,58,10,fill=1,stroke=0)
    c.setFillColor(TAGT); c.setFont(GO,26); c.drawCentredString(167,H-234,"살림팁")
    y=H-390
    c.setFillColor(INK); c.setFont(GO,98); c.drawString(80,y,"전기세"); y-=132
    key="1년 12만원"; kw=tw(key,GO,110)
    c.setFillColor(BOXBG); c.roundRect(72,y-20,kw+36,126,12,fill=1,stroke=0)
    c.setFillColor(BOXT); c.setFont(GO,110); c.drawString(90,y,key); y-=132
    c.setFillColor(INK); c.setFont(GO,98); c.drawString(80,y,"그냥 샙니다")
    c.setFillColor(BODY); c.setFont(MJ,30); c.drawString(80,175,"넘겨서 3초 만에 확인  →")
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,120,W-80,120)
    c.setFillColor(MUTE); c.setFont(MJ,22); c.drawString(80,80,"@today.lim")
    for i in range(4):
        x=W-80-(3-i)*30; c.setFillColor(DOT if i==0 else LINE); c.circle(x,86,7,fill=1,stroke=0)
def render(fn,*a):
    p=f"{out}/_t.pdf"; c=canvas.Canvas(p,pagesize=(W,H)); cover(c,*a); c.showPage(); c.save()
    d=fitz.open(p); d[0].get_pixmap(dpi=72).save(fn); d.close(); os.remove(p); print("saved",fn)

TERRA=C("#BA6A3C"); MUST=C("#CB9A22"); NAVY=C("#324B6E"); FOREST=C("#3F6146")
BURG=C("#8B3A46"); TEAL=C("#2E6E6A"); CORAL=C("#D9725F"); PLUM=C("#6E4A6B")

# (파일, BRAND, TAGBG, TAGT, BOXBG, BOXT, DOT)
render(f"{out}/1_테라x머스타드.png", TERRA, MUST, C("#2A2410"), TERRA, LT, TERRA)
render(f"{out}/2_네이비x머스타드.png", NAVY, MUST, C("#2A2410"), NAVY, LT, NAVY)
render(f"{out}/3_포레스트x테라.png", FOREST, TERRA, LT, FOREST, LT, FOREST)
render(f"{out}/4_버건디x머스타드.png", BURG, MUST, C("#2A2410"), BURG, LT, BURG)
render(f"{out}/5_틸x코랄.png", TEAL, CORAL, LT, TEAL, LT, TEAL)
render(f"{out}/6_플럼x머스타드.png", PLUM, MUST, C("#2A2410"), PLUM, LT, PLUM)
