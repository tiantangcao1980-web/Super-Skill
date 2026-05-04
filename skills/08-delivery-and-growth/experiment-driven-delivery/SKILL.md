---
name: experiment-driven-delivery
description: Use when shipping features behind flags, running A/B tests, gradual rollouts, kill switches, metric guardrails, or fast product iteration loops.
---

# Experiment-Driven Delivery

Production delivery should support learning quickly without betting the whole product on every deploy.

## Delivery Contract

Every experiment needs:

- feature flag name
- rollout cohorts and percentages
- success metric
- guardrail metrics
- dashboard or query path
- kill switch owner
- rollback condition
- decision deadline

## Rollout Pattern

1. Ship behind a disabled flag.
2. Enable for team/internal users.
3. Enable a small percentage.
4. Monitor success and guardrail metrics.
5. Increase rollout, iterate, or kill.
6. Record the decision and evidence.

## Guardrails

- No feature ships without an off switch.
- No rollout advances without metrics.
- No experiment stays ambiguous forever.
- Severe quality, payment, engagement, latency, or error degradation triggers rollback or kill.

## Output

Return a rollout plan, metric checks, and kill/iterate/graduate decision rule.
