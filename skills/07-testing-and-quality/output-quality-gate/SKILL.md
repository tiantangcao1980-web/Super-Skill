---
name: output-quality-gate
description: Use before delivering LLM-generated code, plans, designs, reports, docs, analyses, or agent work products to verify they satisfy the user's intent and include evidence.
---

# Output Quality Gate

An LLM output is done only when it satisfies the user's expected outcome and includes evidence.

## Gate Checklist

Score each item as pass, gap, or not applicable:

- **Intent fit**: answers the real user goal, not just the literal prompt.
- **Completeness**: covers required artifacts, edge cases, and stated constraints.
- **Usability**: the next human or agent can act without guessing.
- **Evidence**: tests, commands, screenshots, links, source references, or explicit inspection.
- **Reliability**: failure modes, rollback, compatibility, and known risks are named.
- **Safety**: no secrets, destructive operations, policy violations, or hidden external dependencies.
- **Token efficiency**: concise final answer, no repeated logs, no irrelevant source dump.

## Output Contract

Before final response, confirm:

```text
User asked for:
Delivered:
Evidence:
Known gaps:
Next useful action:
```

## When A Gap Exists

- Fix it if it is inside scope and feasible.
- Name it if it is real and cannot be closed now.
- Do not imply success from partial checks.

Use `verification-loop` for command evidence and this skill for user-expectation fit.
