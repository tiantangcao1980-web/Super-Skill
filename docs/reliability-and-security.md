# Reliability and Security

Super Skill uses a two-layer verification model.

## Structural Validation

Run:

```bash
bin/super-skill validate --json
```

This checks:

- required skill frontmatter
- lowercase hyphen-case installable names
- duplicate installable skill names
- local links and referenced files
- DesignDNA and vendor resource counts

## Repository Audit

Run:

```bash
bin/super-skill audit --json
```

This checks:

- installable namespace de-duplication
- Cowork vendor duplicate names as source-material metadata
- profile and component manifest drift
- DesignDNA compatibility symlinks
- executable CLI entrypoints
- hardcoded secret-like values
- risky destructive, hard-reset, and pipe-to-shell command patterns

The audit fails on broken contracts and hardcoded secret-like values. Risky command patterns are reported for review because they can be legitimate when documented as warnings, examples, or cleanup scripts.

## Harness Readiness

Run:

```bash
bin/super-skill harness --json
```

This checks whether a project exposes the capabilities agents need for production work: intent/context contracts, agent-legible architecture, deterministic CI, AI review gates, progressive delivery, observability triage, output gates, and learning loops.

## Install Safety

Preview before mutation:

```bash
bin/super-skill plan --profile core --target ~/.codex/skills --json
```

Then install:

```bash
bin/super-skill install --profile core --target ~/.codex/skills
```

Prefer `--dry-run` or `plan` in CI and documentation. Use `--force` only when replacing a known Super Skill-managed target.

## Security Handling

- Do not commit `.env` files or real credentials.
- Keep external integrations optional unless they are audited and central to the skill.
- Treat `vendor/` as source material; do not install it directly into a flat skills runtime.
- When a secret-like finding is real, rotate the credential before publishing a fix.
