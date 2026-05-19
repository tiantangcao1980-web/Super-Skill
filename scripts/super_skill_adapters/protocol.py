"""AgentAdapter runtime protocol (Python mirror of agent-adapter.d.ts).

Spec: specs/current/agent-adapter-runtime.md
Canonical TS source: ../../skills/90-codex-patterns/dev-tool-adapter/references/agent-adapter.d.ts

The Python side ships:
  - dataclass mirrors of AgentDetection / AgentCapabilities / AdapterDetectResult
  - an `AgentAdapter` ABC with the same 5 method names as the TS interface
  - a `NullAdapter` (always returns detection=None) for tools we haven't wired
  - a `ClaudeCodeAdapter` with PATH-scan + version + config dir detect
  - a `CodexAdapter` with the same detect surface
  - REGISTRY mapping runtime id → adapter class

Only `detect()` and `capabilities()` are implemented in v1. `run()` /
`cancel()` / `resume()` raise NotImplementedError until the runner refactor
(spec: atom-runner.md Phase 2/3) lands.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Literal, Mapping, Optional


# ---------------------------------------------------------------------------
# Dataclass mirrors of the TS interface
# ---------------------------------------------------------------------------

AuthState = Literal["ok", "missing", "expired"]
PermissionMode = Literal["strict", "permissive", "none"]


@dataclass
class AgentDetection:
    executable_path: str
    version: str
    config_dir: Optional[str] = None
    skills_dir: Optional[str] = None
    auth_state: AuthState = "ok"

    def to_dict(self) -> dict:
        d = {
            "executablePath": self.executable_path,
            "version": self.version,
            "authState": self.auth_state,
        }
        if self.config_dir is not None:
            d["configDir"] = self.config_dir
        if self.skills_dir is not None:
            d["skillsDir"] = self.skills_dir
        return d


@dataclass
class AgentCapabilities:
    surgical_edit: bool
    native_skill_loading: bool
    streaming: bool
    resume: bool
    permission_mode: PermissionMode
    context_window_hint: Optional[int] = None

    def to_dict(self) -> dict:
        d = {
            "surgicalEdit": self.surgical_edit,
            "nativeSkillLoading": self.native_skill_loading,
            "streaming": self.streaming,
            "resume": self.resume,
            "permissionMode": self.permission_mode,
        }
        if self.context_window_hint is not None:
            d["contextWindowHint"] = self.context_window_hint
        return d


@dataclass
class AdapterDetectResult:
    id: str
    display_name: str
    detection: Optional[AgentDetection]
    capabilities: AgentCapabilities
    recommendation: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "displayName": self.display_name,
            "detection": self.detection.to_dict() if self.detection else None,
            "capabilities": self.capabilities.to_dict(),
            "recommendation": self.recommendation,
        }


# ---------------------------------------------------------------------------
# Abstract base + concrete adapters (detect-only in v1)
# ---------------------------------------------------------------------------

class AgentAdapter:
    """Abstract base. Concrete adapters override `detect()` and
    `capabilities()`. `run`/`cancel`/`resume` are reserved for the atom-runner
    Phase 2 refactor (see specs/current/atom-runner.md)."""

    id: str = ""
    display_name: str = ""

    def detect(self) -> Optional[AgentDetection]:
        raise NotImplementedError

    def capabilities(self) -> AgentCapabilities:
        raise NotImplementedError

    def recommendation(self, detection: Optional[AgentDetection]) -> str:
        if detection is None:
            return (f"{self.display_name} CLI not on PATH. Install it and rerun "
                    f"`bin/super-skill adapt --runtime {self.id} --detect-only`.")
        if detection.auth_state == "missing":
            return f"{self.display_name} found but auth not configured; run its login flow."
        if detection.auth_state == "expired":
            return f"{self.display_name} auth expired; refresh credentials."
        return f"{self.display_name} ready."

    # The three runner methods are intentional NotImplemented stubs in v1.
    # The TS interface declares them; the Python mirror keeps the same shape
    # so future implementations don't have to add new names.
    def run(self, params: Mapping) -> Iterator[dict]:  # noqa: D401
        raise NotImplementedError("run() lands in atom-runner Phase 2/3.")

    def cancel(self, run_id: str) -> None:
        raise NotImplementedError("cancel() lands in atom-runner Phase 2/3.")

    def resume(self, run_id: str, message: str) -> Iterator[dict]:
        raise NotImplementedError("resume() lands in atom-runner Phase 2/3.")


def _run_version(executable: str) -> str:
    """Best-effort `<exe> --version` capture; tolerates exotic CLIs."""
    try:
        proc = subprocess.run(
            [executable, "--version"],
            capture_output=True, text=True, timeout=5, check=False,
        )
        text = (proc.stdout or proc.stderr).splitlines()
        return text[0].strip() if text else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


class NullAdapter(AgentAdapter):
    """Always reports detection=None. Used in tests and as a fallback so the
    registry never raises on unknown runtime ids."""

    id = "null"
    display_name = "Null"

    def detect(self) -> Optional[AgentDetection]:
        return None

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities(
            surgical_edit=False,
            native_skill_loading=False,
            streaming=False,
            resume=False,
            permission_mode="none",
        )


class ClaudeCodeAdapter(AgentAdapter):
    id = "claude-code"
    display_name = "Claude Code"

    def detect(self) -> Optional[AgentDetection]:
        # Claude Code ships as either `claude` or `claude-code`.
        for exe_name in ("claude-code", "claude"):
            exe = shutil.which(exe_name)
            if exe:
                config_dir = Path.home() / ".claude"
                skills_dir = config_dir / "skills"
                auth: AuthState = "ok"
                # Lightweight heuristic: presence of config + a token file imply auth.
                if not config_dir.exists():
                    auth = "missing"
                return AgentDetection(
                    executable_path=exe,
                    version=_run_version(exe),
                    config_dir=str(config_dir) if config_dir.exists() else None,
                    skills_dir=str(skills_dir) if skills_dir.exists() else None,
                    auth_state=auth,
                )
        return None

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities(
            surgical_edit=True,
            native_skill_loading=True,
            streaming=True,
            resume=True,
            permission_mode="strict",
            context_window_hint=200_000,
        )


class CodexAdapter(AgentAdapter):
    id = "codex"
    display_name = "Codex CLI"

    def detect(self) -> Optional[AgentDetection]:
        exe = shutil.which("codex")
        if not exe:
            return None
        config_dir = Path.home() / ".codex"
        skills_dir = config_dir / "skills"
        auth: AuthState = "ok" if config_dir.exists() else "missing"
        return AgentDetection(
            executable_path=exe,
            version=_run_version(exe),
            config_dir=str(config_dir) if config_dir.exists() else None,
            skills_dir=str(skills_dir) if skills_dir.exists() else None,
            auth_state=auth,
        )

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities(
            surgical_edit=True,
            native_skill_loading=True,
            streaming=True,
            resume=False,
            permission_mode="strict",
            context_window_hint=400_000,
        )


REGISTRY: dict[str, type[AgentAdapter]] = {
    NullAdapter.id: NullAdapter,
    ClaudeCodeAdapter.id: ClaudeCodeAdapter,
    CodexAdapter.id: CodexAdapter,
}


def detect_runtime(runtime_id: str) -> AdapterDetectResult:
    """Look up adapter by id (falls back to NullAdapter), run detect+capabilities,
    return a serializable AdapterDetectResult."""
    cls = REGISTRY.get(runtime_id, NullAdapter)
    adapter = cls()
    detection = adapter.detect()
    capabilities = adapter.capabilities()
    return AdapterDetectResult(
        id=adapter.id,
        display_name=adapter.display_name,
        detection=detection,
        capabilities=capabilities,
        recommendation=adapter.recommendation(detection),
    )
