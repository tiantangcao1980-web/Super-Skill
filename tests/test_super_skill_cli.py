from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "super_skill.py"


def run_cli(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(CLI), *args, "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={proc.stdout}\nstderr={proc.stderr}")
    payload = json.loads(proc.stdout)
    if not payload.get("ok"):
        raise AssertionError(f"command returned ok=false: {args}\n{proc.stdout}")
    return payload["data"]


class SuperSkillCliTests(unittest.TestCase):
    def test_validate_has_no_failures(self) -> None:
        data = run_cli("validate")
        self.assertGreaterEqual(data["skills_total"], 90)
        self.assertEqual(data["skills_failed"], 0)

    def test_plan_resolves_core_profile_without_duplicates(self) -> None:
        data = run_cli("plan", "--profile", "core", "--target", "/tmp/super-skill-test")
        names = [item["name"] for item in data["operations"]]
        self.assertEqual(data["skills_total"], len(names))
        self.assertEqual(len(names), len(set(names)))
        self.assertIn("00-orchestration", data["stages"])
        self.assertNotIn("06-development", data["stages"])

    def test_audit_has_no_blocking_failures(self) -> None:
        data = run_cli("audit")
        self.assertEqual(data["failures"], [])
        self.assertEqual(data["secret_findings"], [])
        self.assertGreaterEqual(len(data["compatibility_links"]), 6)

    def test_harness_assessment_reports_capabilities(self) -> None:
        data = run_cli("harness", "--project", ".")
        self.assertGreaterEqual(data["score"], 70)
        self.assertEqual(data["total"], len(data["capabilities"]))
        ids = {item["id"] for item in data["capabilities"]}
        self.assertIn("deterministic-ci", ids)
        self.assertIn("observability-triage", ids)

    def test_hermes_assessment_reports_self_improving_capabilities(self) -> None:
        data = run_cli("hermes", "--project", ".")
        self.assertGreaterEqual(data["score"], 70)
        self.assertEqual(data["total"], len(data["capabilities"]))
        ids = {item["id"] for item in data["capabilities"]}
        self.assertIn("progressive-skill-disclosure", ids)
        self.assertIn("memory-curation", ids)
        self.assertIn("durable-agent-board", ids)


if __name__ == "__main__":
    unittest.main()
