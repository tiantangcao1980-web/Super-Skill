# Goal-Driven Delivery

This fixture validates that Super Skill can support Codex `/goal` style long-running work without losing the existing Ralph Loop and code-simplifier strengths.

Expected workflow:

1. Use `goal-driven-workflow` to turn a fuzzy request into a scoped goal contract.
2. Use OpenSpec or another SDD artifact source so proposal, specs, design, and tasks are visible outside chat.
3. Use a token budget, artifact-backed Done when items, and mechanically detectable Stop if guards.
4. Implement with `ralph-loop` so each slice has PLAN, EXECUTE, VERIFY, DECIDE, and distance to the original goal.
5. Run `code-simplifier` only after verification is green.
6. Finish with `output-quality-gate` and `verification-loop` so every claim maps to evidence.
7. Send only verified, deduplicated lessons to `agent-memory-dream-loop`.

Required phrases: token budget, Stop if, Done when, OpenSpec, Ralph Loop, code-simplifier, evidence, memory.
