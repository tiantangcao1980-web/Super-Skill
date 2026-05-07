---
name: design-craft-gate
description: Context-gated frontend design workflow for AI agents. Use when designing, redesigning, polishing, auditing, or shipping product UI so PRODUCT.md/DESIGN.md, shape briefs, anti-pattern detection, visual iteration, accessibility, responsive behavior, and DesignDNA tokens stay connected.
---

# Design Craft Gate

Use this skill when a request asks for UI design, redesign, frontend polish,
design critique, design audit, landing pages, product surfaces, onboarding,
dashboards, forms, checkout, settings, or visual quality gates.

This skill upgrades the DesignDNA layer with an agent-executable design loop
inspired by Impeccable's context-first design vocabulary. It does not replace
`designdna`, `design-templates`, or `anti-slop`; it sequences them.

## Operating Loop

1. **Teach / document context.** Find or create the design context before
   implementation:
   - Product context: `PRODUCT.md`, `docs/product.md`, `AGENTS.md`, PRD, issue,
     or equivalent.
   - Design context: `DESIGN.md`, `design/tokens.json`, Storybook, screenshots,
     Figma assets, brand guide, or existing components.
   - If neither exists, produce a compact design-context brief first and mark
     assumptions clearly.
2. **Shape before build.** Write a short shape brief covering user goal, surface,
   content/data, constraints, brand/product register, visual direction, anti-goals,
   and acceptance evidence. Do not start UI edits until the brief is specific.
3. **Craft from tokens.** Implement from tokens, existing components, and the
   selected brand/product register. Use `designdna` for system structure and
   framework skills for code-level implementation.
4. **Critique and audit.** Run a two-pass review:
   - Human-readable critique: hierarchy, clarity, copy, state coverage,
     emotional fit, and brand/product consistency.
   - Deterministic scan: `bin/super-skill design-audit --project <path> --json`
     when local files exist.
5. **Polish and harden.** Fix high-severity findings, then verify accessibility,
   responsive behavior, text overflow, empty/error/loading states, performance
   budget, and reduced-motion handling.
6. **Document the delta.** Update `DESIGN.md`, tokens, component notes, or
   `docs/design-quality.md` when a reusable decision was made.

Load [references/design-context.md](references/design-context.md) when the
project lacks `PRODUCT.md`, `DESIGN.md`, tokens, or a current shape brief.

## Required Preflight

Before UI code edits, report this compact preflight in the work notes:

```text
DESIGN_CRAFT_PREFLIGHT:
context=<pass|missing|assumed>
product_register=<brand|product|mixed|unknown>
shape_brief=<pass|missing>
tokens=<pass|missing|not_applicable>
visual_refs=<pass|skipped:reason>
anti_pattern_gate=<planned|pass|skipped:reason>
mutation=<open|blocked>
```

If `shape_brief=missing` or `mutation=blocked`, create the missing brief or
context artifact before implementation unless the user explicitly asked for a
read-only critique.

## Command Vocabulary

Map design requests onto this vocabulary so the agent and user can reuse a
stable design language:

- **teach**: establish `PRODUCT.md` and `DESIGN.md` context.
- **document**: extract tokens, components, and visual rules from existing code.
- **shape**: plan the UX/UI and acceptance evidence before code.
- **craft**: build the shaped surface with visual iteration.
- **critique**: review hierarchy, clarity, fit, and anti-patterns.
- **audit**: run accessibility, responsive, performance, and deterministic
  anti-pattern checks.
- **polish**: align final implementation with tokens and shipping standards.
- **harden**: cover errors, loading, empty states, i18n, text overflow, and
  reduced motion.
- **typeset / colorize / layout / animate / clarify**: focused remediation
  passes for typography, color, layout, motion, and UX writing.

Load [references/command-vocabulary.md](references/command-vocabulary.md) when
the user names one of these actions.

## Design Laws

Always apply these laws unless an existing brand system explicitly overrides
them:

- Use semantic tokens rather than one-off hex/px values.
- Prefer OKLCH or documented palette ramps for new colors.
- Avoid pure `#000000` and pure `#ffffff` as default surfaces/text.
- Treat gray-on-color, default purple/cyan gradients, nested cards, side-tab
  accents, overused fonts, and bounce/elastic motion as suspicious until proven
  intentional.
- Keep line length near 65-75 characters for prose.
- Animate transform/opacity/color, not layout properties.
- Use cards only when they represent repeated objects, modals, or genuinely
  framed tools.
- Design mobile and desktop states together; stable dimensions must prevent
  labels, icons, and dynamic content from shifting the layout.
- Every word in UI copy should remove uncertainty or trigger the next action.

Load [references/anti-patterns.md](references/anti-patterns.md) and
[references/design-quality-rubric.md](references/design-quality-rubric.md) for
review and remediation.

## Handoffs

- Pair with `designdna` for `DESIGN.md`, tokens, archetypes, and brand-system
  consistency.
- Pair with `anti-slop` for mean-fighting UI bans and replacements.
- Pair with `browser-automation` or the relevant frontend testing skill for
  visual and responsive verification.
- Pair with `output-quality-gate` before delivery.

## Attribution

This Super Skill-native workflow adapts design-harness ideas from Impeccable
without vendoring its implementation. See
[references/impeccable-lessons.md](references/impeccable-lessons.md).
