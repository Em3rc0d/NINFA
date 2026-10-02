# Video 003 — Production Package v1

Status: **READY FOR VOICEOVER PRODUCTION**

Working title:

**600 Real Business Tasks Exposed AI Agents — Here’s Where They Break**

## Editorial integrity

This episode analyzes public benchmark evidence.

Do not imply that Does It Automate ran the 600-task benchmark.

The concrete failure replays in this script come from a published Qwen3.6-27B base AutomationBench run unless explicitly stated otherwise.

## Narration script

### VO-01 — Hook

AI agents look incredible in demos.

Give them a clean environment, a simple task, and the right tools, and they can feel almost magical.

But real work is messy.

Real work has exclusions, changing policies, multiple apps, incomplete states, and tasks where doing the wrong thing is worse than doing nothing.

So I went through public AutomationBench evidence to answer a more useful question:

What actually breaks when AI agents are asked to do real business work?

### VO-02 — What the benchmark tests

AutomationBench contains six hundred scored business workflow tasks across sales, marketing, operations, support, finance, and human resources.

The benchmark uses simulated SaaS tools and checks the final state of the environment.

That distinction matters.

An agent does not get credit just because its explanation sounds correct.

The underlying system has to end up in the right state.

And that is where some of the most interesting failures appear.

### VO-03 — Failure type one: doing too much

One public task asks an agent to add the right Director-level contacts to a Salesforce campaign while excluding people from restricted industries, opt-outs, holds, and several title exceptions.

In the published run I analyzed, the agent found all six contacts that should have been enrolled.

That sounds good.

Except every scored "must not be enrolled" check failed.

It knew who to add.

The problem was that it also added people it had been explicitly told to leave alone.

This is a very different failure from "the AI cannot use Salesforce."

The agent could act.

It just could not reliably restrain itself.

### VO-04 — Failure type two: reporting success without changing the system

Another task involves cleaning up hard-bounce email subscribers.

The agent had to archive exactly two addresses, notify operations, mention both addresses, and report the correct archived count.

The published run sent the notification.

It mentioned both addresses.

But the two subscribers it claimed to process were still not archived.

This one is worse than a crash.

The agent produced the communication layer of success while the actual system-of-record state remained wrong.

If a human only reads the message, the workflow looks finished.

If you inspect the system, it is not.

### VO-05 — Failure type three: activity without progress

Then there is a news-digest task.

The agent needed to deduplicate articles, update a log, build the digest, send it, create the required Slack summary, and respect exclusion rules.

The published trace recorded seventy-five tool calls, forty-two steps, and more than two million input tokens.

It passed one active assertion.

One.

It sent an email to the right address.

This is the trap with agentic systems:

A lot of activity can look like progress.

Tool calls are not outcomes.

Steps are not outcomes.

Tokens are definitely not outcomes.

Verified state change is the outcome.

### VO-06 — Failure type four: the workflow breaks between apps

A separate sales task spans multiple platforms.

The published run successfully updated a Salesforce opportunity and created a Google Calendar prep event.

But the larger chain broke across Calendly, Zoom, DocuSign, and the required proposal artifact.

That pattern matters because real automation is rarely one perfect action inside one perfect app.

It is a chain.

And reliability compounds across the chain.

If every individual step is only "usually right," a long workflow can still be fragile.

### VO-07 — The zero-score example

One of the clearest examples is an app-review triage task.

The published run hit fifty steps and made forty-nine tool calls.

It satisfied zero out of twelve scored assertions.

Fifty steps.

Forty-nine tool calls.

Zero out of twelve.

That is why I think the useful question is not:

"Can an AI agent use tools?"

Clearly, yes.

The useful question is:

"Can it complete the entire workflow, preserve constraints, and leave the business system in the correct final state?"

### VO-08 — What this means for automation

None of this means AI agents are useless.

It means the deployment model matters.

For low-risk work, drafts, research, triage, and reversible actions, an imperfect agent can still create a lot of value.

For workflows involving money, compliance, customer records, destructive actions, or multiple systems, the standard has to be higher.

You need validation.

You need checkpoints.

You need idempotency where possible.

You need explicit negative constraints.

And sometimes you need a deterministic workflow around the agent instead of giving the agent complete freedom.

### VO-09 — Closing

The interesting part of AI automation is no longer whether a model can click buttons or call APIs.

We already know it can.

The real engineering problem is reliability.

Can the system know when not to act?

Can it prove that the underlying state actually changed?

Can it recover when one tool in a long chain fails?

And can we verify the result without trusting the agent's own narration of what happened?

That is the difference between an impressive demo and an automation you can actually depend on.

This is Does It Automate.

And that is exactly what we are going to keep testing.

## Chatterbox WAV plan

Generate one WAV per section so failed generations are cheap to redo:

```text
vo_01_hook.wav
vo_02_benchmark.wav
vo_03_overaction.wav
vo_04_false_completion.wav
vo_05_thrashing.wav
vo_06_cross_app.wav
vo_07_zero_score.wav
vo_08_implications.wav
vo_09_close.wav
```

Recommended current production settings for English narration from the validated Spanish reference:

- narration text language: English
- CFG weight: 0.0
- exaggeration: 0.5 starting point
- temperature: 0.8 starting point
- device: CUDA when available
- reference: clean approved voice sample

Do not generate the entire episode as one Chatterbox request.

## Scene plan

### Scene 01 — Demo illusion
Visual:
- polished agent demo UI,
- quick success states,
- then hard cut to error-state montage.

On-screen:
**DEMOS ARE CLEAN. REAL WORK ISN'T.**

### Scene 02 — Benchmark frame
Visual:
- AutomationBench repository / public benchmark evidence,
- simple six-domain grid,
- 600 tasks,
- simulated SaaS tools,
- final-state checks.

On-screen:
**600 BUSINESS TASKS**
**FINAL STATE > CONFIDENT TEXT**

### Scene 03 — Negative selection
Visual:
- contact table,
- six green intended contacts,
- excluded contacts turning red after being incorrectly selected.

On-screen:
**IT KNEW WHO TO ADD.**
**IT DIDN'T KNOW WHO TO LEAVE ALONE.**

### Scene 04 — False completion
Visual:
- email/report says cleanup completed,
- cut to database/subscriber state showing records unchanged.

On-screen:
**REPORT: DONE**
**SYSTEM: NOT DONE**

### Scene 05 — Tool thrashing
Visual:
- rapidly increasing counters:
  - 75 tool calls
  - 42 steps
  - 2M+ input tokens
- result collapses to:
  - 1 assertion passed

On-screen:
**ACTIVITY ≠ PROGRESS**

### Scene 06 — Cross-app fragmentation
Visual:
- Salesforce → Calendar → Calendly → Zoom → DocuSign → artifact
- first two nodes green,
- downstream chain breaks red.

On-screen:
**THE CHAIN IS THE PRODUCT**

### Scene 07 — Zero score
Visual:
- giant counters:
  - 50 STEPS
  - 49 TOOL CALLS
  - 0 / 12

Hold long enough to register.

### Scene 08 — Engineering response
Visual:
agent surrounded by deterministic guardrails:
- validation
- checkpoints
- idempotency
- negative constraints
- human approval

On-screen:
**DON'T JUST ADD AN AGENT.**
**ENGINEER THE SYSTEM AROUND IT.**

### Scene 09 — Close
Visual:
Does It Automate brand close.

On-screen:
**CAN IT ACT?**
then
**CAN YOU TRUST THE RESULT?**

## Evidence discipline

Use real public evidence where possible.

Any reconstructed UI must be labeled as reconstruction.

Numeric statements in graphics must remain attributable to the source ledger.

## Editing target

Target runtime after human pacing: approximately 5–7 minutes.

Do not stretch runtime to fit a target.

Retention priority:
- fast hook,
- one concrete failure every 30–60 seconds,
- visual reset between failure classes,
- no long benchmark-methodology lecture,
- engineering takeaway before close.
