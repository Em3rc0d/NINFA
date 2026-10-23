# NINFA / Remotion: local POC v0.1

**Status: engineering scaffold; real Remotion rendering NOT YET VERIFIED; media release BLOCKED.**

This isolated tool is an optional **silent visual** experiment. It does not replace the existing Python/Pillow Motion v1.4/v1.5, v1.3 FFmpeg voice/caption finisher, long-form production, content research or YouTube operations.

## What exists

- Three React/TypeScript compositions: `CacheRace` (6s), `WebhookReplay` (24s), `AutomationFailure` (6s), all 1080x1920 / 30fps.
- Read-only, fixed-path adapters that verify canonical NINFA fixture contents and the SQLite receipt hash, and preserve the source caveats.
- `node:test` positive/negative scenarios and a local render CLI that checks ffprobe and writes a private SHA-256 receipt with `release_state=BLOCKED`.
- Preview graphics only. **Official brand logo not embedded:** canonical approved bytes are absent. Video 003 is explicitly THIRD-PARTY archival evidence, never a NINFA-run benchmark.

## Installation & testing

Node 20+ and FFmpeg/FFprobe installed. A networked machine is needed to install dependencies; this current ChatGPT execution host cannot fetch npm packages, so the MP4 outputs have not been produced or seen.

```bash
cd tools/remotion-poc
npm test
npm install
npm run typecheck
npm run studio

# Output path must be absolute and OUTSIDE the Git checkout.
node scripts/render.mjs cache /tmp/ninfa-remotion/cache.mp4
node scripts/render.mjs webhook /tmp/ninfa-remotion/webhook.mp4
node scripts/render.mjs automation /tmp/ninfa-remotion/automation.mp4
```

Windows example output: `C:\\NINFA-Review\\cache.mp4`. Do not upload owner voice, review masters or heavy media to Git. **Audit and commit a pinned package-lock.json on the host** after dependency and license review, before any production adoption.

## Truth modes

| Scene | Evidence source | Cannot imply |
|---|---|---|
| cache | `tools/motion-v14/fixtures/cache-proof.json` + v1.3 receipt | Global encoding speedup; observed on one host only |
| webhook | `tools/motion-v15/story.json` + content-hashed `replay_evidence.json` | Real webhook provider or concurrent safety; local *sequential* simulation |
| automation | Video 003 `scene_manifest.json` + `FAILURE_REPLAYS.md` | NINFA ran the benchmark or GPT-5.6 generated the trace |

Automation illustrates six named systems for storytelling; these do **not** correspond one-to-one to the eight scoring assertions. No misleading claim should be made from panel count. All exported artifacts remain demo/review only.

## Same-host benchmark plan

Baseline `cache`: run `python tools/motion-v14/engine.py --manifest tools/motion-v14/fixtures/cache-proof.json --out /absolute/private/baseline-cache.mp4` at the NINFA repository root.

Baseline `webhook`: run `python tools/motion-v15/build.py --out /absolute/private/baseline-webhook` (silent scene 24s) at root.

Compare equivalent duration/size/fps on identical local hardware with three cold and three warm trials each; record Node/Python/FFmpeg versions, CPU/RAM, median wall time, frame count, media bytes and rendered-image legibility. **Automation has no like-for-like baseline; no renderer-speed ratio is valid.** Test visual originality, safe areas on real mobile, factual accuracy, source rights, and audio compatibility with v1.3 independently.

## Go/no-go

**GO candidate only after:** 3 actual render proofs, typecheck and test results, mobile review, licensing/dependency audit, measured performance and separately verified v1.3 finishing. **HOLD currently.** Render PASS cannot authorize exporting, uploading or publishing. Never use GitHub Actions to synthesize voice/video. No paid APIs.

ADR: `docs/decisions/ADR-2026-10-23-REMOTION-POC.md`.
