# NINFA-S01 — evidence-led Short production draft

**Status:** Local experiment verified; VIDEO NOT RENDERED; no YouTube publication approval.
**Editorial mode:** EVIDENCE_BACKED_LOCAL_SIMULATION. This is a test of Python's `zoneinfo` behavior, not an AI agent nor a calendar API.

## Claim ledger

- In `America/Los_Angeles`, 2026-11-01 01:30 local has **two valid UTC instants**: 08:30Z and 09:30Z.
- A **specific permissive Python conversion tested here** defaults to `fold=0`; do not generalize this to every calendar service.
- Our local guard classifies the input as `AMBIGUOUS` and requests clarification rather than silently choosing one.
- 2026-03-08 02:30 local is a non-existent wall-clock time under the tested timezone database.
- No real meeting was created, changed, or observed failing. Do not claim a live provider bug.

## English title hypothesis

One Meeting Time. Two Possible UTC Dates? [Correct to **Two UTC Times** before publishing]

Preferred draft title: **One Meeting Time. Two Different UTC Times.**

## English narration — DRAFT, not mastered

One-thirty in Los Angeles happens twice when daylight saving time ends. The same local time can mean eight-thirty or nine-thirty UTC. A permissive conversion picked one silently. Our local guard stopped and asked for clarification. No calendar API was tested.

## Frame story (concept, timings to fit approved voice)

1. Open with two timestamp cards side by side: `01:30 AM` → `08:30Z / 09:30Z`. No brand intro.
2. Show real local-input values and both `fold` candidates from `evidence.json`.
3. Contrast the permissive `fold=0` selection with `REQUEST_CLARIFICATION`.
4. Closing lesson: `Ambiguous local time? Ask before scheduling.` Small disclosure: `Local Python simulation; no calendar provider tested.`

## Production gates

- [x] Reproducible local simulation and seven unittest checks.
- [x] Evidence JSON generated from actual local execution.
- [ ] Physical visual/video composition and timestamp-legibility QA.
- [ ] Narration recorded or locally generated and personally reviewed.
- [ ] Final copy checked against evidence and actual media.
- [ ] Real Shorts device safe-zone review, optional only after render.
- [ ] Separate human release approval.

**No claims of a published video or model benchmark.**
