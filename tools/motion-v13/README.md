# Motion v1.3 — Local AV Finishing (engineering POC)

**Status:** `LOCAL_FINISHING_PROVEN / GENERAL_VIDEO_FACTORY_NOT_CERTIFIED / REVIEW_ONLY`.
**Authority:** NINFA's [Does It Automate? Shorts motion contract](../../docs/contracts/DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md) and its [voiced v1.2 owner UAT receipt](../../docs/contracts/decisions/MOTION_V1_2_OWNER_UAT_2026-10-08.md).

## Why v1.3 exists

Motion v1.2 rendered a complete clean animation and then re-encoded it with voice and captions. **Every new voice take or subtitle correction should not have to re-render the expensive frame-by-frame visualization.** This tool isolates and reuses the already-rendered *clean visual MP4*:

```text
original motion renderer (already built, not included in this module)
    → LOCAL clean video cache 1080x1920/30fps
    + PRIVATE voice WAV/M4A/MP3
    + review manifest with caption frame intervals
    → FFmpeg local subtitle burn-in + audio/video mux/encode
    → ffprobe stream/frame/duration checks
    → PRIVATE output MP4 + receipt; RELEASE BLOCKED
```

**No reusable visual frame renderer is claimed.** This is a tested, additive **AV finishing stage**, not a complete end-to-end generator, a prodAgentic adapter or a general-purpose media service.

## Requirements

- Python **3.11+**, standard library only for orchestration.
- Local FFmpeg and FFprobe with `libx264`, `aac`, `libass`, plus installed **Lato** font.
- Approved **1080×1920 H.264 30fps** visual source, with EXACT `duration_frames` already rendered, **without narration/captions**.
- The owner-controlled voice file, located privately on the local machine; never committed, linked or copied into GitHub.
- A matching review manifest in `fixtures/` (samples contain **text/timings only**, not private voice bytes or assets).

Local example from NINFA repository root:

```bash
# Fast unit/negative-gate checks (no FFmpeg media test, no internet):
python3 -m unittest discover -s tools/motion-v13/tests -v

# Preflight without writing a MP4:
python3 tools/motion-v13/finish.py \
  --manifest tools/motion-v13/fixtures/dia01.review.json \
  --visual "/private/path/validation-clean.mp4" \
  --voice "/private/path/validation-voice.wav" \
  --out "/private/output/validation" \
  --dry-run

# Finishing pass, local only:
python3 tools/motion-v13/finish.py \
  --manifest tools/motion-v13/fixtures/dia01.review.json \
  --visual "/private/path/validation-clean.mp4" \
  --voice "/private/path/validation-voice.wav" \
  --out "/private/output/validation"
```

The CLI **does not synthesize voice**, invoke Chatterbox or Kokoro, collect raw private recordings, call internet APIs, use GitHub Actions, or post/schedule anything. It cannot certify a speaker by audio analysis. The `mode=ILLUSTRATIVE_POC` and `publish_authority=NONE` constraints are fail-closed; all outputs remain **review only**, including when technical checks pass.

## Actual proof on 2026-10-08

**Tool and fixture code was run in the isolated ChatGPT Linux container, not on the owner's Windows/WSL2 host.**

| Test | Observed outcome |
|---|---|
| Unit and negative contract scenarios | **16/16 PASS**, including foreign language/brand, paid APIs, GitHub Actions, publication, extra keys, ASS caption injection and overlapping captions |
| `dia01` source | Previously rendered 17.50s / 525-frame clean visuals plus **private** previously approved real English owner voice |
| `dia01` finishing | **4.65 s** elapsed; output 1,016,684 B; H.264/AAC; 525 frames; 17.50 s |
| `dia01` repeat | **4.47 s** elapsed; identical full SHA-256 twice: `2bb1af34c5da6e4291597ba0a53762f5bd206c6a67fdc8dcbeeed6dc6c86e752` |
| `dia02` independent fixture | Previously rendered 23.60s / 708-frame clean visuals + private English owner voice |
| `dia02` finishing | **5.93 s** elapsed; H.264/AAC, 708 frames, 23.60s; SHA-256: `ae9a653c463dbd1fff4e8afde9d81a4073413ab78247a05d529b965ff5c63de3` |
| Cost & network | No paid API, no GitHub Actions, no TTS, no network access in the finishing code |
| Claimed gains | **Avoided rebuilding source frames on caption/voice revision**. No end-to-end speedup percentage is claimed (no like-for-like baseline). |

`ffprobe` validates structural truth: codec, duration, frame count. It does **not** assess editorial correctness, word-level alignment, mobile overlay collision, external fact provenance, pronunciation or contrast.

**Hash-keyed output cache:** a second run reuses the existing MP4 only when the visual SHA-256, private voice SHA-256, full manifest SHA-256, frame count, previous blocked-release receipt and output MP4 SHA-256 all match. Changing the audio, captions, manifest or output invalidates the cached result. Add `--force` for an unconditional fresh encode.

Observed on Validation Gate with the same source media: **4.80 seconds** fresh, **1.15 seconds** cached on this particular container. This is a measured single-case skip, not a general end-to-end speedup claim.

## Owner-approved voice treatment (2026-10-09)

Default to the owner-controlled voice recording **without added dynamic-range compression, loudnorm or EQ**. This v1.3 finisher currently sends the voice track to the AAC encoder **without explicit audio filters**, consistent with the owner's preferred A/B mix. Lossy AAC output is not bit-identical to input; listen to the exported MP4 at matched playback volume before approving. Add corrective audio processing only on observed need and after before/after owner listening approval. See [Natural Voice Mix UAT](../../docs/contracts/decisions/NATURAL_VOICE_MIX_UAT_2026-10-09.md). Technical peak checks alone cannot determine acoustic naturalness.

## Privacy, limitations and next gates

- **Do not commit** private `voice_master.wav`, `*.m4a`, finished videos, or `receipt.json` (receipt contains a hash of private voice). Local output directories should preferably be **outside** the checkout.
- This module is intentionally **DoesItAutomate English-only**. The EMERCOD Spanish demonstration proved method portability as a local experiment but its branding/language rules do **not** belong to NINFA's channel-specific contract.
- The explicit font `Lato` must be installed/verified on the target system. System codec availability, text shaping and binary repeatability can differ across FFmpeg/font versions and hardware. Byte-identical runs were observed only in the **same** container.
- No OS-level sandbox/no-egress or untrusted-media security audit has been certified; treat source files from untrusted parties as hazardous before passing to FFmpeg.
- No caption-time ASR validation. Manually timed phrases in v1.2 remain **review pending** for word-level accuracy.
- No automated production-worker authorization or `prodAgentic` integration. No publishing, upload or provider schedules, even when the receipt reads `TECHNICAL_PASS_REVIEW_ONLY`.
- New stories should select an original visual implementation and claims with independent evidence; avoid recycling `dia01`/`dia02` UIs as a generic template.

**Promotion gate:** test separately on the owner's target local host, independent audio/caption reviews, destination overlay QA, artifact rights, original content variation and third-party evidence; preserve the channel's frozen brand and existing motion v1.0 authority.
