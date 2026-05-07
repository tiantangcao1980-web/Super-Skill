# Harness Engineering Validation

This project treats harness engineering as the environment around the model: context, specs, tools, memory, state, validation, evals, deployment, observability, safety, and learning loops that make agent work repeatable.

The 2026 extension in this repository adds four checks that are now central to agent-driven delivery: developer-tool adaptation, provider-neutral model contracts, memory/dream replay as a governed learning loop, and automatic trigger governance.

## Source-Derived Criteria

The X thread argues that AI-first engineering is a workflow redesign: product, architecture, implementation, testing, deployment, monitoring, triage, and team roles are rebuilt around agents. Its most important operating rule is: when an agent fails, fix the missing capability and make it legible and enforceable for the agent.

`walkinglabs/awesome-harness-engineering` frames the field as context engineering, evaluation, observability, orchestration, safe autonomy, and software architecture. Its resource categories add several practical requirements that Super Skill should cover:

- context, memory, and working state
- constraints, guardrails, tool boundaries, and safe autonomy
- specs, agent files, and workflow design
- evals, traces, observability, and benchmarks
- runtimes, sandboxes, durable state, and reference harnesses
- runtime adapters for IDEs and agent hosts
- model routing, structured output, and compatibility gates
- memory promotion, negative lessons, and offline replay

## Current Fit

| Criterion | Super Skill Surface | Status |
| --- | --- | --- |
| Intent and context contract | `intent-contract`, `context-engineering`, `output-quality-gate` | Covered |
| Spec and workflow design | `product-spec`, `design-dev-flow`, `auto-flow`, `AGENTS.md` guidance | Covered |
| Agent-legible architecture | `agent-legible-architecture`, local CLI validation, monorepo-style lifecycle tree | Covered |
| Working state and resumability | `durable-agent-board`, `prompt-cache-layering`, `persistent-memory-curation`, handoff summaries | Covered |
| Tool and sandbox policy | `toolset-sandbox-routing`, `checkpoint-rollback-safety`, `security-review`, `audit` | Covered |
| Deterministic CI validation | `validate`, `audit`, `harness`, `hermes`, Python tests, DesignDNA tests, GitHub Actions | Covered |
| Agent evals and traces | `agent-eval-harness`, `verification-loop`, `browser-automation` trace guidance | Covered as a skill; project-level benchmark corpus is still optional |
| Specialized review gates | `ai-review-gates`, `code-review`, `security-review`, dependency/license audit surfaces | Covered |
| Progressive delivery | `experiment-driven-delivery`, `deployment-patterns`, feature flag and kill-switch guidance | Covered as guidance |
| Observability and triage | `observability-triage-loop`, structured logs/metrics/ticket guidance | Covered as guidance |
| Token and cost control | `token-budgeting`, `prompt-cache-layering`, context-efficient handoffs | Covered |
| Developer tool adaptation | `dev-tool-adapter`, adapter matrix for Cursor, Trae, OpenCode, OpenClaw, Claude Code, Codex | Covered |
| Model adaptation | `model-adaptation-contract`, input/output schemas, routing and compatibility gates | Covered |
| Memory and dream replay | `agent-memory-dream-loop`, `memory` assessment, promotion criteria, negative memory | Covered |
| Automatic trigger governance | `super-skill-memory-harness`, `auto-trigger-policy.json`, `skill-lifecycle-policy.json`, `triggers` assessment | Covered |
| Human risk governance | `harness-engineering`, `agent-routing`, review and approval rules in `AGENTS.md` | Covered |
| Learning loop | `continuous-learning`, `skill-authoring-system`, `skill-evolution-loop`, `hermes` assessment | Covered |

## Verdict

Super Skill now satisfies the core design and development needs for LLM- and agent-driven project work at the skill and workflow layer. It can guide an agent from research to product, design, implementation, testing, release, operations, and learning while keeping the work inspectable and verifiable.

The important caveat: it is a portable skill and workflow harness, not a production platform by itself. For a live product team, the skills must still be connected to concrete systems: CI, feature flags, logs, metrics, Sentry/CloudWatch-style error sources, issue trackers, deployment pipelines, and real eval datasets.

## Validation Projects

`bin/super-skill evals --json` adds deterministic validation projects that act like capability evals for this skill collection:

- `ai-first-saas-launch`: end-to-end research, product, design, development, QA, delivery, operations, and memory.
- `cross-runtime-memory`: Codex hook plugin plus fallback triggers for developer tools without plugin support.
- `design-to-frontend-quality`: design-craft-gate, DesignDNA, PRODUCT/DESIGN context, UI frameworks, deterministic anti-pattern audit, browser/quality checks, and brand sync.
- `incident-to-learning-loop`: observability, debugging, security review, evals, memory, and skill lifecycle gates.
- `token-efficient-llm-io`: intent, context, token budgeting, prompt cache, model contracts, and output quality.

These projects prove the repository exposes the right skills, policies, and validation surfaces. They do not replace live agent runs against a real product backlog.

`bin/super-skill live-evals --json` goes one step further by creating temporary runnable projects from recipes:

- `mini-saas-feedback-loop`: feature flag, kill switch, metrics, rollback, observability, release notes, and memory hook.
- `cross-runtime-memory-adapter`: runtime policy mapping for Codex, Cursor, Trae, OpenCode, OpenClaw, and Claude Code.
- `design-frontend-quality-gate`: DesignDNA tokens, accessible rendering, responsive constraints, and anti-slop checks.

These live evals run code-based graders and unit tests. They still do not call an external LLM; they are the stable executable harness that future model-driven attempts should target.

## Remaining Validation Gaps

- Live production observability is described but not connected to a real telemetry backend in this repository.
- Feature-flag and A/B testing are guidance-level skills unless the target project wires Statsig, LaunchDarkly, or another experimentation provider.
- Agent eval support now includes deterministic live project fixtures, but each adopting project must still supply realistic backlog tasks, traces, model attempts, and no-skill baselines.
- Runtime adapters still need smoke checks inside each target tool because Cursor, Trae, OpenCode, OpenClaw, Claude Code, and Codex evolve quickly.
- The memory/dream loop now has plugin/fallback auto-trigger checks, but downstream projects still need a real eval corpus before any automatic promotion.
- `bin/super-skill harness` is a static readiness scan. It proves the repository exposes harness surfaces; it does not prove a downstream product's runtime behavior without project-specific evals and production signals.

## Verification Commands

```bash
bin/super-skill harness --json
bin/super-skill hermes --json
bin/super-skill memory --json
bin/super-skill triggers --json
bin/super-skill evals --json
bin/super-skill live-evals --json
bin/super-skill memory-plugin --dry-run --json
bin/super-skill validate --json
bin/super-skill audit --json
python3 -m unittest discover -s tests
```
