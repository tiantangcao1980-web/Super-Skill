# Spec: Multi-language ralph-loop verification

- Status: **draft**
- Owner: super-skill maintainers
- Last-updated: 2026-05-19
- Tracked-by: `scripts/super_skill.py::autopilot_ralph_*`, README "Python/JS/Bash/Go"

## Problem

`README.md` claims autopilot ralph-loop runs in **Python/JS/Bash/Go**, but the implementation today only runs Python (`unittest` / bare assertions / `py-compile`). For JS/Bash/Go targets, the impl artifact is written but never executed; the gate cannot detect a regression there.

## Goal

For each non-Python target language, implement a sandbox runner that:
1. Detects required toolchain (node / bash / go) and exits gracefully if missing.
2. Writes the candidate source + a runner script (the equivalent of `run_tests.py`).
3. Executes it under a 60 s wall-clock timeout, captures stdout/stderr.
4. Returns `{ok: bool, stdout, stderr, runtime_ms}` in the same shape as the Python runner.

## Languages

| Lang | Test convention | Runner |
| --- | --- | --- |
| JavaScript | `node --test candidate.test.mjs` (Node 18+) | `node` |
| Bash | `bash run_tests.sh` returning 0 | `bash` |
| Go | `go test ./...` in a temp module | `go` |

## Non-goals

- Multi-language code formatting; ralph only cares about pass/fail.
- Cross-language test harness uniformity; each runner emits its own raw stderr to the next ralph attempt.

## Plan

- [ ] Extract the existing Python runner into `autopilot_ralph_runner_python()`.
- [ ] Add three sibling runners with the same `(candidate_path, attempt_dir) -> dict` signature.
- [ ] Add language detection: prompt keywords → language token (matches existing stub picker).
- [ ] Gate by `bin/super-skill doctor` — runner is invoked only if the toolchain check succeeded.
- [ ] Add `tests/fixtures/ralph/{js,bash,go}/` with a known-good + known-bad sample each.

## Acceptance

- `bin/super-skill doctor --json` reports node/bash/go status (some may be missing on bare CI; that's fine).
- For each available language, `bin/super-skill autopilot --provider stub --prompt 'Build a Node add(a,b)'` runs the JS sandbox and reports `tests.pass`.
- For each language fixture, a deliberately bad candidate causes the next ralph attempt to receive the stderr.
