# -*- coding: utf-8 -*-
"""테라코타+머스타드 조합 2안."""
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
TERRA=C("#BA6A3C"); TERRAT=C("#FBF3E7")
MUST=C("#CB9A22");  MUSTT=C("#2A2410")
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
# A: 테라코타 메인(박스·브랜드) + 머스타드 서브(태그)
render(f"{out}/A_테라메인.png", TERRA, MUST, MUSTT, TERRA, TERRAT, TERRA)
# B: 머스타드 메인(박스) + 테라코타 서브(태그·브랜드)
render(f"{out}/B_머스타드메인.png", TERRA, TERRA, TERRAT, MUST, MUSTT, MUST)
