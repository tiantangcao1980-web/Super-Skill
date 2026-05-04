---
name: harness-engineering
description: Use when redesigning a project, team workflow, or engineering system so AI agents can plan, implement, test, deploy, observe, and repair production software reliably.
---

# Harness Engineering

The agent is not the product. The harness is the product: context, tools, tests, workflows, observability, and constraints that make useful agent work repeatable.

## Core Question

When an agent fails, do not ask it to try harder. Ask:

- What capability was missing?
- What context was illegible?
- What validation was too slow, flaky, or manual?
- What tool boundary was absent?
- What rule should become enforceable?

## Harness Capabilities

| Capability | What Good Looks Like |
| --- | --- |
| Legible architecture | agent can inspect the whole relevant system locally |
| Context contract | task includes goal, constraints, working set, acceptance checks |
| Deterministic validation | typecheck, lint, tests, build, e2e, and parity checks are repeatable |
| Review gates | quality, security, and dependency risks are checked independently |
| Progressive delivery | feature flags, rollout metrics, kill switch, rollback |
| Observability | structured logs, metrics, traces, and errors are queryable by agents |
| Triage loop | production issues cluster into actionable tickets with evidence |
| Learning loop | repeated failures become skills, tests, docs, or automation |

## Upgrade Workflow

1. Map the current workflow from idea to production.
2. Identify the slowest human bottleneck after AI shortens build time.
3. Make the system more legible: consolidate context, document boundaries, add local integration paths.
4. Add deterministic validation before increasing agent autonomy.
5. Add observability and triage before increasing deploy frequency.
6. Add feature gates and rollback before daily production experiments.
7. Convert each recurring failure into a new tool, workflow, test, or skill.

## Output

Produce a harness readiness plan:

- missing capability
- current evidence
- target guardrail
- owner skill/tool/workflow
- verification command or signal
