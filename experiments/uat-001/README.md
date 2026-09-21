# UAT-001 — Open-Source Video Factory

Status: READY TO EXECUTE

## Objective

Produce the same ~75–90 second NINFA test segment we used in Pictory, but through a local/open-source pipeline.

This test exists to answer one question:

> Can NINFA create acceptable YouTube-quality video without depending on a paid video-assembly SaaS?

## Frozen pipeline for this UAT

NINFA script
→ Voicebox local TTS (Kokoro first)
→ real screenshots / browser captures / free stock
→ FFmpeg assembly
→ captions
→ final 16:9 1080p MP4
→ human QA

Pictory is NOT used in this UAT.

## Hardware target

- Intel Core i5-9300H
- 16 GB RAM
- NVIDIA GTX 1650 4 GB
- Windows 64-bit

The UAT must remain usable on this machine.

## Script

Everyone says AI can automate a YouTube channel.
So instead of selling you the idea, I’m building one from zero and measuring what actually happens.

This is Project NINFA: a system designed to research topics, write scripts, capture real software, generate media, assemble videos, publish them, and learn from the results.

But there’s a problem.
Fully generating an eight-minute video with modern video models can become expensive very quickly.

So NINFA takes a different approach.
Most of the video comes from evidence: real interfaces, browser recordings, code, screenshots, results, and diagrams.

Generative video is reserved for scenes where it actually adds something.

For example, if I test an AI agent on one hundred tasks, you shouldn’t be watching a fake robot for ten minutes.
You should see the agent, the failures, the logs, and the numbers.

That changes the economics completely.
Instead of paying to generate every second, we only pay for the parts that genuinely need generation.

And that is the experiment behind this channel:
build AI systems, test them on real work, measure the outcome, and show you what actually works.

## Visual policy

No random robot footage unless the narration explicitly discusses fake/generated robot imagery.

Scene priority:
1. real NINFA/project evidence,
2. real browser/software capture,
3. diagrams/charts,
4. relevant free stock,
5. generated media only when necessary.

## Voice

Primary test:
- Voicebox
- engine: Kokoro
- language: English
- plain TTS; no personality rewrite

Secondary A/B:
- LuxTTS if Kokoro quality is insufficient.

Do not pay for ElevenLabs during UAT-001.

## Output

Required:
- 1920×1080
- 16:9
- H.264 MP4
- AAC audio
- no watermark
- captions
- target duration: 70–90 seconds

## Measurements

Record:
- TTS generation time
- total render time
- human intervention time
- peak RAM
- peak VRAM if available
- final duration
- final file size
- variable monetary cost
- number of irrelevant visual selections
- number of manual visual replacements

## Gate

PASS when:
- understandable/natural narration,
- no material script drift,
- 1080p render completes on target hardware,
- visual relevance is acceptable,
- no obvious AI-slop presentation,
- total variable cash cost <= USD 2 for this UAT,
- human correction time <= 30 minutes.

CONDITIONAL when quality is close but one replaceable component is weak.

REJECT when the local stack cannot produce a credible result without excessive manual work.

## Comparison

After render, compare directly against the Pictory version on:
- voice quality,
- visual relevance,
- pacing,
- presentation quality,
- generation time,
- human effort,
- cost,
- control.

Do not buy Pictory until this comparison is complete.
