from __future__ import annotations


RUNTIMES = ("Codex", "Cursor", "Trae", "OpenCode", "OpenClaw", "Claude Code")


def memory_policy(runtime: str) -> dict:
    if runtime not in RUNTIMES:
        raise ValueError(f"unsupported runtime: {runtime}")
    surface = "plugin hook" if runtime == "Codex" else "implicit fallback skill"
    return {
        "runtime": runtime,
        "surface": surface,
        "fallback_skill": "agent-memory-dream-loop",
        "capture_raw_prompt": False,
        "capture_raw_response": False,
        "auto_promote": False,
        "require_review": True,
        "deduplicate": True,
    }


def all_runtime_policies() -> list[dict]:
    return [memory_policy(runtime) for runtime in RUNTIMES]
