# Observability

The service emits structured logs for `feature_decision`, `rollout_bucket`, `conversion_delta`, `p95_latency_ms`, and `error_rate`.

Triage groups failures by feature key and guardrail. Verification checks that the same metrics resolve after rollback or ramp.
