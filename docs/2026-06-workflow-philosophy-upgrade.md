# 2026-06 Workflow-Philosophy Upgrade

A record of the four-phase upgrade that applied Super Skill's own workflow design
philosophy across the system, plus the skill increments absorbed from adjacent
open-source projects. Captured so the rationale is not lost to git archaeology.

## Why

Two drivers:

1. **Absorb proven lessons** from browser-use / agent-browser / opencli (browser
   automation), taste-skill / huashu-design (design taste), remotion
   (programmatic video), mattpocock & andrej-karpathy skills (skill authoring),
   and google-labs-code/stitch-skills (machine-readable DESIGN.md).
2. **Make the system consistent with its own workflow philosophy** — declarative,
   phased, contract-driven, gated, looped, learn-closed.

## Skill increments (pre-upgrade)

- **`skill-composition`** (new, `00-orchestration`): the discipline for chaining
  multiple skills — frame → build → gate, shared-artifact coupling, conflict
  serialization, override precedence, single-vs-combined decision.
- **`browser-automation`**: added the opencli adapter tier, a four-question
  selection tree, and five cross-tool mechanisms (interactive-element index,
  API-first downgrade chain, credential triple, content-boundary anti-injection,
  knowledge-persistence + autofix).
- **`anti-slop`**: token-triplet vocabulary, geometry-translation dictionary,
  universal quantitative thresholds.
- **`design-craft-gate`**: Asset & Fact Protocol (verify-before-design) and an
  enhance-prompt-style Shape Gap Matrix; DESIGN.md machine-contract law.
- **`designdna`**: machine-parseable `name`+`colors` frontmatter contract and
  orthogonal layering (prompt = layout, tokens at project level).
- **`design-templates`**: cross-page consistency loop (SITE.md / baton /
  metadata).
- **`skill-authoring-system`**: description multi-path triggering, the ~500-line
  progressive-disclosure threshold, shared-artifact composition, glossary
  locking, lifecycle directories.
- **Fix**: `cli-design` mislabeled `jackwener/opencli` as an "Open CLI
  Specification" (it is a website→CLI browser tool); the duplicate `opencli`
  trigger now routes to `browser-automation`.

## The four phases

| Phase | What | Files |
| --- | --- | --- |
| **P1 Orchestration** | Wire `skill-composition` into all six workflows; add missing frame/gate backbone skills per phase; unify Completion Gates. | `workflows/*.md`, `engineering-core-loop`, `agent-routing`, `catalog/lifecycle-map.md` |
| **P2 Deterministic validation** | `bin/super-skill validate` now checks workflow integrity: referenced skills must exist, every workflow must carry `Outputs:` or a gate. CI catches drift. | `scripts/super_skill.py` (`validate_workflows`), `tests/test_super_skill_cli.py` (+3 tests) |
| **P3 Legibility refactor** | Split the 4596-line `designdna/SKILL.md` into a 765-line operating core plus five `references/*.md` (Parts 6–15), honoring the skill's own progressive-disclosure threshold. `{% raw %}` wrappers preserved. | `designdna/SKILL.md`, `designdna/references/` |
| **P4 Docs closure** | `workflows/README.md` documents the philosophy + gate conventions; README links updated. | `workflows/README.md`, `README.md`, this file |

## Conventions established

- **Frame → Build → Gate** ordering for any multi-skill task; gatekeepers never
  run first, never skipped on shippable work.
- Skills compose through **shared artifacts** (`CONTEXT.md`, `DESIGN.md`, ADRs,
  goal contracts), not direct calls.
- Every workflow lists `Skills:` + `Outputs:` per phase and ends in a
  `Completion Gate` / `Done Means`.
- Every `DESIGN.md` carries a parseable `name`+`colors` frontmatter contract.
- A `SKILL.md` body past ~500 lines splits its detail into `references/`.

## Verification (all green)

`validate` (0 warnings / 7 workflows) · `audit` (0 trigger overlaps, 0 secrets) ·
`harness` 100% · `hermes` 100% · `memory` 100% · `evals` 7/7 + 9/9 ·
`live-evals` 4/4 · Python unittest 82 OK (incl. 3 new workflow-validation tests) ·
designdna-cli 76/0.

## Progressive-disclosure status after P3

Only two `SKILL.md` files remain above ~500 lines: `designdna` (765, the
already-split operating core) and the vendored `api-gateway` (665). The latter
is left intact to preserve upstream parity per `AGENTS.md`.
