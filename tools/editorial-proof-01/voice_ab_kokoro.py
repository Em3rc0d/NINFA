#!/usr/bin/env python3
"""Private offline-after-model-download A/B audition of Kokoro presets.

No reference voice, voice cloning, paid API, secret, auto-publish or video edit.
Requires WSL/Linux Python 3.11/3.12, espeak-ng and Kokoro installed independently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LANGUAGE = "a"  # American English; matches official Kokoro preset codes
VOICES = ("am_michael", "af_heart")
AUDITION_SCRIPT = (
    "I replayed the same synthetic event twice. "
    "Without a unique key, SQLite stored two actions. "
    "With the guard, it stored one. "
    "Concurrency was not tested."
)


def check_destination(path: Path) -> Path:
    output = path.expanduser().resolve()
    if output == REPO_ROOT or REPO_ROOT in output.parents:
        raise ValueError("POLICY_BLOCKED: private audio output must be outside NINFA repository")
    if output.exists():
        raise ValueError("POLICY_BLOCKED: refusing to overwrite an existing audition folder")
    return output


def preview(out_dir: Path, dry_run: bool) -> dict:
    out = check_destination(out_dir)
    report = {
        "schema": "ninfa-kokoro-audition-v1",
        "purpose": "Private reference-free English voice A/B audition, NOT release",
        "voices": list(VOICES),
        "script": AUDITION_SCRIPT,
        "script_sha256": hashlib.sha256(AUDITION_SCRIPT.encode("utf8")).hexdigest(),
        "backend": "hexgrad/Kokoro-82M; model/voices per upstream license",
        "expected_sample_rate_hz": 24000,
        "requires_reference_voice": False,
        "publish_authority": "NONE",
        "status": "PREFLIGHT_ONLY" if dry_run else "RENDER_IN_PROGRESS",
    }
    if dry_run:
        return report

    # Delayed imports make --dry-run and test discovery work without model dependencies.
    try:
        import numpy as np
        import soundfile as sf
        from kokoro import KPipeline
    except ImportError as err:
        raise RuntimeError(
            "Kokoro dependencies missing. Use a separate WSL Python 3.11/3.12 venv: "
            "pip install 'kokoro>=0.9.2' soundfile; install espeak-ng first."
        ) from err
    pipeline = KPipeline(lang_code=LANGUAGE)
    audio_files = {}
    for voice in VOICES:
        samples = []
        for _gs, _ps, audio in pipeline(AUDITION_SCRIPT, voice=voice):
            signal = np.asarray(audio, dtype=np.float32).reshape(-1)
            if not np.all(np.isfinite(signal)):
                raise ValueError("POLICY_BLOCKED: model returned non-finite audio")
            if signal.size:
                samples.append(signal)
        if not samples:
            raise RuntimeError(f"Voice {voice} returned no audio")
        concatenated = np.concatenate(samples)
        if len(concatenated) < 24000 or np.max(np.abs(concatenated)) > 1.1:
            raise ValueError("POLICY_BLOCKED: invalid PCM amplitude or length")
        audio_files[voice] = concatenated

    # Fail-closed and no output overwrite. Create only after valid PCM for both voices.
    out.mkdir(parents=True, exist_ok=False)
    try:
        for voice, audio in audio_files.items():
            sf.write(str(out / (voice + ".wav")), audio, 24000, subtype="PCM_16")
        report["status"] = "VOICE_AUDITION_READY_HUMAN_REVIEW"
        report["duration_seconds"] = {
            voice: round(float(len(audio) / 24000), 3)
            for voice, audio in audio_files.items()
        }
        (out / "audition.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    except BaseException:
        # Do not erase possibly important media if write failed; report remains incomplete.
        raise
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(preview(args.out, args.dry_run), indent=2))


if __name__ == "__main__":
    main()
