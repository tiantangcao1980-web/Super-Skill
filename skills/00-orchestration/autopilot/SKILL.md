---
name: autopilot
description: Autonomous closed-loop harness that drives one user request through research → intent → spec → design → ralph-loop implementation → simplifier → output quality gate → delivery plan → memory candidate, writing every artifact to a resumable workspace. Use when the user says "autopilot", "全自动跑", "from prompt to delivery", "research to production", "self-driving build", "harness loop", "do the whole thing", "end-to-end build", or invokes `bin/super-skill autopilot`.
---

# Autopilot — Self-Driving Harness Loop

The `autopilot` command is the runnable form of `harness-engineering`. It takes
one prompt and produces a 9-phase audit trail: each phase loads the canonical
SKILL.md as its system prompt, calls the LLM (or the deterministic stub), and
checkpoints a Markdown/JSON artifact next to a structured `run.json` journal.

## When to invoke

- "Run autopilot on X" / "build X end to end" / "drive this from prompt to delivery"
- A long task you want **resumable** across sessions (artifacts live on disk; rerunning skips completed phases)
- Anywhere you would otherwise type `auto-flow` plus 9 manual handoffs

Do **not** invoke autopilot for one-shot edits, single-file refactors, or live
debugging. Use the canonical sub-skill directly.

## Phases (each one a hard checkpoint)

| # | Phase | Canonical skill | Hard gate |
| - | --- | --- | --- |
| 0 | Research | `requirement-analysis` | — |
| 1 | Intent Contract | `intent-contract` | Goal / Acceptance / Evidence all present |
| 2 | Product Spec | `product-spec` | — |
| 3 | Design Direction | `design-templates` | — |
| 4 | Implementation (Ralph) | `ralph-loop` | Inner loop, max `--max-ralph-rounds` (default 20); Phase-4 sandbox actually runs the generated Python via unittest / bare-tests / py-compile |
| 5 | Code Simplifier | `code-simplifier` | — |
| 6 | Output Quality Gate | `output-quality-gate` | JSON `verdict ∈ {pass, warn}` |
| 7 | Delivery Plan | `deployment-patterns` | — |
| 8 | Memory Candidate | `agent-memory-dream-loop` | No raw prompt/response; review-only |

Phases 1 and 6 are **hard exits**: a failure stops the run and surfaces
`failed_phase` in `run.json`. Phase 4 retries internally up to N attempts before
giving up. Phases 0, 2, 3, 5, 7, 8 are soft — they always proceed but their
artifacts are still graded by phase 6 as a whole.

## How to run

```bash
# Stub provider — offline, deterministic, CI-safe.
bin/super-skill autopilot --provider stub --prompt "Build a Python add(a,b) with tests"

# Real LLM provider.
ANTHROPIC_API_KEY=sk-... bin/super-skill autopilot --provider anthropic \
    --prompt "Build a TODO list API with tests" --project ./build

# Resume a run (idempotent — completed phases are skipped unless --force).
bin/super-skill autopilot --run-id 20260505-142110-f2771f --project ./build
```

Workspace layout: `<project>/.super-skill/autopilot/<run-id>/00-research.md …
08-memory-candidate.md` plus `run.json`. The folder is `.gitignore`-d by default
and **never** stores raw prompts or model responses inside the memory candidate
itself (see anti-patterns below).

## Anti-patterns (named so we never reach for them)

**Wrong: "Autopilot will figure it out from a one-line prompt."** Phase 1 will
fail the contract gate. Always front-load the request with concrete acceptance
hints — autopilot is a harness, not a wishing well.

**Wrong: skipping phase 6 for speed.** The quality gate is the only step that
re-reads the original contract against the final deliverable. Skip it and you
ship slop.

**Wrong: re-running with `--force` after a real failure.** Force regenerates
every phase; you lose the failure breadcrumb. Inspect `run.json`, fix the gating
input, then re-run *without* `--force` so completed phases are preserved.

**Wrong: editing artifacts in place between phases.** Treat the workspace as
append-only. If a phase output is wrong, delete that single file and rerun.

**Wrong: skipping phase 0 because "we already know what to build".** Research is
where you catch the assumption that's about to waste the next 6 phases. Skip it
only when you've literally just run another autopilot whose research you're
explicitly carrying over.

**Wrong: shipping without phase 7.** Delivery is the phase that turns "code that
works on my laptop" into "code with a Dockerfile, a CI workflow, a kill switch,
and a rollback plan". Skipping it leaves the project at MVP-prototype quality.

## Trace requirement

Every phase output must include a `Trace:` line (stub provider does this
automatically; real provider must instruct the model to). The trace is what
`agent-memory-dream-loop` and `checkpoint-rollback-safety` use to decide what
to keep, expire, or revert.

## Composes with

- `requirement-analysis` — phase 0 research backbone (with `user-research`/`market-research` framings)
- `intent-contract` — phase 1 hard gate
- `product-spec` — phase 2
- `design-templates` — phase 3
- `ralph-loop` — phase 4 inner loop
- `code-simplifier` — phase 5
- `output-quality-gate` — phase 6 hard gate
- `deployment-patterns` — phase 7 (with `experiment-driven-delivery` + `observability-triage-loop` framings)
- `agent-memory-dream-loop` — phase 8 candidate writer
- `checkpoint-rollback-safety` — every phase artifact is a rollback point
- `harness-engineering` — the design philosophy this skill operationalises
