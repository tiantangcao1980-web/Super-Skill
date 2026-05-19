"""Super Skill agent-adapter runtime registry.

Spec: specs/current/agent-adapter-runtime.md
Canonical TS interface: skills/90-codex-patterns/dev-tool-adapter/references/agent-adapter.d.ts
"""

from .protocol import (
    AgentDetection,
    AgentCapabilities,
    AgentAdapter,
    NullAdapter,
    ClaudeCodeAdapter,
    CodexAdapter,
    AdapterDetectResult,
    REGISTRY,
    detect_runtime,
)

__all__ = [
    "AgentDetection",
    "AgentCapabilities",
    "AgentAdapter",
    "NullAdapter",
    "ClaudeCodeAdapter",
    "CodexAdapter",
    "AdapterDetectResult",
    "REGISTRY",
    "detect_runtime",
]
