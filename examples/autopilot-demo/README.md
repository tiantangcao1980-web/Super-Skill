# Autopilot Demo

Two ways to see the harness loop end to end:

## 1. Offline (deterministic stub, no API key)

```bash
./run-real-autopilot.sh --offline "Build a Python add(a,b) function with one bare test_add()"
```

Or just run with no key set — the script falls back to stub automatically.

## 2. Real LLM (Anthropic)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
./run-real-autopilot.sh "Build a Python TODO list CLI with one happy-path test"
```

The script:

1. Runs `bin/super-skill autopilot --provider <stub|anthropic>`
2. Sets `--max-ralph-rounds 10` (the inner Ralph loop will retry phase 4 up to 10 times if `python -m unittest`/bare-tests fail)
3. Prints the artifact list and a `cat run.json` hint at the end

## What the artifacts look like

`sample-run/` contains a captured run produced by the offline stub provider against the prompt **"Build a calculator"** — so you can see exactly what gets checkpointed without running anything:

```
sample-run/
├── 00-research.md                ← Problem / users / competitors / assumptions
├── 01-intent-contract.md         ← Goal / Acceptance / Out of scope / Evidence
├── 02-business-case.md           ← TAM/SAM/SOM / ROI table / risks / go-no-go
├── 03-product-spec.md            ← MVP slice / success metric / rollback
├── 04-design.md                  ← DESIGN.md tokens (palette, type, layout)
├── 05-implementation.md          ← code (Python / JS / Bash / Go) with tests
├── 06-simplified.md              ← post-simplifier output
├── 07-quality-gate.json          ← {"verdict":"pass", "score":8, ...}
├── 08-launch-readiness.md        ← Dockerfile / CI / kill switch / rollback / pricing
├── 09-pilot.md                   ← cohort / metrics / rollback triggers / decision rule
├── 10-commercial-delivery.md     ← acceptance / SLA / billing / training / signoff
├── 11-ops-retrospective.md       ← memory candidate + ops dashboard + roadmap
├── run.json                      ← full audit journal
└── timeline.html                 ← single-page rendering of the run
```

Open `run.json` to see per-phase token counts, ralph-loop attempts, hard-gate
verdicts, and the run id.

## Notes

- **Phase 4 actually runs your generated Python.** If the LLM emits broken code,
  `python -m unittest` (or bare `test_*` runner, or `py_compile` for non-test
  code) will fail and the stderr is fed back into the next Ralph attempt.
- **The memory candidate (phase 7) never echoes the raw user prompt** — that's
  enforced by both the canonical agent-memory-dream-loop skill and the live-eval
  in `evals/live-projects/autopilot-end-to-end/`.
- **You can resume** an interrupted run with `bin/super-skill resume --project ./build`.
