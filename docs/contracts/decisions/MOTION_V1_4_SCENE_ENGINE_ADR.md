# ADR — Motion v1.4 bounded Scene Engine

**Date:** 2026-10-08, America/Lima. **Status:** ACCEPTED FOR ISOLATED REVIEW-ONLY EXPERIMENT, **not** production/publishing certification.

## Problem and decision

NINFA Motion v1.3 only assembles an already-rendered visual MP4 with privately held voice and captions. It cannot create the underlying visual story. Motion v1.4 adds a separate, **bounded** local engine:

```text
strict English NINFA JSON storyboard
    → selected visual family (Python/Pillow)
    → silent 1080x1920 H.264, 30fps, deterministic frame index
    → FFprobe and content-hash receipt
    → OPTIONAL later v1.3 finishing with separately approved PRIVATE voice
    → human QA; RELEASE BLOCKED
```

Three families for POC: `cache_race`, `circuit_breaker` and `source_lineage`. They must animate meaningful UI state changes on persistent layouts rather than cutting between unrelated static slides. **These are bounded composition primitives, not arbitrary-generative visuals or a full general-purpose scene language.**

## Authority and provenance

- Official [Does It Automate? brand v1](../../BRAND_IDENTITY.md), [channel thesis](../../CHANNEL_THESIS.md) and [Motion v1.0 policy](../DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md) prevail.
- Channel `DoesItAutomate`, text `en`, owner voice only later through v1.3; no fake logos, uploaded raw voice, remote clips, arbitrary HTML/JS, TTS, paid API, GitHub Actions for media, or publishing credentials.
- `ILLUSTRATIVE_POC` requires a visible **DEMO** label and no fabricated source/score.
- `EVIDENCE_BACKED` is **narrowly limited** to the v1.3 local cache result **4.80s fresh vs 1.15s cached on one host**, sourced to [the versioned receipt](MOTION_V1_3_LOCAL_FINISHING_2026-10-08.md). Do **not** generalize that ratio to other machines.
- All outputs are `TECHNICAL_PASS_REVIEW_ONLY` with `release_state=BLOCKED`. A machine-readable pass is not release approval.

## POC acceptance gates

1. Reject unsupported families, surprise JSON properties, Spanish, nonzero API budget, media Actions, publishing authority, raw voice, arbitrary tags, fake measurements and unsupported evidence.
2. Three distinct 6-second 180-frame visual outputs at 1080×1920 / 30fps / H.264; sample temporal variation and inspect mobile-safe readability.
3. Preserve source/manifest/output SHA, elapsed time, exact FFprobe count. No social posting, cloud runtime or upload.
4. Confirm compatibility with v1.3's clean-input video contract; the **actual voice-to-v1.4 run remains separately untested**.
5. Integrate into NINFA only as a manual, isolated tool with regression tests and documentation. Main long-form runtime and prodAgentic remain unchanged.

## Non-goals and product gates

No general renderer or broad content synthesis, no automatic topic selection, no personal voice ingestion, no cross-account export for EMERCOD, no YouTube publish APIs. Third-party files remain untrusted; OS no-egress/sandbox certification is open. Source/font licensing, owner approval on these new visuals, target WSL2 compatibility, visual safe zones on actual YouTube/TikTok, and word-level caption QA are pending.

**Engineering decision:** ADOPT a **narrow experimental rendering module**, HOLD generalized rendering and any publication authorization. Three different visual composition families are proof of flexibility within a very small parameterized set, **not** certification of all future Shorts.
