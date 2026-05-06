# Goal Contract Details

Goal contracts are optimized for long-running agent work where false completion is more dangerous than slow progress.

## Contract Fields

| Field | Purpose | Failure if missing |
| --- | --- | --- |
| Objective | One concrete change or outcome | Agent optimizes the wrong thing |
| First action | Read/report before edits for specs or brownfield work | Agent starts before context is loaded |
| Scope | What can and cannot change | Scope creep |
| Constraints | Project, safety, tool, and model limits | Agent violates local rules |
| Done when | Evidence-backed success criteria | False completion |
| Stop if | Mechanical guardrails | Runaway or risky continuation |
| Token budget | Soft budget and wrap-up point | Cost/context runaway |

## Audit-Friendliness Rubric

- Excellent: 5-8 Done when items, 3+ Stop if items, concrete files/commands/tests, explicit budget, scoped first action.
- Good: 3+ Done when items, 3+ Stop if items, minor ambiguity only.
- Weak: vague objective, fewer than 3 acceptance items, no budget, or unverifiable stop conditions.
- Refuse to render: the user wants "everything" or "optimize all" without an enumerable source.

## Default Stop Conditions

Use these when relevant:

- Existing tests fail after implementation; do not weaken or delete tests to make them pass.
- A task requires modifying a MUST NOT path.
- A spec conflict is detected.
- A new dependency or credential is required.
- The goal exceeds the budget before all Done when items have evidence.

## Ralph Loop Bridge

Inside implementation, convert each Done when item into a Ralph Loop exit check:

```text
ANCHOR: quote objective + one Done when item
VERIFY: run the command or inspect artifact
DISTANCE: X/Y Done when items proven
DECIDE: continue until every item has evidence
```

Run `code-simplifier` only after the goal is functionally proven.
