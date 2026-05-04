---
name: agent-memory-dream-loop
description: Auto-trigger when work creates reusable experience, repeated failures, user corrections, skill changes, or memory/dream replay needs; connect durable memory, negative lessons, and offline replay into a controlled self-improving harness loop.
---

# Agent Memory Dream Loop

Use this skill when the project needs better agent memory, experience reuse, offline reflection, or a self-improving loop that turns past work into better future performance.

Memory is not a larger prompt. Memory is a governed system for deciding what should be recalled, compressed, evaluated, forgotten, or promoted into skills and tests.

## Automatic Fallback Trigger

Use this as the automatic fallback in tools that do not support plugins or lifecycle hooks.

Trigger this skill without waiting for explicit user invocation when any condition is true:

- A substantial task completed with changed files, verification, release notes, or a reusable workflow.
- A test, build, audit, deployment, user acceptance check, or agent plan failed more than once.
- The user corrected a process, preference, output shape, tool choice, or quality standard that will matter again.
- A new skill is proposed, an existing skill is patched, or overlapping skills are detected.
- The agent needed unusual runtime, model, context, sandbox, or tool-routing knowledge to succeed.

The trigger is controllable:

- Honor `SUPER_SKILL_MEMORY_DISABLED=1` or an equivalent runtime rule as a hard off switch.
- Never store raw prompt, raw assistant output, secrets, private data, customer data, credentials, or unverified claims.
- Create at most one compact candidate per trigger unless the user explicitly asks for a broader review.
- Default to review candidates, not automatic promotion.
- Prefer updating the nearest existing skill, memory, eval, or runbook before creating anything new.

## Memory Tiers

| Tier | Purpose | Storage Shape | Load Policy |
| --- | --- | --- | --- |
| Episodic traces | What happened in a session | logs, diffs, commands, errors, review notes | Retrieve on demand by task, file, error, or decision. |
| Semantic memory | Durable facts and decisions | concise notes with source and date | Load when relevant to the current project or user goal. |
| Procedural memory | How to do repeatable work | skills, runbooks, scripts, checklists | Promote only after repeated usefulness and verification. |
| Evaluation memory | What proves quality | tests, evals, rubrics, benchmarks | Load before model or workflow changes. |
| Negative memory | What failed or was rejected | short anti-pattern records | Load as warnings, not as full transcripts. |

## Dream Loop

Run the dream loop during low-risk offline time, after incidents, or after repeated agent failures.

```mermaid
flowchart LR
  A["Collect traces"] --> B["Redact and classify"]
  B --> C["Compress into memory candidates"]
  C --> D["Replay or simulate tasks offline"]
  D --> E["Mutate skill, prompt, tool, or eval"]
  E --> F["Run baseline comparison"]
  F --> G{"Improves quality?"}
  G -->|yes| H["Promote to durable memory or skill"]
  G -->|no| I["Keep as rejected lesson"]
  H --> J["Update catalog and verification"]
  I --> J
```

## Promotion Criteria

A memory candidate can be promoted only when:

- it has source evidence
- secrets and private data have been removed
- it is shorter than the raw trace
- it is still true for the current project
- it improves at least one eval, test, or review rubric
- it does not conflict with higher-priority instructions
- it has an owner or expiry rule

## Skill Evolution Constraints

Use Hermes-style curation before changing the skill library:

1. Grade the candidate with a rubric: quality gain, repeatability, safety, token impact, overlap, and verification evidence.
2. Bias toward the skill that was just used or the nearest existing skill; do not create a new skill until dedup search fails.
3. Restrict the review surface to memory, skills, catalog, and audit artifacts. Do not let a background review fork use shell, web, deployment, or broad filesystem tools.
4. Mark core harness skills as protected or pinned. Never archive or mutate them automatically.
5. Archive stale low-value skills reversibly instead of deleting them.
6. Write a compact report for every curation run: candidates reviewed, accepted, rejected, archived, restored, and tests run.

## Memory Record Format

```text
Type: semantic | procedural | evaluation | negative
Scope: user | project | skill | runtime | model
Source:
Date:
Claim:
Evidence:
Use when:
Do not use when:
Expiry:
Promotion target:
Verification:
```

## Safety Rules

- Never store secrets, credentials, private keys, auth tokens, personal identifiers, or raw customer data.
- Do not memorize a model claim unless it is verified by source, test, or human decision.
- Prefer deletion or expiry over permanent accumulation.
- Keep raw traces out of always-on context.
- Preserve rejected alternatives when they prevent repeated waste.
- Mark stale memories instead of silently reusing them.

## Harness Integration

If an agent fails, do not just ask the model to try harder. Ask:

1. Which memory was missing?
2. Which memory was stale or harmful?
3. Which skill should have been selected?
4. Which test or eval should have caught this?
5. Which runtime wrapper or tool permission made the task illegible?
6. Which negative lesson should stop this failure from repeating?

The output should be one small artifact: a memory record, skill patch, eval case, runbook note, or rejection note.
