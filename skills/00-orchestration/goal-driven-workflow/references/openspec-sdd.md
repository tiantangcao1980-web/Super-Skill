# OpenSpec / SDD Adapter

OpenSpec-style SDD is a strong source for goal contracts because it turns chat intent into files that can be counted, tested, and archived.

## Expected Artifacts

For `openspec/changes/<change>/`, look for:

- `proposal.md`: why and what changes
- `design.md`: technical approach
- `tasks.md`: implementation checklist
- `specs/`: requirements and scenarios

## First Action Pattern

For SDD goals, start with a read/report action before edits:

```text
First action: read openspec/changes/<change>/proposal.md, design.md, tasks.md, specs/, and AGENTS.md if present; report file/task/requirement counts. Wait for acknowledgment before implementation.
```

This catches missing files, stale specs, and context loading failures early.

## Done When Mapping

Map each artifact to evidence:

- each task in `tasks.md` is checked off with a changed file or commit reference
- each SHALL has a passing test name
- each GIVEN/WHEN/THEN scenario has unit, integration, or e2e coverage
- implementation commands pass with exit code 0
- docs/changelog/spec archive is updated when required

## Stop If Mapping

Typical SDD stop conditions:

- two SHALLs conflict
- a task requires a path outside Scope
- a MUST NOT path appears in `git diff --name-only`
- a new dependency or secret is required
- existing tests fail and the only obvious fix is weakening tests

## Completion Audit

Do not treat `tasks.md` checkboxes alone as completion. The completion audit must inspect the actual files, tests, command output, and spec archive state.
