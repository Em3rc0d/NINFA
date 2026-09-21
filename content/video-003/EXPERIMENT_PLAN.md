# Video 003 — Experiment Plan

## Working title

**I Gave an AI Agent 100 Real Tasks — Here’s Where It Failed**

Status: **BENCHMARK FROZEN / OFFICIAL RUN NOT YET STARTED**

## Objective

Move Does It Automate? beyond testing its own production system and perform a real external stress test of one general-purpose AI agent on useful work.

The experiment must answer:
- what completes cleanly,
- what partially succeeds,
- what fails,
- which categories are strongest/weakest,
- which failures require human rescue,
- what tool/hallucination errors occur,
- how much time/cost the run consumes.

## Pre-registration

The NINFA-100 benchmark is now frozen before the official scored run.

Composition:
- 100 tasks,
- 10 categories,
- 10 tasks per category.

Categories:
1. Research & Verification
2. Data Analysis
3. Coding & Debugging
4. File & Document Operations
5. Web Navigation & Extraction
6. Planning & Constraint Satisfaction
7. Tool Use & Multi-Step Work
8. Error Handling & Robustness
9. Business Workflows
10. Long-Horizon Compound Tasks

The frozen task manifest and hashes are in [BENCHMARK_MANIFEST.md](BENCHMARK_MANIFEST.md).

## Scoring

Every task receives exactly one terminal label:

### PASS
Correct, complete, all hard constraints satisfied, no material human rescue.

### PARTIAL
Useful progress, but a material requirement, artifact, citation, constraint or verification step is missing/incorrect.

### FAIL
Core outcome is not achieved, materially wrong, fabricated, unsafe, or requires the human to redo the task.

### BLOCKED
A required capability/input is genuinely unavailable and the agent correctly reports the blocker without fabricating completion.

## Evaluation doctrine

Prefer deterministic execution-based validation:
- unit tests,
- numeric checks,
- schema validation,
- file validation,
- checksums,
- final-state inspection.

Use manual review only where source quality or semantic correctness cannot be captured deterministically.

No “looks good” scoring.

## Fairness rules

- do not change tasks after seeing results,
- do not rewrite scoring after failures,
- do not cherry-pick tasks for the final score,
- do not retry scored terminal failures unless the task explicitly evaluates recovery,
- no irreversible external side effects,
- every reported score must retain auditable evidence.

## Important integrity note

A 10-task harness dry-run was used only to verify that validators and evidence capture work.

Those dry-run results are **excluded** from the official score because the authoring context had seen the benchmark internals.

The official run must use a clean agent context that has never seen the task set or evaluator design.

## Packaging

Do not freeze a result-based title, failure percentage, “task 17” claim or final thumbnail before the official 100-task run completes.

The final cold open will use the strongest TRUE observed result.

## Aggressive story doctrine

No generic intro.

Final opening pattern:
1. strongest real failure/success,
2. task prompt on screen,
3. agent action,
4. real evidence,
5. live scoreboard,
6. “100 tasks” premise.

Persistent score:
PASS / PARTIAL / FAIL / BLOCKED / REMAINING.

## Visual doctrine

Real task > real browser > real terminal > real artifact > real score.

Graphics support the evidence; they do not replace it.

## Brand contract

Use only the approved Does It Automate? blue monogram / upward-execution-arrow identity.

Do not use the deprecated circuit-D logo.

## Distribution derivatives

After the long-form experiment:
- Short: strongest unexpected failure,
- Short: strongest surprising success,
- Short: final score,
- carousel/community post: category scoreboard,
- poll: what should be stress-tested next.
