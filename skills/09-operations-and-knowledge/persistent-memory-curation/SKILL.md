---
name: persistent-memory-curation
description: Use when deciding what an AI agent should remember across sessions, what should stay in searchable history, and how to keep long-term memory compact and safe.
---

# Persistent Memory Curation

Treat memory as a scarce control plane, not a transcript dump.

## Memory Tiers

| Tier | Use For | Storage Pattern |
| --- | --- | --- |
| Always-on memory | stable user preferences, environment facts, project conventions | compact curated entries |
| Searchable history | episodic details, prior discussions, old investigations | session search or logs |
| Project context | repo rules, run commands, architecture boundaries | AGENTS.md, docs, runbooks |
| Skills | repeatable procedures learned from work | SKILL.md plus references/scripts |

## Save

- User preferences that change future outputs.
- Environment or repo facts that are stable and expensive to rediscover.
- Tool quirks, command gotchas, and local verification patterns.
- Repeated failures that should become a guardrail, test, or skill.

## Skip

- One-off paths, raw logs, large code snippets, temporary plans.
- Facts already documented in project context.
- Secrets, credentials, private tokens, or copied `.env` values.
- Vague diary entries that cannot guide a future action.

## Curation Loop

1. After a task, list durable facts discovered.
2. Classify each fact: memory, session-search only, project doc, skill, or discard.
3. Compress memory entries into short actionable statements.
4. Replace stale entries instead of appending duplicates.
5. Convert repeated memory pressure into a project doc or skill.

## Verification

Before saving or recommending memory, answer:

- Will this still matter in 30 days?
- Is it safer or cheaper to rediscover?
- Could this leak a secret or encode a wrong assumption?
- Does it belong in project context instead?
