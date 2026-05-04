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
bin/super-skill harness
bin/super-skill hermes
bin/super-skill memory
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
- `bin/super-skill harness --json` reports the AI-first harness capability matrix.
- `docs/harness-engineering-validation.md` records the source-derived harness criteria, current evidence, and remaining runtime gaps.
- `bin/super-skill hermes --json` reports the Hermes-style self-improving agent capability matrix.
- `bin/super-skill memory --json` reports the memory, dream replay, and experience reuse capability matrix.
- `bin/super-skill plan --profile core --json` emits a deterministic read-only plan.
- `bin/super-skill plan --profile hermes --json` emits a Hermes-safe plan with native mirror exclusions.
- `bin/super-skill install --profile all --dry-run` exits 0.
- `python3 -m unittest discover -s tests` passes.
- `bin/super-skill catalog` has been regenerated.
- DesignDNA CLI tests pass when package dependencies are installed.
- Git status is clean before tagging or publishing.
