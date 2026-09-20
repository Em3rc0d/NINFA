# Open-Source References

These projects are reference implementations or potential reusable foundations. NINFA should reuse commodity production infrastructure where it reduces time without surrendering editorial quality or creating fragile dependency risk.

## 1. MoneyPrinterTurbo

Repository: https://github.com/harry0703/MoneyPrinterTurbo

Current role: **primary media-generation foundation candidate**.

Useful areas:
- automated AI video workflow,
- TTS,
- footage acquisition,
- subtitles,
- music,
- FFmpeg/video rendering,
- provider integrations.

Verified on 2026-09-20: public, active, MIT-licensed, ~124.8k stars. Its own description emphasizes HD short-video generation, so NINFA must validate long-form suitability rather than assume it.

## 2. TubeAssistant

Repository: https://github.com/metiutek/tube-assistant

Current role: **orchestration, publishing, scheduling and analytics reference**.

Useful areas:
- autonomous topic/script/media pipeline,
- YouTube upload,
- scheduler,
- analytics-driven iteration,
- hybrid stock/AI media,
- operational recovery patterns.

Verified on 2026-09-20: public, MIT-licensed, small/young project (~19 stars). Treat as reference code first, not a production-critical dependency without audit.

Historical note: the old `metiu1/tube-assistant` URL redirects to `metiutek/tube-assistant`.

## 3. youtube-automation-agent

Repository: https://github.com/strangedeev/youtube-automation-agent

Current role: **long-form architecture reference**.

Useful areas:
- long-form documentary-style pipeline,
- outline/chapter structure,
- footage per chapter,
- human approval gate,
- YouTube feedback loop.

Verified on 2026-09-20: public, MIT-licensed, very early project (0 stars at verification). Treat as architectural inspiration rather than trusted infrastructure.

## Reuse policy

- Reuse commodity plumbing.
- Build NINFA's market intelligence, opportunity scoring, research quality, fact checking, experiment design, learning loop, revenue tracking and editorial logic ourselves.
- Pin exact upstream commit/tag when code is integrated.
- Preserve upstream license/copyright notices.
- Audit security, maintenance health, API assumptions and long-form behavior before production adoption.
- Never let a reused pipeline dictate NINFA's editorial strategy.
