# S01 V2 — English narration and caption plan (NOT RECORDED)

**Editorial state:** draft for owner/narration review. No voice recording or voice synthesis was used in the current V2 MP4. No automatic publishing.

| Clip time | Provisional English voice line | On-screen proof |
|---|---|---|
| 0.00–2.75 s | "One local time. Two UTC results." | `01:30 AM → 08:30Z / 09:30Z` |
| 2.75–6.50 s | "Los Angeles has two one-thirties when daylight saving ends." | Two 1:30 analog clocks, offsets UTC−7 / UTC−8 |
| 6.50–10.70 s | "Our Python test found eight-thirty and nine-thirty UTC." | Local `zoneinfo` result, `fold 0`, `fold 1` |
| 10.70–14.60 s | "A permissive conversion picked one. Our guard asked first." | `fold=0 → 08:30Z`, strict `AMBIGUOUS → REQUEST CLARIFICATION` |
| 14.60–18.00 s | "Don't guess. Verify before scheduling." | `AMBIGUOUS · ASK FIRST` |

The line durations are **editorial placeholders**, not forced-aligned captions and not evidence of a natural delivery. Record a real approved human take or generate via the locally approved Chatterbox/Kokoro path; inspect pronunciation and pacing, then adjust the visual runtime if the approved take needs it. **Never speed up the owner’s voice to hit 18s.** If phrase durations do not fit, re-time and re-render motion before publishing.

Audio: current MP4 has only original local procedural UI clicks and whooshes. On final mastering, the voice must remain understandable over SFX; adjust effect level, but avoid unapproved loudness-normalization or other DSP on an approved natural owner recording.

## Strict claim boundaries

- `America/Los_Angeles`, 2026-11-01, 01:30 is ambiguous in the tested IANA database.
- 08:30Z and 09:30Z are the two valid timestamps, one hour apart.
- Only Python zoneinfo and a local guard were tested; no calendar API or AI model.
- `fold=0` selection belongs to the demonstrated *permissive Python conversion*, not all calendars.

Human QA: **PENDING**. Physical Shorts UI safe zone: **PENDING**. Release: **BLOCKED**.
