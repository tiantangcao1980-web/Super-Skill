---
name: checkpoint-rollback-safety
description: Use before risky AI-driven edits, cleanup, refactors, generated code changes, destructive commands, migrations, or parallel agent work where rollback evidence matters.
---

# Checkpoint And Rollback Safety

Fast agent edits need cheap recovery. Add a rollback path before the change, not after damage is discovered.

## Risk Signals

- destructive shell commands
- broad refactors or cleanup
- generated edits across many files
- schema migrations
- dependency updates
- production configuration changes
- parallel work on the same repo

## Safety Procedure

1. Inspect git status and identify unrelated user changes.
2. Create or confirm a checkpoint: git branch, worktree, shadow snapshot, backup, or dry-run artifact.
3. Lock current behavior with tests or captured outputs when behavior is not already protected.
4. Make the smallest reversible edit.
5. Run targeted verification before broad verification.
6. Record how to roll back and what would be lost.

## Rollback Contract

For risky work, final output must include:

- checkpoint or branch name
- files touched
- verification run
- known unverified areas
- rollback command or restore path when appropriate

## Do Not

- hide unrelated dirty worktree changes
- run destructive cleanup without a checkpoint
- treat generated code volume as evidence of progress
- claim safety without a restore path
