# -*- coding: utf-8 -*-
"""오늘살림 1주차 캐러셀 5종 일괄 생성."""
import os, fitz
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO,MJ="HYGothic-Medium","HYSMyeongJo-Medium"
C=colors.HexColor
CREAM=C("#F4EEE1"); WHITE=C("#FCFAF3"); INK=C("#2A2E26"); BODY=C("#5A5F52")
MUTE=C("#9A9483"); LINE=C("#DED6C4"); LT=C("#FBF3E7"); MUST=C("#CB9A22"); MUSTT=C("#2A2410")
PALETTE={"절약":C("#324B6E"),"냉파":C("#3F6146"),"청소":C("#BA6A3C"),"살림템":C("#CB9A22"),"공감":C("#8B3A46")}
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
def head(c,A):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(A); c.setFont(GO,30); c.drawString(80,H-100,"오늘살림")
    c.setFillColor(MUTE); c.setFont(MJ,23); c.drawRightString(W-80,H-98,"계산해주는 살림")
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,H-130,W-80,H-130)
def foot(c,pg,A):
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(80,120,W-80,120)
    c.setFillColor(MUTE); c.setFont(MJ,22); c.drawString(80,80,"@today.lim")
    for i in range(4):
        x=W-80-(3-i)*30; c.setFillColor(A if i==pg-1 else LINE); c.circle(x,86,7,fill=1,stroke=0)
def cover(c,A,tag,l1,key,l3):
    head(c,A)
    c.setFillColor(MUST); tw_=tw(tag,GO,26); c.roundRect(80,H-250,tw_+70,58,10,fill=1,stroke=0)
    c.setFillColor(MUSTT); c.setFont(GO,26); c.drawCentredString(80+(tw_+70)/2,H-234,tag)
    y=H-390
    c.setFillColor(INK); c.setFont(GO,92); c.drawString(80,y,l1); y-=126
    kw=tw(key,GO,104)
    c.setFillColor(A); c.roundRect(72,y-20,kw+36,120,12,fill=1,stroke=0)
    c.setFillColor(LT); c.setFont(GO,104); c.drawString(90,y,key); y-=126
    c.setFillColor(INK); c.setFont(GO,92); c.drawString(80,y,l3)
    c.setFillColor(BODY); c.setFont(MJ,30); c.drawString(80,175,"넘겨서 3초 만에 확인  →")
    foot(c,1,A)
def content(c,A,no,h1,body,hl):
    head(c,A)
    c.setFillColor(A); c.setFont(GO,66); c.drawString(80,H-300,no)
    c.setFillColor(LINE); c.setFont(MJ,26); c.drawString(80,H-345,"─────")
    y=H-450
    c.setFillColor(INK)
    for ln in wrap(h1,GO,58,W-160):
        c.setFont(GO,58); c.drawString(80,y,ln); y-=78
    y-=25; c.setStrokeColor(A); c.setLineWidth(4); c.line(80,y,210,y); y-=70
    c.setFillColor(BODY)
    for ln in wrap(body,MJ,37,W-160):
        c.setFont(MJ,37); c.drawString(80,y,ln); y-=54
    y-=35; kw=tw(hl,GO,50)
    c.setFillColor(A); c.roundRect(76,y-16,kw+34,74,10,fill=1,stroke=0)
    c.setFillColor(LT); c.setFont(GO,50); c.drawString(93,y,hl)
    foot(c,{"01":2,"02":3}[no],A)
def cta(c,A,last):
    head(c,A)
    y=H-420
    c.setFillColor(INK); c.setFont(GO,74); c.drawString(80,y,"오늘 딱"); y-=118
    kw=tw("하나만",GO,104)
    c.setFillColor(A); c.roundRect(72,y-20,kw+36,120,12,fill=1,stroke=0)
    c.setFillColor(LT); c.setFont(GO,104); c.drawString(90,y,"하나만"); y-=124
    c.setFillColor(INK); c.setFont(GO,74); c.drawString(80,y,"해보세요"); y-=140
    c.setFillColor(WHITE); c.roundRect(80,y-215,W-160,250,20,fill=1,stroke=1)
    c.setStrokeColor(LINE); c.roundRect(80,y-215,W-160,250,20,fill=0,stroke=1)
    c.setFillColor(A); c.setFont(GO,42); c.drawString(120,y-75,"저장 · 팔로우")
    c.setFillColor(INK); c.setFont(MJ,34); c.drawString(120,y-135,last)
    c.setFillColor(MUTE); c.setFont(MJ,28); c.drawString(120,y-185,"매일 아침 새 살림팁이 올라와요")
    foot(c,4,A)
out="/home/user/memory/products/cards"; os.makedirs(out,exist_ok=True)
def render(fn,fx):
    p=f"{out}/_t.pdf"; c=canvas.Canvas(p,pagesize=(W,H)); fx(c); c.showPage(); c.save()
    d=fitz.open(p); d[0].get_pixmap(dpi=72).save(fn); d.close(); os.remove(p)

CAR=[
 dict(n="1전기세",p="절약",tag="살림팁",cov=("전기세","1년 12만원","그냥 샙니다"),
   s1=("01","안 쓰는데 켜져 있어요","TV・셋톱박스・충전기는 콘센트에 꽂혀만 있어도 전기를 먹어요. 이게 '대기전력'이에요.","가구당 월 1만원"),
   s2=("02","멀티탭 하나면 끝","개별 스위치 멀티탭에 꽂고 안 쓸 땐 발로 딱 끄기. 습관 없이도 자동 절약.","연 12만원↓"),
   last="프로필 링크 → 살림템 모음"),
 dict(n="2설거지",p="청소",tag="살림팁",cov=("설거지 시간","반으로","줄이는 순서"),
   s1=("01","순서만 바꾸면 돼요","유리컵 → 수저 → 그릇 → 기름기 순. 깨끗한 것부터 씻어야 물・세제가 안 낭비돼요.","물・세제 절약"),
   s2=("02","기름때는 담가두기","기름 팬은 물 받아 담가두면 저절로 불어서 쓱. 문지를 필요가 없어요.","시간 절반↓"),
   last="프로필 링크 → 살림템 모음"),
 dict(n="3냉파",p="냉파",tag="냉파",cov=("냉장고 3칸으로","일주일","버티는 법"),
   s1=("01","'먼저 먹기' 칸 지정","냉동실 한 칸을 '이번 주 먹을 것'으로. 유통기한 임박한 것부터 넣어요.","버리는 돈↓"),
   s2=("02","사기 전 사진 한 장","장보기 전 냉장고 사진 찍기. 있는 걸 또 사는 중복 구매가 사라져요.","장보기 30%↓"),
   last="프로필 링크 → 살림템 모음"),
 dict(n="4절수",p="살림템",tag="살림템",cov=("샤워기만 바꿔도","수도세 30%","줄어요"),
   s1=("01","물을 이렇게 아껴요","절수 샤워헤드는 공기를 섞어 수압은 그대로, 물량만 줄여줘요. 체감 차이 없이 절약.","최대 30%↓"),
   s2=("02","설치는 딱 10초","기존 헤드 돌려 빼고 끼우면 끝. 3천원대인데 몇 달이면 본전 뽑아요.","3천원대"),
   last="프로필 링크 → 살림템 모음"),
 dict(n="5구독료",p="절약",tag="살림팁",cov=("안 보는 구독료","1년 36만원","새고 있어요"),
   s1=("01","나도 모르게 빠져나가요","안 보는 OTT・안 듣는 음원・중복 클라우드. 월 3만원이면 1년에 36만원.","월 3만원"),
   s2=("02","종료일만 적어두세요","무료체험 종료일을 캘린더에 메모. 자동결제 방어가 이걸로 끝나요.","연 36만원↓"),
   last="프로필 링크 → 살림템 모음"),
]
for car in CAR:
    A=PALETTE[car["p"]]; n=car["n"]
    render(f"{out}/{n}_1표지.png", lambda c,A=A,car=car: cover(c,A,car["tag"],*car["cov"]))
    render(f"{out}/{n}_2.png",     lambda c,A=A,car=car: content(c,A,*car["s1"]))
    render(f"{out}/{n}_3.png",     lambda c,A=A,car=car: content(c,A,*car["s2"]))
    render(f"{out}/{n}_4CTA.png",  lambda c,A=A,car=car: cta(c,A,car["last"]))
    print("done",n)
