# Design Command Vocabulary

Use these commands as mental routing labels. They are not required shell
commands; they are reusable design work modes.

## Setup Commands

| Mode | Use when | Output |
| --- | --- | --- |
| `teach` | The project lacks product/design context | `PRODUCT.md` plus optional `DESIGN.md` draft |
| `document` | UI exists but design rules are implicit | token inventory, component notes, `DESIGN.md` update |
| `extract` | Repeated UI should become reusable | tokens/components, migration plan, docs |

## Creation Commands

| Mode | Use when | Output |
| --- | --- | --- |
| `shape` | The user wants UI but the surface is underspecified | shape brief and acceptance evidence |
| `craft` | Shape is clear and code can be changed | implemented surface plus verification |
| `onboard` | First-run, empty, or activation path is weak | activation flow, empty states, first success moment |
| `delight` | The product works but lacks memorability | small, purposeful moments that do not hide core utility |
| `overdrive` | The user explicitly asks for exceptional technical craft | advanced motion/interaction guarded by performance and accessibility |

## Remediation Commands

| Mode | Use when | Output |
| --- | --- | --- |
| `critique` | A design needs judgment before changes | findings ranked by user impact and risk |
| `audit` | A design needs machine-checkable quality evidence | a11y/responsive/performance/anti-pattern report |
| `polish` | The implementation is close but uneven | token alignment, copy, states, spacing, visual QA fixes |
| `harden` | Edge cases are missing | error/loading/empty/i18n/overflow/reduced-motion coverage |
| `typeset` | Typography feels generic or hard to scan | font, scale, hierarchy, line-length fixes |
| `colorize` | Color is generic, inaccessible, or off-brand | semantic palette and contrast fixes |
| `layout` | Rhythm, density, alignment, or composition is weak | responsive layout and spatial hierarchy fixes |
| `animate` | Motion is absent or noisy | purposeful motion with reduced-motion fallback |
| `clarify` | Copy, labels, or error messages are unclear | concise task-oriented UX writing |
| `adapt` | A surface fails a viewport, locale, or device | responsive and contextual variants |
| `optimize` | The design is visually heavy or slow | performance-aware asset/motion/layout simplification |

## Routing Heuristic

If the user asks for a page/component and context is missing, run `teach` or
`shape` first. If context exists, run `craft`. If the user asks whether a design
is good, run `critique` then `audit`. If the user says it is almost there, run
`polish` and only change the smallest surface that improves the outcome.
