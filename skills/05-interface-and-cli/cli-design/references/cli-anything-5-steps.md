# CLI-Anything Five Steps

1. Identify the repeatable capability.
2. Define inputs, outputs, errors, and exit codes.
3. Make the happy path non-interactive.
4. Add `--json` and `--dry-run` where automation needs them.
5. Write a `describe --json` surface so other agents can discover it.

## Quality Bar

The CLI should be usable by both a human in a terminal and an agent in a workflow without hidden state or guesswork.
