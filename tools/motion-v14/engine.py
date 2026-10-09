#!/usr/bin/env python3
"""NINFA Motion v1.4: bounded, zero-API, REVIEW-ONLY visual scene renderer.

Three parameterized composition families; not an arbitrary HTML/JS renderer or publisher.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS = 540,960,30
BG = (10,17,29)
CARD = (20,32,50)
INK = (237,244,252)
SUB = (148,169,189)
ACCENT = (39,199,239)
BLUE = (74,123,242)
GREEN = (65,218,158)
YELLOW = (252,197,95)
RED = (249,112,112)
FONTS = {
    'bold':'/usr/share/fonts/truetype/lato/Lato-Heavy.ttf',
    'regular':'/usr/share/fonts/truetype/lato/Lato-Regular.ttf',
    'medium':'/usr/share/fonts/truetype/lato/Lato-Semibold.ttf'
}
ALLOWED = {'schema','id','brand','language','format','policy','mode','family','title','eyebrow','message','labels','evidence'}
FAMILIES = {'cache_race','circuit_breaker','source_lineage','parallel_jobs'}
FRAME_MAX = 900

def require(test, msg):
    if not test: raise ValueError(msg)

def sha_bytes(b): return hashlib.sha256(b).hexdigest()

def sha_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def validate(m):
    require(type(m) is dict and set(m)==ALLOWED, 'unexpected/missing manifest keys')
    require(m['schema']=='ninfa-scene-v1.4.0', 'schema version')
    require(m['brand']=='DoesItAutomate' and m['language']=='en', 'brand and language fixed')
    require(type(m['id']) is str and len(m['id'])>=4 and len(m['id'])<=48 and all(c.islower() or c.isdigit() or c=='-' for c in m['id']), 'unsafe ID')
    fmt=m['format'];require(type(fmt) is dict and set(fmt)=={'width','height','fps','frames'} and fmt['width']==1080 and fmt['height']==1920 and fmt['fps']==30 and type(fmt['frames']) is int and 90<=fmt['frames']<=FRAME_MAX,'unsupported output geometry')
    p=m['policy'];require(type(p) is dict and set(p)=={'paid_api_usd','github_actions','publish_authority','allow_raw_voice'} and type(p['paid_api_usd']) is int and p['paid_api_usd']==0 and p['github_actions'] is False and p['publish_authority']=='NONE' and p['allow_raw_voice'] is False,'budget/voice/publish gate')
    require(m['mode'] in ('ILLUSTRATIVE_POC','EVIDENCE_BACKED'), 'mode')
    require(m['family'] in FAMILIES, 'unsupported visual family')
    if m['family']=='parallel_jobs':
        require(fmt['frames']==708 and m['mode']=='ILLUSTRATIVE_POC', 'parallel integration demo requires 708 frames and DEMO mode')
    else:
        require(fmt['frames']<=360, 'other visual families capped at 360 frames')
    require(type(m['title']) is str and 4<=len(m['title'])<=35 and '\n' not in m['title'], 'title length')
    require(type(m['eyebrow']) is str and 2<=len(m['eyebrow'])<=36 and '\n' not in m['eyebrow'], 'eyebrow length')
    require(type(m['message']) is str and 4<=len(m['message'])<=75 and '\n' not in m['message'], 'message length')
    require(all(c not in str(m[k]) for c in ('{','}','\\','<','>') for k in ('title','eyebrow','message')),'embedded instructions forbidden')
    lab=m['labels'];require(type(lab) is list and len(lab)==3 and all(type(x) is str and 2<=len(x)<=28 and '\n' not in x for x in lab),'3 labels needed')
    evidence=m['evidence'];require(type(evidence) is dict and set(evidence)=={'source','measurements','disclosure'},'evidence structure')
    require(type(evidence['disclosure']) is str and 4<=len(evidence['disclosure'])<=56,'disclosure needed')
    if m['mode']=='EVIDENCE_BACKED':
        require(m['family']=='cache_race','evidence-renderer limited to verified cache fixture')
        require(evidence['source']=='NINFA/docs/contracts/decisions/MOTION_V1_3_LOCAL_FINISHING_2026-10-08.md','unreviewed provenance')
        require(evidence['measurements']=={'fresh_s':4.80,'cached_s':1.15},'unsupported metrics')
    else:
        require(evidence['source'] is None and evidence['measurements'] is None,'POC must not pretend evidence')
        require('DEMO' in evidence['disclosure'].upper(),'visible demo disclosure needed')
    # At authoring time reject content that cannot fit the declared mobile-safe layout.
    widths = ((m['title'], 38, True, 450), (m['eyebrow'],17,False,420),
              (m['message'],20,False,420), (evidence['disclosure'],13,False,420))
    for text,size,bold,maximum in widths:
        require(font(size,bold).getlength(text) <= maximum, 'text exceeds safe typography width')
    if m['family']=='circuit_breaker':
        require(all(font(16,True).getlength(x)<100 for x in lab), 'breaker label too wide')
    if m['family']=='source_lineage':
        require(all(font(25,False).getlength(x)<285 for x in lab), 'lineage label too wide')
    if m['family']=='parallel_jobs':
        require(all(font(18,True).getlength(x)<150 for x in lab), 'parallel labels too wide')
    return m

def font(s=30,bold=True): return ImageFont.truetype(FONTS['bold' if bold else 'regular'],s)
def smooth(x):x=min(1,max(0,x));return x*x*(3-2*x)
def ramp(t,a,b):return smooth((t-a)/(b-a))
def mix(a,b,r):return a+(b-a)*r

def centered(d, xy, text, size, fill=INK, bold=True):
    x,y=xy; f=font(size,bold);bbox=d.textbbox((0,0),text,font=f);wid=bbox[2]-bbox[0]
    d.text((int(x-wid/2),int(y)),text,font=f,fill=fill)

def label(d,xy,text,color=SUB,size=19):d.text(xy,text,font=font(size,False),fill=color)
def rr(d,box,r=16,fill=CARD,outline=None,width=2):d.rounded_rectangle(tuple(int(z) for z in box),radius=r,fill=fill,outline=outline,width=width)

def base(m,t):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    # Grid subtle static: provides spatial continuity, motion is inside scene modules.
    for x in range(0,W,45):d.line((x,0,x,H),fill=(15,26,39),width=1)
    for y in range(0,H,45):d.line((0,y,W,y),fill=(15,26,39),width=1)
    rr(d,(28,120,512,810),18,(12,23,37),(40,62,84),2)
    label(d,(55,145),m['eyebrow'],ACCENT,17)
    label(d,(55,165),'NINFA  /  MOTION STUDY',SUB,12)
    centered(d,(270,208),m['title'],38)
    # Fixed bottom-safe message. 960-height - 175px = y<=785 for essential content
    centered(d,(270,734),m['message'],20,SUB,False)
    label(d,(55,773),m['evidence']['disclosure'],YELLOW,13)
    # Progress reflects elapsed playback, not fake server metrics.
    d.line((58,794,485,794),fill=(37,55,75),width=4)
    d.line((58,794,58+427*t,794),fill=ACCENT,width=4)
    return im,d

def cache(d,m,t):
    # Persistent timebars with measured values, not render animation pretending benchmarking live.
    width=394;x=74;y0=290
    label(d,(x,y0),'ONE LOCAL HOST / OBSERVED RUN',SUB,16)
    for i,(key,val,color) in enumerate([(m['labels'][0],4.80,BLUE),(m['labels'][1],1.15,GREEN)]):
        y=y0+74+i*127
        label(d,(x,y),key,color,18)
        rr(d,(x,y+34,x+width,y+58),10,(29,46,65))
        # Both bars grow in real-time normalized comparison to observed values.
        fill_fraction = (val / 4.80) * ramp(t,0.18+i*.05,0.78)
        rr(d,(x,y+34,x+max(6,width*fill_fraction),y+58),10,color)
        label(d,(x+3,y+69),f'{val:.2f} s',INK,31)
    rr(d,(74,639,466,695),12,(17,52,55),(48,135,128))
    centered(d,(270,651),f"UNCHANGED INPUTS -> {m['labels'][2]}",19,GREEN)
    # Controlled comparator scanning point moves continuously across the same chart.
    cx=74+int(width*(0.05+0.90*t));d.ellipse((cx-4,403,cx+4,411),fill=ACCENT)

def breaker(d,m,t):
    # Horizontal response conduit that changes state across time.
    label(d,(77,283),'REQUEST ROUTING / SYNTHETIC EXAMPLE',SUB,16)
    for i,n in enumerate(m['labels']):
        x=78+i*151;y=390
        active = (i==0) or (i==1 and .13<t<.55) or (i==2 and t>=.55)
        color=ACCENT if active else (55,78,98)
        rr(d,(x,y,x+112,y+86),14,CARD,color,2)
        centered(d,(x+56,y+30),n,16,INK if active else SUB)
    for x in (190,341):d.line((x,433,x+38,433),fill=(70,116,143),width=3)
    dot_x=180+int(240*ramp(t,.12,.66));dot_y=433
    d.ellipse((dot_x-6,dot_y-6,dot_x+6,dot_y+6),fill=ACCENT)
    state='REQUEST SENT' if t<.3 else ('TIMEOUT' if t<.53 else 'CIRCUIT OPEN')
    color=ACCENT if t<.3 else (YELLOW if t<.53 else RED)
    rr(d,(76,535,466,619),12,(29,42,60))
    centered(d,(270,551),state,26,color)
    label(d,(94,632),'FAIL FAST / ROUTE TO SAFE PATH',SUB,17)
    # A single pulse on state change signals error/decision, not success of a real app.
    if .51<t<.59:d.ellipse((327,379,362,414),outline=RED,width=3)

def lineage(d,m,t):
    # Directed vertical proof graph / three distinct timed nodes.
    stages=['CLAIM','SOURCE','CHECK']; ys=[300,426,552]; colors=[BLUE,ACCENT,GREEN]
    label(d,(80,280),'TRACE THE EVIDENCE PATH',SUB,17)
    for i,(n,y,col) in enumerate(zip(stages,ys,colors)):
        a=ramp(t,.10+i*.22,.40+i*.22)
        color=tuple(int(mix(44,c,a)) for c in col)
        rr(d,(78,y+22,462,y+94),12,(17,30,47),color,2)
        label(d,(104,y+33),f'0{i+1}',color,18)
        label(d,(151,y+45),m['labels'][i],INK if a>.48 else SUB,25)
        if i<2:
            d.line((270,y+94,270,ys[i+1]+22),fill=ACCENT if a>.8 else (39,66,84),width=4)
            d.polygon([(264,ys[i+1]+12),(276,ys[i+1]+12),(270,ys[i+1]+22)],fill=ACCENT if a>.8 else (39,66,84))
    rr(d,(78,682,462,714),10,(31,52,66))
    label(d,(95,689),'NO UNVERIFIED CLAIMS',YELLOW,17)

def stage_window(secs,a,b):
    return ramp(secs,a,b)

def parallel_jobs(d,m,t):
    # Dedicated continuous interface aligned to real owner's English narration,
    # reused for ENGINE INTEGRATION testing, not a claim of new independent benchmark.
    sec=t*708/30
    rr(d,(46,263,494,679),18,(17,29,46),(45,77,99),2)
    label(d,(67,279),'3 SIMULATED INDEPENDENT WAITS',SUB,16)
    # Live elapsed-time ribbon, not an external service timer.
    phase='QUEUE' if sec<2 else ('SEQUENTIAL' if sec<7.5 else ('PARALLEL' if sec<12.6 else ('RESULT' if sec<16.7 else ('NO AI MODEL' if sec<19.3 else 'CONDITION'))))
    rr(d,(67,312,473,348),10,(25,45,65))
    centered(d,(270,317),phase,19,ACCENT)
    # Two persistent comparator bays. The stage changes, but the screen stays put.
    labels=['JOB A','JOB B','JOB C']
    for i,name in enumerate(labels):
        y=385+i*63
        color=[ACCENT,BLUE,GREEN][i]
        label(d,(74,y),name,SUB,17)
        rr(d,(154,y-1,460,y+21),9,(31,47,64))
        # During 2.0–7.3, execute jobs in sequence. During 7.4–12.3, concurrently.
        if sec<2.0: prog=0
        elif sec<7.5:
            starts=[2.0,3.88,5.53];ends=[3.88,5.53,7.5]
            prog=ramp(sec,starts[i],ends[i])
        elif sec<12.5:
            prog=ramp(sec,7.6,11.75-(i*.06))
        else: prog=1.0
        ww=max(0,300*prog)
        if ww>=10:rr(d,(154,y-1,154+ww,y+21),9,color)
        if prog>=.99:
            d.ellipse((464,y,479,y+15),fill=GREEN)
            centered(d,(471,y-1),'✓',15,BG)
        elif prog>.01:
            pulse=3+2*math.sin((sec*5+i))**2
            d.ellipse((154+ww-pulse,y+6-pulse/2,154+ww+pulse,y+6+pulse/2),fill=INK)
    rr(d,(67,598,473,648),11,(20,46,60))
    # Change only this metric row, to avoid slide-style hard cuts.
    if sec<7.5:
        left,right='SEQUENTIAL','0.34 s'
    elif sec<12.5:
        left,right='PARALLEL','0.14 s'
    elif sec<16.7:
        left,right='LOCAL SPEEDUP','~2.4x'
    elif sec<19.3:
        left,right='MODEL CALLS','NONE'
    else:
        left,right='ONLY WORKS IF','INDEPENDENT'
    label(d,(83,614),left,SUB,16)
    f=font(21);wide=d.textbbox((0,0),right,font=f)[2];d.text((450-wide,611),right,font=f,fill=YELLOW)
    # Soft active scanning line, not an arbitrary looping attention grab.
    sy=367+int(202*((sec%5)/5))
    d.line((70,sy,469,sy),fill=(29,62,77),width=1)

def base_parallel(m,t):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    for x in range(0,W,45):d.line((x,0,x,H),fill=(15,26,39),width=1)
    for y in range(0,H,45):d.line((0,y,W,y),fill=(15,26,39),width=1)
    rr(d,(28,113,512,814),18,(12,23,37),(40,62,84),2)
    label(d,(56,126),m['eyebrow'],ACCENT,17)
    centered(d,(270,152),m['title'],34)
    # Subtitle zone is deliberately reserved between header and comparator UI.
    label(d,(62,705),m['message'],SUB,18)
    label(d,(62,751),m['evidence']['disclosure'],YELLOW,13)
    d.line((59,789,481,789),fill=(36,55,77),width=4)
    d.line((59,789,59+422*t,789),fill=ACCENT,width=4)
    return im,d


FAMILY={'cache_race':cache,'circuit_breaker':breaker,'source_lineage':lineage,'parallel_jobs':parallel_jobs}

def create_frame(m,i):
    t=(i+.5)/m['format']['frames']
    im,d=(base_parallel(m,t) if m['family']=='parallel_jobs' else base(m,t))
    FAMILY[m['family']](d,m,t)
    return im

def cmd(args,timeout=180):
    p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
    if p.returncode:raise RuntimeError(f'Command failed: {p.stderr[-1800:]}')
    return p.stdout

def render(m,out):
    validate(m)
    for v in FONTS.values():require(Path(v).is_file(),f'font not installed: {v}')
    require(out.suffix=='.mp4','output must be mp4')
    out.parent.mkdir(parents=True,exist_ok=True)
    frames=m['format']['frames']; start=time.monotonic()
    # deterministic ffmpeg opts and metadata; no audio so finisher v1.3 can add owner voice later.
    flags=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}', '-framerate','30','-i','pipe:0',
           '-vf','scale=1080:1920:flags=bicubic,format=yuv420p', '-c:v','libx264','-preset','ultrafast','-crf','21','-threads','2','-frames:v',str(frames),
           '-an','-metadata','creation_time=1970-01-01T00:00:00Z','-movflags','+faststart',str(out)]
    p=subprocess.Popen(flags,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    try:
        for i in range(frames):p.stdin.write(create_frame(m,i).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace');code=p.wait(timeout=150)
        if code:raise RuntimeError(f'Encoder exited {code}: {err[-1200:]}')
    finally:
        if p.poll() is None:p.kill()
    data=json.loads(cmd(['ffprobe','-v','error','-count_frames','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames','-of','json',str(out)]))
    video=[s for s in data['streams'] if s['codec_type']=='video']
    require(len(video)==1 and len(data['streams'])==1,'expected video-only file')
    v=video[0];require((v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==('h264',1080,1920,'30/1',frames),'output codec/frame mismatch')
    receipt={'engine':'ninfa-motion-v1.4.0','id':m['id'],'status':'TECHNICAL_PASS_REVIEW_ONLY','release_state':'BLOCKED',
             'mode':m['mode'],'family':m['family'],'frames':frames,'duration_s':frames/30,'codec':'h264','audio':'NONE',
             'sha256':sha_file(out),'bytes':out.stat().st_size,'elapsed_s':round(time.monotonic()-start,2),
             'manifest_sha256':sha_bytes(json.dumps(m,sort_keys=True,separators=(',',':')).encode()),
             'editorial':'HUMAN_REVIEW_PENDING','platform_overlay':'NOT_CERTIFIED','voice_assets':'NONE'}
    (out.parent/(m['id']+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--manifest',required=True);a.add_argument('--out',required=True)
    o=a.parse_args()
    p=Path(o.manifest).resolve(strict=True)
    require(p.suffix=='.json' and p.is_file() and p.stat().st_size<30000,'use a small local JSON manifest')
    print(json.dumps(render(json.loads(p.read_text()),Path(o.out).expanduser().resolve()),indent=2))

if __name__=='__main__':main()
