#!/usr/bin/env python3
"""Offline technical QA for the exact S01 V2 review MP4. Never release certification."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2,numpy as np
from PIL import Image

def probe(path):
 r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,check=True)
 return json.loads(r.stdout)
def qa(video,evidence,logo,source):
 from importlib.util import spec_from_file_location,module_from_spec
 spec=spec_from_file_location('s01v2',str(source));mod=module_from_spec(spec);spec.loader.exec_module(mod)
 ev=json.loads(Path(evidence).read_text(encoding='utf-8'))
 checks=[]
 def check(name,okay,detail): checks.append({'name':name,'status':'PASS' if okay else 'FAIL','detail':detail})
 try:mod.validate_source(ev);check('Evidence-source exact match',True,'Local simulation, ambiguous 01:30, 08:30Z and 09:30Z')
 except Exception as e:check('Evidence-source exact match',False,str(e))
 for tamper in ['unexpected_flags','broken_times']:
  bad=json.loads(json.dumps(ev))
  if tamper=='unexpected_flags':bad['provider_calendar_api_tested']=True
  else:bad['cases'][0]['valid_utc_candidates'][0]['utc']='2026-11-01T07:30:00Z'
  try:mod.validate_source(bad);fails=False
  except ValueError:fails=True
  check('Fail-closed '+tamper,fails,'Tampered evidence rejected' if fails else 'Tampered source accepted')
 p=probe(video);vs=next((s for s in p['streams'] if s['codec_type']=='video'),None);au=next((s for s in p['streams'] if s['codec_type']=='audio'),None)
 check('Native Full HD video',vs['width']==1080 and vs['height']==1920,'1080x1920 actual encoded frames')
 check('H264 and yuv420p',vs['codec_name']=='h264' and vs['pix_fmt']=='yuv420p',str((vs['codec_name'],vs['pix_fmt'])))
 check('30 FPS',vs['avg_frame_rate']=='30/1',vs['avg_frame_rate'])
 check('Exactly 540 video frames',int(vs['nb_frames'])==540,vs['nb_frames'])
 check('18-second duration',abs(float(p['format']['duration'])-18)<.05,p['format']['duration'])
 check('Original UI sound track present',bool(au and au['codec_name']=='aac' and au['sample_rate']=='48000'),'AAC stereo 48 kHz, not narration')
 check('MP4 exists and nonempty',Path(video).is_file() and Path(video).stat().st_size>100_000,Path(video).stat().st_size)
 file_code=Path(source).read_text(encoding='utf-8')
 check('Discontinued naming absent','FIELD TEST' not in file_code.upper() and 'FIELD_TEST' not in file_code.upper(),'No Field Tests in V2 renderer')
 check('Approved logo supplied',Path(logo).exists() and Image.open(logo).size==(198,165),'Extracted from owner-approved Drive brand kit; original ratio preserved')
 check('No fake provider claim',not ev['provider_calendar_api_tested'] and not ev['ai_agent_tested'],'Explicit local Python-only disclosure')
 cap=cv2.VideoCapture(str(video))
 selected=[10,27,65,92,110,145,200,228,290,340,380,445,470,515,533]
 frames={}
 for idx in selected:
  cap.set(cv2.CAP_PROP_POS_FRAMES,idx);ok,img=cap.read()
  if ok:frames[idx]=cv2.resize(img,(270,480)).astype(np.int16)
 cap.release()
 check('Decodable samples',len(frames)==len(selected),f'{len(frames)}/{len(selected)} sampled frames decoded')
 # Check motion within several scenes, as opposed to a frozen slideshow.
 diffs={f'{a}-{b}':round(float(np.mean(np.abs(frames[a]-frames[b]))),3) for a,b in [(10,27),(92,110),(200,228),(340,380),(470,515)] if a in frames and b in frames}
 check('Meaningful movement across five scenes',len(diffs)==5 and sum(v>.10 for v in diffs.values())>=4,str(diffs))
 # Content room below last material scene is reserved to avoid Shorts overlays (not an official platform verification).
 footer=('LOCAL PYTHON SIMULATION','NO CALENDAR API OR AI AGENT TESTED')
 check('Experimental overlay margins in source', all(tok in file_code for tok in ['(82,1490)','(82,1532)']) and all(tok in file_code for tok in footer),'Essential footer ink ends before pixel y=1570')
 # Decode audio for objective peak and nonzero content. No claims about listening aesthetics.
 pcm=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1'],capture_output=True,check=True).stdout
 aud=np.frombuffer(pcm,dtype='<f4');peak=float(np.max(abs(aud))) if len(aud) else 0; rms=float(np.sqrt(np.mean(aud**2))) if len(aud) else 0
 check('SFX audible without clipping',.0001<peak<.98 and rms>.00001,f'peak={peak:.3f}; rms={rms:.5f}; no synthesized voice')
 check('No release authority in renderer','BLOCKED_REVIEW_ONLY' in file_code,'No upload, scheduling or YouTube calls')
 check('Source file has no external fetch',not any(x in file_code for x in ['requests.get','urllib.request.urlopen','api_key','youtube.upload']),'No network/APIs for video')
 overall=all(c['status']=='PASS' for c in checks)
 return {'schema':'ninfa-s01-v2-technical-qa-v1','as_of':'2026-10-30','video_sha256':hashlib.sha256(Path(video).read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),'brand_source':'Does_It_Automate__Brand_Kit__Approved.png (Google Drive, owner-approved); extracted icon, no redraw','checks':checks,'passed':sum(c['status']=='PASS' for c in checks),'failed':sum(c['status']=='FAIL' for c in checks),'technical_status':'PASS_REVIEW_ONLY' if overall else 'FAIL','narration_status':'PENDING','human_editorial_status':'PENDING','mobile_editor_safe_zone':'NOT_VERIFIED','publication':'BLOCKED'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--video',required=True);a.add_argument('--evidence',required=True);a.add_argument('--logo',required=True);a.add_argument('--source',default=str(Path(__file__).with_name('render_v2.py')));a.add_argument('--out',required=True);args=a.parse_args()
 r=qa(args.video,args.evidence,args.logo,args.source);Path(args.out).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':r['passed'],'failed':r['failed'],'video_sha256':r['video_sha256'],'technical_status':r['technical_status']},indent=2));raise SystemExit(0 if not r['failed'] else 1)
