# NINFA / Remotion visual audit and Motion V2 redesign

Date: 2026-10-23 · **REVIEW-ONLY** · Owner feedback: "se ven muy planos"

## Primary evidence

The user uploaded actual MP4s: `cache.mp4` (6s/180 frames), `automation.mp4` (6s/180 frames) and `webhook.mp4` (24s/720 frames). Sampled multi-frame contact sheets showed:

- **CacheRace:** one unchanging title and two bars growing; does not show fresh encode vs cache-reuse process.
- **WebhookReplay:** one fixed title/layout for 24 seconds, an early red card, late green card; long low-information holds; source caveat tiny.
- **AutomationFailure:** six card reveals and a terminal 2/8 number; no meaningful system transition, connection or clear story; third-party archived trace attribution is essential.
- Across all three: overly small supporting copy, disproportionate unused space and repeated dashboard/card compositions. A structurally valid MP4 is **not** an audiovisual-quality pass.

## Motion V2 hypothesis, not production decision

Maintain provenance; replace metric-poster choreography with three distinct visual metaphors:
1. `CacheRaceV2`: numeric hook → fresh encode pipeline → cache hit/reuse path → grounded before/after bars. Same 4.80s and 1.15s one-host receipt, no universal speed claim.
2. `WebhookReplayV2`: duplicate synthetic event → both sequential writes → UNIQUE(event_key) constraint → second insert ignored → two-vs-one summary → explicit **concurrency not tested** final frame. No third-party provider or concurrent trace impersonation.
3. `AutomationFailureV2`: 29 calls hook → illustrative named systems revealing PASS/FAIL → 2/8 benchmark scoring result. Source is archived third-party Qwen3.6-27B base public run; the six named systems are NOT the eight per-assertion timeline. Never claim the run belongs to NINFA.

## Contract preservation

Brand frozen; graphite/offwhite/cyan, no substitute logo. Source manifests stay fixed and are checked by the existing adapter; neither the source's numbers nor blocked publication status are writable via React. V2 uses deliberate frame-based state changes and large first-screen copy, not arbitrary user HTML, external assets, stock footage or remote generation. Audio/captions remain out of scope, with existing Motion v1.3 unchanged. Safe zones are experimental; mobile device review required.

## Candidate acceptance gate (currently OPEN)

- [ ] `npm test` + `npm run typecheck` on owner Windows, no regressions in v1
- [ ] All three V2 MP4s rendered and passed ffprobe receipts, independent pixel QA
- [ ] Human compare V1 vs V2 on phone for temporal clarity / visible process / readability / nonrepetitive narrative
- [ ] Correct material caveats persist and are legible; no false measured process
- [ ] Match voice timing and validate v1.3 finisher independently
- [ ] Same-host benchmarks and dependency/rights audit
- [ ] Owner explicitly accepts visual direction. Until then: `V2_VISUAL_EXPERIMENT / PRODUCTION_HOLD / RELEASE_BLOCKED`

Unlike a full general motion renderer, these are **three bounded compositions**. Do not claim improved retention, speed, quality or video-factory certification without external evidence.
