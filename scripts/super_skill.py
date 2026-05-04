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
    "all": set(STAGES),
}


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
    items = []
    for skill_md in iter_skill_files():
        try:
            stage = skill_md.parent.relative_to(SKILLS_ROOT).parts[0]
        except (IndexError, ValueError):
            continue
        if stage in allowed:
            items.append(skill_from_path(skill_md))
    return sorted(items, key=lambda s: (s.stage, s.name, s.relative_path))


def discover_vendor_skills() -> list[Skill]:
    if not VENDOR_ROOT.exists():
        return []
    return [
        skill_from_path(path, source="vendor")
        for path in sorted(VENDOR_ROOT.rglob("SKILL.md"))
    ]


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

    target = Path(args.target).expanduser()
    results = [install_one(skill, target, args.mode, args.force, args.dry_run) for skill in skills]

    if args.json:
        emit_json(True, {"profile": args.profile, "mode": args.mode, "target": str(target), "results": results})
    else:
        print(f"Install profile '{args.profile}' to {target} ({args.mode})")
        for result in results:
            print(f"  {result['status']:<14} {result['name']}")
    return EXIT_OK


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


def cmd_describe(args: argparse.Namespace) -> int:
    payload = {
        "name": "super-skill",
        "version": "0.1.0",
        "commands": [
            {"name": "list", "purpose": "List lifecycle-organized installable skills"},
            {"name": "validate", "purpose": "Check skill frontmatter, duplicate names, links, and resource counts"},
            {"name": "install", "purpose": "Install a profile into a flat agent skill directory"},
            {"name": "vendor", "purpose": "Summarize vendored Cowork domain ecosystem skills"},
            {"name": "catalog", "purpose": "Generate catalog/skill-index.json and catalog/skill-index.md"},
            {"name": "doctor", "purpose": "Check local tools used by Super Skill"},
        ],
        "profiles": sorted(PROFILE_STAGE_PREFIXES),
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
    ins_p.add_argument("--target", default=os.environ.get("CODEX_SKILLS_HOME", "~/.codex/skills"))
    ins_p.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    ins_p.add_argument("--force", action="store_true")
    ins_p.add_argument("--dry-run", action="store_true")
    ins_p.add_argument("--json", action="store_true")
    ins_p.set_defaults(func=cmd_install)

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
