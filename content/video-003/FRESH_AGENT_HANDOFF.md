# Fresh Agent Run Handoff

The official NINFA-100 run must not occur inside the benchmark-authoring chat.

## Why

The authoring context knows the task set and evaluator design. Counting results from that same context would contaminate the experiment.

## Preferred path: isolated API runner

Use `runner/run_ninfa100.py`.

It creates a new Responses API context for every task and gives the tested model only:
- that one frozen task,
- a fresh copy of the fixtures,
- web search,
- restricted local file/code tools.

It does not provide:
- future tasks,
- benchmark authoring discussion,
- freeze hashes,
- evaluator notes,
- previous task conversations.

## Requirements
- Python
- `pip install openai`
- `OPENAI_API_KEY` set by the operator

No API key is stored in the benchmark package.

## Integrity check without spending money

`python runner/run_ninfa100.py --verify-only`

## One-task smoke test

`python runner/run_ninfa100.py --model gpt-5.6-terra --task R-01`

## Full raw run

`python runner/run_ninfa100.py --model gpt-5.6-terra`

The runner creates raw evidence only. Scoring is a separate step under the frozen rubric.

## Cost control

Do not start the full 100-task API run until the operator explicitly approves the API spend/model choice.
