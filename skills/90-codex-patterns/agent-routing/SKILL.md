---
name: agent-routing
description: Use when a task can be handled by direct editing, shell tools, browser tools, MCP connectors, or subagents and the agent needs to choose the lightest reliable execution path.
---

# Agent Routing

## Routing Order

Use the least heavy path that preserves correctness:

1. Direct reasoning for simple stable answers.
2. Shell/file inspection for repository facts.
3. Local scripts for repeatable mechanical checks.
4. MCP/connectors for external systems such as GitHub, Slack, databases, and design tools.
5. Browser verification for UI behavior.
6. Subagents only for independent, bounded, parallel work when the active environment allows it.

## Decision Rules

- If the next result blocks your immediate step, do it locally.
- If tasks are independent and material, split them.
- If an SDK, API, law, price, release, or current product behavior may have changed, verify from primary/current sources.
- If a command output is noisy, summarize only the needed evidence.
- If edits are required, inspect local conventions first.

## Handoff Contract

Every delegated or tool-routed task needs:

- Scope
- Files or systems owned
- Output expected
- Verification expected
- What not to touch

## Stop Conditions

Stop routing and ask only when the next action is destructive, permission-bound, or materially ambiguous.

## Scope Note

This skill chooses the lightest execution *path* within a step. To order
multiple *skills* across a task (frame → build → gate, handoffs, conflict
rules), use `skill-composition`.
