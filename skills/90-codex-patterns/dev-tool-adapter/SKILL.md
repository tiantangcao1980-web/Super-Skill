---
name: dev-tool-adapter
description: Adapt Super Skill workflows across Cursor, Trae, OpenCode, OpenClaw, Claude Code, and Codex without duplicating canonical skill behavior.
---

# Dev Tool Adapter

Use this skill when Super Skill must run inside more than one AI developer tool: Cursor, Trae, OpenCode, OpenClaw, Claude Code, Codex, or another compatible agent runtime.

The goal is portability without drift. Keep the canonical capability in `SKILL.md`, then generate the thinnest runtime wrapper each tool needs.

## Adapter Principles

1. Treat the repository skill as the source of truth.
2. Preserve trigger intent, constraints, tool policy, memory policy, output format, and verification steps.
3. Convert only the runtime envelope: project rules, skill folder path, config file, agent profile, permission settings, or slash command.
4. Do not fork the behavior per tool unless the runtime cannot support a required feature.
5. Record unsupported features and the fallback plan in the adapter output.

## Runtime Matrix

| Runtime | Primary Surface | Adapter Shape | Verification |
| --- | --- | --- | --- |
| Codex | `AGENTS.md`, `.agents/skills/<name>/SKILL.md`, plugins | Symlink or copy canonical skill; keep project rules in `AGENTS.md`; package collections as plugins when distribution is needed. | `codex` can list/load the skill; project instructions are visible; approval and sandbox policy match. |
| Claude Code | `.claude/skills/<name>/SKILL.md`, `~/.claude/skills/<name>/SKILL.md`, `CLAUDE.md` | Copy or symlink skill folder; use `CLAUDE.md` only for project-wide operating rules. | Skill appears as a slash command or auto-loads from description; supporting files resolve. |
| Cursor | `.cursor/rules/*.mdc`, optional `AGENTS.md` | Convert only always-on and file-scoped guidance into `.mdc`; keep larger workflows as referenced skill docs. | Agent sees the rule for the intended path/mode; rule does not overfill context. |
| Trae | `.rules` / project rules, MCP configuration | Convert project constraints and workflow triggers into Markdown rules; keep tool access in MCP config. | Trae loads rules; MCP tools are visible; tool and privacy constraints are explicit. |
| OpenCode | `opencode.json`, `.opencode/agents/`, `.opencode/skills/` | Map roles to agents, permissions to `permission`, and reusable workflows to skills. | `opencode debug config` resolves expected model, skills, agents, and permissions. |
| OpenClaw | `~/.openclaw/skills/<name>/SKILL.md`, `<workspace>/skills/<name>/SKILL.md`, plugins | Install canonical skill folders; prefer workspace skills for project overrides. | `openclaw skills list`, `openclaw skills info <name>`, and `openclaw skills check` pass. |

## Adapter Output

Produce a compact report:

```text
Runtime:
Canonical skill:
Target file or folder:
Wrapper generated:
Behavior preserved:
Unsupported features:
Permission/sandbox mapping:
Memory mapping:
Verification command:
Known drift risk:
```

## Conversion Checklist

- Front-load trigger terms in descriptions because some tools shorten or rank skill lists.
- Keep stable rules small; reference larger files instead of copying them into always-on context.
- Use path-scoped rules when the runtime supports them.
- Prefer symlinks for local development and copies for portable bundles.
- Carry over safety constraints: destructive commands, secrets, network access, tool permissions, and human approval gates.
- Carry over output constraints: schema, evidence, tests, links, and known gaps.
- Carry over memory constraints: what may be remembered, what must expire, and what must never be stored.

## Drift Control

When the same skill is adapted to several runtimes:

1. Compute the canonical skill hash.
2. Add the hash or source path to generated wrappers.
3. Regenerate wrappers after canonical changes.
4. Run runtime-specific smoke checks.
5. Delete wrappers that no longer point at a real canonical skill.

If a runtime requires incompatible behavior, create a small adapter note under `references/` and link it from this skill. Do not duplicate the whole workflow.
