# Product

This fixture provides PRODUCT.md context but deliberately omits visual references so `design-preflight --strict` blocks on the `visual-references` check.

## User goal
Test that strict-mode honestly enforces every preflight check.

## Acceptance
- Strict mode fails.
- `--skip visual-references` passes.
