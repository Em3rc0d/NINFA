"""Read-only technical QA for NINFA-S01 SILENT video review, not release certification."""
from pathlib import Path
import argparse
from PIL import Image, ImageChops
import hashlib
import json
import subprocess
import tempfile

parser=argparse.ArgumentParser()
parser.add_argument('--video',type=Path,required=True)
parser.add_argument('--evidence',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
a=parser.parse_args()
VIDEO,EVIDENCE,OUTPUT=a.video,a.evidence,a.out

def probe():
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,nb_frames,avg_frame_rate,pix_fmt','-of','json',str(VIDEO)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def frame(sec,out):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(VIDEO),'-frames:v','1',str(out)],check=True)
    return Image.open(out).convert('RGB').copy()

data=json.loads(EVIDENCE.read_text())
p=probe(); v=[x for x in p['streams'] if x['codec_type']=='video'][0]
a=[x for x in p['streams'] if x['codec_type']=='audio']
checks={
    'source_is_local_simulation':data['provider_calendar_api_tested'] is False and data['ai_agent_tested'] is False,
    'evidence_has_two_valid_utc_instants':[x['utc'] for x in data['cases'][0]['valid_utc_candidates']]==['2026-11-01T08:30:00Z','2026-11-01T09:30:00Z'],
    'format_h264':v['codec_name']=='h264',
    'resolution_1080x1920':(v['width'],v['height'])==(1080,1920),
    'framerate_30':v['avg_frame_rate']=='30/1',
    'frames_540':int(v['nb_frames'])==540,
    'duration_18_seconds':abs(float(p['format']['duration'])-18)<0.02,
    'silent_review_has_no_audio':len(a)==0,
    'nonempty_encoded_video':VIDEO.stat().st_size>150_000,
}
with tempfile.TemporaryDirectory() as tmp:
    seconds=[1.7,4.5,7.2,10.5,13.7,16.8]
    images=[frame(s,Path(tmp)/f'{i}.png') for i,s in enumerate(seconds)]
    def diff(x,y):
        # mean per-channel difference across a center crop containing explanatory content
        xa=x.crop((100,600,980,1390));ya=y.crop((100,600,980,1390))
        d=ImageChops.difference(xa,ya).convert('L')
        import PIL.ImageStat as S
        return S.Stat(d).mean[0]
    changes=[round(diff(a,b),2) for a,b in zip(images,images[1:])]
    checks['scene_transitions_visibly_distinct']=all(x>5 for x in changes)
    for i,img in enumerate(images):
        checks[f'sample_{i}_valid_image']=img.size==(1080,1920)
status='TECHNICAL_PASS_REVIEW_ONLY' if all(checks.values()) else 'TECHNICAL_FAIL'
report={
    'artifact_id':'NINFA-S01',
    'status':status,
    'artifact':VIDEO.name,
    'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
    'bytes':VIDEO.stat().st_size,
    'video':v,
    'audio_stream_count':len(a),
    'scene_transition_diff_luma':changes,
    'checks':checks,
    'checks_passed':sum(checks.values()),
    'checks_total':len(checks),
    'limitations':['No licensed/approved English narration or captions synchronized to audio.','No owner physical-device Shorts visual-guide QA.','Official logo not available locally: no recreated logo.','This is a video of Python timezone simulation; no calendar API or AI agent tested.','No publishing authorization; silent text-led preview for owner review only.'],
    'publishing_status':'BLOCKED',
}
OUTPUT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':status,'checks_passed':report['checks_passed'],'checks_total':report['checks_total'],'sha256':report['sha256'],'bytes':report['bytes'],'transition_diffs':changes},indent=2))
if status!='TECHNICAL_PASS_REVIEW_ONLY':raise SystemExit(1)