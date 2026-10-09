#!/usr/bin/env python3
"""Motion v1.3: offline, review-only AV finisher. Does not build scenes or publish."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

FPS = 30
W, H = 1080, 1920
MAX_FRAMES = 1800  # shorts only: <= 60s


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def local_file(path: str, extensions: set[str]) -> Path:
    p = Path(path).expanduser().resolve(strict=True)
    if not p.is_file() or p.suffix.lower() not in extensions or p.stat().st_size > 500_000_000:
        raise ValueError('Input must be a supported local file <= 500 MB')
    return p


def run(args: list[str], *, cwd: Path | None = None, timeout: int = 300) -> str:
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
    if p.returncode:
        raise RuntimeError(f'Command exit {p.returncode}: {p.stderr[-1400:]}')
    return p.stdout


def probe(path: Path) -> dict:
    return json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_entries',
                           'format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames,sample_rate',
                           '-of', 'json', str(path)], timeout=150))


def check_input(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError('Manifest must be an object')
    allowed = {'schema', 'channel', 'language', 'id', 'mode', 'fps', 'width', 'height',
               'duration_frames', 'narration_source', 'captions', 'paid_api_usd',
               'github_actions_for_media', 'publish_authority'}
    if set(data) != allowed:
        raise ValueError('Unexpected or missing manifest keys')
    if (data['schema'], data['channel'], data['language']) != ('motion-v1.3-finish', 'DoesItAutomate', 'en'):
        raise ValueError('Only NINFA English DoesItAutomate supported')
    if data['mode'] != 'ILLUSTRATIVE_POC':
        raise ValueError('Finisher currently permits review-only illustrative media; evidence-backed mode not implemented')
    if (data['fps'], data['width'], data['height']) != (FPS, W, H):
        raise ValueError('Wrong format')
    n = data['duration_frames']
    if type(n) is not int or not 1 <= n <= MAX_FRAMES:
        raise ValueError('Frame count out of range')
    if data['narration_source'] not in ('OWNER_HUMAN', 'LOCAL_CHATTERBOX', 'LOCAL_KOKORO'):
        raise ValueError('Narration origin not approved')
    if data['paid_api_usd'] != 0 or data['github_actions_for_media'] is not False or data['publish_authority'] != 'NONE':
        raise ValueError('API/CI/publishing not authorized')
    if not isinstance(data['id'], str) or re.fullmatch(r'[a-z0-9-]{3,64}', data['id']) is None:
        raise ValueError('Unsafe ID')
    segments = data['captions']
    if not isinstance(segments, list) or not 1 <= len(segments) <= 40:
        raise ValueError('Captions required')
    prev = 0
    for seg in segments:
        if not isinstance(seg, dict) or set(seg) != {'start_frame', 'end_frame', 'text'}:
            raise ValueError('Malformed caption')
        a, b, s = seg['start_frame'], seg['end_frame'], seg['text']
        if type(a) is not int or type(b) is not int or not (prev <= a < b <= n):
            raise ValueError('Caption overlap/bounds')
        if not isinstance(s, str) or not s.strip() or len(s) > 140 or len(s.split('\n')) > 2:
            raise ValueError('Caption length/line count')
        if any(ord(ch) < 32 and ch != '\n' for ch in s) or any(c in s for c in '{}\\'):
            raise ValueError('Unsafe ASS caption control characters')
        prev = b
    return data


def ass_stamp(frame: int) -> str:
    cs = round(frame * 100 / FPS)
    return f'{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}'


def create_captions(manifest: dict, output_dir: Path) -> Path:
    # Generate our own ASS file; never execute untrusted ASS override codes.
    head = [
        '[Script Info]', 'Title: Motion v1.3 private local review', 'ScriptType: v4.00+',
        'PlayResX: 1080', 'PlayResY: 1920', 'WrapStyle: 2', 'ScaledBorderAndShadow: yes', '',
        '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        'Style: Narration,Lato,54,&H00F6F9FE,&H00FFFFFF,&H90101828,&H98101828,-1,0,0,0,100,100,0,0,3,12,0,8,80,80,380,1',
        '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]
    for c in manifest['captions']:
        safe = c['text'].replace('\n', r'\N')
        head.append(f"Dialogue: 0,{ass_stamp(c['start_frame'])},{ass_stamp(c['end_frame'])},Narration,,0,0,0,,{safe}")
    dest = output_dir / 'captions.generated.ass'
    dest.write_text('\n'.join(head) + '\n', encoding='utf-8')
    return dest


def assert_visual(p: dict, frames: int) -> None:
    vids = [x for x in p['streams'] if x['codec_type'] == 'video']
    if len(vids) != 1:
        raise ValueError('Video must have one visual stream')
    v = vids[0]
    if (v.get('width'), v.get('height'), v.get('r_frame_rate'), int(v.get('nb_read_frames', -1))) != (W, H, '30/1', frames):
        raise ValueError('Visual source mismatch: expected 1080x1920/30fps/exact frames')


def assemble(manifest: dict, visual: Path, voice: Path, out: Path, *, dry_run: bool = False) -> dict:
    check_input(manifest)
    assert_visual(probe(visual), manifest['duration_frames'])
    voice_probe = probe(voice)
    if not any(s['codec_type'] == 'audio' for s in voice_probe['streams']):
        raise ValueError('No narration stream')
    voice_duration = float(voice_probe['format']['duration'])
    if voice_duration + 0.25 < manifest['captions'][-1]['end_frame'] / FPS:
        raise ValueError('Voice shorter than final subtitle')
    duration = manifest['duration_frames'] / FPS
    plan = {'id': manifest['id'], 'status': 'PREFLIGHT_PASS', 'duration': duration,
            'frames': manifest['duration_frames'], 'visual_sha256': digest(visual),
            'voice_sha256': digest(voice), 'review_only': True}
    if dry_run:
        return plan
    out.mkdir(parents=True, exist_ok=True)
    if not out.is_dir():
        raise ValueError('Invalid output directory')
    captions = create_captions(manifest, out)
    finished = out / (manifest['id'] + '.mp4')
    command = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
        '-i', str(visual), '-i', str(voice),
        '-map', '0:v:0', '-map', '1:a:0',
        '-vf', 'ass=captions.generated.ass,format=yuv420p',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-threads', '2',
        '-frames:v', str(manifest['duration_frames']), '-r', str(FPS),
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
        '-ar', '48000', '-ac', '1', '-t', str(duration),
        '-metadata', 'creation_time=1970-01-01T00:00:00Z',
        '-movflags', '+faststart', str(finished),
    ]
    run(command, cwd=out, timeout=max(120, math.ceil(duration * 15)))
    result = probe(finished)
    assert_visual(result, manifest['duration_frames'])
    audio = [s for s in result['streams'] if s['codec_type'] == 'audio']
    if len(audio) != 1 or audio[0].get('codec_name') != 'aac' or abs(float(result['format']['duration']) - duration) > 0.07:
        raise RuntimeError('Finished audio/video QA failed')
    plan.update({'status': 'TECHNICAL_PASS_REVIEW_ONLY', 'output_sha256': digest(finished),
                 'output_bytes': finished.stat().st_size, 'audio_codec': 'aac',
                 'video_codec': 'h264', 'publish_authority': 'NONE', 'release_state': 'BLOCKED',
                 'subtitle_status': 'MANUAL_PHRASE_TIMING_NOT_WORD_CERTIFIED',
                 'human_editorial_qa': 'PENDING', 'os_sandbox_certified': False})
    (out / 'receipt.json').write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--visual', required=True, help='Approved, clean local 1080x1920 MP4')
    parser.add_argument('--voice', required=True, help='Private local WAV/M4A/MP3, never committed')
    parser.add_argument('--out', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    m = json.loads(local_file(args.manifest, {'.json'}).read_text(encoding='utf-8'))
    result = assemble(m, local_file(args.visual, {'.mp4'}),
                      local_file(args.voice, {'.wav', '.m4a', '.mp3'}),
                      Path(args.out).expanduser().resolve(), dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
