---
name: agent-legible-architecture
description: Use when restructuring, documenting, or assessing architecture so AI agents can understand cross-system impact, run local checks, and make safe changes.
---

# Agent-Legible Architecture

Design architecture so agents can see, reason, test, and modify it.

## Principles

- Prefer one inspectable workspace over scattered opaque repositories when cross-service changes are common.
- Keep service boundaries explicit: contracts, owners, data flow, events, error modes.
- Make local integration tests possible without production-only dependencies.
- Keep generated code, schemas, and contracts discoverable by path.
- Document how to run the smallest meaningful validation for each subsystem.

## Agent Legibility Checklist

- [ ] The agent can find the entrypoint, data model, API contract, and tests from repo search.
- [ ] Cross-service dependencies are represented in docs, schemas, or typed clients.
- [ ] The same command path works for humans, agents, and CI.
- [ ] Environment parity checks catch missing env vars, services, ports, and secrets.
- [ ] Integration failures produce structured logs with request IDs or trace IDs.
- [ ] A change can be rolled back or feature-gated without another large refactor.

## When Fragmentation Hurts

Fragmentation is costly when a single feature repeatedly requires edits across multiple repos, hidden dashboards, manual deployments, or tests that only work after merge. In that case, either unify the workspace or create a first-class context bundle and integration harness.

## Output

Return:

- current legibility gaps
- recommended boundary changes
- required local/CI commands
- docs or schemas to add
- risks of unifying vs. leaving separated
