---
name: designdna
description: >
  Based on Google Stitch DESIGN.md methodology and 58 world-class brand design systems
  (Apple, Tesla, Stripe, Vercel, Linear, Airbnb, Spotify, Notion, etc.),
  this skill provides a complete framework for AI agents to generate production-grade UI
  with distinctive aesthetic quality. Covers design analysis, DESIGN.md creation,
  and pixel-perfect implementation across all frontend platforms.
version: 2.0.0
triggers:
  - design system
  - DESIGN.md
  - design token
  - design audit
  - UI audit
  - color palette
  - typography system
  - shadow system
  - design archetype
  - Stitch prototype
  - brand aesthetic
  - design resource
  - icon library selection
  - font selection
---

{% raw %}


# DesignDNA — AI Design System Skill

## ⚠ Scope Boundary Declaration — Read First

### This skill IS (owns exclusively):
- **DESIGN.md methodology** — the 9-section standard, creation, and maintenance
- **Design system architecture** — tokens, scales, semantic organization
- **Design DNA analysis** — extracting and matching to 10 archetypes from 58 brands
- **UI audit & scoring** — evaluating existing UI against 10 Universal Design Rules
- **Design resource catalog** — icons, images, illustrations, colors, fonts, animations (RESOURCES.md)
- **Design-driven tech stack advisory** — recommending component libraries that best EXPRESS a design intent
- **Consistency enforcement** — the 5 C-rules preventing color/icon/font/illustration drift
- **A2UI protocol** — for agent-driven declarative UI

### This skill IS NOT (defers to other skills):
- **NOT a frontend implementation skill** → defer to `frontend-patterns` for React/Vue/Angular patterns, state management, component architecture, performance optimization
- **NOT a project scaffolding skill** → defer to `web-development` for build config, SDK integration, static hosting, deployment
- **NOT a coding standards skill** → defer to `coding-standards` for naming conventions, file organization, type safety, error handling
- **NOT a deployment skill** → defer to `deployment-patterns` for Docker, CI/CD, cloud config
- **NOT a mini program structure skill** → defer to `miniprogram-development` for project structure, WeChat DevTools, wx.cloud
- **NOT a security skill** → defer to `security-review` for OWASP, injection prevention, auth security
- **NOT an accessibility implementation skill** → defer to `frontend-patterns` for WCAG implementation code; this skill only defines contrast/touch-target SPECIFICATIONS in DESIGN.md

### Relationship with `ui-design` skill:

The `ui-design` skill and this skill are **complementary, not competing**:

| Concern | `ui-design` owns | `designdna` owns |
|---------|-------------------|------------------------------|
| **When to trigger** | User asks to create NEW page/component/interface | User asks about design SYSTEM, tokens, DESIGN.md, audit, brand matching |
| **Aesthetic direction** | Chooses aesthetic direction (e.g. "brutalist", "editorial") | Provides reference archetypes from 58 real brands |
| **Color selection** | Creative color choices for a specific page | Semantic color ORGANIZATION (4-tier text, surface hierarchy, accent rules) |
| **Typography** | Font SELECTION for a specific aesthetic feel | Typography SYSTEM (hierarchy table, weight roles, letter-spacing formula) |
| **Output** | Beautiful individual pages/components | Reusable design system documents (DESIGN.md) |

**Collaboration rules**:
1. If `ui-design` is active and this skill is also triggered → `ui-design` leads creative decisions, this skill provides the SYSTEM STRUCTURE to organize them
2. If a DESIGN.md already exists in the project → BOTH skills must follow it; neither may override it without user approval
3. If `ui-design` picks fonts/colors → this skill organizes them into semantic tokens, hierarchy tables, and CSS variables
4. If this skill recommends an archetype → `ui-design` may refine the aesthetic within that archetype's guardrails

### Tech Stack Advisory — Design Perspective Only

This skill recommends tech stacks **from a design expression perspective**:
- "Which component library best EXPRESSES this design archetype?"
- "Which icon set best MATCHES this visual language?"

It does NOT dictate:
- Framework architecture decisions → `frontend-patterns`
- Build tool configuration → `web-development`
- State management patterns → `frontend-patterns`
- API integration patterns → `backend-patterns` / `api-design`

**When this skill's tech stack suggestion conflicts with another skill**:
→ The OTHER skill wins on implementation details.
→ This skill wins on VISUAL/DESIGN rationale only.
→ Example: This skill says "use Lucide icons for this design archetype". `frontend-patterns` says "use dynamic imports for tree-shaking". Both apply — choose Lucide (design), import dynamically (implementation).

---

> Distilled from 58 world-class brand design systems following Google Stitch's DESIGN.md methodology.
> Source: [DesignDNA-Skills](https://github.com/tiantangcao1980-web/DesignDNA-Skills) | Design data: [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## Library Sub-Skills

For **library-specific implementation guidance** (Taro, NutUI Vue, NutUI React, NutUI UniApp, NutUI Icons, NutUI Templates, NutUI Biz, Taro UI), load the matching skill from [`designdna/skills/`](./skills/).

Quick install:

```bash
# Browse available library skills
npx designdna skills list

# Install a complete stack (framework + UI + icons)
npx designdna skills install-stack taro-react      # Taro + NutUI React + Icons
npx designdna skills install-stack taro-vue        # Taro + NutUI Vue + Icons
npx designdna skills install-stack uniapp          # nutui-uniapp + Icons
npx designdna skills install-stack ai-visual       # GPT Image 2 asset workflow
npx designdna skills install-stack react           # NutUI React + Icons
npx designdna skills install-stack vue             # NutUI Vue + Icons

# Install a single skill
npx designdna skills install nutui-react
npx designdna skills install gpt-image-2
```

These sub-skills teach an AI agent the **how** (installation, component usage, theme tokens, BANNED patterns, pre-flight) for each library. Combine with the brand DNAs in `design-md/` for full "what + how" coverage.

Compatibility guardrails:
- Treat each runtime as having **one primary UI library** unless you are explicitly comparing alternatives.
- Some `install-stack` presets are **reference bundles**, not "use all of these in one app" instructions.
- For WeChat MiniProgram native UI, `vant-weapp` and `tdesign-miniprogram` are alternatives.
- For Flutter, `flutter-material` and `tdesign-flutter` are alternatives unless you have a very deliberate mixed-language design system.
- For generated visual assets, load `gpt-image-2` only when the task needs custom generation or editing; curated real assets still come first when realism/provenance matters.

See [skills/INDEX.md](./skills/INDEX.md) for the full skill catalog.

---

## Open-Source Skill Lessons

DesignDNA incorporates operational lessons from two adjacent skill projects:

- [Huashu Design](https://github.com/alchaincyf/huashu-design): fact-first workflow, core asset protocol, 5-10-2-8 asset selection, direction-advisor fallback, five-dimensional critique, visual verification.
- [Taste Skill](https://github.com/Leonxlnx/taste-skill): single-responsibility skills, dials, anti-slop bans, image-generation reference skills, image-to-code sequencing.

Use these lessons as process patterns, not vendored content. Huashu Design's public repository has a personal-use license; do not copy its assets, scripts, demos, BGM, references, or prompt text into commercial or organizational workflows without authorization. The distilled DesignDNA interpretation lives in [`OPEN-SOURCE-LEARNINGS.md`](./OPEN-SOURCE-LEARNINGS.md).

### Fact-first rule

If a task names a modern product, company, library, version, public figure, event, release, or current design system, verify current facts before making design or implementation claims. This applies especially to package versions, peer dependencies, product launch assets, official logos, product screenshots, and brand guidelines.

### Core asset protocol

For named brand/product work, recognizable assets outrank abstract vibe. Prioritize:

1. Logo
2. Product render/photo for physical products
3. UI screenshots for digital products
4. Color values
5. Fonts
6. Mood keywords

Freeze collected assets into `brand-spec.md` or equivalent notes with source URLs, capture date, local paths, resolution, and usage role. Do not substitute generic SVG silhouettes, fake screenshots, or generated lookalikes when official assets are needed.

### Image-first rule

For visual-risk website, campaign, hero, landing-page, or redesign work, use an image-first loop when generation is available and helpful:

1. Generate or collect clear references.
2. Analyze layout, type, spacing, color, imagery, and component rhythm.
3. Convert findings into DESIGN.md tokens and component rules.
4. Implement from the extracted system.

Prefer one clear section/detail reference over a compressed multi-section board. Do not crop an old generated board as the main source for a new section; generate a fresh section-specific reference if detail fidelity matters.

---

## Pre-flight Checklist (MANDATORY)

**Before emitting any UI code, self-audit with this checklist. Print each item as `[x]` (passed) or `[ ]` (failed) in your output reasoning.**

This is a bias-correction checklist inspired by [taste-skill](https://github.com/Leonxlnx/taste-skill). LLMs have strong statistical priors toward generic patterns — these rules fight the mean.

### Facts & Assets
- [ ] Current facts verified when the task names a modern product/company/library/version
- [ ] Existing DESIGN.md, brand guidelines, screenshots, UI kit, or codebase checked before inventing visuals
- [ ] For brand-specific work: logo/product/UI assets prioritized before colors/fonts
- [ ] Important non-logo hero assets pass the 5-10-2-8 gate or are explicitly marked as placeholders
- [ ] Generated images have prompt/provenance notes and are not presented as official assets

### Typography
- [ ] No Inter unless the brand DNA specifies it
- [ ] ≤ 2 font families used on the page
- [ ] ≤ 4 font weights used total
- [ ] No all-caps headings > 16px
- [ ] Font families match the brand DNA exactly

### Color
- [ ] No pure `#000000` (use warm near-black from brand DNA)
- [ ] No pure `#FFFFFF` surfaces without a brand-specific off-white alternative
- [ ] No default AI purple `#8B5CF6` family unless brand specifies purple
- [ ] No rainbow blue→purple→pink gradient
- [ ] Accent color explicitly from brand DNA palette

### Layout
- [ ] Hero is NOT the generic "centered headline + subhead + 2 buttons" template
- [ ] No 3-column icon-card feature grid
- [ ] No "Trusted by" fake-logo bar
- [ ] At least one section breaks the symmetric 12-column grid
- [ ] Vertical rhythm matches VISUAL_DENSITY dial (< 3 → breathy, > 7 → dense)

### Copy & Content
- [ ] No placeholder names: "John Doe", "Jane Smith", "Acme", "Nexus", "Velocity", "Apex"
- [ ] No fake metrics: "99.99% uptime", "10x faster", "10,000+ users"
- [ ] No AI marketing-speak: "Effortlessly", "Seamlessly", "Revolutionary"
- [ ] No emoji in headings
- [ ] Headlines follow the brand's voice guide (declarative / object-first / conversational / etc.)

### Components
- [ ] No frosted-glass `backdrop-blur` on every card
- [ ] No animated mesh gradient hero background
- [ ] No `ring-purple-500/50` glow on buttons/cards (unless brand specifies purple)
- [ ] No generic stock imagery (brain circuits, chat bubbles, glowing networks)

### Brand DNA Conformance
- [ ] Loaded brand's `DESIGN.md`
- [ ] Loaded brand's `BANNED.md` if present
- [ ] Dial values declared (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, WARMTH, CONTRAST)
- [ ] Every component references a brand token, not a hardcoded hex or px

**If any item is `[ ]`, revise before output. This checklist is not optional.**

See also: `designdna/anti-slop/SKILL.md` for the full reasoning and replacement patterns.

---

## Two-Stage Skill Model (how DesignDNA is meant to be used)

Inspired by [taste-skill's stitch-skill pattern](https://github.com/Leonxlnx/taste-skill), DesignDNA operates in two stages rather than as a single monolithic reference.

### Stage 1 — Methodology load (this file)
The AI editor loads this SKILL.md (~general methodology) once at session start. This teaches the agent:
- How to read a brand DNA directory
- How to apply the 9-section DESIGN.md standard
- How to enforce anti-slop rules and pre-flight checks
- How to pick a brand archetype for the user's project

### Stage 2 — Project artifact generation (CLI-generated)
Run `npx designdna craft --brand=<name>` from the user's project root. This generates a **`PROJECT-DESIGN.md`** file that:
- Bundles the chosen brand's DNA + BANNED patterns
- Declares the project's dial values (formality/motion/density/warmth/contrast)
- Embeds the pre-flight checklist
- Becomes the single source of truth for all future UI generations

After Stage 2, every UI prompt the user types should reference `PROJECT-DESIGN.md` rather than re-explaining the design system.

### Workflow summary

```
┌──────────────────┐      ┌─────────────────────┐      ┌────────────────────┐
│  SKILL.md        │      │  npx designdna      │      │  PROJECT-DESIGN.md │
│  (methodology)   │ ───► │  craft --brand=X    │ ───► │  (project artifact)│
│  Loaded once     │      │  Run once per proj  │      │  Read per prompt   │
└──────────────────┘      └─────────────────────┘      └────────────────────┘
                                     │
                                     ▼
                          Optionally: --blend=Y
                                     --motion=N
                                     --density=N
                                     ...dials overrides
```

### CLI craft examples

```bash
# Pure brand baseline
npx designdna craft --brand=apple --name="Acme Studio"

# Apple baseline, more motion, denser
npx designdna craft --brand=apple --motion=7 --density=5

# Blend two brands 50/50
npx designdna craft --brand=stripe --blend=vercel --name="Modern SaaS"

# 70/30 blend
npx designdna craft --brand=linear --blend=notion --blend-ratio=7:3
```

The resulting `PROJECT-DESIGN.md` is committed to the user's repo and becomes the durable design contract. When the design evolves, they edit this file — everyone (humans and AI) reads from it.

---

## What is DESIGN.md?

DESIGN.md is a concept from [Google Stitch](https://stitch.withgoogle.com/docs/design-md/overview/) — a plain-text design system document that AI agents read to generate consistent, high-quality UI. Markdown is the format LLMs read best; no Figma exports, no JSON schemas, no special tooling required.

| File | Who reads it | What it defines |
|------|-------------|-----------------|
| `AGENTS.md` | Coding agents | How to build the project |
| `DESIGN.md` | Design agents | How the project should look and feel |

---

## DESIGN.md as a Machine Contract (Stitch-skills increments)

> Adapted from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) (Apache-2.0, © Google LLC — not an official Google product). Two mechanisms that make the 9-section standard below machine-readable and drift-resistant.

**A. Parseable frontmatter contract.** Prepend a YAML frontmatter to every
DESIGN.md so other skills and `design-preflight` can read the palette without
parsing prose. The 9 markdown sections stay the human-readable truth; the
frontmatter is the machine mirror.

```yaml
---
name: Acme Console
colors:
  primary: "#294056"        # Deep Muted Teal-Navy – primary actions
  surface: "#0f1115"        # near-black canvas, not #000
  text-primary: "#e8eaed"
  accent: "#3b82f6"
---
```

Write each token as the **triplet** `Semantic Name (#hex) – functional role`
(intent over syntax). A DESIGN.md missing the `name`+`colors` frontmatter is
treated as **incomplete** by downstream design skills.

**B. Orthogonal layering for multi-surface work.** Section 9 below tells you to
bake full specs (hex/size/weight/radius) into each prompt — that is correct for
a **one-shot** surface. For **multi-page or multi-component** projects, invert
it: keep generation prompts to **layout / content / structure only**, and inject
design tokens once at the **project level** (CSS variables, theme file, Tailwind
config from the frontmatter). This keeps style orthogonal to structure so pages
do not re-describe — and silently drift — the brand on every prompt. See
`design-templates` for the cross-page consistency loop that depends on this.

## Part 1: The 9-Section DESIGN.md Standard

Every DESIGN.md MUST follow this exact 9-section architecture. This consistency enables AI agents to parse and implement any design system predictably.

### Section 1: Visual Theme & Atmosphere
**Purpose**: Establish the emotional and philosophical foundation of the design.

**Requirements**:
- 150-300 words of narrative prose, NOT bullet points
- Describe the emotional quality (warm, clinical, cinematic, editorial, etc.)
- Articulate design density (airy vs. data-dense)
- State the core design philosophy in one sentence
- Use sensory/spatial metaphors (e.g., "theater-like darkness", "Swiss watch precision", "parchment warmth")

**Patterns from world-class brands**:
- **Vercel**: "Precision-engineered monochrome" — black/white purity, Geist typeface authority
- **Stripe**: "Whisper-weight elegance" — weight-300 lightness, blue-tinted depth
- **Airbnb**: "Photography-driven warmth" — coral accent, warm near-black (#222222, not #000)
- **Linear**: "Precision in darkness" — dark-mode-native, semi-transparent white layers
- **Tesla**: "Radical subtraction" — zero shadows, single accent color, photography carries emotion
- **Claude**: "Editorial warmth" — parchment canvas, serif/sans split, magazine-like pacing
- **Spotify**: "Content-first darkness" — UI recedes, album art is the primary color source
- **Notion**: "Quality paper, not sterile glass" — warm neutrals, whisper borders
- **Figma**: "White gallery wall displaying colorful art" — monochrome chrome + vibrant showcases
- **Framer**: "Nightclub for web designers" — cinematic dark canvas, extreme letter-spacing compression

### Section 2: Color Palette & Roles
**Purpose**: Define every color with its semantic purpose.

**Organization** (NEVER use a flat list — always group by semantic purpose):

```
### Primary & Brand
- **Brand Color** (`#hexcode`): CSS variable name, semantic purpose and usage

### Secondary & Accent
- Variant 1: description
- Variant 2: description

### Text Scale (3-5 tiers)
- Primary text: color + when to use
- Secondary text: color + when to use
- Tertiary text: color + when to use
- Quaternary/Disabled: color + when to use

### Surface & Background (2-6 variants)
- Base background
- Elevated surface
- Overlay surface

### Interactive States
- Default, Hover, Focus, Active, Disabled

### Borders & Dividers
- Primary border, subtle border, focus ring

### Semantic
- Error, Success, Warning, Info

### Shadows
- Shadow colors with opacity values
```

**Key patterns from top brands**:
- **Always include hex code + semantic name + use case** in every color entry
- **Warm neutrals outperform cold grays**: Airbnb uses #222222 (warm near-black), Claude uses #5e5d59 (olive gray), Notion uses rgba(0,0,0,0.95) — NOT pure #000000
- **Brand accent restraint**: Tesla uses ONE accent color (#3E6AE1). Spotify reserves green ONLY for play/active. Coinbase uses blue only for primary CTAs
- **Dark mode colors**: Linear uses semi-transparent whites for borders (rgba(255,255,255,0.05-0.08)). Raycast uses double-ring containment technique

### Section 3: Typography Rules
**Purpose**: Define the complete type system.

**Required structure**:

1. **Font Families** — Primary, secondary, monospace with fallback stacks
2. **Hierarchy Table** (Markdown table format):

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|------|--------|-------------|----------------|-------|
| Display Hero | ... | ...px | ... | ... | ...px | ... |
| Section Heading | ... | ... | ... | ... | ... | ... |
| Body | ... | ... | ... | ... | ... | ... |

3. **Typography Principles** — Weight philosophy, spacing rules, OpenType features

**Key patterns from top brands**:

**Weight Systems** (no brand uses more than 4 weights):
- **2-weight systems**: Tesla (400/500), Claude (400/500) — hierarchy through serif/sans split or size alone
- **3-weight systems**: Vercel (400/500/600), Stripe (300/400/500) — strict role assignment per weight
- **Micro-weight systems**: Linear (300/400/510/590), Figma (320-540 variable) — precision through interpolation

**Letter-Spacing Rules**:
- **Negative at large sizes**: Universal rule. Vercel: -2.4px at 64px. Framer: -5.5px at 110px. Notion: -2.125px at 64px
- **Zero or positive at body**: Most systems use 0px at 14-16px body text
- **Positive at small sizes**: Raycast uses +0.2px to +0.4px for airy readability in dark UIs
- **Formula**: letter-spacing = -(fontSize * 0.03 to 0.05) for headlines; 0 for body; +(0.01 to 0.02) for captions

**OpenType Features** (frequently required):
- Stripe: `"ss01"` stylistic set required on ALL text
- Linear: `"cv01", "ss03"` on Inter — character variant + stylistic set
- Figma: `kern` enabled globally
- Raycast: `"calt", "kern", "liga", "ss03"` on Inter
- Notion: NotionInter with custom rendering

### Section 4: Component Stylings
**Purpose**: Define visual specifications for all major UI elements.

**Required components** (minimum):
1. **Buttons** — Primary, Secondary, Ghost/Text variants with all states
2. **Cards & Containers** — Standard, Elevated, Featured variants
3. **Input Fields** — Text input, Select, Textarea with focus states
4. **Navigation** — Header, sidebar, tabs, breadcrumbs
5. **Images & Media** — Aspect ratios, border radius, overlay treatment
6. **Distinctive Components** — Brand-specific unique elements

**Format for each component**:
```
### Component Name

**Variant Name (Context)**
- Background: color value
- Text/Color: value
- Padding: value (often asymmetric)
- Radius: value
- Border/Shadow: CSS value
- Hover: state change description
- Focus: state change description
- Use: explicit use case
```

**Key patterns from top brands**:

**Button Philosophies**:
- **Vercel**: Shadow-as-border technique (ring shadow instead of border property)
- **Stripe**: Blue-tinted shadows for chromatic depth
- **Spotify**: Pill-and-circle geometry (9999px radius), uppercase + wide letter-spacing
- **Linear**: Near-transparent backgrounds (rgba(255,255,255,0.02-0.05))
- **Framer**: Frosted pill with inset shadow + scale transform on hover
- **Raycast**: Opacity transition for hover (NOT background-color change)
- **Tesla**: Zero decoration — single blue CTA, everything else is ghost

**Card Patterns**:
- **Notion**: 4-5 layer shadow stacks with cumulative opacity never exceeding 0.05
- **Airbnb**: Three-layer graduated shadows (0.02 + 0.04 + 0.1 opacity) for "warm lift"
- **Framer**: Blue ring shadow border (`rgba(0,153,255,0.15) 0px 0px 0px 1px`)
- **Raycast**: Double-ring technique (outer + inset borders)
- **Claude**: Ring shadows (`0px 0px 0px 1px`) + whisper drops

### Section 5: Layout Principles
**Purpose**: Define spacing, grid, and spatial relationships.

**Required subsections**:
1. **Spacing Scale** — Base unit + full scale table
2. **Grid System** — Column count, gutter, max-width
3. **Whitespace Philosophy** — How space is used as a design element
4. **Border Radius Scale** — Named variants from sharp to pill

**Universal rule**: ALL world-class design systems use **8px as the base unit**.

**Border Radius Scale** (universal pattern — 8 named variants):
| Name | Value | Use |
|------|-------|-----|
| None/Sharp | 0px | Inline tags, dividers |
| Micro | 2px | Small interactive elements |
| Subtle | 4px | Buttons, inputs, small containers |
| Standard | 6-8px | Cards, standard containers |
| Comfortable | 12px | Featured cards, panels |
| Relaxed | 16-20px | Large containers, media |
| Pill | 9999px | Badges, tags, status pills |
| Circle | 50% | Avatars, icon buttons |

### Section 6: Depth & Elevation
**Purpose**: Define how visual layers are communicated.

**Required**: Level table (0 to 3-5 levels) with shadow CSS values and use cases.

**Key shadow philosophies from top brands**:
- **Multi-layer architectural** (Vercel): border + elevation + ambient + inner — each layer serves a distinct purpose
- **Chromatic-tinted** (Stripe): `rgba(50,50,93,0.25)` — shadows carry brand color
- **Warm graduated** (Airbnb): Progressive opacity (0.02 → 0.04 → 0.1) for natural lift
- **Inverted/dark** (Linear): Semi-transparent white borders + inset shadows on dark surfaces
- **Zero shadows** (Tesla): Elevation through z-index, opacity, and photography only
- **Ring-based** (Claude): `0px 0px 0px 1px` ring shadows + whisper ambient drops
- **Multi-ring containment** (Raycast): Outer ring + inset ring + ambient glow

### Section 7: Do's and Don'ts
**Purpose**: Explicit guardrails preventing design drift.

**Format**:
```
### Do
- Use [specific pattern] because [reason]
- Always [required behavior]

### Don't
- Don't use [anti-pattern] because [consequence]
- Never [forbidden behavior]
```

**Minimum 10 rules total** (5 Do + 5 Don't).

**Common patterns across all brands**:
- DO maintain weight restraint (max 3-4 weights)
- DO use brand accent color sparingly (one purpose, not decoration)
- DO include OpenType features when specified
- DO use warm neutrals over cold grays (unless brand dictates otherwise)
- DON'T use pure black (#000000) for text on light backgrounds
- DON'T skip letter-spacing adjustments at different sizes
- DON'T use light/thin weights on dark backgrounds (readability)
- DON'T apply brand colors decoratively (reserve for semantic purposes)
- DON'T use uniform shadow opacity across all elevation levels

### Section 8: Responsive Behavior
**Purpose**: Define how the design adapts across screen sizes.

**Required subsections**:
1. **Breakpoints** — Table with name, pixel width, key layout changes
2. **Touch Targets** — Minimum tap sizes (typically 44x44px minimum)
3. **Collapsing Strategy** — How multi-column layouts simplify
4. **Image Behavior** — How media scales and crops

### Section 9: Agent Prompt Guide
**Purpose**: Enable AI agents to generate brand-matching designs immediately.

**Required subsections**:
1. **Quick Color Reference** — 5-15 most-used colors with hex codes and roles
2. **Example Component Prompts** — 3-5 full natural-language component descriptions with ALL specifications (hex codes, sizes, weights, radii, shadows)
3. **Iteration Tips** — 4-8 practical tips emphasizing brand-critical choices

**Prompt format example**:
> "Create a dark card: #181818 background, 8px radius. Title at 16px weight 700, white text. Subtitle at 14px weight 400, #b3b3b3. Shadow rgba(0,0,0,0.3) 0px 8px 8px on hover."

---

## Part 2: Design Analysis Framework

When analyzing a website to create a DESIGN.md or when generating new UI, follow this systematic approach:

### Step 1: Identify the Design Archetype

Classify the design into one of these proven archetypes (from 58 brand analysis):

| Archetype | Characteristics | Example Brands |
|-----------|----------------|----------------|
| **Precision Monochrome** | Black/white purity, tight type, engineering feel | Vercel, HashiCorp, SpaceX |
| **Warm Editorial** | Parchment tones, serif/sans split, magazine pacing | Claude, Notion, Airbnb |
| **Dark Cinematic** | Deep blacks, single accent, photography-dominant | Tesla, SpaceX, RunwayML |
| **Vibrant Gradient** | Bold color transitions, light weights, data-rich | Stripe, Cohere, Figma |
| **Dark Instrument** | Void-black, multi-ring containment, tool-like precision | Linear, Raycast, Warp, Cursor |
| **Content Stage** | UI recedes, content is hero, pill geometry | Spotify, ElevenLabs, Pinterest |
| **Friendly Warm** | Bright accents, rounded corners, illustration-driven | Zapier, Lovable, Miro |
| **Premium Automotive** | Full-viewport imagery, extreme minimalism, custom type | BMW, Ferrari, Lamborghini, Renault |
| **Enterprise Trust** | Structured grids, blue palettes, data density | IBM, Coinbase, MongoDB |
| **Developer Native** | Monospace accents, code-forward, terminal aesthetic | Supabase, Resend, Expo, Warp |

### Step 2: Extract Design DNA

For each design, identify these 7 DNA markers:

1. **Signature Color Move** — What's the ONE color decision that makes this brand recognizable?
   - Stripe: purple gradients (#533afd)
   - Spotify: green ONLY for play (#1ed760)
   - Airbnb: Rausch Red (#ff385c) as sole accent

2. **Typography Signature** — What's the ONE type decision that defines the brand?
   - Stripe: weight 300 ("whisper-weight authority")
   - Linear: weight 510 (between regular and medium)
   - Framer: -5.5px letter-spacing at 110px (extreme compression)
   - Figma: variable weight 320-540 (never standard 400/500/600)

3. **Depth Philosophy** — How does the brand communicate layers?
   - Shadow-heavy (Vercel), shadow-free (Tesla), ring-based (Claude), chromatic (Stripe)

4. **Geometry DNA** — What shapes dominate?
   - Pill/circle (Spotify), sharp rectangles (Vercel), soft rounds (Airbnb), mixed (Linear)

5. **Temperature** — Warm or cool neutrals?
   - Warm: Claude, Notion, Airbnb (yellow-brown undertones in grays)
   - Cool: Vercel, Linear, IBM (blue-gray undertones)
   - Neutral: Tesla, SpaceX (true grays)

6. **Density** — How much content per viewport?
   - Sparse: Tesla, Apple, SpaceX (one message per screen)
   - Medium: Vercel, Stripe, Notion (balanced information)
   - Dense: Linear, Sentry, PostHog (data-rich dashboards)

7. **Motion Signature** — What's the characteristic animation?
   - Tesla: 0.33s cubic-bezier universal timing
   - Framer: scale(0.85) transform on buttons
   - Raycast: opacity transitions (never background-color changes)

### Step 3: Generate the DESIGN.md

Follow the 9-section structure exactly. Quality checklist:

- [ ] Section 1: 200+ words of philosophical narrative (NOT bullet points)
- [ ] Section 2: 15+ colors organized by semantic purpose (NOT a flat list)
- [ ] Section 3: 10+ typography roles in table format with all 6 columns
- [ ] Section 4: 4+ component categories with variant specifications
- [ ] Section 5: 8px base unit, full spacing scale, border radius table
- [ ] Section 6: 3+ elevation levels with exact CSS shadow values
- [ ] Section 7: 10+ Do/Don't rules with reasons
- [ ] Section 8: Breakpoint table, touch targets, collapsing strategy
- [ ] Section 9: Quick color reference + 3+ example prompts + iteration tips

---

## Part 3: Implementation Guidelines

When implementing UI from a DESIGN.md or generating new interfaces:

### Color Implementation Rules

1. **Never use pure black for text on light backgrounds** — Use warm near-black (#222222, rgba(0,0,0,0.95), or #1a1a1a)
2. **Organize CSS variables by semantic purpose**, not alphabetically:
   ```css
   /* Surface */
   --bg-primary: #ffffff;
   --bg-elevated: #fafafa;
   /* Text */
   --text-primary: #222222;
   --text-secondary: #666666;
   /* Brand */
   --accent: #ff385c;
   ```
3. **Reserve brand accent colors for semantic purposes** — CTAs, active states, links. Never decorative.
4. **Dark mode is not color inversion** — It's a separate palette with luminance-stacking (Linear model: background opacity steps)

### Typography Implementation Rules

1. **Letter-spacing MUST scale with font size**:
   - Display (48px+): negative (-0.03em to -0.05em)
   - Heading (24-48px): slightly negative (-0.01em to -0.02em)
   - Body (14-18px): 0 or normal
   - Caption (10-13px): slightly positive (+0.01em to +0.02em)

2. **Weight assignments must be strict** — each weight has ONE semantic purpose:
   - 300: De-emphasis, secondary information (Stripe model)
   - 400: Body text, reading content
   - 500: UI labels, interactive elements, emphasis
   - 600: Headings, section titles
   - 700: Display, hero statements

3. **Always specify OpenType features** when the design system requires them

4. **Line-height compression at scale**:
   - Display: 0.85-1.0
   - Heading: 1.0-1.2
   - Body: 1.4-1.6
   - Caption: 1.3-1.5

### Shadow Implementation Rules

1. **Multi-layer shadows are superior to single-layer** — Use 2-4 layers for natural depth
2. **Shadow opacity should never exceed 0.3** on any single layer (Notion rule: cumulative max 0.05)
3. **Match shadow temperature to the design**:
   - Warm designs: shadows with brown/yellow tint
   - Cool designs: shadows with blue tint (Stripe: `rgba(50,50,93,0.25)`)
   - Neutral: pure black at low opacity
4. **Ring shadows for containment** — `0px 0px 0px 1px rgba(...)` replaces border for cleaner rendering

### Component Implementation Rules

1. **Buttons**: Max 3 variants (primary, secondary, ghost). States: default, hover, focus, active, disabled
2. **Cards**: Always use multi-layer shadows. Hover state should enhance, not transform
3. **Inputs**: Focus state must be visually distinct (ring, glow, or color shift)
4. **Navigation**: Active state through weight or background change, not color alone

---

## Part 4: Design Quality Anti-Patterns

### Forbidden Patterns (from 58-brand analysis)

These patterns were ABSENT from all 58 world-class design systems:

1. **Generic AI aesthetic** — Default gradient backgrounds, centered layouts, stock imagery
2. **Rainbow color palettes** — More than 3 accent colors competing for attention
3. **Uniform border-radius** — Same radius on every element regardless of size
4. **Single-layer shadows** — `box-shadow: 0 2px 4px rgba(0,0,0,0.1)` alone
5. **Pure black text** (#000000) on white backgrounds
6. **Uniform letter-spacing** — Same tracking at all font sizes
7. **More than 4 font weights** — Weight proliferation dilutes hierarchy
8. **Decorative use of brand colors** — Brand color on borders, backgrounds, dividers
9. **Template-centered layouts** — Everything centered, symmetrical, predictable
10. **Thin/light fonts on dark backgrounds** — Below weight 400 on dark surfaces

### Quality Signals (present in ALL top brands)

1. Negative letter-spacing on headlines (every single one of 58 brands)
2. Multi-layer shadow systems (or deliberate zero-shadow philosophy)
3. Semantic color organization (never a flat color list)
4. Typography hierarchy with 8+ distinct roles
5. Explicit Do's and Don'ts preventing drift
6. Warm neutrals (even "cool" brands avoid pure gray)
7. 8px spacing base unit (universal)
8. Consistent border-radius scale (8 named variants)
9. Brand accent used for ONE primary purpose
10. Component states fully specified (hover, focus, active, disabled)

---

## Part 5: Quick Reference Card

### When starting any UI design task:

1. **Check for existing DESIGN.md** in the project root
2. **If exists**: Read it completely, follow it exactly
3. **If not exists**: Ask the user which brand aesthetic to follow, or identify the closest archetype
4. **Generate DESIGN.md first** before writing any UI code (unless user has existing pages to patch)

### The 10 Universal Design Rules (from 58 brands):

1. Use 8px as base spacing unit
2. Limit to 2-4 font weights maximum
3. Scale letter-spacing inversely with font size
4. Organize colors by semantic purpose
5. Use multi-layer shadows (or deliberately zero)
6. Reserve brand accent for ONE semantic purpose
7. Use warm near-black for text, never pure #000000
8. Define 8 border-radius variants from sharp to pill
9. Every component needs 4 states: default, hover, focus, disabled
10. Write Do's and Don'ts to prevent design drift

---

## References

Heavy domain detail is split out under `references/` (progressive disclosure) and
loaded only when the task needs it:

- [Existing-project audit, prototype workflow & usage scenarios](references/existing-project-and-prototype.md) — Parts 6–8
- [Resource integration & tech-stack catalog](references/resource-and-tech-stack.md) — Parts 9–10
- [Design-to-dev workflow, advanced integration & motion design](references/design-to-dev-and-motion.md) — Parts 11–12A
- [Specialized UI domains — 3D, maps, search, knowledge graph, mini-program](references/specialized-ui-domains.md) — Parts 12B–12J
- [Standalone essentials, compliance & evolution protocols](references/compliance-and-evolution.md) — Parts 13–15

{% endraw %}
