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
| Codex | `bin/super-skill install --target ~/.codex/skills`; add memory/dream hooks with `--with-memory-plugin` |
| Claude Code | `bin/super-skill install --target ~/.claude/skills`; use `agent-memory-dream-loop` implicit trigger fallback |
| Hermes Agent | `bin/super-skill install --profile hermes`; keep Hermes-native mirror exclusions and lifecycle curation |
| Cursor | Use `dev-tool-adapter` to generate `.cursor/rules/*.mdc` wrappers from canonical `SKILL.md`, including memory trigger policy |
| Trae | Use `dev-tool-adapter` to generate `.rules` guidance and keep external tools in MCP config |
| OpenCode | Use `dev-tool-adapter` to map skills, agents, model routing, permissions, and memory trigger rules into `opencode.json` and `.opencode/` |
| OpenClaw | Install canonical folders to `~/.openclaw/skills` or workspace `skills`; verify with OpenClaw skill checks |
| Windsurf/other IDE agents | Use `dev-tool-adapter` guidance; wrappers can be generated from `SKILL.md` |
| Generic agent | Copy skill folders or convert to markdown rules |

## Known Constraints

- Installable skills must have unique names. Current lifecycle skills have no duplicate names.
- Hermes Agent should use `--profile hermes`; it excludes Hermes-native mirror skills to avoid duplicate slash commands and overlapping procedural guidance. `plan` reports existing target-name conflicts, and `install` skips them unless `--force` is used.
- Cowork vendor skills are not flattened by default because several plugin domains intentionally reuse names.
- Some copied skills reference external tools such as Docker, GitHub CLI, Node, browsers, or package managers. `doctor` checks the common baseline only.
- Runtime adapters are thin wrappers. The canonical `SKILL.md` remains the source of truth, and wrappers should record source paths or hashes to avoid drift.
- Model compatibility is governed by `model-adaptation-contract`: switching models requires structured-output, tool-use, failure, and regression checks before promotion.
- Memory portability is governed by `agent-memory-dream-loop`: raw traces stay outside always-on context, and only verified lessons become durable memory.
- Automatic memory triggering is governed by `manifests/auto-trigger-policy.json`: plugin hooks where supported, implicit skill fallback where hooks are unavailable, and no automatic promotion.
- Skill self-evolution is governed by `manifests/skill-lifecycle-policy.json`: protected skills, importance levels, usage/stale review, reversible archive, and dedup before new skills.
- DesignDNA CLI keeps its own Node package under `packages/designdna-cli/`.
- Compatibility symlinks preserve the original DesignDNA layout expected by its CLI and tests: `design-md`, `designdna`, `assets`, `playground`, `showcase`, and `packages/cli`.
- `bin/super-skill audit` treats these compatibility symlinks as a release contract.

## Verification Baseline

```bash
bin/super-skill validate
bin/super-skill plan --profile all --json
bin/super-skill plan --profile hermes --json
bin/super-skill audit
bin/super-skill harness
bin/super-skill hermes
bin/super-skill memory
bin/super-skill triggers
bin/super-skill memory-plugin --dry-run
bin/super-skill install --profile all --dry-run
bin/super-skill install --profile core --dry-run --with-memory-plugin
bin/super-skill doctor
```
