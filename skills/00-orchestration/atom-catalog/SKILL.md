---
name: atom-catalog
description: |
  Use when assembling a custom Super Skill pipeline (autopilot, auto-flow, fanout track, or a third-party harness) from named atomic capabilities rather than hard-coded phases. Lists the implemented and reserved atom ids, the canonical `until` signal vocabulary, and the rule for declaring `od.pipeline.stages[*].atoms[]`.
triggers:
  - atom catalog
  - pipeline atom
  - pipeline stage
  - until signal
  - reserved atom id
  - 原子能力
  - 编排原子
od:
  mode: utility
  category: orchestration
  inspired_by: nexu-io/open-design § first-party atom catalog
---

# Atom Catalog

Atoms are the **smallest reusable harness primitives** in Super Skill: turn-1 question forms, file write/read, ralph attempts, critique juries, memory candidate emit, etc. A plugin or workflow composes atoms into ordered stages instead of redefining the prompt fragment.

Source of truth: `manifests/atoms.json` (21 atoms — 15 implemented, 6 reserved).
Live discovery: `bin/super-skill atoms --json`.

## Why atoms

1. **Replace hardcoded phases**: `autopilot` today has a frozen 12-step list. With atoms, a third-party harness can author its own pipeline (`research-note → intent-contract-form → ralph-attempt → critique-jury → memory-candidate-emit`) without forking Super Skill.
2. **Forward-compat by reservation**: ids in `planned` status (e.g. `discovery-question-form`, `direction-picker`, `figma-extract`, `live-artifact`) **accept references** today; `bin/super-skill atoms --validate` only emits a doctor warning. When a future PR wires the implementation, plugins that already referenced the id don't need to churn.
3. **Convergence signals are locked**: the `until:` vocabulary is restricted to `critique.score`, `iterations`, `user.confirmed`, `preview.ok`, `tests.pass`, `verdict.pass`. Plugins must not invent new signal names.

## Composing a pipeline

A plugin or workflow declares:

```yaml
od:
  pipeline:
    stages:
      - id: discovery
        atoms: [intent-contract-form, research-note]
      - id: build
        atoms: [ralph-attempt]
        repeat: true
        until: "tests.pass || iterations >= 8"
      - id: ship-gate
        atoms: [code-simplifier, critique-jury]
        repeat: true
        until: "critique.score >= 8 || iterations >= 3"
      - id: learn
        atoms: [memory-candidate-emit]
```

Validation rules:
- Every atom id must appear in `manifests/atoms.json` (`bin/super-skill atoms --validate <plugin.yaml>` enforces this).
- Every signal referenced in `until:` must appear in `until_signals.vocabulary`.
- Reserved atoms emit a warning instead of an error so plugins can prepare for upcoming capabilities.

## Relation to existing skills

- The 12 hardcoded `AUTOPILOT_PHASES` in `scripts/super_skill.py` map 1:1 to implemented atoms (see `manifests/atoms.json` `notes:` fields). When the atom-driven runner lands (see `specs/current/atom-runner.md`), autopilot will be rewritten as a pipeline of atoms — the user-facing CLI surface stays identical.
- `ralph-loop` is the canonical implementation of `ralph-attempt`.
- `output-quality-gate` is the canonical implementation of `critique-jury` (5-panel weighted composite).
- `agent-memory-dream-loop` is the canonical implementation of `memory-candidate-emit`, governed by `manifests/auto-trigger-policy.json` (no raw prompt, no auto-promote).

## What this skill does NOT do

- It does not redefine prompts already covered by the canonical skill. The atom is a **pointer** to a skill, not a copy.
- It does not bypass `manifests/skill-lifecycle-policy.json` — atoms inherit the protected/critical status of the underlying skill.
- It does not allow inventing new `until:` signal names. If a new signal is genuinely needed, propose a PR to `manifests/atoms.json` `until_signals.vocabulary` before referencing it.
