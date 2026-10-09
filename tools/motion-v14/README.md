# NINFA Motion v1.4 — Local Scene Engine

**State:** three-family, silent, review-only generator. Does not replace v1.3, does not use paid APIs, hosted renderers, GitHub Actions, or personal voice.

Supported families:
- `cache_race`: displays NINFA's **real measured** 4.80s/1.15s same-host cache comparison (bounded provenance).
- `circuit_breaker`: visually explains a timeout/fallback path; **DEMO only**.
- `source_lineage`: visually connects claim/source/check; **DEMO only**.

Run locally after installing Python 3.11+, Pillow, FFmpeg/FFprobe with libx264 and the Lato font:
```bash
python -m unittest discover -s tools/motion-v14/tests -v
python tools/motion-v14/engine.py --manifest tools/motion-v14/fixtures/cache-proof.json --out /tmp/cache-proof.mp4
python tools/motion-v14/engine.py --manifest tools/motion-v14/fixtures/breaker-demo.json --out /tmp/breaker-demo.mp4
python tools/motion-v14/engine.py --manifest tools/motion-v14/fixtures/source-demo.json --out /tmp/source-demo.mp4
```

Each output is **silent** H.264 1080x1920 at 30fps, 180 frames / 6s. Receipts include SHA-256, resource timing and `release_state=BLOCKED`. The optional v1.3 finisher can later take such a clean video **with a new duration-matched review manifest and private voice**, but v1.4 does NOT invoke v1.3 or guarantee automatic audio synchronization.

**2026-10-08 local isolated Linux experiment:** 18/18 Python tests PASS; three 6s MP4s FFprobe-valid, approximately 5.03/5.05/5.34s rendering on that host. These are narrow engineering fixtures, not approved publishable shorts.

Privacy: no human recording, downloaded font binary, brand logo, heavy MP4 or private receipt belongs in Git. Evidence claim vs demo status is contract-enforced. See [ADR](../../docs/contracts/decisions/MOTION_V1_4_SCENE_ENGINE_ADR.md).
