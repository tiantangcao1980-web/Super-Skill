---
name: agent-eval-harness
description: Use when validating whether an AI agent skill, workflow, prompt, toolset, or autonomous coding loop actually improves results across repeatable tasks.
---

# Agent Eval Harness

Agent capability is not proven by a good demo. It is proven by repeated tasks with traces, deterministic verifiers, baselines, and regression thresholds.

## When To Use

Use this skill when:

- a skill or workflow claims to improve LLM input/output quality
- an agent loop will run autonomously or semi-autonomously
- a tool, MCP server, browser harness, or sandbox policy is being added
- a team wants to compare harness changes rather than only compare models

## Eval Contract

Create a compact eval suite before claiming the harness works:

| Item | Requirement |
| --- | --- |
| Task set | 5-20 realistic tasks from recent work, support tickets, PRs, or product specs |
| Baseline | no-skill baseline, previous workflow, or previous model/harness version |
| Inputs | exact prompt, repo state, fixtures, tool permissions, and environment |
| Trace | JSONL or structured log with decisions, tool calls, errors, retries, and cost |
| Verifier | deterministic verifier first; rubric or trace grading only when deterministic checks are impossible |
| Metrics | pass rate, regression count, unsafe action count, token/cost, latency, and human correction count |
| Threshold | merge, release, or rollback rule tied to the metrics |

## Workflow

1. Pick the harness change to test: skill, prompt layer, tool routing, sandbox, memory, or verification loop.
2. Build task fixtures that represent real user intent, not toy examples.
3. Run the baseline without the new skill or harness change.
4. Run the candidate with the same tasks and comparable tool permissions.
5. Capture a trace for every run, including failure trajectories.
6. Score with deterministic verifiers where possible.
7. Review failed trajectories to identify missing context, missing tools, weak guardrails, or flaky validation.
8. Convert repeated failures into a skill update, test, tool contract, workflow step, or documentation fix.

## Output

Produce an eval report:

- harness change tested
- task set and baseline
- verifier commands or grading rubric
- trace locations
- pass/fail table
- token/cost and latency summary
- top failure modes
- recommended harness changes
- release or rollback decision

## Guardrails

- Do not compare a new skill against an undefined baseline.
- Do not use a model-judged rubric when a deterministic command, assertion, screenshot diff, or API result can prove the outcome.
- Do not hide failures; keep failed traces because they are the raw material for harness evolution.
- Do not generalize from one task. Add tasks until the suite covers research, product, design, development, test, delivery, and operations surfaces relevant to the claim.
