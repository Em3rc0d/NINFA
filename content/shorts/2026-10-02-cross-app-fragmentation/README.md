# Short — 2026-10-02 — Cross-App Fragmentation

Status: **PRODUCTION READY**
Target publish date: **2026-10-02**
Pillar: **AI Failure Lab**
Source episode: Video 003 / public AutomationBench failure replay

## Winning-formula mapping

**EXPECTATION → ACTION → CONTRADICTION → PROOF → LESSON**

- Expectation: one agent should complete a full multi-app sales workflow.
- Action: the archived run made **29 tool calls** across **11 steps**.
- Contradiction: isolated pieces worked, but the end-to-end workflow fragmented across apps.
- Proof: **2 / 8 assertions passed**.
- Lesson: **A working tool call is not a working workflow.**

## Primary title

**6 Apps. 29 Tool Calls. The Workflow Still Broke.**

Alternative held for later testing:
**The AI Worked — Until the Workflow Crossed Apps**

Do not publish both as separate near-duplicate Shorts.

## Voiceover

> Six apps. Twenty-nine tool calls. The agent still passed only two of eight checks. CRM and Calendar worked. Calendly, Zoom, DocuSign, and the proposal didn't. A working tool call is not a working workflow.

Target runtime: **~11–14 s** depending on narration pacing.

## Visual beat sheet

### 0.00–1.40
Large centered typography:
**6 APPS**

Subline:
one sales workflow

Immediate visual: six connected nodes begin appearing.

### 1.40–3.00
Counter snaps to:
**29 TOOL CALLS**

Small evidence label:
published AutomationBench run

### 3.00–7.80
Horizontal workflow chain with rapid status reveal:

Salesforce ✓ → Calendar ✓ → Calendly ✕ → Zoom ✕ → DocuSign ✕ → Proposal ✕

Use clean technical UI, not generic AI imagery.

### 7.80–9.80
Hard cut / punch-in:

**2 / 8**
**CHECKS PASSED**

The number must dominate the frame.

### 9.80–12.50
Final lesson:

**A TOOL CALL ≠ A WORKFLOW**

Small restrained Does It Automate? canonical mark / wordmark.

## Visual direction

Follow the frozen Does It Automate? brand:
- 9:16 vertical, 1080×1920,
- graphite / near-black background,
- off-white typography,
- approved electric blue/cyan accent,
- red only for failure states if needed,
- high contrast,
- fast cuts,
- no stock robots,
- no purple AI gradients,
- no decorative B-roll,
- evidence and system state are the visual.

Canonical logo rule:
- use only the latest approved brand-guide asset from Drive,
- never use the deprecated circuit-D logo,
- if exact extraction cannot be preserved, omit the mark rather than redraw or approximate it.

## Caption / description

A public AutomationBench run tried to execute a full sales workflow across multiple apps.

29 tool calls later, only 2 of 8 checks passed.

The CRM update and calendar prep worked. The chain broke across Calendly, Zoom, DocuSign and the proposal artifact.

A working tool call is not a working workflow.

#AI #AIAgents #AIAutomation #AIEngineering #Automation #DoesItAutomate

## Source integrity

This Short is a replay analysis of a **published public benchmark run**, not a NINFA-owned execution.

Task: sales.full_sales_cycle_orchestrator

Archived Qwen3.6-27B base run:
- score: **0.25**
- assertions passed: **2 / 8**
- tool calls: **29**
- steps: **11**

Passed:
- Google Calendar prep event,
- Salesforce opportunity stage update.

Failed active assertions:
- Calendly event,
- Calendly invitee,
- Zoom meeting,
- Zoom registrant,
- DocuSign envelope,
- ChatGPT conversation artifact.

Primary evidence is documented in:
- content/video-003/FAILURE_REPLAYS.md
- public run artifact: Hert4/automationbench-opera-gemma4

Do not imply:
- that NINFA ran this task,
- that GPT-5.6 Sol produced this exact trace,
- that all AI agents behave this way.

## Publishing hypothesis

This Short tests whether the strongest observed packaging pattern generalizes to a **new failure class**:

**numeric anomaly + multi-app contradiction + immediately visible final-state proof**

It intentionally avoids recycling:
- over-action / restraint failure,
- false “done” / wrong state,
- recipient/context loss,
- 49-call / zero-check thrashing.

## Analytics to capture

After publication record:
- views,
- shown in feed,
- viewed vs swiped away,
- average view duration,
- average percentage viewed,
- retention curve,
- subscribers gained,
- traffic to linked long-form content.

Compare primarily against:
- **The AI Made 49 Tool Calls — And Passed Zero Checks**
- **THE AI KNEW WHAT TO DO — IT JUST COULDN’T STOP.**
