# Source Benchmark Analysis

This note records the source-learning pass that shaped the ultra-lite
engineering profile. The goal is not to vendor whole upstream skill sets; it is
to translate the strongest MIT-licensed patterns into small, testable Super
Skill behaviors.

## Sources Reviewed

| Source | Local revision | License signal | Lessons extracted |
| --- | --- | --- | --- |
| `obra/superpowers` | `f2cbfbe` | MIT LICENSE, copyright Jesse Vincent | Strong skill-first workflow, TDD, verification-before-completion, finishing discipline, and method-level behavior shaping. |
| `forrestchang/andrej-karpathy-skills` | `2c60614` | `license: MIT` in skill metadata | Think first, keep changes simple, prefer surgical edits, avoid premature abstraction, and verify against the real goal. |
| `mattpocock/skills` | `733d312` | MIT LICENSE, copyright Matt Pocock | CONTEXT.md, ADRs, shared language, docs-backed review, architecture maintenance, and practical engineering triage. |

## Translation Into Super Skill

Super Skill already had broad lifecycle coverage. The gap was not another
large bundle; it was a compact default that agents can carry into any project
without inflating context or duplicating runtime-native skills.

New or strengthened capabilities:

- `engineering-core-loop`: a compact route -> contract -> test -> implement ->
  review -> verify -> finish -> learn loop.
- `ultra-lite` install profile: a 12-skill curated profile for high-discipline
  engineering work.
- `domain-context-adr`: shared language and durable decision capture based on
  CONTEXT.md and ADR files, created lazily.
- `safe-command-governance`: a documentation and script safety gate for
  commands that agents tend to copy and execute.
- `evals/projects/ultra-lite-engineering-discipline`: a deterministic fixture
  proving the profile still contains the expected behavior surface.

## Guardrails

- Keep borrowed ideas as concise re-expressions, not copied skill bodies.
- Preserve attribution and license context in documentation and skill notes.
- Prefer a smaller always-on core over loading every specialized skill.
- Require fresh verification before completion claims.
- Promote memory only when a lesson is verified, deduplicated, and safe to
  retain.

## Remaining Work

- Add more transcript-style evals that score real agent behavior, not only
  skill availability and acceptance language.
- Add command remediation annotations for vendor or documentation examples that
  intentionally mention risky commands.
- Keep `ultra-lite` under a strict size cap so it remains useful for
  token-constrained tools.
