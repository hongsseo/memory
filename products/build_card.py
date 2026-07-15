# -*- coding: utf-8 -*-
"""오늘살림 캐러셀 v4 — 크림 매거진(A+D 믹스, 브랜드 크림+세이지). 세로 1080x1350."""
import os, fitz
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO, MJ = "HYGothic-Medium", "HYSMyeongJo-Medium"
C=colors.HexColor
CREAM = C("#F4EEE1")   # 브랜드 크림(프로필 배경)
WHITE = C("#FCFAF3")
SAGE  = C("#5E8262")   # 브랜드 세이지(프로필 글자)
SAGED = C("#3E5B42")   # 딥 세이지
INK   = C("#2A2E26")
BODY  = C("#5A5F52")
MUTE  = C("#9A9483")
LINE  = C("#DED6C4")
W,H=1080,1350
def tw(t,f,s): return pdfmetrics.stringWidth(t,f,s)
def wrap(t,f,s,mw):
    o,cur=[],""
    for w in t.split(" "):
        if tw((cur+" "+w).strip(),f,s)<=mw: cur=(cur+" "+w).strip()
        else:
            if cur:o.append(cur)
            cur=w
    if cur:o.append(cur)
    return o
def head(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(SAGE); c.setFont(GO,30); c.drawString(80,H-100,"오늘살림")
    c.setFillColor(MUTE); c.setFont(MJ,23); c.drawRightString(W-80,H-98,"계산해주는 살림")
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,H-130,W-80,H-130)
def foot(c,pg,tot):
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,120,W-80,120)
    c.setFillColor(MUTE); c.setFont(MJ,22); c.drawString(80,80,"@today.lim")
    for i in range(tot):
        x=W-80-(tot-1-i)*30
        c.setFillColor(SAGE if i==pg-1 else LINE); c.circle(x,86,7,fill=1,stroke=0)
def cover(c,tag,l1,key,l3):
    head(c)
    c.setFillColor(SAGE); c.roundRect(80,H-250,175,58,10,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont(GO,26); c.drawCentredString(167,H-234,tag)
    y=H-390
    c.setFillColor(INK); c.setFont(GO,98); c.drawString(80,y,l1); y-=132
    kw=tw(key,GO,110)
    c.setFillColor(SAGE); c.roundRect(72,y-20,kw+36,126,12,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont(GO,110); c.drawString(90,y,key); y-=132
    c.setFillColor(INK); c.setFont(GO,98); c.drawString(80,y,l3)
    c.setFillColor(BODY); c.setFont(MJ,30); c.drawString(80,175,"넘겨서 3초 만에 확인  →")
    foot(c,1,4)
def content(c,no,h1,body,hl):
    head(c)
    c.setFillColor(SAGE); c.setFont(GO,66); c.drawString(80,H-300,no)
    c.setFillColor(LINE); c.setFont(MJ,26); c.drawString(80,H-345,"─────")
    y=H-450
    c.setFillColor(INK)
    for ln in wrap(h1,GO,60,W-160):
        c.setFont(GO,60); c.drawString(80,y,ln); y-=80
    y-=25; c.setStrokeColor(SAGE); c.setLineWidth(4); c.line(80,y,210,y); y-=70
    c.setFillColor(BODY)
    for ln in wrap(body,MJ,37,W-160):
        c.setFont(MJ,37); c.drawString(80,y,ln); y-=54
    y-=35; kw=tw(hl,GO,50)
    c.setFillColor(SAGE); c.roundRect(76,y-16,kw+34,74,10,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont(GO,50); c.drawString(93,y,hl)
    foot(c,{"01":2,"02":3}[no],4)
def cta(c):
    head(c)
    y=H-420
    c.setFillColor(INK); c.setFont(GO,74); c.drawString(80,y,"오늘 딱"); y-=118
    kw=tw("하나만",GO,104)
    c.setFillColor(SAGE); c.roundRect(72,y-20,kw+36,120,12,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont(GO,104); c.drawString(90,y,"하나만"); y-=124
    c.setFillColor(INK); c.setFont(GO,74); c.drawString(80,y,"해보세요"); y-=140
    c.setFillColor(WHITE); c.roundRect(80,y-215,W-160,250,20,fill=1,stroke=1)
    c.setStrokeColor(LINE); c.roundRect(80,y-215,W-160,250,20,fill=0,stroke=1)
    c.setFillColor(SAGED); c.setFont(GO,42); c.drawString(120,y-75,"저장 · 팔로우")
    c.setFillColor(INK); c.setFont(MJ,34); c.drawString(120,y-135,"프로필 링크 → 살림템 모음")
    c.setFillColor(MUTE); c.setFont(MJ,28); c.drawString(120,y-185,"매일 아침 새 살림팁이 올라와요")
    foot(c,4,4)
out="/home/user/memory/products/cards"; os.makedirs(out,exist_ok=True)
def render(fn,fx):
    p=f"{out}/_t.pdf"; c=canvas.Canvas(p,pagesize=(W,H)); fx(c); c.showPage(); c.save()
    d=fitz.open(p); d[0].get_pixmap(dpi=72).save(fn); d.close(); os.remove(p); print("saved",fn)
render(f"{out}/전기세_1표지.png", lambda c:cover(c,"살림팁","전기세","1년 12만원","그냥 샙니다"))
render(f"{out}/전기세_2원인.png", lambda c:content(c,"01","안 쓰는데 켜져 있어요","TV・셋톱박스・충전기는 콘센트에 꽂혀만 있어도 전기를 먹어요. 이게 '대기전력'이에요.","가구당 월 1만원"))
render(f"{out}/전기세_3해결.png", lambda c:content(c,"02","멀티탭 하나면 끝","개별 스위치 멀티탭에 꽂고, 안 쓸 땐 발로 딱 끄기. 습관 없이도 자동으로 절약돼요.","연 12만원↓"))
render(f"{out}/전기세_4CTA.png", cta)
