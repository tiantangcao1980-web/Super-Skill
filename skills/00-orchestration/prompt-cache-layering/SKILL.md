---
name: prompt-cache-layering
description: Use when designing LLM context, system prompts, memory, project instructions, or ephemeral task context so long sessions stay token-efficient and cache-friendly.
---

# Prompt Cache Layering

Separate stable context from per-turn context. Stable layers should change rarely; volatile data should ride in the user/task layer or tool output.

## Layer Model

| Layer | Examples | Rule |
| --- | --- | --- |
| Identity | agent role, tone, durable behavior rules | stable and short |
| Tool guidance | tool use rules, safety defaults | stable, provider-aware |
| Memory snapshot | curated durable facts | frozen at session start when possible |
| Skill index | names and trigger descriptions | compact, load bodies on demand |
| Project context | AGENTS.md, repo conventions | concise, progressively discovered |
| Ephemeral task context | logs, diffs, screenshots, current goal | inject late; do not mutate stable prompt |

## Workflow

1. Classify every context item by volatility.
2. Put stable, high-value items early and keep them compact.
3. Put task-specific evidence in the current user/task context.
4. Load full skill bodies only when they clearly apply.
5. Summarize long sessions into goal, constraints, progress, decisions, files, next steps, and critical evidence.
6. Preserve exact errors, file paths, commands, and acceptance checks through compression.

## Failure Modes

- Updating the system prompt every turn and losing cache efficiency.
- Saving noisy session details into always-on memory.
- Compressing away the current blocker or verification result.
- Loading every possible rule instead of discovering relevant rules progressively.

## Output

Produce a context layering plan with:

- stable layers
- ephemeral layers
- what can be searched later
- what must be preserved exactly
- what can be safely dropped
