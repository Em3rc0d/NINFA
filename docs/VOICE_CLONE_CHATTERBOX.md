# Local Voice Clone — Chatterbox

Status: **VALIDATED / PRODUCTION-CANDIDATE**

Last validated: 2026-10-02

## Purpose

Provide Does It Automate with a reusable, local, zero-API-cost voice-cloning path for long-form narration.

This is a production component, not a requirement that every video use synthetic narration. Human narration remains valid whenever it gives a better result.

## Validated stack

- Chatterbox Multilingual TTS
- local Docker runtime
- FFmpeg reference normalization
- Gradio local UI
- PyTorch
- NVIDIA CUDA acceleration when available
- no paid TTS API required

## Voice-cloning behavior validated

A Spanish reference clip can be used to generate English narration while preserving speaker identity well enough for Does It Automate production tests.

Important operating rule:

**The output language selector describes the language of the narration text, not the language of the reference clip.**

Example:

- reference: Spanish voice sample
- narration text: English
- output language: English

Using English output settings with Spanish text produces English-style pronunciation of the Spanish text and is therefore not the intended workflow.

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

Keep references outside GitHub if they contain personal voice media. GitHub stores only configuration, documentation and reproducible workflow details.

## Cross-language settings

Validated working pattern for Spanish-reference → English-output:

- language: English
- CFG weight: 0.0 for cross-language generation
- exaggeration: around 0.5 as an initial baseline
- temperature: around 0.8 as an initial baseline

These are starting values, not immutable production constants.

## Hardware validation

### CPU-only baseline

Observed test:
- output audio: ~83 s
- generation time: 837 s
- RTF: ~10.08

Interpretation:
- functional,
- fully local,
- suitable for offline rendering,
- slow for repeated iteration.

### GPU baseline

Validated hardware:
- NVIDIA GeForce GTX 1650
- 4 GB VRAM
- CUDA available inside Chatterbox container

Observed test:
- output audio: 79.9 s
- generation time: 279.9 s
- RTF: ~3.50
- speedup vs CPU baseline: ~2.99x

Interpretation:
- GTX 1650 4 GB is sufficient for the current Chatterbox workload,
- GPU inference is materially better for production,
- still best treated as offline render rather than realtime TTS.

## Docker / WSL notes

Environment validated:
- Windows
- WSL2 Ubuntu 22.04
- Docker Engine running inside WSL
- NVIDIA GPU visible to WSL
- NVIDIA Container Toolkit configured for Docker

The key Docker validation is:

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

The Chatterbox container must use CUDA-enabled PyTorch and expose the GPU.

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

## Known maintenance items

1. Persist all model/support caches so container rebuilds do not redownload secondary assets.
2. Show chunk-level progress in the UI.
3. Save each completed chunk before concatenation.
4. Resume from completed chunks after failure.
5. Surface generation metrics in the UI:
   - audio duration,
   - generation duration,
   - RTF,
   - device,
   - chunk count.
6. Rename UI label from `Output language` to `Narration text language`.
7. Preserve a CPU fallback configuration.
8. Keep model/runtime versions pinned and documented.

## Model/version caution

Do not assume the PyPI release and GitHub master expose identical APIs.

A validated mismatch occurred where the GitHub branch supported a `t3_model="v3"` argument while the installed PyPI package did not.

Production rule:
- pin the exact package version,
- verify its runtime API,
- do not copy parameters from a different upstream revision without testing.

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
