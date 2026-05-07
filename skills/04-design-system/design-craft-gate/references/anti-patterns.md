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
| `low-contrast` | Muted text on light or colored surfaces can fail accessibility | contrast-checked foreground tokens |
| `skipped-heading` | Assistive tech and scanning users lose document structure | sequential heading levels |
| `flat-type-hierarchy` | Repeated type sizes make sections feel undifferentiated | distinct heading scale, weight, or spacing |
| `line-length` | Long prose lines slow reading and reduce comprehension | constrain prose to roughly 65-75 characters |
| `tight-leading` | Dense line height damages readability | comfortable leading for body and compact leading only for display |
| `wide-tracking` | Letter-spaced readable text feels generic and slows scanning | weight, spacing, and semantic labels |
| `all-caps-body` | All-caps body/action copy adds friction | normal case except short metadata labels |
| `justified-text` | Uneven word spacing reduces scan speed | left/start-aligned ragged text |
| `cramped-padding` | Small touch/reading space feels brittle | tokenized padding sized for input and scanning |
| `monotonous-spacing` | Repeated p-4/gap-4 everywhere flattens hierarchy | spacing scale driven by content importance |
| `everything-centered` | Full-page centering is often a prototype default | task-oriented alignment and readable flow |
| `hero-eyebrow-chip` | Decorative pills often hide weak information architecture | real status, category, or navigation affordance |
| `icon-tile-stack` | Oversized icon tiles become filler instead of affordances | icons tied to actions, states, or entities |
| `dark-glow` | Heavy shadows/glows create noisy contrast and dated polish | elevation tokens, borders, or local contrast |
| `border-accent-on-rounded` | Repeated side accents on cards create sameness | semantic status, row grouping, or priority hierarchy |
| `italic-serif-display` | Editorial type contrast can fight product utility | only use when brand voice requires it |
| `single-font` | Generic one-font systems often lack voice and hierarchy | documented type choice or deliberate type pairing |

## Manual Critique Prompts

- What decision does this visual choice help the user make?
- Does this surface reveal real product state or hide behind decoration?
- Is the layout optimized for repeated use or only first impression?
- Are cards used for objects, or are they compensating for weak hierarchy?
- Would the design still work if all gradients were removed?
- Does motion clarify cause/effect, or merely signal "made by AI"?

Use `bin/super-skill design-preflight --project <path> --json` before mutation
and `bin/super-skill design-audit --project <path> --json` for the deterministic
subset, then use human judgment for the rest.
