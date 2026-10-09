# Motion v1.5 — Evidence-first production thread (experimental)

**Target:** Does It Automate? / English Shorts only. **Status:** LOCAL ENGINEERING PASS, silent 24-second review, owner narration and human QA pending. **No upload/publishing authority.**

## What is real

- `replay_lab.py` opens a local SQLite database and delivers **the same synthetic event twice**, sequentially using separate connections. Without a `UNIQUE(event_key)` index it creates 2 rows; with the index it creates 1 row and ignores the duplicate. The recorded result is not from any real webhook provider and does **not** prove concurrency safety.
- `studio.py` only accepts that content-hashed evidence recipe and storyboard, constructs a persistent motion interface at 30fps using Pillow, exports a **silent**, review-only H.264 MP4 through local FFmpeg, and validates 720 decoded frames, 1080×1920 and 24s using ffprobe.
- `build.py` recreates the synthetic evidence and runs the visual generation from the versioned storyboard. The output remains outside the repo.
- `story.json` carries English narration text and **provisional** caption frame intervals, not ASR-certified final timings. The user must record the new script before finishing with v1.3.

## One command (no Actions, cloud or paid APIs)

From the project root with Python 3.11+, Pillow, FFmpeg/FFprobe and Lato/Liberation fonts locally:

```bash
python -m unittest discover -s tools/motion-v15/tests -v
python tools/motion-v15/build.py --out /private/location/review-v15 --dry-run
python tools/motion-v15/build.py --out /private/location/review-v15
```

No GitHub Actions execution, paid inference, TTS or voice cloning. No media/voice binaries committed. Source is an independently authored new bounded scene family; it does **not** allow arbitrary story visualization. The test receipt at `evidence/replay_evidence.json` contains only synthetic data.

## Publication gates (all independent)

1. Human approves actual English performance and adjusts caption timing to WAV/M4A.
2. Mobile Shorts overlay/safe-area check; no text conflicts or inaccessible contrast.
3. Verify any third-party asset/brand usage; the graphic uses **plain text only**, not an invented official logo.
4. Source code/proof review confirms local, sequential, synthetic nature of the test; don't claim a real webhook transaction or concurrent safety.
5. Only then prepare a separately approved distribution artifact, title and description; publishing/scheduling needs a distinct provider authority and receipt.

**Production principle:** a working visual scene is not a released Short. The evidence and motion are reproducible; user voice, final QA and publisher authorization remain the human gates.

## Owner-voice release review (2026-10-09)

The owner recorded English voice separately and approved the **original-source AAC without additional DSP** over the compressed/loudness-normalized variant. A separately delivered **private** 21-second/630-frame H.264/AAC review MP4 has exactly the same encoded AAC audio payload as the approved owner M4A. Eight English subtitles are manually timed at phrase level. The recorded 25/25 SQLite source regressions were rerun.

- [Versioned QA and platform gate findings](../../docs/contracts/decisions/MOTION_V15_PUBLICATION_GATE_REVIEW_2026-10-09.md)
- [Draft English YouTube distribution copy](release/DISTRIBUTION_DRAFT.md)
- [Fail-closed release-gate state](release/release-gates.json)

**Not ready to publish:** the possible bottom YouTube UI overlay on the factual disclaimer requires an actual phone/editor check, then listening verification of subtitle wording and an explicit separate release approval. This repo stores **no voice recordings or final MP4s**.
