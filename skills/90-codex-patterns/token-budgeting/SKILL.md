---
name: token-budgeting
description: Use when context is large, token cost matters, the conversation is long, or an agent workflow needs better recall without dumping full source material.
---

# Token Budgeting

The goal is not to use the largest context. The goal is to keep the right context alive.

## Budget Rules

- Spend tokens on constraints, acceptance criteria, current errors, and diffs.
- Save tokens by linking to files, commands, and generated reports instead of pasting them.
- Search first, then read exact files.
- Summarize repeated patterns once and cite representative paths.
- Preserve decisions and rejected alternatives; drop raw exploration once decisions are made.

## Context Tiers

| Tier | Keep In Prompt | Store By Reference |
| --- | --- | --- |
| Critical | goal, acceptance checks, current blocker, exact file paths | long logs |
| Useful | architecture summary, changed files, verification commands | full docs |
| Background | source project lessons, old alternatives, vendor material | raw upstream repos |

## Compression Pattern

When context is too large:

1. Write a current-state summary.
2. List files changed and files still relevant.
3. List decisions made and open risks.
4. List exact commands already run.
5. Continue from the summary, not the full transcript.

## Anti-Patterns

- Copying entire documents when `rg` plus a focused excerpt is enough.
- Keeping every research note in the active prompt.
- Asking subagents or tools to repeat the same scan.
- Reporting full command logs when only exit code, count, and failing excerpt matter.
