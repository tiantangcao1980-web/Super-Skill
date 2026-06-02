---
name: skill-composition
description: Use when more than one skill could apply to a task and the agent must decide trigger order, how skills hand off, and how to avoid conflicts. Covers process-before-implementation ordering, gatekeeper-last review, shared-artifact coupling, conflict serialization, override precedence, and the single-vs-combined decision. Trigger when a request spans research, design, build, test, and ship; when two skills give conflicting guidance; when building an entry/router skill that dispatches others.
---

# Skill Composition

Skills are not isolated commands. A non-trivial task pulls in several skills, and
the value comes from how they chain. This skill is the doctrine for combining
them so the result is coherent instead of a pile of overlapping advice.

## First Principle

**No skill is the only skill.** Every skill assumes peers exist and must hand off
cleanly. When you load one skill, ask which skill runs before it and which runs
after, then sequence them — do not run them all at once and hope.

## Composition Order

Run skills in lifecycle order, not load order:

1. **Process / posture skills first.** They decide *how* to work:
   `intent-contract`, `goal-driven-workflow`, `context-engineering`,
   `karpathy-discipline`, `debugging`. These frame the task before any builder
   skill touches code.
2. **Domain / implementation skills second.** They decide *what* to build:
   framework skills, `backend-patterns`, `frontend-patterns`, `designdna`.
3. **Gatekeeper skills last.** They decide *whether to ship*: `code-review`,
   `security-review`, `output-quality-gate`, `verification-loop`. Gatekeepers
   never run first and never get skipped on shippable work.

Canonical shape: **Frame → Build → Gate.** "Let's build X" starts at Frame;
"fix this bug" starts at `debugging` then Frame; "review this" jumps to Gate.

## Coupling: Share Artifacts, Not Calls

Skills compose through files, not by invoking each other. Each skill reads a
durable artifact the previous one wrote and writes one for the next:

| Producer | Artifact | Consumer |
| --- | --- | --- |
| `intent-contract` | goal contract (`Done when` / `Stop if`) | engineering / goal loop |
| `domain-context-adr` | `CONTEXT.md`, `docs/adr/` | architecture & build skills |
| `designdna` | `DESIGN.md`, tokens | `design-craft-gate`, frontend skills |
| build skills | code + verification evidence | gatekeeper skills |
| any skill | `.super-skill/memory/*` candidate | `persistent-memory-curation` |

A decision recorded in an ADR or `CONTEXT.md` is settled — downstream skills
**consume it and do not re-litigate it**. This file-based seam is what keeps a
multi-skill run loosely coupled and resumable across sessions.

## Triggering Is Semantic, Not Keyword

A skill joins the composition only if its `description` matches the task. Trust
`description` triggering over hardcoded keyword tables. When a skill that should
have fired stayed silent, the fix is a more specific `description` (see
`skill-authoring-system`), not a manual call.

## Conflict Resolution

When two loaded skills disagree:

1. **User instructions win** (CLAUDE.md / AGENTS.md / direct request) over any
   skill.
2. **Rigid-discipline skills win** over flexible-pattern skills on the same
   point (e.g. `test-driven-development` over a convenience shortcut).
3. **Gatekeeper veto** stands on safety, security, and ship-readiness.
4. **Serialize, never parallelize, conflicting skills.** Two skills that mutate
   the same file or contend on the same decision run in sequence with one owner
   per step.
5. **Name precedence** for same-named skills: enterprise > user > project;
   plugin skills stay namespaced as `plugin:skill`.

## Single vs Combined

Combine skills when the task spans multiple lifecycle phases, needs a quality
gate, or has plural intent. Use one skill when the job is a single bounded
responsibility with no ship risk. Over-combining burns context and tokens;
under-combining skips the gate. State the chosen chain in one line before
acting.

## Router / Entry Pattern

For recurring multi-skill flows, use an entry skill that names its downstream
chain explicitly rather than re-deciding each time. `auto-flow` and
`design-dev-flow` are the reference routers: their body lists every skill they
dispatch and the order. When you build a new router, list the chain in its
`description` and body so the composition is legible.

## Composition Gate

Report this before a multi-skill task starts:

```text
SKILL_COMPOSITION:
chain=<frame-skills → build-skills → gate-skills>
order=<process-first|gatekeeper-last|verified>
coupling=<shared-artifacts:names|inline:reason>
conflicts=<none|resolved:rule>
mode=<combined|single:reason>
```

## Hard Rules

- Never run a gatekeeper skill before the build it gates.
- Never re-open a decision already recorded in an ADR or `CONTEXT.md`.
- Never parallelize skills that contend on the same file or decision.
- Never let a skill assume it is the only skill in the run.

## When To Use Other Skills

- Use `agent-routing` / `toolset-sandbox-routing` to pick the execution path
  *within* a step; this skill picks the *sequence of skills* across steps.
- Use `skill-authoring-system` when a missing or mis-firing trigger is the real
  problem.
- Use `auto-flow` or `design-dev-flow` when the chain is a known end-to-end flow.

## Attribution

Distilled from Anthropic's "skills assume other skills exist" guidance, Matt
Pocock's shared-artifact skill composition (`CONTEXT.md` / ADR seams), and the
process-before-implementation discipline in the Karpathy and Superpowers
ecosystems. A Super Skill-native re-expression, not a vendored copy.
