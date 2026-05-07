# Impeccable Lessons Adapted

Source studied:

- Project: https://github.com/pbakaus/impeccable
- Site: https://impeccable.style
- Local research snapshot: `pbakaus/impeccable` at commit `e587004`
- License: Apache-2.0

What Super Skill adopts:

- Context must come before visual mutation. Product and design context should be
  explicit enough that an agent can explain why a visual choice fits.
- A small shared command vocabulary improves prompt quality. Words such as
  `shape`, `craft`, `critique`, `audit`, and `polish` describe different work
  modes and reduce vague "make it better" loops.
- Deterministic anti-pattern checks are useful because they catch repeatable AI
  design failures before subjective review.
- Design references should be loaded progressively by domain: typography,
  color/contrast, layout, motion, interaction, responsive behavior, and UX copy.
- Browser or screenshot iteration should be part of the delivery loop whenever
  a visual surface changes.

What Super Skill intentionally does not copy:

- No vendored Impeccable distribution, browser extension, command scripts, or
  detector implementation.
- No duplicate `impeccable` skill name. Super Skill keeps a native
  `design-craft-gate` skill that composes with DesignDNA and anti-slop.
- No new Node runtime dependency for the core CLI. The local `design-audit`
  scanner is a smaller dependency-free Python gate.

Use Impeccable as a design-harness reference and keep upstream attribution when
borrowing rule names or concepts.
