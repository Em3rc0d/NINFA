# Chatterbox Local — NINFA

Reproducible local voice-cloning runtime used by Does It Automate.

Status: **validated on WSL2 + Docker Engine + NVIDIA GTX 1650 4 GB**.

## What is included

- Chatterbox Multilingual TTS pinned to `chatterbox-tts==0.1.7`
- Python 3.11
- PyTorch 2.6.0 + CUDA 12.4 wheels
- Gradio local UI
- FFmpeg reference normalization
- long-text chunking
- WAV export
- persistent Hugging Face and pkuseg caches
- NVIDIA Container Toolkit bootstrap for Debian/Ubuntu WSL2
- CPU fallback through `DEVICE=cpu`

No paid TTS API is required.

## Compatibility boundary

"Any WSL" has a hardware/runtime boundary.

The automatic CUDA bootstrap supports:

- WSL2
- Debian/Ubuntu-based distro
- NVIDIA GPU visible to WSL through `nvidia-smi`
- Docker Engine installed inside that WSL distro

It cannot make CUDA work on a machine without a compatible NVIDIA GPU/driver.

Do **not** install a separate Linux NVIDIA display driver inside WSL. WSL uses the Windows NVIDIA driver.

## Fresh WSL setup

From this directory:

```bash
chmod +x scripts/*.sh
./scripts/setup-wsl-cuda.sh
```

The script:

1. verifies WSL,
2. verifies `nvidia-smi`,
3. installs NVIDIA Container Toolkit,
4. runs `nvidia-ctk runtime configure --runtime=docker`,
5. restarts Docker,
6. validates the GPU from an NVIDIA CUDA container.

Expected Docker validation:

```text
Runtimes: ... nvidia ...
NVIDIA GeForce ...
```

## Start Chatterbox

```bash
./scripts/start.sh
```

Open:

```text
http://localhost:7860
```

The start script validates Docker GPU access before building the application.

## Manual GPU validation

```bash
nvidia-smi

docker info | grep -i runtime

docker run --rm --gpus all \
  nvidia/cuda:12.4.1-base-ubuntu22.04 \
  nvidia-smi
```

Inside the running Chatterbox container:

```bash
docker exec chatterbox-local python -c "
import torch
print('CUDA:', torch.cuda.is_available())
print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')
print('VRAM GB:', round(torch.cuda.get_device_properties(0).total_memory/1024**3,2) if torch.cuda.is_available() else 0)
"
```

## Validated benchmark

NINFA test on 2026-10-02:

| Runtime | Audio | Generation | RTF |
| --- | ---: | ---: | ---: |
| CPU | ~83 s | 837 s | ~10.08 |
| GTX 1650 4 GB | 79.9 s | 279.9 s | ~3.50 |

Observed end-to-end GPU speedup vs CPU baseline: about **3x**.

This is a machine-specific baseline, not a universal Chatterbox benchmark.

## Cross-language workflow

Validated case:

```text
Spanish voice reference
        +
English narration text
        ↓
Narration text language = English
CFG = 0.0
Exaggeration ≈ 0.5
Temperature ≈ 0.8
        ↓
English WAV using cloned speaker identity
```

Generate long videos as multiple section WAVs rather than one giant request. A failed section can then be regenerated cheaply.

## Important package API note

The pinned PyPI release `chatterbox-tts==0.1.7` is loaded with:

```python
ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
```

Do not add `t3_model="v3"` to this pinned package. That argument was observed in a different upstream API revision and raised a `TypeError` with the installed PyPI release.

## Data policy

Do not commit:

- personal voice references,
- generated narration WAVs,
- Hugging Face model cache,
- pkuseg cache.

These paths are excluded by `.gitignore`.

## Stop

```bash
./scripts/stop.sh
```

## Maintenance

When upgrading Chatterbox, PyTorch, Gradio, or the CUDA wheel target:

1. change one layer at a time,
2. rebuild with `docker compose build --no-cache`,
3. confirm `torch.cuda.is_available()`,
4. run the same fixed narration/reference benchmark,
5. compare quality, duration, generation time and RTF,
6. only then promote the new versions.
