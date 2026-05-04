from __future__ import annotations

import json
import subprocess
import sys
import tempfile
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

    def test_hermes_profile_excludes_native_mirror_skills(self) -> None:
        data = run_cli("plan", "--profile", "hermes")
        names = {item["name"] for item in data["operations"]}
        excluded = set(data["excluded_skills"])
        self.assertGreaterEqual(len(excluded), 6)
        self.assertEqual(data["target"], str(Path.home() / ".hermes" / "skills"))
        self.assertIn("target_conflicts", data)
        self.assertNotIn("durable-agent-board", names)
        self.assertNotIn("persistent-memory-curation", names)
        self.assertNotIn("skill-evolution-loop", names)
        self.assertIn("harness-engineering", names)
        self.assertTrue(excluded.isdisjoint(names))

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
        self.assertIn("eval-trace-benchmark", ids)
        self.assertIn("observability-triage", ids)
        self.assertIn("tool-sandbox-policy", ids)
        self.assertIn("dev-tool-adaptation", ids)
        self.assertIn("model-adaptation-contract", ids)
        self.assertIn("memory-dream-loop", ids)

    def test_hermes_assessment_reports_self_improving_capabilities(self) -> None:
        data = run_cli("hermes", "--project", ".")
        self.assertGreaterEqual(data["score"], 70)
        self.assertEqual(data["total"], len(data["capabilities"]))
        ids = {item["id"] for item in data["capabilities"]}
        self.assertIn("progressive-skill-disclosure", ids)
        self.assertIn("memory-curation", ids)
        self.assertIn("durable-agent-board", ids)
        self.assertIn("runtime-adapters", ids)

    def test_memory_assessment_reports_dream_loop_capabilities(self) -> None:
        data = run_cli("memory", "--project", ".")
        self.assertGreaterEqual(data["score"], 70)
        self.assertEqual(data["total"], len(data["capabilities"]))
        ids = {item["id"] for item in data["capabilities"]}
        self.assertIn("episodic-traces", ids)
        self.assertIn("procedural-memory", ids)
        self.assertIn("negative-memory", ids)
        self.assertIn("dream-replay", ids)
        self.assertIn("memory-safety", ids)
        self.assertIn("automatic-memory-trigger", ids)
        self.assertIn("skill-lifecycle-curation", ids)

    def test_trigger_policy_reports_controlled_automatic_triggers(self) -> None:
        data = run_cli("triggers")
        self.assertEqual(data["failures"], [])
        trigger_policy = data["auto_trigger_policy"]
        lifecycle_policy = data["skill_lifecycle_policy"]
        self.assertEqual(trigger_policy["fallback_skill"], "agent-memory-dream-loop")
        self.assertGreaterEqual(len(trigger_policy["triggers"]), 4)
        self.assertFalse(trigger_policy["controls"]["capture_raw_prompt"])
        self.assertFalse(trigger_policy["controls"]["capture_raw_response"])
        self.assertFalse(trigger_policy["controls"]["auto_promote"])
        self.assertIn("agent-memory-dream-loop", lifecycle_policy["protected_skills"])
        self.assertFalse(lifecycle_policy["curation"]["auto_delete"])

    def test_memory_plugin_plan_reports_codex_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = run_cli(
                "memory-plugin",
                "--dry-run",
                "--target",
                str(root / "plugins" / "super-skill-memory-harness"),
                "--marketplace",
                str(root / "marketplace.json"),
                "--hooks",
                str(root / "hooks.json"),
                "--config",
                str(root / "config.toml"),
            )
            self.assertEqual(data["plugin"], "super-skill-memory-harness")
            self.assertEqual(data["runtime"], "codex")
            self.assertTrue(data["dry_run"])
            types = {item["type"] for item in data["operations"]}
            self.assertEqual(types, {"plugin-bundle", "marketplace", "hooks", "codex-config"})
            self.assertFalse((root / "marketplace.json").exists())

    def test_install_with_memory_plugin_dry_run_includes_plugin_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = run_cli(
                "install",
                "--profile",
                "core",
                "--target",
                str(root / "skills"),
                "--dry-run",
                "--with-memory-plugin",
                "--memory-plugin-target",
                str(root / "plugins" / "super-skill-memory-harness"),
                "--memory-plugin-marketplace",
                str(root / "marketplace.json"),
                "--memory-plugin-hooks",
                str(root / "hooks.json"),
                "--memory-plugin-config",
                str(root / "config.toml"),
            )
            self.assertIn("memory_plugin", data)
            self.assertEqual(data["memory_plugin"]["plugin"], "super-skill-memory-harness")
            self.assertTrue(all(item["status"].startswith("would-") for item in data["results"]))

    def test_memory_hook_writes_metadata_candidate_without_prompt_content(self) -> None:
        script = ROOT / "plugins" / "super-skill-memory-harness" / "scripts" / "memory_dream_hook.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = {
                "hook_event_name": "Stop",
                "cwd": str(root),
                "model": "test-model",
                "session_id": "session-test",
                "transcript_path": str(root / "transcript.jsonl"),
                "prompt": "do not store this user prompt",
            }
            proc = subprocess.run(
                [sys.executable, str(script), "--event", "stop"],
                cwd=root,
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertTrue(out["continue"])
            candidates = sorted((root / ".super-skill" / "memory" / "inbox").glob("*.md"))
            traces = sorted((root / ".super-skill" / "memory" / "traces").glob("*.jsonl"))
            self.assertEqual(len(candidates), 1)
            self.assertEqual(len(traces), 1)
            body = candidates[0].read_text(encoding="utf-8")
            self.assertIn("review whether any verified lesson should become memory", body)
            self.assertNotIn("do not store this user prompt", body)


if __name__ == "__main__":
    unittest.main()
