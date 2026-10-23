# Independent visual audit — NINFA Motion V2 vs V1

**Date:** 2026-10-23 (America/Lima)
**Evidence:** Owner-uploaded original MP4s (V1) and actual V2 MP4s inspected locally using video-frame samples and full-size stills.
**Decision:** **V2 IMPROVES NARRATIVE, BUT FAILS CURRENT VISUAL-QUALITY GATE. HOLD / NOT FOR PUBLICATION / NO MERGE.**
**Scope:** artistic and informational quality of *these specific videos*. No inference of audience CTR/retention, commercial viability or renderer speed.

## Asset verification (actual bytes, not just owner console)

Independently SHA-256 hashed uploaded MP4s and checked FFprobe streams:

| Variant | SHA-256 (full) | Frames | Video duration |
|---|---|---:|---:|
| Cache V1 | `d7acce60a668accdd40e532a76e51fd233d7cf7bfc140df8fc82fd3144832f5e` | 180 | 6s |
| Cache V2 | `8c2a683dee63a5322f77a6b8f23b3856d3a4342419303798aadad0f1a0ef083d` | 180 | 6s |
| Webhook V1 | `e3ef3a5d9e936f4c11b2df8711b357a2083016264f78bf471df0f0de2128dda8` | 720 | 24s |
| Webhook V2 | `0a379041b555af6f4a35ebb6ee9f9591af2bc066b60bf6b5b4aaa5a1f3e5724c` | 720 | 24s |
| Automation V1 | `445a0eae53775a4d6eb55def0e7942985eb1d9192b8fe625e2351aec33d39b86` | 180 | 6s |
| Automation V2 | `c166826eda457943d21e38bd29de937f6dfd20892a923007845f50c2d56fcc4c` | 180 | 6s |

These V2 SHA-256 values **match the owner's Windows UAT receipts**; the specific rendered bytes were independently inspected. H.264 1080×1920 30fps, with no audio. Media not committed to GitHub. This does NOT constitute approval for YouTube.

## Source-grounded findings

### Cross-cutting issues — MUST FIX

**P0 / visible text collisions at scene transitions.** The scene-component crossfade overlays both scenes rather than separating visual layers. At about **1.6s Cache V2**, the headlines/metrics for `ONE VIDEO. TWO RENDERS.` and `BUILD THE VIDEO.` overlap; at about **4.2s Automation V2**, `TWO WORKED. FOUR BROKE.` and `TOOL USE ≠ SUCCESS.` overlap, corrupting the `2 / 8` line; at about **21.8s Webhook V2**, `2 ACTIONS BECOME 1.` and `CONCURRENCY NOT TESTED.` overlap. Other adjacent scene boundaries are vulnerable. Resolve through true mutually exclusive shots, cut-to-different-layout, or compositor-level masking; do not crossfade two overlapping text layouts over the same location.

**P1 / visual hierarchy and mobile text.** Typography in process nodes, labels, citations and limitations becomes very small at 270px-wide phone-style preview. The content heavily favors the upper/middle section with little action in the central viewport. No physical-device acceptance yet; visual source/caveat legibility must be verified there. Do not shrink provenance into unnoticeable footnotes.

**P1 / limited actual action.** V2 mostly changes text/cards via fades and occasional diagram connections; it still feels like an animated slide deck rather than an experiment. Show animated *state mutation*, moving event tokens, connection paths, cache hit/miss control, database rows, error branches and actual evidence-source linkages. All must be marked illustrative reconstructions unless original recorded footage exists.

**P1 / no owner-approved canonical logo, audio or phrase-aligned captions.** Silent compositions cannot pass final channel identity, mobile caption timing or narration QA. Do not substitute/generated a brand mark.

### CacheRaceV2 — PARTIAL IMPROVEMENT; HOLD

V1: near-static two bars. V2: numeric hook → first encode pathway → cache reuse pathway → measured comparison. The core 4.80s vs 1.15s on-one-host interpretation remains truthful, subject to source review. But process nodes are tiny, overall motion is mainly fades, and 1.6s transition has severe overlapping information. Four scene segments in six seconds risk overloading the viewer once voice/captions are added. The line `ONE VIDEO. TWO RENDERS.` can imply that two full encodes happened even though a cache hit skipped work; clarify the metaphor in future copy.

### WebhookReplayV2 — GREATEST STORYTELLING GAIN; HOLD

V1: two large numerical cards and arrow, little explanation. V2: two events → two naive writes → UNIQUE(event_key) → second sequential write ignored → 2/1 summary → explicit concurrency limitation. Better explanatory order and evidence protection. However it still devotes long periods to near-static centered cards, small event keys/SQL and line-level caveats, plus overlapping headlines around 21.8s. Critical caveat `CONCURRENCY NOT TESTED` appears at the final section but gets obscured by overlapping cards/text on entrance. Keep synthetic/sequential scope consistently visible.

### AutomationFailureV2 — DID NOT SOLVE CENTRAL PROBLEM; HOLD

V1: six PASS/FAIL cards + 2/8. V2: stronger `29 CALLS` hook and outcome, but the central section is still six cards rather than an actual workflow graph/data flow. High-priority accuracy risk: `TWO WORKED. FOUR BROKE.` is a summary of six illustrated named systems, whereas the benchmark's real score is **2 / 8 scored assertions** (two passed, six failed). The visualization and its hierarchy can mislead viewers into interpreting six systems as the eight scored checks. Source ledger confirms the public Qwen3.6-27B base archived run and explicitly prohibits attribution to NINFA. Prefer *eight scored assertion nodes* explicitly grouped by systems, or a real chronological per-assertion replay grounded in the public trace (do not infer sequence). Huge transition overlay corrupts the `2 / 8` result at ~4.2s.

## Motion sampling cross-check (not an artistic quality score)

An exploratory OpenCV calculation compared consecutive downscaled grayscale frames using mean absolute pixel difference. For a threshold <0.05 gray-level (0–255), the share of adjacent pairs with very little global pixel change was:

| Variant | V1 low-change pairs | V2 low-change pairs |
|---|---:|---:|
| Cache | 79% | 65% |
| Webhook | 91% | 76% |
| Automation | 78% | 56% |

This is a *non-perceptual heuristic*: affected by video compression, rendered grain/text/background and chosen threshold. It only supports the observation that V2 changes more pixels; it **cannot** certify good motion design or viewer attention. Do not use as evidence of retention.

## Decision and quality redesign gate

**V1:** technically sound but visually insufficient.
**V2:** technically sound and more explanatory, **visually rejected for production**.
**Remotion renderer:** technically feasible on local Windows; library not rejected.
**Adoption gate:** BLOCKED; PR #12 and #13 stay DRAFT; no merge/publish.

Required before new round of implementation:
1. Specify a **motion grammar**/shot system in docs: action-driven shots, narrative tension, one message per shot, variable pacing, entrance/exit without text collisions, spatial choreography and mobile safe areas.
2. Define explicit 6s and 24s storyboards with voice/caption budget and purpose of each frame range; no multiple stacked walls of text.
3. Preserve meaningful evidence/illustration differentiation, provenance and numerical truth (particularly AutomationBench's 8 scored assertions).
4. User approves shot/storyboard direction **before** additional custom code is piled on.
5. Implement a **single** vertical slice (recommend Webhook; clear input→mechanism→outcome), demonstrate its full motion and independently assess on phone. No three-way V3 bulk generation.
6. If vertical slice is acceptable, test Motion v1.3 voice/caption finisher; then consider additional templates and same-host performance/rights audits.

**Proposed state:** `RENDERER_TECH_PASS / VISUAL_V2_FAIL / MOTION_GRAMMAR_REDESIGN_REQUIRED / RELEASE_BLOCKED`.

The owner originally said V1 looked flat. That prompted V2, but only media review—not successful rendering—can validate that V2 was an improvement suitable for publication. The uploaded bytes confirm it is *not yet suitable*.
