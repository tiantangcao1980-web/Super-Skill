# Feature: Guided Onboarding Experiment

## Intent

Ship a guided onboarding panel behind a feature flag and decide whether to ramp, hold, or roll back from metrics.

## Acceptance Criteria

- The feature flag keeps the panel disabled for users outside the rollout bucket.
- A kill switch can disable the feature without a deploy.
- Metrics include conversion delta, p95 latency, and error rate.
- Rollback happens automatically when guardrails are violated.
- Memory review records the verified lesson after the experiment.

## Harness Notes

The agent must generate tests before claiming completion and must include release notes, observability signals, and verification evidence.
