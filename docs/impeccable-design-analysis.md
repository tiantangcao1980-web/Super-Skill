# Impeccable Design Analysis

Research snapshot: `pbakaus/impeccable` at commit `e587004`
(`2026-05-04`). Source: https://github.com/pbakaus/impeccable and
https://impeccable.style.

## What Matters

Impeccable is valuable because it treats design as harness engineering, not as
one more prompt. Its strongest ideas are:

- one compact design skill with a shared command vocabulary;
- setup gates that make product and design context explicit before mutation;
- progressive references for typography, color/contrast, spatial design,
  motion, interaction, responsive behavior, and UX writing;
- deterministic anti-pattern detection that can run without an LLM;
- cross-tool distribution for Cursor, Claude Code, OpenCode, Codex, Trae, and
  adjacent agent harnesses.

## Fit With Super Skill

Super Skill already had strong design-system material through DesignDNA,
brand systems, UI library skills, and anti-slop guidance. The missing layer was
an executable design workflow that tells an agent exactly when to:

- establish `PRODUCT.md` / `DESIGN.md` context;
- shape a UI before touching code;
- craft from tokens and components;
- critique subjectively;
- audit deterministically;
- polish/harden before delivery.

The new `design-craft-gate` skill fills that sequencing gap while preserving
DesignDNA as the source of truth for tokens, brand archetypes, and system
structure.

## Adopted

- `teach`, `document`, `shape`, `craft`, `critique`, `audit`, `polish`, and
  focused remediation modes as a Super Skill command vocabulary.
- `DESIGN_CRAFT_PREFLIGHT` as a compact context and mutation gate.
- Deterministic `bin/super-skill design-preflight` checks for product/design
  context, shape brief, tokens, visual references, and anti-pattern readiness.
- `bin/super-skill design-extract` for extracting CSS variables, colors,
  typography, spacing, radius, motion, component, and utility-class signals into
  a JSON sidecar plus optional `DESIGN.md` draft.
- `bin/super-skill design-live` for generating a browser live panel with an
  injectable overlay script, computed-style inspection, contrast probes, and
  CSS-variable live variants, plus an optional unpacked Chrome/Chromium
  extension bundle.
- `bin/super-skill design-capture` for optional Playwright browser injection,
  screenshot evidence, and computed-style report capture; the dry-run mode keeps
  CI dependency-light, and `--backend browser-use` supports exploratory CLI or
  authenticated-session capture.
- Deterministic `bin/super-skill design-audit` checks for repeatable AI UI
  patterns such as generic purple/cyan palettes, gradient text, decorative side
  borders, nested cards, pure black/white defaults, low-contrast text, skipped
  heading levels, flat type hierarchy, cramped padding, monotone spacing, bounce
  motion, layout transitions, and tiny text.
- Eval coverage that requires product/design context and anti-pattern evidence
  in the design-to-frontend quality path.

## Not Adopted

- No vendored Impeccable skill distribution.
- No duplicate `impeccable` skill name.
- No mandatory Puppeteer/Playwright runtime dependency in the core Super Skill
  CLI. Playwright is available as a root dev dependency for this repository's
  verification work, while downstream projects can still use dry-run or
  browser-use.

This keeps Super Skill dependency-light and avoids a forked copy of a fast-moving
design project.

## Upgrade Path

For UI work, agents should now load:

1. `design-craft-gate` for workflow sequencing.
2. `designdna` for tokens, system architecture, and brand conformance.
3. `anti-slop` for bias correction.
4. `browser-automation` or a frontend testing skill for visual verification.
5. `output-quality-gate` before delivery.

Run:

```bash
bin/super-skill design-audit --project <frontend-path> --json
bin/super-skill design-preflight --project <project-root> --strict --json
bin/super-skill design-extract --project <frontend-path> \
  --write-sidecar .super-skill/design/design.json \
  --write-design .super-skill/design/DESIGN.generated.md --json
bin/super-skill design-live --project <frontend-path> \
  --target-url http://localhost:3000 \
  --output .super-skill/design/live.html --json
bin/super-skill design-live --project <frontend-path> \
  --write-extension .super-skill/design/extension --json
bin/super-skill design-capture --project <project-root> \
  --url http://localhost:3000 \
  --screenshot .super-skill/design/live.png \
  --report .super-skill/design/capture.json --json
bin/super-skill design-capture --project <project-root> \
  --backend browser-use \
  --url http://localhost:3000 \
  --screenshot .super-skill/design/browser-use.png \
  --report .super-skill/design/browser-use.json --json
```

Use the scans as gates, not as substitutes for design judgment.
