# design-preflight NEGATIVE fixture (strict must block)

Deliberately missing `design/reference/`, `docs/screenshots/`, and any image
files so `design-preflight --strict` will flag `visual-references` as
blocking. The other context files exist so we isolate the failure to the
visual-references check.

Tests assert:

- `design-preflight --strict` fails on this fixture.
- `design-preflight --strict --skip visual-references` passes (opt-out works).
- `design-preflight` without `--strict` still passes (warn-only legacy mode).
