#!/usr/bin/env python3
"""One-command OFFLINE evidence -> scene -> MP4 review export; no voice synthesizer/publisher."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
from replay_lab import generate
from studio import check_proof, check_story, render

HERE=Path(__file__).resolve().parent

def run(out:Path, dry_run=False):
    out=out.expanduser().resolve()
    if HERE in out.parents or out==HERE:raise ValueError('media output must not be in source folder')
    story=json.loads((HERE/'story.json').read_text(encoding='utf8'))
    with TemporaryDirectory(prefix='ninfa-replay-') as temporary:
        proof=generate(Path(temporary))
    check_proof(proof);check_story(story,proof)
    if dry_run:return {'status':'PREFLIGHT_PASS_REVIEW_ONLY','evidence_sha256':proof['sha256_content'],'story':story['id'],'publish':False}
    out.mkdir(parents=True,exist_ok=True)
    evidence=out/'evidence';evidence.mkdir(exist_ok=True)
    (evidence/'replay_evidence.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    receipt=render(story,proof,out/'the-duplicate-webhook_motion-v1.5_SILENT.mp4')
    # Script is the only actual audio contract until user records a new English narration.
    (out/'VOICEOVER_READ_ME.txt').write_text(
        'Does It Automate? — THE DUPLICATE WEBHOOK\n\n'+story['voice_script']+'\n\n'+
        'VOICE DIRECTION: conversational English; emphasize TWICE, TWO ACTIONS, ONE ACTION;\n'
        'slow the ending to stress the sequential/concurrent limitation.\n'
        'Do not force this take into 24 seconds: align scenes to your natural recording.\n'
        'CAPTIONS: frame times in story.json are only draft; adjust to real WAV.\n',encoding='utf8')
    def srt_time(frames):
        ms=round(frames*1000/30)
        return f'{ms//3600000:02}:{(ms//60000)%60:02}:{(ms//1000)%60:02},{ms%1000:03}'
    (out/'SUBTITLES_PLANNED_NOT_ALIGNED.srt').write_text('\n'.join(f"{i}\n{srt_time(c['start_frame'])} --> {srt_time(c['end_frame'])}\n{c['text']}\n" for i,c in enumerate(story['caption_plan'],1)),encoding='utf8')
    (out/'STORYBOARD.json').write_text(json.dumps(story,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--dry-run',action='store_true')
    a=p.parse_args();print(json.dumps(run(Path(a.out),a.dry_run),indent=2))
