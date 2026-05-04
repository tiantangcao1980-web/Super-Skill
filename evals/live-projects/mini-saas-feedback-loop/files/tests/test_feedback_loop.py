from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from feedback_loop import decide_rollout, is_feature_enabled, memory_review_note


class FeedbackLoopTests(unittest.TestCase):
    def test_feature_flag_and_kill_switch(self) -> None:
        config = {"enabled": True, "rollout_percent": 10, "kill_switch": False}
        self.assertTrue(is_feature_enabled(config, 5))
        self.assertFalse(is_feature_enabled(config, 20))
        config["kill_switch"] = True
        self.assertFalse(is_feature_enabled(config, 1))

    def test_rollout_decision_uses_metrics(self) -> None:
        guardrails = {"max_p95_latency_ms": 400, "max_error_rate": 0.01, "min_conversion_delta": 0}
        healthy = {"p95_latency_ms": 210, "error_rate": 0.002, "conversion_delta": 0.04}
        self.assertEqual(decide_rollout(healthy, guardrails)["decision"], "ramp")
        slow = dict(healthy, p95_latency_ms=900)
        self.assertEqual(decide_rollout(slow, guardrails)["decision"], "rollback")
        negative = dict(healthy, conversion_delta=-0.02)
        self.assertEqual(decide_rollout(negative, guardrails)["decision"], "kill")

    def test_memory_note_is_reviewable(self) -> None:
        note = memory_review_note({"decision": "rollback", "reason": "latency guardrail"})
        self.assertIn("verified experiment lesson", note)
        self.assertIn("rollback", note)


if __name__ == "__main__":
    unittest.main()
