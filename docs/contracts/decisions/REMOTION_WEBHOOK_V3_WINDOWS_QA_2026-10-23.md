# NINFA Webhook V3 — Windows technical UAT and QA extractor repair

Date: 2026-10-23. Status: **TECHNICAL_RENDER_PASS / QA_FRAME_EXTRACT_RETRY_REQUIRED / VISUAL_QA_PENDING / RELEASE_BLOCKED**

## Confirmed through owner's Windows PowerShell transcript

- Checked out `exp/remotion-webhook-vertical-slice-20261023` from GitHub.
- `npm test`: **24 PASS, 0 FAIL**; `npm run typecheck`: **PASS**.
- `node scripts/render.mjs webhook-v3 "$review\\renders\\webhook-v3.mp4"`: **PASS**; dynamic localhost port `54290`; H.264 1080×1920/30fps; `720` frames, `7` shots; 78,035 ms total; approx. 1.2 MB.
- Local wrapper ran FFprobe and wrote a media receipt:
  - storyboard SHA-256 `f90bc841af3e7be139cea5c0e2fcad1f0fcfc80f7864d75fb154488e5e06e7e6`
  - video SHA-256 `57ef46fcdc5921c2efdf1e8cd579baa7b93f18447f961ccdc51d13979746d610`
  - props SHA-256 `41c48cc21f815105c0e7b5856b9667b73b544b89f3a438f8aa97f79872554b29`
  - release state `BLOCKED`, publish authority `NONE`
- The independent frame-QA helper **failed** on the user's FFmpeg build at option `-vsync vfr`: `Unrecognized option 'vsync'`. This does **not** invalidate the MP4 or the structural media receipt, but it means frame QA did **not** complete.

## Root cause and repair

The legacy FFmpeg sync option `-vsync` was replaced by the per-output `-fps_mode`, which newer FFmpeg builds require. The image2 extraction uses `-vf select=eq(n\\,frame)+...` with `-fps_mode vfr` to avoid duplicate output frames.

- Smoke-tested 19 selected frame indices using FFmpeg 7.1.5 and the uploaded 720-frame `webhook-v2.mp4`: 19 distinct PNG output files with frame numbers `frame-000.png` … `frame-018.png`.
- Added two targeted regression tests for `-fps_mode vfr` and malformed sampling frames.
- Changed the QA extractor to write to a **private staging directory** under its intended parent and publish the complete folder only after 19 PNGs + `sampling-manifest.json` pass checks; incomplete extraction cleans up without occupying the output path.
- The user's earlier failed execution may already have created an empty `NINFA-Review/qa/webhook-v3` directory. **Do not delete any user data automatically**; retry with `webhook-v3-fixed`.

## Remaining gate / truthful limits

- Current V3 MP4 bytes have NOT been uploaded to this turn; no independent video pixel, motion, provenance-label or mobile safe-zone inspection can be asserted.
- The repaired extractor and new tests still need to run on the user's Windows FFmpeg build. If the output succeeds, inspect all 19 real frames including both sides of the six scene cuts and watch the full 24-second video.
- No voice/caption integration, license/dependency clearance, same-host benchmark, creative-owner approval or merge to `main`.

**RELEASE_BLOCKED** pending independent visual and human approval. Preserve V1, V2 and the existing Motion v1.3 finishing path.
