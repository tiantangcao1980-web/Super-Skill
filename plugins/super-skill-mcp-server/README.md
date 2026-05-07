# Super Skill MCP Server

A minimal stdlib-only MCP (Model Context Protocol) server that exposes
`bin/super-skill autopilot`, `resume`, `llm-eval`, `design-preflight`,
`design-extract`, and `design-audit` as MCP tools.

## Why

So Claude Desktop / Claude Code / Cursor / any MCP-aware client can call the
autonomous Super Skill harness directly, without the user typing the CLI:

> "run autopilot on this project with the prompt: build a todo CLI"

becomes a single MCP `tools/call` to the `autopilot` tool.

## Install (Claude Desktop / Claude Code)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
or the equivalent on your platform:

```json
{
  "mcpServers": {
    "super-skill": {
      "command": "python3",
      "args": [
        "/absolute/path/to/Super Skill/plugins/super-skill-mcp-server/scripts/mcp_server.py"
      ]
    }
  }
}
```

## Tools

| Tool | Purpose |
| --- | --- |
| `autopilot` | Run intent → spec → design → ralph-loop impl → simplifier → quality gate → memory candidate. Returns the run journal. |
| `resume` | Resume the latest (or named) autopilot run. With `list=true`, only show pending vs completed phases. |
| `llm_eval` | Run the contract → impl → gate round trip (used for testing the harness itself). |
| `design_preflight` | Check PRODUCT/DESIGN context, shape brief, tokens, visual references, and anti-pattern readiness before UI mutation. |
| `design_extract` | Extract design tokens, utility classes, component signals, and an optional DESIGN.md draft from frontend files. |
| `design_audit` | Scan frontend files for deterministic AI design anti-patterns and quality risks. |

The LLM-backed tools accept `provider: "stub" | "anthropic"`. Stub is offline
and deterministic. Anthropic requires `ANTHROPIC_API_KEY` in the server's
environment.

## Smoke test

```bash
# Send an initialize + tools/list + tools/call dialogue to the server:
python3 scripts/mcp_server.py < tests/sample_dialogue.jsonl
```

The server is JSON-RPC 2.0 over stdio. Each input line is one request; each
output line is one response.
