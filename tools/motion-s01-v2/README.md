# S01 Motion V2 — native Full HD review

**State: TECHNICAL_PASS_REVIEW_ONLY**. Not a finished Short and not authorized for publication.

A custom five-beat motion study for the real **local Python zoneinfo ambiguity test** in `experiments/timezone-ambiguity`. The renderer draws at **1080×1920 native resolution** with Inter Display, a radial gradient, two analog clock visualizations, a split UTC timeline, permissive-vs-strict handling, and a verified closing statement.

## Reproduce (local Linux; no GitHub Actions or paid API)
- Python 3.11+, `Pillow`, `numpy`, `opencv-python`.
- FFmpeg/ffprobe with `libx264`, AAC, and Inter Display installed under `/usr/share/fonts/opentype/inter`.
- IANA tzdata present for `America/Los_Angeles`.
- Exact approved brand monogram from the owner's Drive **Branding** kit. Keep original brand-kit and extracted asset **private/outside GitHub**. If unavailable omit `--logo`; do not invent one.

```bash
python -m unittest discover -s experiments/timezone-ambiguity -v
python experiments/timezone-ambiguity/run.py --out /tmp/s01-evidence.json
python tools/motion-s01-v2/render_v2.py \
  --evidence /tmp/s01-evidence.json \
  --logo "/private/approved-logo-extracted.png" \
  --out "/private/S01-V2-review.mp4" \
  --contact "/private/S01-V2-contact.png"
python tools/motion-s01-v2/qa_v2.py \
  --source tools/motion-s01-v2/render_v2.py \
  --evidence /tmp/s01-evidence.json \
  --logo "/private/approved-logo-extracted.png" \
  --video "/private/S01-V2-review.mp4" \
  --out "/private/S01-V2-QA.json"
```

The provided private package from the corresponding conversation contains the logo excerpt and rendered media. Do not push the package to the public repository.

## Measured local result (2026-10-30)
- 1080×1920 H.264/yuv420p, 30 fps, 540 frames, 18.0 seconds, AAC 48 kHz stereo **original procedural UI sound effects only**.
- `19/19` technical checks passed.
- MP4 SHA-256: `c5bc78c7530fc406819d756b5a5db615614b09a0d57e0d228d1e7f2201ad35db`.
- Renderer SHA-256: `104e509227be2c645e56a2fd6b1911bb9658fde9544caee31a5dad275e5600f6`.
- Observed output is still **review-only**, not distribution approved. QA does not certify exact spoken timing, voice naturalness, accessibility or platform overlay collision.

## No accidental claim escalation
This is **NOT** an experiment involving a real calendar provider, a live booking, or an AI model. The `fold=0` behavior belongs to one permissive Python conversion under the tested timezone database. The outcome is conditional on the same timezone data. The brand logo is exact extracted pixels from the owner-approved source; it was not redrawn or synthesized.

## Missing release gates
- Approved natural English narration and correctly aligned English captions.
- Owner/editor listens to the finished voice mix.
- Physical-mobile YouTube Shorts UI safe-area review.
- Exact publishing package reviewed and approved by owner in separate turn.

Publishing/scheduling authority: **NONE**. No website/provider access, no Actions render, no private voice or finished MP4 committed.
