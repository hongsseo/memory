# -*- coding: utf-8 -*-
"""오늘살림 인스타 캐러셀 v3 — 볼드 임팩트(검정+네온), 세로 1080x1350."""
import os, fitz
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO, MJ = "HYGothic-Medium", "HYSMyeongJo-Medium"

BG    = colors.HexColor("#171A18")   # 차콜 블랙
CARD  = colors.HexColor("#21251F")
NEON  = colors.HexColor("#C8F03C")   # 네온 라임
NEOND = colors.HexColor("#1A1D14")   # 네온 위 글씨(어둡게)
WHITE = colors.HexColor("#F4F6F1")
MUTE  = colors.HexColor("#9BA69A")
W, H = 1080, 1350

def tw(t,f,s): return pdfmetrics.stringWidth(t,f,s)
def wrap(t,f,s,mw):
    out,cur=[],""
    for w in t.split(" "):
        if tw((cur+" "+w).strip(),f,s)<=mw: cur=(cur+" "+w).strip()
        else:
            if cur: out.append(cur)
            cur=w
    if cur: out.append(cur)
    return out

def base(c):
    c.setFillColor(BG); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(NEON); c.setFont(GO,30); c.drawString(70,H-95,"오늘살림")
    c.setFillColor(MUTE); c.setFont(MJ,22); c.drawRightString(W-70,H-93,"계산해주는 살림")
    c.setStrokeColor(CARD); c.setLineWidth(2); c.line(70,H-125,W-70,H-125)

def footer(c, page, total):
    c.setFillColor(MUTE); c.setFont(MJ,20)
    c.drawString(70,55,"@today.lim")
    # 페이지 도트
    for i in range(total):
        x=W-70-(total-1-i)*30
        c.setFillColor(NEON if i==page-1 else CARD); c.circle(x,62,7,fill=1,stroke=0)

def cover(c, tag, l1, key, l3, bottom):
    base(c)
    # 태그
    c.setFillColor(NEON); c.roundRect(70,H-235,190,60,30,fill=1,stroke=0)
    c.setFillColor(NEOND); c.setFont(GO,26); c.drawCentredString(165,H-219,tag)
    y=H-380
    c.setFillColor(WHITE); c.setFont(GO,96); c.drawString(70,y,l1); y-=130
    kw=tw(key,GO,112)
    c.setFillColor(NEON); c.roundRect(60,y-22,kw+40,132,14,fill=1,stroke=0)
    c.setFillColor(NEOND); c.setFont(GO,112); c.drawString(80,y,key); y-=132
    c.setFillColor(WHITE); c.setFont(GO,96); c.drawString(70,y,l3)
    # 하단 저장 유도
    c.setFillColor(NEON); c.setFont(GO,34); c.drawString(70,180,bottom)
    c.setFillColor(MUTE); c.setFont(MJ,26); c.drawString(70,132,"넘겨서 3초 만에 확인  →")
    footer(c,1,4)

def content(c, no, head, body, hl=None):
    base(c)
    c.setFillColor(NEON); c.setFont(GO,72); c.drawString(70,H-320,no)
    y=H-430
    c.setFillColor(WHITE)
    for ln in wrap(head,GO,62,W-140):
        c.setFont(GO,62); c.drawString(70,y,ln); y-=82
    y-=30
    c.setStrokeColor(NEON); c.setLineWidth(4); c.line(70,y,190,y); y-=70
    c.setFillColor(MUTE)
    for ln in wrap(body,MJ,38,W-140):
        c.setFont(MJ,38); c.drawString(70,y,ln); y-=56
    if hl:
        y-=30
        kw=tw(hl,GO,54)
        c.setFillColor(NEON); c.roundRect(66,y-18,kw+36,80,12,fill=1,stroke=0)
        c.setFillColor(NEOND); c.setFont(GO,54); c.drawString(84,y,hl)
    footer(c,no_i(no),4)

def no_i(no): return {"01":2,"02":3}.get(no,2)

def cta(c):
    base(c)
    y=H-430
    c.setFillColor(WHITE); c.setFont(GO,76); c.drawString(70,y,"오늘 딱"); y-=128
    kw=tw("하나만",GO,110)
    c.setFillColor(NEON); c.roundRect(60,y-22,kw+40,128,14,fill=1,stroke=0)
    c.setFillColor(NEOND); c.setFont(GO,110); c.drawString(80,y,"하나만"); y-=128
    c.setFillColor(WHITE); c.setFont(GO,76); c.drawString(70,y,"해보세요"); y-=150
    # 저장/팔로우 박스
    c.setFillColor(CARD); c.roundRect(60,y-210,W-120,250,20,fill=1,stroke=0)
    c.setFillColor(NEON); c.setFont(GO,40); c.drawString(100,y-70,"저장 · 팔로우")
    c.setFillColor(WHITE); c.setFont(MJ,34); c.drawString(100,y-130,"프로필 링크 → 살림템 모음")
    c.setFillColor(MUTE); c.setFont(MJ,28); c.drawString(100,y-180,"매일 아침 새 살림팁 올라와요")
    footer(c,4,4)

# ── 전기세 캐러셀
out="/home/user/memory/products/cards"
os.makedirs(out,exist_ok=True)
def render(fn, drawfn):
    pdf=f"{out}/_t.pdf"; c=canvas.Canvas(pdf,pagesize=(W,H)); drawfn(c); c.showPage(); c.save()
    d=fitz.open(pdf); d[0].get_pixmap(dpi=72).save(fn); d.close(); os.remove(pdf); print("saved",fn)

render(f"{out}/전기세_1표지.png", lambda c: cover(c,"살림팁","전기세","1년 12만원","그냥 샙니다","저장하고 오늘부터 막기"))
render(f"{out}/전기세_2원인.png", lambda c: content(c,"01","안 쓰는데 켜져 있어요","TV·셋톱박스·충전기는 콘센트에 꽂혀만 있어도 전기를 먹어요. 이게 '대기전력'.","가구당 월 1만원"))
render(f"{out}/전기세_3해결.png", lambda c: content(c,"02","멀티탭 하나면 끝","개별 스위치 멀티탭에 꽂고, 안 쓸 땐 발로 딱 끄기. 습관 없이도 자동 절약.","연 12만원↓"))
render(f"{out}/전기세_4CTA.png", cta)
