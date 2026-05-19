# Critique Jury offline fixtures

Mocks of the Phase 6 quality gate output a real LLM would produce. Each
fixture targets one failure mode so we can prove the grader catches it:

| File | Composite | Expected `autopilot_grade_gate` |
| --- | --- | --- |
| `happy.json` | 8.6 | `verdict=pass`, `ok=True`, `canonical_verdict=pass` |
| `warn.json` | 7.0 | `verdict=warn`, `ok=True`, `canonical_verdict=warn` |
| `fail.json` | 4.0 | `verdict=fail`, `ok=False`, `canonical_verdict=fail` |
| `panel-verdict-mismatch.json` | 4.2 (lying as pass) | `ok=False` — recompute catches the lie |
| `malformed.json` | n/a | `parsed=False`, `ok=False` |

Spec: `specs/current/critique-jury-llm.md`. No real LLM call needed — these
are byte-deterministic JSON files representing the schema the gate enforces.
