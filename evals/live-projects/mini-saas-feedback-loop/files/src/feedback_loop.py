from __future__ import annotations


def is_feature_enabled(config: dict, user_bucket: int) -> bool:
    if config.get("kill_switch"):
        return False
    if not config.get("enabled"):
        return False
    return user_bucket < int(config.get("rollout_percent", 0))


def decide_rollout(metrics: dict, guardrails: dict) -> dict:
    if metrics["p95_latency_ms"] > guardrails["max_p95_latency_ms"]:
        return {"decision": "rollback", "reason": "latency guardrail"}
    if metrics["error_rate"] > guardrails["max_error_rate"]:
        return {"decision": "rollback", "reason": "error guardrail"}
    if metrics["conversion_delta"] < guardrails["min_conversion_delta"]:
        return {"decision": "kill", "reason": "conversion regression"}
    return {"decision": "ramp", "reason": "metrics healthy"}


def memory_review_note(decision: dict) -> str:
    return f"Record verified experiment lesson after {decision['decision']}: {decision['reason']}"
