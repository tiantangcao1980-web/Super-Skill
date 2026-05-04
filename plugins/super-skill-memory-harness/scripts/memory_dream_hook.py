#!/usr/bin/env python3
"""Codex hook for Super Skill memory/dream replay.

The hook intentionally captures metadata and review candidates only. It never
stores raw prompt or assistant text, because durable memory must be promoted by
evidence and review rather than by transcript hoarding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECRET_HINT_RE = re.compile(
    r"(?i)(api[_-]?key|secret|token|password|passwd|private[_-]?key|authorization|credential)"
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_hook_input() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def redact_value(value: Any) -> Any:
    if isinstance(value, str):
        if SECRET_HINT_RE.search(value):
            return "[redacted]"
        return value[:300]
    if isinstance(value, dict):
        return {k: ("[redacted]" if SECRET_HINT_RE.search(str(k)) else redact_value(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_value(item) for item in value[:20]]
    return value


def memory_root(payload: dict[str, Any]) -> Path:
    if os.environ.get("SUPER_SKILL_MEMORY_ROOT"):
        return Path(os.environ["SUPER_SKILL_MEMORY_ROOT"]).expanduser()
    cwd = Path(str(payload.get("cwd") or os.getcwd())).expanduser()
    return cwd / ".super-skill" / "memory"


def safe_metadata(payload: dict[str, Any], event: str) -> dict[str, Any]:
    transcript = payload.get("transcript_path")
    transcript_name = Path(str(transcript)).name if transcript else None
    return {
        "event": event,
        "hook_event_name": payload.get("hook_event_name"),
        "session_id": payload.get("session_id"),
        "cwd": payload.get("cwd"),
        "model": payload.get("model"),
        "source": payload.get("source"),
        "transcript_name": transcript_name,
        "captured_at": now_iso(),
    }


def digest(data: dict[str, Any]) -> str:
    stable = json.dumps(data, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]


def append_trace(root: Path, metadata: dict[str, Any]) -> Path:
    traces = root / "traces"
    traces.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = traces / f"{day}.jsonl"
    path.open("a", encoding="utf-8").write(json.dumps(redact_value(metadata), ensure_ascii=False) + "\n")
    return path


def write_candidate(root: Path, metadata: dict[str, Any]) -> Path | None:
    max_candidates = int(os.environ.get("SUPER_SKILL_MEMORY_MAX_CANDIDATES", "3"))
    inbox = root / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    existing = sorted(inbox.glob(f"{day}-*.md"))
    if len(existing) >= max_candidates:
        return None

    trace_id = digest(metadata)
    path = inbox / f"{day}-{trace_id}.md"
    if path.exists():
        return path

    body = f"""Type: episodic
Scope: project
Source: super-skill-memory-harness hook
Date: {metadata["captured_at"]}
Claim: A Codex session reached {metadata["event"]}; review whether any verified lesson should become memory, an eval, or a skill patch.
Evidence: trace_id={trace_id}; cwd={metadata.get("cwd")}; model={metadata.get("model")}; transcript_name={metadata.get("transcript_name")}
Use when: The completed work revealed a reusable procedure, repeated failure, user correction, or tool/runtime constraint.
Do not use when: The lesson is unverified, secret-bearing, private, one-off, stale, or already covered by an existing skill.
Expiry: review within 14 days
Promotion target: semantic | procedural | evaluation | negative | rejected
Verification: run bin/super-skill triggers --json, audit --json, and the relevant project tests before promotion.
"""
    path.write_text(body, encoding="utf-8")
    return path


def session_start(payload: dict[str, Any]) -> dict[str, Any]:
    root = memory_root(payload)
    metadata = safe_metadata(payload, "session-start")
    append_trace(root, metadata)
    return {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "Super Skill memory harness is active. Keep raw transcript content out of durable memory; "
                "use agent-memory-dream-loop only for verified, deduplicated, reviewable lessons."
            ),
        },
    }


def stop(payload: dict[str, Any]) -> dict[str, Any]:
    root = memory_root(payload)
    metadata = safe_metadata(payload, "stop")
    trace_path = append_trace(root, metadata)
    candidate = write_candidate(root, metadata)
    if candidate is None:
        message = "Super Skill memory harness skipped candidate creation because the per-session/day limit was reached."
    else:
        message = f"Super Skill memory candidate captured for review: {candidate}"
    return {
        "continue": True,
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": f"Memory trace written to {trace_path}. Promote only after review and verification.",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", choices=["session-start", "stop"], required=True)
    args = parser.parse_args(argv)

    if os.environ.get("SUPER_SKILL_MEMORY_DISABLED") == "1":
        return 0

    payload = read_hook_input()
    try:
        out = session_start(payload) if args.event == "session-start" else stop(payload)
    except Exception as exc:  # pragma: no cover - hook boundary must fail open
        out = {"continue": True, "systemMessage": f"Super Skill memory hook failed open: {exc}"}
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
