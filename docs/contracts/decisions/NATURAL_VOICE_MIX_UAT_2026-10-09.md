# Audio UAT — Owner natural voice is the reference (2026-10-09)

**Channel:** Does It Automate? (NINFA).  
**Decision:** `NATURAL_VOICE_MIX_ACCEPTED` for the *The Duplicate Webhook* private review variant.  
**Scope:** approval of voice presentation **only**, not a full review of captions, audiovisual pacing, logo/rights, release or posting.  
**Normative parent:** [Shorts Motion Contract v1](../DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md).

## Why this decision exists

The owner heard the previously delivered voice-integrated `The Duplicate Webhook` Short and reported the audio sounded too saturated. The first mix had received an audio compressor and loudness normalization. Its earlier engineering gate verified no measured digital clipping, but that finding **did not certify naturalness, distortion-free source capture or subjective listening comfort**.

An A/B review was then performed using the **same video frames and captions**, replacing the processed audio with the user's source recording **without additional compressor, loudness normalization or EQ**. The owner explicitly replied: **"Ok me gusta"** to that untreated-voice review output.

Previously reported measurements, retained as historical observations rather than universal targets:

| Variant | Observed integrated loudness | Observed sample peak | Owner impression |
|---|---:|---:|---|
| Prior additionally mastered voice | ~−18.3 LUFS | ~−0.9 dBFS | Too saturated / harsh |
| Original-source voice, no added audio DSP | ~−20.6 LUFS | ~−2.4 dBFS | **Preferred and accepted** |

These two sets of numbers **do not establish an optimal LUFS or sample-peak target** for all future recordings, nor prove that codec compression, source microphone distortion, true peak issues or tonal differences are absent. Do not replace listening with a numerical peak gate.

## Required baseline for subsequent voiced Shorts

- `OWNER_HUMAN` source voice is the default approved acoustic reference. Preserve the natural speaking rate, pronunciation, accent, dynamics and breathing/pause choices.
- **Default audio DSP chain: none** — no additional dynamic-range compression, `loudnorm`, loudness gain boost, EQ, denoise, de-esser, pitch or time stretching. Keep necessary trim/sync and format conversion to MP4-compatible AAC (which is **lossy codec encoding**, not lossless sample identity).
- Re-check the exported MP4 by listening to it, not just the source WAV/M4A. Compare at **matched playback loudness** to avoid a louder-is-better bias.
- Only enable corrective processing after an identified problem, with an audibly compared before/after and explicit owner approval. Do not assume that aggressive processing is a professional default.
- Detect clipping, channel problems, excessively low volume, codec artifacts and background noise as independent QA checks. `peak below 0 dBFS` alone is insufficient. If microphone distortion is embedded in the original, removing processing will not necessarily repair it.
- Work only on a local/private owner-owned voice reference. Never upload the source recording, derived voice fingerprints, final private MP4s or per-recording receipts into Git. No paid voice APIs or GitHub Actions media production.
- `tools/motion-v13/finish.py` already constructs its FFmpeg output with AAC conversion **without explicit compressor/EQ/loudness filters**. Do not silently add such filters in later revisions without change review and a comparative listening test.
- Human editorial gate is still independent of waveform QA. The `The Duplicate Webhook` narrative is a synthetic, local, **sequential** SQLite experiment; the owner audio preference does not certify real webhook provider behavior, concurrent idempotence, subtitles, mobile overlays or a ready-to-publish asset.

## Change-control and verification

Treat the baseline as `NATURAL_UNPROCESSED_VOICE_V1` (meaning *no extra processing*; it does **not** mean unencoded or bit-identical final AAC). Changes require a newly reviewed sample and documentation of input, output, rationale and user listening decision.

**Current release authority:** `NONE`. **Status:** `MIX_STYLE_ACCEPTED`; `SHORT_RELEASE_BLOCKED`.
