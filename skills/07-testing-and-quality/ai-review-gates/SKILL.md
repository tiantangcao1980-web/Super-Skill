---
name: ai-review-gates
description: Use when designing or running AI-assisted pull request review gates for code quality, security, dependency, license, or regression risk before merge.
---

# AI Review Gates

AI review should be a gate with clear scopes, not a generic "review this" comment.

## Parallel Passes

Run separate review lenses:

- **Code quality**: logic, maintainability, performance, test adequacy.
- **Security**: auth boundaries, injection, secrets, data exposure, unsafe defaults.
- **Dependency**: supply chain, license, version drift, vulnerable packages.
- **Product risk**: user-facing behavior, rollout, metrics, rollback, support impact.

## Gate Rules

- Each pass must report findings by severity and file path.
- Critical findings block merge.
- Non-blocking findings become follow-up issues only when the risk is explicit.
- Human reviewers focus on strategy, architecture, and risk acceptance.
- The review prompt must include diff, intent contract, tests run, and rollout plan.

## Review Packet

```text
Intent:
Changed files:
Risk areas:
Tests and evidence:
Rollout/rollback:
Known gaps:
```

## Failure Modes

- One broad review pass misses specialized risks.
- Review comments are suggestions with no merge policy.
- Humans re-review line by line because the agent review lacks evidence.
- Dependency and license risks are treated as an afterthought.
