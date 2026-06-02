# DesignDNA References · Existing-Project Audit, Prototype & Usage Scenarios (Parts 6–8)

> Loaded on demand from the `designdna` skill. See [SKILL.md](../SKILL.md) for the operating core.

{% raw %}

## Part 6: Existing Project UI Audit & Optimization

When the user wants to optimize or upgrade the UI of an existing project, follow this systematic workflow.

### Workflow Overview

```
Existing Project
  ├─ Step 1: Extract current design DNA (read code + screenshots)
  ├─ Step 2: Audit against 10 Universal Rules (identify violations)
  ├─ Step 3: Generate improvement DESIGN.md (target state)
  ├─ Step 4: Prioritized refactoring plan (high-impact first)
  └─ Step 5: Incremental implementation (one system at a time)
```

### Step 1: Extract Current Design DNA

Read the project's existing CSS/styles and identify the current state:

**What to extract**:
```
1. Colors currently in use:
   - grep/search for hex codes (#xxx, #xxxxxx), rgb(), rgba(), hsl()
   - List all unique colors, group by apparent purpose
   - Check: are they organized by semantic purpose? or random?

2. Typography currently in use:
   - font-family declarations (how many fonts?)
   - font-weight values (how many weights? which ones?)
   - font-size values (how many distinct sizes?)
   - letter-spacing values (are they scaling with size?)
   - line-height values (are they compressing at larger sizes?)

3. Spacing patterns:
   - padding/margin values (are they on 8px grid?)
   - gap values
   - Any evidence of a spacing scale?

4. Shadow system:
   - box-shadow declarations (single-layer or multi-layer?)
   - shadow colors (warm, cool, or pure black?)
   - how many distinct shadow levels?

5. Border radius:
   - border-radius values (how many unique values?)
   - are they systematic or random?

6. Component patterns:
   - Button variants and their states
   - Card patterns
   - Input styles
   - Navigation treatment
```

**Commands to run** (adjust for the project's tech stack):
```bash
# Find all color values
grep -rn '#[0-9a-fA-F]\{3,8\}' src/ --include="*.css" --include="*.scss" --include="*.tsx" --include="*.vue"

# Find all font-weight values
grep -rn 'font-weight' src/ --include="*.css" --include="*.scss"

# Find all box-shadow values
grep -rn 'box-shadow' src/ --include="*.css" --include="*.scss"

# Find all border-radius values
grep -rn 'border-radius' src/ --include="*.css" --include="*.scss"

# Find all font-size values
grep -rn 'font-size' src/ --include="*.css" --include="*.scss"
```

### Step 2: Audit Against 10 Universal Rules

Score each rule as PASS / PARTIAL / FAIL:

| # | Rule | Check | Common Violations |
|---|------|-------|-------------------|
| 1 | 8px base spacing | Are padding/margin/gap on 8px grid? | Random values like 13px, 17px, 25px |
| 2 | Max 4 font weights | Count distinct font-weight values | 5+ weights scattered without purpose |
| 3 | Letter-spacing scales | Negative at display, zero at body? | Uniform 0px or uniform -1px everywhere |
| 4 | Semantic color organization | Colors grouped by purpose in variables? | Flat list, or colors defined inline |
| 5 | Multi-layer shadows | 2+ shadow layers per elevation? | Single `0 2px 4px rgba(0,0,0,0.1)` everywhere |
| 6 | Brand accent restraint | Brand color used for ONE purpose? | Brand color on borders, backgrounds, dividers |
| 7 | Warm near-black text | Text color is warm, not #000? | Pure #000000 on white backgrounds |
| 8 | Border-radius scale | Systematic radius variants? | Random values or same radius everywhere |
| 9 | 4 component states | hover/focus/disabled defined? | Missing focus states, no disabled styles |
| 10 | Do's/Don'ts exist | Any design guardrails documented? | No documentation, inconsistent patterns |

### Step 3: Generate Improvement DESIGN.md

Based on the audit, generate a DESIGN.md that:
1. **Preserves** what's already working well (don't break what's good)
2. **Fixes** rule violations with specific improvements
3. **Elevates** the design toward the closest world-class archetype

**Output format for the user**:
```markdown
## UI Audit Report

### Current State
- Design archetype: closest to [archetype]
- Overall score: X/10 rules passing

### Critical Issues (fix first)
1. [Violation]: [current state] → [target state]
2. ...

### Enhancement Opportunities
1. [Improvement]: [why] → [how]
2. ...

### Generated DESIGN.md
[Full 9-section DESIGN.md targeting the improved state]
```

### Step 4: Prioritized Refactoring Plan

Always refactor in this order (highest visual impact → lowest risk):

**Phase 1 — Color System (biggest visual impact, lowest risk)**
- Extract all colors into CSS custom properties
- Reorganize by semantic purpose
- Replace pure #000 with warm near-black
- Establish text hierarchy (4 tiers)

**Phase 2 — Typography (high impact, low risk)**
- Consolidate to 2-4 weights with strict roles
- Add negative letter-spacing to headlines
- Fix line-height compression at scale
- Add OpenType features if applicable

**Phase 3 — Shadow & Depth (medium impact, low risk)**
- Replace single-layer shadows with multi-layer
- Choose a shadow philosophy (warm/ring/chromatic)
- Create elevation scale (3-5 levels)

**Phase 4 — Spacing & Layout (medium impact, medium risk)**
- Align all values to 8px grid
- Create spacing scale tokens
- Normalize border-radius to 8-variant scale

**Phase 5 — Component States (lower visual impact, higher completeness)**
- Add missing hover states
- Add focus rings for keyboard navigation
- Add disabled state styles
- Ensure 44px minimum touch targets

### Step 5: Incremental Implementation

**Key principle**: Implement ONE system at a time. Never mix phases.

For each phase:
1. Create the new design tokens (CSS variables / theme config)
2. Find-and-replace old values → new tokens
3. Visual regression check (screenshot before/after)
4. Commit the phase as a single atomic change

**Example — Phase 1 Color Refactoring**:
```css
/* BEFORE: scattered, flat, pure black */
.title { color: #000; }
.subtitle { color: gray; }
.card { background: white; border: 1px solid #ddd; }

/* AFTER: semantic, warm, organized */
:root {
  --text-primary: #222222;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  --bg-primary: #ffffff;
  --bg-elevated: #fafafa;
  --border-primary: rgba(0,0,0,0.08);
  --border-subtle: rgba(0,0,0,0.04);
}
.title { color: var(--text-primary); }
.subtitle { color: var(--text-secondary); }
.card { background: var(--bg-elevated); border: 1px solid var(--border-primary); }
```

---

## Part 7: Stitch Prototype → Full Project Workflow

When the user has generated prototypes with Google Stitch (or any tool that produces HTML/images), follow this workflow to extract the design system and build the complete project.

### Workflow Overview

```
Stitch Output (HTML + Images)
  ├─ Step 1: Analyze prototype files (read HTML/CSS, view images)
  ├─ Step 2: Extract design tokens (colors, type, spacing, shadows)
  ├─ Step 3: Identify the design archetype (match to 58-brand patterns)
  ├─ Step 4: Generate complete DESIGN.md (fill gaps from archetype)
  ├─ Step 5: Build component library (from prototype patterns)
  ├─ Step 6: Implement full pages (using DESIGN.md + components)
  └─ Step 7: Responsive & production polish
```

### Step 1: Analyze Prototype Files

**For HTML files**:
```
1. Read ALL HTML files the user provides
2. Extract inline styles and <style> blocks
3. Identify linked stylesheets
4. List all unique CSS property values:
   - colors (hex, rgb, rgba, hsl)
   - font-family, font-size, font-weight, letter-spacing, line-height
   - padding, margin, gap (spacing values)
   - border-radius values
   - box-shadow values
   - background (gradients, images)
   - border values
5. Identify component patterns (buttons, cards, inputs, nav)
6. Note layout approach (flexbox, grid, float)
```

**For image files** (screenshots, mockups):
```
1. View the image to understand overall aesthetic direction
2. Note the dominant colors, typography style, spacing density
3. Identify the layout grid and spatial rhythm
4. Identify components visible in the mockup
5. Assess the emotional quality (warm, clinical, cinematic, etc.)
```

### Step 2: Extract Design Tokens

Create a structured extraction from the prototype:

```markdown
## Extracted Tokens from Prototype

### Colors Found
| Hex/Value | Where Used | Suggested Role |
|-----------|-----------|----------------|
| #______ | hero background | bg-primary |
| #______ | heading text | text-primary |
| #______ | CTA button | brand-accent |
| ... | ... | ... |

### Typography Found
| Element | Font | Size | Weight | Line Height | Letter Spacing |
|---------|------|------|--------|-------------|----------------|
| h1 | ... | ...px | ... | ... | ... |
| body | ... | ...px | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

### Spacing Values Found
[list all padding/margin/gap values]

### Shadow Values Found
[list all box-shadow declarations]

### Border Radius Found
[list all border-radius values]

### Components Identified
[list buttons, cards, inputs, nav patterns found]
```

### Step 3: Identify Design Archetype

Compare the extracted tokens against the 10 archetypes:

**Matching heuristics**:
- Dark background + ring shadows + monospace → **Dark Instrument** (Linear/Raycast)
- White background + strict black/white + geometric type → **Precision Monochrome** (Vercel)
- Warm tones + serif headings + photography → **Warm Editorial** (Airbnb/Claude)
- Purple/blue gradients + light weights + data tables → **Enterprise Trust** (Stripe)
- Vivid multi-color + variable fonts + playful → **Vibrant Gradient** (Figma)
- Dark + content-first + pill shapes → **Content Stage** (Spotify)
- Bright accent + rounded + illustrations → **Friendly Warm** (Zapier)
- Full-viewport images + minimal UI + custom type → **Premium Automotive** (Tesla)

### Step 4: Generate Complete DESIGN.md

The prototype likely only covers PART of the design system. Fill the gaps:

**From prototype** (use actual extracted values):
- Section 2: Color Palette — use the extracted colors, organize semantically
- Section 3: Typography — use the extracted type specs
- Section 4: Component Stylings — codify the prototype's component patterns

**Fill from archetype** (use the matched archetype's patterns):
- Section 1: Visual Theme — write narrative based on prototype's aesthetic
- Section 5: Layout Principles — align extracted spacing to 8px grid, create scale
- Section 6: Depth & Elevation — systemize shadows found, or create from archetype
- Section 7: Do's and Don'ts — derive from prototype decisions + archetype rules
- Section 8: Responsive Behavior — create breakpoints matching prototype layout
- Section 9: Agent Prompt Guide — write prompts using actual extracted values

**Gap-filling rules**:
- If prototype has 5 colors → expand to 15+ using archetype's pattern
- If prototype has 3 type sizes → expand to 10+ role hierarchy
- If prototype has no shadows → add the archetype's shadow system
- If prototype has no focus states → add from archetype
- If spacing is not on 8px grid → snap to nearest 8px multiple
- If only light mode → create dark mode palette following archetype

### Step 5: Build Component Library

Extract reusable components from the prototype:

```
1. Identify ALL unique components in the prototype HTML
2. For each component, create a reusable version:
   - Use DESIGN.md tokens (CSS variables, not hardcoded values)
   - Add ALL 4 states (default, hover, focus, disabled)
   - Make responsive (test at mobile/tablet/desktop)
   - Add proper semantic HTML + accessibility attributes

3. Component hierarchy (build in this order):
   Level 1 — Atoms: Button, Input, Badge, Avatar, Icon
   Level 2 — Molecules: Card, Form Group, Nav Item, List Item
   Level 3 — Organisms: Navigation, Hero, Feature Section, Footer
   Level 4 — Templates: Full page layouts
```

### Step 6: Implement Full Pages

With the DESIGN.md + component library ready:

```
1. Create page layouts matching prototype structure
2. Use components from the library (never inline styles)
3. Populate with real content (not Lorem ipsum for final)
4. Check every element against DESIGN.md specifications
5. Verify: colors ✓, type ✓, spacing ✓, shadows ✓, radius ✓, states ✓
```

### Step 7: Production Polish

Final quality gate:

```
□ All colors use CSS variables from DESIGN.md
□ Typography follows the hierarchy table exactly
□ All spacing on 8px grid
□ All shadows match the elevation system
□ All interactive elements have 4 states
□ Responsive at all breakpoints (320px → 1920px)
□ Touch targets ≥ 44px on mobile
□ Contrast ratios meet WCAG AA (4.5:1 body, 3:1 large)
□ Focus rings visible for keyboard navigation
□ No pure #000000 text on light backgrounds
□ Brand accent used for ONE purpose only
□ Design matches prototype intent (screenshot comparison)
```

---

## Part 8: Practical Usage Scenarios

### Scenario A: "Optimize my existing project's UI"

**What to say to AI**:
> "Read my project's CSS/styles and run a UI audit against the DesignDNA rules. Show me what violations exist and create a phased improvement plan."

**What happens**:
1. AI reads your styles (CSS/SCSS/Tailwind config/styled-components)
2. Scores against 10 Universal Rules
3. Identifies closest archetype
4. Generates improvement DESIGN.md
5. Provides Phase 1-5 refactoring plan
6. Implements changes incrementally

### Scenario B: "I have Stitch prototypes, build the full project"

**What to say to AI**:
> "I have HTML prototypes from Google Stitch in [directory]. Extract the design tokens, generate a complete DESIGN.md, then build the full project using [React/Vue/etc.]."

**What happens**:
1. AI reads your prototype HTML files (and views any images)
2. Extracts all design tokens (colors, type, spacing, shadows)
3. Identifies the closest design archetype
4. Generates complete DESIGN.md (filling gaps from archetype)
5. Builds component library using extracted tokens
6. Implements full pages matching prototype layout
7. Adds responsive behavior + production polish

### Scenario C: "Make my UI look like [brand]"

**What to say to AI**:
> "Redesign my project's UI to match the [Stripe/Linear/Notion/etc.] aesthetic. Use the awesome-design-md reference for [brand]."

**What happens**:
1. AI reads the reference brand's DESIGN.md from awesome-design-md collection
2. Audits your current UI against that brand's design system
3. Generates a project-specific DESIGN.md adapting the brand's patterns
4. Implements the redesign following the phased plan

### Scenario D: "Generate a DESIGN.md for my project"

**What to say to AI**:
> "Analyze my project and generate a DESIGN.md. My project is a [type] and I want the aesthetic to feel [description]."

**What happens**:
1. AI identifies the closest archetype
2. Reads your existing code for any design patterns already in place
3. Generates a complete 9-section DESIGN.md
4. Provides example component prompts tuned to your project

### Scenario E: "Review my UI quality"

**What to say to AI**:
> "Review my project's UI against production design standards. Score it and tell me what to fix first."

**What happens**:
1. AI extracts current design DNA from your code
2. Scores each of the 10 Universal Rules
3. Compares against world-class brand patterns
4. Provides prioritized fix list with specific CSS changes

---

### Archetype Quick Selector:

| If the project is... | Use archetype | Reference brands |
|----------------------|---------------|-----------------|
| Developer tool / CLI | Dark Instrument | Linear, Raycast, Warp |
| SaaS / Productivity | Precision Monochrome | Vercel, HashiCorp |
| Consumer / Marketplace | Warm Editorial | Airbnb, Notion |
| Fintech / Data | Enterprise Trust + Gradient | Stripe, Coinbase |
| AI / ML product | Warm Editorial or Dark Cinematic | Claude, xAI |
| Creative tool | Vibrant Gradient | Figma, Framer |
| Media / Content | Content Stage | Spotify, Pinterest |
| Automotive / Luxury | Premium Automotive | Tesla, BMW, Ferrari |
| E-commerce | Friendly Warm | Zapier, Lovable |
| Backend / Infra | Developer Native | Supabase, Resend |

---


{% endraw %}
