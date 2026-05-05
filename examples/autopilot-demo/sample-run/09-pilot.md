## Pilot Plan (stub)
### Pilot cohort
- 3-5 representative customers covering the two primary segments.
- Selection rule: existing engaged users + at least one churn-risk account.
### Scope under flag
- The MVP slice from phase 05; everything else stays on legacy path.
### Success metrics & thresholds
- Activation: ≥70% of pilot users complete the core flow within 7 days.
- Quality: error rate ≤1% across pilot traffic.
- Stickiness: ≥40% week-2 return rate.
### Monitoring & alerting
- Per-cohort dashboards keyed by trace id.
- Pager alerts on error-rate >2% (p1) and >5% (p0).
### Rollback triggers
- Any p0 alert sustained >10 min, or pilot NPS < 0.
### Feedback collection
- In-app prompt at flow completion; weekly 15-min interview with each pilot account.
### Decision rule
- All three metric thresholds met for 2 consecutive weeks → go-wide.
- Any single threshold missed by >20% → iterate, do not expand.
- Trace: stub-ad919ac145

