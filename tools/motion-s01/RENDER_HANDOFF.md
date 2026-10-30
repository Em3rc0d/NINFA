# NINFA-S01 — Review-only renderer handoff

The current S01 render is a truthful **silent text-led demonstration** of the local Python `zoneinfo` experiment. It is **not** approved for publication, and it does not test a real calendar service or an AI model.

## Reproduce locally

Python 3.11+, Pillow, NumPy, FFmpeg with libx264, Lato font, and system IANA timezone data are required.

```bash
python -m unittest discover -s experiments/timezone-ambiguity -v
python experiments/timezone-ambiguity/run.py --out experiments/timezone-ambiguity/evidence.json
python production/render_s01.py --evidence experiments/timezone-ambiguity/evidence.json --out NINFA-S01-review-silent.mp4 --contact NINFA-S01-contact-sheet.png
python production/qa_s01.py --video NINFA-S01-review-silent.mp4 --evidence experiments/timezone-ambiguity/evidence.json --out NINFA-S01-QA.json
```

The render is driven by the evidence JSON, not hardcoded fake provider outcomes. Source evidence hash (SHA256): `7bdc78a27ccf6c0423ed023f96697cf019ad05391dea2d356a43081b145d6089`. Rendered MP4 SHA256: `107e509f9ba59d322adbd5c183e50af450d17bb4b718a03788736ff341f52d13` (binary reproducibility depends on FFmpeg and codecs).

## Gate status

- Evidence reproduction: PASS (7/7 unittests).
- Node Audience Learning: PASS (11/11).
- Video technical/visual frame checks: PASS (16/16).
- Voice: UNAVAILABLE, no narration added.
- Official logo asset: UNAVAILABLE, no fabricated logo added.
- Human editorial / phone overlays / rights review: PENDING.
- Publication: BLOCKED. No upload, schedule or provider-side action.

## Editorial naming (2026-10-30)

Public-facing video cards use `EXPERIMENT 01`, **never** `FIELD TEST`. The research project name NINFA is internal; Does It Automate? is the public channel. This revision was re-rendered and the 16 technical/video checks were rerun.