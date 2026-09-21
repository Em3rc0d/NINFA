# Video 003 — Experiment Plan

## Working title

**I Gave an AI Agent 100 Real Tasks — Here’s Where It Failed**

Status: **TOPIC LOCKED / EXPERIMENT NOT YET RUN**

## Objective

Move Does It Automate? beyond testing its own production system and perform a real external stress test of an AI agent on useful work.

The experiment must answer:
- what percentage of tasks are completed,
- what partially succeeds,
- what fails,
- which categories are strongest/weakest,
- which failures require human rescue,
- what tool/hallucination errors occur,
- how much time/cost the run consumes.

## Pre-registration rule

Freeze the task set, scoring rules and evidence requirements **before** running the agent.

Do not adapt scoring after seeing results merely to improve the story.

## Target task count

**100 tasks**

Suggested category families:
- coding,
- research,
- browser navigation,
- file handling,
- summarization,
- planning,
- data extraction,
- business workflows,
- multi-step tool use.

Exact category counts should be frozen before execution.

## Scoring

Every task receives one of:

### PASS
The requested outcome is completed correctly without material human repair.

### PARTIAL
The agent makes useful progress but misses a material requirement, needs correction, or cannot complete the full task autonomously.

### FAIL
The outcome is materially incorrect, unusable, unsafe for the requested purpose, or requires the human to effectively redo the task.

## Additional flags

Track independently:
- hallucination,
- tool misuse,
- navigation failure,
- instruction-following failure,
- missing evidence,
- human rescue required,
- timeout,
- cost anomaly.

## Evidence contract

For every task retain enough evidence to audit the grade:
- prompt/task definition,
- output/result,
- relevant tool logs/screens,
- elapsed time,
- cost where measurable,
- grader note.

## Packaging constraint

Do **not** claim:
- a specific pass/fail percentage,
- “it failed task 17,”
- “AI is not ready,”
- or another result-based hook

until the experiment actually produces that evidence.

The first-five-second hook can be finalized only after the strongest real result/failure is known.

## Brand contract

Use the exact approved Does It Automate? blue monogram / upward-execution-arrow asset.

Do not use the deprecated circuit-D logo.

## Distribution derivatives

After the long-form experiment:
- Short: strongest unexpected failure,
- Short: final 100-task score,
- Short: strongest/weakest category contrast,
- carousel/community post: PASS / PARTIAL / FAIL summary,
- poll: next category/tool to stress-test.
