---
name: verification-loop
description: Use when work is about to be declared complete, fixed, ready to commit, ready to push, or production-ready and the claim needs fresh evidence from tests, builds, lint, manual checks, or source inspection.
---

# Verification Loop

## Gate

No completion claim without current evidence.

Before saying something works:

1. Identify the smallest command or inspection that proves it.
2. Run the full check, not a remembered or partial one.
3. Read the output and exit code.
4. Fix failures and repeat.
5. Report the evidence and known gaps.

## Evidence Map

| Claim | Evidence |
| --- | --- |
| Skill collection is valid | `bin/super-skill validate` exits 0 |
| CLI works | representative commands exit 0 |
| Package scripts work | package manager test/build output |
| Repo is ready to push | clean status plus committed changes |
| Visual UI is ready | browser screenshot and interaction checks |
| Security posture is acceptable | targeted review plus dependency scan when applicable |

## Reporting

Final reports should separate:

- Changed files
- Verification commands
- Remaining risks

Do not hide skipped checks. A named gap is safer than an implied pass.
