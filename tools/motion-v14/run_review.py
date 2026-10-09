#!/usr/bin/env python3
"""Offline, private, REVIEW-ONLY v1.4 silent scenes -> v1.3 narrated MP4.

This is a bounded integration adapter, not a production media orchestrator or publisher.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]


def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def check_story(scene: dict, finish: dict) -> None:
    if scene['brand'] != finish['channel'] or scene['language'] != finish['language']:
        raise ValueError('Brand/language mismatch between scene and finishing manifest')
    if scene['format']['frames'] != finish['duration_frames']:
        raise ValueError('Scene/finisher frame count mismatch')
    if scene['format']['fps'] != finish['fps']:
        raise ValueError('Scene/finisher fps mismatch')
    if scene['mode'] != finish['mode'] or scene['mode'] != 'ILLUSTRATIVE_POC':
        raise ValueError('Review integration is allowed only for labeled POC demos')
    if finish['publish_authority'] != 'NONE':
        raise ValueError('No publishing authority')


def child_source(file: Path) -> dict:
    return json.loads(file.read_text(encoding='utf-8'))


def run_job(scene_file: Path, finish_file: Path, private_voice: Path, out_dir: Path, *, force: bool=False) -> dict:
    import engine
    spec=importlib.util.spec_from_file_location('ninfa_motion_finisher', REPO_ROOT/'tools/motion-v13/finish.py')
    if spec is None or spec.loader is None: raise RuntimeError('Motion v1.3 local finisher missing')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    scene=engine.validate(child_source(scene_file))
    final=module.check_input(child_source(finish_file))
    check_story(scene,final)
    if not private_voice.is_file() or private_voice.suffix.lower() not in ('.wav','.m4a','.mp3'):
        raise ValueError('Private local narration WAV, M4A or MP3 required')
    if not scene_file.is_file() or not finish_file.is_file(): raise ValueError('Local manifests required')
    if out_dir == REPO_ROOT or REPO_ROOT in out_dir.parents:
        raise ValueError('Private outputs must be outside the NINFA checkout')
    out_dir.mkdir(parents=True,exist_ok=True)
    visual_dir=out_dir/'clean'
    visual_dir.mkdir(exist_ok=True)
    clean=visual_dir/(scene['id']+'.mp4')
    receipt=visual_dir/(scene['id']+'.receipt.json')
    # Reuse visual only when both exact manifest digest and stored MP4 match.
    want=engine.sha_bytes(json.dumps(scene,sort_keys=True,separators=(',',':')).encode())
    visual_hit=False
    if not force and clean.is_file() and receipt.is_file():
        try:
            previous=json.loads(receipt.read_text())
            visual_hit=(previous.get('manifest_sha256')==want and previous.get('sha256')==sha(clean)
                        and previous.get('status')=='TECHNICAL_PASS_REVIEW_ONLY'
                        and previous.get('release_state')=='BLOCKED')
        except (OSError, ValueError):visual_hit=False
    if not visual_hit: engine.render(scene,clean)
    # ffprobe gate and safe audio/caption wrapper run inside existing v1.3 module.
    combined=module.assemble(final,clean,private_voice,out_dir/'finished',force=force)
    # Never serialize or publish the private source file path or private voice SHA.
    return {'status':combined['status'],'review_only':True,'release_state':'BLOCKED',
            'visual_reused':visual_hit,'final_cached':combined.get('cache_hit',False),
            'frames':combined['frames'],'duration_seconds':combined['duration'],
            'audio_codec':combined.get('audio_codec','aac'),
            'output_name':final['id']+'.mp4'}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scene',required=True);p.add_argument('--finish',required=True)
    p.add_argument('--voice',required=True);p.add_argument('--out',required=True)
    p.add_argument('--force',action='store_true')
    a=p.parse_args()
    for name in ('scene','finish'):
        q=Path(getattr(a,name)).expanduser().resolve(strict=True)
        if q.suffix.lower()!='.json' or q.stat().st_size>30000:raise ValueError('Expected small local JSON manifest')
        setattr(a,name,q)
    voice=Path(a.voice).expanduser().resolve(strict=True)
    result=run_job(a.scene,a.finish,voice,Path(a.out).expanduser().resolve(),force=a.force)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
