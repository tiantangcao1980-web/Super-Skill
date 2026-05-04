# AI-First Harness Analysis

Based on the user-provided excerpt from the X post at <https://x.com/intuitiveml/status/2043545596699750791>.

## Core Thesis

The article is not mainly about AI writing code. It is about redesigning the company around a harness where agents can do useful production work:

- product work moves from long specs to rapid experiment loops
- architecture becomes agent-legible
- CI/CD becomes deterministic and non-optional
- review is split into specialized AI gates
- observability becomes queryable by agents
- issues are triaged, fixed, deployed, and re-verified through one loop
- humans shift from code production to architecture, judgment, risk, and taste

This matches the direction of Super Skill: improve the system around the model, not just the prompt.

## What Super Skill Should Adopt

### 1. Harness Engineering

The article's most reusable idea is this rule: when AI fails, improve the harness. Do not ask the model to try harder.

Super Skill implementation:

- `harness-engineering`
- `context-engineering`
- `token-budgeting`
- `bin/super-skill harness`

### 2. Agent-Legible Architecture

Agents need to inspect the relevant system, understand boundaries, and run checks locally. Fragmented systems reduce leverage.

Super Skill implementation:

- `agent-legible-architecture`
- `context-engineering`
- `workflows/harness-engineering-operating-loop.md`

### 3. Product Iteration At Agent Speed

When implementation takes hours, product discovery cannot take weeks. PM becomes hypothesis, experiment, metric, and decision design.

Super Skill implementation:

- `agentic-product-iteration`
- `experiment-driven-delivery`

### 4. Fast Validation

Fast AI without fast validation creates fast-moving technical debt.

Super Skill implementation:

- `ai-review-gates`
- `qa-strategy`
- `verification-loop`
- `output-quality-gate`

### 5. Self-Healing Operations

The most advanced loop in the article is production signal to clustered issue to fix to deploy to re-verification.

Super Skill implementation:

- `observability-triage-loop`
- `debugging`
- `security-review`
- `github`

## Capability Map

| Article Practice | Super Skill Surface |
| --- | --- |
| Harness engineering | `harness-engineering`, `bin/super-skill harness` |
| Structured task prompt | `intent-contract`, `context-engineering` |
| Monorepo / inspectable system | `agent-legible-architecture` |
| Six-phase CI/CD | `qa-strategy`, `deployment-patterns`, `verification-loop` |
| Parallel AI review passes | `ai-review-gates`, `code-review`, `security-review` |
| Feature flags and A/B tests | `agentic-product-iteration`, `experiment-driven-delivery` |
| CloudWatch/Sentry triage | `observability-triage-loop`, `debugging` |
| Auto-created tickets | `github`, future Linear connector support |
| Architect/operator roles | `harness-engineering`, `agent-routing` |
| AI-native marketing/release ops | `documentation`, `programmatic-video`, `continuous-learning` |

## Practical Adoption Sequence

1. Run `bin/super-skill harness --json`.
2. Fix deterministic validation before increasing agent autonomy.
3. Make context and architecture legible.
4. Add AI review gates.
5. Add feature flags and experiment rules.
6. Add observability and triage loops.
7. Convert recurring failures into skills, tools, or CI gates.

## Warning

The article's throughput claims only make sense after the harness exists. Copying the speed without the gates creates production risk. The safe order is:

```text
legibility -> validation -> review gates -> progressive delivery -> observability -> self-healing
```
