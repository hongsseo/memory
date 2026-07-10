# -*- coding: utf-8 -*-
"""오늘살림 무료 리드마그넷 — 30일 살림 루틴 체크리스트 (A4 인쇄용 PDF)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
GO = "HYGothic-Medium"     # 고딕(제목)
MJ = "HYSMyeongJo-Medium"  # 명조(본문)

# 팔레트
INK   = colors.HexColor("#22312B")
SAGE  = colors.HexColor("#6B8F71")
SAGEL = colors.HexColor("#E8F0EA")
CREAM = colors.HexColor("#F7F5EF")
LINE  = colors.HexColor("#D8D8CF")
GRAY  = colors.HexColor("#8A8A80")

W, H = A4
M = 16*mm

# 30일 루틴 (주차별 테마 + 하루 3개 미션)  ※ CID 폰트는 이모지 미지원 → 텍스트만 사용
WEEKS = [
    ("1주차 ・ 기초 세우기", [
        ("자기 전 싱크대 비우기", "설거지 몰아두지 않기"),
        ("식탁 위 5초 닦기", "물건 제자리 1개"),
        ("냉장고 '먼저 먹기존' 지정", "1주일치 앞칸으로"),
        ("장보기 전 3줄 메모", "있는 것・식단・필요한 것"),
        ("안 쓰는 대기전력 1개 뽑기", "월 1만원 절약 시작"),
        ("수건 1회 삶기", "쉰내 리셋"),
        ("이번 주 지출 큰 것 1개 체크", "가계부 첫 줄"),
    ]),
    ("2주차 ・ 절약 습관", [
        ("구독 서비스 1개 점검", "안 쓰면 해지"),
        ("세제・생필품 mL당 가격 비교", "다음 장보기 반영"),
        ("냉파 데이 (냉장고 파먹기)", "장보기 30%↓"),
        ("영수증 1장 훑어보기", "가장 많이 쓴 항목"),
        ("택배박스 바로 접기", "송장은 떼서 버리기"),
        ("마감 할인 시간대 장보기", "정육・반찬 반값"),
        ("이번 주 절약액 적어보기", "숫자로 확인"),
    ]),
    ("3주차 ・ 공간 정리", [
        ("서랍 1칸 비우기", "안 쓰는 것 버리기"),
        ("냉장고 유통기한 스캔", "임박한 것 오늘 요리"),
        ("욕실 물기 제거 습관", "샤워 후 스퀴지 30초"),
        ("옷장 안 입는 옷 3벌 빼기", "기부/판매 박스로"),
        ("주방 수납 라벨 붙이기", "뭐가 있는지 보이게"),
        ("현관・신발장 정리", "하루 1구역"),
        ("정리 전후 사진 찍기", "동기부여용"),
    ]),
    ("4주차 ・ 루틴 완성", [
        ("나만의 아침 살림 3개 정하기", "10분 루틴화"),
        ("주간 식단 미리 짜기", "충동구매 방지"),
        ("고정지출 리스트 만들기", "새는 돈 찾기"),
        ("살림템 1개 사진+후기 남기기", "쓰레드 소재로"),
        ("한 달 지출 결산", "가장 줄일 항목 1개"),
        ("다음 달 예산 세우기", "카테고리별"),
        ("나에게 칭찬 한마디 쓰기", "한 달 완주 축하!"),
    ]),
]

c = canvas.Canvas("/home/user/memory/products/오늘살림_가계부/오늘살림_30일_체크리스트.pdf", pagesize=A4)

def cover():
    c.setFillColor(SAGEL); c.rect(0, H-70*mm, W, 70*mm, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(GO, 30)
    c.drawCentredString(W/2, H-38*mm, "오늘살림 30일 체크리스트")
    c.setFillColor(SAGE); c.setFont(GO, 14)
    c.drawCentredString(W/2, H-48*mm, "계산해주는 살림 ・ 하루 3개씩, 한 달이면 집이 달라져요")
    # 사용법
    y = H-88*mm
    c.setFillColor(SAGE); c.rect(M, y-0.5*mm, 3.2*mm, 3.2*mm, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(GO, 13); c.drawString(M+6*mm, y, "이렇게 쓰세요")
    y -= 9*mm
    c.setFont(MJ, 11); c.setFillColor(INK)
    for line in [
        "① 하루에 딱 3개만. 다 못 해도 1개만 하면 성공이에요.",
        "② 한 칸씩 체크하며 채워보세요. 눈에 보이면 계속하게 돼요.",
        "③ 4주 뒤, 절약된 돈과 정리된 집이 남습니다.",
    ]:
        c.drawString(M+2*mm, y, line); y -= 7.5*mm
    # 팁 박스
    y -= 3*mm
    c.setFillColor(CREAM); c.roundRect(M, y-16*mm, W-2*M, 16*mm, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(LINE); c.roundRect(M, y-16*mm, W-2*M, 16*mm, 3*mm, fill=0, stroke=1)
    c.setFillColor(SAGE); c.setFont(GO, 9); c.drawString(M+5*mm, y-6.5*mm, "TIP")
    c.setFillColor(INK); c.setFont(MJ, 11)
    c.drawString(M+15*mm, y-7*mm,  "완벽하게 하려다 지치지 마세요. '오늘 1개'가 30일이면 30개예요.")
    c.drawString(M+15*mm, y-13*mm, "더 확실한 절약은 「오늘살림 가계부 템플릿」으로 이어가세요.")
    # 진행바 안내
    y -= 26*mm
    c.setFillColor(INK); c.setFont(GO, 12); c.drawString(M, y, "나의 30일 진행")
    y -= 8*mm
    box = (W-2*M)/30
    for i in range(30):
        c.setStrokeColor(LINE); c.setFillColor(colors.white)
        c.rect(M+i*box, y-box, box-1.2, box-1.2, fill=1, stroke=1)
        c.setFillColor(GRAY); c.setFont(MJ, 6)
        c.drawCentredString(M+i*box+(box-1.2)/2, y-box+ (box-1.2)/2 -2, str(i+1))
    c.setFont(MJ, 9); c.setFillColor(GRAY)
    c.drawString(M, y-box-6*mm, "한 칸이 하루예요. 해낸 날은 칠하세요.")
    footer()
    c.showPage()

def footer():
    c.setStrokeColor(LINE); c.line(M, 15*mm, W-M, 15*mm)
    c.setFillColor(GRAY); c.setFont(MJ, 8)
    c.drawString(M, 10*mm, "오늘살림 ・ 계산해주는 살림")
    c.drawRightString(W-M, 10*mm, "무료 배포용 ・ 개인 사용 ・ 재판매 금지")

def checkbox(x, y, s=4.6*mm):
    c.setStrokeColor(SAGE); c.setLineWidth(1); c.rect(x, y, s, s, fill=0, stroke=1)

def week_page(idx, title, days):
    # 헤더 밴드
    c.setFillColor(SAGE); c.rect(0, H-24*mm, W, 24*mm, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont(GO, 18)
    c.drawString(M, H-16*mm, title)
    c.setFont(MJ, 10)
    c.drawRightString(W-M, H-16*mm, f"{idx*7-6}~{idx*7}일차")
    y = H-36*mm
    rowh = 21*mm
    for di, (task, sub) in enumerate(days):
        day_no = (idx-1)*7 + di + 1
        # 행 배경
        c.setFillColor(CREAM if di % 2 == 0 else colors.white)
        c.roundRect(M, y-rowh+4*mm, W-2*M, rowh-3*mm, 2*mm, fill=1, stroke=0)
        # Day 뱃지
        c.setFillColor(SAGEL); c.roundRect(M+3*mm, y-rowh+7*mm, 16*mm, rowh-9*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(SAGE); c.setFont(GO, 9)
        c.drawCentredString(M+11*mm, y-8*mm, "DAY")
        c.setFont(GO, 15); c.drawCentredString(M+11*mm, y-14*mm, str(day_no))
        # 미션 텍스트
        c.setFillColor(INK); c.setFont(GO, 12.5)
        c.drawString(M+24*mm, y-9*mm, task)
        c.setFillColor(GRAY); c.setFont(MJ, 10)
        c.drawString(M+24*mm, y-15*mm, "・ " + sub)
        # 체크박스
        checkbox(W-M-9*mm, y-13*mm)
        y -= rowh
    footer()
    c.showPage()

cover()
for i,(title,days) in enumerate(WEEKS, start=1):
    week_page(i, title, days)

# 마지막장: 다음 단계(업셀)
c.setFillColor(SAGEL); c.rect(0, H-70*mm, W, 70*mm, fill=1, stroke=0)
c.setFillColor(INK); c.setFont(GO, 24)
c.drawCentredString(W/2, H-40*mm, "30일, 정말 고생했어요")
c.setFillColor(SAGE); c.setFont(MJ, 13)
c.drawCentredString(W/2, H-50*mm, "이제 '숫자로' 살림을 관리할 차례예요.")
y = H-90*mm
c.setFillColor(INK); c.setFont(GO, 14); c.drawString(M, y, "다음 단계")
y -= 11*mm
c.setFont(MJ, 11)
bullets = [
    ["「오늘살림 가계부 템플릿」 — 카테고리별 예산을 정하면 지출・절약액을",
     "자동으로 계산해주는 엑셀. 이 체크리스트에서 익힌 습관을 '돈'으로 연결해요."],
    ["매일 아침 07:30, 오늘살림 쓰레드에서 새 팁을 받아보세요."],
]
for lines in bullets:
    c.setFillColor(SAGE); c.rect(M, y-0.3*mm, 2.8*mm, 2.8*mm, fill=1, stroke=0)
    c.setFillColor(INK)
    for k, ln in enumerate(lines):
        c.drawString(M+6*mm, y - k*6.5*mm, ln)
    y -= 6.5*mm*len(lines) + 3*mm
footer()
c.showPage()
c.save()
print("saved: 오늘살림_30일_체크리스트.pdf")
