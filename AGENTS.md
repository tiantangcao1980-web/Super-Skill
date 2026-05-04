# Super Skill Agent Guide

This repository is a lifecycle-organized skills collection. Keep `SKILL.md` files as the source of truth.

## Rules

- Use `bin/super-skill validate` before claiming the repository is healthy.
- Use `bin/super-skill catalog` after adding, removing, or moving skills.
- Keep installable skill names lowercase hyphen-case and globally unique.
- Keep vendor ecosystems under `vendor/` unless a skill is namespaced for flat installation.
- Preserve upstream license and NOTICE files when importing third-party material.
- Prefer small, self-contained skill folders with progressive disclosure: `SKILL.md`, then `references/`, `scripts/`, `assets/`.

## Commit Messages

Use the Lore-style trailer protocol when making commits:

```text
Explain why the change was made

Constraint: ...
Rejected: ... | ...
Confidence: high
Scope-risk: narrow
Tested: ...
Not-tested: ...
```
