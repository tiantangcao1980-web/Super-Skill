---
name: engineering-core-loop
description: Compact always-on engineering loop for AI-agent development: skill/context check, goal contract, TDD or explicit test exception, small implementation, review gates, verification evidence, finish decision, and memory candidate. Use when starting non-trivial code work, reviewing implementation plans, or installing a minimal Super Skill profile.
---

# Engineering Core Loop

This is the small sharp loop inside the larger Super Skill lifecycle. It keeps
agent-driven work from becoming a broad prompt-and-pray run.

## Loop

1. **Route.** Check relevant skills and project instructions before acting.
   If a task is simple enough to skip a skill, say why in one short sentence.
2. **Contract.** Convert the request into a goal with scope, constraints,
   `Done when`, `Stop if`, and verification commands.
3. **Test first.** For feature, bug, refactor, or behavior work, write one
   failing test or name the explicit exception. Do not invent broad tests.
4. **Implement small.** Make the smallest change that satisfies the current
   acceptance item. Keep every changed line traceable to the request.
5. **Review.** Run focused review lenses: correctness, security/safety,
   dependency/license risk, and product/rollout risk when relevant.
6. **Verify fresh.** Run the commands that prove the claim now. Read output
   and report remaining gaps.
7. **Finish deliberately.** Choose commit, PR, keep branch, or cleanup based
   on evidence and user intent.
8. **Learn safely.** Promote only verified, deduplicated lessons into memory.
   Never store raw prompts, raw responses, or private session transcripts.

## Default Gates

```text
ENGINEERING_CORE_LOOP:
route=<skill/context checked|skipped:reason>
contract=<goal|inline|missing>
test_first=<red-green|exception:reason|not_applicable>
implementation=<small|blocked|not_started>
review=<quality|security|dependency|product|skipped:reason>
verification=<command:evidence|missing>
finish=<commit|pr|keep|cleanup|not_ready>
memory=<candidate|skipped:reason>
```

## Hard Rules

- No completion claim without fresh verification evidence.
- No speculative abstraction before a second real use.
- No drive-by refactor, formatting churn, or unrelated cleanup.
- No weakening tests to make implementation pass.
- No destructive git or filesystem cleanup without an explicit user request.
- No persistent memory write unless the lesson is verified, deduplicated, and
  reviewable.

## When To Use Other Skills

- Use `skill-composition` when more than one skill applies and you need the
  trigger order, handoffs, and conflict rules across them.
- Use `goal-driven-workflow` when the task spans multiple phases or sessions.
- Use `test-driven-development` for any protected behavior change.
- Use `karpathy-discipline` when scope may bloat or assumptions are fuzzy.
- Use `domain-context-adr` when language, boundaries, or decisions need
  durable documentation.
- Use `safe-command-governance` before documenting or running risky commands.
- Use `verification-loop` before final status, commit, PR, or push.

## Attribution

This Super Skill-native loop adapts engineering discipline patterns from
Superpowers, Karpathy-style coding guardrails, and Matt Pocock's skills
ecosystem. Those projects are MIT licensed; this skill is a concise
re-expression for the Super Skill lifecycle rather than a vendored copy.
