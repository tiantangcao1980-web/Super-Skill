# Spec: Make design-preflight `--strict` honestly strict

- Status: **draft**
- Owner: super-skill maintainers
- Last-updated: 2026-05-19
- Tracked-by: `scripts/super_skill.py::cmd_design_preflight`, `evals/live-projects/design-frontend-quality-gate/`

## Problem

Today `bin/super-skill design-preflight --strict` returns `visual_refs=skipped:missing` for the live-eval fixture but still reports `OK` overall. CI accepts this. The audit report claimed "门是有效的" but the fixture itself has no visual refs, so the strict mode does not enforce what the field promises.

## Goal

Promote `visual-references` to a required check under `--strict`:
1. `--strict` (no extra flags) requires PRODUCT/DESIGN/shape-brief/tokens to be present **and** at least one visual reference dir to contain ≥ 1 image.
2. `--strict --skip visual-references` retains today's behavior for projects that genuinely don't need pixel fidelity.
3. The live-eval fixture is updated to include a real (tiny SVG) reference image so the strict happy path keeps passing.

## Non-goals

- Pixel-similarity checks against the reference. That's a separate spec (`design-capture`).

## Plan

- [ ] In `cmd_design_preflight`, when `--strict` is set, `visual-references` missing must fail (currently it emits a warning).
- [ ] Add `--skip <check-id>` argument with the existing `DESIGN_PREFLIGHT_CHECK_IDS` whitelist.
- [ ] Add `evals/live-projects/design-frontend-quality-gate/files/design/reference/sample.svg` so the fixture passes strict honestly.
- [ ] Add a negative fixture under `tests/fixtures/design-preflight/strict-missing-refs/` (no `design/reference/`) and assert strict mode fails.

## Acceptance

- `bin/super-skill design-preflight --project evals/live-projects/design-frontend-quality-gate/files --strict` returns ok = True.
- `bin/super-skill design-preflight --project tests/fixtures/design-preflight/strict-missing-refs --strict` returns ok = False with `visual-references: missing`.
- `bin/super-skill design-preflight --project tests/fixtures/design-preflight/strict-missing-refs --strict --skip visual-references` returns ok = True.
