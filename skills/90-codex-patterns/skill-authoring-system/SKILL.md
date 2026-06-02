---
name: skill-authoring-system
description: Use when creating, refactoring, validating, or packaging AI agent skills, especially when deciding what belongs in SKILL.md versus references, scripts, assets, and installer metadata.
---

# Skill Authoring System

## Core Rule

Treat a skill as a compact operating manual, not a blog post. The body should teach the agent exactly what it cannot infer reliably, while heavy details move to `references/`, deterministic behavior moves to `scripts/`, and reusable output material moves to `assets/`.

## Recommended Shape

```
skill-name/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
```

## Authoring Checklist

- Use lowercase hyphen-case names.
- Make `description` answer "when should this trigger?", not "what is the whole workflow?"
- Keep the primary body short enough to scan.
- Link every reference file from `SKILL.md`.
- Prefer examples that expose decisions, not toy snippets.
- Add scripts only for fragile, repeated, or mechanical operations.
- Validate with a realistic prompt before publishing.

## Description As Trigger

The `description` is the only thing that decides whether a skill fires. Write it
to match how the task actually arrives, on multiple paths, not just one keyword:

```
description: <one-line capability>. Use when <explicit intent>; when <domain
term appears, e.g. "red-green-refactor">; when <behavior signal, e.g. the user
wants integration tests>; when the user says "<literal phrasing they'd use>".
```

- Cover explicit intent, domain terms, behavior signals, and the user's own
  likely phrasing. A skill that should have fired but stayed silent is almost
  always an under-specified `description`, not a missing manual call.
- Describe *when to trigger*, never the whole workflow — if the description
  summarizes the process, the agent reads it and skips the body.
- Keep responsibilities single. Two trigger surfaces that rarely co-occur are a
  sign you have two skills.

## Composing With Other Skills

Author every skill assuming peers exist (see `skill-composition`):

- **Compose through shared artifacts, not calls.** Read what an upstream skill
  wrote (`CONTEXT.md`, `DESIGN.md`, an ADR, a goal contract) and write a durable
  artifact for the next skill. Do not hardcode "then invoke skill X".
- **Lock language with a glossary.** When a skill introduces domain terms
  (Module, Interface, Seam, Depth), define them once at the top and reuse them
  verbatim so they stay consistent across composed skills.
- **Point to setup only for hard dependencies.** Put one-time configuration in a
  separate `setup-*` skill; do not make every skill carry init weight.
- **Declare order, not just capability.** If a skill belongs before or after
  others (process-first, gatekeeper-last), say so in the body.

## Skill Evolution Loop

Use test-driven thinking for important skill changes:

1. Capture a realistic pressure prompt where the current skill fails, overfires, or stays silent.
2. Identify the exact behavior the skill should change.
3. Update the smallest trigger text or body section that addresses that behavior.
4. Re-run validation: frontmatter, links, duplicate names, and a realistic manual prompt if possible.
5. Record the source idea and adaptation decision in the project docs when the skill came from another repo.

## Progressive Disclosure

1. Frontmatter: discovery and trigger routing.
2. `SKILL.md`: essential workflow and guardrails.
3. References: domain detail loaded only when needed.
4. Scripts/assets: deterministic execution and reusable material.

**Threshold rule:** when a `SKILL.md` body grows past ~500 lines, split the heavy
detail into named `references/*.md` and keep the body to decisions and flow. A
long body crowds out the task context it is meant to serve.

**Lifecycle by directory:** group skills by lifecycle phase, and use a
`deprecated/` folder for retired skills and `in-progress/` for ones still being
shaped, so every skill has a clear maturity and home instead of one flat pile.

## Failure Modes

- Huge `SKILL.md` files that crowd out the task context.
- Descriptions that summarize the process so the agent skips the body.
- Orphaned references nobody knows to load.
- Mixed responsibilities that should be separate skills.
- Direct upstream ports that preserve branding but do not fit the local lifecycle namespace.
