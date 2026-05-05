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

    def test_capability_evals_validate_projects_and_global_checks(self) -> None:
        data = run_cli("evals")
        self.assertEqual(data["failures"], [])
        self.assertGreaterEqual(data["projects_total"], 5)
        self.assertEqual(data["projects_passed"], data["projects_total"])
        self.assertEqual(data["global_checks_passed"], data["global_checks_total"])
        project_names = {item["project"] for item in data["projects"]}
        self.assertIn("ai-first-saas-launch", project_names)
        self.assertIn("cross-runtime-memory", project_names)

    def test_capability_evals_reject_unknown_project(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(CLI), "evals", "--project", "missing-project", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertNotEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "EVALS_FAILED")

    def test_live_evals_run_local_project_graders(self) -> None:
        data = run_cli("live-evals")
        self.assertEqual(data["failures"], [])
        self.assertGreaterEqual(data["projects_total"], 3)
        self.assertEqual(data["projects_passed"], data["projects_total"])
        project_names = {item["project"] for item in data["projects"]}
        self.assertIn("mini-saas-feedback-loop", project_names)
        self.assertIn("cross-runtime-memory-adapter", project_names)
        self.assertIn("design-frontend-quality-gate", project_names)

    def test_live_evals_reject_unknown_project(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(CLI), "live-evals", "--project", "missing-project", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertNotEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "LIVE_EVALS_FAILED")

    def test_adapt_dry_run_emits_file_per_tool(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            for tool in ("cursor", "trae", "windsurf", "opencode", "claude-code", "openclaw"):
                data = run_cli("adapt", "--tool", tool, "--project", td, "--dry-run")
                self.assertEqual(data["tool"], tool)
                self.assertEqual(data["dry_run"], True)
                self.assertEqual(data["written"], [])
                self.assertEqual(len(data["files"]), 1)
                self.assertGreater(data["files"][0]["bytes"], 100)

    def test_adapt_real_write_creates_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli("adapt", "--tool", "cursor", "--project", td)
            self.assertEqual(len(data["written"]), 1)
            wrote = Path(data["written"][0])
            self.assertTrue(wrote.exists())
            content = wrote.read_text(encoding="utf-8")
            self.assertIn("Super Skill Bridge (Cursor)", content)
            self.assertIn("agent-memory-dream-loop", content)

    def test_adapt_codex_and_hermes_emit_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            for tool in ("codex", "hermes"):
                data = run_cli("adapt", "--tool", tool, "--project", td)
                self.assertEqual(data["written"], [])
                self.assertGreater(len(data["notes"]), 0)
                joined = " ".join(data["notes"])
                self.assertIn("super-skill install", joined)

    def test_adapt_does_not_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_cli("adapt", "--tool", "cursor", "--project", td)
            data = run_cli("adapt", "--tool", "cursor", "--project", td)
            # Second run should skip because file exists.
            joined_notes = " ".join(data["notes"])
            self.assertIn("skipped existing", joined_notes)
            self.assertEqual(data["written"], [])
            # With --force it overwrites.
            data2 = run_cli("adapt", "--tool", "cursor", "--project", td, "--force")
            self.assertEqual(len(data2["written"]), 1)

    def test_llm_eval_stub_passes_full_loop(self) -> None:
        data = run_cli("llm-eval", "--provider", "stub")
        self.assertEqual(data["provider"], "stub")
        self.assertEqual(len(data["phases"]), 3)
        stages = [p["stage"] for p in data["phases"]]
        self.assertEqual(stages, ["contract", "implementation", "gate"])
        contract_grade = data["phases"][0]["grade"]
        self.assertTrue(contract_grade["ok"])
        self.assertEqual(set(contract_grade["found"]), {"goal", "acceptance", "evidence"})
        gate_grade = data["phases"][2]["grade"]
        self.assertTrue(gate_grade["ok"])
        self.assertEqual(gate_grade["verdict"], "pass")
        self.assertTrue(data["ok"])

    def test_llm_eval_stub_with_show_outputs_includes_payload(self) -> None:
        data = run_cli("llm-eval", "--provider", "stub", "--show-outputs", "--prompt", "make a counter")
        self.assertIn("outputs", data)
        self.assertIn("contract", data["outputs"])
        self.assertIn("Intent Contract", data["outputs"]["contract"])


if __name__ == "__main__":
    unittest.main()
