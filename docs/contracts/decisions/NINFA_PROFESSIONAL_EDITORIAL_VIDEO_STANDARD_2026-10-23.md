# NINFA — Professional-editor video standard (editorial direction)

**Date:** 2026-10-23
**Status:** Editorial direction / proposed acceptance rubric. NOT a claim that the current output meets it.
**Scope:** Does It Automate? English YouTube videos, Shorts and long-form sequences.
**Owner brief:** "Debe parecer un video de esos que son editados, los que le pagabas a un editor para que lo haga." Higgsfield-grade photorealism is **optional**, not a requirement.

## Core intent

Produce **human-editor-quality technology documentary/explainer videos**, not silent, static product dashboards, generic presentations, AI-vibe slides, software-demo templates or imitation stock film. The audience should experience an intentionally edited audiovisual story about a real automation experiment, with measured facts and limitations communicated clearly.

The production value comes primarily from **editorial decisions**:
1. Structure: hook / test conditions / what happens / evidence / consequence / limitation / takeaway.
2. Voice-first editing: lock a credible English narration script and target performance before precise shot and caption timings. Text is not a substitute for narration.
3. Primary footage: prefer actual recorded test footage, real screencasts, console activity, tool UI, logs, artifacts, charts or documentary B-roll with provenance and rights; redact accounts, tokens, names and secrets.
4. Purposeful editorial montage: make cuts, punches, progressive reveals, tracked crop/zoom, speed ramps (when appropriate), match-cuts and reframes explain mechanisms. Avoid editing at a fixed artificial cadence.
5. Sound design: clear voice; quiet, licensed or original music; sparing click/impact/transition cues matched to meaningful events; balance loudness and avoid constant dramatic sound.
6. Visual system: restrained brand colors, functional hierarchy, strong contrast, professional typography, minimal kinetic headlines, backgrounds used intentionally, actual approved logo only.
7. Phrase-/word-aligned captions from **the final audio**, readable within platform overlays; no debug `CAPTIONS RESERVED` or `NO OFFICIAL LOGO` text in any candidate for publication.
8. Appropriate cinematic techniques (2.5D camera, depth-of-field, lens-like zoom, light or reconstructed 3D environments) are **optional** only when they materially clarify the story. Do not pursue generic Higgsfield-style spectacle.

## Footage evidence taxonomy

- **RECORDED:** Captured evidence from the actual run; may show authentic UI/logs and original metrics.
- **RECONSTRUCTED:** Programmatic visual reconstruction from verifiable experiment logs; label it as illustration/reconstruction. Do not fabricate the original chronological trace or beyond-scope tests.
- **ILLUSTRATIVE:** Metaphor/stock/AI-generated scene or B-roll, not proof that any real action happened. Label when a reasonable audience might otherwise mistake it for evidence.
- **UNVERIFIED:** Never publish as a factual claim or demonstrate as real footage until sourced and verified.

Clear on-screen and voice distinction between reconstructed events and recorded real-world results is mandatory. For Webhook replay specifically, two *sequential synthetic SQLite* deliveries, 2 naive actions and 1 guarded action are evidenced; network-provider behavior and concurrency are **not tested**. Do not reinterpret a moving graphic as factual evidence of a live webhook.

## What was wrong with the Remotion V1–V3 aesthetic

- Composition: static backgrounds, repeated headline + card/grid + footer, with few variations in shot size, framing or imagery.
- Motion: large share of the animation was small diagram or opacity changes; an editing-grade scene should be paced around a visible cause/effect.
- Audio: silence, no actual voice track, no sound cues, no phrase-synced captions.
- Content: too much small technical copy shown simultaneously; evidence stays in static footnotes instead of appearing when the statement is made.
- Story: cut points based on fixed shots instead of voice/action beats.
- Branding: no approved canonical logo bytes included, debug labels visible.

Technical correctness and accurate rendering are necessary but **not sufficient** for a professional-editor verdict.

## Editing brief: one local Webhook finishing pilot, not an all-NINFA migration

**Goal:** Convert the already tested 24s Webhook V3 visual proof into a complete, narratively edited **private audiovisual** demonstration without changing factual scope.

**Suggested shot inventory — not an automatically approved new timeline:**
1. 0–3s: urgent hook tied to the factual duplicate event; animated visual + narration, no overlong title card.
2. 3–7s: crop into authentic SQLite output or explicitly reconstructed event evidence; track two duplicate deliveries, one clear action per beat.
3. 7–11s: unprotected case, evidence-based two writes, readable highlighted row 1→row 2; an edit with cause and result.
4. 11–15s: show the unique constraint entering the technical demonstration with subtle punch/zoom, not another four-second stationary card.
5. 15–20s: trace the first success and second ignored attempt in a fluid continuous diagram; avoid misleading concurrency.
6. 20–24s: cut to clean 2→1 difference and clearly present **sequential only / concurrency not tested**, with final narration and an intentional ending.

This is an example **editorial structure**, not 1:1 mandated cuts: rewrite timings from the final voice performance and available authentic footage. Preserve provenance, script/visual truth and each material caveat.

**Finishing stack candidates (zero paid inference required for core functionality):**
- Research, script, real experiment receipt/manifests, local screencasts and human-reviewed evidence.
- Narration through owner-approved private recording or local Kokoro/Chatterbox where licensing and consent are cleared.
- Local timing/alignment and animated but understated captions.
- Remotion for measured graphics, timeline compositing and accurate data-driven diagrams; FFmpeg Motion v1.3 for local final assembly, codec/audio validation and signed review receipt.
- Optional Blender/Three.js for spatial shots if evidence/creative direction benefits. No new expensive model/API should become essential.
- Never use cloud/render/voice GitHub Actions; never auto-publish or add sensitive voice files to public Git.

## Objective and human acceptance gates

**Engineering (mechanical):** clean build; fail-closed source receipt; all frames and stream properties validated; versioned footage provenance; no unlicensed media; reproducible local inputs.
**Editorial (must be human evaluated):** a viewer can understand the hook and what was tested without reading a fixed dashboard; every shot earns its screen time; continuity, motion and visual hierarchy work at playback speed; no dead air or forced effects; professional voice/SFX balance; readable captions; mobile-safe right/top/bottom overlays; factual material limitations stay comprehensible.
**Channel fit:** credible testing over AI hype. Real evidence receives prominence; illustrative scenes are never treated as proof. Voice, style and logo use the channel-approved identity.
**Release:** owner approval is required *after* reviewing the finished MP4 on phone and desktop. A passing test suite, model-generated aesthetic, static screenshot rubric or subjective assistant opinion alone cannot authorize GO.

## Decision

**APPROVE AS DIRECTION / DO NOT CLAIM QUALITY ACHIEVED.**
- Stop making new mute 3-way V4/V5 scene packs to chase visual polish.
- Keep Remotion as a **possible compositor**, not the editorial strategy.
- Test one **voice-led, professionally edited** Webhook full audiovisual slice. Compare directly with reference examples from human-edited technical YouTube videos and owner feedback.
- If full edited slice still looks like PowerPoint, redesign editing format/media mix; do not confuse that with a reason to rewrite all underlying rendering code.

**Repository state:** purely creative/requirements document in experimental branch; does not change `main`, release state or GitHub publishing authority.
