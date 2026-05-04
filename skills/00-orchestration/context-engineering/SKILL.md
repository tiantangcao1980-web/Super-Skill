---
name: context-engineering
description: Use when preparing LLM or AI agent context for large codebases, long documents, multi-step work, multi-session handoffs, or token-constrained tasks.
---

# Context Engineering

Context is an input product. Build the smallest context package that lets the agent make correct decisions.

## Context Pack

Use this structure for non-trivial work:

```text
Goal: one sentence
User expectation: what success feels like to the user
Current state: facts verified from files, commands, or sources
Working set: exact files, symbols, docs, URLs, screenshots, or datasets
Constraints: stack, style, safety, compatibility, time
Decisions made: settled choices and rejected alternatives
Unknowns: open questions and how to resolve them
Output contract: expected artifacts and evidence
Token budget: what to read fully, skim, search, or ignore
```

## Progressive Disclosure

1. **Intent capsule**: 100-200 words.
2. **Working set**: only the files, excerpts, source links, and commands needed now.
3. **Evidence appendix**: logs, long docs, or traces referenced by path rather than pasted.
4. **Handoff summary**: compact current state when the session is long or context is near limit.

## Token Discipline

- Prefer `rg`, file paths, and short excerpts over bulk pasting.
- Summarize stable facts once; do not repeat them in every prompt.
- Keep high-entropy data: failing errors, acceptance criteria, API contracts, diffs, and exact commands.
- Drop low-value data: generic explanations, duplicate logs, full vendor docs, stale plans.
- When context grows, create a fresh context pack before continuing.

## Failure Modes

- The model receives too much context and misses the important constraint.
- The model receives summaries with no evidence pointers.
- The prompt contains goals but no acceptance tests.
- The handoff preserves chronology but loses the current decision state.
