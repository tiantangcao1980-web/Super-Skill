---
name: intent-contract
description: Use when a user request is broad, ambiguous, high-impact, or expectation-sensitive and the agent needs to turn it into a clear delivery contract before research, design, coding, or final output.
---

# Intent Contract

Convert a user's hope into a delivery contract the agent can execute and verify.

## Contract Fields

- **User outcome**: what the user wants to be true after the work.
- **Audience**: who will use, read, buy, approve, or maintain the result.
- **Definition of done**: concrete acceptance checks.
- **Non-goals**: what should stay out of scope.
- **Constraints**: time, budget, stack, compliance, brand, data, platform, language.
- **Output shape**: repo changes, docs, demos, analysis, design, code, deployment, or report.
- **Quality bar**: performance, security, reliability, usability, visual polish, maintainability.
- **Evidence**: commands, screenshots, tests, review, links, or manual checks that prove completion.

## Workflow

1. Restate the user's desired outcome in one sentence.
2. Extract explicit constraints from the message and local project docs.
3. Add reasonable assumptions for reversible choices.
4. Identify any truly blocking ambiguity.
5. Produce or update the contract before deep work.
6. Use `output-quality-gate` before final delivery.

## Anti-Patterns

- Treating the user's first sentence as the full spec.
- Asking many questions when a safe assumption and verification loop would work.
- Optimizing for code volume instead of user-perceived success.
- Delivering artifacts without tying them back to the user's original expectation.
