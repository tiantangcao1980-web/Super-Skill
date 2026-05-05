---
name: business-case
description: Decide whether a project deserves the budget. Outputs a tight business case with market sizing, ROI estimate, cost/revenue model, risk register, and an explicit go / no-go / pivot recommendation. Use when a stakeholder asks "should we build this?", when preparing a project charter or steering-committee deck, when committing engineering capacity to a new initiative, when a feature request needs ROI justification, or when invoked as autopilot's phase 02-business-case.
---

# Business Case — Should we build this?

**Tradeoff.** This skill biases toward kill-it-early over invest-anyway. For
exploratory R&D where the answer is obviously "yes, prototype it", use
judgment and skip — running the full case adds 2-3 LLM calls of friction.
For anything that costs >1 quarter of engineering time, run all six sections.

## The six required sections

### 1. Problem worth solving

- Restate the problem in one sentence in the language of a non-technical
  stakeholder. If you can't, stop — phase 0 research wasn't deep enough.
- Cite at least one piece of evidence the problem exists today (interview
  quote, support ticket count, churn signal, competitor pricing data).

### 2. Market sizing (TAM / SAM / SOM)

- TAM: total addressable market — order of magnitude is enough.
- SAM: serviceable available market — what we could realistically reach.
- SOM: serviceable obtainable market — what we'd actually capture in 12 months.
- One number per row, with a unit (revenue / users / transactions).

### 3. Business model

- Who pays? (B2B / B2C / B2B2C / sponsored / freemium / usage-based)
- How do we charge? (subscription / per-seat / per-transaction / tier)
- What's the unit economics? (rough CAC, LTV, gross margin)
- One sentence on the moat (why us vs. competitor X).

### 4. ROI estimate

| Side | Year 1 | Year 2 | Year 3 |
| --- | --- | --- | --- |
| Cost (engineering + ops + marketing) | $ | $ | $ |
| Revenue / measurable savings | $ | $ | $ |
| Net | $ | $ | $ |

- Payback period (months until cumulative net ≥ 0).
- IRR or simple multiple — pick one, don't over-engineer.

### 5. Risk register

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Technical (e.g. unproven dependency) | L/M/H | L/M/H | … |
| Market (e.g. competitor ship) | L/M/H | L/M/H | … |
| Compliance (e.g. data residency) | L/M/H | L/M/H | … |
| Delivery (e.g. team capacity) | L/M/H | L/M/H | … |

If any risk is High × High and has no mitigation, surface it as a blocker.

### 6. Recommendation — go / no-go / pivot

- **Go**: budget is X, deadline is Y, owner is Z. List the next-three-actions.
- **No-go**: state the disqualifying risk or ROI gap. Suggest one cheaper
  alternative that addresses the same problem.
- **Pivot**: recommend a smaller scope or different market segment that
  lifts the ROI above threshold.

## Anti-patterns

**Wrong: "we'll figure out the business model later".** A project without a
business model is a hobby. Phase 02 exists to catch this before phase 05
implementation burns six weeks.

**Wrong: hand-wavy market sizing ("massive market!").** TAM/SAM/SOM with
real numbers — even rough ones — beats vibes. If the market is genuinely
unknowable, the recommendation is "spike a 2-week paid pilot, then revisit".

**Wrong: hiding risks because they'd kill the project.** A high-likelihood
high-impact risk with a credible mitigation is fine. A hidden risk
discovered at phase 09 pilot is what kills companies.

**Wrong: ROI based only on revenue.** Cost-saving and risk-reduction count
too. State the dollar value of the savings or the avoided fine.

## Composes with

- `requirement-analysis` (phase 0) — feeds the problem statement
- `intent-contract` (phase 1) — the acceptance criteria become the
  measurable side of the ROI table
- `experiment-driven-delivery` (phase 9 pilot) — the success metrics
  defined here are what the pilot is supposed to validate
- `output-quality-gate` (phase 7) — checks deliverable against business case
