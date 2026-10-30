#!/usr/bin/env python3
"""DoesItAutomate S01 - native 1080x1920, offline evidence-first motion study.

No voice, no external calendar API, no logo reconstruction, no publishing.
Requires Pillow, numpy, FFmpeg/ffprobe, Inter Display fonts.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, wave, struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,DURATION = 1080,1920,30,18
FRAMES=FPS*DURATION
FONT_DIR=Path('/usr/share/fonts/opentype/inter')
REG=FONT_DIR/'InterDisplay-Regular.otf'; SEMI=FONT_DIR/'InterDisplay-SemiBold.otf'; BOLD=FONT_DIR/'InterDisplay-Bold.otf'; BLACK=FONT_DIR/'InterDisplay-Black.otf'
MONO=Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
C={'bg':(7,13,25),'panel':(15,27,45),'line':(48,70,96),'text':(240,246,252),'muted':(147,174,200),'cyan':(84,218,255),'mint':(99,242,203),'amber':(255,191,105),'red':(253,121,120),'white':(255,255,255),'low':(35,56,80)}
FONTS={}
def ft(size,style='reg'):
    k=(size,style)
    if k not in FONTS:
        FONTS[k]=ImageFont.truetype({'reg':REG,'semi':SEMI,'bold':BOLD,'black':BLACK,'mono':MONO}[style],size)
    return FONTS[k]
def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def entry(t,at=.0,dur=.50): return ease((t-at)/dur)
def blend(a,b,f):return tuple(int(a[i]*(1-f)+b[i]*f) for i in range(3))
def text(d,xy,s,size=44,col='text',style='reg',anchor=None,stroke=0):
    color=C[col] if isinstance(col,str) else col
    d.text((int(xy[0]),int(xy[1])),str(s),font=ft(size,style),fill=color,anchor=anchor,stroke_width=stroke,stroke_fill=C['bg'])
def block(d,box,fill='panel',outline='line',rad=32,width=2):
    d.rounded_rectangle(tuple(map(int,box)),radius=rad,fill=C[fill] if isinstance(fill,str) else fill,outline=C[outline] if isinstance(outline,str) else outline,width=width)
def line(d,points,color='cyan',width=5):
    d.line([(int(x),int(y)) for x,y in points],fill=C[color] if isinstance(color,str) else color,width=width,joint='curve')
def tw(d,center,r,angle,color='cyan',width=7,seconds=0):
    # crisp native-resolution analog clock with 12 ticks and smooth hands
    cx,cy=center
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=C['panel'],outline=C['line'],width=3)
    d.arc((cx-r-5,cy-r-5,cx+r+5,cy+r+5),-90,angle-90,fill=C[color],width=10)
    for i in range(12):
        an=math.radians(i*30-90)
        outer=(cx+math.cos(an)*(r-22),cy+math.sin(an)*(r-22))
        inner=(cx+math.cos(an)*(r-(49 if i%3==0 else 35)),cy+math.sin(an)*(r-(49 if i%3==0 else 35)))
        line(d,[inner,outer],'muted' if i%3==0 else 'low',5 if i%3==0 else 3)
    minute=30*6; hour=(1.5)*30
    for deg,length,width,c in ((hour,r*.51,12,'text'),(minute,r*.70,8,color)):
        theta=math.radians(deg-90)
        px=cx+math.cos(theta)*length;py=cy+math.sin(theta)*length
        line(d,[(cx,cy),(px,py)],c,width)
    d.ellipse((cx-11,cy-11,cx+11,cy+11),fill=C[color])
    text(d,(cx,cy+r+61),'1:30 AM',43,'text','bold','mm')
def base_image():
    yy,xx=np.ogrid[:H,:W]
    light=np.clip(1-np.sqrt(((xx-760)/1100)**2+((yy-120)/1200)**2),0,1)
    light2=np.clip(1-np.sqrt(((xx-100)/1200)**2+((yy-1350)/1450)**2),0,1)
    arr=np.empty((H,W,3),dtype=np.uint8)
    for i,v in enumerate((7,13,25)):
        arr[:,:,i]=np.clip(v+np.array([2,9,16])[i]*light+np.array([0,5,11])[i]*light2,0,255).astype(np.uint8)
    im=Image.fromarray(arr,'RGB');d=ImageDraw.Draw(im)
    # ultra-subtle perspective engineering grid
    for x in range(0,W,90):line(d,[(x,220),(x,1700)],(19,34,52),1)
    for y in range(220,1701,90):line(d,[(0,y),(W,y)],(19,34,52),1)
    # edge hairlines and safe-area based layout
    line(d,[(78,240),(1002,240)],(41,67,90),2)
    line(d,[(78,1475),(1002,1475)],(40,62,86),2)
    return im
BASE=base_image()

def header(d,t,section,part):
    # top within experimental safe area (not platform-certified)
    text(d,(180,276),'DOES IT AUTOMATE?',36,'text','bold')
    text(d,(999,284),f'{part} / 05',28,'muted','mono','ra')
    rounded='#'
    line(d,[(82,340),(82+int(916*max(.02,([0.0,2.75,6.5,10.7,14.6][part-1]+t)/DURATION)),340)],'cyan',7)
    text(d,(82,385),section.upper(),28,'cyan','semi')
    # footer inside assumed safe height
    text(d,(82,1490),'LOCAL PYTHON SIMULATION',27,'cyan','semi')
    text(d,(82,1532),'NO CALENDAR API OR AI AGENT TESTED',26,'muted','reg')

def animated_ring(d,cx,cy,r,progress,color):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=C['low'],width=5)
    d.arc((cx-r,cy-r,cx+r,cy+r),-90,-90+int(359*progress),fill=C[color],width=9)

def scene_hook(d,t,ev):
    header(d,t,'The scheduling paradox',1)
    p=entry(t,.06,.42)
    text(d,(82,464-int(30*(1-p))),'ONE LOCAL TIME.',75,'text','black')
    text(d,(82,568-int(25*(1-p))),'TWO UTC TIMES.',75,'cyan','black')
    text(d,(86,693),'LOS ANGELES    •    NOV 01, 2026',30,'muted','semi')
    block(d,(90,770,990,970),rad=35)
    text(d,(540,835),'01:30 AM',110,'text','black','mm')
    text(d,(540,921),'LOCAL WALL CLOCK',29,'muted','semi','mm')
    # split is visually evident in first second; no intro logo beat
    prog=entry(t,.48,.78)
    line(d,[(540,970),(540,1043)],'cyan',5)
    line(d,[(540,1043),(280+(260*(1-prog)),1110)],'cyan',5)
    line(d,[(540,1043),(800-(260*(1-prog)),1110)],'mint',5)
    for x,lab,clr in [(273,'08:30Z','cyan'),(807,'09:30Z','mint')]:
        rad=int(12*math.sin(t*4)**2)
        block(d,(x-203,1123,x+203,1285),'panel',clr,30,3)
        text(d,(x,1170),lab,64,clr,'black','mt')
    # Moving signal on each fork makes the ambiguity visible throughout the beat.
    if t>.7:
        p=(t*.68)%1.0
        for x,c in ((273,'cyan'),(807,'mint')):
            px=540+(x-540)*p;py=1043+(1103-1043)*p
            d.ellipse((px-10,py-10,px+10,py+10),fill=C[c])
    text(d,(540,1400),'SAME CLOCK. DIFFERENT INSTANTS.',34,'amber','semi','mt')

def scene_clocks(d,t,ev):
    header(d,t,'Why the clock repeats',2)
    text(d,(82,462),'1:30 HAPPENS',73,'text','black')
    text(d,(82,554),'TWICE.',88,'mint','black')
    tw(d,(312,861),184,-90+340*entry(t,.15,.85),'cyan')
    tw(d,(766,861),184,-90+340*entry(t,.48,.95),'mint')
    # One illuminated sweep per physical-clock ring. No fake extra result.
    for cx,clr,phase in ((312,'cyan',0),(766,'mint',.35)):
        angle=-math.pi/2+math.tau*((t/2.4+phase)%1)
        px=cx+187*math.cos(angle);py=861+187*math.sin(angle)
        d.ellipse((px-11,py-11,px+11,py+11),fill=C[clr])
    text(d,(312,1150),'FIRST OCCURRENCE',28,'muted','semi','mm')
    text(d,(766,1150),'SECOND OCCURRENCE',28,'muted','semi','mm')
    text(d,(312,1200),'UTC−7',44,'cyan','bold','mm')
    text(d,(766,1200),'UTC−8',44,'mint','bold','mm')
    block(d,(95,1320,985,1450),'panel','line',28)
    text(d,(540,1376),'ONE HOUR APART — BOTH VALID',39,'text','bold','mm')

def draw_fork(d,t,ev):
    header(d,t,'Verified in zoneinfo',3)
    text(d,(82,464),'ONE INPUT.',82,'text','black')
    text(d,(82,564),'TWO INSTANTS.',78,'cyan','black')
    block(d,(250,690,830,838),'panel','cyan',28,3)
    text(d,(540,743),'01:30 · LOS ANGELES',50,'text','bold','mt')
    text(d,(540,804),'2026-11-01',31,'muted','mono','mm')
    branch=entry(t,.45,1.1)
    d.ellipse((525,849,555,879),fill=C['white'])
    # progressive geometric split / path
    y1=870; y2=1068
    line(d,[(540,y1),(540,y1+120*branch)],'cyan',7)
    if branch>.35:
        q=ease((branch-.35)/.65)
        line(d,[(540,990),(540-280*q,y2)],'cyan',7)
        line(d,[(540,990),(540+280*q,y2)],'mint',7)
    for cx,col,fold,time in [(278,'cyan','FOLD 0 · UTC−7','08:30Z'),(802,'mint','FOLD 1 · UTC−8','09:30Z')]:
        block(d,(cx-219,1085,cx+219,1290),'panel',col,32,3)
        text(d,(cx,1134),fold,29,'muted','semi','mt')
        text(d,(cx,1202),time,80,col,'black','mm')
    # Light travelling down each verified path.
    if branch>.88:
        p=(t*.62)%1
        for x,clr in ((278,'cyan'),(802,'mint')):
            px=540+(x-540)*p;py=990+(1068-990)*p
            d.ellipse((px-10,py-10,px+10,py+10),fill=C[clr])
    text(d,(540,1400),'2 VALID UTC CANDIDATES',37,'amber','semi','mt')

def draw_guard(d,t,ev):
    header(d,t,'Two handling strategies',4)
    text(d,(82,464),'PICK ONE?',85,'text','black')
    text(d,(82,560),'OR CHECK FIRST?',68,'cyan','black')
    a=entry(t,.3,.5)
    block(d,(81,720,999,997),'panel','line',36,3)
    text(d,(124,760),'PERMISSIVE CONVERSION',34,'muted','semi')
    text(d,(124,831),'fold = 0',49,'text','mono')
    text(d,(920,846),'08:30Z',59,'amber','bold','ra')
    text(d,(124,921),'Selects an instant without asking',33,'muted','reg')
    block(d,(81,1050,999,1425),'panel','mint',36,4)
    # simple recognizable verification mark
    d.ellipse((125,1100,209,1184),outline=C['mint'],width=6)
    line(d,[(149,1142),(166,1161),(189,1120)],'mint',8)
    text(d,(239,1098),'STRICT LOCAL GUARD',35,'muted','semi')
    text(d,(123,1210),'AMBIGUOUS',83,'amber','black')
    text(d,(124,1325),'REQUEST CLARIFICATION',47,'mint','bold')
    # The guard verifies the input before permitting a single instant to leave.
    line(d,[(124,1392),(124+int(822*((t*.44)%1)),1392)],'mint',5)

def scene_close(d,t,ev):
    header(d,t,'The engineering lesson',5)
    text(d,(82,458),'DON’T GUESS',91,'text','black')
    text(d,(82,572),'THE TIME.',91,'cyan','black')
    # single hero timeline with choice badge
    cx,cy=540,966
    prog=entry(t,.3,.78)
    animated_ring(d,cx,cy,230,prog,'mint')
    theta=math.tau*((t*.22)%1)-math.pi/2
    xx=cx+231*math.cos(theta);yy=cy+231*math.sin(theta)
    d.ellipse((xx-10,yy-10,xx+10,yy+10),fill=C['mint'])
    d.ellipse((cx-191,cy-191,cx+191,cy+191),fill=C['panel'])
    text(d,(cx,867),'01:30 AM',77,'text','black','mm')
    text(d,(cx,972),'AMBIGUOUS',43,'amber','bold','mm')
    text(d,(cx,1050),'ASK FIRST',52,'mint','black','mm')
    text(d,(540,1340),'VERIFY BEFORE SCHEDULING.',43,'text','semi','mm')

STAGES=[(0.0,2.75,scene_hook),(2.75,6.5,scene_clocks),(6.5,10.7,draw_fork),(10.7,14.6,draw_guard),(14.6,18.,scene_close)]
def validate_source(ev):
    if ev.get('experiment_id')!='NINFA-S01' or ev.get('experiment_type')!='OFFLINE_LOCAL_SIMULATION':raise ValueError('Invalid S01 experiment provenance')
    if ev.get('provider_calendar_api_tested') is not False or ev.get('ai_agent_tested') is not False:raise ValueError('Actual provider/AI test status mismatch')
    c=next((c for c in ev['cases'] if c['case_id']=='fall_repeated_hour'),None)
    if c is None or c['timezone']!='America/Los_Angeles' or c['local_iso']!='2026-11-01T01:30:00' or c['status']!='AMBIGUOUS':raise ValueError('Source not the declared DST ambiguity case')
    if [(v['fold'],v['utc']) for v in c['valid_utc_candidates']] != [(0,'2026-11-01T08:30:00Z'),(1,'2026-11-01T09:30:00Z')]:raise ValueError('Time labels are inconsistent with measured evidence')
    return c

LOGO=None
def frame(fi,ev):
    t=fi/FPS
    im=BASE.copy()
    if LOGO is not None: im.paste(LOGO,(83,259),LOGO)
    d=ImageDraw.Draw(im)
    scene=next(draw for start,end,draw in STAGES if start<=t<end)
    # animated sparse scan line, subtle and stationary grid for stability
    px=int(50+980*(t%3.25)/3.25)
    line(d,[(px,244),(px,259)],'cyan',3)
    scene(d,t-next(start for start,end,draw in STAGES if start<=t<end),ev)
    # scan-overlaid steps fade at transition (small, no compulsory intro)
    return im

def sfx(duration=DURATION,sr=48000):
    n=round(duration*sr); x=np.zeros(n,dtype=np.float64)
    def add(at,which,amp=0.17):
        nonlocal x
        secs=.22 if which=='tick' else .5
        m=int(secs*sr);q=np.arange(m)/sr
        if which=='tick':
            wave=np.sin(2*np.pi*1900*q)*np.exp(-q*44)+np.sin(2*np.pi*940*q)*np.exp(-q*64)
        else:
            wave=(np.sin(2*np.pi*(420*q+100*q*q))+np.sin(2*np.pi*(640*q+60*q*q))*.45)*np.exp(-q*12)
        i=int(at*sr); x[i:min(i+m,n)] += amp*wave[:max(0,min(i+m,n)-i)]
    for t in [0.05,.65,1.15,2.75,6.50,7.15,8.25,10.70,12.5,14.60,16.0]:add(t,'tick',.12)
    for t in [1.0,6.65,10.85,14.72]:add(t,'whoosh',.085)
    # light dynamic acoustic markers; explicitly not a synthesized voice or soundtrack
    peak=np.max(np.abs(x)) or 1
    x=np.clip(x/max(1,peak/.68),-0.7,0.7)
    return (x*32767).astype('<i2'),sr

def render(source,out,contact,with_sfx=True,crf=17,logo=None):
    global LOGO
    LOGO=Image.open(logo).convert('RGBA').resize((79,66),Image.Resampling.LANCZOS) if logo else None
    ev=json.loads(Path(source).read_text(encoding='utf-8'));validate_source(ev)
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    wav=out.with_suffix('.sfx.wav')
    audio,sr=sfx()
    with wave.open(str(wav),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(audio.tobytes())
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0']
    if with_sfx:cmd.extend(['-i',str(wav),'-map','0:v','-map','1:a'])
    else:cmd.extend(['-map','0:v'])
    cmd.extend(['-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf',str(crf),'-profile:v','high','-level','4.2','-movflags','+faststart','-metadata','title=DoesItAutomate - S01 V2 review'])
    if with_sfx:cmd.extend(['-c:a','aac','-b:a','160k','-ar','48000','-ac','2'])
    else:cmd.extend(['-an'])
    cmd.extend(['-t',str(DURATION),str(out)])
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    contact_frames=[]
    selected={15,105,206,335,460,515}
    try:
        for fi in range(FRAMES):
            im=frame(fi,ev)
            if fi in selected:
                contact_frames.append(im.copy())
            p.stdin.write(im.tobytes())
            if fi and fi%90==0:print(f'render {fi}/{FRAMES}',flush=True)
        p.stdin.close();stderr=p.stderr.read().decode('utf-8','replace');rc=p.wait()
    except Exception:
        p.kill();raise
    if rc!=0:raise RuntimeError(stderr)
    sheet=Image.new('RGB',(1080,3*960),(8,13,22))
    for i,im in enumerate(contact_frames):
        sheet.paste(im.resize((540,960),Image.Resampling.LANCZOS),((i%2)*540,(i//2)*960))
    if contact:sheet.save(contact,optimize=True)
    if wav.exists():wav.unlink()
    print(json.dumps({'video':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'width':W,'height':H,'fps':FPS,'frames':FRAMES,'duration':DURATION,'audio':'PROCEDURAL_UI_SFX_ONLY' if with_sfx else 'SILENT','narration':'NOT_INCLUDED','publication':'BLOCKED_REVIEW_ONLY','contact':str(contact)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--evidence',required=True);p.add_argument('--out',required=True);p.add_argument('--contact',required=True);p.add_argument('--no-sfx',action='store_true');p.add_argument('--logo',help='Owner-approved canonical brand mark file; optional, never synthesized');a=p.parse_args()
    render(a.evidence,a.out,a.contact,not a.no_sfx,logo=a.logo)
