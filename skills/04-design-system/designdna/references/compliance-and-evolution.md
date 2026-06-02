# DesignDNA References · Standalone Essentials, Compliance & Evolution Protocols (Parts 13–15)

> Loaded on demand from the `designdna` skill. See [SKILL.md](../SKILL.md) for the operating core.

{% raw %}

## Part 13: Standalone Essentials — Self-Sufficient Design Implementation

> When this skill runs WITHOUT companion skills (`frontend-patterns`, `coding-standards`, `ui-design`, etc.),
> it must carry enough implementation knowledge to produce professional results independently.
> These essentials are absorbed from companion skills but scoped to DESIGN IMPLEMENTATION only.

### 13.1 Component Architecture Essentials (from frontend-patterns)

**When writing UI components, follow this hierarchy**:

```
Atoms    → Single-purpose, no internal state (Button, Input, Badge, Avatar, Icon)
Molecules → Combine 2-3 atoms (FormField = Label + Input + Error, SearchBar = Input + Button)
Organisms → Sections with business logic (Header, HeroSection, ProductCard, Footer)
Templates → Full page layouts composing organisms
Pages    → Templates populated with real data
```

**Component file structure**:
```
ComponentName/
├── ComponentName.tsx        # Component logic
├── ComponentName.styles.ts  # Styles (or .module.css / Tailwind classes)
├── ComponentName.types.ts   # TypeScript interfaces
└── index.ts                 # Re-export
```

**State management for UI**:
- Local UI state (open/closed, hover, active) → `useState` / `ref()`
- Shared UI state (theme, sidebar, modal) → Context / Pinia / Zustand
- Server state (data fetching) → React Query / SWR / useFetch

### 13.2 CSS Architecture Essentials (from coding-standards)

**CSS variable naming convention**:
```css
/* Semantic token layers: primitive → semantic → component */

/* Layer 1: Primitives (raw values) */
--color-blue-500: #3b82f6;
--color-gray-900: #222222;
--font-size-16: 1rem;
--space-4: 16px;

/* Layer 2: Semantic (purpose-based, reference primitives) */
--text-primary: var(--color-gray-900);
--bg-primary: #ffffff;
--accent: var(--color-blue-500);
--gap-default: var(--space-4);

/* Layer 3: Component (specific use, reference semantic) */
--button-bg: var(--accent);
--button-text: #ffffff;
--card-bg: var(--bg-primary);
--card-shadow: var(--shadow-md);
```

**Tailwind best practices**:
```jsx
// ✅ GOOD: Semantic class grouping, readable
<button className="
  bg-blue-600 text-white font-medium
  px-4 py-2 rounded-lg
  hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-150
">

// ❌ BAD: Random order, hard to scan
<button className="text-white rounded-lg bg-blue-600 py-2 px-4 hover:bg-blue-700">
```

### 13.3 Accessibility Essentials (from frontend-patterns)

**Minimum requirements for every UI**:

```
1. Color contrast: WCAG AA → 4.5:1 for body text, 3:1 for large text (18px+)
2. Focus indicators: Every interactive element MUST have visible focus ring
3. Touch targets: Minimum 44x44px on mobile
4. Keyboard navigation: Tab order must be logical, Enter/Space activate buttons
5. Semantic HTML: Use <button> not <div onClick>, <nav> not <div class="nav">
6. Alt text: Every <img> has meaningful alt or alt="" if decorative
7. ARIA: Only when semantic HTML isn't sufficient; aria-label for icon-only buttons
```

**Focus ring pattern** (use in every project):
```css
/* Modern focus-visible ring */
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
:focus:not(:focus-visible) {
  outline: none;
}
```

### 13.4 Responsive Essentials (from frontend-patterns)

**Mobile-first breakpoint pattern**:
```css
/* Base: mobile (320px+) */
.container { padding: 16px; }

/* Tablet: 768px+ */
@media (min-width: 768px) {
  .container { padding: 24px; max-width: 720px; }
}

/* Desktop: 1024px+ */
@media (min-width: 1024px) {
  .container { padding: 32px; max-width: 960px; }
}

/* Wide: 1280px+ */
@media (min-width: 1280px) {
  .container { max-width: 1200px; }
}
```

**Responsive typography scale**:
```css
/* Fluid type: scales between mobile and desktop */
h1 { font-size: clamp(2rem, 5vw, 4rem); }
h2 { font-size: clamp(1.5rem, 3vw, 2.5rem); }
body { font-size: clamp(0.875rem, 1.5vw, 1rem); }
```

---

## Part 14: Design System Compliance Protocol

> **THE core problem this solves**: You create a DESIGN.md → tell the LLM to follow it → LLM partially ignores it.
> This protocol makes compliance MECHANICAL, not optional.

### 14.1 The Pre-Flight Check (MANDATORY before writing ANY UI code)

Every time the AI agent is about to write UI code for a page or component, it MUST execute this protocol BEFORE writing the first line:

```
┌─────────────────────────────────────────────────────┐
│           DESIGN SYSTEM PRE-FLIGHT CHECK            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. READ: Open and read the project's DESIGN.md     │
│     (or design system config file) completely.      │
│     If it doesn't exist → STOP, create it first.   │
│                                                     │
│  2. DECLARE: Before writing code, list explicitly:  │
│     "I will use these tokens from DESIGN.md:"       │
│     - Colors: [list specific hex/variable names]    │
│     - Typography: [list specific roles/sizes]       │
│     - Spacing: [list specific values]               │
│     - Shadows: [list specific levels]               │
│     - Radius: [list specific variants]              │
│     - Components: [list library components to use]  │
│                                                     │
│  3. WRITE: Implement using ONLY declared tokens.    │
│     Every CSS value must trace to DESIGN.md.        │
│                                                     │
│  4. VERIFY: After writing, run the Post-Flight.     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 14.2 The Post-Flight Check (MANDATORY after writing ANY UI code)

```
┌─────────────────────────────────────────────────────┐
│          DESIGN SYSTEM POST-FLIGHT CHECK            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  For EVERY new/modified file, verify:               │
│                                                     │
│  COLORS:                                            │
│  □ Zero inline hex values (all use variables)       │
│  □ No color not in DESIGN.md palette                │
│  □ Brand accent used for correct purpose only       │
│                                                     │
│  TYPOGRAPHY:                                        │
│  □ Font family matches DESIGN.md                    │
│  □ Font sizes from hierarchy table only             │
│  □ Font weights from approved list only             │
│  □ Letter-spacing scales with size                  │
│                                                     │
│  SPACING:                                           │
│  □ All values on 8px grid                           │
│  □ All values use spacing tokens                    │
│                                                     │
│  SHADOWS:                                           │
│  □ Shadows match elevation system levels            │
│  □ No invented shadow values                        │
│                                                     │
│  COMPONENTS:                                        │
│  □ 4 states: default, hover, focus, disabled        │
│  □ Using design system component, not hand-built    │
│                                                     │
│  ICONS:                                             │
│  □ All from declared icon library                   │
│  □ No emoji or text-as-icon                         │
│                                                     │
│  If ANY check fails → FIX before moving on.         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 14.3 The Compliance Report (output to user)

After every significant UI implementation, output a brief compliance report:

```markdown
## Design System Compliance Report

### Files modified: 3
- src/components/ProductCard.tsx ✅ PASS
- src/pages/Dashboard.tsx ✅ PASS
- src/components/Sidebar.tsx ⚠️ 1 issue

### Issues found:
1. Sidebar.tsx line 42: `color: #666` → should be `var(--text-secondary)` → **FIXED**

### Tokens used from DESIGN.md:
- Colors: --text-primary, --text-secondary, --bg-elevated, --accent, --border-primary
- Typography: Body (16px/400), Heading 3 (22px/600), Caption (12px/500)
- Spacing: space-3 (12px), space-4 (16px), space-6 (32px)
- Shadows: Level 1 (card rest)
- Radius: Standard (8px), Pill (9999px)

### Compliance: 100% (after fix)
```

### 14.4 The "Show Me the Token" Rule

**When the LLM writes any CSS value, it must be able to answer: "Which DESIGN.md token is this?"**

```
✅ TRACEABLE:
  color: var(--text-primary)           → DESIGN.md Section 2, Text Primary
  font-size: 16px                      → DESIGN.md Section 3, Body role
  padding: 16px                        → DESIGN.md Section 5, space-4
  border-radius: 8px                   → DESIGN.md Section 5, Standard
  box-shadow: var(--shadow-card)       → DESIGN.md Section 6, Level 1

❌ UNTRACEABLE (violation):
  color: #555                          → Not in DESIGN.md! Which token?
  font-size: 15px                      → Not in hierarchy table!
  padding: 13px                        → Not on 8px grid!
  border-radius: 5px                   → Not in radius scale!
  box-shadow: 0 2px 4px rgba(0,0,0,0.1) → Not in elevation system!
```

---

## Part 15: Design System Evolution Protocol

> **THE other core problem**: You update the design system, but changes don't propagate to existing code.

### 15.1 When to Evolve the Design System

Trigger design system evolution when:
- A design decision proves wrong in practice ("this blue CTA doesn't convert well")
- New features need tokens not yet in the system ("we need a warning state")
- Brand refresh or aesthetic adjustment ("make it warmer")
- Accessibility audit finds contrast issues
- User explicitly says "update the design system"

### 15.2 The Evolution Workflow

```
Step 1: DOCUMENT the change
  ├─ What: "Change primary CTA from #3b82f6 to #2563eb"
  ├─ Why: "Contrast ratio was 3.8:1, needs 4.5:1 for WCAG AA"
  └─ Scope: "All primary buttons, links, and focus rings"

Step 2: UPDATE DESIGN.md
  ├─ Edit the specific token in the DESIGN.md file
  ├─ Update Section 9 (Agent Prompt Guide) if hex values are referenced
  ├─ Update Section 7 (Do's/Don'ts) if rules are affected
  └─ Add a changelog entry at bottom of DESIGN.md:
      ## Changelog
      - [date] Changed --accent from #3b82f6 to #2563eb (WCAG contrast fix)

Step 3: FIND all usages of the old value
  Run search across entire codebase:
    - grep for old hex value (#3b82f6)
    - grep for the CSS variable name (--accent)
    - grep for Tailwind class (bg-blue-500 → bg-blue-600)
    - List ALL files and line numbers

Step 4: UPDATE all usages
  ├─ If using CSS variables → update ONLY the variable definition (one place!)
  ├─ If using Tailwind → find-replace class names
  ├─ If hardcoded values exist → replace with variable reference
  └─ Verify zero remaining old values

Step 5: VERIFY with Post-Flight Check
  Run the Post-Flight Check on ALL modified files
  Output a Compliance Report showing the migration is complete

Step 6: CONFIRM with user
  "Design system updated: --accent changed from #3b82f6 to #2563eb.
   Updated in 12 files. Zero remaining old values. Compliance: 100%."
```

### 15.3 Adding New Tokens

When the design system needs to grow (new color, new typography role, new component):

```
1. Check: does an existing token already cover this need?
   (Often a "new" color is just an existing token used differently)

2. If truly new:
   a. Add to the correct section of DESIGN.md
   b. Choose a semantic name (--status-warning, not --yellow-500)
   c. Add the CSS variable to the theme file
   d. Document its purpose and usage rules
   e. Add a Do/Don't if the new token has constraints

3. Update Section 9 (Agent Prompt Guide) to include the new token
```

### 15.4 Design System Changelog

Every DESIGN.md should end with a changelog section:

```markdown
---

## Changelog

| Date | Change | Reason | Scope |
|------|--------|--------|-------|
| 2026-04-11 | Initial DESIGN.md | Project creation | Full system |
| 2026-04-15 | --accent: #3b82f6 → #2563eb | WCAG contrast fix | Buttons, links, focus |
| 2026-04-20 | Added --status-warning: #f59e0b | New notification feature | Alerts, badges |
| 2026-04-25 | Body line-height: 1.5 → 1.6 | Readability improvement | All body text |
```

### 15.5 The "Single Source of Truth" Enforcement

```
DESIGN.md is the SINGLE SOURCE OF TRUTH.

When there's a conflict between:
  - DESIGN.md says #2563eb
  - Code says #3b82f6
  → DESIGN.md WINS. Fix the code.

When there's a conflict between:
  - DESIGN.md says font-weight: 600
  - A component uses font-weight: 700
  → DESIGN.md WINS. Fix the component.

The ONLY exception:
  - User explicitly says "change the design system to match what's in the code"
  → Then update DESIGN.md to match, making the code the new truth.
  → This is a DESIGN SYSTEM EVOLUTION, follow 15.2 workflow.
```


{% endraw %}
