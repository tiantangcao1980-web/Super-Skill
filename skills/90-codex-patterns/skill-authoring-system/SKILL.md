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

## Failure Modes

- Huge `SKILL.md` files that crowd out the task context.
- Descriptions that summarize the process so the agent skips the body.
- Orphaned references nobody knows to load.
- Mixed responsibilities that should be separate skills.
- Direct upstream ports that preserve branding but do not fit the local lifecycle namespace.
