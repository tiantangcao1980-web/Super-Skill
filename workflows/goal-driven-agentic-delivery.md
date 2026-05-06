# Goal-Driven Agentic Delivery

Use this workflow when a task is too large for a single prompt but should not become an unmanaged autonomous run.

## 1. Clarify

Use `intent-contract` or Plan mode to turn the user request into:

- target user or system outcome
- explicit scope
- constraints and forbidden paths
- acceptance criteria
- verification commands

## 2. Externalize Specs

For product or feature work, prefer OpenSpec or `product-spec`:

- proposal
- specs / requirements
- design
- tasks

The goal should point at files, not rely on chat memory.

## 3. Build Goal Contract

Generate a goal with:

```bash
bin/super-skill goal --objective "<concrete objective>" \
  --scope "<path or subsystem>" \
  --done "<artifact-backed acceptance item>" \
  --done "<command exits 0>" \
  --done "<test name covers requirement>" \
  --stop-if "<mechanically detectable blocker>" \
  --stop-if "<MUST NOT path appears in diff>" \
  --stop-if "<new dependency required>" \
  --budget 120000
```

Paste the rendered command into Codex `/goal`.

## 4. Execute in Ralph Slices

Inside the goal, use `ralph-loop` for each implementation slice:

- quote the goal anchor
- plan one minimal step
- execute
- verify
- update distance to Done when checklist
- continue or stop

## 5. Simplify After Green

Run `code-simplifier` only after tests and goal evidence are green:

- remove temporary scaffolding
- delete dead code
- inline unjustified abstractions
- preserve public API and behavior

## 6. Audit Completion

Before marking complete:

- map every goal requirement to evidence
- inspect actual files and command output
- confirm tests cover the requirement, not just unrelated code
- report missing or weak evidence instead of claiming completion

## 7. Learn Safely

Use `agent-memory-dream-loop` only for verified lessons:

- no raw prompt or response content
- deduplicate before promotion
- keep scope, source, date, and verification evidence
- prefer skill patch or eval when the lesson is procedural
