# Workflows — Design Philosophy & Conventions

Workflows are the **declarative skill chains** of Super Skill. Each one names, per
lifecycle phase, *which skills run* and *what artifacts they produce*, so an agent
can drive a non-trivial task without prompt-and-pray.

## Design Philosophy

Every workflow follows the same shape:

1. **Phased.** Numbered stages (`0..N`) in lifecycle order, not load order.
2. **Skills + Outputs per phase.** Each phase lists its `Skills:` and the
   `Outputs:` it must produce. The Outputs are the **shared-artifact seam** the
   next phase consumes — never re-decide an upstream Output.
3. **Frame → Build → Gate.** Process/posture skills frame the work, domain skills
   build it, gatekeeper skills decide whether to ship. Gatekeepers never run
   first and are never skipped on shippable work.
4. **Looped, with verification.** Long stages run as `ralph-loop` slices: plan one
   minimal step, execute, verify, repeat.
5. **Closed learning loop.** The final stage routes verified lessons into memory,
   docs, tests, or skills (or rejects them as negative memory).
6. **Explicit Done.** Each workflow ends in a `Completion Gate` / `Done Means`
   block stating when the work is actually finished.

This is the discipline that `skill-composition` encodes; every workflow references
it as the cross-cutting orchestration skill.

## Conventions (enforced by `bin/super-skill validate`)

`validate` runs a deterministic **workflow integrity check** (see
`validate_workflows` in `scripts/super_skill.py`):

- Every skill referenced as a `` - `name` `` list item must be a real installable
  skill (or an allowlisted non-skill such as a sibling workflow or the memory
  plugin). A typo'd or removed skill fails the build.
- Every workflow must carry artifact/gate discipline: an `Outputs:` block or a
  `Completion Gate` / `Done` / `Audit` heading.

CI runs `validate --json`, so workflow drift is caught automatically.

## The Workflows

| Workflow | Use when |
| --- | --- |
| [research-to-delivery](research-to-delivery.md) | A project starts from an idea, requirement, product bet, or redesign — full `0..9` lifecycle. |
| [agentic-context-to-delivery](agentic-context-to-delivery.md) | Agent/LLM-driven work where quality depends on input clarity **and** output verification. |
| [goal-driven-agentic-delivery](goal-driven-agentic-delivery.md) | A task too large for one prompt but that should not become an unmanaged autonomous run. |
| [harness-engineering-operating-loop](harness-engineering-operating-loop.md) | Moving a team from AI-assisted to AI-first delivery (system/harness building). |
| [hermes-engineering-learning-loop](hermes-engineering-learning-loop.md) | After complex work or repeated failures, when future agents should get better. |
| [adaptive-agent-memory-harness-loop](adaptive-agent-memory-harness-loop.md) | Multi-tool, multi-LLM projects needing durable learning without token bloat. |

## Adding or editing a workflow

1. Keep the `Skills:` / `Outputs:` shape; list real skill names in backticked
   list items.
2. Give it a `Completion Gate` (or `Done Means`) section.
3. Reference `skill-composition` for the chaining discipline.
4. Run `bin/super-skill validate` and `bin/super-skill catalog` before claiming
   it healthy.
