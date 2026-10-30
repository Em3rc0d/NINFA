# MK1 — Audience-learning slice (2026-10-30)

Status: **IMPLEMENTATION PROPOSED; NO CHANNEL PUBLISH AUTHORITY**

## Data receipt
Transcribed from owner-supplied YouTube Studio screenshots/text on 2026-10-30. Source snapshots have **since-published** windows, not matched 48-hour windows. `shown_in_feed` is absent.

| Short | Lifetime views | Engaged views | Stayed to watch | AVD | Shorts feed share |
|---|---:|---:|---:|---:|---:|
| 29 Tool Calls Across 6 Apps | 99 | 13 | 14.4% | 12s / 13s | 83.7% |
| AI Said "Done." The System Disagreed. (Sep 28) | 45 | 6 | 15.0% | 8s / 12s | 79.1% |
| The AI Made 49 Tool Calls — And Passed Zero Checks | 207 | unknown | 40.1% | 9s / 11s | 79.7% |
| The AI Said "Done"… But Nothing Changed (Oct 28) | 11 | 3 (last-28d report) | unknown | 12s / 25s | unknown |

**Caution:** 11-view video's engaged views were in a **last-28-days** table, not a standalone since-published engaged-view report; treat that value as mixed window unless rechecked. The snapshot JSON therefore leaves its engaged views null. Search terms for Sep 28 Short included unrelated Japanese keyword `撮り鉄`, too little evidence to infer a SEO issue.

## Decisions
1. The 14.4% vs 15.0% stayed rates are almost equal; the 99 vs 45 views do **not** establish that the stronger short had a better opening. Missing *shown in feed* blocks a distribution explanation.
2. Conditional duration (12/13 vs 8/12 seconds) differs, but counts are small and averages rounded.
3. Launch editorial tests of authentic openings, not claims of algorithmic understanding.
4. Prepare six varied **unrun** briefs. No script can claim an observed outcome until execution evidence exists.
5. Track 48h/day-7 metric windows prospectively. 25% stayed-to-watch and 75% conditional duration are internal *hypothesis targets*, not YouTube standards or release gates.
6. Explicit source and human review before rendering or platform upload.

## Execution
```bash
node --test tools/audience-learning/learning.test.mjs
node tools/audience-learning/learning.mjs
```

## Boundaries
No media binaries, voice, private credentials, auto-posting, API spend or GitHub Actions render. Historical incident keys are a preliminary inventory; manual editorial originality screening remains required. The frozen brand and Motion v1 publication gates have precedence.

Next owner inputs after experiments: record raw source hashes, test logs, drafts and future `shown_in_feed`; then perform visual/audio/mobile QA and separate explicit publication approval.
