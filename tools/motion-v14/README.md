# NINFA Motion v1.4 — Local Scene Engine

**State:** three original 6-second families plus one bounded 23.6-second narrated-integration family. v1.4 scene rendering remains silent; a separate local command can now invoke the existing v1.3 finisher with private owner voice. No paid APIs, hosted renderers or GitHub Actions.

Supported families:
- `cache_race`: displays NINFA's **real measured** 4.80s/1.15s same-host cache comparison (bounded provenance).
- `circuit_breaker`: visually explains a timeout/fallback path; **DEMO only**.
- `source_lineage`: visually connects claim/source/check; **DEMO only**.
- `parallel_jobs`: 23.6-second **DEMO** of three simulated local waits, added solely to test v1.4 → v1.3 on a previously recorded English voiceover. This is not a new benchmark or a replacement for the three original families.

Run locally after installing Python 3.11+, Pillow, FFmpeg/FFprobe with libx264 and the Lato font:
```bash
python -m unittest discover -s tools/motion-v14/tests -v
python tools/motion-v14/engine.py --manifest tools/motion-v14/fixtures/cache-proof.json --out /tmp/cache-proof.mp4
python tools/motion-v14/engine.py --manifest tools/motion-v14/fixtures/breaker-demo.json --out /tmp/breaker-demo.mp4
python tools/motion-v14/engine.py --manifest tools/motion-v14/fixtures/source-demo.json --out /tmp/source-demo.mp4
```

The original three scene families create **silent** H.264 1080x1920 at 30fps, 180 frames / 6s. The integration-only `parallel_jobs` family creates 708 frames / 23.6s. Receipts include SHA-256 and `release_state=BLOCKED`. The underlying v1.4 scene generator still exports silent visuals; `run_review.py` is an explicitly separate local wrapper that then calls v1.3 for narration/captions. This is **not** general scene-to-story automation or automatic word-level sync.

**2026-10-08 original local proof:** three 6s MP4s FFprobe-valid, approximately 5.03/5.05/5.34s rendering on the test host. **Integration proof:** 26/26 Python tests PASS; one 23.6s, 708-frame `parallel_jobs` clean video rendered, then composed with the owner's existing English voice and 8 phrase-timed captions through v1.3. Both visual and final output caches were confirmed on an identical second run. This is a **technical review proof**, not owner approval or publication certification.

Privacy: no human recording, downloaded font binary, brand logo, heavy MP4 or private receipt belongs in Git. Evidence claim vs demo status is contract-enforced. See [ADR](../../docs/contracts/decisions/MOTION_V1_4_SCENE_ENGINE_ADR.md).

## One-command v1.4 → v1.3 owner-voice review (local only)

From the repository root (no Docker, GitHub Actions or paid services; both Python tools installed, Pillow and FFmpeg available):

```bash
python3 tools/motion-v14/run_review.py \
  --scene tools/motion-v14/fixtures/parallel-voice-demo.json \
  --finish tools/motion-v14/fixtures/finishing/parallel-v13-finish.review.json \
  --voice "/private/path/your-english-voice.wav" \
  --out "/private/review-output"
```

The tool keeps **visual outputs and narrated final MP4 outside the NINFA checkout**, checks duration, language and story mode across both contracts, then verifies the results. A repeat with unchanged inputs reuses the hash-checked visual and finished MP4. Pass `--force` to regenerate. Source voices are never uploaded by this CLI, but its **private** v1.3 receipt contains a voice hash: don't commit the output directory or distribute that receipt.

The visual and subtitle content in this narrow proof refer to the earlier three simulated sleep jobs: 0.34s sequential and 0.14s parallel, *not* production API throughput. The final MP4's voice was reused from a previously recorded approved English script, **not synthesized and not a new editorial story**. Captions were manually aligned by phrases, **not automatically certified at word level**.

See the [integration validation record](../../docs/contracts/decisions/MOTION_V14_V13_NARRATION_INTEGRATION_2026-10-08.md). This helper is **review-only** (`ILLUSTRATIVE_POC` and `release_state=BLOCKED`); it cannot publish anything.
