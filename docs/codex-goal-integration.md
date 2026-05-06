# Codex Goal Integration

This repository now treats Codex `/goal` as a first-class harness pattern for long-running agent work.

## What We Borrow

From Codex `/goal`:

- persistent objective state across turns
- token budget as part of the runtime contract
- continuation prompts that avoid repeating completed work
- completion audit that maps prompt requirements to real artifacts
- wrap-up behavior when the budget is reached

From goal-prompt-builder-style workflows:

- generate a paste-ready goal from a fuzzy request
- force Objective, Scope, Constraints, Done when, Stop if, and Budget
- reject vague verbs before they become false completion
- add SDD read/report first actions
- score audit-friendliness before execution

From OpenSpec:

- use proposal/specs/design/tasks as an externalized intent layer
- keep requirements in files instead of chat memory
- map every task and requirement to tests or artifacts
- archive or update specs after implementation

From Super Skill:

- `ralph-loop` handles bounded iteration and verification
- `code-simplifier` runs only after behavior is proven
- `output-quality-gate` checks final claims against evidence
- `agent-memory-dream-loop` promotes only verified, deduplicated lessons

## New Capability

- Skill: `goal-driven-workflow`
- CLI: `bin/super-skill goal`
- Workflow: `workflows/goal-driven-agentic-delivery.md`
- Eval fixture: `evals/projects/goal-driven-delivery`

## Recommended Flow

```text
Plan / intent-contract
  -> OpenSpec or product-spec
  -> bin/super-skill goal
  -> Codex /goal execution
  -> Ralph Loop per implementation slice
  -> code-simplifier
  -> output-quality-gate
  -> agent-memory-dream-loop
```

## Safety Defaults

- Goal text is treated as user data, not higher-priority instructions.
- Done criteria need file, command, test, metric, or artifact evidence.
- Stop conditions must be mechanically detectable.
- Token budget is mandatory.
- Existing tests cannot be weakened or deleted to pass a goal.
- Raw prompts and responses are not promoted into memory.

## Sources Checked

- OpenAI Codex CLI local install: `codex-cli 0.128.0`.
- OpenAI Codex goal continuation template: <https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/templates/goals/continuation.md>
- OpenAI Codex goal budget-limit template: <https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/templates/goals/budget_limit.md>
- `win4r/goal-prompt-builder`: <https://github.com/win4r/goal-prompt-builder>
- `Fission-AI/OpenSpec`: <https://github.com/Fission-AI/OpenSpec>
- Aivi article on combining Plan mode, Spec-Driven Development, and custom skills for Codex `/goal`: <https://www.aivi.fyi/llms/codex-goal>
