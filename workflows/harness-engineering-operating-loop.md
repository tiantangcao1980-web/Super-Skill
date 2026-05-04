# Harness Engineering Operating Loop

Use this workflow when a team wants to move from AI-assisted development to AI-first delivery.

## 0. Readiness Assessment

Skills/tools:

- `harness-engineering`
- `bin/super-skill harness --json`
- `bin/super-skill hermes --json`

Outputs:

- harness readiness score
- Hermes-style self-improving readiness score
- missing capability list
- ordered upgrade plan

## 1. Make The System Legible

Skills:

- `agent-legible-architecture`
- `context-engineering`
- `prompt-cache-layering`
- `token-budgeting`
- `durable-agent-board`

Outputs:

- architecture map
- local validation commands
- service boundaries and contracts
- context pack template
- stable and ephemeral prompt layer map
- resumable working-state and handoff contract

## 2. Make Tooling Safe And Bounded

Skills:

- `toolset-sandbox-routing`
- `checkpoint-rollback-safety`
- `security-review`

Outputs:

- tool permission map
- sandbox/worktree/container policy
- destructive-action approval gates
- prompt-injection and secret-handling rules
- checkpoint and rollback contract for risky changes

## 3. Make Validation Deterministic

Skills:

- `qa-strategy`
- `test-driven-development`
- `e2e-testing`
- `verification-loop`
- `agent-eval-harness`

Outputs:

- CI quality gates
- unit/integration/e2e coverage map
- environment parity checks
- agent eval task set, traces, deterministic verifiers, and no-skill baseline

## 4. Add Review Gates

Skills:

- `ai-review-gates`
- `code-review`
- `security-review`

Outputs:

- code quality review pass
- security review pass
- dependency/license review pass
- product-risk review pass

## 5. Add Progressive Delivery

Skills:

- `agentic-product-iteration`
- `experiment-driven-delivery`
- `deployment-patterns`

Outputs:

- feature flag strategy
- rollout/kill decision rules
- A/B or cohort experiment plan

## 6. Add Observability And Triage

Skills:

- `observability-triage-loop`
- `debugging`
- `documentation`

Outputs:

- structured signal checklist
- health report workflow
- clustered triage ticket format
- post-fix re-verification signal

## 7. Close The Learning Loop

Skills:

- `persistent-memory-curation`
- `continuous-learning`
- `skill-evolution-loop`
- `skill-authoring-system`
- `output-quality-gate`

Outputs:

- new or updated skills
- curated memory/session-history/project-context decisions
- runbooks
- CI/audit/tool improvements
- final user-expectation fit check
