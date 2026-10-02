# Local Voice Clone — Chatterbox

Status: **VALIDATED / PRODUCTION-CANDIDATE**

Last validated: 2026-10-02

## Canonical implementation

The reproducible implementation now lives in:

`tools/chatterbox-local/`

That directory contains the pinned Chatterbox runtime, CUDA-enabled Docker image, Docker Compose definition, WSL2 NVIDIA Container Toolkit bootstrap, start/stop scripts, Gradio application and cache policy.

The implementation is the source of truth for executable setup. This document records the architectural and operational decisions.

## Purpose

Provide Does It Automate with a reusable, local, zero-API-cost voice-cloning path for long-form narration.

This is a production component, not a requirement that every video use synthetic narration. Human narration remains valid whenever it gives a better result.

## Validated stack

- Chatterbox Multilingual TTS, pinned PyPI release `chatterbox-tts==0.1.7`
- Python 3.11
- PyTorch 2.6.0 with CUDA 12.4 wheels
- local Docker Engine under WSL2
- NVIDIA Container Toolkit
- FFmpeg reference normalization
- Gradio local UI
- no paid TTS API required

## Voice-cloning behavior validated

A Spanish reference clip can be used to generate English narration while preserving speaker identity well enough for Does It Automate production tests.

Important operating rule:

**The language selector describes the language of the narration text, not the language of the reference clip.**

Example:

- reference: Spanish voice sample
- narration text: English
- narration text language: English

Using English language settings with Spanish narration text produces English-style pronunciation of that Spanish text and is not the intended workflow.

## Reference guidance

Preferred reference:

- 10–30 seconds
- one speaker only
- clean voice
- no music
- no other speakers
- no clipping
- low room echo
- natural delivery

Existing OBS recordings are acceptable when the voice is clean.

Keep personal reference voice media outside GitHub. The repository stores only code, configuration, documentation and reproducible workflow details.

## Cross-language settings

Validated starting point for Spanish-reference → English-output:

- narration text language: English
- CFG weight: 0.0
- exaggeration: around 0.5
- temperature: around 0.8

These are starting values, not immutable production constants.

## Hardware validation

### CPU-only baseline

Observed test:

- output audio: ~83 s
- generation time: 837 s
- RTF: ~10.08

### GPU baseline

Validated hardware:

- NVIDIA GeForce GTX 1650
- 4 GB VRAM
- CUDA visible inside the Chatterbox container

Observed test:

- output audio: 79.9 s
- generation time: 279.9 s
- RTF: ~3.50
- observed end-to-end speedup vs CPU baseline: about 3x

Interpretation:

- GTX 1650 4 GB is sufficient for the current workload,
- GPU inference is materially better for production,
- the system is still best treated as offline rendering rather than realtime TTS.

## WSL2 / Docker CUDA bootstrap

Validated environment:

- Windows
- WSL2 Ubuntu 22.04
- Docker Engine running inside WSL
- NVIDIA GPU visible to WSL
- NVIDIA Container Toolkit configured for Docker

Canonical bootstrap:

```bash
cd tools/chatterbox-local
chmod +x scripts/*.sh
./scripts/setup-wsl-cuda.sh
./scripts/start.sh
```

The setup script intentionally does not install a Linux NVIDIA display driver. WSL consumes the Windows NVIDIA driver.

## Current production flow

```text
script
  ↓
voice reference
  ↓
Chatterbox Multilingual
  ↓
chunked narration
  ↓
WAV
  ↓
audio QA / loudness normalization
  ↓
scene manifest / renderer
  ↓
final video
```

## Model/version caution

Do not assume the PyPI release and GitHub master expose identical APIs.

A validated mismatch occurred where an upstream revision showed a `t3_model="v3"` argument while the installed PyPI package did not accept it.

The pinned implementation therefore uses:

```python
ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
```

Production rule:

- pin the exact package version,
- verify its runtime API,
- do not copy parameters from a different upstream revision without testing.

## Maintenance backlog

The executable package already persists Hugging Face and pkuseg caches and exposes benchmark metrics.

Next improvements:

1. chunk-level progress,
2. save completed chunks before concatenation,
3. resume from completed chunks after failure,
4. optional per-section manifest generation,
5. repeatable audio QA/mastering pass.

## Cost conclusion

Marginal TTS API cost: **S/0**

Actual costs:

- local electricity,
- existing hardware,
- storage,
- human review time.

## Production acceptance

The voice clone is considered usable for Does It Automate when:

- speaker identity is convincing,
- pronunciation is correct,
- artifacts are acceptable,
- narration matches the intended language,
- the render completes deterministically enough for offline production.

Current state: **accepted for real-video production testing.**
