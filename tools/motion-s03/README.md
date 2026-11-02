# Does It Automate? — S03: Crash Recovery Short

**Status:** `TECHNICAL_PASS_REVIEW_ONLY`, owner release blocked. **Date:** November 1, 2026. Public label: **Experiment** (not “Field Tests”).

This is an original local subprocess-crash/restart demonstration, showing an automation resuming work after a process interruption. **No AI model or external provider is used**; do not frame this as an agent performance comparison or a real production guarantee.

## Reproduction (repo root)

Python 3.11+ with `Pillow`, `numpy`, `opencv-python`, system FFmpeg/FFprobe with libx264/AAC, Inter Display fonts under `/usr/share/fonts/opentype/inter`, and a working SQLite build. The model and video generator incur no paid API charges.

```bash
python -m unittest discover -s experiments/crash-recovery -v
python experiments/crash-recovery/replay.py run --out /tmp/ninfa-s03-evidence
python tools/motion-s03/render_s03.py \
  --evidence /tmp/ninfa-s03-evidence/evidence.json \
  --out /tmp/ninfa-s03-review.mp4 \
  --contact /tmp/ninfa-s03-contact.png \
  --logo /private/owner-approved-logo-excerpt.png
python tools/motion-s03/qa_s03.py \
  --video /tmp/ninfa-s03-review.mp4 \
  --evidence /tmp/ninfa-s03-evidence/evidence.json \
  --renderer tools/motion-s03/render_s03.py \
  --logo /private/owner-approved-logo-excerpt.png \
  --out /tmp/ninfa-s03-QA.json
```

`--logo` uses **only** the unmodified owner-approved mark extracted from the brand kit available in NINFA Google Drive `03_Media/Branding`. If that asset is missing, omit the mark rather than invent it. Do not commit brand-kit binaries, human voices, review MP4s or private receipts to GitHub.

## Verified local results

- Workflow: four *local SQLite* steps (`READ`, `VALIDATE`, `TRANSFORM`, `STORE`).
- Both real subprocesses exited with code `27` after completing two steps.
- Naive restart: `6` stored actions, `2` repeated.
- Atomic local SQLite checkpoint: `4` stored actions, `0` repeated.
- Experiment tests: **12/12 PASS**.
- Visual review: native **1080 × 1920**, H.264, 30 fps, 540 frames/18 seconds, original procedural AAC UI SFX only.
- Technical and evidence QA: **27/27 PASS**.
- Review MP4 SHA-256: `eb450dbf3caaeab6ba04e178ca06f0f7db292dffe08e146bd0ad113138d28340`.
- Evidence core digest: `6b885aa90b71c7f48f7725d36fe27b12fa233407a6b04c5fdab30f976e1f202c`.

**Boundary:** The use of one SQLite transaction for each action/checkpoint pair does not establish exactly-once semantics for remote effects or distributed queues. No external services, AI models or network calls were tested. Repeated actions count is a property of this local demonstration alone.

### Release blockers

Natural English voice, caption synchronization, real phone overlay review, editorial approval. `publication_authority = NONE`. A passing structural QA is not evidence of audience demand or a publishable final video.

See [storyboard](../../content/shorts/2026-11-01-crash-recovery/STORYBOARD.md) and [decision receipt](../../docs/contracts/decisions/S03_CRASH_RECOVERY_LOCAL_REVIEW_2026-11-01.md).
