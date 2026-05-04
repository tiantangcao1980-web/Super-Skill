---
name: agentic-product-iteration
description: Use when product planning, PM work, or feature discovery needs to move at AI-agent implementation speed through rapid prototype, ship, measure, and iterate loops.
---

# Agentic Product Iteration

When build time collapses, long specification cycles become the bottleneck. Product work shifts from committee planning to fast evidence loops.

## Loop

1. Define the user outcome and metric.
2. Slice the smallest shippable experiment.
3. Put the feature behind a gate.
4. Ship to internal users or a small cohort.
5. Read behavioral, quality, and business metrics.
6. Kill, iterate, or graduate the feature the same day when possible.

## Product Contract

Each experiment needs:

- hypothesis
- target user/cohort
- success metric
- guardrail metrics
- feature flag or rollback path
- expected lifetime if inconclusive
- decision rule: ship, iterate, or kill

## Anti-Patterns

- Writing a large PRD when the feature can be safely tested in hours.
- Treating A/B testing as a launch ceremony instead of a product decision tool.
- Keeping bad features alive because implementation was expensive.
- Letting PM, design, marketing, or QA operate at human-speed while engineering operates at agent-speed.

## Output

Produce an experiment brief and a same-day decision plan.
