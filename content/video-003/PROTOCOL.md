# NINFA-100 Experiment Protocol

## Fairness
1. Freeze all 100 tasks before the first scored run.
2. Freeze exact agent/model/tool configuration before the run.
3. Do not rewrite a task after seeing a failure.
4. Do not cherry-pick tasks for the final score.
5. A task may be retried only when it explicitly evaluates recovery behavior.
6. Side effects are disabled.
7. Prefer deterministic validation.
8. Manual scoring must cite observed evidence.
9. Result-based packaging is finalized only after the run.

## Score labels
PASS / PARTIAL / FAIL / BLOCKED

## Secondary metrics
- duration,
- tool calls,
- recovery attempts,
- human interventions,
- fabricated claims,
- invalid citations,
- unsafe side-effect attempts,
- artifacts created,
- category pass rate.

## Evidence per task
- task definition,
- final response,
- artifacts,
- trace summary,
- score,
- screenshots when relevant.

## Official execution integrity
The official tested agent must run in a clean context that has not seen the benchmark authoring discussion or evaluator internals.
