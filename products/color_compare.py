# -*- coding: utf-8 -*-
"""크림 배경 + 강조색 4종 비교."""
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
W,H=1080,1350
def tw(t,f,s): return pdfmetrics.stringWidth(t,f,s)
out="/home/user/memory/products/cards"; os.makedirs(out,exist_ok=True)
def cover(c, ACC, ontext):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(ACC); c.setFont(GO,30); c.drawString(80,H-100,"오늘살림")
    c.setFillColor(MUTE); c.setFont(MJ,23); c.drawRightString(W-80,H-98,"계산해주는 살림")
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,H-130,W-80,H-130)
    c.setFillColor(ACC); c.roundRect(80,H-250,175,58,10,fill=1,stroke=0)
    c.setFillColor(ontext); c.setFont(GO,26); c.drawCentredString(167,H-234,"살림팁")
    y=H-390
    c.setFillColor(INK); c.setFont(GO,98); c.drawString(80,y,"전기세"); y-=132
    key="1년 12만원"; kw=tw(key,GO,110)
    c.setFillColor(ACC); c.roundRect(72,y-20,kw+36,126,12,fill=1,stroke=0)
    c.setFillColor(ontext); c.setFont(GO,110); c.drawString(90,y,key); y-=132
    c.setFillColor(INK); c.setFont(GO,98); c.drawString(80,y,"그냥 샙니다")
    c.setFillColor(BODY); c.setFont(MJ,30); c.drawString(80,175,"넘겨서 3초 만에 확인  →")
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,120,W-80,120)
    c.setFillColor(MUTE); c.setFont(MJ,22); c.drawString(80,80,"@today.lim")
    for i in range(4):
        x=W-80-(3-i)*30; c.setFillColor(ACC if i==0 else LINE); c.circle(x,86,7,fill=1,stroke=0)
def render(fn,ACC,ont):
    p=f"{out}/_t.pdf"; c=canvas.Canvas(p,pagesize=(W,H)); cover(c,ACC,ont); c.showPage(); c.save()
    d=fitz.open(p); d[0].get_pixmap(dpi=72).save(fn); d.close(); os.remove(p); print("saved",fn)
render(f"{out}/1_테라코타.png", C("#BA6A3C"), C("#FBF3E7"))   # 테라코타(따뜻)
render(f"{out}/2_머스타드.png", C("#C9971F"), C("#2A2410"))   # 머스타드(밝은)
render(f"{out}/3_코랄.png",     C("#D9725F"), C("#FBF1EC"))   # 더스티 코랄
render(f"{out}/4_네이비.png",   C("#324B6E"), C("#EAF0F6"))   # 네이비(고대비)
