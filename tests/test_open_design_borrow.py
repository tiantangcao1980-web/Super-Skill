"""Tests for the open-design–borrow round.

Covers the four new contracts:

1. Anti-AI-slop rules (P0 cardinal sins) actually fire on a deliberately bad
   fixture, and do **not** fire on the existing happy live-eval fixture.
2. The Critique Jury weighted composite math is correct; the autopilot
   grader catches a panel-vs-verdict mismatch as not-ok.
3. The atom catalog accepts a valid pipeline and rejects unknown atom ids /
   unknown until-signal names.
4. The audit picks up super-skill.json sidecars, surfaces the count, and
   fails the audit when a sidecar is malformed.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "super_skill.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_super_skill_module():
    if "super_skill" in sys.modules:
        return sys.modules["super_skill"]
    import importlib.util
    spec = importlib.util.spec_from_file_location("super_skill", CLI)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["super_skill"] = mod
    spec.loader.exec_module(mod)
    return mod


def run_cli_raw(*args: str, cwd: Path = ROOT, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), *args, "--json"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def run_cli(*args: str, cwd: Path = ROOT, timeout: int = 30) -> dict:
    proc = run_cli_raw(*args, cwd=cwd, timeout=timeout)
    if proc.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={proc.stdout[:500]}\nstderr={proc.stderr[:500]}")
    payload = json.loads(proc.stdout)
    if not payload.get("ok"):
        raise AssertionError(f"command returned ok=false: {args}\n{proc.stdout[:500]}")
    return payload["data"]


def run_cli_expect_failure(*args: str, cwd: Path = ROOT, timeout: int = 30) -> dict:
    proc = run_cli_raw(*args, cwd=cwd, timeout=timeout)
    payload = json.loads(proc.stdout)
    assert proc.returncode != 0, f"expected non-zero exit, got 0; stdout={proc.stdout[:500]}"
    assert not payload.get("ok"), f"expected ok=false, got ok=true; stdout={proc.stdout[:500]}"
    return payload.get("error") or {}


# ---------------------------------------------------------------------------
# Anti-AI-slop fixture coverage
# ---------------------------------------------------------------------------

class AntiSlopRuleTests(unittest.TestCase):
    """Prove the seven cardinal sins fire on a deliberately bad fixture."""

    POSITIVE_FIXTURE = FIXTURES / "anti-slop-positive"

    def test_positive_fixture_trips_p0_rules(self) -> None:
        proc = run_cli_raw("design-audit", "--project", str(self.POSITIVE_FIXTURE), "--fail-on-findings")
        # design-audit with --fail-on-findings exits non-zero if any finding exists.
        self.assertNotEqual(proc.returncode, 0, "expected design-audit to flag the cardinal-sins fixture")
        payload = json.loads(proc.stdout)
        data = payload.get("error") or payload.get("data")
        rules_fired = set(data["findings_by_rule"].keys())
        # Six P0 rules must fire (ai-dashboard-tile depends on same-line CSS, included in fixture).
        required = {
            "tailwind-indigo-hex",
            "trust-two-stop-gradient",
            "emoji-feature-icon",
            "invented-metric",
            "lorem-filler-copy",
            "ai-dashboard-tile",
        }
        missing = required - rules_fired
        self.assertFalse(missing, f"P0 anti-slop rules failed to fire: {missing}")
        # Plus the P1 placeholder-cdn rule.
        self.assertIn("placeholder-cdn", rules_fired)
        # P0 weight is 25 so a single P0 already pushes score below the pass band.
        self.assertEqual(data["status"], "fail")
        self.assertEqual(data["findings_by_severity"].get("P0", 0) >= 6, True,
                         f"expected ≥6 P0 findings, got {data['findings_by_severity']}")

    def test_happy_live_fixture_still_passes(self) -> None:
        """Make sure the new P0 rules don't regress the existing live-eval happy path."""
        happy_dir = ROOT / "evals" / "live-projects" / "design-frontend-quality-gate" / "files" / "src"
        data = run_cli("design-audit", "--project", str(happy_dir), "--fail-on-findings")
        self.assertEqual(data["findings_total"], 0)
        self.assertEqual(data["status"], "pass")
        self.assertEqual(data["score"], 100)


# ---------------------------------------------------------------------------
# Critique Jury (5-panel weighted composite)
# ---------------------------------------------------------------------------

class CritiqueJuryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = _load_super_skill_module()

    def test_weights_sum_to_one(self) -> None:
        total = sum(self.mod.CRITIQUE_JURY_WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0, places=6)

    def test_panels_are_the_five_expected(self) -> None:
        self.assertEqual(
            set(self.mod.CRITIQUE_JURY_PANELS),
            {"critic", "brand", "a11y", "copy", "designer"},
        )

    def test_composite_threshold_is_8(self) -> None:
        self.assertEqual(self.mod.CRITIQUE_JURY_THRESHOLD, 8.0)
        self.assertEqual(self.mod.CRITIQUE_JURY_MAX_ROUNDS, 3)

    def test_composite_passing_panel(self) -> None:
        panel = {role: {"score": 9} for role in self.mod.CRITIQUE_JURY_PANELS}
        composite = self.mod.critique_jury_composite(panel)
        self.assertGreaterEqual(composite, self.mod.CRITIQUE_JURY_THRESHOLD)
        self.assertEqual(self.mod.critique_jury_verdict(composite), "pass")

    def test_composite_failing_panel(self) -> None:
        panel = {role: {"score": 4} for role in self.mod.CRITIQUE_JURY_PANELS}
        composite = self.mod.critique_jury_composite(panel)
        self.assertLess(composite, self.mod.CRITIQUE_JURY_THRESHOLD - 1.5)
        self.assertEqual(self.mod.critique_jury_verdict(composite), "fail")

    def test_grader_catches_panel_verdict_mismatch(self) -> None:
        """A model that claims `verdict: pass` while the panel sums below the
        threshold must be marked not-ok by the recompute safeguard."""
        text = json.dumps({
            "matches_intent": True,
            "evidence_present": True,
            "missing": [],
            "verdict": "pass",       # lying
            "score": 9,
            "panel": {
                "critic":   {"score": 3, "notes": "bad"},
                "brand":    {"score": 4, "notes": "bad"},
                "a11y":     {"score": 4, "notes": "bad"},
                "copy":     {"score": 4, "notes": "bad"},
                "designer": {"score": 4, "notes": "bad"},
            },
            "composite": 8.6,        # lying
            "threshold": 8.0,
            "round": 1,
        })
        result = self.mod.autopilot_grade_gate(text)
        self.assertTrue(result["parsed"])
        self.assertLess(result["composite_recomputed"], 6.5)
        self.assertEqual(result["canonical_verdict"], "fail")
        self.assertFalse(result["ok"], "lying verdict must be caught by recompute")


# ---------------------------------------------------------------------------
# Atom catalog validator
# ---------------------------------------------------------------------------

class AtomCatalogTests(unittest.TestCase):
    def test_catalog_has_implemented_atoms(self) -> None:
        data = run_cli("atoms")
        self.assertGreaterEqual(data["implemented"], 10)
        vocab = set(data["until_signals"]["vocabulary"])
        self.assertIn("critique.score", vocab)
        self.assertIn("iterations", vocab)
        self.assertIn("tests.pass", vocab)

    def test_validate_accepts_good_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "good.json"
            p.write_text(json.dumps({
                "od": {"pipeline": {"stages": [
                    {"id": "build", "atoms": ["ralph-attempt"], "until": "tests.pass || iterations >= 5"},
                    {"id": "gate", "atoms": ["critique-jury"], "until": "critique.score >= 8"},
                ]}}
            }), encoding="utf-8")
            data = run_cli("atoms", "--validate", str(p))
            self.assertEqual(data["failures"], [])
            self.assertEqual(data["validation"]["referenced_atoms"],
                             ["ralph-attempt", "critique-jury"])

    def test_validate_rejects_unknown_atom_and_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text(json.dumps({
                "od": {"pipeline": {"stages": [
                    {"id": "x", "atoms": ["unknown-atom-xyz"], "until": "made.up.signal && iterations >= 5"},
                ]}}
            }), encoding="utf-8")
            err = run_cli_expect_failure("atoms", "--validate", str(p))
            checks = {f["check"] for f in err.get("failures", [])}
            self.assertIn("unknown-atom", checks)
            self.assertIn("unknown-until-signal", checks)

    def test_validate_warns_on_planned_atom(self) -> None:
        """Planned atoms should be allowed (forward-compat) but warn."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "planned.json"
            p.write_text(json.dumps({
                "od": {"pipeline": {"stages": [
                    {"id": "preview", "atoms": ["live-artifact"], "until": "preview.ok"},
                ]}}
            }), encoding="utf-8")
            data = run_cli("atoms", "--validate", str(p))
            self.assertEqual(data["failures"], [])
            warnings = {w["check"] for w in data.get("warnings", [])}
            self.assertIn("planned-atom", warnings)


# ---------------------------------------------------------------------------
# super-skill.json sidecar
# ---------------------------------------------------------------------------

class SuperSkillSidecarTests(unittest.TestCase):
    SIDECAR = ROOT / "skills" / "00-orchestration" / "atom-catalog" / "super-skill.json"

    def test_atom_catalog_ships_sidecar(self) -> None:
        self.assertTrue(self.SIDECAR.exists(), "atom-catalog ships a super-skill.json sidecar")
        data = json.loads(self.SIDECAR.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "atom-catalog")
        self.assertEqual(data["specVersion"], "1.0.0")

    def test_audit_reports_sidecar_count(self) -> None:
        data = run_cli("audit")
        paths = [m["path"] for m in data["super_skill_manifests"]]
        self.assertIn(
            "skills/00-orchestration/atom-catalog/super-skill.json", paths,
            f"sidecar missing from audit report: {paths}",
        )

    def test_audit_fails_on_broken_sidecar(self) -> None:
        """Temporarily corrupt the sidecar and confirm audit fails. Restore after."""
        original = self.SIDECAR.read_text(encoding="utf-8")
        try:
            self.SIDECAR.write_text("{not valid json", encoding="utf-8")
            err = run_cli_expect_failure("audit")
            checks = {f["check"] for f in err.get("failures", [])}
            self.assertIn("super-skill-manifests", checks)
        finally:
            self.SIDECAR.write_text(original, encoding="utf-8")


# ---------------------------------------------------------------------------
# CONTEXT.md + craft/ presence
# ---------------------------------------------------------------------------

class DocsBorrowingTests(unittest.TestCase):
    def test_context_md_exists_and_defines_core_terms(self) -> None:
        path = ROOT / "CONTEXT.md"
        self.assertTrue(path.exists())
        body = path.read_text(encoding="utf-8")
        for term in (
            "**Skill**",
            "**Installable Skill**",
            "**Atom**",
            "**Phase**",
            "**Stage**",
            "**Critique Jury",
            "**Memory Candidate**",
            "**Protected Skill**",
            "**Risky Pattern**",
        ):
            self.assertIn(term, body, f"CONTEXT.md missing term: {term}")

    def test_craft_directory_has_brand_agnostic_rules(self) -> None:
        craft = ROOT / "craft"
        self.assertTrue(craft.is_dir())
        for required in (
            "README.md",
            "anti-ai-slop.md",
            "typography.md",
            "color.md",
            "accessibility-baseline.md",
            "state-coverage.md",
            "animation-discipline.md",
            "form-validation.md",
            "laws-of-ux.md",
        ):
            self.assertTrue((craft / required).is_file(), f"craft/{required} missing")


if __name__ == "__main__":
    unittest.main()
