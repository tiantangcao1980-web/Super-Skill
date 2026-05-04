# Cross-Runtime Memory Bootstrap

## User Goal

Install Super Skill into multiple AI developer tools while keeping one canonical memory/dream behavior. Codex should use plugin hooks; tools without plugin support should use the automatic fallback skill.

## Expected Workflow

Runtime adapter -> selective install profile -> Codex memory plugin dry run -> non-plugin fallback trigger policy -> skill lifecycle controls -> audit.

## Acceptance Evidence

- The plugin is hook-only and does not duplicate the canonical memory skill.
- The fallback skill is `agent-memory-dream-loop`.
- Trigger controls forbid raw prompt/response capture and automatic promotion.
- Cursor, Trae, OpenCode, OpenClaw, Claude Code, and Codex are represented in the runtime fallback policy.
