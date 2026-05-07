# Design Anti-Patterns

These are deterministic or near-deterministic warning signs in AI-generated UI.
They are not absolute bans; an existing brand system may override them, but the
agent must make the intent explicit.

## High-Signal Rules

| Pattern | Why it matters | Prefer |
| --- | --- | --- |
| `gradient-text` | Often hides weak hierarchy behind decoration | solid or tokenized accent text |
| `ai-color-palette` | Purple/cyan gradients are a common AI default | brand-specific or task-specific color strategy |
| `side-tab` | Decorative left/right accent borders create repeated card sameness | structure, typography, or data priority |
| `nested-cards` | Cards inside cards add noise and reduce scan speed | sections, rows, dividers, or true repeated items |
| `pure-black-white` | Harsh defaults and weak brand warmth | near-black, off-white, tinted neutrals |
| `gray-on-color` | Low contrast and muted status meaning | accessible color pairs with semantic roles |
| `overused-font` | Generic SaaS feel when not brand-driven | brand font or intentionally selected alternative |
| `bounce-easing` | Dated, playful motion in serious product contexts | ease-out quart/quint/expo or spring only with intent |
| `layout-transition` | Animating layout properties is janky and hard to reason about | transform, opacity, color |
| `tiny-text` | Accessibility and scan-speed risk | at least 12px for auxiliary text, larger for body |

## Manual Critique Prompts

- What decision does this visual choice help the user make?
- Does this surface reveal real product state or hide behind decoration?
- Is the layout optimized for repeated use or only first impression?
- Are cards used for objects, or are they compensating for weak hierarchy?
- Would the design still work if all gradients were removed?
- Does motion clarify cause/effect, or merely signal "made by AI"?

Use `bin/super-skill design-audit --project <path> --json` for the deterministic
subset, then use human judgment for the rest.
