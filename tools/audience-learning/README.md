# NINFA Audience Learning v1 — offline gate

This is an **observation and editorial-preflight tool**, not a YouTube optimizer or publishing service.

Run from repository root with Node.js 20+ (no dependencies):
```bash
node --test tools/audience-learning/learning.test.mjs
node tools/audience-learning/learning.mjs
```

Optional positional arguments: path to manual Studio metrics JSON, path to 6-candidate JSON.

## Rules
- Source: user-transcribed YouTube Studio values, identified as `MANUAL_YOUTUBE_STUDIO`, not live API data. Preserve date and measurement window.
- `views`, `engaged_views`, `stayed_to_watch_pct`, `shown_in_feed` are **not interchangeable**. The measured percentage staying is not `engaged_views/views`.
- Null means unknown. Never impute `shown_in_feed` from views or traffic share.
- Video `average_view_duration_sec / duration_sec` is approximate due to rounded seconds and conditional viewer population, not initial-hold rate.
- Threshold `<25% stayed` is an **experimental flag**, not a YouTube benchmark, predictive promise or causal conclusion.
- A `NOT_RUN` experiment must not make result claims. Evidence sources and final claim QA are human responsibility.
- All candidates stay `BLOCKED_PENDING_EVIDENCE_AND_HUMAN_QA`. The tool cannot export, upload, schedule, or publish.
- Cross-experiment novelty is enforced using stable `incident_key` and `angle_key`. Existing incident history is manually curated and **not guaranteed complete**; human review remains mandatory.
- Compare at matched **first 48 hours** and **day 7** after future publication; do not infer equivalent impressions or exposure from lifetime totals.
- Final release remains controlled by `docs/contracts/DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md` and additional human/phone QA.

The six entries are **experiment briefs**, not six measured Shorts, produced MP4s or publishable scripts.
