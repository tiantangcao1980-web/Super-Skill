---
name: selective-install-planning
description: Use when packaging, installing, publishing, or auditing Super Skill profiles across Codex, Claude, or other agent skill directories.
---

# Selective Install Planning

Treat installation as a plan before it becomes a mutation.

## Operating Model

- Profiles live in `manifests/install-profiles.json`.
- Components live in `manifests/install-components.json`.
- The lifecycle source of truth remains `skills/<stage>/<skill>/SKILL.md`.
- Agent runtimes usually consume a flat namespace, so installable skill names must be unique.

## Workflow

1. Preview with `bin/super-skill plan --profile <profile> --json`.
2. Validate structure with `bin/super-skill validate --json`.
3. Audit compatibility and safety with `bin/super-skill audit --json`.
4. Install with `bin/super-skill install --profile <profile> --target <skills-dir>`.

## Rules

- Never install from `vendor/` directly unless a future namespace plan exists.
- Keep compatibility symlinks intact for DesignDNA.
- Add new installable skills to the lifecycle stage that owns the user's intent, not the upstream source label.
- Prefer a local CLI or script for deterministic checks; promote to MCP only when a persistent tool boundary is worth the operational cost.
