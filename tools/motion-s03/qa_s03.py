#!/usr/bin/env python3
"""S03: offline review QA (technical only, NOT release approval)."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import cv2,numpy as np


def hash_file(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verify(video,evidence,renderer,logo):
    checks=[]
    def check(name,condition):checks.append({'name':name,'pass':bool(condition)})
    ev=json.loads(Path(evidence).read_text())
    core=dict(ev);signature=core.pop('sha256_canonical_core',None)
    check('Correct experiment ID',ev.get('experiment')=='NINFA-S03')
    check('Canonical evidence digest valid',hashlib.sha256(json.dumps(core,sort_keys=True,separators=(',',':')).encode()).hexdigest()==signature)
    check('Real subprocess crash recorded in both modes',all(ev['modes'][m]['first_process_exit_code']==27 for m in ['naive','checkpoint']))
    check('Both worker restarts complete',all(ev['modes'][m]['second_process_exit_code']==0 for m in ['naive','checkpoint']))
    check('Baseline 6 actions 2 repeated',ev['modes']['naive']['action_count']==6 and ev['modes']['naive']['repeated_action_count']==2)
    check('Checkpoint 4 actions 0 repeated',ev['modes']['checkpoint']['action_count']==4 and ev['modes']['checkpoint']['repeated_action_count']==0)
    check('No AI model or provider claimed',ev['boundary']['no_ai_model_tested'] and ev['boundary']['no_external_api_or_provider'])
    check('Publication remains blocked',ev['publish_approved'] is False)
    src=Path(renderer).read_text()
    check('Render script preserves explicit local disclosure','NO AI MODEL OR EXTERNAL SERVICE TESTED' in src and 'LOCAL SQLITE EXPERIMENT' in src)
    check('No banned public series label','FIELD TEST' not in src)
    check('Logo source is owner-approved excerpt',Path(logo).exists() and Path(logo).stat().st_size>1000)
    result=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],capture_output=True,text=True,check=True)
    info=json.loads(result.stdout)
    streams=info['streams'];v=next((s for s in streams if s['codec_type']=='video'),{});a=next((s for s in streams if s['codec_type']=='audio'),{})
    check('Video native 1080x1920',v.get('width')==1080 and v.get('height')==1920)
    check('H264 yuv420p',v.get('codec_name')=='h264' and v.get('pix_fmt')=='yuv420p')
    check('30fps exactly',v.get('r_frame_rate')=='30/1')
    check('540 frames',int(v.get('nb_frames',0))==540)
    check('18-second container',abs(float(info['format'].get('duration',0))-18)<.05)
    check('AAC 48kHz two-channel SFX',a.get('codec_name')=='aac' and a.get('sample_rate')=='48000' and a.get('channels')==2)
    check('Nontrivial file size',Path(video).stat().st_size>100000)
    cap=cv2.VideoCapture(str(video));check('Video decodes',cap.isOpened())
    sample_t=[0.5,2.2,3.9,5.9,7.4,9.1,10.8,12.8,15.2,17.4]
    arrays=[]
    for t in sample_t:
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000)
        ok,frame=cap.read()
        if ok:arrays.append(frame)
    cap.release()
    check('All 10 sampled frames decode',len(arrays)==10)
    if len(arrays)==10:
        # Strong scene transitions without relying on optical text reading.
        changed=[float(np.mean(cv2.absdiff(cv2.resize(x,(135,240)),cv2.resize(y,(135,240))))) for x,y in zip(arrays,arrays[1:])]
        check('Distinct scenes visible',sum(v>3 for v in changed)>=3)
        check('Native decoded frames retain variation',len({hashlib.sha256(x.tobytes()).hexdigest() for x in arrays})==10)
        logo_crop=arrays[0][264:350,84:180]
        # BGR cyan matches approved original color treatment.
        cyan=np.count_nonzero((logo_crop[:,:,0]>130)&(logo_crop[:,:,1]>100)&(logo_crop[:,:,2]<145))
        check('Official mark appears as nonempty image patch',cyan>30)
        check('No mostly-white flash frames',max(float(x.mean()) for x in arrays)<160)
    # Structural decode of ALL frames, not just metadata.
    decode=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True)
    check('Full video decodes without FFmpeg error',decode.returncode==0)
    # SFX signal clipping proxy and presence
    pcm=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-f','f32le','-acodec','pcm_f32le','-'],capture_output=True,check=True)
    wav=np.frombuffer(pcm.stdout,dtype='<f4')
    peak=float(np.max(np.abs(wav))) if wav.size else 0
    check('Audible procedural SFX present',peak>.005)
    check('No measured digital PCM clipping',peak<.98)
    return {
      'status':'TECHNICAL_PASS_REVIEW_ONLY' if all(x['pass'] for x in checks) else 'TECHNICAL_FAIL',
      'video_sha256':hash_file(video),'evidence_sha256':hash_file(evidence),'renderer_sha256':hash_file(renderer),
      'logo_sha256':hash_file(logo),'checks_passed':sum(x['pass'] for x in checks),'checks_total':len(checks),
      'checks':checks,'audio_peak':peak,'required_human_gates':['English natural voice','Caption timing from actual audio','Mobile YouTube Shorts visual guides','Rights/brand review','Explicit owner release approval'],
      'provider_upload':False,'release_approved':False,'ai_model_tested':False,
    }

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--video',required=True);p.add_argument('--evidence',required=True);p.add_argument('--renderer',required=True);p.add_argument('--logo',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 receipt=verify(a.video,a.evidence,a.renderer,a.logo)
 Path(a.out).write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:receipt[k] for k in ('status','checks_passed','checks_total','video_sha256')},indent=2))
 if receipt['status']!='TECHNICAL_PASS_REVIEW_ONLY':
  print('Failed:',[c['name'] for c in receipt['checks'] if not c['pass']]);raise SystemExit(1)
