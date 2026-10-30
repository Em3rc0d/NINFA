#!/usr/bin/env python3
"""S01 storyboard-driven, offline, SILENT visual proof, not publication approved."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W,H,FPS,SEC=540,960,30,18
FULL_W,FULL_H=1080,1920
FRAMES=FPS*SEC
BG='#0A101D'; PANEL='#121E31'; INK='#EDF5FF'; MUTED='#9DB2C9'; CYAN='#53D8FF'; GREEN='#60E8C4'; AMBER='#FFBA6D'; RED='#FF847A'; STROKE='#294055'
FONT_DIR=Path('/usr/share/fonts/truetype/lato')
REG=FONT_DIR/'Lato-Regular.ttf'
BOLD=FONT_DIR/'Lato-Heavy.ttf'
BLACK=FONT_DIR/'Lato-Black.ttf'
SEMIBOLD=FONT_DIR/'Lato-Semibold.ttf'
F={}
def font(n:int,style='reg'):
    key=(n,style)
    if key not in F:
        F[key]=ImageFont.truetype({'reg':REG,'bold':BOLD,'black':BLACK,'semi':SEMIBOLD}[style],n)
    return F[key]

def smooth(v):
    v=max(0,min(1,v)); return v*v*(3-2*v)

def rounded(d,b,fill,outline=None,r=18,width=1):
    d.rounded_rectangle(tuple(int(x) for x in b),radius=r,fill=fill,outline=outline,width=width)

def text(d,xy,s,size=20,color=INK,style='reg',anchor=None,spacing=5):
    d.multiline_text((int(xy[0]),int(xy[1])),str(s),font=font(size,style),fill=color,anchor=anchor,spacing=spacing,align='center' if anchor and 'm' in anchor else 'left')

def line(d,points,fill=CYAN,width=2):
    d.line([(int(x),int(y)) for x,y in points],fill=fill,width=width,joint='curve')

def card(d,y,label,value,color=CYAN,sub='',x=61,w=418,h=104):
    rounded(d,(x,y,x+w,y+h),PANEL,STROKE,r=18,width=2)
    rounded(d,(x+13,y+17,x+18,y+h-17),color,r=2)
    text(d,(x+33,y+13),label.upper(),15,MUTED,'semi')
    text(d,(x+32,y+37),value,38,INK,'black')
    if sub:text(d,(x+w-19,y+81),sub,12,MUTED,'reg',anchor='ra')

def heading(d,section,title,t,at):
    k=smooth((t-at)/.38)
    text(d,(64,176+int((1-k)*13)),section.upper(),16,CYAN,'semi')
    text(d,(64,206+int((1-k)*20)),title,40,INK,'black',spacing=2)
    line(d,[(64,319),(64+int(70*k),319)],CYAN,4)

def base_image():
    yy,xx=np.indices((H,W))
    r=np.maximum(0,1-np.sqrt(((xx-470)/650)**2+((yy-75)/650)**2))
    base=np.zeros((H,W,3),dtype=np.uint8)
    base[:,:,0]=(10+3*r).astype('uint8')
    base[:,:,1]=(16+15*r).astype('uint8')
    base[:,:,2]=(29+26*r).astype('uint8')
    im=Image.fromarray(base,'RGB');d=ImageDraw.Draw(im)
    for x in range(36,W,40):line(d,[(x,119),(x,839)],'#142338',1)
    for y in range(119,840,40):line(d,[(36,y),(505,y)],'#142338',1)
    rounded(d,(40,114,500,814),None,'#263D55',r=26,width=2)
    rounded(d,(64,132,84,152),CYAN,r=6)
    text(d,(96,131),'EXPERIMENT 01',14,MUTED,'semi')
    text(d,(480,142),'01',14,CYAN,'black',anchor='ra')
    line(d,[(64,160),(475,160)],'#31435B',1)
    # Provider/source caveat always legible in the experimental safe area.
    line(d,[(64,718),(475,718)],'#304258',1)
    text(d,(64,731),'LOCAL PYTHON SIMULATION',15,CYAN,'semi')
    text(d,(64,754),'NO CALENDAR PROVIDER TESTED',14,MUTED,'semi')
    text(d,(64,783),'DOES IT AUTOMATE?  •  EXPERIMENTAL REVIEW',11,MUTED,'semi')
    return im

STAGES=[(0,2.7,'HOOK'),(2.7,5.8,'TWO_INSTANCES'),(5.8,9.2,'EVIDENCE'),(9.2,12.0,'PERMISSIVE'),(12.0,16.0,'GUARD'),(16.0,18.0,'LESSON')]

def make_frame(base,fi,source):
    t=fi/FPS
    im=base.copy();d=ImageDraw.Draw(im)
    d.rounded_rectangle((40,114,40+int(460*(fi+1)/FRAMES),117),radius=1,fill=CYAN)
    time=source['cases'][0]
    choice=time['valid_utc_candidates']
    assert len(choice)==2
    if t<2.7:
        heading(d,'an unusual scheduling edge case','ONE TIME.\nTWO UTC RESULTS.',t,0)
        amt=smooth((t-.30)/.5)
        rounded(d,(72,380,468,483),PANEL,STROKE,18,2)
        text(d,(270,396),'LOS ANGELES  /  NOV 1, 2026',16,MUTED,'semi',anchor='mt')
        text(d,(270,421),'01:30 AM',42,INK,'black',anchor='mt')
        off=int(100*(1-smooth((t-.85)/.6)))
        for x,v,c in ((72,choice[0]['utc'][11:16]+'Z',CYAN),(278,choice[1]['utc'][11:16]+'Z',GREEN)):
            if t>.9:
                rounded(d,(x,522+off,x+190,610+off),PANEL,c,15,2)
                text(d,(x+95,541+off),v,28,INK,'black',anchor='mt')
        if t>1.4:text(d,(270,647),'SAME WALL CLOCK. TWO INSTANTS.',16,CYAN,'semi',anchor='mt')
    elif t<5.8:
        heading(d,'daylight-saving overlap','1:30 AM\nHAPPENS TWICE.',t,2.7)
        p=smooth((t-3.1)/.55)
        card(d,372,'fold = 0  •  PDT (UTC−7)',choice[0]['utc'][11:16]+' UTC',CYAN,'first occurrence')
        if p>.05:
            card(d,493,'fold = 1  •  PST (UTC−8)',choice[1]['utc'][11:16]+' UTC',GREEN,'second occurrence')
        text(d,(70,652),'AN HOUR APART',19,AMBER,'black')
        line(d,[(266,664),(468,664)],AMBER,2)
    elif t<9.2:
        heading(d,'reproduced in Python','THE INPUT\nIS AMBIGUOUS.',t,5.8)
        rounded(d,(65,360,475,615),PANEL,STROKE,18,2)
        text(d,(88,383),'LOCAL INPUT',15,CYAN,'semi')
        text(d,(88,410),'2026-11-01 01:30',26,INK,'bold')
        text(d,(88,453),'America/Los_Angeles',18,MUTED,'semi')
        line(d,[(88,495),(453,495)],STROKE,2)
        for i,c in enumerate(choice):
            text(d,(90,518+i*39),f"fold {c['fold']}   →   {c['utc'][11:16]}Z",23,CYAN if i==0 else GREEN,'semi')
        text(d,(72,653),'2 VERIFIED UTC CANDIDATES',18,AMBER,'black')
    elif t<12.0:
        heading(d,'without explicit validation','PERMISSIVE\nCONVERSION.',t,9.2)
        rounded(d,(66,388,474,575),PANEL,STROKE,18,2)
        text(d,(91,413),'fold = 0  •  default selection',18,MUTED,'semi')
        text(d,(90,448),source['cases'][0]['permissive_fold0_utc'][11:16]+' UTC',42,INK,'black')
        line(d,[(93,519),(445,519)],STROKE,2)
        text(d,(90,535),'AMBIGUITY NOT FLAGGED',15,AMBER,'semi')
        text(d,(70,628),'THIS IS PYTHON BEHAVIOR,',16,MUTED,'semi')
        text(d,(70,650),'NOT A CALENDAR API BUG.',16,MUTED,'semi')
    elif t<16.0:
        heading(d,'the checked alternative','EXPLICIT\nGUARDRAIL.',t,12.0)
        rounded(d,(64,377,476,598),PANEL,GREEN,20,2)
        text(d,(88,408),'DETECTED',17,MUTED,'semi')
        text(d,(88,443),'AMBIGUOUS',38,AMBER,'black')
        line(d,[(88,506),(446,506)],STROKE,2)
        text(d,(88,531),'REQUEST CLARIFICATION',22,GREEN,'black')
        text(d,(70,631),'DON’T GUESS WHICH INSTANT.',18,INK,'semi')
    else:
        heading(d,'the engineering lesson','ASK BEFORE\nSCHEDULING.',t,16.0)
        rounded(d,(65,388,475,576),PANEL,GREEN,20,2)
        text(d,(270,413),'AMBIGUOUS LOCAL TIME',17,AMBER,'semi',anchor='mt')
        text(d,(270,461),'VERIFY FIRST.',32,GREEN,'black',anchor='mt')
        text(d,(270,530),'No provider or AI model tested.',16,MUTED,'semi',anchor='mt')
    return im

def run(out:Path,evidence:Path,contact:Path|None=None):
    source=json.loads(evidence.read_text(encoding='utf-8'))
    assert source['experiment_id']=='NINFA-S01' and source['provider_calendar_api_tested'] is False
    assert source['cases'][0]['status']=='AMBIGUOUS'
    out.parent.mkdir(parents=True,exist_ok=True)
    base=base_image()
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-vf',f'scale={FULL_W}:{FULL_H}:flags=lanczos,format=yuv420p','-an','-c:v','libx264','-preset','veryfast','-crf','20','-profile:v','high','-movflags','+faststart','-metadata','title=NINFA S01 timezone ambiguity - silent review','-t',str(SEC),str(out)]
    ss={int(sec*FPS) for sec in [1.7,4.5,7.2,10.5,13.7,16.8]}
    frames=[]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(FRAMES):
            frame=make_frame(base,i,source)
            if i in ss: frames.append((i,frame.copy()))
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        if process.wait()!=0:raise RuntimeError(process.stderr.read().decode('utf8',errors='replace'))
    except Exception:
        process.kill();raise
    if contact:
        sheet=Image.new('RGB',(W*3,H*2),'#06101C')
        for k,(_,img) in enumerate(frames):sheet.paste(img,((k%3)*W,(k//3)*H))
        sheet.save(contact)
    h=hashlib.sha256(out.read_bytes()).hexdigest()
    return {'video':str(out),'sha256':h,'frames_expected':FRAMES,'duration_expected':SEC,'fps_expected':FPS,'resolution_expected':[FULL_W,FULL_H],'narration':'NONE','audio':'NONE','publication':'BLOCKED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--contact',type=Path);a=ap.parse_args()
    print(json.dumps(run(a.out,a.evidence,a.contact),indent=2))