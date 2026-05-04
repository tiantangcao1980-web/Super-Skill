# Token Naming

Prefer semantic tokens over raw palette names in application code.

| Layer | Example |
| --- | --- |
| Primitive | `color-blue-600`, `space-4`, `radius-2` |
| Semantic | `color-action-primary`, `color-surface-raised` |
| Component | `button-primary-bg`, `card-border` |

## Rules

- Components consume semantic/component tokens, not hardcoded hex values.
- Do not encode one-off layout in global tokens.
- Keep light/dark mode values behind the same semantic names.
- Name by role first, color second.
