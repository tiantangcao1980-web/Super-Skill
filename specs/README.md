# specs/ — Living specs

This directory holds **active design specs** for Super Skill — the work-in-progress contracts that drive the next 1-3 commit windows. Borrowed from [`nexu-io/open-design`](https://github.com/nexu-io/open-design) which keeps its long PR-plans (`specs/current/critique-theater-plan.md`, etc.) as repo-first citizens rather than burying them in GitHub Issues.

## Layout

```
specs/
├── README.md           ← this file
├── current/            ← active specs that today's PRs are implementing
│   └── *.md
└── archive/            ← (future) shipped specs that are kept for history
```

## Rules

1. A spec lives in `specs/current/` only while it is being actively implemented or about to be. Once the work ships, **move** the file to `specs/archive/<YYYY-MM>/` and tag the commit that completed it.
2. Each spec opens with `Status` (`draft` / `building` / `ready-for-review` / `shipped`), `Owner`, and `Last-updated`.
3. Specs are allowed to be long. The goal is "no implementation context lives only in someone's head".
4. PRs that change implementation **must also** update the matching spec in the same diff — otherwise CI's structural audit will eventually drift.

## Index

| File | Status | What it pins down |
| --- | --- | --- |
| `current/atom-runner.md` | building | The PR-sized plan for rewriting `AUTOPILOT_PHASES` as a runtime over `manifests/atoms.json`, including the `until:` evaluator and stage-event protocol. |
| `current/critique-jury-llm.md` | building | Wire real LLM providers (anthropic / openai) into the 5-panel critique gate, with provider-agnostic JSON schema and tamper-evident composite recompute. |
| `current/ralph-multi-language.md` | draft | Lift ralph-loop verification from Python-only to also run JavaScript / Bash / Go test loops, closing the README's "Python/JS/Bash/Go" over-promise. |
| `current/design-audit-strict.md` | draft | Make `design-preflight --strict` actually fail when `visual-references` are missing, and add real-asset path discovery so brand-strict mode is honest. |
| `current/agent-adapter-runtime.md` | draft | Promote `dev-tool-adapter` from a wrapper code generator to a runtime adapter contract with `detect()` / `capabilities()` / streaming `AgentEvent`. |
| `current/atom-runner-rollout.md` | draft | Cut-over plan from frozen 12 phases to atom-driven pipeline, including back-compat for existing run.json checkpoints. |
