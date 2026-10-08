# PV-POC-001 — Video render proof (experiment record)

**Date:** 2026-10-07 America/Lima. **Status:** `PASS_OUTPUT_ONLY / SOURCE_ARCHIVAL_PENDING / NOT_PRODUCTION`.

This experimental record exists to preserve evidence without changing NINFA's existing long-form workflows. It is **not** proof that NINFA's previously documented production had a versioned reusable video renderer. The test was carried out independently in an assistant work container.

## What was built

- Three original, synthetic scenes; 1080×1920 at 30 fps; exactly 300 frames (10 seconds).
- Python/Pillow frame compositor streaming trusted, authored RGB frames to FFmpeg 7.1.5 / H.264 MP4.
- Lato typefaces from Debian `fonts-lato`, documented OFL-1.1; no font binaries stored here.
- No audio, third-party prompts/media, external URLs, API spend, cloud deployment, post scheduling, brand logo or personal voice files.
- A conservative experimental text-safe-zone `top:220 right:85 bottom:350 left:85`, checked via text bounding boxes on each frame. This is not a certified TikTok overlay profile.

## Observed result

- FFprobe: 1080×1920, H.264, 30/1 fps, 300 decoded frames, 10.0 s, no audio stream.
- Two **independent full render executions** yielded byte-identical MP4 files at SHA-256:
  `44aa178c3aac0baf76dacec93ade73c740d11d0cc8ab28e8d4018ac09d5fca98`.
- File size: 771,848 bytes.
- Measured render function elapsed times: 19.68 s and 25.24 s. First run peak observed process memory about 131.7 MiB; second peak not measured.
- Input tests: six negative contract fixtures + one negative unsafe-text test, plus sampled temporal frame variance.

See [machine-readable evidence](RECEIPT.json).

## Honesty boundary

The exact tested `render.py`, `self_test.py`, `verify_receipt.py`, `manifest.json`, video and contact sheet are packaged together in the conversation artifact **PV-POC-001_reproducible.zip** provided to the project owner. This branch **does not yet archive the tested source or MP4**, so another GitHub-only checkout cannot reproduce the result from this branch. Their SHA-256 identifiers are preserved in the receipt for later import verification. Large videos are intentionally excluded from GitHub under the media storage policy.

Code made no network calls, but **OS-level no-egress/credential isolation was not certified**, and no untrusted agent-generated JS was executed. Human editorial quality, account branding, actual TikTok safe-zone, WSL2 host preflight, job custody, integration into prodAgentic and scheduling are all OPEN.

## Scope decision

`ADOPT`: time-indexed storyboard, original content only, local render as viable narrow proof.
`HOLD`: adapter productization, OS sandbox, approved versioned artifact store, cross-account tests, human QA and release certification.
`REJECT`: claiming NINFA audio/TTS code renders MP4, copying voice assets, presenting this proof as an integrated Content Seller/TikTok scheduling workflow.

Technical analysis and candidate architecture: [Programmatic Video MK1 PR #30](https://github.com/Em3rc0d/personal_knowledge/pull/30).
Product integration RFC: [prodAgentic issue #71](https://github.com/Em3rc0d/prodAgentic/issues/71).

**This record stays on an experiment branch and must not be merged as production evidence until tested source is archived/re-reviewed and owner acceptance gates are handled.**
