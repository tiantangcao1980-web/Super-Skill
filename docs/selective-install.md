# Selective Install

Super Skill keeps a human-friendly lifecycle tree and installs it into the flat namespace expected by most agent runtimes.

## Manifests

- Profiles: `manifests/install-profiles.json`
- Components: `manifests/install-components.json`

Profiles resolve to lifecycle stages. Components provide a stable vocabulary for future finer-grained installs without changing the current directory layout.

## Profiles

- `core`: research-to-delivery baseline without stack-specific development packs
- `dev`: interface, development, quality, delivery, operations, and Codex patterns
- `design`: DesignDNA plus quality skills
- `hermes`: Hermes Agent target profile; installs the broad lifecycle set to `~/.hermes/skills` by default while excluding Hermes-native mirror skills
- `all`: complete installable namespace

## Hermes Agent Profile

Hermes Agent already has native runtime primitives for memory, skill evolution, prompt compression/layering, toolset routing, Kanban, and checkpoint rollback. The `hermes` profile therefore excludes these Super Skill mirrors by default:

- `checkpoint-rollback-safety`
- `durable-agent-board`
- `persistent-memory-curation`
- `prompt-cache-layering`
- `skill-evolution-loop`
- `toolset-sandbox-routing`

Use `all` only when you intentionally want those skills installed as external guidance inside Hermes too.

`plan` also reports `target_conflicts` for any skill directory that already exists in the target. `install` skips existing targets unless `--force` is explicitly provided.

## Commands

```bash
bin/super-skill plan --profile dev --json
bin/super-skill install --profile dev --target ~/.codex/skills
bin/super-skill plan --profile hermes --json
bin/super-skill install --profile hermes
bin/super-skill audit --json
```

`plan` is read-only. `install --dry-run` remains available for compatibility, but `plan` is better for machine-readable preflight checks.
