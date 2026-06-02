# Agentic Context To Delivery Workflow

Use this workflow when a project is driven by an AI agent or LLM and quality depends on both input clarity and output verification.

> **Orchestration.** Run the phases with `skill-composition` (frame → build → gate; couple phases through each phase's `Outputs` as shared artifacts; serialize conflicting skills).

## 0. Intent Contract

Skills:

- `intent-contract`

Outputs:

- user outcome
- definition of done
- output shape
- constraints and non-goals

## 1. Context Pack

Skills:

- `context-engineering`
- `prompt-cache-layering`
- `token-budgeting`
- `file-curation`
- `domain-context-adr`
- `model-adaptation-contract`

Outputs:

- compact context pack
- stable versus ephemeral prompt layers
- working file/source list
- decisions and open unknowns
- token budget
- model profile, output schema, and fallback policy

## 2. Runtime And Lifecycle Execution

Skills:

- `engineering-core-loop`
- `karpathy-discipline`
- `goal-driven-workflow`
- `dev-tool-adapter`
- `harness-engineering`
- `agent-legible-architecture`
- `toolset-sandbox-routing`
- `durable-agent-board`
- `auto-flow`
- `research-to-delivery` lifecycle skills
- `design-dev-flow`
- `test-driven-development`

Outputs:

- product/design/development artifacts
- agent-readable architecture and validation plan
- runtime adapter and tool permission map
- toolset, sandbox, and durable-task routing decisions
- implementation with evidence
- changed files and decision records

## 3. Quality Verification

Skills:

- `ai-review-gates`
- `qa-strategy`
- `verification-loop`
- `security-review`
- `safe-command-governance`
- `performance`
- `checkpoint-rollback-safety`
- `browser-automation`
- `output-quality-gate`

Outputs:

- test and audit evidence
- checkpoint or rollback evidence for risky work
- risk list
- user-expectation fit check

## 4. Progressive Delivery And Observation

Skills:

- `agentic-product-iteration`
- `experiment-driven-delivery`
- `observability-triage-loop`

Outputs:

- feature flag and rollout plan
- success and guardrail metrics
- kill/iterate/graduate decision rule
- production signal and triage plan

## 5. Delivery And Learning

Skills:

- `git`
- `github`
- `documentation`
- `agent-memory-dream-loop`
- `persistent-memory-curation`
- `continuous-learning`
- `skill-evolution-loop`
- `skill-authoring-system`

Outputs:

- commit, PR, release, or deployed artifact
- concise final report
- reusable lessons routed into memory, searchable history, docs, tests, automation, skills, or rejected negative memory

## Completion Gate

Do not declare done until:

- Each phase produced its named `Outputs`, or recorded why it was skipped.
- Quality Verification shows fresh evidence, not a stale or assumed pass.
- The intent contract's definition of done and output shape are satisfied.
- Lessons are routed into memory/docs/skills (or rejected as negative memory).
