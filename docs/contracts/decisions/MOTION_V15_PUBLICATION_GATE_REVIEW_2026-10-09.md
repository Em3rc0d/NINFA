# Motion v1.5 — publication gate review (2026-10-09)

**Channel:** Does It Automate? (English). **Short:** *The Duplicate Webhook*.  
**Decision:** `TECHNICAL_AND_LOCAL_FACTUAL_QA_PASS / PUBLISH_RELEASE_BLOCKED`.  
**Date:** 2026-10-09, America/Lima.  
**Owner direction:** visual direction accepted; untreated original-source narration accepted; neither implies authorization to publish.

## Source-of-truth hierarchy

- [Frozen Does It Automate? identity](../../BRAND_IDENTITY.md), [channel thesis](../../CHANNEL_THESIS.md) and [Motion contract v1](../DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md).
- [Evidence-first v1.5 replay receipt](MOTION_V1_5_DUPLICATE_WEBHOOK_LOCAL_PROOF_2026-10-09.md), and versioned [replay experiment](../../../tools/motion-v15/replay_lab.py) / [fixture](../../../tools/motion-v15/evidence/replay_evidence.json).
- [Natural voice UAT](NATURAL_VOICE_MIX_UAT_2026-10-09.md). **The approved audio variant is the original-source, untreated AAC**, not the earlier mastered voice.
- YouTube Help: [Shorts upload](https://support.google.com/youtube/answer/12779649), [visual guides](https://support.google.com/youtube/answer/16215842).

## Results observed in local QA

| Gate | State | Exact basis |
|---|---|---|
| Experiment truth | **PASS, limited** | Replayed two separate **sequential** SQLite connections with identical synthetic `event_key`. Naive stored 2 actions; `UNIQUE(event_key)` stored 1. Recomputed canonical content digest matches the committed fixture. |
| Regression | **PASS** | 25/25 local tests including source tampering and false claims, performed from the archived isolated production source bundle. |
| Video file | **PASS** | H.264, 1080 × 1920, 30fps, **630 decoded frames**, approximately **21.0 seconds**. |
| Audio | **PASS — exact source payload** | Original owner M4A AAC encoded payload extracted as ADTS from original and approved MP4 is **byte-identical**; decoded PCM samples also match. No added DSP in this approved variant. Private audio/MP4 hashes intentionally not written to public Git. |
| Loudness/clipping proxy | **PASS structural, not aesthetic certification** | Previously observed −20.6 LUFS, −2.4 dBFS true peak in the untreated review MP4. Absence of digital clipping cannot prove no source microphone distortion. |
| Subtitle structure | **PASS** | Eight consecutive, non-overlapping, 1–2-line English phrase-caption intervals, all within video length; wording conveys `UNIQUE index` and concurrency caveat. |
| Subtitle *word-level* alignment | **PENDING** | Manually edited by phrases; no word-level ASR/forced alignment or separately documented owner line-by-line inspection. First- and third-person verb endings should be verified by listening. |
| Visual safe-zone desktop simulation | **RISK IDENTIFIED** | Footer with local sequential disclaimer lies in **possible bottom UI obstruction area**. Caption + spoken closing still convey the caveat. Approximated overlay is **not** an official YouTube UI preview. |
| Actual phone/Shorts editor visual guides | **PENDING** | YouTube's own editor displays visual guides; this has not been checked on the user's device/account. No fixed assistant-derived pixel rules can substitute for that check. |
| Final human editorial/publishing authorization | **PENDING** | The owner previously approved visual direction and natural voice mix only. No title/description, privacy or release permission supplied. |
| Provider-side state | **NONE** | Nothing uploaded, scheduled or published; no external receipt and no Actions media render. |

## Honest editorial framing

Correct claim: **"We delivered one simulated event twice, sequentially, through local SQLite. A unique event-key index prevented a second stored action."**

Do not imply real provider webhooks, live payment/order handling, **concurrency safety**, production throughput, agent benchmarking, exactly-once delivery across external systems or generalized guarantees. State explicitly that a concurrency test remains outstanding.

The proposed public title/description may be drafted, but publication must wait for the owner to verify platform overlays on their mobile device and sign off on the exact draft.

## Platform review workflow (human, no API)

1. Open the private review MP4 in YouTube Shorts' **editor / preview** on the intended phone, without uploading it publicly.
2. Check YouTube's **visual guides** near action icons, descriptions, title and bottom areas. Check especially the lower disclaimer. Decide whether to adjust or remove the footer if obscured. A third-party static overlay preview is not a measurement.
3. Listen at normal phone volume, verify all 8 subtitle lines against the owner's actual pronunciation, and examine first/last second, orientation, loop, text contrast and flicker.
4. Approve or request corrections to the English title, description, source attribution, claims and final exact binary.
5. **Only after** an explicit subsequent command may any publishing/scheduling flow be attempted; provider state must be independently observed.

## Security, storage and release states

- Public Git stores **only documentation, synthetic test data and review gate state**. No raw user voice, voice SHA, encoded audio, edited MP4, private report, phone identifiers or secret/API tokens.
- The reusable review master and proposed copy are delivered in a separate **private user package**, not uploaded to NINFA.
- `READY_FOR_OWNER_PHONE_QA` is the **maximal status justified** for this milestone. It is **not** `READY_TO_PUBLISH`.
- `publication_authority = NONE`; `upload = NOT_PERFORMED`; `schedule = NOT_PERFORMED`.

**Next gate:** owner inspection in actual Shorts UI, word/caption check and explicit publication approval. The prior accepted visual and sound should not be silently remastered.
