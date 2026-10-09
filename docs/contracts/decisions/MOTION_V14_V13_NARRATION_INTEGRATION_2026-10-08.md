# Motion v1.4 → v1.3 end-to-end narrated integration receipt

**Date:** 2026-10-08 (America/Lima)
**Status:** `INTEGRATION_TECHNICAL_PASS / HUMAN_UAT_PENDING / RELEASE_BLOCKED`
**Proof location:** Local assistant container only; MP4 and owner voice are held in **private conversation artifacts**, not in this Git repository.

## What was actually executed

1. A **new fourth bounded visual family** `parallel_jobs` was added to NINFA's local v1.4 Scene Engine. This creates a fresh **23.6s** 9:16 animation from a JSON scene fixture rather than accepting a pre-rendered video.
2. The story is **not new**: it is an alternative animation of the earlier **Parallel Execution** test so that we can reuse the owner's already-approved English narration. It does not represent a second independent measurement.
3. The v1.3 finisher independently consumed: newly generated clean visual MP4, **private local owner voice WAV**, and a review-only caption manifest manually aligned by phrase. It exported H.264 + AAC MP4, English subtitles, and private integrity receipt.
4. An additive `tools/motion-v14/run_review.py` now performs both stages via one local command, with a SHA-gated cache for the clean v1.4 video followed by v1.3's existing audio/caption SHA cache.
5. A second run with identical inputs returned `visual_reused=true` and `final_cached=true`, with unchanged MP4 bytes.

### Technical observations

| Check | Result |
|---|---|
| Full Python tests | **26 / 26 PASS** on isolated Linux environment |
| Visual rendering | H.264 1080×1920, 30 FPS, **708 decoded frames**, 23.6 s |
| Final composition | H.264 video + AAC audio, 708 decoded video frames, 23.6 s |
| Clean visual SHA256 | `edaa307a2ec8e96ff7977ff2b01f55e19b8704badc803ac2d1bb2608ef0a07cd` |
| Final audio peaks | Approx. −19 dBFS mean / −2 dBFS max; no measured clipping |
| Repeated pipeline | **Both** visual and final finishing cached successfully |
| Real user voice | YES, reused securely from prior 23.6 s Parallel Execution short |
| Paid voice/video APIs | **$0** |
| GitHub Actions media runs | **0** |
| Scheduling/publishing | **NONE** |
| Caption verification | By manually set phrase intervals; **not word-accurate/certified** |
| Human editorial review | **PENDING** |

### Truth boundary

The numbers `0.34s`, `0.14s`, and `~2.4x` refer only to the earlier **three independent simulated local wait jobs** used in the already-reviewed demonstration. The new graphic prominently indicates **DEMO / SIMULATED SLEEP TASKS**. This is not proof about API, AI-agent or production performance, and it is not a newly rerun benchmark.

**No raw human voice or finished MP4 bytes are committed**. Do not persist voice SHA, private file paths, GitHub Action artifacts or personal recordings. Public Git only stores the safe scene and caption text/timing manifests and source code.

### Acceptance and remaining risks

- **GO** for the narrowly scoped **manually operated integration helper**, not for product-wide or unmanned video production.
- **HOLD** on channel publication: the new animation hasn't received owner UAT; logo authenticity, source rights, on-device overlay/safe-zone accessibility, word-level subtitle sync and substantive editorial review remain to be certified.
- **HOLD** on generality: fourth `parallel_jobs` family is a bounded same-story integration exercise, not evidence that any arbitrary script can be visualized.
- **HOLD** on WSL2 target host, OS-level sandbox/no-egress certification and cross-brand EMERCOD/prodAgentic integration.

The existing [Does It Automate? Motion v1 policy](../DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md), [Motion v1.2 owner UAT](MOTION_V1_2_OWNER_UAT_2026-10-08.md) and [Motion v1.3 finishing proof](MOTION_V1_3_LOCAL_FINISHING_2026-10-08.md) remain independently authoritative.

**No owner approval to publish is implied by approval to run an engineering experiment.**
