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
- `all`: complete installable namespace

## Commands

```bash
bin/super-skill plan --profile dev --json
bin/super-skill install --profile dev --target ~/.codex/skills
bin/super-skill audit --json
```

`plan` is read-only. `install --dry-run` remains available for compatibility, but `plan` is better for machine-readable preflight checks.
