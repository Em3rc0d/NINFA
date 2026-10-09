#!/usr/bin/env python3
"""Motion v1.5: bounded evidence-backed vertical event-replay scene.

CPU-only Pillow -> FFmpeg. Review-only output, no audio, network, publishing or TTS.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

W,H,FPS = 540,960,30
BG=(8,15,27); PANEL=(18,30,48); CYAN=(47,204,242); LIME=(80,217,153)
AMBER=(244,174,100); INK=(239,246,253); MUTED=(144,168,190); GRID=(18,29,43)
FONT='/usr/share/fonts/truetype/lato/Lato-Heavy.ttf'
REG='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
MONO='/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf'
if not Path(MONO).exists(): MONO='/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'

def F(n,bold=False,mono=False):return ImageFont.truetype(MONO if mono else FONT if bold else REG,n)
def clamp(x):return min(1,max(0,x))
def ease(x):x=clamp(x);return x*x*(3-2*x)
def seg(t,a,b):return ease((t-a)/(b-a))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def check_proof(p):
    if set(p)!={'schema','experimental_mode','description','inputs','naive','guarded','limitations','api_spend_usd','github_actions_media','published','sha256_content'}:raise ValueError('unknown evidence fields')
    proof=dict(p);h=proof.pop('sha256_content')
    if hashlib.sha256(canonical(proof).encode()).hexdigest()!=h:raise ValueError('tampered evidence receipt')
    if p['schema']!='local-replay-v1' or p['experimental_mode']!='LOCAL_SYNTHETIC_SEQUENTIAL':raise ValueError('only local sequential replay allowed')
    if p['inputs']!={'event_key':'evt_local_001','sequence':['evt_local_001','evt_local_001']}:raise ValueError('unexpected event fixture')
    if p['naive']['attempts']!=2 or p['naive']['new_actions']!=2 or p['naive']['inserted']!=[True,True]:raise ValueError('naive count not reproduced')
    if p['guarded']['attempts']!=2 or p['guarded']['new_actions']!=1 or p['guarded']['inserted']!=[True,False]:raise ValueError('guarded count not reproduced')
    if type(p['api_spend_usd']) is not int or p['api_spend_usd']!=0 or p['github_actions_media'] is not False or p['published'] is not False:raise ValueError('restricted policy')
    return p

def check_story(m,p):
    if type(m) is not dict or set(m)!={'schema','id','brand','language','format','status','family','evidence_sha256','headlines','voice_script','caption_plan','rules'}:raise ValueError('unknown storyboard keys')
    if m['schema']!='ninfa-motion-v1.5' or m['brand']!='DoesItAutomate' or m['language']!='en' or m['family']!='event_replay':raise ValueError('unsupported brand or family')
    if m['status']!='EVIDENCE_BACKED_LOCAL' or m['evidence_sha256']!=p['sha256_content']:raise ValueError('storyboard evidence mismatch')
    if m['format']!={'width':1080,'height':1920,'fps':30,'frames':720}:raise ValueError('only 24 second local review supported')
    if m['rules']!={'paid_api_usd':0,'media_actions':False,'publish_authority':'NONE','raw_voice_in_git':False}:raise ValueError('runtime or policy not approved')
    if type(m['id']) is not str or not m['id'].replace('-','').isalnum() or len(m['id'])>64:raise ValueError('unsafe ID')
    if type(m['headlines']) is not list or len(m['headlines'])!=5:raise ValueError('five stage heads required')
    for line in m['headlines']:
      if type(line) is not str or not 2<=len(line)<=40 or any(x in line for x in ('\\','{','}','<','>','\n')):raise ValueError('unsafe headline')
      if F(24,True).getlength(line)>465:raise ValueError('headline too wide for safe area')
    if type(m['voice_script']) is not str or len(m['voice_script'])>440 or not m['voice_script'].strip():raise ValueError('missing voice script')
    cues=m['caption_plan'];last=0
    if type(cues) is not list or not 3<=len(cues)<=12:raise ValueError('invalid caption plan')
    for c in cues:
      if type(c) is not dict or set(c)!={'start_frame','end_frame','text'}:raise ValueError('bad caption object')
      a,b=c['start_frame'],c['end_frame']
      if type(a) is not int or type(b) is not int or not last<=a<b<=720:raise ValueError('bad caption time')
      if type(c['text']) is not str or not c['text'] or len(c['text'])>86 or any(x in c['text'] for x in ('{','}','\\','<','>')):raise ValueError('unsafe caption')
      last=b
    return m

def rounded(d,xy,rad=14,fill=PANEL,outline=None,width=2):d.rounded_rectangle(tuple(round(z) for z in xy),radius=rad,fill=fill,outline=outline,width=width)
def txt(d,x,y,s,n=19,c=INK,bold=False,mono=False):d.text((x,y),s,font=F(n,bold,mono),fill=c)
def mid(d,x,y,s,n=19,c=INK,bold=False):
    font=F(n,bold);w=d.textbbox((0,0),s,font=font)[2];d.text((round(x-w/2),y),s,font=font,fill=c)
def event_token(d,x,y,name,accent=CYAN,alpha=1):
    if alpha<=0:return
    rounded(d,(x,y,x+136,y+38),10,(20,44,59),accent,2)
    txt(d,x+12,y+10,name,13,INK,True,True)

def frame(m,p,index):
    t=(index+.5)/FPS
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    for x in range(0,W,38):d.line((x,0,x,H),fill=GRID)
    for y in range(0,H,38):d.line((0,y,W,y),fill=GRID)
    # No logo substitute; small plain channel text only.
    txt(d,42,94,'DOES IT AUTOMATE?  /  LOCAL LAB',15,CYAN,True)
    mid(d,270,137,'ONE EVENT. TWO DELIVERIES.',28,INK,True)
    # Keep vertical 185..253 free for future v1.3 top-aligned subtitles.
    rounded(d,(32,263,508,806),22,(12,26,41),(40,67,88),2)
    txt(d,52,282,'EVENT INPUT',15,CYAN,True)
    txt(d,52,309,'evt_local_001',16,INK,False,True)
    rr=(lambda x: x)
    rounded(d,(348,294,483,335),12,(25,43,60),(45,73,94))
    mid(d,414,302,'REPLAY x2',17,INK,True)
    # Event packets advance to the same database side with staggered timing.
    d.line((52,364,492,364),fill=(47,82,101),width=4)
    for i in range(2):
        progress=seg(t, .7+i*1.45, 4.4+i*1.45)
        if progress>0:
            x=56+388*progress
            dot=(CYAN if i==0 else AMBER)
            d.ellipse((x-10,354,x+10,374),fill=dot)
            if progress<.995:txt(d,max(55,x-30),342,'#'+str(i+1),12,dot,True)
    txt(d,52,395,'SAME PAYLOAD   •   TWO SEQUENTIAL CALLS',13,MUTED,False,True)
    # Continuous lanes remain visible while emphasis changes.
    lanes=[('NO UNIQUE KEY',AMBER,438),('UNIQUE EVENT KEY',LIME,576)]
    for k,(name,color,yy) in enumerate(lanes):
        focused=(0.14 if (k==0 and 5<t<10) or (k==1 and 10<=t<19) else 0)
        weight=2+(1 if focused else 0)
        rounded(d,(48,yy,492,yy+124),14,(19,35,52),color if focused else (55,75,93),weight)
        txt(d,68,yy+13,name,19,color,True)
        txt(d,68,yy+41,'SQLite actions table',14,MUTED)
        txt(d,68,yy+93,'STORED',13,MUTED,True)
        count=p['naive']['new_actions'] if k==0 else p['guarded']['new_actions']
        # Counts remain zero until narrated beat, then animate upward once.
        if k==0:shown=round(count*seg(t,5.0,8.1))
        else:shown=round(count*seg(t,13.5,15.1))
        txt(d,138,yy+79,str(shown),32,color,True)
        # Distinct rows with subtle activity for actions being inserted.
        for j in range(count):
            visible=seg(t,5.5+j*1.1,6.2+j*1.1) if k==0 else seg(t,13.3,14.1)
            if visible>.02:
                y=yy+66
                x=245+j*91
                rounded(d,(x,y,x+82,y+35),10,(37,67,71) if k==1 else (72,52,47))
                txt(d,x+10,y+9,'ACTION '+str(j+1),11,INK,True)
    # Policy barrier appears precisely as second guarded retry gets rejected.
    if 15<=t<19:
        q=seg(t,15,16)
        rounded(d,(256,711,485,746),11,(31,63,57),(80,217,153),2)
        txt(d,266,720,'REPLAY SKIPPED',15,LIME,True)
        if q>0.5:txt(d,462,715,'✓',17,LIME,True)
    elif t>=19:
        # The final beat makes the untested concurrency boundary explicit.
        # One label appears first, then the missing test is highlighted.
        q1=seg(t,19.1,20.3);q2=seg(t,20.5,22.2)
        rounded(d,(65,708,260,749),10,(28,63,53),LIME,2)
        txt(d,75,714,'SEQUENTIAL  ✓',15,LIME,True)
        txt(d,75,732,'TESTED',11,INK,True)
        if q2>0:
            warn=(int(244*q2),int(174*q2),int(100*q2))
            rounded(d,(269,708,479,749),10,(68,47,40),warn,2)
            txt(d,279,714,'CONCURRENT  ?',15,AMBER,True)
            txt(d,279,732,'NOT TESTED',11,INK,True)
    # Compares both in a persistent summary ribbon.
    stage=0 if t<5 else 1 if t<10 else 2 if t<14 else 3 if t<19 else 4
    stage_head=m['headlines'][stage]
    rounded(d,(49,759,491,796),10,(25,46,65))
    mid(d,270,765,stage_head,19,LIME if stage>=3 else CYAN,True)
    # Timebase progress / actual 24s media progress. Not a fake benchmark meter.
    d.line((53,830,488,830),fill=(45,60,79),width=4)
    d.line((53,830,53+(435*t/24),830),fill=CYAN,width=5)
    # Bottom footnote is ALWAYS visible and tells provenance / limits.
    txt(d,51,844,'LOCAL SQLITE REPLAY  •  SYNTHETIC INPUT',13,MUTED,True)
    txt(d,51,871,'Sequential only. Concurrency not tested.',15,AMBER)
    return im

def ffprobe(path):
    result=subprocess.run(['ffprobe','-v','error','-count_frames','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames','-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(result.stdout)

def render(story,evidence,out):
    check_proof(evidence);check_story(story,evidence)
    out=Path(out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate','30','-i','pipe:0','-vf','scale=1080:1920:flags=bicubic,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','20','-threads','2','-frames:v','720','-an','-metadata','creation_time=1970-01-01T00:00:00Z','-movflags','+faststart',str(out)]
    start=time.perf_counter()
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
      for i in range(720):p.stdin.write(frame(story,evidence,i).tobytes())
      p.stdin.close()
      err=p.stderr.read().decode(errors='replace')
      code=p.wait(timeout=150)
      if code:raise RuntimeError('ffmpeg failed: '+err[-1300:])
    finally:
      if p.poll() is None:p.kill()
    media=ffprobe(out)
    tracks=media['streams']
    if len(tracks)!=1 or (tracks[0]['codec_type'],tracks[0]['codec_name'],tracks[0]['width'],tracks[0]['height'],tracks[0]['r_frame_rate'],tracks[0]['nb_read_frames'])!=('video','h264',1080,1920,'30/1','720') or abs(float(media['format']['duration'])-24)>0.07:raise ValueError('MP4 structural failure')
    receipt={'schema':'ninfa-motion-v1.5-result','story_id':story['id'],'status':'TECHNICAL_PASS_REVIEW_ONLY','release_state':'BLOCKED','evidence_sha256':evidence['sha256_content'],'story_sha256':hashlib.sha256(canonical(story).encode()).hexdigest(),'mp4_sha256':sha(out),'seconds':24,'frames':720,'elapsed_s':round(time.perf_counter()-start,2),'narration':'PENDING_OWNER_RECORDING','caption_timing':'PLANNED_NOT_AUDIO_ALIGNED','platform_safe_zone':'NOT_CERTIFIED','published':False,'paid_api_usd':0}
    (out.parent/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt

def main():
    a=argparse.ArgumentParser();a.add_argument('--story',required=True);a.add_argument('--evidence',required=True);a.add_argument('--out',required=True);args=a.parse_args()
    m=json.loads(Path(args.story).read_text());p=json.loads(Path(args.evidence).read_text());print(json.dumps(render(m,p,Path(args.out)),indent=2))
if __name__=='__main__':main()
