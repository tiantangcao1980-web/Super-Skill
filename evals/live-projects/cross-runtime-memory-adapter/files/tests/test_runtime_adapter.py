from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from runtime_adapter import RUNTIMES, all_runtime_policies, memory_policy


class RuntimeAdapterTests(unittest.TestCase):
    def test_every_supported_runtime_has_safe_policy(self) -> None:
        policies = all_runtime_policies()
        self.assertEqual({item["runtime"] for item in policies}, set(RUNTIMES))
        for policy in policies:
            self.assertFalse(policy["capture_raw_prompt"])
            self.assertFalse(policy["capture_raw_response"])
            self.assertFalse(policy["auto_promote"])
            self.assertTrue(policy["require_review"])
            self.assertEqual(policy["fallback_skill"], "agent-memory-dream-loop")

    def test_codex_uses_plugin_surface(self) -> None:
        self.assertEqual(memory_policy("Codex")["surface"], "plugin hook")
        self.assertEqual(memory_policy("Cursor")["surface"], "implicit fallback skill")

    def test_unknown_runtime_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            memory_policy("UnknownIDE")


if __name__ == "__main__":
    unittest.main()
