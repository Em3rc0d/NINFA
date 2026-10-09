# UAT receipt — Motion v1.2, voice-integrated Shorts

**Date:** 2026-10-08 (America/Lima)
**Review source:** owner feedback in the PV-POC motion production conversation: "Me gusta tbh pero le falta voice, no?" followed by receipt of three separate owner recordings, three finished Motion v1.2 review MP4s and explicit verdict **"me parece interesante lo que conseguimos, validated."**
**Decision:** `OWNER_ACCEPTED_AS_AUDIOVISUAL_REFERENCE`, not `PUBLISH_APPROVED`, `TEMPLATE_CERTIFIED` or `AUTOMATED_RENDERER_CERTIFIED`.
**Contract:** [Does It Automate? Shorts Motion v1.0.0](../DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md). This acceptance receipt documents implementation evidence; it does **not** change the frozen brand or versioned contract's release requirements.

## Evaluated batch

| Video | Language | Observed delivery | Editorial classification |
|---|---|---|---|
| Does It Automate? — Validation Gate | English | ~17.5 seconds; owner-recorded voice; 1080×1920, 30fps, H.264 + AAC; subtitles | Local scripted demonstration — not claimed as a real production-system run |
| Does It Automate? — Parallel Execution | English | ~23.6 seconds; owner-recorded voice; 1080×1920, 30fps, H.264 + AAC; subtitles | Synthetic/local benchmark example; no universal performance promise |
| EMERCOD — Offline-first | Spanish | ~20.4 seconds; owner-recorded voice; 1080×1920, 30fps, H.264 + AAC; subtitles | Separate channel/brand, local SQLite educational demo; **not subject to Does It Automate?'s English-only rule** |

A previous silent **Motion v1.1** revision reduced slide-like scene cuts by maintaining evolving UI states and purpose-driven micro-motion. **Motion v1.2** added the user's real voice, adjusted scene runtimes to natural speech (without forced time compression), placed subtitles by phrase and rendered audio/video in local tools. The owner's present `validated` message approves the **creative outcome of this reviewed batch**. It must not be converted into a claim that each source assertion was externally corroborated.

## Findings worth preserving

1. **Continuous meaningful visual change** is preferred over discrete PowerPoint-like slide transitions.
2. Each short should retain a persistent subject and let actions or state evolve while the spoken explanation proceeds.
3. Human-recorded voice and narration-led animation are the present **quality reference**, not a requirement that personal narration files be stored with the repository.
4. Do not force target duration to 15 seconds when recordings need longer; fit visuals to voice, never distort voice to match the animation.
5. Does It Automate? remains **English-only**. EMERCOD's Spanish video is a method example, not a transferable language or branding requirement.
6. Topic/visual novelty stays mandatory: different subjects need different visual metaphors, while retaining reusable timing/composition rules.
7. Preserve the **US$0 paid-API** posture, keep **GitHub Actions out of video/TTS production** and hold voice files privately. No social post was scheduled or published through this UAT.

## QA and authority matrix

| Gate | State | Reason |
|---|---|---|
| Creative quality of this specific review batch | **OWNER ACCEPTED** | Explicit `validated` owner feedback after receiving three video outputs |
| Technical MP4/audio checks | **REPORTED PASS FOR BATCH** | 1080×1920, H.264/AAC/frame counts, audio peaks and sampled motion checks in production session; not a new independent target-host audit |
| Human listening and general impression | **OWNER ACCEPTED AT BATCH LEVEL** | Approval does not supply word-level transcript alignment certificate |
| Subtitle timing at word level | **PENDING** | Subtitle placement manually aligned by phrase |
| Official final brand logo use | **NOT VERIFIED FOR THIS BATCH** | Owner-approved canonical logo must be used unchanged when embedded |
| Independent claim / source evidence | **PARTIAL / PENDING** | Illustrative local proofs; distinguish demonstrations and benchmark context from third-party claims |
| Platform safe zones & accessibility on target devices | **PENDING** | Real on-device destination overlay review not recorded |
| Full reusable renderer certification | **NOT CERTIFIED** | Only individual review outputs, not generalized cross-topic regression/test suite |
| Publish/upload/schedule permission | **NONE** | Human quality approval is not provider-side authority |

## Storage and next gate

The actual MP4s, source recordings, subtitles and review ZIP were delivered to the owner in the production conversation. **Do not mirror private voice clips, final MP4s, or temporary conversation sandbox URLs into GitHub**. This receipt stays lightweight; it is not a downloadable media archive.

Before calling the visual system `TEMPLATE_CERTIFIED`, retain three independent **Does It Automate?** topics rather than counting EMERCOD as a third Does It Automate? Short, include at least one fully evidence-backed and independently checked example, review exact spoken/subtitle synchronization, verify platform overlays, and complete mobile QA with a human. No product-side prodAgentic integration is implied.

**Decision summary:** `MOTION_V1_2_BATCH_VALIDATED` · `DIA_CREATIVE_REFERENCE_ACCEPTED` · `RELEASE_BLOCKED` · `NO_CLOUD_SPEND`.
