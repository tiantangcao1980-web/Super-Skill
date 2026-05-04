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
import shutil
import subprocess
import sys
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
        "patterns": [r"agent-routing", r"provider", r"auxiliary", r"model routing", r"fallback"],
        "paths": ["docs", "workflows", "skills", "AGENTS.md"],
        "recommendation": "Route main, auxiliary, review, and low-risk tasks to appropriate models with fallback policy.",
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


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path
    stage: str
    source: str
    relative_path: str


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

    if args.json:
        emit_json(
            True,
            {
                "profile": args.profile,
                "mode": args.mode,
                "target": str(target),
                "excluded_skills": profile_excluded_skills(args.profile),
                "results": results,
            },
        )
    else:
        print(f"Install profile '{args.profile}' to {target} ({args.mode})")
        for result in results:
            print(f"  {result['status']:<14} {result['name']}")
    return EXIT_OK


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
            {"name": "vendor", "purpose": "Summarize vendored Cowork domain ecosystem skills"},
            {"name": "catalog", "purpose": "Generate catalog/skill-index.json and catalog/skill-index.md"},
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


def cmd_catalog(args: argparse.Namespace) -> int:
    skills = discover_skills("all")
    vendor_skills = discover_vendor_skills()
    payload = {
        "generated_at": int(time.time()),
        "installable_skills": [skill_dict(s) for s in skills],
        "vendor_skills": [skill_dict(s) for s in vendor_skills],
        "profiles": {k: sorted(v) for k, v in PROFILE_STAGE_PREFIXES.items()},
        "profile_excludes": {k: sorted(v) for k, v in PROFILE_SKILL_EXCLUDES.items()},
    }

    CATALOG_ROOT.mkdir(parents=True, exist_ok=True)
    json_path = CATALOG_ROOT / "skill-index.json"
    md_path = CATALOG_ROOT / "skill-index.md"
    if not args.dry_run:
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        md_path.write_text(render_catalog_md(skills, vendor_skills), encoding="utf-8")

    if args.json:
        emit_json(True, {"json": str(json_path), "markdown": str(md_path), "dry_run": args.dry_run})
    else:
        print(f"Catalog {'would be written' if args.dry_run else 'written'}:")
        print(f"  {json_path}")
        print(f"  {md_path}")
    return EXIT_OK


def render_catalog_md(skills: list[Skill], vendor_skills: list[Skill]) -> str:
    lines = [
        "# Super Skill Catalog",
        "",
        "Generated by `bin/super-skill catalog`.",
        "",
        f"- Installable lifecycle skills: {len(skills)}",
        f"- Vendored Cowork domain skill files: {len(vendor_skills)}",
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
