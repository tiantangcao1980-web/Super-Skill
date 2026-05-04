# OpenCLI Essentials

Good CLIs are discoverable, scriptable, and stable.

## Required Behaviors

- `--help` on every command.
- `--json` for machine-readable output.
- Stable exit codes: `0` success, `1` runtime error, `2` usage error, `3` dependency missing, `130` interrupted.
- Errors include code, message, hint, and request id when JSON mode is used.
- No interactive prompt when `--yes`, `--json`, or CI mode is active.

## Command Shape

Use nouns for resource families and verbs for actions:

```text
tool list
tool describe --json
tool install <name> --dry-run
tool validate
```
