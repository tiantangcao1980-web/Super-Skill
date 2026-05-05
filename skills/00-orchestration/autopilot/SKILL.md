---
name: autopilot
description: Autonomous closed-loop harness that drives one user request through 12 phases — research → intent → business case → spec → design → ralph-loop implementation → simplifier → quality gate → launch readiness → pilot → commercial delivery → ops & retrospective — covering the full needs-to-commercial-delivery lifecycle in one resumable workspace. Use when the user says "autopilot", "全自动跑", "from prompt to delivery", "research to production", "needs to commercial delivery", "self-driving build", "harness loop", "do the whole thing", "end-to-end project", or invokes `bin/super-skill autopilot`.
---

# Autopilot — Self-Driving Harness Loop

The `autopilot` command is the runnable form of `harness-engineering`. It takes
one prompt and produces a **12-phase** audit trail mapped 1:1 to the standard
10-stage commercial project lifecycle (需求 → 商业交付). Each phase loads the
canonical SKILL.md as its system prompt, calls the LLM (or the deterministic
stub), and checkpoints a Markdown/JSON artifact next to a structured
`run.json` journal.

## When to invoke

- "Run autopilot on X" / "build X end to end" / "drive this from prompt to delivery"
- A long task you want **resumable** across sessions (artifacts live on disk; rerunning skips completed phases)
- Anywhere you would otherwise type `auto-flow` plus 9 manual handoffs

Do **not** invoke autopilot for one-shot edits, single-file refactors, or live
debugging. Use the canonical sub-skill directly.

## Phases (12, mapped to the 10-stage business lifecycle)

| # | Phase | Business stage | Canonical skill | Hard gate |
| - | --- | --- | --- | --- |
| 0 | Research | 1 需求发现 | `requirement-analysis` | — |
| 1 | Intent Contract | 2 需求分析 | `intent-contract` | Goal / Acceptance / Evidence all present |
| 2 | Business Case | 3 商业可行性 / 立项评估 | `business-case` | — |
| 3 | Product Spec | 4 方案-产品 | `product-spec` | — |
| 4 | Design Direction | 4 方案-设计 | `design-templates` | — |
| 5 | Implementation (Ralph) | 5 研发 | `ralph-loop` | Inner loop, max `--max-ralph-rounds` (default 20); sandbox actually runs the generated code (Python/JS/Bash/Go) |
| 6 | Code Simplifier | 5 研发 (b) | `code-simplifier` | — |
| 7 | Output Quality Gate | 6 测试与验证 | `output-quality-gate` | JSON `verdict ∈ {pass, warn}` |
| 8 | Launch Readiness | 7 上线 / 商业化准备 | `deployment-patterns` | — |
| 9 | Pilot / Gradual Rollout | 8 试点 / 灰度 | `experiment-driven-delivery` | — |
| 10 | Commercial Delivery | 9 正式商业交付 | `deployment-patterns` (commercial framing) | — |
| 11 | Ops & Retrospective | 10 运营 / 复盘 / 持续迭代 | `agent-memory-dream-loop` | No raw prompt/response in memory candidate |

Phases 1 (intent contract) and 7 (quality gate) are **hard exits** — failure
stops the run and surfaces `failed_phase` in `run.json`. Phase 5 (ralph)
retries internally up to N attempts before giving up. Every other phase is
soft and always proceeds; phase 7 grades the run as a whole.

## How to run

```bash
# Stub provider — offline, deterministic, CI-safe.
bin/super-skill autopilot --provider stub --prompt "Build a Python add(a,b) with tests"

# Real LLM provider.
ANTHROPIC_API_KEY=sk-... bin/super-skill autopilot --provider anthropic \
    --prompt "Build a TODO list API with tests" --project ./build

# Resume a run (idempotent — completed phases are skipped unless --force).
bin/super-skill autopilot --run-id 20260505-142110-f2771f --project ./build

# Iterate on a prior run with new feedback. Each phase sees the prior version
# alongside the feedback and produces an UPDATED artifact, not a fresh one.
# run.json captures parent_run_id + full lineage chain.
bin/super-skill autopilot --based-on <parent-run-id> --project ./build \
    --feedback "User reports the rejection message is too terse; expand it and add a 4xx error code."
```

Workspace layout: `<project>/.super-skill/autopilot/<run-id>/00-research.md …
11-ops-retrospective.md` plus `run.json`. The folder is `.gitignore`-d by
default and **never** stores raw prompts or model responses inside the memory
candidate itself (see anti-patterns below).

## Anti-patterns (named so we never reach for them)

**Wrong: "Autopilot will figure it out from a one-line prompt."** Phase 1 will
fail the contract gate. Always front-load the request with concrete acceptance
hints — autopilot is a harness, not a wishing well.

**Wrong: skipping phase 7 for speed.** The quality gate is the only step that
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

**Wrong: shipping without phase 8.** Launch readiness is the phase that turns
"code that works on my laptop" into "code with a Dockerfile, a CI workflow, a
kill switch, a pricing model, and a rollback plan". Skipping it leaves the
project at prototype quality.

**Wrong: skipping phase 9 (pilot).** A direct-to-GA launch is how product
launches blow up under real traffic. The pilot's whole job is to find the
problem in 5 cohort customers instead of 5,000.

**Wrong: stopping at phase 8 because "the code is deployed".** Deployed code
without a signed acceptance form, an SLA, billing triggers, training, and a
support runbook is not delivered. Phase 10 closes that gap.

**Wrong: re-running autopilot from scratch when you mean to iterate.** A new
autopilot run with the same prompt produces a fresh contract that may drift
from the original intent. Use `--based-on <parent-run-id> --feedback "..."`
so each phase sees the prior version and is told to *update* it.

**Wrong: feeding the prior implementation back as the new prompt.** That makes
the contract describe code instead of intent. Iterate-mode loads prior artifacts
into context automatically — your `--feedback` is the only thing that changes.

## Trace requirement

Every phase output must include a `Trace:` line (stub provider does this
automatically; real provider must instruct the model to). The trace is what
`agent-memory-dream-loop` and `checkpoint-rollback-safety` use to decide what
to keep, expire, or revert.

## Composes with

- `requirement-analysis` — phase 0 research (with `user-research`/`market-research`)
- `intent-contract` — phase 1 hard gate
- `business-case` — phase 2 ROI / risk / go-no-go
- `product-spec` — phase 3
- `design-templates` — phase 4
- `ralph-loop` — phase 5 inner loop (multi-language sandbox)
- `code-simplifier` — phase 6
- `output-quality-gate` — phase 7 hard gate
- `deployment-patterns` — phases 8 (launch) and 10 (commercial)
- `experiment-driven-delivery` — phase 9 pilot
- `agent-memory-dream-loop` — phase 11 ops + retrospective
- `continuous-learning`, `observability-triage-loop` — phase 11 framings
- `checkpoint-rollback-safety` — every phase artifact is a rollback point
- `harness-engineering` — the design philosophy this skill operationalises
