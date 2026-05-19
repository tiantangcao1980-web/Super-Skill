"""Tests for the AgentAdapter runtime contract.

Spec: specs/current/agent-adapter-runtime.md
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "super_skill.py"


def _load_super_skill_adapters():
    if "super_skill_adapters" in sys.modules:
        return sys.modules["super_skill_adapters"]
    sys.path.insert(0, str(ROOT / "scripts"))
    import super_skill_adapters  # noqa: WPS433  intentional dynamic import
    return super_skill_adapters


MOD = _load_super_skill_adapters()


def run_cli(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(CLI), *args, "--json"],
        cwd=ROOT, capture_output=True, text=True, timeout=30, check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={proc.stdout}\nstderr={proc.stderr}")
    payload = json.loads(proc.stdout)
    if not payload.get("ok"):
        raise AssertionError(f"command returned ok=false: {args}\n{proc.stdout}")
    return payload["data"]


def run_cli_expect_failure(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(CLI), *args, "--json"],
        cwd=ROOT, capture_output=True, text=True, timeout=30, check=False,
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode != 0
    assert not payload.get("ok")
    return payload.get("error") or {}


# ---------------------------------------------------------------------------
# Protocol mirror parity tests
# ---------------------------------------------------------------------------

class ProtocolDataclassTests(unittest.TestCase):
    def test_detection_to_dict_uses_ts_field_names(self) -> None:
        d = MOD.AgentDetection(
            executable_path="/usr/bin/foo", version="1.2.3",
            config_dir="/tmp/cfg", skills_dir="/tmp/cfg/skills",
        )
        out = d.to_dict()
        self.assertEqual(out["executablePath"], "/usr/bin/foo")
        self.assertEqual(out["configDir"], "/tmp/cfg")
        self.assertEqual(out["skillsDir"], "/tmp/cfg/skills")
        self.assertEqual(out["authState"], "ok")

    def test_capabilities_to_dict_uses_ts_field_names(self) -> None:
        c = MOD.AgentCapabilities(
            surgical_edit=True, native_skill_loading=True,
            streaming=True, resume=False, permission_mode="strict",
            context_window_hint=128000,
        )
        out = c.to_dict()
        self.assertEqual(out["surgicalEdit"], True)
        self.assertEqual(out["nativeSkillLoading"], True)
        self.assertEqual(out["permissionMode"], "strict")
        self.assertEqual(out["contextWindowHint"], 128000)

    def test_registry_has_known_runtimes(self) -> None:
        self.assertIn("null", MOD.REGISTRY)
        self.assertIn("claude-code", MOD.REGISTRY)
        self.assertIn("codex", MOD.REGISTRY)

    def test_null_adapter_returns_no_detection(self) -> None:
        result = MOD.detect_runtime("null")
        self.assertIsNone(result.detection)
        self.assertEqual(result.id, "null")
        self.assertFalse(result.capabilities.streaming)

    def test_unknown_runtime_falls_back_to_null(self) -> None:
        result = MOD.detect_runtime("not-a-real-id")
        self.assertEqual(result.id, "null")
        self.assertIsNone(result.detection)

    def test_run_not_implemented_v1(self) -> None:
        adapter = MOD.NullAdapter()
        with self.assertRaises(NotImplementedError):
            list(adapter.run({"runId": "r1", "cwd": "/tmp", "systemPrompt": "", "userPrompt": ""}))


class TsAndPythonSchemaStayInSyncTests(unittest.TestCase):
    """The TS file is the source of truth. Make sure the Python dataclass
    field names round-trip to the same camelCase keys."""

    TS_FILE = (ROOT / "skills" / "90-codex-patterns" / "dev-tool-adapter"
               / "references" / "agent-adapter.d.ts")

    def setUp(self) -> None:
        self.assertTrue(self.TS_FILE.exists())
        self.ts_text = self.TS_FILE.read_text(encoding="utf-8")

    def test_ts_interface_keys_present_in_python_output(self) -> None:
        detection = MOD.AgentDetection(
            executable_path="x", version="y",
            config_dir="c", skills_dir="s",
        )
        for key in detection.to_dict():
            self.assertIn(key, self.ts_text,
                          f"Python output key {key!r} missing from TS interface")

    def test_ts_capabilities_keys_present_in_python_output(self) -> None:
        caps = MOD.AgentCapabilities(
            surgical_edit=True, native_skill_loading=True,
            streaming=True, resume=True, permission_mode="strict",
            context_window_hint=1000,
        )
        for key in caps.to_dict():
            self.assertIn(key, self.ts_text,
                          f"Python output key {key!r} missing from TS interface")


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------

class AdaptCliDetectOnlyTests(unittest.TestCase):
    def test_detect_only_null(self) -> None:
        data = run_cli("adapt", "--runtime", "null", "--detect-only")
        self.assertEqual(data["id"], "null")
        self.assertIsNone(data["detection"])

    def test_detect_only_requires_runtime(self) -> None:
        err = run_cli_expect_failure("adapt", "--detect-only")
        self.assertIn("requires --runtime", err.get("message", ""))

    @unittest.skipUnless(shutil.which("claude") or shutil.which("claude-code"),
                         "claude CLI not on PATH")
    def test_detect_only_claude_code_found(self) -> None:
        data = run_cli("adapt", "--runtime", "claude-code", "--detect-only")
        self.assertEqual(data["id"], "claude-code")
        self.assertIsNotNone(data["detection"])
        self.assertTrue(data["capabilities"]["streaming"])

    def test_codegen_still_works(self) -> None:
        """The legacy codegen path must keep working when --tool is given."""
        data = run_cli("adapt", "--tool", "cursor",
                       "--project", "/tmp/super-skill-test-adapt-cursor",
                       "--dry-run")
        self.assertEqual(data["tool"], "cursor")
        self.assertGreaterEqual(len(data["files"]), 1)


if __name__ == "__main__":
    unittest.main()
