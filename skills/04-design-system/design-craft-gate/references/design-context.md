# Design Context Contract

Design agents need product context and visual context. Treat both as first-class
inputs.

## Product Context

Look for:

- `PRODUCT.md`
- PRD, issue, user story, or OpenSpec change
- `AGENTS.md` product guidance
- analytics, funnel notes, support tickets, or sales objections

Minimum fields:

- target user
- user job and success moment
- business goal
- key constraints
- anti-goals
- confidence level and open questions

## Design Context

Look for:

- `DESIGN.md`
- `design/tokens.json`
- brand guideline, Figma frame, screenshot, Storybook, component library
- existing CSS variables, theme config, Tailwind config, component primitives

Minimum fields:

- brand/product register: brand-led, product-led, mixed, or unknown
- palette and semantic token roles
- typography roles and scale
- spacing/radius/elevation rules
- interaction/motion rules
- banned patterns and anti-references

## Shape Brief Template

```text
Surface:
User goal:
Primary task:
Content/data available:
Brand/product register:
Visual direction:
Constraints:
Anti-goals:
States to cover:
Responsive targets:
Acceptance evidence:
Open questions:
```

Keep the shape brief compact. It should guide code and review, not become a
static spec that blocks iteration.
