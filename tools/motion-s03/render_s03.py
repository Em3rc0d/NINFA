#!/usr/bin/env python3
"""NINFA S03 native-1080p motion short. Evidence-backed LOCAL SQLite crash/restart only.

No AI agent/model, real customers, provider APIs, scheduled publish or remote network.
This output is REVIEW-ONLY, without approved English narration.
"""
import argparse, hashlib, json, math, subprocess, tempfile, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W,H,FPS,LENGTH=1080,1920,30,18
FRAMES=FPS*LENGTH
INK=(238,245,255);BG=(7,13,26);PANEL=(16,29,48);PANEL2=(21,38,61);MUTED=(145,173,205)
BLUE=(77,206,255);GREEN=(88,239,190);RED=(255,108,108);AMBER=(255,194,111);GREY=(53,75,100)
FONT_DIR=Path('/usr/share/fonts/opentype/inter')
FONTS={}
LOGO=None

def font(size,weight='regular'):
    key=(size,weight)
    if key not in FONTS:
        files={'regular':'InterDisplay-Regular.otf','medium':'InterDisplay-Medium.otf','bold':'InterDisplay-Bold.otf','black':'InterDisplay-Black.otf'}
        FONTS[key]=ImageFont.truetype(str(FONT_DIR/files[weight]),size)
    return FONTS[key]

def ease(v):
    v=max(0,min(1,v));return v*v*(3-2*v)

def lerp(a,b,v):return a+(b-a)*v

def txt(d,x,y,s,sz=40,col=INK,weight='regular',anchor=None):
    d.text((int(x),int(y)),str(s),font=font(sz,weight),fill=col,anchor=anchor)

def rect(d,xy,color=PANEL,outline=GREY,r=26,width=2):
    d.rounded_rectangle(tuple(int(v) for v in xy),radius=r,fill=color,outline=outline,width=width)

def rule(d,p1,p2,col=BLUE,w=4):
    d.line([tuple(map(int,p1)),tuple(map(int,p2))],fill=col,width=w,joint='curve')

def frame_base():
    yy,xx=np.ogrid[:H,:W]
    top=np.clip(1-np.sqrt(((xx-820)/1100)**2+((yy-100)/1380)**2),0,1)
    bottom=np.clip(1-np.sqrt(((xx-80)/1200)**2+((yy-1450)/1200)**2),0,1)
    a=np.empty((H,W,3),dtype=np.uint8)
    for c,v in enumerate(BG):
        a[:,:,c]=np.clip(v+[3,8,14][c]*top+[1,4,9][c]*bottom,0,255).astype('uint8')
    image=Image.fromarray(a,'RGB'); d=ImageDraw.Draw(image)
    for x in range(74,W-70,92):rule(d,(x,225),(x,1690),(20,35,55),1)
    for y in range(225,1690,92):rule(d,(0,y),(W,y),(20,35,55),1)
    rule(d,(82,242),(998,242),GREY,2)
    rule(d,(82,1492),(998,1492),GREY,2)
    return image
BASE=frame_base()

def header(d,t,part,title):
    # Logo is the extracted exact owner-approved asset; no alternative made by code.
    if LOGO is None:
        txt(d,82,267,'DOES IT AUTOMATE?',35,INK,'bold')
    else:
        txt(d,214,272,'DOES IT AUTOMATE?',35,INK,'bold')
    txt(d,998,280,f'{part}/05',27,MUTED,'medium','ra')
    txt(d,82,354,title.upper(),25,BLUE,'bold')
    rule(d,(82,328),(82+916*min(1,t/LENGTH),328),BLUE,6)
    txt(d,82,1512,'LOCAL SQLITE EXPERIMENT',27,BLUE,'bold')
    txt(d,82,1561,'NO AI MODEL OR EXTERNAL SERVICE TESTED',24,MUTED,'regular')

def tag(d,x,y,label,color=BLUE):
    w=int(d.textbbox((0,0),label,font=font(25,'bold'))[2])+52
    rect(d,(x,y,x+w,y+57),PANEL,color,15,2)
    txt(d,x+26,y+14,label,25,color,'bold')
    return w

def step_box(d,cx,cy,name,index,status='pending',w=204):
    c={'ok':GREEN,'active':BLUE,'bad':RED,'pending':GREY,'restore':AMBER}[status]
    rect(d,(cx-w/2,cy-67,cx+w/2,cy+71),PANEL,c,21,3 if status!='pending' else 2)
    txt(d,cx,cy-34,str(index).zfill(2),31,c,'black','mm')
    txt(d,cx,cy+22,name,24,INK if status!='pending' else MUTED,'bold','mm')

def lightning(d,x,y,scale=1.0):
    pts=[(-30,-95),(22,-95),(-11,-16),(52,-16),(-48,104),(-19,15),(-76,15)]
    d.polygon([(int(x+px*scale),int(y+py*scale)) for px,py in pts],fill=RED)

def center_pill(d,cx,cy,title,col=BLUE,w=690,h=114):
    rect(d,(cx-w/2,cy-h/2,cx+w/2,cy+h/2),PANEL2,col,25,3)
    txt(d,cx,cy,title,49,col,'black','mm')

def s1(d,s,ev):
    t=s
    txt(d,82,460,'I CRASHED THE',80,INK,'black')
    txt(d,82,553,'AUTOMATION.',78,RED,'black')
    txt(d,82,688,'AT STEP 2 OF 4',45,MUTED,'bold')
    for idx,(nm,cx) in enumerate(zip(('READ','VALIDATE','BUILD','STORE'),(174,418,662,906))):
        status='ok' if idx<2 else 'pending'
        step_box(d,cx,1015,nm,idx+1,status,w=205)
        if idx<3:rule(d,(cx+110,1015),(cx+128,1015),BLUE if idx<1 else GREY,6)
    # sudden process-stop animation after some time
    fade=ease((t-.23)/.22)
    if fade>0:
        lightning(d,539,1209,.85+.12*math.sin(t*15))
        txt(d,540,1370,'WORKER EXITED · CODE 27',36,RED,'bold','mm')
    # pulsing visual stop band
    if t>1.4:
        alpha=.5+.5*math.sin(t*17)**2
        rule(d,(84,787),(84+int(912*alpha),787),RED,7)

def s2(d,s,ev):
    txt(d,82,469,'RESTART THE JOB.',72,INK,'black')
    txt(d,82,563,'WHAT REPEATS?',78,BLUE,'black')
    # 4 blocks and the restarted progress sweep
    for i,nm in enumerate(('READ','VALIDATE','BUILD','STORE')):
        x=91+(i%2)*458;y=815+(i//2)*235
        c=AMBER if i<2 else GREY
        rect(d,(x,y,x+436,y+201),PANEL,c,25,3)
        txt(d,x+31,y+34,f'STEP {i+1:02d}',29,c,'medium')
        txt(d,x+31,y+91,nm,45,INK,'bold')
        txt(d,x+399,y+99,'✓' if i<2 else '—',37,c,'bold','ra')
    center_pill(d,540,1373,'2 STEPS COMPLETED',AMBER,820,117)
    # signal from process up, cuts back down
    p=(s*1.0)%1
    rule(d,(540,742),(540,742+int(49*p)),RED,8)

def trace(d,x,y,records,col,show_until,w=830,step=84):
    for i,(name,phase) in enumerate(records):
        if i>=show_until:break
        yy=y+i*step
        rect(d,(x,yy,x+w,yy+70),PANEL2,col if phase==2 else GREY,16,2)
        txt(d,x+29,yy+17,f'{i+1:02d}',27,col if phase==2 else MUTED,'bold')
        txt(d,x+100,yy+16,name,32,INK,'bold')
        txt(d,x+w-28,yy+17,('RESTART' if phase==2 else 'BEFORE CRASH'),25,col if phase==2 else MUTED,'medium','ra')

def s3(d,s,ev):
    txt(d,82,460,'WITHOUT SAVING',74,INK,'black')
    txt(d,82,548,'PROGRESS',91,RED,'black')
    txt(d,84,700,'THE WORKER STARTS OVER.',34,MUTED,'medium')
    data=[(x['step'],x['phase']) for x in ev['modes']['naive']['actions']]
    n=min(len(data),max(1,int(lerp(1,len(data),ease((s-.17)/2.4)))))
    trace(d,112,788,data,RED,n,860,94)
    if s>2.2:
        rect(d,(210,1368,870,1460),PANEL,RED,23,3)
        txt(d,540,1411,'6 ACTIONS  ·  2 REPEATED',36,RED,'black','mm')

def s4(d,s,ev):
    txt(d,82,460,'SAVE THE',89,INK,'black')
    txt(d,82,555,'CHECKPOINT.',81,GREEN,'black')
    txt(d,83,695,'RESTART FROM THE LAST SAVED STEP.',31,MUTED,'medium')
    data=[(x['step'],x['phase']) for x in ev['modes']['checkpoint']['actions']]
    n=min(len(data),max(1,int(lerp(1,len(data),ease((s-.2)/2.5)))))
    trace(d,112,800,data,GREEN,n,860,132)
    # checkpoints visibly stored; show 2 already saved
    for x in (220,540,860):
        rule(d,(x,1395),(x,1410),GREEN,3)
    rect(d,(140,1415,940,1481),PANEL,GREEN,18,2)
    txt(d,540,1447,'RESUME  →  STEP 03',36,GREEN,'black','mm')

def s5(d,s,ev):
    txt(d,82,462,'SAME JOB.',88,INK,'black')
    txt(d,82,565,'DIFFERENT RESTART.',61,BLUE,'black')
    # Head-to-head final score
    for x,col,title,count in [(292,RED,'NO CHECKPOINT',6),(788,GREEN,'CHECKPOINT',4)]:
        rect(d,(x-225,738,x+225,1182),PANEL,col,36,4)
        txt(d,x,812,title,29,col,'bold','mm')
        txt(d,x,985,str(count),177,INK,'black','mm')
        txt(d,x,1096,'ACTIONS',35,MUTED,'bold','mm')
    # comparator divider
    center_pill(d,540,1275,'2 REPEATS AVOIDED',BLUE,850,115)
    txt(d,540,1430,'ONLY FOR THIS LOCAL SQLITE WORKFLOW',29,MUTED,'medium','mm')

STAGES=[(0,2.8,s1,'CRASH AT STEP 2'),(2.8,5.4,s2,'RESTART THE WORKER'),(5.4,9.7,s3,'NAIVE REPLAY'),(9.7,14.0,s4,'CHECKPOINT RECOVERY'),(14.0,18.0,s5,'THE MEASURED RESULT')]

def validate(ev):
    if ev.get('schema')!='ninfa-local-crash-recovery-v1' or ev.get('experiment')!='NINFA-S03':raise ValueError('Wrong experiment provenance')
    if ev.get('actual_worker_process_crashed') is not True or ev.get('forced_exit_code')!=27:raise ValueError('No confirmed crash')
    if ev.get('boundary',{}).get('no_ai_model_tested') is not True or ev['boundary'].get('no_external_api_or_provider') is not True:raise ValueError('External/AI claim mismatch')
    m=ev['modes']; assert m['naive']['action_count']==6 and m['checkpoint']['action_count']==4
    assert m['naive']['repeated_action_count']==2 and m['checkpoint']['repeated_action_count']==0
    raw=dict(ev);signature=raw.pop('sha256_canonical_core','')
    h=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if signature!=h:raise ValueError('Evidence digest mismatch')


def rgb_frame(i,ev):
    t=i/FPS
    image=BASE.copy();d=ImageDraw.Draw(image)
    if LOGO is not None:image.paste(LOGO,(84,264),LOGO)
    at,end,fn,title=next(stage for stage in STAGES if stage[0]<=t<stage[1])
    header(d,t,STAGES.index((at,end,fn,title))+1,title)
    fn(d,t-at,ev)
    # light pulse along top edge
    px=round(90+900*((t*.28)%1.0))
    rule(d,(px,243),(px,256),BLUE,4)
    # subtle scene edge progress dots
    for j in range(5):
        d.ellipse((487+j*27,1645,501+j*27,1659),fill=BLUE if j==STAGES.index((at,end,fn,title)) else GREY)
    return image

def sfx(path):
    sr=48000;n=LENGTH*sr; wave_data=np.zeros(n,dtype=np.float64)
    events=[(.06,330,.22,.05),(.75,660,.10,.08),(1.2,240,.14,.14),(2.8,490,.22,.08),(5.4,220,.26,.13),(7.7,240,.19,.10),(9.7,450,.19,.10),(11.1,800,.10,.08),(13.95,700,.23,.12),(15.2,920,.20,.10)]
    for at,f,duration,amp in events:
        start=int(at*sr);count=min(int(duration*sr),n-start)
        if count<=0:continue
        tt=np.arange(count)/sr
        env=(1-np.exp(-tt*100))*np.exp(-tt*13)
        tone=np.sin(2*np.pi*(f*tt+40*tt*tt))*env*amp
        wave_data[start:start+count]+=tone
    peak=max(.0001,np.max(np.abs(wave_data)))
    wave_data=np.clip(wave_data/max(1,peak/.32),-.95,.95)
    stereo=np.column_stack([wave_data,wave_data*.93]).astype('float32')
    pcm=(stereo*32767).astype('<i2')
    with wave.open(str(path),'wb') as wf:
        wf.setnchannels(2);wf.setframerate(sr);wf.setsampwidth(2);wf.writeframes(pcm.tobytes())

def render(source,out,contact=None,logo=None):
    global LOGO
    ev=json.loads(Path(source).read_text())
    validate(ev)
    if logo:
        asset=Image.open(logo).convert('RGBA')
        if asset.width<100 or asset.height<100:raise ValueError('Logo asset too small')
        asset.thumbnail((87,78),Image.Resampling.LANCZOS)
        LOGO=asset
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        wav=Path(td)/'effects.wav';sfx(wav)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-ac','2','-shortest','-movflags','+faststart',str(out)]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        shots=[]
        try:
            for i in range(FRAMES):
                image=rgb_frame(i,ev)
                if i in [12,91,182,251,326,411,489,527]:shots.append(image.copy())
                p.stdin.write(image.tobytes())
            p.stdin.close()
            err=p.stderr.read().decode(errors='replace')
            code=p.wait()
            if code:raise RuntimeError(f'ffmpeg exit {code}: {err}')
        except Exception:
            p.kill();p.wait();raise
        if contact:
            thumb_w=330;thumb_h=round(thumb_w*H/W)
            canvas=Image.new('RGB',(4*thumb_w,2*thumb_h),BG)
            for i,image in enumerate(shots):
                im=image.resize((thumb_w,thumb_h),Image.Resampling.LANCZOS)
                canvas.paste(im,((i%4)*thumb_w,(i//4)*thumb_h))
            canvas.save(contact,optimize=True)
    print(json.dumps({'path':str(out),'sha256':hashlib.sha256(Path(out).read_bytes()).hexdigest(),'frames':FRAMES,'native_resolution':[W,H],'audio':'ORIGINAL_UI_SFX_ONLY','voice':'NONE','state':'REVIEW_ONLY','source_evidence_sha':ev['sha256_canonical_core']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--evidence',required=True);p.add_argument('--out',required=True);p.add_argument('--contact');p.add_argument('--logo');a=p.parse_args()
    render(a.evidence,a.out,a.contact,a.logo)
