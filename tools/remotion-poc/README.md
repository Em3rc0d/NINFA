# NINFA / Remotion: local POC v0.1

**Status: 3/3 WINDOWS RENDER TECHNICAL PASS REPORTED; VISUAL/MOBILE QA + BENCHMARK PENDING; RELEASE BLOCKED.**

This isolated tool is an optional **silent visual** experiment. It does not replace the existing Python/Pillow Motion v1.4/v1.5, v1.3 FFmpeg voice/caption finisher, long-form production, content research or YouTube operations.

## What exists

- Three React/TypeScript compositions: `CacheRace` (6s), `WebhookReplay` (24s), `AutomationFailure` (6s), all 1080x1920 / 30fps.
- Read-only, fixed-path adapters that verify canonical NINFA fixture contents and the SQLite receipt hash, and preserve the source caveats.
- `node:test` positive/negative scenarios and a local render CLI that checks ffprobe and writes a private SHA-256 receipt with `release_state=BLOCKED`.
- Preview graphics only. **Official brand logo not embedded:** canonical approved bytes are absent. Video 003 is explicitly THIRD-PARTY archival evidence, never a NINFA-run benchmark.

## Installation & testing

Node 20+ and FFmpeg/FFprobe installed. The owner's Windows host successfully completed three CLI renders with H264/ffprobe receipts on 2026-10-23 (see [Windows evidence record](../../docs/contracts/decisions/REMOTION_WINDOWS_RENDER_UAT_2026-10-23.md)). The final MP4 bytes have not been independently inspected. Install dependencies only on a trusted networked host.

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

## Fix: render CLI sees the Studio startup page on localhost:3000

When Studio is running on port 3000, Remotion CLI might accidentally hit
its HTML startup page instead of its own bundled rendering server, raising
`window.getStaticCompositions is undefined`. The render wrapper now
**reserves a distinct ephemeral TCP port from the operating system** and
passes it to Remotion as `--port=<number>`. This is independent of the
Studio URL; Studio may remain open during renders.

After updating this branch, rerun `npm test` and `npm run typecheck`;
then execute the three `node scripts/render.mjs ...` commands again.
You do **not** need to reinstall packages or Chrome. If another server
races to occupy the selected port, retry once, or stop Studio with Ctrl+C
and rerun. No render success is asserted until MP4 and ffprobe receipt exist.

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

## Windows 2026-10-23 validation and Node 24 hardening

After the Studio/:3000 conflict was fixed, the owner reported **10/10 tests, TypeScript typecheck, and three technical MP4 renders** on Windows. The renderer's H264 / FPS / frame-count receipts are recorded in [the Windows evidence record](../../docs/contracts/decisions/REMOTION_WINDOWS_RENDER_UAT_2026-10-23.md). Visual review has not been performed here.

Node 24 emitted `DEP0190` due to the Windows shell wrapper. We now execute the installed Remotion CLI JavaScript entrypoint directly through `process.execPath` with `shell:false`. The separate-port logic remains unchanged. The owner subsequently confirmed **13/13 tests PASS**, TypeScript typecheck PASS and a full hardened CacheRace MP4 render on Windows Node 24.11.1 with no DEP0190 warning (commit `f5606c2`). Its SHA-256 matches the pre-hardening render. The remaining gates concern visual QA, Pillow comparisons, v1.3 finishing, dependency/rights review and release authority.

## Go/no-go

**GO candidate only after:** 3 actual render proofs, typecheck and test results, mobile review, licensing/dependency audit, measured performance and separately verified v1.3 finishing. **HOLD currently.** Render PASS cannot authorize exporting, uploading or publishing. Never use GitHub Actions to synthesize voice/video. No paid APIs.

ADR: `docs/decisions/ADR-2026-10-23-REMOTION-POC.md`.
