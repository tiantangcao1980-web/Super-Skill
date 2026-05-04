---
name: test-driven-development
description: Use when implementing a feature, bug fix, refactor, or behavior change where automated tests can protect the result before production code changes.
---

# Test-Driven Development

Use a small red-green-refactor loop.

## Loop

1. Write one failing test that describes the next behavior.
2. Run only the relevant test and confirm it fails for the expected reason.
3. Write the smallest production change that makes it pass.
4. Run the focused test, then the nearest broader suite.
5. Refactor only while tests stay green.
6. Repeat for the next behavior.

## Guardrails

- Test behavior and public contracts, not private implementation details.
- Prefer real collaborators; mock only slow, nondeterministic, or external boundaries.
- If a test passes before the implementation change, fix the test before continuing.
- If the failure is setup noise, correct setup until the test fails on the intended missing behavior.
- Do not bundle cleanup into the green step. Refactor after evidence is green.

## Output Evidence

When reporting, include:

- the failing test command and expected failure observed
- the passing focused command
- the broader command that guards regressions
- any intentionally untested area
