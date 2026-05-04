---
name: cross-tool-packaging
description: Use when exporting or adapting skills for Codex, Claude Code, Cursor, Windsurf, opencode, Hermes, or other AI coding environments with different skill or rule file layouts.
---

# Cross-Tool Packaging

## Source Of Truth

Keep canonical behavior in each `SKILL.md`. Generate tool-specific wrappers from that source rather than hand-maintaining parallel prompt files.

## Target Shapes

| Target | Shape |
| --- | --- |
| Codex | `AGENTS.md` plus installable skill folders |
| Claude Code | `~/.claude/skills/<name>/SKILL.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | workspace rules or imported markdown |
| opencode | `.opencode/skills/*.md` plus index |
| Generic agent | plain markdown with frontmatter preserved |

## Compatibility Rules

- Preserve frontmatter `name` and `description`.
- Flatten only when names are unique.
- Namespace plugin bundles that intentionally reuse names.
- Keep assets and references relative to the copied skill folder.
- Validate after export by checking every referenced local file.

## Release Checklist

- Catalog generated.
- Installer dry-run succeeds.
- Duplicate names explained.
- Licenses and NOTICE updated.
- README shows the recommended install path.
