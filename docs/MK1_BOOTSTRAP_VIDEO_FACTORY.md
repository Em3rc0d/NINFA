# MK1 Bootstrap Video Factory

## Decision

NINFA will bootstrap with a local/open-source production path before paying for Pictory or another recurring video assembly SaaS.

Pictory remains an optional accelerator that must earn its seat after the channel has traction or revenue.

## Reuse map

- `youtube-automation-agent`: long-form pipeline and human-review patterns.
- `MoneyPrinterTurbo`: media/TTS/subtitles/rendering components.
- `TubeAssistant`: publishing, scheduling, analytics and orchestration patterns.
- Voicebox: local TTS service.
- Playwright: real software/browser captures.
- FFmpeg: final composition and finishing.

## First implementation slice

Only build what UAT-001 requires:

1. scene manifest ingestion,
2. local Voicebox TTS,
3. media slots,
4. FFmpeg timeline assembly,
5. captions,
6. 1080p export,
7. measurement report.

No YouTube auto-publishing yet.
No full autonomous topic miner yet.
No cloud deployment.
No paid generative-video dependency.

## Upgrade rule

A paid tool can enter the production stack only when it demonstrably:
- improves output quality,
- materially reduces human time,
- or produces more value/revenue than its recurring cost.

## Next gate

UAT-001 local render vs Pictory preview:
PASS / CONDITIONAL / REJECT.
