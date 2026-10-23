# ADR — Remotion visual renderer for Project NINFA

Date: 2026-10-23 (America/Lima)
Status: ACCEPTED FOR ISOLATED POC / PRODUCTION NOT APPROVED
Release: BLOCKED

## Context
NINFA MK1 has proven its local FFmpeg long-form pipeline; Motion v1.3 already handles local voice and captions, v1.4 has narrow Pillow compositions, and v1.5 has evidence-first SQLite replay. Remotion could improve visual flexibility but cannot solve audience retention alone.

## Decision
Evaluate exactly three silent 1080x1920 30fps React/Remotion compositions under tools/remotion-poc, with a narrow read-only adapter referencing actual canonical NINFA manifests. Existing FFmpeg, voice and all existing Motion engines remain untouched. Version candidate: Remotion 4.0.538. No GitHub Actions media, external APIs, hosted inference, paid spend, automatic distribution or publishing credentials.

Cases:
1. Cache proof: measured 4.80 s fresh vs 1.15 s cached ON ONE LOCAL TEST HOST (Motion v1.3 receipt / v1.4 fixture).
2. Synthetic SQLite duplicate event: naive 2 actions, unique-key guarded 1; SEQUENTIAL, no concurrency or real provider claims (Motion v1.5).
3. Third-party archived AutomationBench result: Qwen3.6-27B base public run, 2/8 assertions, 29 calls; NOT executed by NINFA (Video 003 archived replay).

Architecture: canonical source/receipt -> fail-closed adapter -> typed bounded Remotion compositions -> local silent MP4 -> ffprobe + private SHA review receipt -> FUTURE independently evaluated Motion v1.3 finishing -> human/mobile/editorial QA -> explicit owner approval under the existing publishing contract.

Authority: docs/BRAND_IDENTITY.md and docs/contracts/DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md. English narration and captions; official brand bytes only or omit logo. Experimental 220 top / 350 bottom / 85 lateral safe-area margins are NOT official YouTube requirements. Source truth, recorded voice privacy and current natural untreated voice policy remain intact.

## POC acceptance
- Install reviewed and pinned dependencies with a committed lockfile on an approved local host.
- Run offline adapter tests, reject changed source metrics or unknown families.
- Successfully render all 3 silent videos; confirm H264 1080x1920 30fps, exact frames and no unexpected audio.
- On the SAME host, compare three cold/warm runs of cache versus v1.4 (180 frames) and webhook versus v1.5 (720 frames); report median wall time, CPU/RAM, file size, machine versions and subjective readability. No fair automation baseline exists, so avoid fake speed ratios.
- Verify rendering with actual mobile screen, captions/audio v1.3 separately, licensing/dependencies, original design and real evidentiary claims. No publication permission inherited from passing POC tests.

Remotion is specially licensed, not blanket MIT. Individual/eligible small-entity free use is documented upstream; reassess commercial eligibility and evolving 5.0 terms before broad adoption.

Gates: GO CANDIDATE only after all evidence; HOLD on unknowns; REJECT on licensing, truth, unsafe source execution, prohibitive resources or poor mobile readability. As of this ADR, no MP4/benchmark proven, no shipping or automated publishing authorized.

References: https://github.com/remotion-dev/remotion , https://www.remotion.dev/docs/ssr , https://www.remotion.dev/docs/composition , https://github.com/remotion-dev/remotion/blob/main/LICENSE.md .
