# NINFA — Offline editorial audiovisual feasibility experiment

**Date:** 2026-10-23 (America/Lima)
**Status:** `END_TO_END_ASSEMBLY_TECH_PASS / OWNER_REJECTED_EDITORIAL_QUALITY / APPROACH_STOPPED / RELEASE_BLOCKED`
**Purpose:** Test whether NINFA can locally assemble something resembling a *human-edited technology explainer*, rather than assume a silent Remotion composition equals a finished YouTube video.

## User-directed quality target

The objective is not necessarily Higgsfield-style AI photorealism; it is **a video that feels edited by a paid human editor**: real footage/evidence, narrative voice, deliberate cuts, reframes, appropriate motion, sound design, readable captions, official channel identity and fact-checked claims. The existing Webhook V1–V3 compositions by themselves do not meet this standard.

## Source boundaries

- Owner-provided input: `webhook-v3-polished.mp4`, **SHA-256** `8e8b4f76be482a0021ee9a456c6c9f937881b33e935889529829ed72a276a277`.
- NINFA public receipt: `tools/motion-v15/evidence/replay_evidence.json`, local synthetic **SEQUENTIAL** SQLite replay of two deliveries of `evt_local_001`; naive **2** stored actions, uniqueness guard **1** stored action, second insert ignored.
- The input visuals themselves are a **reconstruction**. No cloud webhook, production concurrency, financial transaction or real external workflow was recorded.
- Source metadata and logo policy remain unchanged. No counterfeit owner logo was created.

## What was actually built and measured in the current container

Created a completely local 24-second **private editorial feasibility sample** using the verified owner video and a temporary Python + FFmpeg assembly script. The ChatGPT local container has FFmpeg 7.1.5, Python/Pillow/NumPy/SciPy and eSpeak; it **does not have a preinstalled natural-sounding voice model such as Kokoro or Chatterbox**.

The sample incorporates:
- Seven fact-grounded editorial beats (hook 0–2.6s, naive 2.6–6.7s, source receipt 6.7–9.8s, unique key 9.8–13.3s, guarded 13.3–18.4s, comparison 18.4–21.2s, limitation 21.2–24s).
- Camera-like punches/reframes and cuts based on the prior V3 reconstructed footage.
- One inserted *illustrated crop of exact source-receipt JSON values*, labeled `ACTUAL LOCAL RECEIPT`. The graphic is **not a screenshot of the actual original experiment** and must not be treated as actual provider footage.
- Original procedural ambient bed with small sound transitions (no stock licensing); a temporary eSpeak voice track, *not* a professional natural narrator.
- Seven ASS caption segments timed to each **actual generated WAV phrase** rather than arbitrary visual scene length.
- Fail-closed SHA check on source input, authoring receipt, seven contiguous 30fps cuts and no publication authority.

Technical result for **private sample** `webhook-editorial-pilot-PRIVATE.mp4`:
- Output SHA-256 `0e6eb91de3300ea8fe0c7b66edb590f8338096a4a43b21be53c09c6bc62fc599`.
- FFprobe duration **24.000s**, H.264 **1080 × 1920, 30fps, 720 video frames** + **AAC 48kHz stereo** audio.
- Output size **3,965,446 bytes**, no remote APIs/costs used.
- Companion generated artifacts: `editorial_contact.jpg`, `editorial-proof-receipt.json`, `build_editor_pilot.py`, locally rendered subtitle `captions.ass`. The source bundle and MP4 were shared as ChatGPT conversation sandbox artifacts, **not committed to GitHub**.

**IMPORTANT:** The complete sample clip's image montage was inspected and **still reads visually like a technical presentation**, despite added edits. The synthetic eSpeak narrator is noticeably robotic. Therefore it is technically valid but **NOT an achieved professional-editor finish**. Do not mark the product-quality gate as PASS or reuse this as a certified brand template.

## Root causes that still block paid-editor-level visual quality

1. **Media supply:** Camera pans on static V3 reconstructed slides cannot replace actual screen recordings of a test, cutaways to real artifacts, meaningful B-roll and narrative visual variety.
2. **Voice:** Local eSpeak allows demonstration of sync but not natural, broadcast-grade English performance. Need validated, appropriately licensed local Kokoro/Chatterbox recording or a human narrator.
3. **Montage:** Even with seven shots, the footage continues to use the same dark data-visualization surface. Editors need alternate footage, scale and editorial pacing; not just crossfades or zooming the existing composition.
4. **Brand/platform:** No owner-approved canonical logo is included. Caption visibility and mobile platform safe-area overlays remain subject to actual phone QA, and no real-audience claims have been gathered.
5. **Source integrity:** The local JSON-derived graphic is an interpretive reconstruction and must be clearly distinguished from true recorded footage. The experiment's sequential-only scope must remain audible and visible.

## Decision and next evidence-led gate

- **Capability GO:** the no-paid-API offline assembly stack can produce a validated **MP4 with synchronized synthetic voice, captions and procedural sound**.
- **Editorial-quality FAIL (explicit owner rejection):** the generated sample is low-quality, visually a PowerPoint-to-video with purposeless vibration and poorly sounding robotic speech; it fails the professional human-editor standard. Do **not** merge into main, bulk-convert other NINFA videos or auto-publish.
- Obtain a genuine redacted screen capture of a representative local test (or reproducibly record a fresh local test clearly labeled as a new experiment), plus actual output logs. The current source alone does not give us true captured action B-roll.
- Use a licensed, consent-cleared **natural** voice or approved human recording. Align captions to the new **final** audio, not to temporary eSpeak timings.
- Re-edit this **single** Webhook vertical slice with at least two types of genuine evidence footage and one evidence-grounded animation, then judge it at normal speed on a physical phone.
- Clear rights, branding, license, caption-safe margins and human editorial approval separately. Retain `publish_authority=NONE` until explicit owner release authority.

**Do not conflate this technical feasibility proof with a finished professional-channel video.**

## Owner acceptance verdict — explicitly rejected

The owner reviewed the `webhook-editorial-pilot-PRIVATE.mp4` output and stated:

> "en verdad es una muy mala calidad, sigue siendo la ppt de pptx con vibración sin sentido y un sonido demasiado robótico de malísima calidad."

This supersedes the earlier tentative editorial HOLD: **the actual pilot is REJECTED / FAIL**, not a borderline pass or a template to polish.

### Engineering postmortem

1. **Incorrect source-media strategy:** Almost all visual content was reused from the previously rejected static Remotion V3 layout. Camera shakes/reframes and transitions do not turn that footage into a documentary edit.
2. **Motion without purpose:** Vibrations and generic camera moves were added without a visual cause or data-driven narrative function. No repeated animation pass or more CSS polish should be proposed as the fix.
3. **Placeholder voice mistaken for deliverable:** eSpeak TTS was adequate only for validating assembly/clock timing; it is **unacceptable** as the channel narrator and must not be used in any quality candidate. Do not claim that an encoded WAV equals natural voice.
4. **No authentic shot inventory:** A professionally edited technology explainer needs actual evidence-first screencasts, context-specific inserts and causally motivated cuts. The JSON proof graphic alone cannot replace evidence footage.
5. **Misleading evaluation risk:** Passing codec, frame count, SHA receipt and caption generation is only a technical infrastructure milestone. It has zero standing as audience/editorial approval.

### Corrective decision / stop rule

- **KILL the present editorial assembly recipe** as a candidate creative workflow. Preserve the private sample solely as a negative test and do not publish/distribute it as NINFA marketing.
- **Keep** SHA validation, fail-closed publication authority, and local FFmpeg/Remotion capabilities as optional infrastructure. No claim that Remotion itself is rejected or accepted as production editor.
- **STOP** applying generic camera shake, artificial zooms or extra motion to the same single static scene collection. Do not build a Webhook V4/5 or three-way new template pack on this approach.
- **Next valid experiment only after media/narration prerequisites:**
  (a) reproduce or capture an authentic, redacted local SQLite replay with real terminal/result recordings and versioned receipt, clearly attributed;
  (b) produce a human-reviewed concise English script and **natural** voice performance (approved human recording or appropriately licensed/validated local TTS);
  (c) assemble a short evidence-led cut using genuine screen footage + an explanatory visualization only where necessary;
  (d) review the **rough cut** at normal speed on mobile before layering music, effects or additional production;
  (e) only continue if the owner explicitly judges the edited work to be substantially closer to a professional human-edited technology video.
- No generation, narration or remote service should be purchased to rescue this failed sample by default.

**Final decision:** `ASSEMBLY_TECH_PASS / PROFESSIONAL_VIDEO_POC_FAIL_OWNER / CURRENT_RECIPE_KILL / PRODUCTION_AND_PUBLISH_BLOCKED`.
