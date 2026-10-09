# Motion v1.3 — local AV finishing experiment receipt

**Date:** 2026-10-08, America/Lima.
**Status:** `PASS_NARROW_LOCAL_FINISHING` / `NOT_FULL_VIDEO_FACTORY` / `NOT_PUBLISH_CERTIFIED`.
**Module:** [tools/motion-v13](../../../tools/motion-v13/README.md).
**Authority:** Existing Does It Automate? [Shorts motion contract v1](../DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md) and the owner's [Motion v1.2 batch UAT](MOTION_V1_2_OWNER_UAT_2026-10-08.md).

## Scope

A new additive, local-only **AV finishing module** was implemented using **Python standard library orchestration + FFmpeg/FFprobe**. It accepts an already rendered clean 1080×1920 30-fps video (cached visual layer), a private local user voice file, and an English caption-frame manifest. It produces a H.264/AAC review MP4 and a private JSON QA receipt. It does **not** synthesize audio, render original visual scenes, retrieve third-party media, connect to providers, or post/schedule anything.

**The v1.2 owner acceptance was for the audiovisual quality reference, not a blanket certification of this new software.** Motion v1.3 is an engineering proof for avoiding repeated visual rendering and optionally skipping unchanged finishing jobs with a verified digest cache.

## Test evidence — isolated assistant container

- Python tests: **16/16 PASS** after adding cache invalidation and strict input checks; includes illegal languages/brands, unauthorized paid/API/CI/publishing flags, unsupported voices, overlap, duration and unsafe caption escapes.
- Source chain exactness: tested local `finish.py`, `tests/test_finish.py`, and both review JSON manifests were checked against matching Git blob SHA-1 after uploading; no private voice bytes were transferred to GitHub.
- Real owner voice and visuals were processed only on the local isolated host.
- Validation Gate (`dia01`): **17.5s, 525 frames, H264/AAC**. First proof finish **4.65s**, independent complete rerun **4.47s**, two byte-identical outputs: SHA-256 `2bb1af34c5da6e4291597ba0a53762f5bd206c6a67fdc8dcbeeed6dc6c86e752`.
- Parallel Execution (`dia02`): **23.6s, 708 frames, H264/AAC**, finished in **5.93s**, SHA-256 `ae9a653c463dbd1fff4e8afde9d81a4073413ab78247a05d529b965ff5c63de3`.
- Cache-specific Validation Gate test after adoption: **4.80s fresh / 1.15s cached** on this host. Source, voice, manifest and output digests must match; otherwise the cache is invalidated and the MP4 is rendered again.
- API spend: `$0`, no GitHub Actions or remote TTS. Real costs of local electricity/hardware and user editing still apply.

## What is NOT established

1. This module **does not contain a reusable motion scene renderer**. The clean original video for the demos came from the previously produced v1.2 local artifact.
2. The claim 'automatically produces new Shorts' is **not** supported; only finishing, preflight and cache are demonstrated.
3. Not tested on the user's Windows/WSL2 host, no security isolation certification, no mobile-native overlay QA, no word-level subtitle timing certificate or brand-source review. Byte-identical results established only on a single isolated Linux machine and pinned inputs.
4. `ILLUSTRATIVE_POC` is required in the initial module and outputs are always `release_state=BLOCKED`. Evidence-backed publish-ready content is explicitly **not implemented** and shall not be spoofed.
5. Does It Automate? is English only. EMERCOD is a distinct brand and its Spanish fixture was **intentionally excluded** from NINFA's module. Reuse across brands requires separate approved architecture.
6. No user audio, raw recordings, private voice hashes from receipts, heavy MP4s or secret environment files were committed to GitHub.
7. No prodAgentic workflow modification, no Cloud/CI media runtime, no automatic approval, upload or social schedule.

## Next acceptance gates

Run reproducibility and FFmpeg/font compatibility on the user's target workstation; add voice-time alignment QA or human adjustment receipts, visual frame renderer ownership, artifact-retention rules and actual mobile safe-area tests. For live evidence-backed videos, document sources and required rights and extend the contract only after review. Treat cached result integrity independently from approval authority.

**Decision:** `ADOPT_FOR_LOCAL_REVIEW_WORKFLOW` with explicit limitations; `HOLD_PUBLICATION`, `HOLD_GENERAL_RENDERER_CERTIFICATION`.
