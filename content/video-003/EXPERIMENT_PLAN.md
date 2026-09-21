# Video 003 — Public-Evidence Analysis Plan

## Working title

**600 Real Business Tasks Exposed AI Agents — Here’s Where They Break**

Status: **PIVOTED — PUBLIC-EVIDENCE MODE / NO PAID API RUN REQUIRED**

## Why this replaces the original plan

The original idea was to run a fresh 100-task benchmark ourselves.

That would create avoidable API spend while duplicating work that already exists publicly.

Video 003 will instead analyze published, reproducible agent benchmarks and public task/result evidence.

Critical integrity rule:

> Do not imply that Does It Automate? executed benchmark runs that were performed by third parties.

We may reconstruct, visualize, compare and explain public results, but attribution must remain explicit.

## Primary evidence source — Zapier AutomationBench

AutomationBench evaluates realistic business workflows across 47 simulated SaaS tools.

Public benchmark:
- 600 scored tasks,
- 100 Sales,
- 100 Marketing,
- 100 Operations,
- 100 Support,
- 100 Finance,
- 100 HR.

The benchmark checks final simulated application state using deterministic assertions rather than subjective LLM-as-judge scoring.

Public results observed on 2026-09-21:
- Claude Opus 5 — 50.3%
- Kimi K3 — 46.67%
- Claude Fable 5 — 46.17%
- GPT-5.6 Sol — 45.83%
- Gemini 3.6 Flash — 45.00%
- GPT-5.6 Terra — 37.17%
- Claude Sonnet 5 — 34.67%
- GLM 5.2 — 26.17%

Source:
https://github.com/zapier/AutomationBench

## Harder official leaderboard context

Zapier also publishes a separate official leaderboard using a held-out private task set.

Important:
- public and private scores are NOT the same test,
- private tasks are intentionally harder,
- do not directly present the two score tables as equivalent runs.

Current official leaderboard snapshot observed on 2026-09-21 includes:
- GPT 6 Astra (Max) — 41.4%
- GPT-5.6 Sol (Max) — 28.77%

Source:
https://zapier.com/benchmarks

These private scores are useful as additional evidence that performance drops materially on harder held-out work, but must be labeled as a different benchmark split/version.

## Supporting evidence sources

Potential supporting segments:
- SWE-bench public task/results/log artifacts for software-engineering failures.
- OSWorld / OSWorld 2.x for computer-use and long-horizon desktop tasks.
- GAIA for browsing/tool-use/reasoning tasks.

These should support the story, not turn the video into a benchmark encyclopedia.

## Aggressive cold open

Preferred opening, subject to final fact-check immediately before render:

> “The best public run I found on 600 realistic business tasks barely cleared half. GPT-5.6 Sol passed 45.83%. And on Zapier’s harder held-out benchmark, Sol drops below thirty percent.”

Then immediately:
- show the actual leaderboard,
- show the six work domains,
- show one representative task structure,
- explain that these are third-party benchmark results, not our own run.

No logo intro before the evidence.

## Story arc

1. **Cold open:** brutally low completion rates.
2. **What counts as ‘real work’?** Explain simulated CRM/inbox/calendar/tool state.
3. **Why this benchmark matters:** final-state assertions, not vibes.
4. **600-task public scoreboard:** models side by side.
5. **What 45.83% actually means:** strict all-assertions pass/fail.
6. **Where agents break:** inspect representative task structures and failure classes available in public evidence.
7. **Harder held-out reality:** clearly separated official private leaderboard.
8. **Supporting benchmarks:** one or two short examples from coding/computer-use research.
9. **Interpretation:** capable, useful, but reliability remains workload-dependent.
10. **What I would automate today vs keep human-supervised.**
11. **Next experiment tease.**

## Visual doctrine

Use real source material:
- benchmark repository,
- leaderboard screenshots,
- task definitions,
- assertion/scoring diagrams,
- public logs/trajectories where licensed/available,
- simple charts rebuilt from cited public numbers.

Do not fake an agent UI or fabricate an execution trace and present it as real.

Re-enactments are permitted only when visibly labeled:
**RECONSTRUCTION FROM PUBLIC BENCHMARK DATA**

## Packaging hypotheses

### Title A
**600 Real Business Tasks Exposed AI Agents — Here’s Where They Break**

### Title B
**I Analyzed 600 Real AI Agent Tasks. The Results Are Brutal**

### Title C
**AI Agents Look Incredible — Until You Test Real Work**

### Thumbnail concepts

1. **600 TASKS / 45.83%**
2. **AI AGENTS vs REAL WORK**
3. **FAILED HERE** + real benchmark task screenshot

Use only the canonical approved blue Does It Automate? mark.

## Cost doctrine

Expected model/API benchmark cost for this episode:
**$0**

Research, analysis, charts, narration and editing can use existing project capabilities and public evidence.

Do not spend API credits merely to reproduce already-published benchmark results unless a later episode specifically requires independent replication.
