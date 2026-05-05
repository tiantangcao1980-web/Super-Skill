# Super Skill MCP Server

A minimal stdlib-only MCP (Model Context Protocol) server that exposes
`bin/super-skill autopilot`, `resume`, and `llm-eval` as MCP tools.

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

All three accept `provider: "stub" | "anthropic"`. Stub is offline & deterministic.
Anthropic requires `ANTHROPIC_API_KEY` in the server's environment.

## Smoke test

```bash
# Send an initialize + tools/list + tools/call dialogue to the server:
python3 scripts/mcp_server.py < tests/sample_dialogue.jsonl
```

The server is JSON-RPC 2.0 over stdio. Each input line is one request; each
output line is one response.
