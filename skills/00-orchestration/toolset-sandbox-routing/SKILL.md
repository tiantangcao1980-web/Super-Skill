---
name: toolset-sandbox-routing
description: Use when deciding which tools, integrations, sandboxes, models, or execution environments an AI agent should have for a task while preserving safety and token efficiency.
---

# Toolset And Sandbox Routing

Tool access is a capability contract. Give the agent enough tools to complete the job and no more than the job needs.

## Routing Matrix

| Task Shape | Toolset | Boundary |
| --- | --- | --- |
| Read-only repo lookup | search and file read | no mutation |
| Code implementation | file edit, terminal, tests | repo worktree or local sandbox |
| Risky shell work | terminal in container or disposable worktree | approvals/checkpoints |
| External research | web/search only | cite sources |
| Long-running automation | scheduled job or durable queue | bounded prompt and delivery target |
| Secret-dependent integration | connector or env allowlist | never expose secrets in prompt |

## Procedure

1. Identify the task's required capabilities.
2. Exclude tools that add side effects without helping the goal.
3. Prefer read-only tools until the working set is clear.
4. Use containers, worktrees, or remote sandboxes for risky or parallel work.
5. Require human or policy gates for destructive commands, secrets, production deploys, and irreversible changes.
6. Route cheap auxiliary work to cheaper models only when quality risk is low.
7. Record tool assumptions in the final verification evidence.

## Red Flags

- A subtask gets full terminal and network access without a reason.
- A background or scheduled job can create more background jobs.
- A tool result contains secrets that would enter memory or logs.
- A model is asked to infer capability availability instead of checking it.

## Verification

Confirm:

- chosen tools map to task requirements
- side effects are bounded
- approval or rollback exists for risky operations
- outputs include enough evidence for review
