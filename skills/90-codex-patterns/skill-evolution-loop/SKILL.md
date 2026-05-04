---
name: skill-evolution-loop
description: Use when turning completed agent work, repeated failures, user corrections, or useful workflows into improved skills without bloating the skill collection.
---

# Skill Evolution Loop

Skills should evolve from evidence. Do not create a skill just because a task was interesting.

## Trigger Conditions

Create or update a skill when one of these is true:

- The agent needed a non-obvious sequence of steps.
- A failure repeated or was expensive to diagnose.
- The user corrected the process in a way that will matter again.
- A workflow crossed tools, files, providers, or review gates.
- A deterministic script would save repeated context and reduce mistakes.

Automatic skill evolution must stay controlled. If a plugin, hook, background review, or implicit trigger proposes an update, treat it as a candidate until it passes the gates below.

## Decision Tree

1. If the lesson is a stable fact about one project, update project context.
2. If the lesson is a user preference, record compact memory.
3. If the lesson is a reusable procedure, update or create a skill.
4. If the lesson is mechanical or fragile, add a script under the skill.
5. If the lesson is broad philosophy, write docs, not a skill.

## Update Procedure

1. Capture the pressure prompt or failure pattern.
2. Find the nearest existing skill before creating a new one.
3. Change the smallest trigger text, workflow step, reference, or script needed.
4. Keep `SKILL.md` compact; move detail to `references/`.
5. Validate frontmatter, links, duplicate names, and install plan.
6. Record the source inspiration and local adaptation in docs when borrowed from another project.

## Curator Constraints

Borrow the Hermes Curator pattern, but keep mutation bounded:

- Run curation on a schedule or after substantial work, not on every tiny turn.
- Use rubric-first review instead of free-form "improve the skill" prompts.
- Prefer active-update: update a skill that was just loaded before touching unrelated skills.
- Restrict the review toolset to memory, skills, catalog, and audit evidence.
- Track usage, last-used time, importance, and stale candidates outside `SKILL.md`.
- Never auto-delete. Archive reversibly and protect `critical` and `important` skills.
- A new skill requires dedup search, overlap explanation, verification evidence, and a catalog/audit pass.

## Anti-Bloat Checks

- Could this be one paragraph in an existing skill?
- Would the skill trigger too often?
- Does the description clearly say when to use it?
- Is the body mostly generic advice the model already knows?
- Is there verification evidence that the new behavior helps?
