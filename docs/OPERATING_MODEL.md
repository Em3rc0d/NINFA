# Operating Model

## Persistence

### GitHub — technical source of truth
Store:
- thesis and MK decisions,
- architecture,
- code,
- experiment definitions,
- scene manifests,
- prompts/config,
- content status,
- analytics schemas,
- lightweight publication metadata,
- cost models,
- references.

### Google Drive — operational archive
Store:
- approved brand guides,
- lightweight scripts,
- captions,
- thumbnails,
- publication packages,
- research exports,
- analytics snapshots,
- operational docs.

### YouTube — video delivery
Published long-form video binaries live on YouTube.

### ChatGPT — continuity layer
Useful for active execution, but not the canonical store for detailed project state.

## Heavy-media rule

Do not upload final long-form MP4 renders to GitHub or the NINFA Drive repository by default.

Reason:
- unnecessary storage growth,
- poor versioning economics,
- video already has a delivery surface,
- scripts/manifests/captions are sufficient to reproduce editorial state.

Exceptions require an explicit reason.

## Production loop

Market signals → topic scoring → research → experiment/build → script → fact-check → scene/demo plan → evidence capture → narration → render → packaging → QA → human approval → upload → analytics → learning loop.

## Current production architecture

Script → structured scene manifest → local Kokoro narration → evidence/graphics → FFmpeg renderer → SRT → QA → YouTube.

Real interfaces and evidence take priority over generic generated footage.

## Engineering principle

Reuse audited commodity plumbing where it saves time. Build NINFA's differentiated research quality, experiment design, opportunity scoring, editorial logic, learning loop and revenue tracking ourselves.

## Capital principle

Available budget is not a spending target.

A recurring paid tool earns its seat only when it measurably:
- improves output quality,
- saves meaningful human time,
- or generates more value/revenue than it costs.

## Distribution principle

A long-form episode is the research nucleus, not the only deliverable.

Expected derivative system:
- 2–3 Shorts,
- one carousel/image/community post,
- one poll or teaser,
- internal links/end screen/cards,
- analytics review,
- feedback into the next episode.
