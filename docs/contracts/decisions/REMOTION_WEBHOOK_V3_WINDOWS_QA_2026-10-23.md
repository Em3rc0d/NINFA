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

## Independent still-frame visual audit and corrective patch — 2026-10-23

**Scope:** The owner provided the complete 19-frame PNG set and `sampling-manifest.json`, covering each of seven shot centers and both sides of all six cuts. This is a genuine inspection of the submitted stills at 1080 × 1920; the original V3 MP4 bytes were **not uploaded**, so the uploaded PNGs cannot independently prove the manifest's MP4 SHA. The manifest reports `source_video_sha256=57ef46fcdc5921c2efdf1e8cd579baa7b93f18447f961ccdc51d13979746d610` and 19 source-frame selections, consistent with Windows output.

**Owner Windows after QA compatibility patch:** `npm test` **26/26 PASS**, `npm run typecheck` PASS, and `inspect-webhook-v3.mjs` returned `FRAME_SAMPLES_READY_REVIEW_ONLY` with 19 PNGs, 6 cuts, `release_state=BLOCKED`. QA extractor gate is therefore technically PASSED for this host.

### Visual findings against original V3 frames

- **Improvement demonstrated:** Seven mutually exclusive shots show a sequential incoming event, two persisted rows with no key constraint, introduction of `UNIQUE(event_key)`, one persisted guarded row and an ignored duplicate, final 2 vs 1 outcome and explicit concurrency limitation. No simultaneous headings/ghosting at six sampled cut boundaries. The 2/1 facts and limitations are coherent with the SQLite synthetic receipt.
- **P0 layout infringement:** `Compare` shot at frames 552, 594 and 635 places `Synthetic sequential SQLite result.` immediately across the footer's horizontal top border. Root layout top is 343, compare note is shot-local y930 and footer is y1304: y=1273 before 35px font height, which overlaps footer line. The note is moved to local y855, leaving at least 24px clear.
- **P1 occlusion:** Terminal status circles are drawn in SVG near x630, but a later-painted SQLite panel begins at x622 and covers the circles; only clipped green halves remain at frames 144/209 and 475/551. Remove the obscured terminal circles; the actual persisted row and the constraint panel's ✓/× now carry status.
- **P1 premature success cue:** In guarded shot frame399 the green ✓ within the unique-key guard is visible before first delivery reaches it. Make its opacity a local-frame progression (start frame42) so status follows the event.
- **P1 remaining creative gaps:** Screenshot audit is not a full-motion/phone test; large lettered headings and diagnostics still occupy much of the frame. The owner-approved official logo, voice, real phrase-aligned captions and measured platform attention remain unverified. Do not infer retention or upload readiness.
- **No truth changes:** Seven shot intervals, the event-source receipt, the 2-vs-1 counts and explicit `CONCURRENCY NOT TESTED` remain unchanged.
- **Code gate:** Two visual regression checks added; Windows is expected to report **28/28 tests** after pulling this patch, but it has **not** yet been rendered or checked with the corrected source.

**Conclusion:** `FRAME_EXTRACTION_PASS / VISUAL_STILL_QA_PARTIAL_PASS_WITH_CORRECTIONS / PATCH_RE_RENDER_PENDING / RELEASE_BLOCKED`. Retain all prior assets and V1/V2 compositions, no `main` merge and no automatic publication.
