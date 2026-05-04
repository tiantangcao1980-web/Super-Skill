from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from render_dashboard import load_tokens, render_dashboard


class DashboardQualityTests(unittest.TestCase):
    def test_render_uses_tokens_and_accessibility(self) -> None:
        tokens = load_tokens(ROOT / "design" / "tokens.json")
        html = render_dashboard(tokens)
        self.assertIn(tokens["brand"], html)
        self.assertIn("aria-label", html)
        self.assertIn("grid-template-columns", html)
        self.assertIn("--accent", html)

    def test_render_avoids_visual_slop_patterns(self) -> None:
        html = render_dashboard(load_tokens(ROOT / "design" / "tokens.json")).lower()
        self.assertNotIn("letter-spacing: -", html)
        self.assertNotIn("gradient orb", html)
        self.assertNotIn("bokeh", html)
        self.assertNotIn("manual svg hero", html)


if __name__ == "__main__":
    unittest.main()
