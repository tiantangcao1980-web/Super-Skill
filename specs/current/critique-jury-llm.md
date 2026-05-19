# Spec: Critique Jury — wire real LLM providers

- Status: **building**
- Owner: super-skill maintainers
- Last-updated: 2026-05-19
- Tracked-by: `scripts/super_skill.py::critique_jury_*`, `AUTOPILOT_PHASES[07-gate]`

## Problem

Phase 6 today produces a Critique Jury panel with 5 panelist scores under stub provider. Real `--provider anthropic` mode has the new prompt template but the recompute-from-panel safeguard is not exercised by CI (no API key in CI). If the real model emits `verdict: pass` while panel scores actually composite to 5.0, only the runtime catches it — and there is no test fixture that proves the catch works.

## Goal

1. Implement an offline LLM-output fixture set that simulates real-provider responses (well-formed, malformed, panel-vs-verdict mismatch, missing panelist, malformed score).
2. Run each fixture through `autopilot_grade_gate()` and assert canonical_verdict / ok behavior.
3. Wire the recompute-from-panel into `cmd_llm_eval` so even the simpler one-shot llm-eval path enjoys the same protection.

## Non-goals

- Adding real network calls in CI (still reserved for the user with `ANTHROPIC_API_KEY`).
- Changing the 0.40 / 0.20 / 0.20 / 0.20 / 0.00 weighting in v1.

## Plan

- [ ] Add `tests/fixtures/critique-jury/*.json` for 5 cases:
    - happy.json — pass, composite = 8.6
    - warn.json — warn, composite = 7.0
    - fail.json — fail, composite = 4.0
    - panel-verdict-mismatch.json — claims `verdict: pass` but composite recomputes to 4.2 → ok must be False
    - malformed.json — invalid JSON / missing panel
- [ ] Test `autopilot_grade_gate()` on each.
- [ ] Same wiring for `llm_grade_gate()`.
- [ ] Document the weights table in `skills/07-testing-and-quality/output-quality-gate/SKILL.md`.

## Acceptance

- `python3 -m unittest discover -s tests` includes critique-jury fixture cases and all pass.
- `bin/super-skill autopilot --provider stub` continues to PASS.
- Manual run with `--provider anthropic` (user-driven) verifies the real model produces a panel that recomputes consistently.
