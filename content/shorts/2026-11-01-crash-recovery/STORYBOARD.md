# S03 — I Crashed My Automation at Step 2

**Channel:** Does It Automate? · **Content label:** Experiment · **Status:** LOCAL TECHNICAL PREVIEW; publication blocked.

## Verified case

A local Python subprocess ran a four-step SQLite workflow: READ → VALIDATE → TRANSFORM → STORE. It was intentionally terminated by `os._exit(27)` after its second completed step and restarted. The naive worker restarted from step one: six recorded actions total (two repeats). The checkpointed worker stored each local action and completion marker in one SQLite transaction, resumed at step three and recorded four actions total (zero repeated actions). Tests executed locally: 12/12 pass. All numbers in the video come from `evidence.json`.

**Critical caveat:** no AI model, external SaaS, network request, customer, webhook provider, real money movement or distributed transaction was tested. This does not prove external exactly-once processing. Our result is specific to the demonstrated local SQLite workflow.

## Visual narrative (18 seconds)

| Time | Beat | On-screen takeaway |
|---|---|---|
| 0.0–2.8s | Kill the worker at step two | `I CRASHED THE AUTOMATION.` |
| 2.8–5.4s | Restart and examine work | `2 STEPS COMPLETED` |
| 5.4–9.7s | Naive restart begins from start | `6 ACTIONS · 2 REPEATED` |
| 9.7–14.0s | Persisted checkpoint resumes | `RESUME → STEP 03` |
| 14.0–18.0s | Verified comparison | `6 → 4 actions` / `2 repeats avoided` |

## Suggested natural English voiceover — DRAFT ONLY

> I killed this local automation after step two. Without a saved checkpoint, restarting repeated both completed steps: six actions total. With a SQLite checkpoint, it resumed at step three: four actions. No external services were tested.

This script requires human listening and timing to fit. It is not an approved or produced voice track. A text-led, sound-effects-only review MP4 exists but should **not** be uploaded as a finished Short.

## Headline / distribution draft

**Title hypothesis:** `I Crashed My Automation at Step 2 — Then Restarted It`.

**Description draft:** `I intentionally killed a local four-step workflow, then restarted it with and without SQLite checkpoints. The naive restart recorded 6 actions, including 2 repeats; the checkpointed run recorded 4. This is a controlled local Python/SQLite demonstration, not a production or AI-agent reliability benchmark. Code and evidence are available in the NINFA repository.`

**No fixed performance prediction.** Wait for proper release and compare source-specific initial-hold, shown-in-feed, engaged views and duration retention in matched windows.

## Release gates

- [x] Local process interruption and retry observed.
- [x] Real evidence and source archived.
- [x] 12/12 experiment unit tests.
- [x] Native 1080x1920 visual preview and original SFX.
- [x] 27/27 offline structural/video/claim QA.
- [ ] Approved natural English narration.
- [ ] Subtitles aligned against actual recorded audio.
- [ ] Human review of on-screen numbers and pacing.
- [ ] Actual phone Shorts-UI safe-area check.
- [ ] Explicit owner approval to upload or publish.

`publish_authority: NONE` / `video_state: REVIEW_ONLY`.
