# Does It Automate? — Shorts Motion Contract v1.0.0

**Authority:** Project NINFA, public channel **Does It Automate?** (\`@DoesItAutomate\`).
**Decision date:** 2026-10-08 (America/Lima).
**Approval classification:** **CREATIVE DIRECTION ACCEPTED BY OWNER** after viewing PV-POC-006; **individual assets and reusable production system NOT certified**.
**Change status:** Proposed versioned document on an isolated PR until merged into the NINFA default branch.
**Depends on:** [Frozen Brand Identity v1](../BRAND_IDENTITY.md), [Channel Thesis](../CHANNEL_THESIS.md), [Media Storage Policy](../MEDIA_STORAGE_POLICY.md), [Distribution Strategy](../DISTRIBUTION_STRATEGY.md).
**Machine contract:** [JSON Schema](shorts-motion-v1.schema.json); [non-sensitive PV-POC-006 fixture](fixtures/pv-poc-006.reference.json); [offline validator](../../tools/contracts/validate_short_contract.mjs).

## 1. Decision: freeze *a visual language*, not one template

PV-POC-006 was preferred by the owner over PV-POC-005. Preserve the demonstrated direction:

1. **Show the work.** Use visual state transitions, real interfaces/logs/diagrams/meaningful motion rather than text-only posters. Distinguish **real evidence** from clearly labeled illustrative UI.
2. **Motion has a cause.** Every substantial animated beat communicates an input, transformation, decision, measurable result, contradiction, or a verified state change. Motion-only decoration cannot replace proof.
3. **Tech-lab, not generic AI slop.** Graphite/near-black foundation, off-white content, measured electric-blue/cyan highlights; high contrast, clear hierarchy, restrained glow; avoid purple AI gradients, glowing brains, robot-head clichés and stock filler.
4. **Narration leads; visuals explain.** English voiceover, English on-screen labels and English captions. Align transitions to the *actual* audio timebase. Speak naturally; never accelerate the owner’s voice just to match an arbitrary runtime.
5. **Original compositions.** Reuse components and rhythm rules, **not identical scripts, hooks, screen sequences or storyboard scaffolding** across multiple releases. Different experiments deserve different visual evidence.
6. **Channel brand is not a freehand logo.** Only embed the exact approved mark from the latest owner-approved brand guide; if unavailable, **do not fake, trace, reinterpret or reconstruct it**. The deprecated circuit-D logo must never return.
7. **Human approves release.** A passing MP4 test does not certify editorial truth, voice performance, correct brand asset, mobile-safe overlay placement, or publication.

This is a **design-direction contract** for NINFA’s English-language Shorts. It is **not** a claim that PV-POC-006 (a stylized demonstration with illustrative interface screens) is ready to publish, or that its 10-second script is a general winning formula.

## 2. Narration and audio ownership

- **Allowed source types:** \`OWNER_HUMAN\` (preferred reference), \`LOCAL_CHATTERBOX\`, \`LOCAL_KOKORO\`, or intentional \`NONE\` with separately approved text-led format. Any synthesized narration must pass subjective English pronunciation/prosody QA.
- **Disallowed for this zero-paid-API operating profile:** paid TTS/video APIs, Piper/eSpeak as auto-approved production voices, periodic GitHub Actions voice rendering and mandatory cloud inference.
- Chatterbox is a locally documented production candidate ([voice cloning guide](../VOICE_CLONE_CHATTERBOX.md)), not permission to ingest personal references into third-party services. Kokoro remains a local alternative.
- Preserve owner-controlled voice recordings **outside public GitHub and source PRs**, with explicit consent for any clone, and do not redistribute narrator reference clips.
- Audio mastering can remove noise, normalize level and trim silence; pitch, tempo and accent should not be modified without listening/approval.
- No background music is required. Only add sound effects or licensed music where they contribute information and are permitted; \`$0 API\` is **not** a claim of zero electricity, editing time, storage or hardware cost.

## 3. Content and evidence rules

Canonical editorial question: **“We test AI systems on real work.”** The current evidence-backed Shorts pattern is **EXPECTATION → ACTION → CONTRADICTION → PROOF → LESSON**, when a real contradiction exists. Other formats are permissible only when they show a real system outcome rather than fabricated benchmarks.

Separate content modes:

| Mode | Meaning | Release posture |
|---|---|---|
| \`ILLUSTRATIVE_POC\` | Synthetic/mock interfaces to test composition or engineering capability | **Not eligible for publication as a real experiment**; explicitly label demonstration and keep release blocked |
| \`EVIDENCE_BACKED\` | Claims grounded in actual evidence, source, verified artifact and attributable experiment | Eligible for human editorial review after all evidence and QA gates |
| \`MIXED_LABELED\` | Real results plus reconstructive or illustrative animations | Must distinguish both visually; source links and reconstruction disclosures required |

- Never display unobserved \`PASS\`, \`RESULT VALIDATED\`, \`READY TO PUBLISH\`, throughput, latency, revenue, benchmark score or automated behavior as if verified. In a POC, mark mock/status indicators as **DEMO / SIMULATED** or remove them.
- Source evidence must be retained and accurately attributed. UI reconstructions must be labeled and must not impersonate third-party products.
- Novelty applies at topic, incident, hook, visual metaphor and storytelling level; a new text overlay does not make a reused short original.
- The first 1–3 seconds should orient viewers immediately to an actual contradiction/experiment outcome when available, **not a mandatory branded intro**.

## 4. Temporal and mobile presentation constraints

**Default configuration for PV-POC-006 only:** 1080×1920 pixels, 30 fps, 10 seconds, H.264 video with AAC audio (or intentionally silent export). These dimensions are a proven **experiment configuration**, not universal limits on short duration/format.

- Author timings in integer **frames**; enforce \`duration_frames = round(duration_seconds * fps)\`, ordered, non-overlapping beat ranges and subtitles within video bounds.
- Important words/UI states must be readable on a physical mobile screen. No blanket claim that all graphics are accessible merely because the encoder succeeded.
- Initial *experimental* protection margins at 1080×1920: **top 220 px, bottom 350 px, left/right 85 px**. These are **NOT an official YouTube Shorts/TikTok safe-area specification**. Retest overlays on the actual target platform/device before publication.
- For narration-led Shorts: meaningful subtitles must follow the actual words and timing, normally 1–2 concise lines. No subtitle over important data, labels or controls.
- Provide visual evidence of transitions (sampled or decoded frames, contact sheet, detected state differences) plus manual inspection for overlaps, jitter, clipping, flicker, motion accessibility, legibility and pacing.
- Never let the renderer modify final spoken content or create new factual claims.

## 5. Engineering boundaries and resource budget

\`\`\`text
NINFA editorial & evidence → approved English script and reference ownership
→ storyboard (timed, frame-based; explicit evidence-vs-demo state)
→ locally generated graphics / actual approved evidence
→ privately held English voice WAV (or approved local offline TTS)
→ FFmpeg local MP4 → ffprobe + visual/audio QA
→ human editor-in-chief → approved export bundle
                          ╳ automatic posting/scheduling authority
\`\`\`

- **S/ 0 / US$ 0 paid-API spend is the hard default.** No API billing, subscription, quota-based remote inference or new hosted worker without separate owner authorization.
- **No GitHub Actions for video/voice production.** Existing experimental CI proof is archival only; local rendering is the execution target. GitHub hosts documentation, source and small manifests—not human voice clips or final production MP4s.
- Preserve exact voice reference privacy, local media asset provenance, font and SFX licenses. Treat third-party file/script ingestion as untrusted; sandbox no-egress/no-secrets before executing arbitrary supplied HTML/JS.
- The NINFA channel contract does **not** transfer brand/voice to \`content-seller\` or \`prodAgentic\`. The distinct [programmatic-video candidate architecture](https://github.com/Em3rc0d/personal_knowledge/pull/30) and [prodAgentic RFC #71](https://github.com/Em3rc0d/prodAgentic/issues/71) require their own product authority. Keep the static PNG renderer untouched.
- No automated uploading, scheduling or publishing is authorized by this contract. Provider-side publication requires a **separate explicit approval and durable receipt**.

## 6. Artifact gates: machine PASS is not editorial PASS

| Gate | Required evidence to pass | PV-POC-006 observation |
|---|---|---|
| \`G0\` Scope and source ownership | English script, allowed voice and assets, rights, no private audio committed | Human voice recorded; private distribution only |
| \`G1\` Motion clarity | At least three distinct purposeful beats; input/state → change → explanation; real mobile review | Owner **prefers this direction** vs PV-POC-005 |
| \`G2\` Technical | Render succeeded, format/duration/frame count/audio codec observed, source+tool versions, receipt | **PASS for technical pilot**: 1080×1920 H264/AAC, 300 frames, 10 seconds |
| \`G3\` Truth and brand | Verified claims or labels; canonical logo bytes only if approved; no mock result pretending real | **NOT PASSED**: demo UI, no official mark embedded, claims need contextual labeling |
| \`G4\` Audio and captions | Voice intelligibility, sync, pronunciation, captions not obstructing content | Automated preliminary checks; human detailed QA remains open |
| \`G5\` Platform and accessibility | Real phone preview and measured destination overlays; readable labels, motion/photosensitivity QA | Experimental margins only; **NOT CERTIFIED** |
| \`G6\` Publishing | Human release approval, exact artifact digest, correct title/claims, provider authority independent | **BLOCKED**; no upload/schedule/publish performed |

**Release is fail-closed:** a \`BLOCKED\`, \`PENDING\` or \`REJECTED\` required gate prevents \`APPROVED_FOR_EXPORT\`. \`ILLUSTRATIVE_POC\` is automatically \`BLOCKED\` for normal publication.

PV-POC-006 observed output digest (not stored in Git):
\`bc17ebb25da40252abc092afb420a97695ec9d0b0f80e50cfc152d1d98dfce98\`.
Its raw/processed owner-voice assets remain private, not included in this repository.

## 7. Anti-template test: required before adopting as a reusable channel standard

Create **three genuinely different examples** using different truthful technical stories and varied visual composition (not 3 rewordings of the idea→script→design→render sample). At least one should include actual evidence/attributed data rather than fabricated UI. Compare on mobile with the owner; review:
- independent state-change clarity without subtitles;
- true claim ↔ displayed proof correspondence;
- caption collisions and visual hierarchy;
- natural narration and deliberate silent beats;
- freshness vs previous shorts, and no repeated hooks/visual skeleton.

**Promotion decision:**
- **NOW:** \`CREATIVE_DIRECTION_ACCEPTED\` — freeze design principles for drafts.
- **NOT YET:** \`TEMPLATE_CERTIFIED\`, \`CHANNEL_PUBLISH_APPROVED\`, \`AUTOMATED_VIDEO_ADAPTER_READY\`.
- **Next evidence:** 3 independent variations + human QA + at least one real proof-based story + storage/runtime/rights review. A subsequent versioned decision must cite these artifacts.

## 8. Change control

- The frozen v1 channel brand cannot be modified by this contract. If conflict arises, [Brand Identity](../BRAND_IDENTITY.md) and [Channel Thesis](../CHANNEL_THESIS.md) win.
- Breaking changes (visual identity, narrator policy, trust/release authority, English-only rule, expense budget) require owner approval and new **major** contract version.
- Non-breaking refinements to illustrative presets, default timings or QA diagnostics receive minor/patch versions plus a review note.
- The channel-specific creative contract is independent from any future cross-account rendering schema in prodAgentic.

**Editor-in-chief decision on PV-POC-006:** "Me gusta más." This is evidence of **relative creative preference**, not permission to publish, a guarantee of audience performance, or a universal endorsement of every mock QA claim.
