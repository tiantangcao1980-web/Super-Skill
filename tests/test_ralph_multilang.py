"""Direct tests for the four ralph language runners (Python/JS/Bash/Go).

Each test that requires a non-Python toolchain skips itself if the executable
is not on PATH. Spec: specs/current/ralph-multi-language.md
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_super_skill_module():
    if "super_skill" in sys.modules:
        return sys.modules["super_skill"]
    import importlib.util
    spec = importlib.util.spec_from_file_location("super_skill", ROOT / "scripts" / "super_skill.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["super_skill"] = mod
    spec.loader.exec_module(mod)
    return mod


MOD = _load_super_skill_module()


class PythonRunnerTests(unittest.TestCase):
    def test_passing_bare_tests(self) -> None:
        code = (
            "def add(a, b):\n    return a + b\n\n"
            "def test_add():\n    assert add(1, 2) == 3\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_python_tests(code, Path(tmp))
        self.assertTrue(res["ok"], res)
        self.assertIn(res["kind"], {"bare-tests", "unittest"})

    def test_failing_bare_tests_reports_stderr(self) -> None:
        code = (
            "def add(a, b):\n    return 0\n\n"   # deliberately wrong
            "def test_add():\n    assert add(1, 2) == 3\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_python_tests(code, Path(tmp))
        self.assertFalse(res["ok"], "ralph must catch deliberately broken Python code")
        self.assertIn("FAIL", res.get("stderr_tail", ""))

    def test_py_compile_only_for_no_tests(self) -> None:
        code = "def hello():\n    return 'hi'\n"
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_python_tests(code, Path(tmp))
        self.assertTrue(res["ok"], res)
        self.assertEqual(res["kind"], "py-compile")


@unittest.skipUnless(shutil.which("node"), "node not on PATH; skipping JS ralph runner test")
class JavaScriptRunnerTests(unittest.TestCase):
    def test_passing_node_bare_tests(self) -> None:
        code = (
            "function add(a, b) { return a + b; }\n"
            "function test_add() {\n"
            "  if (add(1, 2) !== 3) throw new Error('expected 3');\n"
            "}\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_javascript(code, Path(tmp), ext="js")
        self.assertTrue(res["ok"], res)
        self.assertIn("node", res["argv"][0])

    def test_failing_node_test_reports_stderr(self) -> None:
        code = (
            "function add(a, b) { return 0; }\n"  # wrong
            "function test_add() {\n"
            "  if (add(1, 2) !== 3) throw new Error('expected 3');\n"
            "}\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_javascript(code, Path(tmp), ext="js")
        self.assertFalse(res["ok"])
        self.assertIn("FAIL", res.get("stderr_tail", ""))


@unittest.skipUnless(shutil.which("bash"), "bash not on PATH; skipping Bash ralph runner test")
class BashRunnerTests(unittest.TestCase):
    def test_safe_set_e_executes(self) -> None:
        code = "set -euo pipefail\nA=$((1 + 2))\n[[ \"$A\" == 3 ]]\n"
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_bash(code, Path(tmp))
        self.assertTrue(res["ok"], res)
        self.assertEqual(res["kind"], "bash-exec")

    def test_parse_check_fails_on_syntax_error(self) -> None:
        code = "if [ then echo 'broken'\n"  # missing condition
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_bash(code, Path(tmp))
        self.assertFalse(res["ok"], res)
        self.assertEqual(res["kind"], "bash-parse")

    def test_without_set_e_only_parse_checks(self) -> None:
        """Scripts without `set -e` are not executed (safety default)."""
        code = "echo hello\n"
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_bash(code, Path(tmp))
        self.assertTrue(res["ok"], res)
        self.assertEqual(res["kind"], "bash-parse-only")


@unittest.skipUnless(shutil.which("go"), "go not on PATH; skipping Go ralph runner test")
class GoRunnerTests(unittest.TestCase):
    def test_go_vet_on_simple_pkg(self) -> None:
        code = (
            "package main\n\nimport \"fmt\"\n\n"
            "func main() {\n    fmt.Println(\"hi\")\n}\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_go(code, Path(tmp))
        self.assertTrue(res["ok"], res)
        self.assertIn(res["kind"], {"go-vet", "go-test"})

    def test_go_vet_fails_on_obviously_broken(self) -> None:
        code = "package main\n\nfunc main(\n"  # unfinished
        with tempfile.TemporaryDirectory() as tmp:
            res = MOD.autopilot_run_go(code, Path(tmp))
        self.assertFalse(res["ok"], res)


class DoctorRalphTests(unittest.TestCase):
    """Doctor must surface which language runners are available."""

    def test_doctor_reports_python_runner(self) -> None:
        # Doctor always reports python because that's required to run the CLI itself.
        from io import StringIO
        import argparse, json as _json, contextlib
        ns = argparse.Namespace(json=True)
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            MOD.cmd_doctor(ns)
        payload = _json.loads(buf.getvalue())
        langs = {r["language"]: r["available"] for r in payload["data"]["ralph_runners"]}
        self.assertIn("python", langs)
        self.assertIn("javascript", langs)
        self.assertIn("bash", langs)
        self.assertIn("go", langs)
        self.assertTrue(langs["python"], "doctor must mark python as available")


if __name__ == "__main__":
    unittest.main()
