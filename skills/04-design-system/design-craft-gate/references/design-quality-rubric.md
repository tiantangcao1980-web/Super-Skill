# Design Quality Rubric

Rank design issues by user impact, not by how easy they are to fix.

| Severity | Meaning | Examples |
| --- | --- | --- |
| P0 | Blocks task completion or violates trust/safety | inaccessible primary action, destructive action ambiguity |
| P1 | Creates serious comprehension, accessibility, or reliability risk | low contrast on key text, broken mobile layout, missing error state |
| P2 | Degrades perceived quality or repeated-use efficiency | generic typography, noisy card layout, weak hierarchy |
| P3 | Minor polish or consistency drift | one-off spacing, minor token mismatch, copy tone drift |

## Score

Start at 100 and subtract:

- P0: 25
- P1: 12
- P2: 6
- P3: 3

Below 70 is not ready to ship. Between 70 and 84 requires a focused polish pass.
Above 85 is acceptable if P0/P1 are absent and the user goal is satisfied.

## Evidence Checklist

- context loaded or assumptions documented
- shape brief exists for new work
- token/component alignment checked
- `design-preflight` passes or missing context is explicitly documented
- deterministic anti-pattern scan run when files exist
- accessibility labels and contrast checked
- responsive behavior checked for mobile and desktop
- loading, empty, error, disabled, and overflow states considered
- performance/motion budget considered
- reusable decisions documented
