# Runtime Memory Policy

Supported developer tools: Codex, Cursor, Trae, OpenCode, OpenClaw, and Claude Code.

Codex uses the plugin hook path. Tools without plugin support use the `agent-memory-dream-loop` fallback skill through generated rules or workspace guidance.

Controls:

- `capture_raw_prompt`: false
- `capture_raw_response`: false
- `auto_promote`: false
- `require_review`: true
- `deduplicate`: true

Every memory or skill update is a candidate until review verifies source, scope, date, expiry, and evidence.
