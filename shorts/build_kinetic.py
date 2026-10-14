# -*- coding: utf-8 -*-
"""
오늘살림 상황극 숏츠 생성기 (키네틱 타이포 + 효과음)
skits.json을 읽어 각 상황극을 1080x1920 세로 숏츠(mp4)로 렌더링.
- 폰트 없으면 자동 다운로드(Google Fonts, OFL 무료)
- 비트별 pop/slideup/shake 애니 + pop/boing/ding 효과음
- product=true면 쿠팡파트너스 고지 인트로 자동 삽입
사용: python3 build_kinetic.py [출력폴더]   (기본 ./out)
"""
import os, sys, json, math, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FD   = os.path.join(HERE, "fonts"); os.makedirs(FD, exist_ok=True)
OUT  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
TMP  = os.path.join(HERE, ".tmp_frames"); os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 30

FONT_URLS = {
    "BlackHanSans-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/blackhansans/BlackHanSans-Regular.ttf",
    "Jua-Regular.ttf":          "https://raw.githubusercontent.com/google/fonts/main/ofl/jua/Jua-Regular.ttf",
    "DoHyeon-Regular.ttf":      "https://raw.githubusercontent.com/google/fonts/main/ofl/dohyeon/DoHyeon-Regular.ttf",
    "Gaegu-Bold.ttf":           "https://raw.githubusercontent.com/google/fonts/main/ofl/gaegu/Gaegu-Bold.ttf",
}
def ensure_fonts():
    for name, url in FONT_URLS.items():
        p = os.path.join(FD, name)
        if not os.path.exists(p) or os.path.getsize(p) < 10000:
            print("  폰트 다운로드:", name)
            urllib.request.urlretrieve(url, p)
ensure_fonts()

from PIL import Image, ImageDraw, ImageFont
FONTS = {"BLACK":"BlackHanSans-Regular.ttf","JUA":"Jua-Regular.ttf","DOH":"DoHyeon-Regular.ttf","GAEGU":"Gaegu-Bold.ttf"}
COLORS = {"CREAM":"#F4EEE1","NAVY":"#243B63","RED":"#E23B3B","YEL":"#FFC83D","GREEN":"#2E8B57",
          "INK":"#2B2B2B","WHITE":"#FFFFFF","GRAY":"#9A9A9A","BLUE_LT":"#ABC4E8"}
_fc = {}
def font(code, size):
    k=(code,size)
    if k not in _fc: _fc[k]=ImageFont.truetype(os.path.join(FD,FONTS[code]),size)
    return _fc[k]

DISCLOSURE_BEAT = {"dur":2.0,"bg":"GRAY","anim":"pop","sfx":"pop_soft",
    "lines":[["쿠팡파트너스 활동으로","JUA",56,"WHITE"],["수수료를 받을 수 있어요","JUA",56,"WHITE"]]}

def block_img(lines):
    pad, gap = 60, 26
    specs=[(t,font(fc,sz),sz,COLORS[col]) for (t,fc,sz,col) in lines]
    tmp=Image.new("RGBA",(10,10)); d=ImageDraw.Draw(tmp)
    hs=[]; ws=[]
    for t,f,sz,col in specs:
        bb=d.textbbox((0,0),t,font=f); ws.append(bb[2]-bb[0]); hs.append(bb[3]-bb[1]+int(sz*0.32))
    bw=min(max(ws)+pad*2, W-40); bh=sum(hs)+gap*(len(specs)-1)+pad*2
    img=Image.new("RGBA",(bw,bh),(0,0,0,0)); d=ImageDraw.Draw(img); y=pad
    for (t,f,sz,col),h in zip(specs,hs):
        bb=d.textbbox((0,0),t,font=f); w=bb[2]-bb[0]; x=(bw-w)//2-bb[0]
        for ox,oy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2)]:
            d.text((x+ox,y-bb[1]+oy),t,font=f,fill=(0,0,0,65))
        d.text((x,y-bb[1]),t,font=f,fill=col)
        y+=h+gap
    return img

def ease_out_back(p):
    p=max(0.0,min(1.0,p)); c1=1.70158; c3=c1+1
    return 1+c3*((p-1)**3)+c1*((p-1)**2)

TAGF=font("JUA",40)
def render_skit(sid, skit):
    beats=list(skit["beats"])
    is_product=bool(skit.get("product"))   # 훅 살리려 인트로 대신 상시 띠배너 사용
    # 누적 시간
    t0=0.0
    for b in beats: b["_s"]=t0; b["_e"]=t0+b["dur"]; t0+=b["dur"]
    total=t0
    blocks=[block_img(b["lines"]) for b in beats]
    fdir=os.path.join(TMP,sid); os.makedirs(fdir,exist_ok=True)
    for f in os.listdir(fdir): os.remove(os.path.join(fdir,f))
    N=int(total*FPS)
    for i in range(N):
        t=i/FPS; bi=len(beats)-1
        for j,b in enumerate(beats):
            if b["_s"]<=t<b["_e"]: bi=j; break
        b=beats[bi]; blk=blocks[bi]; bg=COLORS[b["bg"]]; anim=b["anim"]; lt=t-b["_s"]
        frame=Image.new("RGBA",(W,H),bg)
        scale=1.0; dx=dy=0; alpha=255; intro=0.38
        if anim=="pop":
            scale=0.35+0.65*ease_out_back(lt/intro) if lt<intro else 1.0
            alpha=int(255*min(1,lt/0.18))
        elif anim=="slideup":
            p=min(1,lt/intro); dy=int((1-p)*130); alpha=int(255*min(1,lt/0.2))
        elif anim=="shake":
            scale=0.4+0.6*ease_out_back(lt/0.3) if lt<0.3 else 1.0
            amp=max(0,38*(1-lt/0.9)); dx=int(math.sin(lt*48)*amp); dy=int(math.cos(lt*41)*amp*0.6)
            alpha=int(255*min(1,lt/0.12))
        bw,bh=blk.size; nw,nh=max(1,int(bw*scale)),max(1,int(bh*scale))
        b2=blk.resize((nw,nh),Image.LANCZOS)
        if alpha<255:
            a=b2.split()[3].point(lambda v:int(v*alpha/255)); b2.putalpha(a)
        frame.alpha_composite(b2,((W-nw)//2+dx,(H-nh)//2+dy))
        d=ImageDraw.Draw(frame); tag="@today.lim ・ 오늘살림"
        bb=d.textbbox((0,0),tag,font=TAGF)
        tc=(0,0,0,120) if b["bg"] in ("CREAM","YEL","GRAY") else (255,255,255,160)
        d.text(((W-(bb[2]-bb[0]))//2,H-112),tag,font=TAGF,fill=tc)
        if is_product:   # 상시 유료광고 띠배너(공정위 표시, 영상 내내 노출)
            bt="유료광고 · 쿠팡파트너스"; bf=font("JUA",34)
            bb2=d.textbbox((0,0),bt,font=bf); tw=bb2[2]-bb2[0]
            x0=(W-tw)//2-26; y0=52; x1=(W+tw)//2+26; y1=y0+34+28
            d.rounded_rectangle([x0,y0,x1,y1],radius=(y1-y0)//2,fill=(0,0,0,120))
            d.text(((W-tw)//2-bb2[0], y0+16-bb2[1]), bt, font=bf, fill=(255,255,255,235))
        frame.convert("RGB").save(os.path.join(fdir,f"f{i:04d}.png"))
    # 효과음 이벤트
    SFX={"pop":(1200,0.09,0.45),"pop_soft":(1050,0.09,0.4),"boing":(170,0.34,0.6),"ding":(1976,0.55,0.5)}
    AUTO={"pop":"pop","slideup":"pop_soft","shake":"boing"}
    events=[]
    for b in beats:
        typ=b.get("sfx") or AUTO.get(b["anim"],"pop")
        events.append((b["_s"]+0.03, typ))
    # ffmpeg: 프레임 + 사인 입력들 → 믹스 → mux
    cmd=["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",os.path.join(fdir,"f%04d.png")]
    filt=[]; labels=[]
    for idx,(tm,typ) in enumerate(events):
        f0,d0,v0=SFX[typ]; cmd+=["-f","lavfi","-i",f"sine=frequency={f0}:duration={d0}"]
        ms=int(tm*1000); lab=f"a{idx}"
        filt.append(f"[{idx+1}]afade=t=out:st=0:d={d0},volume={v0},adelay={ms}|{ms}[{lab}]")
        labels.append(f"[{lab}]")
    filt.append("".join(labels)+f"amix=inputs={len(events)}:normalize=0,apad[aout]")
    out=os.path.join(OUT,f"오늘살림_{sid}_상황극.mp4")
    cmd+=["-filter_complex",";".join(filt),"-map","0:v","-map","[aout]",
          "-c:v","libx264","-pix_fmt","yuv420p","-r",str(FPS),"-c:a","aac","-b:a","128k",
          "-shortest","-movflags","+faststart",out]
    subprocess.run(cmd,check=True)
    for f in os.listdir(fdir): os.remove(os.path.join(fdir,f))
    print(f"  ✅ {sid}  ({round(total,1)}s)  → {out}")
    return out

if __name__=="__main__":
    skits=json.load(open(os.path.join(HERE,"skits.json"),encoding="utf-8"))["skits"]
    ids=[a for a in sys.argv[2:]] if len(sys.argv)>2 else None   # 특정 id만 렌더(선택)
    todo={k:v for k,v in skits.items() if not ids or k in ids}
    print(f"상황극 {len(todo)}개 생성 → {OUT}")
    for sid,skit in todo.items():
        render_skit(sid,skit)
    print("완료.")
