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

## Owner Windows UAT — V2 technical rendering, 2026-10-23

**Environment:** Owner's Windows PowerShell, checkout `exp/remotion-visual-v2-20261023`, Remotion 4.0.538.

**Owner-reported test results:**
- `npm test`: **14 passed / 0 failed**, including the new bounded V2 command test.
- `npm run typecheck`: **PASS**.
- All 3 V2 compositions bundled, rendered, encoded and generated the CLI wrapper's structural `ffprobe` receipts. Output files are private, in sibling `NINFA-Review/renders`; **no MP4 bytes were uploaded for V2 independent visual review**.
- Codec H.264, 1080×1920, 30fps; no audio; all receipts `release_state: BLOCKED`, `publish_authority: NONE`.

| Composition | Output | Frames / clip length | Elapsed wall time | Approx size | Reported video SHA-256 |
|---|---|---|---:|---:|---|
| `CacheRaceV2` | `cache-v2.mp4` | 180 / 6s | 60,301 ms | 837.5 kB | `8c2a683dee63a5322f77a6b8f23b3856d3a4342419303798aadad0f1a0ef083d` |
| `WebhookReplayV2` | `webhook-v2.mp4` | 720 / 24s | 62,661 ms | 1.6 MB | `0a379041b555af6f4a35ebb6ee9f9591af2bc066b60bf6b5b4aaa5a1f3e5724c` |
| `AutomationFailureV2` | `automation-v2.mp4` | 180 / 6s | 18,371 ms | 699.9 kB | `c166826eda457943d21e38bd29de937f6dfd20892a923007845f50c2d56fcc4c` |

**Caveats:** Previous V1 times: cache 14,550 ms, webhook 48,476 ms, automation 19,656 ms; these are **one-off wall times**, not matched benchmarks, and the V2 cache includes a cold bundle (~11.9s). MP4 file size is **not** evidence of motion quality. V1 and V2 props SHA values remain equal for each case, confirming that the supplied manifest props are identical; the artistic render output differs. The `windows.exe` command-not-found line before actual commands was not a NINFA test failure.

**Gate update:** `V2_WINDOWS_TECHNICAL_RENDER_PASS_REPORTED / INDEPENDENT_VISUAL_REVIEW_PENDING / RELEASE_BLOCKED`.

### Next visual comparison rubric (do not pre-score)

For each of V1 and V2, review first 0–2 seconds, midpoint, final frame, and in-between motion at normal playback speed:
- Is the hook understandable without pausing?
- Does the sequence reveal an **input → mechanism → outcome**, rather than just changing dashboards?
- Are numeric claims and source caveats visible long enough on a real 1080×1920 phone?
- Does the visual metaphor clearly distinguish reconstructed/illustrative scenes from actual measured evidence?
- Are there empty static holds, excessive reading, obscured text, off-safe-area content or redundant scenes?
- Are 6-second cuts too rapid, and are 24-second scenes unnecessarily padded?
- Can narration and phrase-aligned captions be added without visual collisions?

**No user visual preference judgment or production adoption result is recorded until the three actual V2 MP4s are inspected and accepted.**

## Candidate acceptance gate (currently OPEN)

- [x] `npm test` 14/14 + `npm run typecheck` PASS on owner Windows, no regressions in v1
- [x] All three V2 MP4s rendered and passed wrapper's ffprobe structural receipts (owner logs)
- [ ] Independent V2 MP4 pixel/motion quality audit
- [ ] Human compare V1 vs V2 on phone for temporal clarity / visible process / readability / nonrepetitive narrative
- [ ] Correct material caveats persist and are legible; no false measured process
- [ ] Match voice timing and validate v1.3 finisher independently
- [ ] Same-host benchmarks and dependency/rights audit
- [ ] Owner explicitly accepts visual direction. Until then: `V2_VISUAL_EXPERIMENT / PRODUCTION_HOLD / RELEASE_BLOCKED`

Unlike a full general motion renderer, these are **three bounded compositions**. Do not claim improved retention, speed, quality or video-factory certification without external evidence.
