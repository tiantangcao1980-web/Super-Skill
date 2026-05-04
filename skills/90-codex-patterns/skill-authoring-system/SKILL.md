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
