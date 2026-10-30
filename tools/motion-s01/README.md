# Motion S01 — timezone ambiguity (SILENT review only)

This narrow renderer illustrates **only** the local Python `zoneinfo` simulation in `experiments/timezone-ambiguity`. It is not a generic motion engine, a real calendar test, an AI-agent benchmark, or approved media for publication.

Run from the repository root (Python 3.11+, Pillow, NumPy, FFmpeg/FFprobe with H.264, installed Lato font and IANA tzdb):

```bash
python -m unittest discover -s experiments/timezone-ambiguity -v
python experiments/timezone-ambiguity/run.py --out experiments/timezone-ambiguity/evidence.json
mkdir -p /tmp/ninfa-s01
python tools/motion-s01/render_s01.py \
  --evidence experiments/timezone-ambiguity/evidence.json \
  --out /tmp/ninfa-s01/S01-review-silent.mp4 \
  --contact /tmp/ninfa-s01/S01-contact-sheet.png
python tools/motion-s01/qa_s01.py \
  --video /tmp/ninfa-s01/S01-review-silent.mp4 \
  --evidence experiments/timezone-ambiguity/evidence.json \
  --out /tmp/ninfa-s01/S01-QA.json
```

**Observed local QA (2026-10-30):** H.264 1080×1920, 30 fps, 540 frames / 18 seconds, 16/16 structural and sample-frame checks PASS. Original local silent review binary SHA256: `107e509f9ba59d322adbd5c183e50af450d17bb4b718a03788736ff341f52d13`. FFmpeg version differences may change binary hashes.

The on-video header is `EXPERIMENT 01`, not the retired “Field Tests” series label; the public identity is Does It Automate? Official logo asset was not present, so no fake logo was created.

**Status:** `TECHNICAL_PASS_REVIEW_ONLY / NO_AUDIO / NO_PUBLICATION_AUTHORITY`. These checks do not establish mobile overlay clearance, correct/natural audio, approved captions, human editorial sign-off, or published state.

Reproducible review is available in the conversation privately. Keep final MP4, voice masters, device captures and private receipts **out of GitHub**. `RENDER_HANDOFF.md` uses paths relative to the downloadable standalone package, whereas this README uses repository-root paths.
