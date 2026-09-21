# Video 003 — Source Ledger

Last verified: 2026-09-21

## Primary

### Zapier AutomationBench — public repository
https://github.com/zapier/AutomationBench

Use for:
- benchmark design,
- six domains,
- 600 public scored tasks,
- 47 simulated SaaS tools,
- public pass-rate table,
- deterministic scoring methodology.

Important distinction:
The repository explicitly says the public task set differs from the harder private official leaderboard set.

### Zapier AutomationBench — official leaderboard
https://zapier.com/benchmarks

Use for:
- current held-out/private leaderboard snapshot,
- cost/task where shown,
- current version/ranking context.

Do not merge this score table with the public 600-task score table as though they came from the same test.

## Supporting

### SWE-bench experiments
https://github.com/swe-bench/experiments

Use for:
- public predictions,
- execution logs,
- trajectories,
- per-instance results,
- software-engineering agent evidence.

### OSWorld
https://github.com/xlang-ai/OSWorld-V2

Use for:
- computer-use agent benchmark context,
- long-horizon desktop tasks,
- public trajectories/data where available.

### GAIA
https://huggingface.co/spaces/gaia-benchmark/leaderboard

Use for:
- browsing/tool-use/reasoning benchmark context.

## Citation doctrine

Every numeric result shown in Video 003 must retain:
- benchmark name,
- split/type (public vs held-out/private),
- model name,
- reasoning setting if published,
- retrieval/verification date.

No benchmark number enters narration or thumbnail without a traceable source.
