# Project NINFA

**Autonomous AI Media Engine**

NINFA is the internal production and learning engine behind the public English-language YouTube brand **Does It Automate?**.

## Current phase

**MK1 — Production validated; distribution and audience-learning phase**

NINFA has crossed the first end-to-end production gate:
- a full local/open-source video factory works,
- local Kokoro narration is viable,
- 1080p long-form assembly works,
- two complete long-form episodes have been produced,
- the next milestone is repeatable audience growth and real experiment-driven content.

## Public brand

- **Channel:** Does It Automate?
- **Handle:** @DoesItAutomate
- **Promise:** We test AI systems on real work.
- **Internal engine:** Project NINFA

Brand identity is frozen in [docs/BRAND_IDENTITY.md](docs/BRAND_IDENTITY.md).

## North star

Build an autonomous, profitable English-language technology media business where YouTube is the primary distribution channel and the content engine is the compounding asset.

## Canonical persistence

- **GitHub:** technical source of truth — decisions, architecture, code, manifests, research summaries, experiment definitions, content state and analytics schemas.
- **Google Drive:** operational archive — brand guides, lightweight publication packages, scripts, thumbnails, captions, research exports and analytics snapshots.
- **YouTube:** published video binaries and audience behavior.
- **ChatGPT context:** continuity layer only.

### Heavy-media rule

Do **not** store final long-form MP4 renders in GitHub or the project Drive repository unless explicitly required. Keep repositories lightweight. Preserve scripts, manifests, captions, thumbnails, brand assets, metadata and reproducibility instructions instead.

See [docs/MEDIA_STORAGE_POLICY.md](docs/MEDIA_STORAGE_POLICY.md).

## Channel thesis

We build, test and explain AI systems that actually do useful work.

Primary content pillars:
- Build & Automate
- Experiments & Stress Tests
- Replace / Compare / Decide
- Business & Economics

Long-form duration is **topic-driven**. There is no fixed 8-minute or 10-minute mandate. The first two production episodes naturally landed around five minutes; future videos should be as long as the evidence and story justify.

Target automation remains **90–95% of production operations**, with a human editor-in-chief as the final quality and factual gate.

See [docs/CHANNEL_THESIS.md](docs/CHANNEL_THESIS.md).

## Production stack proven in MK1

Script → scene manifest → local Kokoro narration → real evidence / browser captures / diagrams / motion graphics → FFmpeg assembly → captions → QA → YouTube.

Paid tooling may enter the stack only when it earns its seat through measurable quality, time or revenue improvement.

## Content state

1. **Video 001 — complete / published**
   - *I Built an AI YouTube Video Factory for $0 — Here’s What Actually Worked*
   - Origin story and proof of the local factory.
2. **Video 002 — complete / uploaded**
   - *I Replaced a Paid AI Video Editor With Free Tools — Here’s What Happened*
   - Pictory vs local NINFA workflow.
3. **Video 003 — next production**
   - *I Gave an AI Agent 100 Real Tasks — Here’s Where It Failed*
   - First external stress-test episode; results must be measured before packaging claims are finalized.

See [content/CONTENT_STATUS.md](content/CONTENT_STATUS.md).

## Distribution loop

Each long-form experiment should become a small distribution system:

Long-form → 2–3 Shorts → one image/carousel/community post → one poll/teaser → end screen/cards → analytics → next-video learning.

See [docs/DISTRIBUTION_STRATEGY.md](docs/DISTRIBUTION_STRATEGY.md).

## Open-source references

NINFA reuses commodity production infrastructure where appropriate instead of rebuilding everything from scratch.

- `harry0703/MoneyPrinterTurbo`
- `metiutek/tube-assistant`
- `strangedeev/youtube-automation-agent`
- Voicebox / Kokoro
- Playwright
- FFmpeg

See [docs/REFERENCES.md](docs/REFERENCES.md).

## Current gate

MK1 now asks:

> Can this system repeatedly produce videos people choose to click, continue watching and want more of?

The next proof is external: impressions, CTR, first-30-second retention, average view duration, traffic sources, returning viewers and conversion into the next video.
