---
name: karpathy-discipline
description: Posture skill that enforces "think before coding, simplicity first, surgical changes, goal-driven execution" — the four working rules distilled from Andrej Karpathy's commentary on LLM coding failure modes. Use when writing, reviewing, or refactoring code; when you catch yourself adding speculative abstractions; when the user says "do exactly what I asked, nothing more"; when the task is "fix this bug", "refactor X", or "add validation" and you need to reframe it as verifiable success criteria.
---

# Karpathy Discipline — Posture Before Code

**Tradeoff.** This skill biases toward caution and small diffs over speed.
For a 5-line one-shot script, use judgment and skip it. For anything that
will be reviewed, merged, or shipped, run all four rules.

## The four rules

### 1. Think before coding

- Surface every assumption *before* writing code. If you don't know the
  language version, the data shape, or who calls this function, **ask**.
- Never silently pick. A silent pick becomes a hidden bug 100% of the time
  the picker guessed wrong.

### 2. Simplicity first

- The minimum code that makes the test pass is the right code.
- *"If 200 lines could be 50, rewrite it."* — Karpathy's smell test.
- No error handling for impossible scenarios. No `try/except` around a
  call that cannot raise. No fallbacks for branches that cannot be reached.
- Senior-engineer smell test: would a senior engineer roll their eyes at
  this abstraction? If yes, delete it.

### 3. Surgical changes

- Every changed line should trace directly to the user's request.
- Don't refactor adjacent code "while you're there". File the cleanup as
  a follow-up; don't bundle it.
- Only remove orphans your edit caused. Pre-existing unused code is not
  your problem unless removing it was the request.

### 4. Goal-driven execution — restate every task as a test

| Vague request | Test-shaped restatement |
| --- | --- |
| "Fix the bug" | Write a failing test that reproduces it; make it pass; nothing else changes |
| "Refactor X" | Tests pass before AND after; no behavior change is observable |
| "Add validation" | Write tests for invalid inputs first; then make them fail correctly |
| "Make it faster" | Write a benchmark that shows the current speed; the change must beat it |
| "Clean up Y" | Define "clean": fewer lines? fewer abstractions? a specific lint rule? |

> *"Don't tell it what to do — give it success criteria and watch it go."*
> — Karpathy

If you can't write a verifiable test for the request, the request is not
specified yet. Stop and ask.

## When this skill fires inside autopilot

- Phase 1 (intent-contract): the test-shaped restatement is the contract's
  "Acceptance" section.
- Phase 5 (code-simplifier): rule 2 (simplicity) and rule 3 (surgical) drive
  what gets deleted.
- Phase 6 (output-quality-gate): the gate checks that every line in the
  deliverable traces to a contract acceptance item.

## Anti-patterns

**Wrong: "let me also fix this nearby thing while I'm here".** Bundles two
diffs into one, breaks bisect, makes review hard. File a follow-up.

**Wrong: defensive code for impossible inputs.** `if user is None: raise` in
a function whose only caller passes a fresh constructor. Delete it; trust
the caller; if the caller is the bug, fix the caller.

**Wrong: "we'll need this abstraction later".** YAGNI. Add it when the
second caller appears, not before.

**Wrong: skipping the test-shape rewrite.** Going straight to code on a
vague request is how you ship the wrong feature.

## Composes with

- `intent-contract` — the test-shape rewrite IS the contract's acceptance
- `code-simplifier` — rule 2 + rule 3 drive what gets pruned
- `output-quality-gate` — rule 3 (every line traces to request) is a gate criterion
- `verification-loop` — the test-shaped restatement is what verification runs
