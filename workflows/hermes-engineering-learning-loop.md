# Hermes Engineering Learning Loop

Use this workflow after complex agent work, repeated failures, long sessions, or any task where future agents should become better.

> **Orchestration.** Sequence these stages with `skill-composition` (frame → build → gate); each stage consumes the prior stage's named outputs as shared artifacts.

## 1. Capture The Experience

Skills:

- `agent-memory-dream-loop`
- `persistent-memory-curation`
- `context-engineering`

Output:

- durable facts
- temporary facts
- project conventions
- repeated failures
- negative lessons
- useful command/test evidence

Decision:

- memory, session history, project docs, skill, test, automation, or discard

## 2. Preserve Context Without Bloat

Skills:

- `prompt-cache-layering`
- `token-budgeting`

Output:

- stable prompt layers
- ephemeral task context
- exact evidence to preserve
- large artifacts referenced by path

## 3. Evolve Skills From Evidence

Skills:

- `agent-memory-dream-loop`
- `skill-evolution-loop`
- `skill-authoring-system`

Output:

- updated skill or new skill
- reason for update
- pressure prompt or failure pattern
- validation command
- dream replay or baseline comparison result

Guardrail:

- prefer updating an existing skill over creating a nearby duplicate

## 4. Route Tools And Execution Environments

Skills:

- `dev-tool-adapter`
- `model-adaptation-contract`
- `toolset-sandbox-routing`
- `agent-routing`

Output:

- required capabilities
- excluded capabilities
- runtime adapter target
- model profile, output contract, and fallback policy
- sandbox/worktree/container decision
- approval or rollback gate

## 5. Promote Long Work To A Durable Board

Skills:

- `durable-agent-board`
- `auto-flow`

Use this when:

- work spans roles
- work needs human unblock
- work must survive restart
- recurring automation needs deduplication
- audit history matters

Output:

- tasks with owners, status, dependencies, workspace, and acceptance checks

## 6. Add Safety Before Speed

Skills:

- `checkpoint-rollback-safety`
- `security-review`
- `ai-review-gates`

Output:

- checkpoint or branch
- rollback path
- review lanes
- targeted verification

## 7. Close The Loop

Skills:

- `observability-triage-loop`
- `continuous-learning`
- `output-quality-gate`

Output:

- resolved/remaining risks
- tests or checks added
- docs or runbooks updated
- skills updated
- memory candidates promoted or rejected
- next automation candidate

## Done Means

- useful facts are stored in the right layer
- raw traces are outside always-on context
- dream replay has either promoted a useful artifact or recorded a rejected lesson
- repeated workflow is encoded as a skill or script
- risky work has rollback evidence
- long work has durable state
- final output maps back to user intent and verification
