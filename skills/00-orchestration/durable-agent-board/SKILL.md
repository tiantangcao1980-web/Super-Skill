---
name: durable-agent-board
description: Use when coordinating multi-agent, long-running, interruptible, or human-in-the-loop work that should survive context compression, restarts, retries, or ownership handoffs.
---

# Durable Agent Board

Use a durable board when work is a queue, not a single function call.

## Use A Board When

- Work crosses agent roles or human review.
- Tasks must survive restarts, interruptions, or context compression.
- A worker may block and need later input.
- Multiple attempts, comments, or handoffs must be auditable.
- Automation should deduplicate recurring tasks.

Use normal delegation for short bounded research or implementation that must return immediately to the parent context.

## Board Schema

Each task should have:

- id and title
- owner or role
- status: triage, todo, ready, running, blocked, done, archived
- body with goal, constraints, working set, and acceptance checks
- comments or handoff history
- dependency links
- workspace or worktree path
- idempotency key for recurring automation
- verification result

## Workflow

1. Decompose the goal into board tasks with clear acceptance checks.
2. Link dependencies so downstream work starts only after upstream proof.
3. Assign each task to the smallest capable role.
4. Require workers to write completion summaries with changed files, tests, and blockers.
5. Reclaim stalled work and auto-block repeated spawn or setup failures.
6. Keep human comments and unblock decisions in the task record.

## Verification

The board is healthy when every active task has an owner, a next action, a current status, and an auditable latest event.
