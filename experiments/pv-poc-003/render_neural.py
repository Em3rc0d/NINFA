#!/usr/bin/env python3
"""PV-POC-003: fixed original 3-scene neural Spanish TTS proof. No network in this script."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import time

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "model.onnx"
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
SR = 48000
SECONDS = 10
SCENES = (
    {"id": "idea", "start": 0.15, "end": 3.00, "text": "De una idea, nace un video.", "subtitle": "De una idea, nace un video."},
    {"id": "flujo", "start": 3.13, "end": 7.00, "text": "Primero el guion, luego el diseño y el render.", "subtitle": "Primero el guion, luego el diseño\\Ny el render."},
    {"id": "qa", "start": 7.02, "end": 10.00, "text": "Y al final, validamos el resultado.", "subtitle": "Y al final, validamos el resultado."},
)

def run(args: list[str], *, input_text: str | None = None) -> str:
    result = subprocess.run(args, text=True, input=input_text, capture_output=True, check=False, timeout=180)
    if result.returncode:
        raise RuntimeError("Command failed: " + repr(args) + "\n" + result.stderr[-1800:])
    return result.stdout

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def srt_time(value: float) -> str:
    ms = int(round(value * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"

def ass_time(value: float) -> str:
    cs = int(round(value * 100))
    return f"{cs // 360000:01}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"

def synthesize() -> tuple[list[dict], Path]:
    assert MODEL.is_file() and MODEL.stat().st_size > 40_000_000, "Approved Piper voice model missing"
    master = np.zeros(SR * SECONDS, dtype=np.float64)
    timing = []
    for ix, scene in enumerate(SCENES, 1):
        raw = OUT / f"piper-{ix:02}.wav"
        run(["piper", "--model", str(MODEL), "--output_file", str(raw)], input_text=scene["text"] + "\n")
        meta = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(raw)]))
        natural_duration = float(meta["format"]["duration"])
        available = scene["end"] - scene["start"] - 0.06
        tempo = max(1.0, natural_duration / available)
        if tempo > 1.25:
            raise ValueError(f"Neural voice too long for {scene['id']}: {natural_duration:.2f}s vs {available:.2f}s; tempo={tempo:.3f}")
        processed = OUT / f"aligned-{ix:02}.wav"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(raw), "-af", f"atempo={tempo:.6f}", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(processed)])
        audio, sample_rate = sf.read(processed, dtype="float64")
        if sample_rate != SR or audio.ndim != 1:
            raise ValueError("Unexpected voice audio format")
        start_idx = round(scene["start"] * SR)
        end_idx = start_idx + len(audio)
        allowed_end = round(scene["end"] * SR)
        if end_idx > allowed_end:
            raise ValueError(f"Voice overlaps next scene: {scene['id']}")
        fade = min(900, len(audio) // 8)
        if fade > 0:
            audio[:fade] *= np.linspace(0, 1, fade)
            audio[-fade:] *= np.linspace(1, 0, fade)
        master[start_idx:end_idx] += audio
        rms = float(np.sqrt(np.mean(audio**2)))
        if rms < 0.003:
            raise ValueError(f"Missing audio in {scene['id']}")
        timing.append({**scene, "natural_voice_duration": round(natural_duration, 3), "aligned_voice_duration": round(len(audio) / SR, 3), "tempo_factor": round(tempo, 4), "voice_sha256": sha(raw), "rms": round(rms, 5)})
    peak = float(np.max(np.abs(master)))
    if not np.isfinite(peak) or peak < 0.03:
        raise ValueError("Invalid master signal")
    master *= min(0.92 / peak, 1.5)
    master_path = OUT / "narracion-neuronal.wav"
    sf.write(master_path, np.clip(master, -1, 1), SR, subtype="PCM_16")
    return timing, master_path

def captions(timing: list[dict]) -> Path:
    srt = []
    ass = [
        "[Script Info]", "Title: PV-POC-003 captions", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "ScaledBorderAndShadow: yes", "WrapStyle: 2", "",
        "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Captions,Lato,49,&H00F7F7F7,&H00FFFFFF,&H820B111F,&H820B111F,-1,0,0,0,100,100,0,0,3,13,0,2,90,90,380,1", "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for idx, scene in enumerate(timing, 1):
        begin = scene["start"]
        end = min(scene["end"], begin + scene["aligned_voice_duration"] + 0.05)
        srt.append(f"{idx}\n{srt_time(begin)} --> {srt_time(end)}\n{scene['subtitle'].replace(chr(92) + 'N', chr(10))}\n")
        ass.append(f"Dialogue: 0,{ass_time(begin)},{ass_time(end)},Captions,,0,0,0,,{scene['subtitle']}")
    (OUT / "subtitulos.srt").write_text("\n".join(srt), encoding="utf8")
    path = OUT / "subtitulos.ass"
    path.write_text("\n".join(ass) + "\n", encoding="utf8")
    return path

def video(voice_path: Path, ass_path: Path) -> Path:
    font = "/usr/share/fonts/truetype/lato/Lato-Heavy.ttf"
    if not Path(font).is_file():
        raise ValueError("Lato font missing on GitHub runner")
    def text(string: str, y: int, size: int, start: int, end: int) -> str:
        return "drawtext=" + ":".join((f"fontfile={font}", f"text='{string}'", f"fontsize={size}", "fontcolor=0xF2F7FB", "x=(w-text_w)/2", f"y={y}", f"enable='between(t,{start},{end})'"))
    filters = [
        text("DE IDEA", 575, 100, 0, 3), text("A VIDEO", 700, 123, 0, 3),
        text("UN FLUJO", 485, 90, 3, 7), text("TRES PASOS", 615, 112, 3, 7), text("GUION  -  DISENO  -  RENDER", 950, 46, 3, 7),
        text("10 SEGUNDOS", 560, 92, 7, 10), text("300 FRAMES", 700, 75, 7, 10), text("VOZ NEURONAL", 975, 55, 7, 10),
        f"ass={ass_path}:fontsdir=/usr/share/fonts/truetype/lato", "format=yuv420p",
    ]
    out = OUT / "pv-poc-003-voz-neuronal.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-f", "lavfi", "-i", "color=c=0x0b111f:s=1080x1920:r=30:d=10", "-i", str(voice_path), "-vf", ",".join(filters), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "21", "-pix_fmt", "yuv420p", "-threads", "2", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "1", "-t", str(SECONDS), "-movflags", "+faststart", "-metadata", "creation_time=1970-01-01T00:00:00Z", str(out)])
    return out

def check(path: Path) -> dict:
    data = json.loads(run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate,nb_read_frames,sample_rate", "-of", "json", str(path)]))
    v = [s for s in data["streams"] if s["codec_type"] == "video"]
    a = [s for s in data["streams"] if s["codec_type"] == "audio"]
    if len(v) != 1 or len(a) != 1:
        raise ValueError("Expected exactly one video and audio stream")
    if (v[0]["codec_name"], v[0]["width"], v[0]["height"], v[0]["r_frame_rate"], v[0]["nb_read_frames"]) != ("h264", 1080, 1920, "30/1", "300"):
        raise ValueError("Frame or video codec verification failed")
    if a[0]["codec_name"] != "aac" or abs(float(data["format"]["duration"]) - 10) > 0.06:
        raise ValueError("Sound or duration verification failed")
    return data

def main() -> None:
    began = time.perf_counter()
    timing, master = synthesize()
    subtitles = captions(timing)
    final = video(master, subtitles)
    probe = check(final)
    receipt = {"schema": "pv-poc-003/v1", "status": "TECHNICAL_PASS_HUMAN_AUDIO_QA_PENDING", "voice": "Piper es_MX-claude-high VITS", "model_sha256": sha(MODEL), "raw_segments": timing, "master_sha256": sha(master), "mp4_sha256": sha(final), "output_probe": probe, "elapsed_seconds": round(time.perf_counter() - began, 2), "human_naturalness_rating": "NOT_EVALUATED", "network_access": "GitHub runner installation/model fetch only; no network in renderer script", "scheduled": False, "published": False}
    (OUT / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps({"status": receipt["status"], "voice": receipt["voice"], "seconds": probe["format"]["duration"], "sha256": receipt["mp4_sha256"], "timing": [{"id": x["id"], "duration": x["natural_voice_duration"], "tempo": x["tempo_factor"]} for x in timing]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
