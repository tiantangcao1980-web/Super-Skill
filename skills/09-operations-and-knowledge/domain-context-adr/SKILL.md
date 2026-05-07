---
name: domain-context-adr
description: Capture shared project language and durable architectural decisions. Use when terms are fuzzy, a plan depends on domain boundaries, architecture choices should not be re-litigated, or a project lacks CONTEXT.md / docs/adr documentation.
---

# Domain Context And ADR

AI agents work better when the codebase has a shared language and a record of
why hard-to-reverse decisions exist.

## Context Files

Use the smallest structure that fits:

```text
CONTEXT.md                 # one bounded context
docs/adr/0001-title.md     # project-level decisions
```

For multiple contexts:

```text
CONTEXT-MAP.md
src/<context>/CONTEXT.md
src/<context>/docs/adr/0001-title.md
```

Create these files lazily. Do not create documentation just to satisfy a
template; create it when a term or decision is carrying real work.

## Glossary Discipline

When a user or codebase uses a fuzzy term:

1. Find existing definitions in `CONTEXT.md`, `CONTEXT-MAP.md`, README, docs,
   tests, route names, schemas, or public APIs.
2. If meanings conflict, state the conflict and propose one canonical term.
3. Record only domain terms that a non-implementation stakeholder would care
   about.
4. Keep implementation names out unless they are also domain language.

Suggested `CONTEXT.md` shape:

```markdown
# Context

## Language

**Canonical Term**
: Definition in business/domain language.
Avoid: overloaded or deprecated alternatives.

## Relationships

- A Customer owns many Subscriptions.

## Flagged Ambiguities

- "Account" previously meant both Customer and User; use Customer for billing
  owner and User for login identity.
```

## ADR Gate

Create an ADR only when all are true:

- The decision is meaningfully hard to reverse.
- The decision would surprise a future maintainer without context.
- Real alternatives existed and were rejected for concrete reasons.

Suggested ADR shape:

```markdown
# ADR-0001: Title

Date: YYYY-MM-DD
Status: Accepted

## Context

## Decision

## Alternatives Considered

## Consequences

## Revisit When
```

## Agent Workflow

1. Read context and ADRs before proposing architecture changes.
2. Use glossary terms in tests, PRDs, issues, and code review findings.
3. When a rejected architecture idea keeps recurring, record the reason as an
   ADR instead of rediscovering it.
4. When an ADR blocks a tempting refactor, mention the ADR and only challenge it
   if fresh evidence shows real friction.

## Attribution

This skill adapts MIT-licensed ideas from Matt Pocock's context, ADR, grilling,
and architecture-improvement skills into Super Skill's operations and knowledge
stage.
