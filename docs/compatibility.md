# Compatibility

## Runtime Layout

The repository uses lifecycle directories:

```text
skills/04-design-system/designdna/SKILL.md
```

Agent runtimes usually use a flat directory:

```text
~/.codex/skills/designdna/SKILL.md
~/.claude/skills/designdna/SKILL.md
```

Use `bin/super-skill install` to bridge the layouts.
Use `bin/super-skill plan` first when you need a read-only preview for CI, review, or dry-run reports.

## Supported Targets

| Target | Method |
| --- | --- |
| Codex | `bin/super-skill install --target ~/.codex/skills` |
| Claude Code | `bin/super-skill install --target ~/.claude/skills` |
| Hermes Agent | `bin/super-skill install --profile hermes` |
| Cursor/Windsurf/opencode | Use `cross-tool-packaging` guidance; wrappers can be generated from `SKILL.md` |
| Generic agent | Copy skill folders or convert to markdown rules |

## Known Constraints

- Installable skills must have unique names. Current lifecycle skills have no duplicate names.
- Hermes Agent should use `--profile hermes`; it excludes Hermes-native mirror skills to avoid duplicate slash commands and overlapping procedural guidance. `plan` reports existing target-name conflicts, and `install` skips them unless `--force` is used.
- Cowork vendor skills are not flattened by default because several plugin domains intentionally reuse names.
- Some copied skills reference external tools such as Docker, GitHub CLI, Node, browsers, or package managers. `doctor` checks the common baseline only.
- DesignDNA CLI keeps its own Node package under `packages/designdna-cli/`.
- Compatibility symlinks preserve the original DesignDNA layout expected by its CLI and tests: `design-md`, `designdna`, `assets`, `playground`, `showcase`, and `packages/cli`.
- `bin/super-skill audit` treats these compatibility symlinks as a release contract.

## Verification Baseline

```bash
bin/super-skill validate
bin/super-skill plan --profile all --json
bin/super-skill plan --profile hermes --json
bin/super-skill audit
bin/super-skill install --profile all --dry-run
bin/super-skill doctor
```
