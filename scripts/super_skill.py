#!/usr/bin/env python3
"""Super Skill repository CLI.

The repository keeps skills organized by lifecycle directories, while agent
runtime directories usually expect a flat skill namespace. This CLI bridges the
two views without introducing external dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
VENDOR_ROOT = ROOT / "vendor" / "cowork"
CATALOG_ROOT = ROOT / "catalog"
MANIFEST_ROOT = ROOT / "manifests"
PLUGIN_ROOT = ROOT / "plugins"
EVALS_ROOT = ROOT / "evals"
LIVE_EVALS_ROOT = EVALS_ROOT / "live-projects"
MEMORY_PLUGIN_NAME = "super-skill-memory-harness"
AUTO_TRIGGER_POLICY_PATH = MANIFEST_ROOT / "auto-trigger-policy.json"
SKILL_LIFECYCLE_POLICY_PATH = MANIFEST_ROOT / "skill-lifecycle-policy.json"

EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2
EXIT_DEPENDENCY = 3

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

STAGES = {
    "00-orchestration": "Orchestration",
    "01-research": "Research",
    "02-analysis": "Analysis",
    "03-product": "Product",
    "04-design-system": "Design",
    "05-interface-and-cli": "Interface",
    "06-development": "Development",
    "07-testing-and-quality": "Quality",
    "08-delivery-and-growth": "Delivery",
    "09-operations-and-knowledge": "Operations",
    "90-codex-patterns": "Codex Patterns",
}

PROFILE_STAGE_PREFIXES = {
    "core": {
        "00-orchestration",
        "01-research",
        "02-analysis",
        "03-product",
        "04-design-system",
        "05-interface-and-cli",
        "07-testing-and-quality",
        "08-delivery-and-growth",
        "09-operations-and-knowledge",
        "90-codex-patterns",
    },
    "dev": {
        "05-interface-and-cli",
        "06-development",
        "07-testing-and-quality",
        "08-delivery-and-growth",
        "09-operations-and-knowledge",
        "90-codex-patterns",
    },
    "design": {"04-design-system", "07-testing-and-quality"},
    "hermes": set(STAGES),
    "all": set(STAGES),
}

PROFILE_SKILL_EXCLUDES = {
    "hermes": {
        # Hermes Agent already ships these as runtime primitives or tightly
        # integrated workflows. Keep Super Skill's adaptations for other
        # runtimes, but do not install them into Hermes by default.
        "checkpoint-rollback-safety",
        "durable-agent-board",
        "persistent-memory-curation",
        "prompt-cache-layering",
        "skill-evolution-loop",
        "toolset-sandbox-routing",
    },
}

COMPATIBILITY_LINKS = {
    "design-md": "resources/design-md",
    "designdna": "skills/04-design-system/designdna",
    "assets": "resources/designdna-assets",
    "playground": "resources/designdna-playground",
    "showcase": "resources/designdna-showcase",
    "packages/cli": "packages/designdna-cli",
}

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".ts",
    ".tsx",
    ".txt",
    ".yml",
    ".yaml",
}

SECRET_PATTERNS = {
    "private-key-block": re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{36,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "openai-api-key": re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"),
    "hardcoded-secret-assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|password|passwd|private[_-]?key)\b"
        r"\s*[:=]\s*[\"']?([A-Za-z0-9_./+=-]{24,})[\"']?"
    ),
}

RISKY_PATTERNS = {
    "rm-rf": re.compile(r"\brm\s+-rf\b"),
    "git-reset-hard": re.compile(r"\bgit\s+reset\s+--hard\b"),
    "curl-pipe-shell": re.compile(r"\bcurl\b[^\n|]*\|\s*(?:sh|bash)\b"),
    "chmod-777": re.compile(r"\bchmod\s+777\b"),
}

HARNESS_IGNORES = {".git", ".omx", "node_modules", "dist", "coverage", "__pycache__"}

HARNESS_CAPABILITIES = [
    {
        "id": "intent-context",
        "label": "Intent and context contracts",
        "patterns": [r"intent-contract", r"context-engineering", r"acceptance checks?", r"context pack"],
        "min_matches": 2,
        "paths": ["AGENTS.md", "docs", "workflows", "skills"],
        "recommendation": "Add intent-contract and context-engineering guidance before agent execution.",
    },
    {
        "id": "spec-workflow-design",
        "label": "Spec and workflow design",
        "patterns": [
            r"product-spec",
            r"spec-driven",
            r"PRD",
            r"acceptance criteria",
            r"AGENTS\.md",
            r"feature list",
            r"design-dev-flow",
        ],
        "min_matches": 2,
        "paths": ["AGENTS.md", "docs", "workflows", "skills"],
        "recommendation": "Turn product intent into executable specs, feature lists, and acceptance checks before implementation.",
    },
    {
        "id": "agent-legibility",
        "label": "Agent-legible architecture",
        "patterns": [r"monorepo", r"workspace", r"architecture", r"local integration", r"environment parity"],
        "min_matches": 2,
        "paths": ["AGENTS.md", "docs", "package.json", "pnpm-workspace.yaml", "turbo.json", "nx.json"],
        "recommendation": "Document service boundaries, local run commands, and integration checks agents can execute.",
    },
    {
        "id": "working-state-resume",
        "label": "Working state and resumability",
        "patterns": [
            r"durable-agent-board",
            r"working state",
            r"handoff summary",
            r"resume",
            r"checkpoint",
            r"session history",
            r"task state",
            r"human unblock",
        ],
        "min_matches": 2,
        "paths": ["AGENTS.md", "docs", "workflows", "skills"],
        "recommendation": "Persist task state, handoff summaries, checkpoints, and unblock decisions for long-running agent work.",
    },
    {
        "id": "tool-sandbox-policy",
        "label": "Tool, sandbox, and permission policy",
        "patterns": [
            r"toolset-sandbox-routing",
            r"tool boundary",
            r"tool access",
            r"sandbox",
            r"approval",
            r"permission",
            r"prompt injection",
            r"MCP",
            r"blocklist",
        ],
        "min_matches": 2,
        "paths": ["AGENTS.md", "docs", "workflows", "skills"],
        "recommendation": "Make tool access, sandbox level, prompt-injection handling, and irreversible-action gates explicit.",
    },
    {
        "id": "deterministic-ci",
        "label": "Deterministic CI validation",
        "patterns": [r"typecheck", r"lint", r"unit", r"integration", r"e2e", r"docker", r"audit"],
        "min_matches": 2,
        "paths": [".github/workflows", "package.json", "Makefile"],
        "recommendation": "Make typecheck, lint, tests, builds, e2e, and parity checks repeatable in CI.",
    },
    {
        "id": "eval-trace-benchmark",
        "label": "Agent evals, traces, and benchmarks",
        "patterns": [
            r"agent-eval-harness",
            r"\bevals?\b",
            r"trace",
            r"trajectory",
            r"benchmark",
            r"no-skill baseline",
            r"deterministic verifier",
            r"JSONL",
        ],
        "min_matches": 2,
        "paths": [".github/workflows", "docs", "workflows", "skills", "tests"],
        "recommendation": "Add repeatable agent-task evals with traces, deterministic verifiers, baselines, and benchmark mapping.",
    },
    {
        "id": "ai-review-gates",
        "label": "AI review gates",
        "patterns": [r"ai-review-gates", r"claude", r"coderabbit", r"security review", r"dependency scan", r"license"],
        "min_matches": 2,
        "paths": [".github", "docs", "skills", "AGENTS.md"],
        "recommendation": "Split PR review into code quality, security, dependency, and product-risk passes.",
    },
    {
        "id": "progressive-delivery",
        "label": "Progressive delivery and experiments",
        "patterns": [r"feature flag", r"statsig", r"launchdarkly", r"rollout", r"kill switch", r"A/B", r"rollback"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", ".github/workflows"],
        "recommendation": "Ship risky changes behind flags with rollout metrics, guardrails, and a kill decision rule.",
    },
    {
        "id": "observability-triage",
        "label": "Observability and triage loop",
        "patterns": [r"sentry", r"cloudwatch", r"datadog", r"opentelemetry", r"structured logs?", r"metrics", r"triage"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", ".github/workflows"],
        "recommendation": "Expose structured logs, metrics, errors, deploy events, and auto-created investigation tickets.",
    },
    {
        "id": "token-cost-control",
        "label": "Token, cost, and context efficiency",
        "patterns": [
            r"token-budgeting",
            r"prompt-cache-layering",
            r"token",
            r"cost",
            r"context-efficient",
            r"cache",
            r"compression",
        ],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "AGENTS.md", "README.md"],
        "recommendation": "Budget stable and volatile context separately, track cost-sensitive loops, and avoid repeated scans.",
    },
    {
        "id": "dev-tool-adaptation",
        "label": "Developer tool runtime adaptation",
        "patterns": [
            r"dev-tool-adapter",
            r"Cursor",
            r"Trae",
            r"OpenCode",
            r"OpenClaw",
            r"Claude Code",
            r"Codex",
            r"runtime adapter",
        ],
        "min_matches": 3,
        "paths": ["README.md", "docs", "workflows", "skills"],
        "recommendation": "Map canonical skills to each developer tool's native rule, skill, agent, and permission surfaces.",
    },
    {
        "id": "model-adaptation-contract",
        "label": "Model adaptation and output contracts",
        "patterns": [
            r"model-adaptation-contract",
            r"model profile",
            r"structured output",
            r"output schema",
            r"model routing",
            r"fallback policy",
            r"compatibility gate",
        ],
        "min_matches": 3,
        "paths": ["README.md", "docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Define provider-neutral model profiles, input contracts, output schemas, and eval gates.",
    },
    {
        "id": "memory-dream-loop",
        "label": "Memory and dream replay loop",
        "patterns": [
            r"agent-memory-dream-loop",
            r"dream loop",
            r"dream replay",
            r"episodic traces?",
            r"semantic memory",
            r"procedural memory",
            r"negative memory",
            r"memory candidates?",
        ],
        "min_matches": 3,
        "paths": ["README.md", "docs", "workflows", "skills"],
        "recommendation": "Turn verified experience into bounded memory, offline replay, skill patches, evals, and rejected lessons.",
    },
    {
        "id": "auto-trigger-governance",
        "label": "Automatic trigger governance",
        "patterns": [
            r"auto-trigger",
            r"automatic trigger",
            r"SessionStart",
            r"\bStop\b",
            r"trigger policy",
            r"fallback skill",
            r"controllable",
            r"opt-in",
        ],
        "min_matches": 3,
        "paths": ["README.md", "docs", "workflows", "skills", "manifests", "plugins"],
        "recommendation": "Define automatic trigger surfaces, control gates, and fallback skill behavior for runtimes without plugins.",
    },
    {
        "id": "output-quality",
        "label": "Output quality gate",
        "patterns": [r"output-quality-gate", r"verification-loop", r"evidence before claims", r"known gaps"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Require final outputs to map delivered artifacts back to user intent and verification evidence.",
    },
    {
        "id": "human-risk-governance",
        "label": "Human judgment and risk governance",
        "patterns": [r"human review", r"architect", r"operator", r"approval", r"product-risk", r"risk", r"judgment"],
        "min_matches": 2,
        "paths": ["AGENTS.md", "docs", "workflows", "skills"],
        "recommendation": "Define where humans judge product risk, architecture, security, taste, and irreversible decisions.",
    },
    {
        "id": "learning-loop",
        "label": "Learning and harness evolution",
        "patterns": [r"continuous-learning", r"skill-authoring-system", r"postmortem", r"lessons learned", r"runbook"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Convert repeated failures into tests, skills, docs, runbooks, or automation.",
    },
]

HERMES_CAPABILITIES = [
    {
        "id": "progressive-skill-disclosure",
        "label": "Progressive skill disclosure",
        "patterns": [r"progressive disclosure", r"skill-evolution-loop", r"skill-authoring-system", r"references/", r"scripts/"],
        "paths": ["README.md", "docs", "workflows", "skills"],
        "recommendation": "Keep skill discovery compact, load detailed references on demand, and evolve skills from evidence.",
    },
    {
        "id": "memory-curation",
        "label": "Bounded persistent memory curation",
        "patterns": [r"persistent-memory-curation", r"memory tiers", r"searchable history", r"durable facts", r"session history"],
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Separate durable memory, searchable history, project context, and procedural skills.",
    },
    {
        "id": "prompt-cache-layering",
        "label": "Prompt cache and context layering",
        "patterns": [r"prompt-cache-layering", r"stable prompt", r"ephemeral", r"frozen", r"token-budgeting"],
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Separate stable prompt layers from volatile task evidence and preserve exact blockers through compression.",
    },
    {
        "id": "toolset-sandbox-routing",
        "label": "Toolset and sandbox routing",
        "patterns": [r"toolset-sandbox-routing", r"tool access", r"sandbox", r"worktree", r"approval", r"rollback"],
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Map task capability needs to minimal toolsets, sandboxes, approvals, and rollback gates.",
    },
    {
        "id": "durable-agent-board",
        "label": "Durable agent work board",
        "patterns": [r"durable-agent-board", r"durable board", r"work queue", r"kanban", r"human unblock", r"idempotency"],
        "paths": ["docs", "workflows", "skills"],
        "recommendation": "Use durable task state for multi-role, retryable, human-in-the-loop, or restart-safe work.",
    },
    {
        "id": "checkpoint-rollback",
        "label": "Checkpoint and rollback safety",
        "patterns": [r"checkpoint-rollback-safety", r"checkpoint", r"rollback", r"shadow", r"worktree"],
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Add checkpoints, worktrees, dry runs, or restore paths before risky agent-driven edits.",
    },
    {
        "id": "scheduled-agent-ops",
        "label": "Scheduled agent operations",
        "patterns": [r"cron", r"scheduled", r"observability-triage-loop", r"daily", r"automation"],
        "paths": ["docs", "workflows", "skills", ".github/workflows"],
        "recommendation": "Turn recurring checks into scheduled agent jobs with bounded context and delivery targets.",
    },
    {
        "id": "provider-aux-routing",
        "label": "Provider and auxiliary model routing",
        "patterns": [
            r"agent-routing",
            r"provider",
            r"auxiliary",
            r"model routing",
            r"fallback",
            r"model-adaptation-contract",
        ],
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Route main, auxiliary, review, and low-risk tasks to appropriate models with fallback policy.",
    },
    {
        "id": "runtime-adapters",
        "label": "Runtime adapters for developer tools",
        "patterns": [r"dev-tool-adapter", r"Cursor", r"Trae", r"OpenCode", r"OpenClaw", r"Claude Code", r"Codex"],
        "paths": ["README.md", "docs", "workflows", "skills"],
        "recommendation": "Keep one canonical skill body and generate thin wrappers for each agent runtime.",
    },
    {
        "id": "session-search-history",
        "label": "Session search and history recall",
        "patterns": [r"session search", r"session history", r"searchable history", r"past conversations?", r"recall"],
        "paths": ["docs", "workflows", "skills"],
        "recommendation": "Keep detailed episodic recall outside always-on memory and retrieve it on demand.",
    },
    {
        "id": "learning-loop",
        "label": "Closed learning loop",
        "patterns": [r"skill-evolution-loop", r"continuous-learning", r"learning loop", r"lessons learned", r"postmortem"],
        "paths": ["README.md", "docs", "workflows", "skills"],
        "recommendation": "Convert repeated successes and failures into memory, docs, tests, skills, or automation.",
    },
]

MEMORY_CAPABILITIES = [
    {
        "id": "episodic-traces",
        "label": "Episodic trace capture",
        "patterns": [r"episodic traces?", r"logs", r"diffs", r"commands", r"errors", r"review notes"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Capture raw session evidence outside always-on context and retrieve it by task, file, or failure mode.",
    },
    {
        "id": "semantic-memory",
        "label": "Semantic memory with provenance",
        "patterns": [r"semantic memory", r"durable facts", r"decisions", r"source", r"date", r"scope"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Store verified facts and decisions with source, date, scope, and expiry.",
    },
    {
        "id": "procedural-memory",
        "label": "Procedural memory through skills",
        "patterns": [r"procedural memory", r"skills", r"runbooks?", r"scripts", r"checklists?", r"skill-authoring-system"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "README.md"],
        "recommendation": "Promote repeated useful procedures into skills, runbooks, scripts, or checklists.",
    },
    {
        "id": "evaluation-memory",
        "label": "Evaluation and benchmark memory",
        "patterns": [r"evaluation memory", r"evals?", r"benchmarks?", r"rubric", r"regression", r"baseline"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "tests", ".github/workflows"],
        "recommendation": "Keep regression examples, rubrics, and baselines near model and skill changes.",
    },
    {
        "id": "negative-memory",
        "label": "Negative memory and rejected lessons",
        "patterns": [r"negative memory", r"rejected", r"anti-pattern", r"failure mode", r"do not use"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Store short rejected approaches and anti-patterns to prevent repeated waste.",
    },
    {
        "id": "dream-replay",
        "label": "Offline dream replay loop",
        "patterns": [r"dream loop", r"dream replay", r"offline replay", r"simulate", r"memory candidates?", r"baseline comparison"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills"],
        "recommendation": "Replay traces offline, mutate one artifact, and compare against a baseline before promotion.",
    },
    {
        "id": "promotion-gate",
        "label": "Memory promotion gate",
        "patterns": [r"promotion criteria", r"promote", r"source evidence", r"expiry", r"verification", r"owner"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills"],
        "recommendation": "Promote memories only with evidence, redaction, freshness, verification, and expiry policy.",
    },
    {
        "id": "memory-safety",
        "label": "Memory safety and privacy",
        "patterns": [r"secrets", r"private data", r"PII", r"raw customer data", r"stale", r"verified"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Block secrets, private data, stale claims, and unverified model assertions from durable memory.",
    },
    {
        "id": "automatic-memory-trigger",
        "label": "Automatic memory trigger controls",
        "patterns": [
            r"auto-trigger",
            r"automatic trigger",
            r"SessionStart",
            r"\bStop\b",
            r"fallback skill",
            r"trigger policy",
            r"controllable",
            r"capture_raw_prompt",
        ],
        "min_matches": 3,
        "paths": ["README.md", "docs", "workflows", "skills", "manifests", "plugins"],
        "recommendation": "Install plugin hooks where possible, and use a controlled implicit skill trigger where plugins are unavailable.",
    },
    {
        "id": "token-efficient-recall",
        "label": "Token-efficient recall",
        "patterns": [r"token", r"always-on context", r"retrieve", r"pointer", r"compression", r"prompt-cache"],
        "min_matches": 2,
        "paths": ["docs", "workflows", "skills", "README.md"],
        "recommendation": "Keep traces and large references outside prompts; load compact memories by relevance.",
    },
    {
        "id": "skill-lifecycle-curation",
        "label": "Skill lifecycle curation",
        "patterns": [
            r"Curator",
            r"usage tracking",
            r"importance",
            r"archive",
            r"pinned",
            r"stale",
            r"dedup",
            r"skill lifecycle",
        ],
        "min_matches": 3,
        "paths": ["README.md", "docs", "workflows", "skills", "manifests"],
        "recommendation": "Constrain self-evolution with usage stats, importance levels, reversible archive state, and duplicate checks.",
    },
]


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path
    stage: str
    source: str
    relative_path: str


@dataclass(frozen=True)
class Plugin:
    name: str
    version: str
    description: str
    path: Path
    relative_path: str
    manifest: dict


def request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


def emit_json(ok: bool, payload: dict, code: str | None = None) -> None:
    body = {
        "ok": ok,
        "request_id": request_id(),
        "ts": int(time.time()),
    }
    if ok:
        body["data"] = payload
    else:
        body["error"] = {"code": code or "ERROR", **payload}
    print(json.dumps(body, ensure_ascii=False, indent=2))


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FM_RE.match(text)
    if not match:
        return {}

    data: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal key, buf
        if key is not None:
            value = "\n".join(buf).strip()
            if value.startswith((">", "|")):
                lines = [line.strip() for line in value[1:].splitlines()]
                value = " ".join(line for line in lines if line)
            data[key] = value.strip("\"'")
        key = None
        buf = []

    for raw in match.group(1).splitlines():
        if raw and not raw.startswith((" ", "-")) and ":" in raw:
            flush()
            k, _, v = raw.partition(":")
            key = k.strip()
            buf = [v.strip()]
        else:
            buf.append(raw)
    flush()
    return data


def skill_from_path(path: Path, source: str = "core") -> Skill:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    name = fm.get("name") or path.parent.name
    desc = fm.get("description") or ""
    rel = path.parent.relative_to(ROOT).as_posix()
    parts = path.parent.relative_to(SKILLS_ROOT).parts if source == "core" else ()
    stage = parts[0] if parts else source
    return Skill(name=name, description=desc, path=path.parent, stage=stage, source=source, relative_path=rel)


def iter_skill_files(root: Path = SKILLS_ROOT) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("SKILL.md"))


def discover_skills(profile: str = "all") -> list[Skill]:
    allowed = PROFILE_STAGE_PREFIXES.get(profile)
    if allowed is None:
        raise ValueError(f"unknown profile: {profile}")
    excluded = PROFILE_SKILL_EXCLUDES.get(profile, set())
    items = []
    for skill_md in iter_skill_files():
        try:
            stage = skill_md.parent.relative_to(SKILLS_ROOT).parts[0]
        except (IndexError, ValueError):
            continue
        if stage not in allowed:
            continue
        skill = skill_from_path(skill_md)
        if skill.name not in excluded:
            items.append(skill)
    return sorted(items, key=lambda s: (s.stage, s.name, s.relative_path))


def discover_vendor_skills() -> list[Skill]:
    if not VENDOR_ROOT.exists():
        return []
    return [
        skill_from_path(path, source="vendor")
        for path in sorted(VENDOR_ROOT.rglob("SKILL.md"))
    ]


def plugin_from_manifest(manifest_path: Path) -> Plugin:
    manifest = read_json_file(manifest_path)
    plugin_path = manifest_path.parents[1]
    rel = plugin_path.relative_to(ROOT).as_posix()
    return Plugin(
        name=str(manifest.get("name") or plugin_path.name),
        version=str(manifest.get("version") or ""),
        description=str(manifest.get("description") or ""),
        path=plugin_path,
        relative_path=rel,
        manifest=manifest,
    )


def discover_plugins() -> list[Plugin]:
    if not PLUGIN_ROOT.exists():
        return []

    plugins = []
    for manifest_path in sorted(PLUGIN_ROOT.glob("*/.codex-plugin/plugin.json")):
        try:
            plugins.append(plugin_from_manifest(manifest_path))
        except (OSError, json.JSONDecodeError, ValueError):
            continue
    return sorted(plugins, key=lambda p: (p.name, p.relative_path))


def manifest_relative_path(plugin: Plugin, value: str) -> Path:
    clean = value[2:] if value.startswith("./") else value
    return plugin.path / clean


def plugin_manifest_paths(plugin: Plugin) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    for field in ("skills", "mcpServers", "apps", "hooks"):
        value = plugin.manifest.get(field)
        if isinstance(value, str):
            out.append((field, manifest_relative_path(plugin, value)))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    out.append((field, manifest_relative_path(plugin, item)))
    default_hooks = plugin.path / "hooks" / "hooks.json"
    if "hooks" not in plugin.manifest and default_hooks.exists():
        out.append(("hooks", default_hooks))
    return out


def validate_plugin(plugin: Plugin) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = plugin.path / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        errors.append("missing .codex-plugin/plugin.json")
    if not plugin.name:
        errors.append("manifest.name missing")
    elif not NAME_RE.match(plugin.name):
        errors.append(f"invalid plugin name '{plugin.name}'")
    if plugin.name and plugin.name != plugin.path.name:
        warnings.append("plugin name differs from folder name")
    if not plugin.version:
        errors.append("manifest.version missing")
    if not plugin.description:
        errors.append("manifest.description missing")
    elif len(plugin.description) < 20:
        warnings.append("description is short")

    for field, path in plugin_manifest_paths(plugin):
        if not path.exists():
            errors.append(f"manifest.{field} path not found: {path.relative_to(plugin.path)}")
        if field == "hooks" and path.exists():
            try:
                read_json_file(path)
            except json.JSONDecodeError as exc:
                errors.append(f"manifest.hooks invalid JSON: {exc}")

    skills_path = plugin.manifest.get("skills")
    if isinstance(skills_path, str):
        skills_root = manifest_relative_path(plugin, skills_path)
        if skills_root.exists():
            skill_files = sorted(skills_root.rglob("SKILL.md"))
            if not skill_files:
                warnings.append("manifest.skills contains no SKILL.md files")
            for skill_md in skill_files:
                text = skill_md.read_text(encoding="utf-8", errors="replace")
                fm = parse_frontmatter(text)
                if not fm.get("name"):
                    errors.append(f"plugin skill missing name: {skill_md.relative_to(plugin.path)}")
                if not fm.get("description"):
                    errors.append(f"plugin skill missing description: {skill_md.relative_to(plugin.path)}")

    return errors, warnings


def tracked_repo_files() -> list[Path]:
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        proc = None

    if proc and proc.returncode == 0:
        return [ROOT / line for line in proc.stdout.splitlines() if line]

    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in {".git", ".omx", "node_modules"} for part in path.parts)
    ]


def read_json_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def default_target_for_profile(profile: str) -> str:
    if profile == "hermes":
        return os.environ.get("HERMES_SKILLS_HOME", "~/.hermes/skills")
    return os.environ.get("CODEX_SKILLS_HOME", "~/.codex/skills")


def profile_excluded_skills(profile: str) -> list[str]:
    all_names = {skill.name for skill in discover_skills("all")}
    return sorted(name for name in PROFILE_SKILL_EXCLUDES.get(profile, set()) if name in all_names)


def iter_project_files(project: Path) -> Iterable[Path]:
    if not project.exists():
        return []
    return sorted(
        path
        for path in project.rglob("*")
        if path.is_file() and not any(part in HARNESS_IGNORES for part in path.relative_to(project).parts)
    )


def project_text_for_paths(project: Path, path_hints: list[str]) -> tuple[str, list[str]]:
    chunks: list[str] = []
    evidence: list[str] = []
    for hint in path_hints:
        target = project / hint
        candidates = [target] if target.is_file() else []
        if target.is_dir():
            candidates = [p for p in iter_project_files(target) if p.suffix.lower() in TEXT_SUFFIXES]
        for path in candidates[:80]:
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"Makefile", "AGENTS.md"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            chunks.append(text[:12000])
            evidence.append(path.relative_to(project).as_posix())
    return "\n".join(chunks), sorted(set(evidence))


def group_by_stage(skills: list[Skill]) -> dict[str, list[Skill]]:
    grouped: dict[str, list[Skill]] = {}
    for skill in skills:
        grouped.setdefault(skill.stage, []).append(skill)
    return grouped


def duplicate_names(skills: list[Skill]) -> dict[str, list[Skill]]:
    seen: dict[str, list[Skill]] = {}
    for skill in skills:
        seen.setdefault(skill.name, []).append(skill)
    return {name: vals for name, vals in seen.items() if len(vals) > 1}


def local_markdown_links(skill: Skill) -> list[Path]:
    text = (skill.path / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    out = []
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if "://" in target:
            continue
        clean = target.split("#", 1)[0].strip()
        if clean and clean.endswith((".md", ".yaml", ".json", ".py", ".sh")):
            out.append(skill.path / clean)
    return out


def validate_skill(skill: Skill) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_md = skill.path / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)

    if not fm:
        errors.append("missing YAML frontmatter")
    if not skill.name:
        errors.append("frontmatter.name missing")
    elif not NAME_RE.match(skill.name):
        errors.append(f"invalid name '{skill.name}'")
    if not skill.description:
        errors.append("frontmatter.description missing")
    elif len(skill.description) < 20:
        warnings.append("description is short")

    for linked in local_markdown_links(skill):
        if not linked.exists():
            warnings.append(f"linked local file not found: {linked.relative_to(skill.path)}")

    if (skill.path / "references").exists():
        for ref in sorted((skill.path / "references").glob("*.md")):
            rel = ref.relative_to(skill.path).as_posix()
            if rel not in text:
                warnings.append(f"reference not linked from SKILL.md: {rel}")

    return errors, warnings


def cmd_list(args: argparse.Namespace) -> int:
    skills = discover_skills(args.profile)
    if args.json:
        emit_json(True, {"profile": args.profile, "total": len(skills), "skills": [skill_dict(s) for s in skills]})
        return EXIT_OK

    print(f"Super Skill profile '{args.profile}' ({len(skills)} skills)")
    for stage, items in group_by_stage(skills).items():
        print(f"\n{STAGES.get(stage, stage)}")
        for skill in items:
            print(f"  {skill.name:<28} {skill.description[:100]}")
    return EXIT_OK


def cmd_vendor(args: argparse.Namespace) -> int:
    skills = discover_vendor_skills()
    dups = duplicate_names(skills)
    if args.json:
        emit_json(
            True,
            {
                "total": len(skills),
                "unique_names": len({s.name for s in skills}),
                "duplicates": {k: [s.relative_path for s in v] for k, v in dups.items()},
                "skills": [skill_dict(s) for s in skills],
            },
        )
        return EXIT_OK

    print(f"Cowork vendor ecosystem: {len(skills)} skill files, {len({s.name for s in skills})} unique names")
    if dups:
        print("Duplicate names are intentionally kept in vendor form:")
        for name, items in sorted(dups.items()):
            print(f"  {name}: {', '.join(s.relative_path for s in items)}")
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    skills = discover_skills("all")
    failures = []
    warnings = []
    for skill in skills:
        errs, warns = validate_skill(skill)
        if errs:
            failures.append({"skill": skill_dict(skill), "errors": errs})
        if warns:
            warnings.append({"skill": skill_dict(skill), "warnings": warns})

    dups = duplicate_names(skills)
    if dups:
        failures.append(
            {
                "skill": {"name": "<namespace>"},
                "errors": [f"duplicate installable skill name: {name}" for name in sorted(dups)],
            }
        )

    design_brands = [p for p in (ROOT / "resources" / "design-md").iterdir() if p.is_dir()] if (ROOT / "resources" / "design-md").exists() else []
    vendor_skills = discover_vendor_skills()
    payload = {
        "skills_total": len(skills),
        "skills_failed": len(failures),
        "warnings_total": sum(len(w["warnings"]) for w in warnings),
        "design_brands": len(design_brands),
        "vendor_skill_files": len(vendor_skills),
        "failures": failures,
        "warnings": warnings,
    }

    if args.json:
        emit_json(not failures, payload, code="VALIDATION_FAILED" if failures else None)
    else:
        print(f"Installable skills: {len(skills)}")
        print(f"Design brand systems: {len(design_brands)}")
        print(f"Vendor skill files: {len(vendor_skills)}")
        print(f"Warnings: {payload['warnings_total']}")
        if failures:
            print("\nFailures:")
            for failure in failures:
                print(f"  {failure['skill']['name']}")
                for err in failure["errors"]:
                    print(f"    - {err}")
        else:
            print("Validation passed.")
    return EXIT_RUNTIME if failures else EXIT_OK


def build_install_plan(profile: str, target: str | None, mode: str) -> dict:
    skills = discover_skills(profile)
    dups = duplicate_names(skills)
    if dups:
        raise ValueError(f"duplicate installable skill names: {', '.join(sorted(dups))}")

    resolved_target = target or default_target_for_profile(profile)
    target_path = Path(resolved_target).expanduser()
    action = "symlink" if mode == "symlink" else "copy"
    operations = []
    for skill in skills:
        dest = target_path / skill.name
        operations.append(
            {
                "name": skill.name,
                "stage": skill.stage,
                "stage_label": STAGES.get(skill.stage, skill.stage),
                "source": skill.relative_path,
                "target": str(dest),
                "action": action,
                "target_exists": dest.exists() or dest.is_symlink(),
            }
        )
    return {
        "profile": profile,
        "mode": mode,
        "target": str(target_path),
        "skills_total": len(skills),
        "stages": sorted({s.stage for s in skills}),
        "excluded_skills": profile_excluded_skills(profile),
        "target_conflicts": [op for op in operations if op["target_exists"]],
        "operations": operations,
    }


def default_memory_plugin_marketplace() -> Path:
    return Path("~/.agents/plugins/marketplace.json").expanduser()


def marketplace_root_for_path(marketplace: Path) -> Path:
    expanded = marketplace.expanduser()
    if expanded.name == "marketplace.json" and expanded.parent.name == "plugins" and expanded.parent.parent.name == ".agents":
        return expanded.parent.parent.parent
    return expanded.parent


def default_memory_plugin_target(marketplace: Path | None = None) -> Path:
    root = marketplace_root_for_path(marketplace or default_memory_plugin_marketplace())
    if root == Path.home():
        return root / ".codex" / "plugins" / MEMORY_PLUGIN_NAME
    return root / "plugins" / MEMORY_PLUGIN_NAME


def default_codex_hooks_path() -> Path:
    return Path("~/.codex/hooks.json").expanduser()


def default_codex_config_path() -> Path:
    return Path("~/.codex/config.toml").expanduser()


def memory_plugin_hook_config(script_path: Path) -> dict:
    quoted_script = shlex.quote(str(script_path.expanduser()))
    return {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 {quoted_script} --event session-start",
                            "timeout": 10,
                        }
                    ],
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 {quoted_script} --event stop",
                            "timeout": 30,
                        }
                    ],
                }
            ],
        }
    }


def hooks_group_commands(group: dict) -> set[str]:
    return {
        str(item.get("command"))
        for item in group.get("hooks", [])
        if isinstance(item, dict) and item.get("type") == "command" and item.get("command")
    }


def merge_hook_config(existing: dict, update: dict) -> dict:
    merged = dict(existing)
    merged_hooks = dict(merged.get("hooks") or {})
    for event, groups in (update.get("hooks") or {}).items():
        current = list(merged_hooks.get(event) or [])
        current_commands = set().union(*(hooks_group_commands(group) for group in current)) if current else set()
        for group in groups:
            commands = hooks_group_commands(group)
            if commands and commands.issubset(current_commands):
                continue
            current.append(group)
            current_commands.update(commands)
        merged_hooks[event] = current
    merged["hooks"] = merged_hooks
    return merged


def marketplace_source_path(marketplace: Path, target: Path) -> tuple[str, list[str]]:
    warnings: list[str] = []
    root = marketplace_root_for_path(marketplace)
    resolved_target = target.expanduser()
    try:
        rel = resolved_target.relative_to(root)
        return f"./{rel.as_posix()}", warnings
    except ValueError:
        warnings.append("plugin target is outside marketplace root; using absolute local source path")
        return str(resolved_target), warnings


def marketplace_payload_with_plugin(existing: dict, marketplace: Path, target: Path) -> tuple[dict, list[str]]:
    payload = dict(existing) if existing else {}
    payload.setdefault("name", "super-skill-local")
    payload.setdefault("interface", {"displayName": "Super Skill Local"})
    plugins = [item for item in payload.get("plugins", []) if item.get("name") != MEMORY_PLUGIN_NAME]
    source_path, warnings = marketplace_source_path(marketplace, target)
    plugins.append(
        {
            "name": MEMORY_PLUGIN_NAME,
            "source": {
                "source": "local",
                "path": source_path,
            },
            "policy": {
                "installation": "INSTALLED_BY_DEFAULT",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
    )
    payload["plugins"] = sorted(plugins, key=lambda item: item.get("name", ""))
    return payload, warnings


def read_existing_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return read_json_file(path)


def install_directory(source: Path, target: Path, mode: str, force: bool, dry_run: bool) -> dict:
    if target.exists() or target.is_symlink():
        if not force:
            return {"name": MEMORY_PLUGIN_NAME, "status": "skipped", "reason": "target exists", "target": str(target)}
        if dry_run:
            return {"name": MEMORY_PLUGIN_NAME, "status": "would-replace", "target": str(target)}
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)

    action = "symlink" if mode == "symlink" else "copy"
    if dry_run:
        return {"name": MEMORY_PLUGIN_NAME, "status": f"would-{action}", "target": str(target)}

    target.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        target.symlink_to(source)
    else:
        shutil.copytree(source, target)
    return {"name": MEMORY_PLUGIN_NAME, "status": action, "target": str(target)}


def update_codex_config_for_hooks(config_path: Path, force: bool, dry_run: bool) -> dict:
    if config_path.exists():
        text = config_path.read_text(encoding="utf-8", errors="replace")
    else:
        text = ""

    if re.search(r"(?m)^\s*codex_hooks\s*=\s*true\s*$", text):
        return {"path": str(config_path), "status": "already-enabled"}

    if re.search(r"(?m)^\s*codex_hooks\s*=\s*false\s*$", text):
        if not force:
            return {
                "path": str(config_path),
                "status": "blocked",
                "reason": "codex_hooks is explicitly false; rerun with --force to enable",
            }
        updated = re.sub(r"(?m)^(\s*)codex_hooks\s*=\s*false\s*$", r"\1codex_hooks = true", text, count=1)
    elif re.search(r"(?m)^\[features\]\s*$", text):
        updated = re.sub(r"(?m)^(\[features\]\s*)$", r"\1\ncodex_hooks = true", text, count=1)
    else:
        prefix = "" if not text or text.endswith("\n") else "\n"
        updated = f"{text}{prefix}\n[features]\ncodex_hooks = true\n"

    if dry_run:
        return {"path": str(config_path), "status": "would-update" if config_path.exists() else "would-create"}

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(updated, encoding="utf-8")
    return {"path": str(config_path), "status": "updated" if text else "created"}


def install_memory_plugin_payload(
    *,
    runtime: str,
    target: str | None,
    marketplace: str | None,
    hooks: str | None,
    config: str | None,
    mode: str,
    force: bool,
    dry_run: bool,
) -> dict:
    if runtime != "codex":
        raise ValueError("memory plugin currently supports runtime=codex")

    source = PLUGIN_ROOT / MEMORY_PLUGIN_NAME
    if not source.exists():
        raise ValueError(f"memory plugin source not found: {source.relative_to(ROOT)}")

    marketplace_path = Path(marketplace).expanduser() if marketplace else default_memory_plugin_marketplace()
    target_path = Path(target).expanduser() if target else default_memory_plugin_target(marketplace_path)
    hooks_path = Path(hooks).expanduser() if hooks else default_codex_hooks_path()
    config_path = Path(config).expanduser() if config else default_codex_config_path()
    installed_script = target_path / "scripts" / "memory_dream_hook.py"

    operations: list[dict] = []
    warnings: list[str] = []

    operations.append({"type": "plugin-bundle", **install_directory(source, target_path, mode, force, dry_run)})

    marketplace_existing = read_existing_json(marketplace_path)
    marketplace_next, marketplace_warnings = marketplace_payload_with_plugin(marketplace_existing, marketplace_path, target_path)
    warnings.extend(marketplace_warnings)
    if dry_run:
        marketplace_status = "would-update" if marketplace_path.exists() else "would-create"
    else:
        marketplace_path.parent.mkdir(parents=True, exist_ok=True)
        marketplace_path.write_text(json.dumps(marketplace_next, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        marketplace_status = "updated" if marketplace_existing else "created"
    operations.append(
        {
            "type": "marketplace",
            "path": str(marketplace_path),
            "status": marketplace_status,
            "plugin_source": next(
                item["source"]["path"]
                for item in marketplace_next.get("plugins", [])
                if item.get("name") == MEMORY_PLUGIN_NAME
            ),
        }
    )

    hooks_existing = read_existing_json(hooks_path)
    hooks_next = merge_hook_config(hooks_existing, memory_plugin_hook_config(installed_script))
    if dry_run:
        hooks_status = "would-update" if hooks_path.exists() else "would-create"
    else:
        hooks_path.parent.mkdir(parents=True, exist_ok=True)
        hooks_path.write_text(json.dumps(hooks_next, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        hooks_status = "updated" if hooks_existing else "created"
    operations.append({"type": "hooks", "path": str(hooks_path), "status": hooks_status, "script": str(installed_script)})

    config_op = update_codex_config_for_hooks(config_path, force, dry_run)
    config_op["type"] = "codex-config"
    if config_op.get("status") == "blocked":
        warnings.append(str(config_op.get("reason")))
    operations.append(config_op)

    return {
        "runtime": runtime,
        "plugin": MEMORY_PLUGIN_NAME,
        "source": str(source),
        "target": str(target_path),
        "mode": mode,
        "marketplace": str(marketplace_path),
        "hooks": str(hooks_path),
        "config": str(config_path),
        "dry_run": dry_run,
        "operations": operations,
        "warnings": warnings,
    }


def memory_plugin_has_blocker(payload: dict) -> bool:
    return any(op.get("status") == "blocked" for op in payload.get("operations", []))


def cmd_plan(args: argparse.Namespace) -> int:
    plan = build_install_plan(args.profile, args.target, args.mode)
    if args.json:
        emit_json(True, plan)
    else:
        print(f"Install plan '{args.profile}' to {plan['target']} ({args.mode})")
        print(f"Skills: {plan['skills_total']}")
        for op in plan["operations"]:
            print(f"  {op['action']:<8} {op['name']:<30} {op['target']}")
    return EXIT_OK


def install_one(skill: Skill, target: Path, mode: str, force: bool, dry_run: bool) -> dict:
    dest = target / skill.name
    action = "symlink" if mode == "symlink" else "copy"
    if dest.exists() or dest.is_symlink():
        if not force:
            return {"name": skill.name, "status": "skipped", "reason": "target exists", "target": str(dest)}
        if dry_run:
            return {"name": skill.name, "status": "would-replace", "target": str(dest)}
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        else:
            shutil.rmtree(dest)

    if dry_run:
        return {"name": skill.name, "status": f"would-{action}", "target": str(dest)}

    target.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        dest.symlink_to(skill.path)
    else:
        shutil.copytree(skill.path, dest)
    return {"name": skill.name, "status": action, "target": str(dest)}


def cmd_install(args: argparse.Namespace) -> int:
    skills = discover_skills(args.profile)
    dups = duplicate_names(skills)
    if dups:
        emit_json(
            False,
            {"message": "duplicate installable skill names", "duplicates": sorted(dups)},
            code="VALIDATION_FAILED",
        )
        return EXIT_RUNTIME

    target = Path(args.target or default_target_for_profile(args.profile)).expanduser()
    results = [install_one(skill, target, args.mode, args.force, args.dry_run) for skill in skills]
    memory_plugin = None
    if args.with_memory_plugin:
        memory_plugin = install_memory_plugin_payload(
            runtime="codex",
            target=args.memory_plugin_target,
            marketplace=args.memory_plugin_marketplace,
            hooks=args.memory_plugin_hooks,
            config=args.memory_plugin_config,
            mode=args.mode,
            force=args.force,
            dry_run=args.dry_run,
        )
        if memory_plugin_has_blocker(memory_plugin):
            if args.json:
                emit_json(
                    False,
                    {"message": "memory plugin install is blocked", "memory_plugin": memory_plugin},
                    code="MEMORY_PLUGIN_BLOCKED",
                )
            else:
                print("error: memory plugin install is blocked", file=sys.stderr)
            return EXIT_RUNTIME

    if args.json:
        payload = {
            "profile": args.profile,
            "mode": args.mode,
            "target": str(target),
            "excluded_skills": profile_excluded_skills(args.profile),
            "results": results,
        }
        if memory_plugin:
            payload["memory_plugin"] = memory_plugin
        emit_json(True, payload)
    else:
        print(f"Install profile '{args.profile}' to {target} ({args.mode})")
        for result in results:
            print(f"  {result['status']:<14} {result['name']}")
        if memory_plugin:
            print(f"Memory plugin: {memory_plugin['plugin']} -> {memory_plugin['target']}")
    return EXIT_OK


def cmd_memory_plugin(args: argparse.Namespace) -> int:
    payload = install_memory_plugin_payload(
        runtime=args.runtime,
        target=args.target,
        marketplace=args.marketplace,
        hooks=args.hooks,
        config=args.config,
        mode=args.mode,
        force=args.force,
        dry_run=args.dry_run,
    )
    blocked = memory_plugin_has_blocker(payload)
    if args.json:
        emit_json(not blocked, payload, code="MEMORY_PLUGIN_BLOCKED" if blocked else None)
    else:
        print(f"Memory plugin '{payload['plugin']}' for {payload['runtime']}:")
        for op in payload["operations"]:
            print(f"  {op['type']:<14} {op['status']:<14} {op.get('path') or op.get('target')}")
        for warning in payload["warnings"]:
            print(f"warning: {warning}")
    return EXIT_RUNTIME if blocked else EXIT_OK


def cmd_triggers(args: argparse.Namespace) -> int:
    trigger_errors, trigger_warnings, trigger_policy = auto_trigger_policy_report()
    lifecycle_errors, lifecycle_warnings, lifecycle_policy = skill_lifecycle_policy_report()
    failures = trigger_errors + lifecycle_errors
    payload = {
        "auto_trigger_policy": trigger_policy,
        "skill_lifecycle_policy": lifecycle_policy,
        "warnings": trigger_warnings + lifecycle_warnings,
        "failures": failures,
    }
    if args.json:
        emit_json(not failures, payload, code="TRIGGER_POLICY_FAILED" if failures else None)
    else:
        if failures:
            print("Trigger policy failures:")
            for failure in failures:
                print(f"  {failure['check']}: {failure['message']}")
        else:
            print(f"Fallback skill: {trigger_policy.get('fallback_skill')}")
            print(f"Automatic triggers: {len(trigger_policy.get('triggers', []))}")
            print(f"Protected skills: {len(lifecycle_policy.get('protected_skills', []))}")
    return EXIT_RUNTIME if failures else EXIT_OK


def eval_project_dirs() -> list[Path]:
    root = EVALS_ROOT / "projects"
    if not root.exists():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def evaluate_project_fixture(project_dir: Path, skills_by_name: dict[str, Skill]) -> dict:
    skill_map_path = project_dir / "skill-map.json"
    brief_path = project_dir / "project.md"
    checks: list[dict] = []

    if not skill_map_path.exists() or not brief_path.exists():
        return {
            "project": project_dir.name,
            "ok": False,
            "checks": [
                {
                    "id": "fixture-files",
                    "ok": False,
                    "message": "missing project.md or skill-map.json",
                }
            ],
        }

    spec = read_json_file(skill_map_path)
    brief = brief_path.read_text(encoding="utf-8", errors="replace")
    required_skills = spec.get("required_skills", [])
    required_stages = spec.get("required_stages", [])
    required_phrases = spec.get("required_phrases", [])

    missing_skills = sorted(name for name in required_skills if name not in skills_by_name)
    checks.append(
        {
            "id": "required-skills",
            "ok": not missing_skills,
            "expected": len(required_skills),
            "missing": missing_skills,
        }
    )

    present_stages = sorted({skills_by_name[name].stage for name in required_skills if name in skills_by_name})
    missing_stages = sorted(set(required_stages) - set(present_stages))
    checks.append(
        {
            "id": "lifecycle-stage-coverage",
            "ok": not missing_stages,
            "expected": required_stages,
            "present": present_stages,
            "missing": missing_stages,
        }
    )

    text = brief.lower()
    missing_phrases = sorted(phrase for phrase in required_phrases if phrase.lower() not in text)
    checks.append(
        {
            "id": "acceptance-language",
            "ok": not missing_phrases,
            "expected": required_phrases,
            "missing": missing_phrases,
        }
    )

    return {
        "project": spec.get("project", project_dir.name),
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
    }


def run_memory_hook_probe(workspace: Path, prompt: str = "do not store this raw prompt") -> dict:
    script = PLUGIN_ROOT / MEMORY_PLUGIN_NAME / "scripts" / "memory_dream_hook.py"
    if not script.exists():
        return {"id": "memory-hook-simulation", "ok": False, "message": "hook script missing"}

    payload = {
        "hook_event_name": "Stop",
        "cwd": str(workspace),
        "model": "eval-model",
        "session_id": "eval-session",
        "transcript_path": str(workspace / "transcript.jsonl"),
        "prompt": prompt,
    }
    proc = subprocess.run(
        [sys.executable, str(script), "--event", "stop"],
        cwd=workspace,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if proc.returncode != 0:
        return {
            "id": "memory-hook-simulation",
            "ok": False,
            "message": "hook exited non-zero",
            "stderr": proc.stderr[:500],
        }
    candidates = sorted((workspace / ".super-skill" / "memory" / "inbox").glob("*.md"))
    traces = sorted((workspace / ".super-skill" / "memory" / "traces").glob("*.jsonl"))
    candidate_text = candidates[0].read_text(encoding="utf-8") if candidates else ""
    return {
        "id": "memory-hook-simulation",
        "ok": bool(candidates) and bool(traces) and prompt not in candidate_text,
        "candidates": len(candidates),
        "traces": len(traces),
        "raw_prompt_stored": prompt in candidate_text,
    }


def simulate_memory_hook_eval() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        return run_memory_hook_probe(Path(tmp))


def evaluate_capability_suite(project_filter: str | None = None) -> dict:
    skills = discover_skills("all")
    skills_by_name = {skill.name: skill for skill in skills}
    projects = []
    for project_dir in eval_project_dirs():
        if project_filter and project_dir.name != project_filter:
            continue
        projects.append(evaluate_project_fixture(project_dir, skills_by_name))

    install_dups = duplicate_names(skills)
    trigger_errors, _, trigger_policy = auto_trigger_policy_report()
    lifecycle_errors, _, lifecycle_policy = skill_lifecycle_policy_report()
    plugin_errors, plugin_warnings = plugin_manifest_report()
    plugins = discover_plugins()
    memory_plugin = next((plugin for plugin in plugins if plugin.name == MEMORY_PLUGIN_NAME), None)
    harness_report = assess_harness(ROOT)
    hermes_report = assess_hermes(ROOT)
    memory_report = assess_memory(ROOT)

    global_checks = [
        {
            "id": "project-filter",
            "ok": not project_filter or bool(projects),
            "project": project_filter,
        },
        {
            "id": "installable-skill-uniqueness",
            "ok": not install_dups,
            "duplicates": sorted(install_dups),
        },
        {
            "id": "harness-readiness",
            "ok": harness_report["score"] >= 100,
            "score": harness_report["score"],
        },
        {
            "id": "hermes-readiness",
            "ok": hermes_report["score"] >= 100,
            "score": hermes_report["score"],
        },
        {
            "id": "memory-readiness",
            "ok": memory_report["score"] >= 100,
            "score": memory_report["score"],
        },
        {
            "id": "trigger-policy",
            "ok": not trigger_errors
            and trigger_policy.get("fallback_skill") == "agent-memory-dream-loop"
            and not trigger_policy.get("controls", {}).get("capture_raw_prompt")
            and not trigger_policy.get("controls", {}).get("capture_raw_response")
            and not trigger_policy.get("controls", {}).get("auto_promote"),
            "triggers": len(trigger_policy.get("triggers", [])) if trigger_policy else 0,
        },
        {
            "id": "skill-lifecycle-policy",
            "ok": not lifecycle_errors
            and lifecycle_policy.get("curation", {}).get("require_dedup_before_create") is True
            and lifecycle_policy.get("curation", {}).get("archive_is_reversible") is True
            and lifecycle_policy.get("curation", {}).get("auto_delete") is False,
            "protected_skills": len(lifecycle_policy.get("protected_skills", [])) if lifecycle_policy else 0,
        },
        {
            "id": "codex-plugin-hook-only",
            "ok": bool(memory_plugin)
            and not plugin_errors
            and not plugin_warnings
            and memory_plugin.manifest.get("hooks")
            and "skills" not in memory_plugin.manifest,
            "plugin": MEMORY_PLUGIN_NAME if memory_plugin else None,
        },
        simulate_memory_hook_eval(),
    ]

    failures = [
        {"scope": "project", "project": project["project"], "checks": [c for c in project["checks"] if not c["ok"]]}
        for project in projects
        if not project["ok"]
    ]
    failed_global = [check for check in global_checks if not check["ok"]]
    if failed_global:
        failures.append({"scope": "global", "checks": failed_global})

    return {
        "projects_total": len(projects),
        "projects_passed": sum(1 for project in projects if project["ok"]),
        "global_checks_total": len(global_checks),
        "global_checks_passed": sum(1 for check in global_checks if check["ok"]),
        "projects": projects,
        "global_checks": global_checks,
        "failures": failures,
    }


def cmd_evals(args: argparse.Namespace) -> int:
    payload = evaluate_capability_suite(args.project)
    ok = not payload["failures"]
    if args.json:
        emit_json(ok, payload, code="EVALS_FAILED" if not ok else None)
    else:
        print(f"Capability eval projects: {payload['projects_passed']}/{payload['projects_total']} passed")
        print(f"Global checks: {payload['global_checks_passed']}/{payload['global_checks_total']} passed")
        if payload["failures"]:
            print("Failures:")
            for failure in payload["failures"]:
                print(f"  {failure['scope']}: {failure.get('project', '<global>')}")
    return EXIT_OK if ok else EXIT_RUNTIME


def live_project_dirs() -> list[Path]:
    if not LIVE_EVALS_ROOT.exists():
        return []
    return sorted(path for path in LIVE_EVALS_ROOT.iterdir() if path.is_dir())


def command_argv(argv: list[str]) -> list[str]:
    out = []
    for part in argv:
        if part == "{python}":
            out.append(sys.executable)
            continue
        # Allow `{root}` and `{python}` to appear as substrings, e.g. `{root}/bin/x`.
        replaced = part.replace("{root}", str(ROOT)).replace("{python}", sys.executable)
        out.append(replaced)
    return out


def check_live_required_files(workspace: Path, required_files: list[str]) -> dict:
    """Check that each required path exists. Glob patterns (containing * or ?)
    must match at least one file under workspace."""
    missing: list[str] = []
    for path in required_files:
        if any(ch in path for ch in "*?["):
            matches = list(workspace.glob(path))
            if not matches:
                missing.append(path)
        else:
            if not (workspace / path).exists():
                missing.append(path)
    return {"id": "required-files", "ok": not missing, "expected": len(required_files), "missing": sorted(missing)}


def _resolve_content_targets(workspace: Path, path_spec: str) -> list[Path]:
    if any(ch in path_spec for ch in "*?["):
        return sorted(workspace.glob(path_spec))
    p = workspace / path_spec
    return [p] if p.exists() else []


def check_live_required_content(workspace: Path, content_checks: list[dict]) -> dict:
    missing: list[dict] = []
    for item in content_checks:
        targets = _resolve_content_targets(workspace, item["path"])
        if not targets:
            for pattern in item.get("patterns", []):
                missing.append({"path": item["path"], "pattern": pattern, "reason": "no matching file"})
            continue
        # Concatenate text from all matched files (handles glob expansion).
        text = "\n".join(t.read_text(encoding="utf-8", errors="replace") for t in targets).lower()
        for pattern in item.get("patterns", []):
            if pattern.lower() not in text:
                missing.append({"path": item["path"], "pattern": pattern})
    return {"id": "required-content", "ok": not missing, "missing": missing}


def check_live_forbidden_content(workspace: Path, content_checks: list[dict]) -> dict:
    hits: list[dict] = []
    for item in content_checks:
        targets = _resolve_content_targets(workspace, item["path"])
        for target in targets:
            text = target.read_text(encoding="utf-8", errors="replace").lower()
            for pattern in item.get("patterns", []):
                if pattern.lower() in text:
                    hits.append({"path": str(target.relative_to(workspace)), "pattern": pattern})
    return {"id": "forbidden-content", "ok": not hits, "hits": hits}


def run_live_commands(workspace: Path, commands: list[dict], scope: str = "commands") -> dict:
    results = []
    for command in commands:
        argv = command_argv(command.get("argv", []))
        expected_exit = command.get("expect_exit", 0)
        try:
            proc = subprocess.run(
                argv,
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=command.get("timeout", 60),
                check=False,
            )
            results.append(
                {
                    "id": command.get("id", scope),
                    "ok": proc.returncode == expected_exit,
                    "argv": argv,
                    "returncode": proc.returncode,
                    "expected_exit": expected_exit,
                    "stdout_tail": proc.stdout[-800:],
                    "stderr_tail": proc.stderr[-800:],
                }
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append(
                {
                    "id": command.get("id", scope),
                    "ok": False,
                    "argv": argv,
                    "error": str(exc),
                }
            )
    return {"id": scope, "ok": all(result["ok"] for result in results), "results": results}


def run_live_capability_scans(workspace: Path, scans: list[dict]) -> dict:
    assessors = {
        "harness": assess_harness,
        "hermes": assess_hermes,
        "memory": assess_memory,
    }
    results = []
    for scan in scans:
        kind = scan.get("kind")
        assessor = assessors.get(kind)
        if assessor is None:
            results.append({"kind": kind, "ok": False, "message": "unknown scan kind"})
            continue
        report = assessor(workspace)
        min_score = scan.get("min_score", 0)
        results.append({"kind": kind, "ok": report["score"] >= min_score, "score": report["score"], "min_score": min_score})
    return {"id": "capability-scans", "ok": all(result["ok"] for result in results), "results": results}


def run_live_eval_project(project_dir: Path, skills_by_name: dict[str, Skill], keep: bool = False) -> dict:
    recipe_path = project_dir / "recipe.json"
    files_root = project_dir / "files"
    if not recipe_path.exists() or not files_root.exists():
        return {
            "project": project_dir.name,
            "ok": False,
            "checks": [{"id": "fixture-files", "ok": False, "message": "missing recipe.json or files/"}],
        }

    recipe = read_json_file(recipe_path)
    temp_ctx: tempfile.TemporaryDirectory[str] | None = None
    if keep:
        workspace = Path(tempfile.mkdtemp(prefix=f"super-skill-live-{project_dir.name}-"))
    else:
        temp_ctx = tempfile.TemporaryDirectory(prefix=f"super-skill-live-{project_dir.name}-")
        workspace = Path(temp_ctx.name)

    try:
        shutil.copytree(files_root, workspace, dirs_exist_ok=True)
        required_skills = recipe.get("required_skills", [])
        acceptance = recipe.get("acceptance", {})
        checks: list[dict] = []

        missing_skills = sorted(name for name in required_skills if name not in skills_by_name)
        checks.append({"id": "required-skills", "ok": not missing_skills, "expected": len(required_skills), "missing": missing_skills})

        # setup_commands run BEFORE file/content checks so a recipe can drive the
        # workspace through autopilot (or another generator) and then assert on
        # the resulting artifacts. The post-acceptance `commands` block still
        # runs last, after the file/content/forbidden/capability checks.
        setup = acceptance.get("setup_commands", [])
        if setup:
            checks.append(run_live_commands(workspace, setup, scope="setup"))

        checks.append(check_live_required_files(workspace, acceptance.get("required_files", [])))
        checks.append(check_live_required_content(workspace, acceptance.get("required_content", [])))
        checks.append(check_live_forbidden_content(workspace, acceptance.get("forbidden_content", [])))
        if acceptance.get("capability_scans"):
            checks.append(run_live_capability_scans(workspace, acceptance["capability_scans"]))
        checks.append(run_live_commands(workspace, acceptance.get("commands", [])))
        if acceptance.get("memory_hook"):
            checks.append(run_memory_hook_probe(workspace, prompt="live eval secret prompt"))

        return {
            "project": recipe.get("project", project_dir.name),
            "description": recipe.get("description"),
            "ok": all(check["ok"] for check in checks),
            "workspace": str(workspace) if keep else None,
            "checks": checks,
        }
    finally:
        if temp_ctx is not None:
            temp_ctx.cleanup()


def evaluate_live_suite(project_filter: str | None = None, keep: bool = False) -> dict:
    skills = discover_skills("all")
    skills_by_name = {skill.name: skill for skill in skills}
    projects = []
    for project_dir in live_project_dirs():
        if project_filter and project_dir.name != project_filter:
            continue
        projects.append(run_live_eval_project(project_dir, skills_by_name, keep=keep))

    global_checks = [{"id": "project-filter", "ok": not project_filter or bool(projects), "project": project_filter}]
    failures = [
        {"scope": "project", "project": project["project"], "checks": [c for c in project["checks"] if not c["ok"]]}
        for project in projects
        if not project["ok"]
    ]
    failed_global = [check for check in global_checks if not check["ok"]]
    if failed_global:
        failures.append({"scope": "global", "checks": failed_global})

    return {
        "projects_total": len(projects),
        "projects_passed": sum(1 for project in projects if project["ok"]),
        "global_checks_total": len(global_checks),
        "global_checks_passed": sum(1 for check in global_checks if check["ok"]),
        "keep": keep,
        "projects": projects,
        "global_checks": global_checks,
        "failures": failures,
    }


def cmd_live_evals(args: argparse.Namespace) -> int:
    payload = evaluate_live_suite(args.project, keep=args.keep)
    ok = not payload["failures"]
    if args.json:
        emit_json(ok, payload, code="LIVE_EVALS_FAILED" if not ok else None)
    else:
        print(f"Live eval projects: {payload['projects_passed']}/{payload['projects_total']} passed")
        for project in payload["projects"]:
            status = "PASS" if project["ok"] else "FAIL"
            print(f"[{status}] {project['project']}")
            if args.keep and project.get("workspace"):
                print(f"      workspace: {project['workspace']}")
        if payload["failures"]:
            print("Failures:")
            for failure in payload["failures"]:
                print(f"  {failure['scope']}: {failure.get('project', '<global>')}")
    return EXIT_OK if ok else EXIT_RUNTIME


# --- llm-eval: end-to-end real LLM round trip through intent-contract ---
#               → implementation → output-quality-gate
#
# Goal: prove the canonical contract → output → gate loop works against a real
# (or stubbed) language model, not just file-structure graders.

LLM_DEFAULT_PROMPT = (
    "Implement a Python function add(a, b) that returns a + b, with one unit test."
)


def llm_load_skill_body(name: str) -> str:
    matches = list(SKILLS_ROOT.rglob(f"{name}/SKILL.md"))
    if not matches:
        raise FileNotFoundError(f"canonical skill not found: {name}")
    text = matches[0].read_text(encoding="utf-8")
    # Strip the SKILL.md frontmatter — keep body as the system context.
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)
    if len(body) > 6000:
        body = body[:6000] + "\n\n[...truncated for token budget]"
    return body


def llm_call_stub(stage: str, system: str, user: str) -> dict:
    """Deterministic offline pseudo-LLM. Validates that the harness wires the
    skill body, user input, and stage tag through without touching network.

    Stage ids understood:
      - llm-eval: contract / implementation / gate
      - autopilot: 00-research / 01-intent / 02-spec / 03-design / 04-impl /
        05-simplify / 06-gate / 07-delivery / 08-memory
    """
    digest = hashlib_sha1(f"{stage}|{system}|{user}")[:10]
    request = user[:160].replace("\n", " ").strip()
    # Iteration marker: stub stays deterministic but proves the iteration
    # context reached the phase. Real-LLM mode can ignore this — the model is
    # expected to actually rework the artifact based on the prior version.
    is_iteration = "Prior version of this phase" in user
    iteration_note = "\n_(Iteration: rebuilt on top of prior run; feedback applied above.)_\n" if is_iteration else ""

    if stage == "00-research":
        body = textwrap.dedent(f"""\
            ## Research Note (stub)
            - Problem statement: derived from request shape; one user-facing pain
              point to validate before designing.
            - Target users: primary segment plus one adjacent segment for
              acceptance-test framing.
            - Competitor landscape: 2-3 closest tools that solve the same job;
              call out what each one omits.
            - Key assumptions to validate:
              - Users actually do this enough to pay attention to a tool.
              - The fastest path through the workflow is shorter than the status quo.
              - The deliverable can be measured against an objective acceptance.
            - Open questions: budget, deadline, deployment surface, audit constraints.
            - Trace: stub-{digest}
            """)
    elif stage in ("contract", "01-intent"):
        body = textwrap.dedent(f"""\
            ## Intent Contract (stub)
            - Goal: {request}
            - Acceptance:
              - The deliverable matches the user goal.
              - One unit test is included if the goal mentions code.
              - Output is a single self-contained snippet.
            - Out of scope: framework choice changes, deployment.
            - Evidence: passing test + one-line summary.
            - Trace: stub-{digest}
            """)
    elif stage == "02-spec":
        body = textwrap.dedent(f"""\
            ## Product Spec (stub)
            - Problem: {request}
            - MVP slice: smallest deliverable that proves the contract.
            - Success metric: contract acceptance items pass.
            - Rollback: revert to last green checkpoint.
            - Trace: stub-{digest}
            """)
    elif stage == "03-design":
        body = textwrap.dedent(f"""\
            # DESIGN.md (stub)
            - Purpose: deliver the request without AI-slop defaults.
            - Aesthetic Direction: editorial, brutalist-leaning, asymmetric.
            - Color Palette: #0F172A, #F1F5F9, #F97316, #14B8A6.
            - Typography: serif headlines (Source Serif), monospaced data (JetBrains Mono).
            - Layout Strategy: 12-col fluid grid, max-width 72ch for prose.
            - Trace: stub-{digest}
            """)
    elif stage in ("implementation", "04-impl"):
        # Stub picks a language from prompt keywords so the multi-language
        # sandbox can be exercised end-to-end. Default = Python.
        target_lang = "python"
        lc = user.lower()
        if any(k in lc for k in (" javascript", " node.js", "node ", " js ", "javascript ")):
            target_lang = "javascript"
        elif any(k in lc for k in ("bash ", " shell", "shell script")):
            target_lang = "bash"
        elif any(k in lc for k in ("golang", " go ", " go function")):
            target_lang = "go"
        if target_lang == "python":
            body = textwrap.dedent(f"""\
                ```python
                def add(a, b):
                    \"\"\"Implements: {request[:80]}\"\"\"
                    return a + b


                def test_add():
                    assert add(1, 2) == 3
                    assert add(-1, 1) == 0
                ```
                """)
        elif target_lang == "javascript":
            body = textwrap.dedent(f"""\
                ```javascript
                function add(a, b) {{
                    // Implements: {request[:80]}
                    return a + b;
                }}

                function test_add() {{
                    if (add(1, 2) !== 3) throw new Error('1+2 should be 3');
                    if (add(-1, 1) !== 0) throw new Error('-1+1 should be 0');
                }}
                ```
                """)
        elif target_lang == "bash":
            body = textwrap.dedent(f"""\
                ```bash
                #!/usr/bin/env bash
                # Implements: {request[:80]}
                set -euo pipefail

                add() {{
                    echo $(( $1 + $2 ))
                }}

                test_add() {{
                    [ "$(add 1 2)" = "3" ] || {{ echo "FAIL 1+2" >&2; exit 1; }}
                    [ "$(add -1 1)" = "0" ] || {{ echo "FAIL -1+1" >&2; exit 1; }}
                }}

                test_add
                ```
                """)
        elif target_lang == "go":
            body = textwrap.dedent(f"""\
                ```go
                package candidate

                import "testing"

                func Add(a, b int) int {{ return a + b }}

                func TestAdd(t *testing.T) {{
                    if Add(1, 2) != 3 {{ t.Fatalf("1+2 != 3") }}
                    if Add(-1, 1) != 0 {{ t.Fatalf("-1+1 != 0") }}
                }}
                ```
                """)
    elif stage == "05-simplify":
        # 05 has the same language-detection rule as 04 — must produce a
        # functional version of the same artifact, just simplified.
        target_lang = "python"
        lc = user.lower()
        if any(k in lc for k in (" javascript", " node.js", "node ", " js ", "javascript ")):
            target_lang = "javascript"
        elif any(k in lc for k in ("bash ", " shell", "shell script")):
            target_lang = "bash"
        if target_lang == "javascript":
            body = textwrap.dedent("""\
                ```javascript
                function add(a, b) { return a + b; }
                function test_add() {
                    if (add(1, 2) !== 3) throw new Error('1+2');
                    if (add(-1, 1) !== 0) throw new Error('-1+1');
                }
                ```
                """)
        elif target_lang == "bash":
            body = textwrap.dedent("""\
                ```bash
                #!/usr/bin/env bash
                set -euo pipefail
                add() { echo $(( $1 + $2 )); }
                [ "$(add 1 2)" = "3" ] || exit 1
                [ "$(add -1 1)" = "0" ] || exit 1
                ```
                """)
        else:
            body = textwrap.dedent(f"""\
                ```python
                def add(a, b):
                    return a + b


                def test_add():
                    assert add(1, 2) == 3
                    assert add(-1, 1) == 0
                ```
                """)
    elif stage in ("gate", "06-gate"):
        body = json.dumps(
            {
                "matches_intent": True,
                "evidence_present": True,
                "missing": [],
                "score": 8,
                "verdict": "pass",
                "trace": f"stub-{digest}",
            },
            ensure_ascii=False,
            indent=2,
        )
    elif stage == "07-delivery":
        body = textwrap.dedent(f"""\
            ## Delivery Plan (stub)
            - Dockerfile sketch:
              FROM python:3.11-slim
              WORKDIR /app
              COPY . .
              CMD ["python", "-m", "candidate"]
            - CI workflow outline (.github/workflows/ci.yml):
              jobs.test runs `python -m unittest discover` on push and PR; deploy
              job gated on test job and only fires on tags `v*`.
            - Feature flag + kill switch:
              env-var DELIVERY_KILL=1 short-circuits the entry point so a runaway
              release can be turned off without redeploy.
            - Observability hooks:
              structured JSON logs to stdout; counter for matched-vs-rejected;
              error log carries the trace id from earlier phases.
            - Rollback plan:
              previous container tag stays warm; revert by re-pointing the alias.
            - Release notes (draft): "Initial MVP slice. See run.json trace stub-{digest}."
            - Trace: stub-{digest}
            """)
    elif stage in ("07-memory", "08-memory"):
        # Hermes principle: memory candidates must NOT echo the raw user prompt
        # — that's how prompts leak across sessions. Reference the run by trace
        # only and let the reviewer pull the originating prompt from run.json.
        body = textwrap.dedent(f"""\
            Type: episodic
            Scope: project
            Claim: Autopilot harness produced a green research → delivery loop for one task (see run.json for originating intent).
            Evidence: trace=stub-{digest}; phases=9; rolled back at: none
            Use when: A future request resembles this contract shape.
            Do not use when: The deliverable was unverified or contained secrets.
            Expiry: review within 14 days
            """)
    else:
        body = "{}"
    # Only annotate prose phases. Appending markdown would corrupt:
    #   - 04-impl / 05-simplify (raw Python — would fail the test runner)
    #   - 06-gate / "gate" (strict JSON — would fail the JSON parser)
    structured_stages = {"implementation", "04-impl", "05-simplify", "gate", "06-gate"}
    if iteration_note and body and body != "{}" and stage not in structured_stages:
        body = body.rstrip() + "\n" + iteration_note
    return {"text": body, "model": "stub-deterministic-v1", "tokens_in": len(system) + len(user), "tokens_out": len(body)}


def hashlib_sha1(s: str) -> str:
    import hashlib
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def llm_call_anthropic(stage: str, system: str, user: str, model: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set; export it or use --provider stub")
    import urllib.request
    payload = {
        "model": model,
        "max_tokens": 2048,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    text_parts = [b.get("text", "") for b in body.get("content", []) if b.get("type") == "text"]
    text = "\n".join(text_parts).strip()
    usage = body.get("usage", {})
    return {
        "text": text,
        "model": body.get("model", model),
        "tokens_in": usage.get("input_tokens", 0),
        "tokens_out": usage.get("output_tokens", 0),
    }


def llm_call(provider: str, stage: str, system: str, user: str, model: str) -> dict:
    if provider == "stub":
        return llm_call_stub(stage, system, user)
    if provider == "anthropic":
        return llm_call_anthropic(stage, system, user, model)
    raise ValueError(f"unsupported provider: {provider}")


def llm_grade_contract(text: str) -> dict:
    needed = ("goal", "acceptance", "evidence")
    found = [n for n in needed if re.search(n, text, re.I)]
    return {"required": list(needed), "found": found, "ok": len(found) == len(needed)}


def llm_grade_gate(text: str) -> dict:
    try:
        payload = json.loads(text)
        ok = bool(payload.get("matches_intent")) and payload.get("verdict") in ("pass", "warn")
        return {"parsed": True, "verdict": payload.get("verdict"), "score": payload.get("score"), "ok": ok}
    except Exception:
        # Lenient fallback: look for verdict keyword.
        m = re.search(r"verdict[\"'\s:]*([a-z]+)", text, re.I)
        verdict = m.group(1).lower() if m else None
        return {"parsed": False, "verdict": verdict, "score": None, "ok": verdict in ("pass", "warn")}


# --- autopilot: autonomous harness-engineering closed loop ---------------
#
# A runnable end-to-end orchestrator that takes one user prompt and walks it
# through intent → spec → design → ralph-loop implementation → simplifier →
# output-quality-gate → memory capture, writing every artifact to a per-run
# workspace so the loop is auditable and resumable.

AUTOPILOT_PHASES = [
    # (id, label, canonical_skill, output_filename, system_prefix)
    ("00-research", "Research",             "requirement-analysis",   "00-research.md",
        "Apply `requirement-analysis` (and draw on `user-research`/`market-research` framings if relevant). Output a compact research note with sections: Problem statement, Target users, Competitor landscape (1-3 bullets), Key assumptions to validate, Open questions, Trace. No solution proposed yet."),
    ("01-intent",   "Intent Contract",      "intent-contract",        "01-intent-contract.md",
        "Apply the Super Skill `intent-contract` skill below. Produce a compact contract with sections Goal, Acceptance, Out of scope, Evidence, Trace. No implementation."),
    ("02-spec",     "Product Spec",         "product-spec",           "02-product-spec.md",
        "Apply `product-spec`. Convert the contract into a PRD with MVP slice, success metrics, and rollout plan. Markdown only."),
    ("03-design",   "Design Direction",     "design-templates",       "03-design.md",
        "Apply `design-templates`. Output a small DESIGN.md with Purpose, Aesthetic Direction, Color Palette (hex), Typography, Layout Strategy. Avoid AI-slop defaults."),
    ("04-impl",     "Implementation (Ralph loop)", "ralph-loop",      "04-implementation.md",
        "Apply `ralph-loop`. Implement the MVP from the contract+PRD+DESIGN. Output the deliverable code or text. After it, list the exit-condition checklist actually met."),
    ("05-simplify", "Code Simplifier",      "code-simplifier",        "05-simplified.md",
        "Apply `code-simplifier`. Remove dead code, premature abstractions, redundant comments, future-proofing shims. Preserve observable behavior. Output the simplified deliverable."),
    ("06-gate",     "Output Quality Gate",  "output-quality-gate",    "06-quality-gate.json",
        "Apply `output-quality-gate`. Score the simplified deliverable against the original contract. Strict JSON only: "
        '{"matches_intent": bool, "evidence_present": bool, "missing": [str], "score": int(0..10), "verdict": "pass"|"warn"|"fail", "trace": str}.'),
    ("07-delivery", "Delivery Plan",        "deployment-patterns",    "07-delivery.md",
        "Apply `deployment-patterns` (and draw on `experiment-driven-delivery`/`observability-triage-loop` for rollout + monitoring). Output a delivery plan with: Dockerfile sketch (or non-containerized equivalent), CI workflow outline (.github/workflows/ci.yml shape), Feature flag + kill switch plan, Observability hooks (logs / metrics / errors), Rollback plan, Release notes draft, Trace."),
    ("08-memory",   "Memory Candidate",     "agent-memory-dream-loop","08-memory-candidate.md",
        "Apply `agent-memory-dream-loop`. Produce ONE reviewable memory candidate as plain text. Include Type, Scope, Claim, Evidence, Use when, Do not use when, Expiry. Never include raw user prompt or raw model response — summarise."),
]


def autopilot_run_id() -> str:
    # Include milliseconds so two runs in the same second still sort correctly.
    now = time.time()
    base = time.strftime("%Y%m%d-%H%M%S", time.localtime(now))
    millis = int((now - int(now)) * 1000)
    return f"{base}-{millis:03d}-{uuid.uuid4().hex[:6]}"


def autopilot_workspace(project: Path, run_id: str) -> Path:
    return project / ".super-skill" / "autopilot" / run_id


CODE_BLOCK_RE = re.compile(r"```(\w+)?\s*\n(.*?)```", re.S)
# Match optional file headers above a fenced block. Accepts these shapes:
#   ### file: src/main.py     |   File: src/main.py     |   `src/main.py`
FILE_HEADER_RE = re.compile(
    r"(?:^|\n)\s*(?:#+\s*)?(?:[Ff]ile\s*:\s*|`)([\w./\-]+\.[a-zA-Z0-9]+)`?\s*\n+```(\w+)?\s*\n(.*?)```",
    re.S,
)


LANG_EXT = {
    "python": "py", "py": "py",
    "javascript": "js", "js": "js", "node": "js",
    "typescript": "ts", "ts": "ts",
    "bash": "sh", "shell": "sh", "sh": "sh",
    "go": "go", "golang": "go",
}


def autopilot_extract_code(text: str) -> tuple[str | None, str]:
    """Extract the largest fenced code block + its language hint. If no fences,
    treat the whole text as a candidate. Returns (lang_hint, code).

    For multi-file extraction, see autopilot_extract_files."""
    blocks = CODE_BLOCK_RE.findall(text)
    if blocks:
        lang, code = max(blocks, key=lambda b: len(b[1]))
        return (lang.lower() if lang else None, code.strip())
    if re.search(r"^\s*(def |class |import |from \w+ import)", text, re.M):
        return ("python", text.strip())
    return (None, text.strip())


def autopilot_extract_files(text: str) -> list[tuple[str, str | None, str]]:
    """Return a list of (path, lang_hint, code) tuples.

    Recognises 'file: <path>' headers immediately above fenced blocks. If no
    headers are present, falls back to the legacy single-block extraction and
    synthesises a path of `candidate.<ext>` based on the language hint.
    """
    headed = FILE_HEADER_RE.findall(text)
    if headed:
        return [(p.strip(), (lang.lower() if lang else None), code.strip()) for p, lang, code in headed]
    lang, code = autopilot_extract_code(text)
    if not code:
        return []
    ext = LANG_EXT.get(lang or "", "py")
    return [(f"candidate.{ext}", lang, code)]


def autopilot_dominant_language(files: list[tuple[str, str | None, str]]) -> str | None:
    """Pick the language to run tests against. Prefers explicit lang hint,
    falls back to file extension."""
    for path, lang, _code in files:
        if lang:
            return lang
        if "." in path:
            ext = path.rsplit(".", 1)[1].lower()
            for k, v in LANG_EXT.items():
                if v == ext:
                    return k
    return None


def autopilot_run_python_tests(code: str, workdir: Path, timeout: int = 30) -> dict:
    """Verify Python code generated by phase 4 by actually running it.

    Strategy:
      - If the code has `class X(unittest.TestCase)`, run `python -m unittest`.
      - Else if it has bare `def test_*(...)` functions, generate a runner that
        imports the module and calls every test_* callable — failure raises.
      - Else byte-compile only (must at least parse).

    Returns {ok, kind, returncode, argv, stdout_tail, stderr_tail}.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    candidate = workdir / "candidate.py"
    candidate.write_text(code + "\n", encoding="utf-8")

    has_testcase = bool(re.search(r"^\s*class\s+\w+\(.*TestCase", code, re.M))
    bare_tests = re.findall(r"^\s*def\s+(test_\w+)\s*\(\s*\)", code, re.M)

    try:
        if has_testcase:
            argv = [sys.executable, "-m", "unittest", "candidate"]
            kind = "unittest"
        elif bare_tests:
            runner = workdir / "run_tests.py"
            runner.write_text(textwrap.dedent(f"""\
                import candidate, sys
                _failed = 0
                for _name in {bare_tests!r}:
                    try:
                        getattr(candidate, _name)()
                    except Exception as exc:
                        _failed += 1
                        print(f'FAIL {{_name}}: {{exc!r}}', file=sys.stderr)
                sys.exit(1 if _failed else 0)
                """), encoding="utf-8")
            argv = [sys.executable, "run_tests.py"]
            kind = "bare-tests"
        else:
            argv = [sys.executable, "-m", "py_compile", str(candidate)]
            kind = "py-compile"
        proc = subprocess.run(argv, cwd=workdir, capture_output=True, text=True, timeout=timeout, check=False)
        return {
            "ok": proc.returncode == 0,
            "kind": kind,
            "returncode": proc.returncode,
            "argv": argv,
            "stdout_tail": proc.stdout[-800:],
            "stderr_tail": proc.stderr[-800:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "kind": "exception", "error": str(exc)}


def autopilot_run_javascript(code: str, workdir: Path, ext: str = "js", timeout: int = 30) -> dict:
    """Verify JavaScript/TypeScript: write candidate.<ext>, run with node.

    Strategy: if code defines bare `function test_<name>()` or `test('name', ...)`
    helpers, generate a runner that calls them. Otherwise just `node candidate.js`
    (must execute without uncaught error)."""
    if not shutil.which("node"):
        return {"ok": True, "kind": "skipped", "reason": "node not on PATH"}
    workdir.mkdir(parents=True, exist_ok=True)
    candidate = workdir / f"candidate.{ext}"
    candidate.write_text(code + "\n", encoding="utf-8")
    bare_tests = re.findall(r"^\s*(?:export\s+)?function\s+(test_\w+)\s*\(\s*\)", code, re.M)
    if bare_tests:
        runner = workdir / "run_tests.js"
        names = json.dumps(bare_tests)
        runner.write_text(textwrap.dedent(f"""\
            const mod = require('./{candidate.name}');
            const names = {names};
            let failed = 0;
            for (const name of names) {{
                try {{
                    if (typeof mod[name] === 'function') mod[name]();
                    else if (typeof globalThis[name] === 'function') globalThis[name]();
                    else throw new Error('not exported');
                }} catch (e) {{
                    failed++;
                    process.stderr.write(`FAIL ${{name}}: ${{e.message || e}}\\n`);
                }}
            }}
            process.exit(failed ? 1 : 0);
            """), encoding="utf-8")
        # Re-write candidate to ensure tests are exported under module.exports.
        export_block = "\nmodule.exports = { " + ", ".join(bare_tests) + " };\n"
        candidate.write_text(code + export_block, encoding="utf-8")
        argv = ["node", "run_tests.js"]
        kind = "node-bare-tests"
    else:
        argv = ["node", candidate.name]
        kind = "node-exec"
    try:
        proc = subprocess.run(argv, cwd=workdir, capture_output=True, text=True, timeout=timeout, check=False)
        return {
            "ok": proc.returncode == 0,
            "kind": kind,
            "returncode": proc.returncode,
            "argv": argv,
            "stdout_tail": proc.stdout[-800:],
            "stderr_tail": proc.stderr[-800:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "kind": "exception", "error": str(exc)}


def autopilot_run_bash(code: str, workdir: Path, timeout: int = 30) -> dict:
    """Verify Bash: write candidate.sh, run `bash -n` (parse-check) and then
    execute. Many shell scripts are side-effecting, so 'parse-check passed'
    is the safest non-destructive default; we only execute if the code looks
    like it terminates quickly (presence of `set -e` plus no obvious loops)."""
    if not shutil.which("bash"):
        return {"ok": True, "kind": "skipped", "reason": "bash not on PATH"}
    workdir.mkdir(parents=True, exist_ok=True)
    candidate = workdir / "candidate.sh"
    candidate.write_text(code + "\n", encoding="utf-8")
    try:
        # Always parse-check.
        parse = subprocess.run(["bash", "-n", str(candidate)], cwd=workdir, capture_output=True, text=True, timeout=timeout, check=False)
        if parse.returncode != 0:
            return {
                "ok": False, "kind": "bash-parse",
                "returncode": parse.returncode, "argv": ["bash", "-n", candidate.name],
                "stdout_tail": parse.stdout[-800:], "stderr_tail": parse.stderr[-800:],
            }
        # Execute only if it looks safe.
        is_safe_to_run = "set -e" in code or "set -euo pipefail" in code
        is_safe_to_run = is_safe_to_run and not re.search(r"\b(rm\s+-rf|sudo|curl|wget|>\s*/dev|kill\s+-9)\b", code)
        if not is_safe_to_run:
            return {"ok": True, "kind": "bash-parse-only", "returncode": 0, "argv": ["bash", "-n", candidate.name],
                    "stdout_tail": "", "stderr_tail": "skipped execution: script lacks `set -e` or contains potentially destructive commands"}
        run = subprocess.run(["bash", str(candidate)], cwd=workdir, capture_output=True, text=True, timeout=timeout, check=False)
        return {
            "ok": run.returncode == 0, "kind": "bash-exec",
            "returncode": run.returncode, "argv": ["bash", candidate.name],
            "stdout_tail": run.stdout[-800:], "stderr_tail": run.stderr[-800:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "kind": "exception", "error": str(exc)}


def autopilot_run_go(code: str, workdir: Path, timeout: int = 60) -> dict:
    """Verify Go: write candidate.go, run `go vet` (then `go test ./...` if any
    `func Test*(t *testing.T)` is present)."""
    if not shutil.which("go"):
        return {"ok": True, "kind": "skipped", "reason": "go not on PATH"}
    workdir.mkdir(parents=True, exist_ok=True)
    candidate = workdir / "candidate.go"
    candidate.write_text(code + "\n", encoding="utf-8")
    has_tests = bool(re.search(r"^\s*func\s+Test\w+\s*\(\s*\w+\s*\*testing\.T\s*\)", code, re.M))
    try:
        # `go vet` works without a module file in older versions; init a module first.
        subprocess.run(["go", "mod", "init", "candidate"], cwd=workdir, capture_output=True, text=True, timeout=timeout, check=False)
        if has_tests:
            argv = ["go", "test", "./..."]
            kind = "go-test"
        else:
            argv = ["go", "vet", "./..."]
            kind = "go-vet"
        proc = subprocess.run(argv, cwd=workdir, capture_output=True, text=True, timeout=timeout, check=False)
        return {
            "ok": proc.returncode == 0,
            "kind": kind, "returncode": proc.returncode, "argv": argv,
            "stdout_tail": proc.stdout[-800:], "stderr_tail": proc.stderr[-800:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "kind": "exception", "error": str(exc)}


def autopilot_test_implementation(text: str, workdir: Path) -> dict:
    """Verify phase-4 output. Multi-file aware; supports Python, JS/TS, Bash, Go.

    For multi-file output (recognised by `file: <path>` headers above fenced
    blocks), every file is written first, then the runner picks up the dominant
    language and runs verification against the file at conventional name (Python
    runs against the longest .py file written; JS uses candidate.js if present;
    etc.).

    For unknown languages or missing toolchains, returns kind=skipped with a
    reason — the ralph loop's length heuristic still proceeds.
    """
    files = autopilot_extract_files(text)
    if not files:
        return {"ok": False, "kind": "skipped", "reason": "no extractable code"}

    workdir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for path, _lang, code in files:
        target = workdir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(code + "\n", encoding="utf-8")
        written.append(target)

    lang = autopilot_dominant_language(files)

    if lang in ("python", "py"):
        # Re-use the existing runner against the longest .py file in workdir.
        py_files = sorted([p for p in written if p.suffix == ".py"], key=lambda p: -p.stat().st_size)
        target = py_files[0] if py_files else written[0]
        return autopilot_run_python_tests(target.read_text(encoding="utf-8"), workdir)
    if lang in ("javascript", "js", "node"):
        target = next((p for p in written if p.suffix == ".js"), written[0])
        return autopilot_run_javascript(target.read_text(encoding="utf-8"), workdir, ext="js")
    if lang in ("typescript", "ts"):
        target = next((p for p in written if p.suffix == ".ts"), written[0])
        return autopilot_run_javascript(target.read_text(encoding="utf-8"), workdir, ext="ts")
    if lang in ("bash", "shell", "sh"):
        target = next((p for p in written if p.suffix == ".sh"), written[0])
        return autopilot_run_bash(target.read_text(encoding="utf-8"), workdir)
    if lang in ("go", "golang"):
        target = next((p for p in written if p.suffix == ".go"), written[0])
        return autopilot_run_go(target.read_text(encoding="utf-8"), workdir)
    return {"ok": True, "kind": "skipped", "reason": f"unsupported language: {lang}"}


def autopilot_grade_intent(text: str) -> dict:
    needed = ("goal", "acceptance", "evidence")
    found = [n for n in needed if re.search(n, text, re.I)]
    return {"required": list(needed), "found": found, "ok": len(found) == len(needed)}


def autopilot_grade_gate(text: str) -> dict:
    try:
        body = json.loads(text)
        verdict = body.get("verdict")
        return {
            "parsed": True,
            "verdict": verdict,
            "score": body.get("score"),
            "missing": body.get("missing", []),
            "ok": bool(body.get("matches_intent")) and verdict in ("pass", "warn"),
        }
    except Exception:
        m = re.search(r"verdict[\"'\s:]*([a-z]+)", text, re.I)
        return {"parsed": False, "verdict": (m.group(1).lower() if m else None), "score": None, "ok": False}


def autopilot_run_phase(
    phase: tuple,
    provider: str,
    model: str,
    user_prompt: str,
    prior_artifacts: dict[str, str],
    workspace: Path,
    force: bool,
    iteration: dict | None = None,
) -> dict:
    """Run one autopilot phase.

    `iteration`, when provided, is the iterate-mode context:
        {"parent_run_id": str, "feedback": str, "parent_artifacts": dict[str,str]}
    The parent run's artifact for the SAME phase is fed in as a 'Prior version'
    so the LLM produces an incremental update rather than re-deriving from
    scratch. The user's new feedback is front-loaded as the first context line.
    """
    phase_id, label, canonical, filename, system_prefix = phase
    out_path = workspace / filename
    if out_path.exists() and not force:
        text = out_path.read_text(encoding="utf-8")
        return {
            "phase": phase_id,
            "label": label,
            "skill": canonical,
            "output": str(out_path),
            "tokens_in": 0,
            "tokens_out": 0,
            "skipped": True,
            "text": text,
        }

    skill_body = llm_load_skill_body(canonical)
    context_lines = [f"User request: {user_prompt}"]
    if iteration:
        if iteration.get("feedback"):
            context_lines.append(f"\n=== New feedback (drives this iteration) ===\n{iteration['feedback']}")
        prior_for_phase = (iteration.get("parent_artifacts") or {}).get(phase_id)
        if prior_for_phase:
            snippet = prior_for_phase if len(prior_for_phase) <= 4000 else prior_for_phase[:4000] + "\n[...truncated]"
            context_lines.append(
                f"\n=== Prior version of this phase (run {iteration.get('parent_run_id','?')}) ===\n{snippet}\n"
                "Produce an UPDATED version that addresses the new feedback while staying anchored to the prior intent."
            )
    for label_, content in prior_artifacts.items():
        snippet = content if len(content) <= 4000 else content[:4000] + "\n[...truncated]"
        context_lines.append(f"\n--- {label_} ---\n{snippet}")
    user_msg = "\n".join(context_lines)

    system_msg = system_prefix + "\n\n=== Canonical skill ===\n" + skill_body
    call = llm_call(provider, phase_id, system_msg, user_msg, model)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(call["text"] + "\n", encoding="utf-8")

    return {
        "phase": phase_id,
        "label": label,
        "skill": canonical,
        "output": str(out_path),
        "tokens_in": call.get("tokens_in", 0),
        "tokens_out": call.get("tokens_out", 0),
        "skipped": False,
        "text": call["text"],
    }


def autopilot_load_parent_run(project: Path, parent_run_id: str) -> dict:
    """Load a prior run's artifacts (keyed by phase id) and journal."""
    parent_dir = autopilot_workspace(project, parent_run_id)
    if not parent_dir.exists():
        raise FileNotFoundError(f"parent run not found: {parent_dir}")
    journal_path = parent_dir / "run.json"
    journal = read_json_file(journal_path) if journal_path.exists() else {}
    parent_artifacts: dict[str, str] = {}
    for phase_id, _label, _skill, filename, _prefix in AUTOPILOT_PHASES:
        path = parent_dir / filename
        if path.exists():
            parent_artifacts[phase_id] = path.read_text(encoding="utf-8")
    return {
        "parent_run_id": parent_run_id,
        "parent_workspace": str(parent_dir),
        "parent_journal": journal,
        "parent_artifacts": parent_artifacts,
    }


def cmd_autopilot(args: argparse.Namespace) -> int:
    provider = args.provider
    if provider == "auto":
        provider = "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "stub"
    model = args.model or {
        "anthropic": "claude-haiku-4-5-20251001",
        "stub": "stub-deterministic-v1",
    }.get(provider, "stub-deterministic-v1")

    project = Path(args.project).resolve()
    project.mkdir(parents=True, exist_ok=True)

    # Iterate mode: load parent run's artifacts + journal so each phase sees a
    # "Prior version" alongside the new feedback.
    iteration = None
    parent_run_id = getattr(args, "based_on", None)
    feedback = getattr(args, "feedback", None) or ""
    if parent_run_id:
        try:
            parent_ctx = autopilot_load_parent_run(project, parent_run_id)
        except FileNotFoundError as exc:
            emit_json(False, {"message": str(exc)}, code="USAGE") if args.json else print(str(exc))
            return EXIT_USAGE
        iteration = {
            "parent_run_id": parent_run_id,
            "feedback": feedback,
            "parent_artifacts": parent_ctx["parent_artifacts"],
        }
        # If user did not supply a prompt, inherit from parent for continuity.
        inherited_prompt = parent_ctx["parent_journal"].get("user_prompt")
        user_prompt = args.prompt or inherited_prompt or "Iterate on the prior run."
    else:
        user_prompt = args.prompt or "Build a small Python CLI that adds two numbers and ships with one unit test."

    run_id = args.run_id or autopilot_run_id()
    workspace = autopilot_workspace(project, run_id)
    workspace.mkdir(parents=True, exist_ok=True)

    skip = set((args.skip or "").split(",")) if args.skip else set()
    skip.discard("")

    phases_to_run = [p for p in AUTOPILOT_PHASES if p[0] not in skip]
    requested_skills = sorted({p[2] for p in phases_to_run})

    if args.dry_run:
        plan = {
            "run_id": run_id,
            "workspace": str(workspace),
            "provider": provider,
            "model": model,
            "phases_planned": [{"id": p[0], "label": p[1], "skill": p[2]} for p in phases_to_run],
            "skills_required": requested_skills,
            "max_ralph_rounds": args.max_ralph_rounds,
        }
        emit_json(True, plan) if args.json else print(json.dumps(plan, ensure_ascii=False, indent=2))
        return EXIT_OK

    artifacts: dict[str, str] = {}
    phase_results: list[dict] = []
    overall_ok = True
    failed_phase: str | None = None

    for phase in phases_to_run:
        phase_id = phase[0]
        # Ralph inner loop only wraps the implementation phase.
        if phase_id == "04-impl":
            attempts: list[dict] = []
            last_result: dict | None = None
            sandbox = workspace / "04-impl-sandbox"
            for attempt in range(1, args.max_ralph_rounds + 1):
                local_force = args.force or attempt > 1
                result = autopilot_run_phase(
                    phase, provider, model, user_prompt, artifacts, workspace,
                    force=local_force, iteration=iteration,
                )
                # First-line grader: non-empty / non-trivial output.
                length_ok = bool(result["text"].strip()) and len(result["text"]) > 20
                # Real-runner grader: extract code, run it (Python-aware; other langs skip cleanly).
                test_result = autopilot_test_implementation(result["text"], sandbox / f"attempt-{attempt}") if length_ok else {"ok": False, "kind": "skipped", "reason": "phase output too short"}
                impl_ok = length_ok and test_result["ok"]
                attempts.append({
                    "attempt": attempt,
                    "ok": impl_ok,
                    "length_ok": length_ok,
                    "test_kind": test_result.get("kind"),
                    "test_returncode": test_result.get("returncode"),
                    "test_stderr_tail": test_result.get("stderr_tail", "")[-300:],
                    "tokens_out": result["tokens_out"],
                })
                last_result = result
                if impl_ok:
                    break
                # Surface the actual failure to the next attempt — this is the
                # Ralph loop's "failure → retry with feedback" contract.
                feedback_lines = []
                if not length_ok:
                    feedback_lines.append("Previous attempt was empty or trivially short. Provide concrete code with at least one unit test.")
                if test_result.get("kind") == "py-compile":
                    feedback_lines.append("Previous attempt failed Python byte-compile.")
                elif test_result.get("kind") == "unittest":
                    feedback_lines.append("Previous attempt failed unit tests.")
                stderr = test_result.get("stderr_tail", "").strip()
                if stderr:
                    feedback_lines.append("Stderr:\n" + stderr[-600:])
                artifacts["Previous attempt error"] = "\n".join(feedback_lines) or "Previous attempt failed verification."
            result = last_result or result
            result["ralph_attempts"] = attempts
            result["ralph_passed"] = bool(attempts and attempts[-1]["ok"])
            artifacts.pop("Previous attempt error", None)
            phase_results.append(result)
            artifacts[phase[1]] = result["text"]
            if not result["ralph_passed"]:
                overall_ok = False
                failed_phase = phase_id
                break
            continue

        result = autopilot_run_phase(
            phase, provider, model, user_prompt, artifacts, workspace,
            force=args.force, iteration=iteration,
        )
        phase_results.append(result)
        artifacts[phase[1]] = result["text"]

        # Hard gates: phase 1 contract must pass; phase 6 quality gate must pass.
        if phase_id == "01-intent":
            grade = autopilot_grade_intent(result["text"])
            result["grade"] = grade
            if not grade["ok"]:
                overall_ok = False
                failed_phase = phase_id
                break
        elif phase_id == "06-gate":
            grade = autopilot_grade_gate(result["text"])
            result["grade"] = grade
            if not grade["ok"]:
                overall_ok = False
                failed_phase = phase_id
                break

    # Build lineage chain: walk parent_run_id pointers backwards.
    lineage: list[str] = []
    if iteration:
        lineage.append(parent_run_id)
        cursor = parent_run_id
        seen = {cursor, run_id}
        while True:
            try:
                journal = read_json_file(autopilot_workspace(project, cursor) / "run.json")
            except (FileNotFoundError, json.JSONDecodeError):
                break
            ancestor = journal.get("parent_run_id")
            if not ancestor or ancestor in seen:
                break
            seen.add(ancestor)
            lineage.append(ancestor)
            cursor = ancestor

    # Persist the run journal.
    run_journal = {
        "run_id": run_id,
        "workspace": str(workspace),
        "provider": provider,
        "model": model,
        "user_prompt": user_prompt,
        "started_at": int(time.time()),
        "parent_run_id": parent_run_id if iteration else None,
        "feedback": feedback if iteration else None,
        "lineage": lineage,
        "phases": [
            {k: v for k, v in pr.items() if k != "text"}
            for pr in phase_results
        ],
        "ok": overall_ok,
        "failed_phase": failed_phase,
        "skipped": sorted(skip),
    }
    (workspace / "run.json").write_text(json.dumps(run_journal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    payload = dict(run_journal)
    if args.show_outputs:
        payload["outputs"] = {pr["phase"]: pr.get("text", "") for pr in phase_results}

    if args.json:
        emit_json(overall_ok, payload, code="AUTOPILOT_FAILED" if not overall_ok else None)
    else:
        print(f"autopilot run: {run_id}")
        print(f"  workspace: {workspace}")
        print(f"  provider: {provider}  model: {model}")
        for pr in phase_results:
            tag = "skipped" if pr.get("skipped") else "ran"
            extra = ""
            if pr.get("ralph_attempts"):
                extra = f"  ralph={len(pr['ralph_attempts'])} attempts pass={pr.get('ralph_passed')}"
            grade = pr.get("grade")
            if grade:
                extra += f"  grade={grade}"
            print(f"  [{pr['phase']}] {pr['label']:24s} {tag:7s} tokens_out={pr.get('tokens_out')}{extra}")
        if failed_phase:
            print(f"  FAILED at: {failed_phase}")
        print(f"overall: {'PASS' if overall_ok else 'FAIL'}")
    return EXIT_OK if overall_ok else EXIT_RUNTIME


def autopilot_render_html(journal: dict, run_dir: Path) -> str:
    """Render an autopilot run.json as a single self-contained HTML timeline.

    No external deps. Inlines tiny CSS. The page shows: header (run id,
    provider, model, prompt summary, overall verdict), phase timeline cards
    with per-phase token counts and grade badges, and a foldable ralph-loop
    attempts table for phase 4.
    """
    def esc(s: str) -> str:
        return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    overall_ok = bool(journal.get("ok"))
    badge_color = "#14B8A6" if overall_ok else "#F97316"
    verdict = "PASS" if overall_ok else "FAIL"
    failed = journal.get("failed_phase") or "—"
    started = journal.get("started_at")
    started_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(started)) if started else "—"
    parent_run_id = journal.get("parent_run_id")
    feedback = journal.get("feedback") or ""
    lineage = journal.get("lineage") or []

    phase_cards: list[str] = []
    for ph in journal.get("phases", []):
        skipped = ph.get("skipped")
        ok = True
        grade = ph.get("grade") or {}
        if "ok" in grade and not grade["ok"]:
            ok = False
        if ph.get("ralph_passed") is False:
            ok = False
        status_label = "skipped" if skipped else ("ok" if ok else "fail")
        status_color = "#94A3B8" if skipped else ("#14B8A6" if ok else "#F97316")

        attempts_html = ""
        if ph.get("ralph_attempts"):
            rows = ""
            for a in ph["ralph_attempts"]:
                rc = a.get("test_returncode")
                rows += (
                    f"<tr>"
                    f"<td>{a['attempt']}</td>"
                    f"<td>{esc(a.get('test_kind') or '')}</td>"
                    f"<td>{rc if rc is not None else '—'}</td>"
                    f"<td>{'✓' if a['ok'] else '✗'}</td>"
                    f"<td>{a.get('tokens_out')}</td>"
                    f"<td><pre>{esc((a.get('test_stderr_tail') or '').strip()[:240])}</pre></td>"
                    f"</tr>"
                )
            attempts_html = (
                "<details class='attempts'><summary>Ralph attempts</summary>"
                "<table><thead><tr><th>#</th><th>kind</th><th>rc</th><th>ok</th><th>tokens_out</th><th>stderr_tail</th></tr></thead>"
                f"<tbody>{rows}</tbody></table></details>"
            )

        grade_pill = ""
        if grade:
            ok_ = grade.get("ok")
            verdict_ = grade.get("verdict")
            score_ = grade.get("score")
            text = (
                ("verdict=" + verdict_ + " score=" + str(score_)) if verdict_ else
                ("ok" if ok_ else "fail")
            )
            color = "#14B8A6" if ok_ else "#F97316"
            grade_pill = f"<span class='pill' style='background:{color}'>{esc(text)}</span>"

        phase_cards.append(
            f"<article class='phase'>"
            f"<header><h3>{esc(ph['phase'])} · {esc(ph['label'])}</h3>"
            f"<span class='pill' style='background:{status_color}'>{status_label}</span>"
            f"{grade_pill}</header>"
            f"<dl>"
            f"<dt>skill</dt><dd><code>{esc(ph['skill'])}</code></dd>"
            f"<dt>tokens</dt><dd>in={ph.get('tokens_in')} · out={ph.get('tokens_out')}</dd>"
            f"<dt>output</dt><dd><code>{esc(Path(ph.get('output','')).name)}</code></dd>"
            f"</dl>"
            f"{attempts_html}"
            f"</article>"
        )

    css = """
        :root { --bg:#0F172A; --fg:#F1F5F9; --muted:#94A3B8; --pill-fg:#0F172A; }
        body { background:var(--bg); color:var(--fg); font-family: 'Source Serif Pro','Charter','Iowan Old Style',Georgia,serif; max-width:960px; margin:2rem auto; padding:0 1rem; }
        h1 { font-size:2.2rem; margin:0 0 0.4rem; }
        .meta { color:var(--muted); font-family: 'JetBrains Mono','Menlo',monospace; font-size:.85rem; margin-bottom:2rem; }
        .verdict { font-size:1.4rem; font-weight:700; padding:0.4rem 1rem; border-radius:0.4rem; color:var(--pill-fg); }
        .timeline { display:grid; gap:1rem; }
        .phase { background:rgba(255,255,255,0.04); border-left:4px solid var(--muted); padding:0.8rem 1.2rem; border-radius:0 0.4rem 0.4rem 0; }
        .phase header { display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap; }
        .phase header h3 { margin:0; flex:1 1 100%; font-size:1.05rem; }
        .pill { color:var(--pill-fg); padding:0.15rem 0.55rem; border-radius:1rem; font-size:0.75rem; font-family: 'JetBrains Mono',monospace; font-weight:600; }
        dl { display:grid; grid-template-columns: max-content 1fr; gap:0.2rem 0.8rem; margin:0.6rem 0; font-size:0.9rem; }
        dt { color:var(--muted); }
        code { font-family: 'JetBrains Mono',monospace; font-size:0.85em; }
        details.attempts { margin-top:0.6rem; }
        details summary { cursor:pointer; color:var(--muted); font-family:'JetBrains Mono',monospace; font-size:0.8rem; }
        table { width:100%; border-collapse:collapse; margin-top:0.4rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem; }
        th, td { text-align:left; padding:0.3rem 0.5rem; border-bottom:1px solid rgba(255,255,255,0.08); vertical-align:top; }
        pre { margin:0; white-space:pre-wrap; word-break:break-word; max-width:36ch; }
    """
    user_prompt = esc(journal.get("user_prompt", "")[:200])
    run_id = esc(journal.get("run_id", run_dir.name))

    lineage_block = ""
    if parent_run_id or lineage:
        chain_items = [f"<code>{esc(run_id)}</code> <em>(this run)</em>"]
        for ancestor in [parent_run_id] + [a for a in lineage if a != parent_run_id]:
            if ancestor:
                chain_items.append(f"<code>{esc(ancestor)}</code>")
        chain = " ← ".join(chain_items)
        feedback_html = f"<p style='color:var(--muted);'><strong>Feedback:</strong> “{esc(feedback)}”</p>" if feedback else ""
        lineage_block = (
            "<section class='lineage'>"
            f"<h2>Lineage</h2><p>{chain}</p>{feedback_html}"
            "</section>"
        )

    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><title>Autopilot · {run_id}</title>
<style>{css}
.lineage {{ background:rgba(20,184,166,0.08); border-left:4px solid #14B8A6; padding:0.6rem 1rem; border-radius:0 0.4rem 0.4rem 0; margin:0 0 1.2rem; }}
.lineage h2 {{ font-size:0.95rem; color:var(--muted); margin:0 0 0.4rem; font-family:'JetBrains Mono',monospace; text-transform:uppercase; letter-spacing:0.06em; }}
.lineage p {{ margin:0; font-family:'JetBrains Mono',monospace; font-size:0.82rem; }}
</style></head><body>
<h1>Autopilot run</h1>
<div class='meta'>
  <span class='verdict' style='background:{badge_color}'>{verdict}</span>
  &nbsp;run-id <code>{run_id}</code>
  · provider <code>{esc(journal.get('provider',''))}</code>
  · model <code>{esc(journal.get('model',''))}</code>
  · started {started_str}
  · failed-phase <code>{esc(failed)}</code>
</div>
<p style='color:var(--muted);font-style:italic;'>“{user_prompt}”</p>
{lineage_block}
<section class='timeline'>{''.join(phase_cards)}</section>
</body></html>
"""


def cmd_visualize(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    base = project / ".super-skill" / "autopilot"
    if not base.exists():
        emit_json(False, {"message": f"no autopilot runs under {base}"}, code="USAGE") if args.json else print(f"no autopilot runs under {base}")
        return EXIT_USAGE
    runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name)
    if not runs:
        emit_json(False, {"message": "no runs to visualize"}, code="USAGE") if args.json else print("no runs to visualize")
        return EXIT_USAGE
    target = (base / args.run_id) if args.run_id else runs[-1]
    journal_path = target / "run.json"
    if not journal_path.exists():
        emit_json(False, {"message": f"missing run.json: {journal_path}"}, code="USAGE") if args.json else print(f"missing run.json: {journal_path}")
        return EXIT_USAGE
    journal = read_json_file(journal_path)
    html = autopilot_render_html(journal, target)
    out_path = Path(args.output) if args.output else target / "timeline.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    payload = {"run_id": target.name, "output": str(out_path), "bytes": len(html)}
    if args.json:
        emit_json(True, payload)
    else:
        print(f"wrote {out_path} ({len(html)} bytes)")
    return EXIT_OK


def cmd_resume(args: argparse.Namespace) -> int:
    """Resume an autopilot run. Two modes:
       - --run-id <id>: resume that specific run
       - default: pick the latest run under <project>/.super-skill/autopilot/

    Resume IS autopilot with --run-id and without --force, but as its own
    command it surfaces the workflow more clearly and prints what's pending.
    """
    project = Path(args.project).resolve()
    base = project / ".super-skill" / "autopilot"
    if not base.exists():
        emit_json(False, {"message": f"no autopilot runs under {base}"}, code="USAGE") if args.json else print(f"no autopilot runs under {base}")
        return EXIT_USAGE

    runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name)
    if not runs:
        emit_json(False, {"message": "no runs to resume"}, code="USAGE") if args.json else print("no runs to resume")
        return EXIT_USAGE

    if args.run_id:
        target = base / args.run_id
        if not target.exists():
            emit_json(False, {"message": f"run id not found: {args.run_id}", "available": [p.name for p in runs]}, code="USAGE") if args.json else print(f"run id not found: {args.run_id}")
            return EXIT_USAGE
    else:
        target = runs[-1]

    journal_path = target / "run.json"
    journal: dict = read_json_file(journal_path) if journal_path.exists() else {}
    completed = {p["phase"] for p in journal.get("phases", []) if p.get("output") and Path(p["output"]).exists()}
    pending = [p[0] for p in AUTOPILOT_PHASES if p[0] not in completed]

    if args.list:
        payload = {
            "project": str(project),
            "run_id": target.name,
            "completed_phases": sorted(completed),
            "pending_phases": pending,
            "journal_ok": journal.get("ok"),
            "user_prompt": journal.get("user_prompt"),
        }
        if args.json:
            emit_json(True, payload)
        else:
            print(f"resume target: {target.name}")
            print(f"  completed: {sorted(completed)}")
            print(f"  pending:   {pending}")
        return EXIT_OK

    # Delegate to autopilot with --run-id; force=False so completed phases skip.
    forwarded = argparse.Namespace(
        prompt=journal.get("user_prompt") or args.prompt,
        provider=args.provider,
        model=args.model,
        project=str(project),
        run_id=target.name,
        max_ralph_rounds=args.max_ralph_rounds,
        skip=args.skip,
        force=False,
        dry_run=args.dry_run,
        show_outputs=args.show_outputs,
        json=args.json,
    )
    return cmd_autopilot(forwarded)


def cmd_llm_eval(args: argparse.Namespace) -> int:
    provider = args.provider
    if provider == "auto":
        provider = "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "stub"
    model = args.model or {
        "anthropic": "claude-haiku-4-5-20251001",
        "stub": "stub-deterministic-v1",
    }.get(provider, "stub-deterministic-v1")
    user_prompt = args.prompt or LLM_DEFAULT_PROMPT

    try:
        intent_skill = llm_load_skill_body("intent-contract")
        gate_skill = llm_load_skill_body("output-quality-gate")
    except FileNotFoundError as exc:
        emit_json(False, {"message": str(exc)}, code="USAGE")
        return EXIT_USAGE

    # Phase 1: contract
    contract_call = llm_call(
        provider,
        "contract",
        system=(
            "You apply the Super Skill `intent-contract` skill below. Output a "
            "compact contract (Goal, Acceptance, Out of scope, Evidence) for the "
            "user request. Do not implement anything yet.\n\n" + intent_skill
        ),
        user=user_prompt,
        model=model,
    )
    contract_grade = llm_grade_contract(contract_call["text"])

    # Phase 2: implementation against the contract
    impl_call = llm_call(
        provider,
        "implementation",
        system=(
            "You implement the deliverable that satisfies the contract below. "
            "Return only the final code or text, no commentary."
        ),
        user=f"Contract:\n{contract_call['text']}\n\nOriginal request: {user_prompt}",
        model=model,
    )

    # Phase 3: output-quality-gate
    gate_call = llm_call(
        provider,
        "gate",
        system=(
            "You apply the Super Skill `output-quality-gate` skill below. Score "
            "the deliverable against the contract. Respond with strict JSON: "
            '{"matches_intent": bool, "evidence_present": bool, "missing": [str], '
            '"score": int(0..10), "verdict": "pass"|"warn"|"fail", "trace": str}. '
            "No prose.\n\n" + gate_skill
        ),
        user=f"Contract:\n{contract_call['text']}\n\nDeliverable:\n{impl_call['text']}",
        model=model,
    )
    gate_grade = llm_grade_gate(gate_call["text"])

    overall_ok = contract_grade["ok"] and gate_grade["ok"]
    payload = {
        "provider": provider,
        "model": model,
        "user_prompt": user_prompt,
        "phases": [
            {"stage": "contract", "tokens_in": contract_call.get("tokens_in"), "tokens_out": contract_call.get("tokens_out"), "grade": contract_grade},
            {"stage": "implementation", "tokens_in": impl_call.get("tokens_in"), "tokens_out": impl_call.get("tokens_out")},
            {"stage": "gate", "tokens_in": gate_call.get("tokens_in"), "tokens_out": gate_call.get("tokens_out"), "grade": gate_grade},
        ],
        "ok": overall_ok,
    }
    if args.show_outputs:
        payload["outputs"] = {
            "contract": contract_call["text"],
            "implementation": impl_call["text"],
            "gate": gate_call["text"],
        }
    if args.json:
        emit_json(overall_ok, payload, code="LLM_EVAL_FAILED" if not overall_ok else None)
    else:
        print(f"llm-eval: provider={provider} model={model}")
        print(f"  prompt: {user_prompt[:80]}")
        for ph in payload["phases"]:
            line = f"  [{ph['stage']:14s}] tokens_in={ph.get('tokens_in')} tokens_out={ph.get('tokens_out')}"
            if ph.get("grade"):
                line += f" grade={ph['grade']}"
            print(line)
        print(f"overall: {'PASS' if overall_ok else 'FAIL'}")
    return EXIT_OK if overall_ok else EXIT_RUNTIME


def profile_manifest_report() -> tuple[list[dict], list[dict]]:
    errors: list[dict] = []
    warnings: list[dict] = []
    profiles_path = MANIFEST_ROOT / "install-profiles.json"
    components_path = MANIFEST_ROOT / "install-components.json"

    if not profiles_path.exists():
        errors.append({"check": "manifest", "message": "missing manifests/install-profiles.json"})
    if not components_path.exists():
        errors.append({"check": "manifest", "message": "missing manifests/install-components.json"})
    if errors:
        return errors, warnings

    try:
        profiles = read_json_file(profiles_path)
        components = read_json_file(components_path)
    except json.JSONDecodeError as exc:
        errors.append({"check": "manifest", "message": f"invalid manifest JSON: {exc}"})
        return errors, warnings

    component_ids = {item.get("id") for item in components.get("components", [])}
    installable_names = {skill.name for skill in discover_skills("all")}
    for profile_name, expected_stages in sorted(PROFILE_STAGE_PREFIXES.items()):
        profile = profiles.get("profiles", {}).get(profile_name)
        if not profile:
            errors.append({"check": "manifest", "message": f"profile missing from manifest: {profile_name}"})
            continue
        stages = set(profile.get("stages", []))
        if stages != expected_stages:
            errors.append(
                {
                    "check": "manifest",
                    "message": f"profile stage drift: {profile_name}",
                    "expected": sorted(expected_stages),
                    "actual": sorted(stages),
                }
            )
        for component_id in profile.get("components", []):
            if component_id not in component_ids:
                errors.append(
                    {
                        "check": "manifest",
                        "message": f"profile references unknown component: {profile_name} -> {component_id}",
                    }
                )
        manifest_excludes = set(profile.get("excludes", []))
        expected_excludes = PROFILE_SKILL_EXCLUDES.get(profile_name, set())
        if manifest_excludes != expected_excludes:
            errors.append(
                {
                    "check": "manifest",
                    "message": f"profile exclude drift: {profile_name}",
                    "expected": sorted(expected_excludes),
                    "actual": sorted(manifest_excludes),
                }
            )
        unknown_excludes = manifest_excludes - installable_names
        if unknown_excludes:
            errors.append(
                {
                    "check": "manifest",
                    "message": f"profile excludes unknown skill: {profile_name}",
                    "items": sorted(unknown_excludes),
                }
            )

    manifest_profiles = set(profiles.get("profiles", {}))
    extra = manifest_profiles - set(PROFILE_STAGE_PREFIXES)
    if extra:
        warnings.append({"check": "manifest", "message": f"manifest-only profiles: {', '.join(sorted(extra))}"})
    return errors, warnings


def plugin_manifest_report() -> tuple[list[dict], list[dict]]:
    errors: list[dict] = []
    warnings: list[dict] = []
    if not PLUGIN_ROOT.exists():
        return errors, warnings

    for manifest_path in sorted(PLUGIN_ROOT.glob("*/.codex-plugin/plugin.json")):
        try:
            plugin = plugin_from_manifest(manifest_path)
        except json.JSONDecodeError as exc:
            errors.append({"check": "plugin", "message": f"invalid plugin JSON: {manifest_path.relative_to(ROOT)}: {exc}"})
            continue
        errs, warns = validate_plugin(plugin)
        if errs:
            errors.append({"check": "plugin", "plugin": plugin.name, "items": errs})
        if warns:
            warnings.append({"check": "plugin", "plugin": plugin.name, "items": warns})
    return errors, warnings


def auto_trigger_policy_report() -> tuple[list[dict], list[dict], dict]:
    errors: list[dict] = []
    warnings: list[dict] = []
    if not AUTO_TRIGGER_POLICY_PATH.exists():
        errors.append({"check": "auto-trigger-policy", "message": "missing manifests/auto-trigger-policy.json"})
        return errors, warnings, {}

    try:
        policy = read_json_file(AUTO_TRIGGER_POLICY_PATH)
    except json.JSONDecodeError as exc:
        errors.append({"check": "auto-trigger-policy", "message": f"invalid JSON: {exc}"})
        return errors, warnings, {}

    installable_names = {skill.name for skill in discover_skills("all")}
    fallback = policy.get("fallback_skill")
    if fallback not in installable_names:
        errors.append({"check": "auto-trigger-policy", "message": f"unknown fallback_skill: {fallback}"})

    triggers = policy.get("triggers", [])
    if not isinstance(triggers, list) or not triggers:
        errors.append({"check": "auto-trigger-policy", "message": "triggers must be a non-empty list"})
    else:
        trigger_ids = [item.get("id") for item in triggers if isinstance(item, dict)]
        duplicates = sorted({item for item in trigger_ids if trigger_ids.count(item) > 1})
        if duplicates:
            errors.append({"check": "auto-trigger-policy", "message": "duplicate trigger ids", "items": duplicates})
        for item in triggers:
            if not isinstance(item, dict):
                errors.append({"check": "auto-trigger-policy", "message": "trigger item must be an object"})
                continue
            for field in ("id", "surface", "condition", "action", "control"):
                if field not in item:
                    errors.append(
                        {
                            "check": "auto-trigger-policy",
                            "message": f"trigger missing {field}: {item.get('id', '<unknown>')}",
                        }
                    )
            control = item.get("control", {})
            if isinstance(control, dict) and control.get("auto_promote", True):
                errors.append(
                    {
                        "check": "auto-trigger-policy",
                        "message": f"trigger may auto-promote memory without review: {item.get('id', '<unknown>')}",
                    }
                )

    required_controls = {"capture_raw_prompt", "capture_raw_response", "auto_promote", "require_review", "deduplicate"}
    controls = policy.get("controls", {})
    missing_controls = sorted(required_controls - set(controls)) if isinstance(controls, dict) else sorted(required_controls)
    if missing_controls:
        errors.append({"check": "auto-trigger-policy", "message": "missing global controls", "items": missing_controls})
    elif controls.get("capture_raw_prompt") or controls.get("capture_raw_response") or controls.get("auto_promote"):
        errors.append({"check": "auto-trigger-policy", "message": "unsafe global capture or promotion control is enabled"})

    return errors, warnings, policy


def skill_lifecycle_policy_report() -> tuple[list[dict], list[dict], dict]:
    errors: list[dict] = []
    warnings: list[dict] = []
    if not SKILL_LIFECYCLE_POLICY_PATH.exists():
        errors.append({"check": "skill-lifecycle-policy", "message": "missing manifests/skill-lifecycle-policy.json"})
        return errors, warnings, {}

    try:
        policy = read_json_file(SKILL_LIFECYCLE_POLICY_PATH)
    except json.JSONDecodeError as exc:
        errors.append({"check": "skill-lifecycle-policy", "message": f"invalid JSON: {exc}"})
        return errors, warnings, {}

    levels = policy.get("importance_levels", {})
    for level in ("critical", "important", "normal", "low"):
        if level not in levels:
            errors.append({"check": "skill-lifecycle-policy", "message": f"missing importance level: {level}"})
    protected = policy.get("protected_skills", [])
    installable_names = {skill.name for skill in discover_skills("all")}
    unknown_protected = sorted(set(protected) - installable_names) if isinstance(protected, list) else []
    if unknown_protected:
        errors.append({"check": "skill-lifecycle-policy", "message": "unknown protected skills", "items": unknown_protected})

    curation = policy.get("curation", {})
    if not isinstance(curation, dict):
        errors.append({"check": "skill-lifecycle-policy", "message": "curation must be an object"})
    else:
        if curation.get("auto_delete", True):
            errors.append({"check": "skill-lifecycle-policy", "message": "auto_delete must be false"})
        if not curation.get("archive_is_reversible", False):
            errors.append({"check": "skill-lifecycle-policy", "message": "archive_is_reversible must be true"})
        if not curation.get("require_dedup_before_create", False):
            errors.append({"check": "skill-lifecycle-policy", "message": "require_dedup_before_create must be true"})
        allowed = set(curation.get("allowed_toolsets", []))
        if allowed - {"memory", "skills", "catalog", "audit"}:
            errors.append(
                {
                    "check": "skill-lifecycle-policy",
                    "message": "curation allowed_toolsets are too broad",
                    "items": sorted(allowed),
                }
            )

    return errors, warnings, policy


def compatibility_report() -> list[dict]:
    results = []
    for link_rel, target_rel in sorted(COMPATIBILITY_LINKS.items()):
        link = ROOT / link_rel
        target = ROOT / target_rel
        ok = link.is_symlink() and link.exists() and target.exists() and link.resolve() == target.resolve()
        results.append(
            {
                "path": link_rel,
                "expected_target": target_rel,
                "exists": link.exists(),
                "is_symlink": link.is_symlink(),
                "ok": ok,
            }
        )
    return results


def looks_like_placeholder(value: str) -> bool:
    lowered = value.lower()
    if value.startswith("$") or "{" in value or "}" in value:
        return True
    return any(part in lowered for part in ("example", "placeholder", "changeme", "your", "test", "xxx", "token"))


def scan_text_file(path: Path) -> tuple[list[dict], list[dict]]:
    secrets: list[dict] = []
    risks: list[dict] = []
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return secrets, risks
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return secrets, risks

    rel = path.relative_to(ROOT).as_posix()
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, pattern in SECRET_PATTERNS.items():
            match = pattern.search(line)
            if not match:
                continue
            value = match.group(1) if match.groups() else match.group(0)
            if name == "hardcoded-secret-assignment" and looks_like_placeholder(value):
                continue
            secrets.append({"file": rel, "line": lineno, "pattern": name})

        for name, pattern in RISKY_PATTERNS.items():
            if pattern.search(line):
                risks.append({"file": rel, "line": lineno, "pattern": name})
    return secrets, risks


def cmd_audit(args: argparse.Namespace) -> int:
    skills = discover_skills("all")
    vendor_skills = discover_vendor_skills()
    install_dups = duplicate_names(skills)
    vendor_dups = duplicate_names(vendor_skills)
    manifest_errors, manifest_warnings = profile_manifest_report()
    plugin_errors, plugin_warnings = plugin_manifest_report()
    trigger_errors, trigger_warnings, trigger_policy = auto_trigger_policy_report()
    lifecycle_errors, lifecycle_warnings, lifecycle_policy = skill_lifecycle_policy_report()
    plugins = discover_plugins()
    compatibility = compatibility_report()

    secret_findings: list[dict] = []
    risky_findings: list[dict] = []
    for path in tracked_repo_files():
        secrets, risks = scan_text_file(path)
        secret_findings.extend(secrets)
        risky_findings.extend(risks)

    executable_checks = []
    for rel in ("bin/super-skill", "scripts/super_skill.py"):
        path = ROOT / rel
        executable_checks.append({"path": rel, "exists": path.exists(), "executable": os.access(path, os.X_OK)})

    failures = []
    if install_dups:
        failures.append({"check": "installable-duplicates", "items": sorted(install_dups)})
    broken_links = [item for item in compatibility if not item["ok"]]
    if broken_links:
        failures.append({"check": "compatibility-links", "items": broken_links})
    if manifest_errors:
        failures.append({"check": "manifests", "items": manifest_errors})
    if plugin_errors:
        failures.append({"check": "plugins", "items": plugin_errors})
    if trigger_errors:
        failures.append({"check": "auto-trigger-policy", "items": trigger_errors})
    if lifecycle_errors:
        failures.append({"check": "skill-lifecycle-policy", "items": lifecycle_errors})
    missing_exec = [item for item in executable_checks if not (item["exists"] and item["executable"])]
    if missing_exec:
        failures.append({"check": "executables", "items": missing_exec})
    if secret_findings:
        failures.append({"check": "secrets", "items": secret_findings})

    payload = {
        "skills_total": len(skills),
        "vendor_skill_files": len(vendor_skills),
        "installable_duplicate_names": {k: [s.relative_path for s in v] for k, v in install_dups.items()},
        "vendor_duplicate_names": {k: [s.relative_path for s in v] for k, v in vendor_dups.items()},
        "compatibility_links": compatibility,
        "manifest_warnings": manifest_warnings,
        "codex_plugins": [plugin_dict(plugin) for plugin in plugins],
        "plugin_warnings": plugin_warnings,
        "auto_trigger_policy": {
            "path": AUTO_TRIGGER_POLICY_PATH.relative_to(ROOT).as_posix(),
            "fallback_skill": trigger_policy.get("fallback_skill"),
            "triggers": len(trigger_policy.get("triggers", [])) if trigger_policy else 0,
            "warnings": trigger_warnings,
        },
        "skill_lifecycle_policy": {
            "path": SKILL_LIFECYCLE_POLICY_PATH.relative_to(ROOT).as_posix(),
            "protected_skills": len(lifecycle_policy.get("protected_skills", [])) if lifecycle_policy else 0,
            "warnings": lifecycle_warnings,
        },
        "secret_findings": secret_findings,
        "risky_pattern_findings": risky_findings,
        "executable_checks": executable_checks,
        "failures": failures,
    }

    if args.json:
        emit_json(not failures, payload, code="AUDIT_FAILED" if failures else None)
    else:
        print(f"Installable skills: {len(skills)}")
        print(f"Vendor skill files: {len(vendor_skills)}")
        print(f"Codex plugins: {len(plugins)}")
        print(f"Auto triggers: {payload['auto_trigger_policy']['triggers']}")
        print(f"Protected skills: {payload['skill_lifecycle_policy']['protected_skills']}")
        print(f"Installable duplicate names: {len(install_dups)}")
        print(f"Vendor duplicate names: {len(vendor_dups)}")
        print(f"Compatibility links: {len(compatibility) - len(broken_links)}/{len(compatibility)} ok")
        print(f"Secret findings: {len(secret_findings)}")
        print(f"Risky pattern findings: {len(risky_findings)}")
        if failures:
            print("\nFailures:")
            for failure in failures:
                print(f"  {failure['check']}: {len(failure['items'])}")
        else:
            print("Audit passed.")
    return EXIT_RUNTIME if failures else EXIT_OK


def cmd_doctor(args: argparse.Namespace) -> int:
    checks = []
    for name, command in {
        "python": ["python3", "--version"],
        "git": ["git", "--version"],
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "gh": ["gh", "--version"],
    }.items():
        try:
            proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=10, check=False)
            ok = proc.returncode == 0
            version = (proc.stdout or proc.stderr).splitlines()[0] if (proc.stdout or proc.stderr) else ""
        except (OSError, subprocess.TimeoutExpired) as exc:
            ok = False
            version = str(exc)
        checks.append({"name": name, "ok": ok, "version": version})

    ok = all(c["ok"] for c in checks[:3])
    if args.json:
        emit_json(ok, {"checks": checks}, code="DEPENDENCY_MISSING" if not ok else None)
    else:
        for check in checks:
            mark = "OK" if check["ok"] else "MISS"
            print(f"[{mark}] {check['name']}: {check['version']}")
    return EXIT_OK if ok else EXIT_DEPENDENCY


def assess_capability_set(project: Path, capabilities_spec: list[dict]) -> dict:
    project = project.expanduser().resolve()
    capabilities = []
    present = 0
    for capability in capabilities_spec:
        haystack, files = project_text_for_paths(project, capability["paths"])
        matches = []
        for pattern in capability["patterns"]:
            if re.search(pattern, haystack, re.I):
                matches.append(pattern)
        minimum = capability.get("min_matches", 1)
        status = "present" if len(matches) >= minimum else "missing"
        if status == "present":
            present += 1
        capabilities.append(
            {
                "id": capability["id"],
                "label": capability["label"],
                "status": status,
                "matches": matches[:8],
                "matches_total": len(matches),
                "minimum_matches": minimum,
                "coverage": round(len(matches) / max(len(capability["patterns"]), 1), 2),
                "evidence_files": files[:12],
                "recommendation": capability["recommendation"],
            }
        )

    score = round((present / len(capabilities_spec)) * 100)
    return {
        "project": str(project),
        "score": score,
        "present": present,
        "total": len(capabilities_spec),
        "capabilities": capabilities,
    }


def assess_harness(project: Path) -> dict:
    return assess_capability_set(project, HARNESS_CAPABILITIES)


def cmd_harness(args: argparse.Namespace) -> int:
    project = Path(args.project)
    if not project.expanduser().exists():
        if args.json:
            emit_json(False, {"message": f"project path not found: {project}"}, code="USAGE")
        else:
            print(f"error: project path not found: {project}", file=sys.stderr)
        return EXIT_USAGE

    payload = assess_harness(project)
    if args.json:
        emit_json(True, payload)
    else:
        print(f"Harness readiness: {payload['score']}% ({payload['present']}/{payload['total']})")
        print(f"Project: {payload['project']}")
        for item in payload["capabilities"]:
            mark = "OK" if item["status"] == "present" else "MISS"
            print(f"[{mark}] {item['label']}")
            if item["status"] != "present":
                print(f"      {item['recommendation']}")
    return EXIT_OK


def assess_hermes(project: Path) -> dict:
    return assess_capability_set(project, HERMES_CAPABILITIES)


def cmd_hermes(args: argparse.Namespace) -> int:
    project = Path(args.project)
    if not project.expanduser().exists():
        if args.json:
            emit_json(False, {"message": f"project path not found: {project}"}, code="USAGE")
        else:
            print(f"error: project path not found: {project}", file=sys.stderr)
        return EXIT_USAGE

    payload = assess_hermes(project)
    if args.json:
        emit_json(True, payload)
    else:
        print(f"Hermes engineering readiness: {payload['score']}% ({payload['present']}/{payload['total']})")
        print(f"Project: {payload['project']}")
        for item in payload["capabilities"]:
            mark = "OK" if item["status"] == "present" else "MISS"
            print(f"[{mark}] {item['label']}")
            if item["status"] != "present":
                print(f"      {item['recommendation']}")
    return EXIT_OK


def assess_memory(project: Path) -> dict:
    return assess_capability_set(project, MEMORY_CAPABILITIES)


def cmd_memory(args: argparse.Namespace) -> int:
    project = Path(args.project)
    if not project.expanduser().exists():
        if args.json:
            emit_json(False, {"message": f"project path not found: {project}"}, code="USAGE")
        else:
            print(f"error: project path not found: {project}", file=sys.stderr)
        return EXIT_USAGE

    payload = assess_memory(project)
    if args.json:
        emit_json(True, payload)
    else:
        print(f"Agent memory readiness: {payload['score']}% ({payload['present']}/{payload['total']})")
        print(f"Project: {payload['project']}")
        for item in payload["capabilities"]:
            mark = "OK" if item["status"] == "present" else "MISS"
            print(f"[{mark}] {item['label']}")
            if item["status"] != "present":
                print(f"      {item['recommendation']}")
    return EXIT_OK


def cmd_describe(args: argparse.Namespace) -> int:
    payload = {
        "name": "super-skill",
        "version": "0.1.0",
        "commands": [
            {"name": "list", "purpose": "List lifecycle-organized installable skills"},
            {"name": "validate", "purpose": "Check skill frontmatter, duplicate names, links, and resource counts"},
            {"name": "plan", "purpose": "Preview a resolved install plan without mutating the target"},
            {"name": "install", "purpose": "Install a profile into a flat agent skill directory"},
            {"name": "audit", "purpose": "Check duplicates, manifests, compatibility links, secrets, and risky patterns"},
            {"name": "harness", "purpose": "Assess AI-first harness readiness for this or another project"},
            {"name": "hermes", "purpose": "Assess Hermes-inspired self-improving agent system readiness"},
            {"name": "memory", "purpose": "Assess agent memory, experience reuse, and dream replay readiness"},
            {"name": "memory-plugin", "purpose": "Install or preview the automatic memory/dream Codex plugin"},
            {"name": "triggers", "purpose": "Validate automatic trigger and skill lifecycle controls"},
            {"name": "evals", "purpose": "Run validation projects that prove lifecycle, harness, memory, and runtime coverage"},
            {"name": "live-evals", "purpose": "Run local live validation projects with deterministic graders in temporary workspaces"},
            {"name": "vendor", "purpose": "Summarize vendored Cowork domain ecosystem skills"},
            {"name": "catalog", "purpose": "Generate catalog/skill-index.json and catalog/skill-index.md"},
            {"name": "adapt", "purpose": "Generate per-tool runtime wrappers for Cursor/Trae/Windsurf/OpenCode/Claude Code/Codex/OpenClaw/Hermes"},
            {"name": "llm-eval", "purpose": "Run a real (or stubbed) intent-contract → implementation → output-quality-gate round trip"},
            {"name": "autopilot", "purpose": "Autonomous closed loop: intent → spec → design → ralph-loop impl → simplifier → quality-gate → memory candidate, with checkpoint per phase"},
            {"name": "resume", "purpose": "Resume the latest or a named autopilot run; --list shows pending vs completed phases"},
            {"name": "visualize", "purpose": "Render an autopilot run.json as a single self-contained HTML timeline"},
            {"name": "doctor", "purpose": "Check local tools used by Super Skill"},
        ],
        "profiles": sorted(PROFILE_STAGE_PREFIXES),
        "manifests": {
            "profiles": "manifests/install-profiles.json",
            "components": "manifests/install-components.json",
        },
    }
    if args.json:
        emit_json(True, payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return EXIT_OK


def skill_dict(skill: Skill) -> dict:
    return {
        "name": skill.name,
        "description": skill.description,
        "stage": skill.stage,
        "stage_label": STAGES.get(skill.stage, skill.stage),
        "source": skill.source,
        "path": skill.relative_path,
    }


def plugin_dict(plugin: Plugin) -> dict:
    return {
        "name": plugin.name,
        "version": plugin.version,
        "description": plugin.description,
        "path": plugin.relative_path,
        "skills": plugin.manifest.get("skills"),
        "hooks": plugin.manifest.get("hooks"),
    }


def cmd_catalog(args: argparse.Namespace) -> int:
    skills = discover_skills("all")
    vendor_skills = discover_vendor_skills()
    plugins = discover_plugins()
    payload = {
        "generated_at": int(time.time()),
        "installable_skills": [skill_dict(s) for s in skills],
        "vendor_skills": [skill_dict(s) for s in vendor_skills],
        "codex_plugins": [plugin_dict(p) for p in plugins],
        "profiles": {k: sorted(v) for k, v in PROFILE_STAGE_PREFIXES.items()},
        "profile_excludes": {k: sorted(v) for k, v in PROFILE_SKILL_EXCLUDES.items()},
    }

    CATALOG_ROOT.mkdir(parents=True, exist_ok=True)
    json_path = CATALOG_ROOT / "skill-index.json"
    md_path = CATALOG_ROOT / "skill-index.md"
    if not args.dry_run:
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        md_path.write_text(render_catalog_md(skills, vendor_skills, plugins), encoding="utf-8")

    if args.json:
        emit_json(True, {"json": str(json_path), "markdown": str(md_path), "dry_run": args.dry_run})
    else:
        print(f"Catalog {'would be written' if args.dry_run else 'written'}:")
        print(f"  {json_path}")
        print(f"  {md_path}")
    return EXIT_OK


def render_catalog_md(skills: list[Skill], vendor_skills: list[Skill], plugins: list[Plugin]) -> str:
    lines = [
        "# Super Skill Catalog",
        "",
        "Generated by `bin/super-skill catalog`.",
        "",
        f"- Installable lifecycle skills: {len(skills)}",
        f"- Vendored Cowork domain skill files: {len(vendor_skills)}",
        f"- Codex plugins: {len(plugins)}",
        f"- DesignDNA brand systems: {count_design_brands()}",
        "",
        "## Lifecycle Skills",
        "",
    ]
    for stage, items in group_by_stage(skills).items():
        lines.append(f"### {STAGES.get(stage, stage)}")
        lines.append("")
        for skill in items:
            lines.append(f"- `{skill.name}` — {skill.description}")
        lines.append("")

    dups = duplicate_names(vendor_skills)
    lines.extend([
        "## Install Profiles",
        "",
        "Profiles can include stage sets and, for runtime-specific targets, explicit skill exclusions.",
        "",
    ])
    for profile in sorted(PROFILE_STAGE_PREFIXES):
        excluded = profile_excluded_skills(profile)
        if excluded:
            lines.append(f"- `{profile}` excludes: {', '.join(f'`{name}`' for name in excluded)}")
        else:
            lines.append(f"- `{profile}` excludes: none")
    lines.extend([
        "",
        "## Codex Plugins",
        "",
    ])
    if plugins:
        for plugin in plugins:
            lines.append(f"- `{plugin.name}` v{plugin.version} — {plugin.description}")
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Vendor Ecosystem",
        "",
        "Cowork vendor skills are preserved as domain plugin source material because several domains intentionally reuse generic names.",
        "",
        f"- Vendor skill files: {len(vendor_skills)}",
        f"- Unique vendor names: {len({s.name for s in vendor_skills})}",
        "",
    ])
    if dups:
        lines.append("### Vendor Duplicate Names")
        lines.append("")
        for name, items in sorted(dups.items()):
            paths = ", ".join(f"`{s.relative_path}`" for s in items)
            lines.append(f"- `{name}`: {paths}")
        lines.append("")
    return "\n".join(lines)


def count_design_brands() -> int:
    root = ROOT / "resources" / "design-md"
    return len([p for p in root.iterdir() if p.is_dir()]) if root.exists() else 0


# --- adapt: generate per-tool runtime wrappers ----------------------------

ADAPT_TOOLS = (
    "cursor",
    "trae",
    "windsurf",
    "opencode",
    "claude-code",
    "codex",
    "openclaw",
    "hermes",
)


def adapt_default_target(tool: str, project: Path) -> Path:
    if tool == "cursor":
        return project / ".cursor" / "rules" / "super-skill.mdc"
    if tool == "trae":
        return project / ".trae" / "rules" / "super-skill.md"
    if tool == "windsurf":
        return project / ".windsurfrules"
    if tool == "opencode":
        return project / "opencode.json"
    if tool == "claude-code":
        return project / "CLAUDE.md"
    if tool == "openclaw":
        return project / "skills" / "super-skill-bridge" / "SKILL.md"
    if tool in ("codex", "hermes"):
        # No file emitted; commands delegate to install/memory-plugin.
        return project
    raise ValueError(f"unsupported tool: {tool}")


def adapt_skill_summary(skills: list[Skill], max_skills: int = 40) -> list[dict]:
    items = []
    for s in skills:
        desc = (s.description or "").replace("\n", " ").strip()
        if len(desc) > 220:
            desc = desc[:217].rstrip() + "..."
        items.append({"name": s.name, "stage": s.stage, "description": desc})
    return items[:max_skills]


def adapt_render_cursor(skills: list[Skill], canonical: Path) -> str:
    summary = adapt_skill_summary(skills)
    lines = [
        "---",
        "description: Super Skill bridge — auto-loaded canonical skills from a sibling repo.",
        "globs: ['**/*']",
        "alwaysApply: true",
        "---",
        "",
        "# Super Skill Bridge (Cursor)",
        "",
        f"Canonical repo: `{canonical}`",
        "",
        "When a request matches one of the skills below, follow that skill's `SKILL.md`",
        "(under `skills/<stage>/<name>/SKILL.md` in the canonical repo). Do not duplicate",
        "the skill body here — the canonical file is the source of truth. Trigger semantics",
        "are encoded in each skill's frontmatter `description`.",
        "",
        "## Available skills",
        "",
    ]
    by_stage: dict[str, list[dict]] = {}
    for it in summary:
        by_stage.setdefault(it["stage"], []).append(it)
    for stage in sorted(by_stage):
        lines.append(f"### {STAGES.get(stage, stage)}")
        lines.append("")
        for it in by_stage[stage]:
            lines.append(f"- **{it['name']}** — {it['description']}")
        lines.append("")
    lines += [
        "## Memory & dream-replay",
        "",
        "Use `agent-memory-dream-loop` to capture lessons after substantial work, repeated failures,",
        "or user corrections. Never store raw prompt/response. Off switch: `SUPER_SKILL_MEMORY_DISABLED=1`.",
        "",
    ]
    return "\n".join(lines) + "\n"


def adapt_render_trae(skills: list[Skill], canonical: Path) -> str:
    # Trae rules are similar to Cursor's plain markdown — reuse, drop frontmatter.
    body = adapt_render_cursor(skills, canonical)
    body = re.sub(r"^---.*?---\n+", "", body, flags=re.S)
    return "# Super Skill Bridge (Trae)\n\n" + body[len("# Super Skill Bridge (Cursor)\n\n"):]


def adapt_render_windsurf(skills: list[Skill], canonical: Path) -> str:
    summary = adapt_skill_summary(skills)
    lines = [
        "# Super Skill Bridge (Windsurf)",
        "",
        f"Canonical repo: {canonical}",
        "",
        "Treat each skill listed below as an implicit trigger. When the user request matches",
        "a skill description, follow the canonical `SKILL.md`. Do not duplicate skill body here.",
        "",
    ]
    for it in summary:
        lines.append(f"- {it['name']}: {it['description']}")
    lines.append("")
    lines.append("Memory: route through agent-memory-dream-loop; never store raw prompts; respect SUPER_SKILL_MEMORY_DISABLED=1.")
    return "\n".join(lines) + "\n"


def adapt_render_opencode(skills: list[Skill], canonical: Path) -> dict:
    return {
        "$schema": "https://opencode.ai/config.schema.json",
        "instructions": [
            f"Super Skill bridge active. Canonical repo: {canonical}",
            "Use skills under canonical 'skills/<stage>/<name>/SKILL.md' as the source of truth.",
            "Memory uses agent-memory-dream-loop. Off switch: SUPER_SKILL_MEMORY_DISABLED=1.",
        ],
        "rules": [
            f"{it['name']}: {it['description']}" for it in adapt_skill_summary(skills, max_skills=80)
        ],
    }


def adapt_render_claude_code(skills: list[Skill], canonical: Path) -> str:
    lines = [
        "# Super Skill (Claude Code)",
        "",
        f"Canonical repo: `{canonical}`",
        "",
        "Skills are installed as symlinks under `~/.claude/skills/`. Claude Code auto-loads",
        "skill descriptions for implicit triggering. To (re)install:",
        "",
        f"    {canonical}/bin/super-skill install --profile all --target ~/.claude/skills --force",
        "",
        "## Operating rules",
        "",
        "- Front-load trigger keywords in user requests to help Claude Code pick the right skill.",
        "- Memory candidates land in `.super-skill/memory/inbox/` per project; review before promoting.",
        "- Off switch: `SUPER_SKILL_MEMORY_DISABLED=1`.",
        "- Protected skills (never auto-archive): see `manifests/skill-lifecycle-policy.json`.",
        "",
    ]
    return "\n".join(lines) + "\n"


def adapt_render_openclaw(skills: list[Skill], canonical: Path) -> str:
    lines = [
        "---",
        "name: super-skill-bridge",
        "description: Bridge skill that points OpenClaw at the canonical Super Skill repo. Use when an OpenClaw workspace needs Super Skill capabilities without copying the full lifecycle into the workspace.",
        "---",
        "",
        "# Super Skill Bridge (OpenClaw)",
        "",
        f"Canonical repo: `{canonical}`",
        "",
        "Install canonical skills into the workspace skills directory:",
        "",
        f"    {canonical}/bin/super-skill install --profile all --target ./skills --force --mode symlink",
        "",
        "or globally:",
        "",
        f"    {canonical}/bin/super-skill install --profile all --target ~/.openclaw/skills --force",
        "",
        "## Routing",
        "",
        "Treat each installed skill's frontmatter description as the implicit trigger.",
        "Memory uses canonical `agent-memory-dream-loop`; never store raw prompts.",
        "",
    ]
    return "\n".join(lines) + "\n"


def adapt_codex_instructions(canonical: Path) -> list[str]:
    return [
        f"cd '{canonical}' && bin/super-skill install --profile all --target ~/.codex/skills --with-memory-plugin --force",
        "After install, verify hooks: ~/.codex/config.toml should reference the memory plugin.",
        "Off switch: SUPER_SKILL_MEMORY_DISABLED=1",
    ]


def adapt_hermes_instructions(canonical: Path) -> list[str]:
    return [
        f"cd '{canonical}' && bin/super-skill install --profile hermes --target ~/.hermes/skills --force",
        "The 'hermes' profile excludes Hermes-native skills to avoid mirroring duplicates.",
        "Verify with: bin/super-skill plan --profile hermes --json",
    ]


def cmd_adapt(args: argparse.Namespace) -> int:
    tool = args.tool
    project = Path(args.project).resolve()
    canonical = ROOT
    skills = discover_skills("all")

    files: list[dict] = []
    notes: list[str] = []
    target = adapt_default_target(tool, project) if args.target is None else Path(args.target).resolve()

    if tool == "cursor":
        files.append({"path": str(target), "content": adapt_render_cursor(skills, canonical)})
    elif tool == "trae":
        files.append({"path": str(target), "content": adapt_render_trae(skills, canonical)})
    elif tool == "windsurf":
        files.append({"path": str(target), "content": adapt_render_windsurf(skills, canonical)})
    elif tool == "opencode":
        # Merge with existing opencode.json if present.
        existing: dict = {}
        if target.exists():
            try:
                existing = json.loads(target.read_text(encoding="utf-8"))
            except Exception as exc:
                notes.append(f"existing opencode.json could not be parsed: {exc}; will overwrite")
        merged = dict(existing)
        adapter_payload = adapt_render_opencode(skills, canonical)
        # Preserve user keys; only set/overwrite our own.
        merged["$schema"] = adapter_payload["$schema"]
        instr = list(merged.get("instructions") or [])
        for line in adapter_payload["instructions"]:
            if line not in instr:
                instr.append(line)
        merged["instructions"] = instr
        merged["rules"] = adapter_payload["rules"]
        files.append({"path": str(target), "content": json.dumps(merged, ensure_ascii=False, indent=2) + "\n"})
    elif tool == "claude-code":
        files.append({"path": str(target), "content": adapt_render_claude_code(skills, canonical)})
    elif tool == "openclaw":
        files.append({"path": str(target), "content": adapt_render_openclaw(skills, canonical)})
    elif tool == "codex":
        notes.extend(adapt_codex_instructions(canonical))
    elif tool == "hermes":
        notes.extend(adapt_hermes_instructions(canonical))
    else:
        emit_json(False, {"message": f"unsupported tool: {tool}"}, code="USAGE")
        return EXIT_USAGE

    written = []
    if not args.dry_run:
        for f in files:
            p = Path(f["path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.exists() and not args.force:
                notes.append(f"skipped existing file (use --force to overwrite): {p}")
                continue
            p.write_text(f["content"], encoding="utf-8")
            written.append(str(p))

    payload = {
        "tool": tool,
        "project": str(project),
        "canonical": str(canonical),
        "skills_count": len(skills),
        "files": [{"path": f["path"], "bytes": len(f["content"])} for f in files],
        "written": written,
        "notes": notes,
        "dry_run": args.dry_run,
    }
    if args.json:
        emit_json(True, payload)
    else:
        print(f"adapter: {tool}")
        print(f"canonical: {canonical}")
        print(f"target project: {project}")
        for f in files:
            kind = "would write" if args.dry_run else ("wrote" if f["path"] in written else "skipped")
            print(f"  {kind}: {f['path']} ({len(f['content'])} bytes)")
        for n in notes:
            print(f"  note: {n}")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="super-skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Manage the Super Skill lifecycle skill collection.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="list skills")
    list_p.add_argument("--profile", choices=sorted(PROFILE_STAGE_PREFIXES), default="all")
    list_p.add_argument("--json", action="store_true")
    list_p.set_defaults(func=cmd_list)

    val_p = sub.add_parser("validate", help="validate repository skills")
    val_p.add_argument("--json", action="store_true")
    val_p.set_defaults(func=cmd_validate)

    ins_p = sub.add_parser("install", help="install skills into a flat agent skill directory")
    ins_p.add_argument("--profile", choices=sorted(PROFILE_STAGE_PREFIXES), default="all")
    ins_p.add_argument("--target", default=None)
    ins_p.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    ins_p.add_argument("--force", action="store_true")
    ins_p.add_argument("--dry-run", action="store_true")
    ins_p.add_argument("--with-memory-plugin", action="store_true")
    ins_p.add_argument("--memory-plugin-target", default=None)
    ins_p.add_argument("--memory-plugin-marketplace", default=None)
    ins_p.add_argument("--memory-plugin-hooks", default=None)
    ins_p.add_argument("--memory-plugin-config", default=None)
    ins_p.add_argument("--json", action="store_true")
    ins_p.set_defaults(func=cmd_install)

    plan_p = sub.add_parser("plan", help="preview install operations without mutating files")
    plan_p.add_argument("--profile", choices=sorted(PROFILE_STAGE_PREFIXES), default="all")
    plan_p.add_argument("--target", default=None)
    plan_p.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    plan_p.add_argument("--json", action="store_true")
    plan_p.set_defaults(func=cmd_plan)

    audit_p = sub.add_parser("audit", help="audit duplicate, compatibility, reliability, and security posture")
    audit_p.add_argument("--json", action="store_true")
    audit_p.set_defaults(func=cmd_audit)

    harness_p = sub.add_parser("harness", help="assess AI-first harness readiness")
    harness_p.add_argument("--project", default=".")
    harness_p.add_argument("--json", action="store_true")
    harness_p.set_defaults(func=cmd_harness)

    hermes_p = sub.add_parser("hermes", help="assess Hermes-inspired self-improving agent system readiness")
    hermes_p.add_argument("--project", default=".")
    hermes_p.add_argument("--json", action="store_true")
    hermes_p.set_defaults(func=cmd_hermes)

    memory_p = sub.add_parser("memory", help="assess agent memory and dream replay readiness")
    memory_p.add_argument("--project", default=".")
    memory_p.add_argument("--json", action="store_true")
    memory_p.set_defaults(func=cmd_memory)

    memory_plugin_p = sub.add_parser("memory-plugin", help="install the automatic memory/dream Codex plugin")
    memory_plugin_p.add_argument("--runtime", choices=["codex"], default="codex")
    memory_plugin_p.add_argument("--target", default=None)
    memory_plugin_p.add_argument("--marketplace", default=None)
    memory_plugin_p.add_argument("--hooks", default=None)
    memory_plugin_p.add_argument("--config", default=None)
    memory_plugin_p.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    memory_plugin_p.add_argument("--force", action="store_true")
    memory_plugin_p.add_argument("--dry-run", action="store_true")
    memory_plugin_p.add_argument("--json", action="store_true")
    memory_plugin_p.set_defaults(func=cmd_memory_plugin)

    triggers_p = sub.add_parser("triggers", help="validate automatic trigger and skill lifecycle controls")
    triggers_p.add_argument("--json", action="store_true")
    triggers_p.set_defaults(func=cmd_triggers)

    evals_p = sub.add_parser("evals", help="run capability validation projects")
    evals_p.add_argument("--project", default=None)
    evals_p.add_argument("--json", action="store_true")
    evals_p.set_defaults(func=cmd_evals)

    live_evals_p = sub.add_parser("live-evals", help="run local live validation projects")
    live_evals_p.add_argument("--project", default=None)
    live_evals_p.add_argument("--keep", action="store_true", help="keep generated workspaces for debugging")
    live_evals_p.add_argument("--json", action="store_true")
    live_evals_p.set_defaults(func=cmd_live_evals)

    vendor_p = sub.add_parser("vendor", help="summarize vendored domain ecosystem")
    vendor_p.add_argument("--json", action="store_true")
    vendor_p.set_defaults(func=cmd_vendor)

    doc_p = sub.add_parser("doctor", help="check local dependencies")
    doc_p.add_argument("--json", action="store_true")
    doc_p.set_defaults(func=cmd_doctor)

    desc_p = sub.add_parser("describe", help="describe CLI schema")
    desc_p.add_argument("--json", action="store_true")
    desc_p.set_defaults(func=cmd_describe)

    cat_p = sub.add_parser("catalog", help="generate catalog files")
    cat_p.add_argument("--dry-run", action="store_true")
    cat_p.add_argument("--json", action="store_true")
    cat_p.set_defaults(func=cmd_catalog)

    adapt_p = sub.add_parser(
        "adapt",
        help="generate per-tool runtime wrappers (cursor/trae/windsurf/opencode/claude-code/codex/openclaw/hermes)",
    )
    adapt_p.add_argument("--tool", choices=ADAPT_TOOLS, required=True)
    adapt_p.add_argument("--project", default=".", help="project root that should receive the wrapper (default: cwd)")
    adapt_p.add_argument("--target", default=None, help="explicit output path (default: tool-specific convention)")
    adapt_p.add_argument("--force", action="store_true", help="overwrite existing wrapper files")
    adapt_p.add_argument("--dry-run", action="store_true")
    adapt_p.add_argument("--json", action="store_true")
    adapt_p.set_defaults(func=cmd_adapt)

    llm_p = sub.add_parser(
        "llm-eval",
        help="run a real (or stubbed) intent-contract → implementation → output-quality-gate round trip",
    )
    llm_p.add_argument("--prompt", default=None, help="user task prompt (default: built-in calculator example)")
    llm_p.add_argument("--provider", choices=["auto", "stub", "anthropic"], default="auto")
    llm_p.add_argument("--model", default=None, help="provider-specific model id (default: provider best-fit)")
    llm_p.add_argument("--show-outputs", action="store_true", help="include phase outputs in the JSON payload")
    llm_p.add_argument("--json", action="store_true")
    llm_p.set_defaults(func=cmd_llm_eval)

    auto_p = sub.add_parser(
        "autopilot",
        help="run the autonomous harness-engineering closed loop end-to-end (intent → spec → design → ralph-loop impl → simplifier → quality-gate → memory)",
    )
    auto_p.add_argument("--prompt", default=None, help="user request that drives the run")
    auto_p.add_argument("--provider", choices=["auto", "stub", "anthropic"], default="auto")
    auto_p.add_argument("--model", default=None)
    auto_p.add_argument("--project", default=".", help="project root that owns the run workspace")
    auto_p.add_argument("--run-id", default=None, help="explicit run id (default: timestamped)")
    auto_p.add_argument("--max-ralph-rounds", type=int, default=20)
    auto_p.add_argument("--skip", default=None, help="comma-separated phase ids to skip (e.g. '03-design,08-memory')")
    auto_p.add_argument("--force", action="store_true", help="regenerate phase artifacts even if present")
    auto_p.add_argument("--dry-run", action="store_true")
    auto_p.add_argument("--show-outputs", action="store_true")
    auto_p.add_argument("--based-on", dest="based_on", default=None,
        help="parent run id; in iterate mode each phase sees prior version + new feedback")
    auto_p.add_argument("--feedback", default=None,
        help="new feedback to drive the iteration (use with --based-on)")
    auto_p.add_argument("--json", action="store_true")
    auto_p.set_defaults(func=cmd_autopilot)

    viz_p = sub.add_parser(
        "visualize",
        help="render an autopilot run.json as a single self-contained HTML timeline",
    )
    viz_p.add_argument("--project", default=".", help="project root that owns the run workspace")
    viz_p.add_argument("--run-id", default=None, help="run id to render (default: latest)")
    viz_p.add_argument("--output", default=None, help="output path (default: <run_dir>/timeline.html)")
    viz_p.add_argument("--json", action="store_true")
    viz_p.set_defaults(func=cmd_visualize)

    res_p = sub.add_parser(
        "resume",
        help="resume the latest (or named) autopilot run; use --list to inspect without rerunning",
    )
    res_p.add_argument("--project", default=".", help="project root that owns the run workspace")
    res_p.add_argument("--run-id", default=None, help="resume this run id (default: latest under project)")
    res_p.add_argument("--list", action="store_true", help="show pending vs completed phases and exit")
    res_p.add_argument("--prompt", default=None, help="override prompt if the original journal lost it")
    res_p.add_argument("--provider", choices=["auto", "stub", "anthropic"], default="auto")
    res_p.add_argument("--model", default=None)
    res_p.add_argument("--max-ralph-rounds", type=int, default=20)
    res_p.add_argument("--skip", default=None)
    res_p.add_argument("--dry-run", action="store_true")
    res_p.add_argument("--show-outputs", action="store_true")
    res_p.add_argument("--json", action="store_true")
    res_p.set_defaults(func=cmd_resume)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except BrokenPipeError:
        return EXIT_OK
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(textwrap.dedent(f"""\
        error: internal failure
        hint: rerun with --json where available or inspect the traceback locally
        detail: {exc}
        """).strip(), file=sys.stderr)
        return EXIT_RUNTIME


if __name__ == "__main__":
    raise SystemExit(main())
