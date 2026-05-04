---
name: observability-triage-loop
description: Use when designing production health reports, error clustering, incident triage, self-healing workflows, Sentry/CloudWatch style analysis, or auto-created investigation tickets.
---

# Observability Triage Loop

Agents can only repair what they can observe. Logs, metrics, traces, and tickets must be structured enough for an agent to query and act on.

## Required Signals

- structured logs with service, endpoint, user or tenant impact, request ID, and error class
- metrics for latency, errors, traffic, conversions, cost, and business guardrails
- exception aggregation with stack traces and release versions
- deploy events and feature-flag events
- ownership metadata for services and routes

## Daily Loop

1. Query production signals.
2. Summarize system health for humans.
3. Cluster errors by root pattern, not by raw message count.
4. Score severity: user impact, revenue impact, frequency, regression, security, data risk, blast radius, age, trend.
5. Create or update investigation tickets with sample logs and suggested paths.
6. After a fix deploys, re-check the original signal.
7. Close, reopen, or escalate based on evidence.

## Ticket Shape

```text
Cluster:
Severity:
Affected users/endpoints:
First seen / trend:
Sample logs:
Suspected cause:
Suggested investigation:
Verification signal:
```

## Anti-Patterns

- Human-only dashboards that agents cannot query.
- Unstructured logs with missing correlation IDs.
- Duplicate tickets for the same error pattern.
- Closing incidents because a PR merged, not because production signals recovered.
