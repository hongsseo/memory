# -*- coding: utf-8 -*-
"""전기세 표지 4스타일 비교 (세로 1080x1350)."""
import os, fitz
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO, MJ = "HYGothic-Medium", "HYSMyeongJo-Medium"
W,H=1080,1350
C=colors.HexColor
def tw(t,f,s): return pdfmetrics.stringWidth(t,f,s)
out="/home/user/memory/products/cards"; os.makedirs(out,exist_ok=True)
def render(fn,fn2):
    pdf=f"{out}/_t.pdf"; c=canvas.Canvas(pdf,pagesize=(W,H)); fn2(c); c.showPage(); c.save()
    d=fitz.open(pdf); d[0].get_pixmap(dpi=72).save(fn); d.close(); os.remove(pdf); print("saved",fn)

# A) 크림 미니멀 — 명조, 여백, 톤다운. 프리미엄/에디토리얼
def styleA(c):
    c.setFillColor(C("#F3EEE3")); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(C("#7C8B6F")); c.setFont(MJ,26); c.drawString(80,H-130,"오늘살림  ·  계산해주는 살림")
    c.setStrokeColor(C("#D8CFBE")); c.setLineWidth(1.5); c.line(80,H-160,W-80,H-160)
    c.setFillColor(C("#4A5240")); c.setFont(MJ,24); c.drawString(80,H-260,"S A V I N G  N O T E")
    y=H-380
    c.setFillColor(C("#2B2E26")); c.setFont(MJ,84)
    c.drawString(80,y,"전기세, 이게"); y-=118
    c.setFillColor(C("#B4703A")); c.setFont(MJ,110)
    c.drawString(80,y,"1년 12만원"); y-=118
    c.setFillColor(C("#2B2E26")); c.setFont(MJ,84)
    c.drawString(80,y,"새고 있었어요")
    c.setStrokeColor(C("#B4703A")); c.setLineWidth(3); c.line(80,y-70,220,y-70)
    c.setFillColor(C("#8A8674")); c.setFont(MJ,30); c.drawString(80,200,"넘겨서 확인하기  →")

# B) 머스타드 컬러팝 — 밝은 배경 단색, 검정 고딕, 발랄
def styleB(c):
    c.setFillColor(C("#F2C230")); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(C("#1A1A1A")); c.setFont(GO,30); c.drawString(80,H-120,"오늘살림")
    c.setFillColor(C("#5A4A00")); c.setFont(MJ,24); c.drawRightString(W-80,H-118,"계산해주는 살림")
    y=H-360
    c.setFillColor(C("#1A1A1A")); c.setFont(GO,100); c.drawString(80,y,"전기세"); y-=140
    # 밑줄 강조
    key="1년 12만원"; c.setFont(GO,116); kw=tw(key,GO,116)
    c.drawString(80,y,key)
    c.setStrokeColor(C("#E5453A")); c.setLineWidth(16); c.line(80,y-14,80+kw,y-14); y-=142
    c.setFillColor(C("#1A1A1A")); c.setFont(GO,100); c.drawString(80,y,"그냥 샙니다")
    c.setFillColor(C("#1A1A1A")); c.setFont(GO,36); c.drawString(80,200,"저장 필수  |  넘겨보기 →")

# C) 파스텔 소프트 — 민트 배경, 둥근 필, 부드러움
def styleC(c):
    c.setFillColor(C("#DCEEE4")); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(C("#FFFFFF")); c.roundRect(60,150,W-120,H-320,40,fill=1,stroke=0)
    c.setFillColor(C("#4E7A5A")); c.setFont(GO,28); c.drawCentredString(W/2,H-250,"오늘의 살림 한 스푼")
    y=H-420
    c.setFillColor(C("#33413A")); c.setFont(GO,78)
    c.drawCentredString(W/2,y,"전기세 이거"); y-=118
    key="1년 12만원"; kw=tw(key,GO,86)
    c.setFillColor(C("#F6C7BC")); c.roundRect(W/2-kw/2-30,y-24,kw+60,116,58,fill=1,stroke=0)
    c.setFillColor(C("#9C4A2E")); c.setFont(GO,86); c.drawCentredString(W/2,y,key); y-=126
    c.setFillColor(C("#33413A")); c.setFont(GO,78); c.drawCentredString(W/2,y,"새고 있었어요")
    c.setFillColor(C("#7FA98C")); c.setFont(MJ,30); c.drawCentredString(W/2,250,"저장하고 하나씩 따라해요  ♡")

# D) 화이트 매거진 — 흰 배경, 초대형 고딕, 레드 포인트 바
def styleD(c):
    c.setFillColor(C("#FFFFFF")); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(C("#E5453A")); c.rect(0,H-14,W,14,fill=1,stroke=0)
    c.setFillColor(C("#111111")); c.setFont(GO,30); c.drawString(80,H-110,"오늘살림")
    c.setFillColor(C("#999999")); c.setFont(MJ,24); c.drawRightString(W-80,H-108,"계산해주는 살림")
    c.setFillColor(C("#E5453A")); c.roundRect(80,H-230,170,58,8,fill=1,stroke=0)
    c.setFillColor(C("#FFFFFF")); c.setFont(GO,26); c.drawCentredString(165,H-214,"살림팁")
    y=H-370
    c.setFillColor(C("#111111")); c.setFont(GO,104); c.drawString(80,y,"전기세"); y-=142
    c.setFillColor(C("#E5453A")); c.setFont(GO,120); c.drawString(80,y,"1년 12만원"); y-=140
    c.setFillColor(C("#111111")); c.setFont(GO,104); c.drawString(80,y,"샙니다")
    c.setFillColor(C("#666666")); c.setFont(MJ,30); c.drawString(80,190,"→ 넘겨서 3초 만에 확인")

render(f"{out}/A_크림미니멀.png",styleA)
render(f"{out}/B_머스타드팝.png",styleB)
render(f"{out}/C_파스텔소프트.png",styleC)
render(f"{out}/D_화이트매거진.png",styleD)
