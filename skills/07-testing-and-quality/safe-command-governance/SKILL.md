---
name: safe-command-governance
description: Audit, document, and replace risky shell/git/install commands such as curl-pipe-shell, rm -rf, git reset --hard, chmod 777, or forceful installers. Use before adding examples, install docs, cleanup scripts, or agent-executable commands.
---

# Safe Command Governance

Agents copy commands. Treat every command in docs, scripts, and examples as
potentially executable.

## Risky Command Classes

| Pattern | Risk | Safer default |
| --- | --- | --- |
| `curl ... | sh` / `curl ... | bash` | Executes unaudited remote code | Download to a file, inspect, verify checksum, then run |
| `rm -rf <path>` | Irreversible data loss | Use trash/quarantine, explicit path checks, or dry-run first |
| `git reset --hard` | Discards local work | Use `git status`, stash/branch backup, or `git restore` on named files |
| `chmod 777` | Grants broad write/execute access | Use least-privilege mode and explain owner/group |
| Forceful install overwrite | Destroys local customizations | Preview plan, conflict list, backup, `--force` opt-in |

## Documentation Rule

Any risky command that remains must include:

```text
Danger: <what can be lost or executed>
Safer alternative: <copy-pastable safer flow>
Use only when: <narrow condition>
```

Prefer replacing the risky command with the safer flow. Keep the risky form
only when it is the subject being explained or a known upstream command.

## Script Rule

Scripts that perform destructive actions must have:

- resolved absolute path checks
- refusal on empty, root, home, or repository root targets
- dry-run or preview mode when feasible
- explicit `--force` or equivalent user opt-in
- clear stderr message on refusal

## Audit Commands

```bash
bin/super-skill audit --json
rg -n "curl .*\\| *(sh|bash)|rm -rf|git reset --hard|chmod 777" README.md docs skills scripts vendor
```

## Review Output

Report:

- risky command locations
- whether each is an executable instruction, quoted warning, or generated data
- remediation status: replaced, annotated, accepted upstream/vendor, or blocked
- remaining risk

## Attribution

This skill strengthens Super Skill's safety gate after comparing with
MIT-licensed engineering-skill projects that emphasize small, reviewable,
agent-safe workflows.
