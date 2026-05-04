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
| Context contract | task includes goal, constraints, working set, acceptance checks |
| Spec workflow | product/design/engineering intent becomes executable specs, feature lists, and exit criteria |
| Legible architecture | agent can inspect the whole relevant system locally |
| Working state | long work has resumable task state, handoff summaries, checkpoints, and unblock records |
| Tool and sandbox policy | tools, MCP access, permissions, approvals, and destructive-action gates are explicit |
| Deterministic validation | typecheck, lint, tests, build, e2e, and parity checks are repeatable |
| Agent eval harness | skills and workflows are measured against baselines with traces and deterministic verifiers |
| Review gates | quality, security, and dependency risks are checked independently |
| Progressive delivery | feature flags, rollout metrics, kill switch, rollback |
| Observability | structured logs, metrics, traces, and errors are queryable by agents |
| Triage loop | production issues cluster into actionable tickets with evidence |
| Token and cost control | stable context, volatile evidence, retries, and scans are budgeted deliberately |
| Human risk governance | humans judge architecture, security, product risk, taste, and irreversible changes |
| Learning loop | repeated failures become skills, tests, docs, or automation |

## HarnessCard

For serious projects, summarize the harness as a compact card:

- Control: instructions, specs, guardrails, approvals, and stop conditions.
- Agency: tools, permissions, memory, state, delegation, and recovery paths.
- Runtime: CI, evals, traces, observability, deployment, rollback, and cost limits.
- Evidence: commands, dashboards, traces, tickets, and benchmark results proving the card is true.

## Upgrade Workflow

1. Map the current workflow from idea to production.
2. Identify the slowest human bottleneck after AI shortens build time.
3. Make the system more legible: consolidate context, document boundaries, add local integration paths.
4. Add resumable working state for long-running or human-in-the-loop work.
5. Define tool, sandbox, and approval boundaries before increasing autonomy.
6. Add deterministic validation and agent evals before trusting generated changes.
7. Add observability and triage before increasing deploy frequency.
8. Add feature gates and rollback before daily production experiments.
9. Convert each recurring failure into a new tool, workflow, test, or skill.

## Output

Produce a harness readiness plan:

- missing capability
- current evidence
- target guardrail
- owner skill/tool/workflow
- verification command or signal
- eval or trace evidence required before release
