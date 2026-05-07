#!/usr/bin/env python3
"""Minimal MCP server that exposes Super Skill commands as tools.

This is an intentionally tiny, stdlib-only implementation of the Model Context
Protocol over stdio (JSON-RPC 2.0). It is sufficient to be loaded by Claude
Desktop / Claude Code / Cursor / any MCP-aware client and call:

  - autopilot(prompt, provider="stub", project=".", run_id=None, ...)
  - resume(project=".", run_id=None, list=False, ...)
  - llm_eval(prompt=None, provider="stub")
  - design_preflight(project=".", strict=False, max_findings=50)
  - design_extract(project=".", write_sidecar=None, write_design=None)
  - design_live(project=".", target_url=None, output=None)
  - design_capture(project=".", url, screenshot=None, report=None, dry_run=False)
  - design_audit(project=".", max_findings=200)

The tools wrap `bin/super-skill` via subprocess. We deliberately do not
re-implement the CLI here — the canonical surface stays the CLI so behavior is
identical for human and MCP clients.

Protocol notes (subset of MCP we implement):
  - initialize → {protocolVersion, capabilities, serverInfo}
  - notifications/initialized (no reply)
  - tools/list → {tools: [...]}
  - tools/call → {content: [{type:"text", text:"..."}], isError?}
  - shutdown → {} (graceful close)

Anything else returns method-not-found per JSON-RPC.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2].parent  # plugins/<name>/scripts/ -> repo root
SUPER_SKILL_BIN = REPO_ROOT / "bin" / "super-skill"
SCRIPT_PATH = REPO_ROOT / "scripts" / "super_skill.py"

PROTOCOL_VERSION = "2024-11-05"


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def reply(req_id: Any, result: dict | None = None, error: dict | None = None) -> None:
    out: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result or {}
    emit(out)


def call_super_skill(argv: list[str], timeout: int = 120) -> dict:
    """Subprocess into bin/super-skill, return parsed JSON if --json was passed."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *argv, "--json"],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    try:
        body = json.loads(proc.stdout)
    except json.JSONDecodeError:
        body = {"ok": False, "error": {"code": "BAD_OUTPUT", "stdout_tail": proc.stdout[-400:], "stderr_tail": proc.stderr[-400:]}}
    body["_returncode"] = proc.returncode
    return body


TOOLS = [
    {
        "name": "autopilot",
        "description": (
            "Run the Super Skill autonomous closed-loop harness end-to-end "
            "(intent → spec → design → ralph-loop impl → simplifier → quality gate "
            "→ memory candidate). Produces checkpointed artifacts under "
            "<project>/.super-skill/autopilot/<run-id>/. Use 'stub' provider for "
            "deterministic offline runs; use 'anthropic' (env ANTHROPIC_API_KEY) for "
            "real LLM."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "User request that drives the run"},
                "provider": {"type": "string", "enum": ["auto", "stub", "anthropic"], "default": "stub"},
                "project": {"type": "string", "default": ".", "description": "Workspace root"},
                "run_id": {"type": "string", "description": "Optional explicit run id"},
                "max_ralph_rounds": {"type": "integer", "default": 20},
                "skip": {"type": "string", "description": "Comma-separated phase ids to skip"},
                "force": {"type": "boolean", "default": False},
                "dry_run": {"type": "boolean", "default": False},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "resume",
        "description": "Resume the latest (or named) autopilot run. With list=true, only report pending vs completed phases.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": "."},
                "run_id": {"type": "string"},
                "list": {"type": "boolean", "default": False},
                "provider": {"type": "string", "enum": ["auto", "stub", "anthropic"], "default": "stub"},
                "max_ralph_rounds": {"type": "integer", "default": 20},
                "skip": {"type": "string"},
                "dry_run": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "llm_eval",
        "description": "Run a real (or stubbed) intent-contract → implementation → output-quality-gate round trip and report token usage + grader results.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "provider": {"type": "string", "enum": ["auto", "stub", "anthropic"], "default": "stub"},
                "show_outputs": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "design_audit",
        "description": "Scan frontend files for deterministic AI design anti-patterns and design quality risks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": ".", "description": "File or directory to scan"},
                "max_findings": {"type": "integer", "default": 200},
                "fail_on_findings": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "design_preflight",
        "description": "Check PRODUCT/DESIGN context, shape brief, tokens, visual references, and anti-pattern readiness before UI mutation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": ".", "description": "Project root or frontend surface to check"},
                "max_findings": {"type": "integer", "default": 50},
                "strict": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "design_extract",
        "description": "Extract design tokens, utility classes, component signals, and an optional DESIGN.md draft from frontend files.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": ".", "description": "Project root or frontend surface to scan"},
                "max_items": {"type": "integer", "default": 16},
                "write_sidecar": {"type": "string", "description": "Optional JSON sidecar output path"},
                "write_design": {"type": "string", "description": "Optional generated DESIGN.md draft output path"},
                "force": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "design_live",
        "description": "Generate a browser live design panel with overlay script, computed-style inspection, and CSS-variable variants.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": ".", "description": "Project root or frontend surface to summarize"},
                "target_url": {"type": "string", "description": "Optional URL the overlay should be used against"},
                "output": {"type": "string", "description": "Optional path for generated live panel HTML"},
                "write_extension": {"type": "string", "description": "Optional directory for an unpacked Chrome extension bundle"},
                "max_items": {"type": "integer", "default": 8},
                "force": {"type": "boolean", "default": False},
                "include_html": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "design_capture",
        "description": "Inject the design live overlay in a real Playwright browser session and capture screenshot + computed-style report.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": ".", "description": "Project root used as the capture working directory"},
                "url": {"type": "string", "description": "URL to open before injecting the overlay"},
                "screenshot": {"type": "string", "description": "Optional screenshot output path"},
                "report": {"type": "string", "description": "Optional computed-style report output path"},
                "runner": {"type": "string", "description": "Optional path to write the generated Playwright runner"},
                "viewport": {"type": "string", "default": "1440x900"},
                "timeout_ms": {"type": "integer", "default": 30000},
                "wait_until": {"type": "string", "enum": ["load", "domcontentloaded", "networkidle"], "default": "networkidle"},
                "storage_state": {"type": "string", "description": "Optional Playwright storage-state JSON path"},
                "browser_channel": {"type": "string", "description": "Optional Playwright Chromium channel, for example chrome"},
                "headed": {"type": "boolean", "default": False},
                "dry_run": {"type": "boolean", "default": False},
                "force": {"type": "boolean", "default": False},
            },
            "required": ["url"],
        },
    },
]


def build_argv_autopilot(args: dict) -> list[str]:
    argv = ["autopilot", "--prompt", str(args.get("prompt", ""))]
    argv += ["--provider", args.get("provider", "stub")]
    argv += ["--project", args.get("project", ".")]
    if args.get("run_id"): argv += ["--run-id", args["run_id"]]
    if args.get("max_ralph_rounds") is not None: argv += ["--max-ralph-rounds", str(args["max_ralph_rounds"])]
    if args.get("skip"): argv += ["--skip", args["skip"]]
    if args.get("force"): argv += ["--force"]
    if args.get("dry_run"): argv += ["--dry-run"]
    return argv


def build_argv_resume(args: dict) -> list[str]:
    argv = ["resume", "--project", args.get("project", ".")]
    argv += ["--provider", args.get("provider", "stub")]
    if args.get("run_id"): argv += ["--run-id", args["run_id"]]
    if args.get("list"): argv += ["--list"]
    if args.get("max_ralph_rounds") is not None: argv += ["--max-ralph-rounds", str(args["max_ralph_rounds"])]
    if args.get("skip"): argv += ["--skip", args["skip"]]
    if args.get("dry_run"): argv += ["--dry-run"]
    return argv


def build_argv_llm_eval(args: dict) -> list[str]:
    argv = ["llm-eval", "--provider", args.get("provider", "stub")]
    if args.get("prompt"): argv += ["--prompt", args["prompt"]]
    if args.get("show_outputs"): argv += ["--show-outputs"]
    return argv


def build_argv_design_audit(args: dict) -> list[str]:
    argv = ["design-audit", "--project", args.get("project", ".")]
    if args.get("max_findings") is not None:
        argv += ["--max-findings", str(args["max_findings"])]
    if args.get("fail_on_findings"):
        argv += ["--fail-on-findings"]
    return argv


def build_argv_design_preflight(args: dict) -> list[str]:
    argv = ["design-preflight", "--project", args.get("project", ".")]
    if args.get("max_findings") is not None:
        argv += ["--max-findings", str(args["max_findings"])]
    if args.get("strict"):
        argv += ["--strict"]
    return argv


def build_argv_design_extract(args: dict) -> list[str]:
    argv = ["design-extract", "--project", args.get("project", ".")]
    if args.get("max_items") is not None:
        argv += ["--max-items", str(args["max_items"])]
    if args.get("write_sidecar"):
        argv += ["--write-sidecar", args["write_sidecar"]]
    if args.get("write_design"):
        argv += ["--write-design", args["write_design"]]
    if args.get("force"):
        argv += ["--force"]
    return argv


def build_argv_design_live(args: dict) -> list[str]:
    argv = ["design-live", "--project", args.get("project", ".")]
    if args.get("target_url"):
        argv += ["--target-url", args["target_url"]]
    if args.get("output"):
        argv += ["--output", args["output"]]
    if args.get("write_extension"):
        argv += ["--write-extension", args["write_extension"]]
    if args.get("max_items") is not None:
        argv += ["--max-items", str(args["max_items"])]
    if args.get("force"):
        argv += ["--force"]
    if args.get("include_html"):
        argv += ["--include-html"]
    return argv


def build_argv_design_capture(args: dict) -> list[str]:
    argv = ["design-capture", "--project", args.get("project", ".")]
    if args.get("url"):
        argv += ["--url", args["url"]]
    if args.get("screenshot"):
        argv += ["--screenshot", args["screenshot"]]
    if args.get("report"):
        argv += ["--report", args["report"]]
    if args.get("runner"):
        argv += ["--runner", args["runner"]]
    if args.get("viewport"):
        argv += ["--viewport", args["viewport"]]
    if args.get("timeout_ms") is not None:
        argv += ["--timeout-ms", str(args["timeout_ms"])]
    if args.get("wait_until"):
        argv += ["--wait-until", args["wait_until"]]
    if args.get("storage_state"):
        argv += ["--storage-state", args["storage_state"]]
    if args.get("browser_channel"):
        argv += ["--browser-channel", args["browser_channel"]]
    if args.get("headed"):
        argv += ["--headed"]
    if args.get("dry_run"):
        argv += ["--dry-run"]
    if args.get("force"):
        argv += ["--force"]
    return argv


TOOL_DISPATCH = {
    "autopilot": build_argv_autopilot,
    "resume": build_argv_resume,
    "llm_eval": build_argv_llm_eval,
    "design_audit": build_argv_design_audit,
    "design_preflight": build_argv_design_preflight,
    "design_extract": build_argv_design_extract,
    "design_live": build_argv_design_live,
    "design_capture": build_argv_design_capture,
}


def handle_tools_call(req_id: Any, params: dict) -> None:
    name = params.get("name")
    args = params.get("arguments") or {}
    builder = TOOL_DISPATCH.get(name)
    if not builder:
        reply(req_id, error={"code": -32601, "message": f"unknown tool: {name}"})
        return
    try:
        argv = builder(args)
    except Exception as exc:
        reply(req_id, error={"code": -32602, "message": f"invalid arguments: {exc}"})
        return
    body = call_super_skill(argv)
    is_error = not bool(body.get("ok"))
    text = json.dumps(body, ensure_ascii=False, indent=2)
    reply(req_id, result={"content": [{"type": "text", "text": text}], "isError": is_error})


def handle_request(message: dict) -> None:
    method = message.get("method")
    req_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        reply(req_id, result={
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "super-skill-mcp-server", "version": "0.1.0"},
        })
        return
    if method == "notifications/initialized":
        return  # no reply
    if method == "tools/list":
        reply(req_id, result={"tools": TOOLS})
        return
    if method == "tools/call":
        handle_tools_call(req_id, params)
        return
    if method == "shutdown":
        reply(req_id, result={})
        return
    if method == "ping":
        reply(req_id, result={})
        return

    if req_id is None:
        return  # notification we don't handle
    reply(req_id, error={"code": -32601, "message": f"method not found: {method}"})


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            emit({"jsonrpc": "2.0", "error": {"code": -32700, "message": f"parse error: {exc}"}, "id": None})
            continue
        try:
            handle_request(message)
        except Exception as exc:  # pragma: no cover - defensive
            emit({"jsonrpc": "2.0", "id": message.get("id"), "error": {"code": -32603, "message": f"internal error: {exc}"}})
    return 0


if __name__ == "__main__":
    sys.exit(main())
