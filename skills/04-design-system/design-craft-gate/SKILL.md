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
   - Extraction path: when UI exists but design rules are implicit, run
     `bin/super-skill design-extract --project <path> --json` and use the
     sidecar/markdown draft as a review artifact.
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
   - Live browser pass: `bin/super-skill design-live --project <path>
     --target-url <url> --output .super-skill/design/live.html --json` when
     true computed styles, element overlay, or variant probing matters. Add
     `--write-extension .super-skill/design/extension` when the review should
     happen inside a real Chrome/Chromium tab.
   - Capture pass: `bin/super-skill design-capture --project <root>
     --url <url> --screenshot .super-skill/design/live.png
     --report .super-skill/design/capture.json --json` when an agent needs
     browser-injected screenshot and computed-style evidence. Use `--dry-run`
     in CI or offline environments that should not require Playwright. Use
     `--backend browser-use` for exploratory or authenticated-session capture,
     then promote stable paths back to Playwright.
   - Context gate: `bin/super-skill design-preflight --project <path> --json`
     before mutating a product UI when local files exist.
   - Deterministic scan: `bin/super-skill design-audit --project <path> --json`
     when local files exist.
5. **Polish and harden.** Fix high-severity findings, then verify accessibility,
   responsive behavior, text overflow, empty/error/loading states, performance
   budget, and reduced-motion handling.
6. **Document the delta.** Update `DESIGN.md`, tokens, component notes, or
   `docs/design-quality.md` when a reusable decision was made.

Load [references/design-context.md](references/design-context.md) when the
project lacks `PRODUCT.md`, `DESIGN.md`, tokens, or a current shape brief.

## Asset & Fact Protocol

Run this before designing anything tied to a real brand, product, or library.

- **Verify before design (Principle #0).** If the request names a real product,
  version, or component library, confirm it exists and its current specs with a
  quick `WebSearch` first. Ten seconds of checking saves an hour redoing work
  built on a wrong assumption.
- **Assets are facts, not memory.** Never guess a brand's colors, logo, or
  imagery. Resolve them through a degradation chain and freeze the result:
  1. Ask the user for brand assets or a guide when ambiguous.
  2. Search official sources: brand site, press kit, public design system.
  3. Download with fallbacks — logo: SVG → inline SVG → PNG; imagery: hero shot
     → press image → representative frame.
  4. `grep` real hex / token values out of the downloaded assets — never
     eyeball a color.
  5. Freeze into `brand-spec.md` (or `DESIGN.md` tokens) so every downstream
     skill consumes verified facts, not guesses.

This pairs with `designdna` as the token authority and feeds the shared-artifact
seam in `skill-composition`.

## Shape Gap Matrix

Before writing the shape brief, fill this gap matrix (adapted from
stitch-skills' `enhance-prompt`, Apache-2.0). Each row is `known | assumed |
ask`; anything left `ask` blocks the build until resolved or explicitly waived.

| Dimension | Resolved? |
| --- | --- |
| Platform / device (web, mobile, responsive range) | known / assumed / ask |
| Page type & primary job (landing, dashboard, form, checkout…) | known / assumed / ask |
| Structure & key sections (what blocks, in what order) | known / assumed / ask |
| Style register (brand vs product, dials) | known / assumed / ask |
| Colors & tokens (frontmatter contract present?) | known / assumed / ask |
| Component vocabulary (which library / patterns) | known / assumed / ask |
| Content & data (real copy, real numbers, states) | known / assumed / ask |

Turn every `assumed` into an explicit assumption in the brief, and every `ask`
into a question or a verified fact before UI edits.

## Required Preflight

Before UI code edits, report this compact preflight in the work notes:

```text
DESIGN_CRAFT_PREFLIGHT:
context=<pass|missing|assumed>
product_register=<brand|product|mixed|unknown>
shape_brief=<pass|missing>
tokens=<pass|missing|not_applicable>
visual_refs=<pass|skipped:reason>
assets=<verified|not_applicable|assumed:reason>
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
  Use `design-extract` when local files exist.
- **shape**: plan the UX/UI and acceptance evidence before code.
- **craft**: build the shaped surface with visual iteration.
- **critique**: review hierarchy, clarity, fit, and anti-patterns.
- **audit**: run context, accessibility, responsive, performance, and
  deterministic anti-pattern checks.
- **live**: generate a browser overlay panel for computed styles, contrast
  probes, and CSS-variable variants.
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
- Every `DESIGN.md` carries a parseable `name`+`colors` YAML frontmatter (the
  machine contract from `designdna`); treat a missing frontmatter as an
  incomplete design system. For multi-page surfaces, keep generation prompts to
  layout/content and inject tokens once at project level.
- Prefer OKLCH or documented palette ramps for new colors.
- Avoid pure `#000000` and pure `#ffffff` as default surfaces/text.
- Treat gray-on-color, default purple/cyan gradients, nested cards, side-tab
  accents, low-contrast gray text, skipped heading levels, cramped padding,
  flat type hierarchy, overused fonts, and bounce/elastic motion as suspicious
  until proven intentional.
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
