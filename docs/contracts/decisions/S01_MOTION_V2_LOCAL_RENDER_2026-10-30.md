# NINFA S01 — Motion V2 technical receipt (2026-10-30)

**Decision:** `TECHNICAL_PASS_REVIEW_ONLY / PUBLICATION_BLOCKED`.

## Provenance

Source: `experiments/timezone-ambiguity/run.py` and `evidence.json` from the verified S01 local simulation. It models **Nov 1, 2026 01:30 in America/Los_Angeles**, a repeated wall-clock time with two UTC instants `08:30Z` and `09:30Z`. No real calendar provider or AI agent was tested.

Brand: the mark appearing in the review MP4 was cropped and alpha-masked **without redrawing** from the owner-approved `Does_It_Automate__Brand_Kit__Approved.png` in the NINFA Drive `03_Media/Branding` folder. Approved source remains in Drive and excerpt stays private; source code does not embed a replacement logo.

## Video contract

- Native 1080×1920 at 30 fps; exactly 540 frames and 18.000 seconds.
- H.264, YUV420p, AAC stereo 48 kHz; **UI sound effects only**. No natural or synthetic narration was inserted.
- Five distinct visual beats: paradox, two clocks, UTC branch, handling strategies, decision.
- Original on-screen footer discloses local Python simulation and no provider/agent test.
- Discontinued public label “Field Tests” is not used.
- MP4 SHA-256: `c5bc78c7530fc406819d756b5a5db615614b09a0d57e0d228d1e7f2201ad35db`.
- Offline QA: **19/19 PASS** (FFprobe metadata, decoded frames, measured motion, source-tamper rejection, logo input, overlay geometry proxy, audio nonzero/no clipping).
- Exact local renderer SHA-256: `104e509227be2c645e56a2fd6b1911bb9658fde9544caee31a5dad275e5600f6`.

## Important limitations

- This is a **technical** check, not proof of audience preference, readability on a real phone or compatibility with the YouTube Shorts editor.
- Native Inter Display font and source assets must be installed on another render environment. Exact output SHA may vary by FFmpeg, fonts and image encoders.
- Natural English narration and captions are absent. No final video can be approved until separately produced and reviewed.
- No GitHub Actions media render, paid APIs, YouTube upload, scheduling or publication.

**Next required:** add approved natural English voice, align phrase captions from the actual recorded waveform, conduct device-level overlay review and obtain explicit final editorial release approval.
