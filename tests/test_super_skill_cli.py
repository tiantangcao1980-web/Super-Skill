from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "super_skill.py"


def _load_super_skill_module():
    """Load scripts/super_skill.py once, register it in sys.modules so unittest
    can resolve __module__ for any classes defined there."""
    if "super_skill" in sys.modules:
        return sys.modules["super_skill"]
    import importlib.util
    spec = importlib.util.spec_from_file_location("super_skill", ROOT / "scripts" / "super_skill.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["super_skill"] = mod
    spec.loader.exec_module(mod)
    return mod


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

    def test_autopilot_dry_run_lists_twelve_phases(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli("autopilot", "--provider", "stub", "--project", td, "--dry-run")
            self.assertEqual(len(data["phases_planned"]), 12)
            ids = [p["id"] for p in data["phases_planned"]]
            self.assertEqual(
                ids,
                ["00-research", "01-intent", "02-business-case",
                 "03-spec", "04-design", "05-impl", "06-simplify",
                 "07-gate", "08-launch", "09-pilot", "10-commerce", "11-ops"],
            )

    def test_autopilot_stub_full_run_passes_all_phases(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "Build add(a,b)")
            self.assertTrue(data["ok"])
            self.assertIsNone(data["failed_phase"])
            self.assertEqual(len(data["phases"]), 12)
            phase_by_id = {p["phase"]: p for p in data["phases"]}
            self.assertTrue(phase_by_id["01-intent"]["grade"]["ok"])
            self.assertTrue(phase_by_id["07-gate"]["grade"]["ok"])
            self.assertGreaterEqual(len(phase_by_id["05-impl"]["ralph_attempts"]), 1)
            workspace = Path(data["workspace"])
            self.assertTrue(workspace.exists())
            self.assertTrue((workspace / "run.json").exists())
            # Every business-stage artifact must be on disk.
            for fname in ("00-research.md", "02-business-case.md",
                          "08-launch-readiness.md", "09-pilot.md",
                          "10-commercial-delivery.md", "11-ops-retrospective.md"):
                self.assertTrue((workspace / fname).exists(), f"{fname} missing")

    def test_autopilot_resume_skips_existing_phases(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            first = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "Build add(a,b)")
            run_id = first["run_id"]
            second = run_cli(
                "autopilot", "--provider", "stub", "--project", td,
                "--prompt", "Build add(a,b)", "--run-id", run_id,
            )
            self.assertTrue(second["ok"])
            for ph in second["phases"]:
                self.assertTrue(
                    ph["skipped"], f"phase {ph['phase']} should have been skipped on resume",
                )

    def test_autopilot_skip_phase(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli("autopilot", "--provider", "stub", "--project", td, "--skip", "11-ops")
            stages = [p["phase"] for p in data["phases"]]
            self.assertNotIn("11-ops", stages)

    def test_autopilot_memory_candidate_does_not_echo_prompt(self) -> None:
        marker_phrase = "marker-do-not-leak-9f1c2"
        with tempfile.TemporaryDirectory() as td:
            data = run_cli(
                "autopilot", "--provider", "stub", "--project", td,
                "--prompt", f"Build a thing. Marker: {marker_phrase}",
            )
            self.assertTrue(data["ok"])
            workspace = Path(data["workspace"])
            mem = (workspace / "11-ops-retrospective.md").read_text(encoding="utf-8")
            self.assertNotIn(
                marker_phrase, mem,
                "memory candidate must not echo raw user prompt — Hermes principle violated",
            )

    def test_live_evals_includes_autopilot_project(self) -> None:
        data = run_cli("live-evals", "--project", "autopilot-end-to-end")
        self.assertEqual(data["projects_total"], 1)
        self.assertEqual(data["projects_passed"], 1)
        proj = data["projects"][0]
        self.assertEqual(proj["project"], "autopilot-end-to-end")
        self.assertTrue(proj["ok"])

    def test_autopilot_phase4_runs_real_python_tests(self) -> None:
        """Phase-4 ralph loop should record kind=bare-tests/unittest/py-compile,
        not just a length heuristic. Stub's candidate has bare def test_*()."""
        with tempfile.TemporaryDirectory() as td:
            data = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "add a,b")
            phase4 = next(p for p in data["phases"] if p["phase"] == "05-impl")
            attempts = phase4["ralph_attempts"]
            self.assertGreaterEqual(len(attempts), 1)
            kinds = {a["test_kind"] for a in attempts}
            # Stub emits bare def test_* style; runner picks bare-tests.
            self.assertIn("bare-tests", kinds)
            self.assertEqual(attempts[-1]["test_returncode"], 0)
            self.assertTrue(attempts[-1]["ok"])

    def test_autopilot_python_runner_detects_broken_code(self) -> None:
        """Direct test of the Phase-4 sandbox runner — failure path."""
        mod = _load_super_skill_module()
        with tempfile.TemporaryDirectory() as td:
            broken = "def test_thing():\n    assert 1 == 2  # always fails\n"
            res = mod.autopilot_run_python_tests(broken, Path(td) / "broken")
            self.assertFalse(res["ok"])
            self.assertEqual(res["kind"], "bare-tests")
            self.assertNotEqual(res["returncode"], 0)
            self.assertIn("FAIL", res.get("stderr_tail", ""))

            syntax_err = "def lol(:\n    pass\n"
            res2 = mod.autopilot_run_python_tests(syntax_err, Path(td) / "broken2")
            self.assertFalse(res2["ok"])
            self.assertIn(res2["kind"], {"py-compile", "bare-tests"})

            ok_code = "def add(a,b): return a+b\n\ndef test_add():\n    assert add(1,2) == 3\n"
            res3 = mod.autopilot_run_python_tests(ok_code, Path(td) / "ok")
            self.assertTrue(res3["ok"])
            self.assertEqual(res3["kind"], "bare-tests")

    def test_resume_list_reports_completed_and_pending(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            first = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "Build add(a,b)")
            run_id = first["run_id"]
            data = run_cli("resume", "--project", td, "--run-id", run_id, "--list")
            self.assertEqual(data["run_id"], run_id)
            self.assertEqual(len(data["completed_phases"]), 12)
            self.assertEqual(data["pending_phases"], [])

    def test_resume_picks_latest_run_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            first = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "First")
            second = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "Second")
            data = run_cli("resume", "--project", td, "--list")
            # Latest is `second` because run ids sort lexicographically by timestamp.
            self.assertEqual(data["run_id"], second["run_id"])

    def test_mcp_server_responds_to_initialize_and_tools_list(self) -> None:
        ROOT = Path(__file__).resolve().parents[1]
        server = ROOT / "plugins" / "super-skill-mcp-server" / "scripts" / "mcp_server.py"
        dialogue = "\n".join([
            '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}}}',
            '{"jsonrpc":"2.0","id":2,"method":"tools/list"}',
            '{"jsonrpc":"2.0","id":3,"method":"shutdown"}',
        ]) + "\n"
        proc = subprocess.run(
            [sys.executable, str(server)],
            input=dialogue, capture_output=True, text=True, timeout=15, check=False,
        )
        lines = [json.loads(l) for l in proc.stdout.splitlines() if l.strip()]
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0]["result"]["serverInfo"]["name"], "super-skill-mcp-server")
        tool_names = [t["name"] for t in lines[1]["result"]["tools"]]
        self.assertIn("autopilot", tool_names)
        self.assertIn("resume", tool_names)
        self.assertIn("llm_eval", tool_names)

    def test_mcp_server_dispatches_autopilot_dry_run(self) -> None:
        ROOT = Path(__file__).resolve().parents[1]
        server = ROOT / "plugins" / "super-skill-mcp-server" / "scripts" / "mcp_server.py"
        with tempfile.TemporaryDirectory() as td:
            dialogue = "\n".join([
                '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}}}',
                json.dumps({
                    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": "autopilot", "arguments": {"prompt": "p", "provider": "stub", "project": td, "dry_run": True}},
                }),
            ]) + "\n"
            proc = subprocess.run(
                [sys.executable, str(server)],
                input=dialogue, capture_output=True, text=True, timeout=30, check=False,
            )
            lines = [json.loads(l) for l in proc.stdout.splitlines() if l.strip()]
            call_reply = lines[1]
            self.assertFalse(call_reply["result"].get("isError"))
            inner = json.loads(call_reply["result"]["content"][0]["text"])
            self.assertTrue(inner["ok"])
            self.assertEqual(len(inner["data"]["phases_planned"]), 12)

    def test_visualize_renders_html_for_latest_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "render me")
            data = run_cli("visualize", "--project", td)
            html_path = Path(data["output"])
            self.assertTrue(html_path.exists())
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("Autopilot run", html)
            self.assertIn("Intent Contract", html)
            self.assertIn("Output Quality Gate", html)
            self.assertIn("Ralph attempts", html)

    def test_visualize_uses_explicit_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            first = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "first")
            data = run_cli("visualize", "--project", td, "--run-id", first["run_id"])
            self.assertIn(first["run_id"], data["output"])

    def test_autopilot_iterate_links_parent_and_records_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            parent = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "Build add(a,b)")
            self.assertTrue(parent["ok"])
            self.assertIsNone(parent["parent_run_id"])
            self.assertEqual(parent["lineage"], [])

            child = run_cli(
                "autopilot", "--provider", "stub", "--project", td,
                "--based-on", parent["run_id"],
                "--feedback", "Add float support",
            )
            self.assertTrue(child["ok"])
            self.assertEqual(child["parent_run_id"], parent["run_id"])
            self.assertEqual(child["feedback"], "Add float support")
            self.assertEqual(child["lineage"], [parent["run_id"]])
            # Child inherits parent's prompt when --prompt is omitted.
            self.assertEqual(child["user_prompt"], parent["user_prompt"])

    def test_autopilot_iterate_three_generations_record_full_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            r1 = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "v1")
            r2 = run_cli("autopilot", "--provider", "stub", "--project", td,
                         "--based-on", r1["run_id"], "--feedback", "Add A")
            r3 = run_cli("autopilot", "--provider", "stub", "--project", td,
                         "--based-on", r2["run_id"], "--feedback", "Add B")
            self.assertEqual(r3["parent_run_id"], r2["run_id"])
            self.assertEqual(r3["lineage"], [r2["run_id"], r1["run_id"]])

    def test_autopilot_iterate_marker_lands_on_prose_phases_only(self) -> None:
        """Stub appends an iteration marker to prose artifacts so we can prove
        the iteration context reaches each phase. It must NOT corrupt the
        Python (phase 4/5) or strict JSON (phase 6) artifacts."""
        with tempfile.TemporaryDirectory() as td:
            parent = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "Build add(a,b)")
            child = run_cli(
                "autopilot", "--provider", "stub", "--project", td,
                "--based-on", parent["run_id"], "--feedback", "Float support",
            )
            self.assertTrue(child["ok"])
            child_dir = Path(child["workspace"])
            for prose in ("00-research.md", "01-intent-contract.md",
                          "02-business-case.md", "03-product-spec.md",
                          "04-design.md", "08-launch-readiness.md",
                          "09-pilot.md", "10-commercial-delivery.md",
                          "11-ops-retrospective.md"):
                self.assertIn(
                    "Iteration:", (child_dir / prose).read_text(encoding="utf-8"),
                    f"{prose} missing iteration marker",
                )
            for structured in ("05-implementation.md", "06-simplified.md", "07-quality-gate.json"):
                self.assertNotIn(
                    "Iteration:", (child_dir / structured).read_text(encoding="utf-8"),
                    f"{structured} must NOT contain iteration marker (would corrupt parser)",
                )

    def test_autopilot_iterate_rejects_unknown_parent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [sys.executable, str(CLI), "autopilot",
                 "--provider", "stub", "--project", td,
                 "--based-on", "20260101-000000-000-deadbe",
                 "--feedback", "x", "--json"],
                cwd=ROOT, capture_output=True, text=True, timeout=30, check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            payload = json.loads(proc.stdout)
            self.assertFalse(payload["ok"])

    def test_extract_files_recognises_file_headers(self) -> None:
        mod = _load_super_skill_module()
        text = (
            "Two files:\n\n"
            "### file: src/add.py\n```python\ndef add(a,b): return a+b\n```\n"
            "### file: src/add.js\n```javascript\nfunction add(a,b){return a+b}\n```\n"
        )
        files = mod.autopilot_extract_files(text)
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0][0], "src/add.py")
        self.assertEqual(files[0][1], "python")
        self.assertEqual(files[1][0], "src/add.js")
        self.assertEqual(files[1][1], "javascript")
        self.assertEqual(mod.autopilot_dominant_language(files), "python")

    def test_extract_files_falls_back_to_single_block(self) -> None:
        mod = _load_super_skill_module()
        text = "```python\ndef foo(): pass\n```"
        files = mod.autopilot_extract_files(text)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0][0], "candidate.py")
        self.assertEqual(files[0][1], "python")

    def test_javascript_runner_passes_and_fails(self) -> None:
        mod = _load_super_skill_module()
        if not shutil.which("node"):
            self.skipTest("node not on PATH")
        with tempfile.TemporaryDirectory() as td:
            ok = mod.autopilot_run_javascript(
                "function add(a,b){return a+b}\nfunction test_add(){if(add(1,2)!==3) throw new Error('x')}",
                Path(td) / "ok",
            )
            self.assertTrue(ok["ok"])
            self.assertEqual(ok["kind"], "node-bare-tests")
            bad = mod.autopilot_run_javascript(
                "function add(a,b){return a+b}\nfunction test_add(){if(add(1,2)!==99) throw new Error('boom')}",
                Path(td) / "bad",
            )
            self.assertFalse(bad["ok"])
            self.assertIn("FAIL", bad["stderr_tail"])

    def test_bash_runner_parse_only_when_unsafe(self) -> None:
        mod = _load_super_skill_module()
        if not shutil.which("bash"):
            self.skipTest("bash not on PATH")
        with tempfile.TemporaryDirectory() as td:
            res = mod.autopilot_run_bash("echo hello", Path(td))
            self.assertTrue(res["ok"])
            self.assertEqual(res["kind"], "bash-parse-only")

    def test_bash_runner_executes_with_set_e(self) -> None:
        mod = _load_super_skill_module()
        if not shutil.which("bash"):
            self.skipTest("bash not on PATH")
        with tempfile.TemporaryDirectory() as td:
            res = mod.autopilot_run_bash("set -euo pipefail\necho ok", Path(td))
            self.assertTrue(res["ok"])
            self.assertEqual(res["kind"], "bash-exec")

    def test_unsupported_language_returns_skipped(self) -> None:
        mod = _load_super_skill_module()
        with tempfile.TemporaryDirectory() as td:
            res = mod.autopilot_test_implementation("```rust\nfn main(){}\n```", Path(td))
            self.assertEqual(res["kind"], "skipped")
            self.assertIn("rust", res.get("reason", "").lower())

    def test_autopilot_end_to_end_javascript_via_stub(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli(
                "autopilot", "--provider", "stub", "--project", td,
                "--prompt", "Build a JavaScript add(a,b) with one bare test_add() function",
            )
            self.assertTrue(data["ok"])
            phase4 = next(p for p in data["phases"] if p["phase"] == "05-impl")
            self.assertEqual(phase4["ralph_attempts"][-1]["test_kind"], "node-bare-tests")
            self.assertTrue(phase4["ralph_attempts"][-1]["ok"])

    def test_fanout_runs_three_tracks_in_parallel(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli(
                "fanout", "--provider", "stub", "--project", td,
                "--prompt", "Build a tool",
                "--tracks", "frontend-miniapp,backend-api,docs",
            )
            self.assertTrue(data["ok"])
            self.assertEqual(len(data["tracks"]), 3)
            names = [t["track"] for t in data["tracks"]]
            self.assertEqual(names, ["frontend-miniapp", "backend-api", "docs"])
            for t in data["tracks"]:
                self.assertTrue(t["ok"], f"track {t['track']} failed: {t}")
                self.assertIsNotNone(t["run_id"])
            # All three run ids must be distinct.
            run_ids = [t["run_id"] for t in data["tracks"]]
            self.assertEqual(len(set(run_ids)), 3)

    def test_fanout_writes_journal_and_fanout_id_into_each_track(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli(
                "fanout", "--provider", "stub", "--project", td,
                "--prompt", "x", "--tracks", "a,b",
            )
            fid = data["fanout_id"]
            fanout_journal = Path(td) / ".super-skill" / "fanout" / fid / "fanout.json"
            self.assertTrue(fanout_journal.exists())
            for t in data["tracks"]:
                track_journal = Path(t["workspace"]) / "run.json"
                self.assertTrue(track_journal.exists())
                tj = json.loads(track_journal.read_text(encoding="utf-8"))
                self.assertEqual(tj["fanout_id"], fid)
                self.assertEqual(tj["track_name"], t["track"])

    def test_fanout_dry_run_returns_plan(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli(
                "fanout", "--provider", "stub", "--project", td,
                "--prompt", "x", "--tracks", "a,b,c", "--dry-run",
            )
            self.assertEqual(len(data["tracks"]), 3)
            for t in data["tracks"]:
                self.assertIn("[track:", t["sub_prompt"])

    def test_visualize_fanout_renders_summary_html(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            data = run_cli(
                "fanout", "--provider", "stub", "--project", td,
                "--prompt", "x", "--tracks", "a,b",
            )
            fid = data["fanout_id"]
            viz = run_cli("visualize", "--project", td, "--fanout-id", fid)
            html = Path(viz["output"]).read_text(encoding="utf-8")
            self.assertIn("Fanout", html)
            self.assertIn("parallel tracks", html)
            for t in data["tracks"]:
                self.assertIn(t["track"], html)
                self.assertIn(t["run_id"], html)

    def test_fanout_rejects_empty_tracks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [sys.executable, str(CLI), "fanout",
                 "--provider", "stub", "--project", td,
                 "--prompt", "x", "--tracks", "  ", "--json"],
                cwd=ROOT, capture_output=True, text=True, timeout=30, check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            payload = json.loads(proc.stdout)
            self.assertFalse(payload["ok"])

    def test_visualize_renders_lineage_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            parent = run_cli("autopilot", "--provider", "stub", "--project", td, "--prompt", "v1")
            child = run_cli(
                "autopilot", "--provider", "stub", "--project", td,
                "--based-on", parent["run_id"], "--feedback", "iterate me please",
            )
            data = run_cli("visualize", "--project", td, "--run-id", child["run_id"])
            html = Path(data["output"]).read_text(encoding="utf-8")
            self.assertIn("Lineage", html)
            self.assertIn(parent["run_id"], html)
            self.assertIn("iterate me please", html)

    def test_autopilot_extract_code_picks_largest_fenced_block(self) -> None:
        mod = _load_super_skill_module()
        text = "Intro\n```python\ndef tiny(): pass\n```\nMiddle\n```python\ndef bigger():\n    return 42\n\nclass T:\n    pass\n```\nDone."
        lang, code = mod.autopilot_extract_code(text)
        self.assertEqual(lang, "python")
        self.assertIn("bigger", code)
        self.assertNotIn("tiny", code)


if __name__ == "__main__":
    unittest.main()
