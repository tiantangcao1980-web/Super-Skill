# Spec: Atom-driven autopilot runner

- Status: **building**
- Owner: super-skill maintainers
- Last-updated: 2026-05-19
- Tracked-by: `manifests/atoms.json`, `skills/00-orchestration/atom-catalog/SKILL.md`, `bin/super-skill atoms`

## Problem

`autopilot` today uses a **frozen** `AUTOPILOT_PHASES` list of 12 tuples in `scripts/super_skill.py`. Third parties can't author their own pipeline (e.g. a `code-migration` track that skips business-case) without forking the file. open-design's atom catalog + `od.pipeline.stages[*].atoms[]` model proves a cleaner alternative: declare the pipeline once in data, execute it from a thin runner.

## Goal

Rewrite the autopilot runner so:
1. Each phase is resolved from `manifests/atoms.json` by atom id.
2. Pipelines are declared as data (default = the existing 12-phase autopilot pipeline) in `manifests/pipelines/autopilot.json` and `manifests/pipelines/auto-flow.json`.
3. Plugin/skill authors can publish their own pipeline JSON next to their SKILL.md and Super Skill executes it under the same harness.
4. `until:` expressions evaluate against the locked v1 signal vocabulary; unknown signals are runtime errors.

## Non-goals

- Changing the `bin/super-skill autopilot` CLI surface or argument names. Users must not have to relearn.
- Changing the `run.json` / `timeline.html` output shape (only adding fields).
- Switching skills from Markdown SKILL.md to something else.

## Plan

### Phase 1 — declarative form (shipped)
- [x] Land `manifests/atoms.json` with 21 atoms (15 implemented, 6 reserved).
- [x] Land `bin/super-skill atoms --validate` that catches `unknown-atom` + `unknown-until-signal`.
- [x] Land `skills/00-orchestration/atom-catalog/SKILL.md` that documents composition.

### Phase 1.5 — declarative pipeline JSONs (this PR)
- [x] Land `manifests/pipelines/autopilot.json` — every stage from `AUTOPILOT_PHASES` written as data, referencing canonical atom ids.
- [x] Land `manifests/pipelines/ultra-lite.json` — minimal 5-stage code-work pipeline that proves the format works for non-autopilot scopes.
- [x] Land `bin/super-skill atoms --validate manifests/pipelines/*.json` wired into CI.
- [x] Land integrity test: pipeline JSON `stage.id` / `output` / `label` arrays must match the in-code `AUTOPILOT_PHASES` tuple list 1:1 so they cannot drift.

### Phase 2 — runner refactor (next PR)
- [ ] Extract every atom's prompt fragment from `llm_call_stub()` and the `AUTOPILOT_PHASES` tuple into a per-atom dict (`{atom_id: {system_prefix, output_filename, run_fn, ...}}`).
- [ ] Build `autopilot_run_pipeline(pipeline_json, workspace, provider, model)` that loops over `pipeline.stages`, expanding atoms in order, honoring `repeat: true` + `until:`.
- [ ] Keep the existing `cmd_autopilot` as a thin wrapper that loads the default pipeline JSON and calls the new runner.

### Phase 3 — plugin authoring (later)
- [ ] Add `bin/super-skill autopilot --pipeline path/to/pipeline.json`.
- [ ] Discovery: when a skill folder ships `pipeline.json`, surface it via `bin/super-skill list --pipelines`.

## `until:` evaluator semantics (v1)

```
until_expr := expression ( ("||" | "&&") expression )*
expression := signal_name comparison number | signal_name
comparison := ">=" | ">" | "<=" | "<" | "==" | "!="
```

Allowed `signal_name` (locked in `manifests/atoms.json` `until_signals.vocabulary`):
- `critique.score`
- `iterations`
- `user.confirmed`
- `preview.ok`
- `tests.pass`
- `verdict.pass`

Evaluator MUST refuse expressions that use any other identifier. No string interpolation, no arbitrary function calls.

## Risks

- **Loss of audit clarity**: removing the explicit 12-tuple list makes it harder to skim what autopilot does. Mitigation: keep `manifests/pipelines/autopilot.json` checked in with one line of human-readable description per stage.
- **Backward compatibility for resume()**: existing `run.json` files reference phase ids like `00-research`. Solution: pipeline JSON declares `phase_id_for_resume` so an old run resumed under the new runner still maps.
- **Plugin authors can write malicious `until:`**: hence the locked vocabulary + no eval/exec.

## Acceptance

- `bin/super-skill autopilot --provider stub --prompt 'demo'` produces a byte-identical `run.json` (modulo runtime timestamps) under the new runner.
- `bin/super-skill atoms --validate manifests/pipelines/autopilot.json` returns ok.
- `bin/super-skill atoms --validate evals/fixtures/bad-pipeline.json` reports `unknown-atom` + `unknown-until-signal`.
- All existing tests pass.
