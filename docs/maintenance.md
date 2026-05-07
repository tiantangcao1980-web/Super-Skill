# Maintenance

## Add A Skill

1. Put it under the matching lifecycle directory in `skills/`.
2. Use lowercase hyphen-case `name`.
3. Keep `description` focused on trigger conditions.
4. Keep heavy details in `references/`, scripts in `scripts/`, reusable assets in `assets/`.
5. Run:

```bash
bin/super-skill validate
bin/super-skill audit
bin/super-skill design-preflight --project <project-root>
bin/super-skill design-extract --project <frontend-path>
bin/super-skill design-audit --project <frontend-path>
bin/super-skill harness
bin/super-skill hermes
bin/super-skill memory
bin/super-skill triggers
bin/super-skill goal --objective "Implement scoped change" \
  --scope "src/example" \
  --done "example.test exits 0" \
  --done "README.md documents the change" \
  --done "git diff stays inside src/example and README.md" \
  --stop-if "new dependency required" \
  --stop-if "existing tests fail" \
  --stop-if "secrets appear in diff" \
  --budget 80000
bin/super-skill evals
bin/super-skill live-evals
bin/super-skill memory-plugin --dry-run
bin/super-skill plan --profile hermes
bin/super-skill catalog
```

## Move A Skill

Moving a skill between lifecycle directories is safe if the skill folder remains self-contained and the `name` does not change.

## Update Vendor Content

Vendor content lives outside installable `skills/` unless names are explicitly namespaced. If promoting a vendor skill into lifecycle skills, rename both folder and frontmatter, for example:

```text
sales-call-prep
marketing-competitive-analysis
```

Then update NOTICE and run validation.

## Release Checklist

- `bin/super-skill validate` exits 0.
- `bin/super-skill audit` exits 0 with no blocking failures.
- `bin/super-skill design-audit --project <frontend-path> --json` reports deterministic design anti-pattern findings for review.
- `bin/super-skill design-preflight --project <project-root> --json` reports PRODUCT/DESIGN context, shape brief, token, visual reference, and anti-pattern readiness.
- `bin/super-skill design-extract --project <frontend-path> --json` reports extracted design tokens, component signals, utility classes, recommendations, and optional sidecar / DESIGN.md draft outputs.
- `bin/super-skill harness --json` reports the AI-first harness capability matrix.
- `docs/harness-engineering-validation.md` records the source-derived harness criteria, current evidence, and remaining runtime gaps.
- `bin/super-skill hermes --json` reports the Hermes-style self-improving agent capability matrix.
- `bin/super-skill memory --json` reports the memory, dream replay, and experience reuse capability matrix.
- `bin/super-skill triggers --json` reports automatic trigger and skill lifecycle policy validity.
- `bin/super-skill goal --json ...` renders an audit-friendly Codex `/goal` contract with budget, Done when, and Stop if checks.
- `bin/super-skill evals --json` runs validation projects for lifecycle coverage, goal-driven delivery, cross-runtime memory, DesignDNA/frontend quality, incident learning, and token-efficient LLM I/O.
- `bin/super-skill live-evals --json` runs local temporary project graders for SaaS feedback loops, runtime memory adapters, and DesignDNA frontend quality.
- `bin/super-skill memory-plugin --dry-run --json` reports Codex plugin, marketplace, hook, and config operations without mutating the machine.
- `bin/super-skill plan --profile core --json` emits a deterministic read-only plan.
- `bin/super-skill plan --profile hermes --json` emits a Hermes-safe plan with native mirror exclusions.
- `bin/super-skill install --profile all --dry-run` exits 0.
- `bin/super-skill install --profile core --dry-run --with-memory-plugin --json` verifies first-install plugin bootstrap.
- `python3 -m unittest discover -s tests` passes.
- `bin/super-skill catalog` has been regenerated.
- DesignDNA CLI tests pass when package dependencies are installed.
- Git status is clean before tagging or publishing.
