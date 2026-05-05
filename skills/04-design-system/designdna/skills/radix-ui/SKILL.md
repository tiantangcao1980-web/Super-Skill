---
name: radix-ui
description: Radix UI — two sibling libraries. Radix Primitives (18.8k stars) is unstyled, accessible React primitives (Dialog, Popover, Tooltip, Select, etc.) used by shadcn/ui and thousands of custom design systems. Radix Themes (8.3k stars, v3.3) is an opinionated styled layer on Primitives with 12-step color scales. Both active 2026. Use when building a React desktop or B2B admin/dashboard UI.
---

# Radix UI — Primitives + Themes

> **Sources**:
> - [radix-ui/primitives](https://github.com/radix-ui/primitives) · 18.8k ⭐ · 🟢 active
> - [radix-ui/themes](https://github.com/radix-ui/themes) · 8.3k ⭐ · v3.3.0 · 🟢 active
>
> **NPM**: `@radix-ui/react-*` (primitives) · `@radix-ui/themes` (styled)
> **Docs**: https://www.radix-ui.com/primitives · https://www.radix-ui.com/themes

## 1. Which to pick

### Radix Primitives
- You're building a **custom design system** (Tailwind + your own styles)
- Want accessibility correctness without opinionated styling
- Using shadcn/ui (which is built on Primitives)

### Radix Themes
- Want **drop-in styled UI** without writing CSS
- Like Radix's 12-step color scales
- Want "modern, clean, slightly softer than Material" aesthetic

## 2. Install

### Primitives (per-component)

```bash
npm install @radix-ui/react-dialog @radix-ui/react-popover @radix-ui/react-select
# etc.
```

### Themes (all-in-one)

```bash
npm install @radix-ui/themes
```

```tsx
// Root
import '@radix-ui/themes/styles.css';
import { Theme } from '@radix-ui/themes';

<Theme
  accentColor="indigo"
  grayColor="slate"
  radius="medium"
  appearance="light"  // or 'dark'
>
  <App />
</Theme>
```

## 3. Primitives catalog

Each is a separate package `@radix-ui/react-<name>`:

`accordion` · `alert-dialog` · `aspect-ratio` · `avatar` · `checkbox` · `collapsible` · `context-menu` · `dialog` · `dropdown-menu` · `form` · `hover-card` · `label` · `menubar` · `navigation-menu` · `popover` · `progress` · `radio-group` · `scroll-area` · `select` · `separator` · `slider` · `slot` · `switch` · `tabs` · `toast` · `toggle` · `toggle-group` · `toolbar` · `tooltip` · `visually-hidden`

Full list: https://www.radix-ui.com/primitives/docs/overview/introduction

## 4. Themes component catalog

`AlertDialog` · `AspectRatio` · `Avatar` · `Badge` · `Blockquote` · `Box` · `Button` · `Callout` · `Card` · `Checkbox` · `CheckboxCards` · `CheckboxGroup` · `Code` · `ContextMenu` · `DataList` · `Dialog` · `DropdownMenu` · `Em` · `Flex` · `Grid` · `HoverCard` · `IconButton` · `Inset` · `Kbd` · `Link` · `Popover` · `Progress` · `Quote` · `RadioCards` · `RadioGroup` · `ScrollArea` · `SegmentedControl` · `Select` · `Separator` · `Skeleton` · `Slider` · `Spinner` · `Strong` · `Switch` · `Table` · `Tabs` · `Text` · `TextArea` · `TextField` · `Theme` · `ThemePanel` · `Tooltip`

## 5. Usage — Primitives (headless)

### Dialog

```tsx
import * as Dialog from '@radix-ui/react-dialog';
import { X } from 'lucide-react';

<Dialog.Root>
  <Dialog.Trigger asChild>
    <button className="btn-primary">Open</button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/50 z-50" />
    <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg z-50 w-96">
      <Dialog.Title className="text-lg font-semibold">Confirm</Dialog.Title>
      <Dialog.Description className="text-sm text-gray-600 mt-2">
        Are you sure?
      </Dialog.Description>
      <div className="flex justify-end gap-2 mt-4">
        <Dialog.Close className="btn-secondary">Cancel</Dialog.Close>
        <Dialog.Close className="btn-primary">Confirm</Dialog.Close>
      </div>
      <Dialog.Close className="absolute top-4 right-4">
        <X size={16} />
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

### Select

```tsx
import * as Select from '@radix-ui/react-select';
import { Check, ChevronDown } from 'lucide-react';

<Select.Root>
  <Select.Trigger className="...">
    <Select.Value placeholder="Select a fruit…" />
    <Select.Icon><ChevronDown /></Select.Icon>
  </Select.Trigger>
  <Select.Portal>
    <Select.Content className="bg-white border rounded shadow">
      <Select.Viewport>
        <Select.Item value="apple">
          <Select.ItemText>Apple</Select.ItemText>
          <Select.ItemIndicator><Check /></Select.ItemIndicator>
        </Select.Item>
        <Select.Item value="banana">
          <Select.ItemText>Banana</Select.ItemText>
        </Select.Item>
      </Select.Viewport>
    </Select.Content>
  </Select.Portal>
</Select.Root>
```

## 6. Usage — Themes (styled)

### Button

```tsx
import { Button, IconButton } from '@radix-ui/themes';
import { TrashIcon } from '@radix-ui/react-icons';

<Button variant="solid" color="indigo" onClick={save}>Save</Button>
<Button variant="soft">Cancel</Button>
<Button color="red" variant="surface"><TrashIcon /> Delete</Button>
<Button size="3" radius="full">Large round</Button>
<IconButton><TrashIcon /></IconButton>
```

### Card + layout

```tsx
import { Card, Flex, Text, Heading, Button, Box } from '@radix-ui/themes';

<Card size="3">
  <Flex direction="column" gap="2">
    <Heading size="4">Project name</Heading>
    <Text color="gray" size="2">Description goes here.</Text>
    <Box mt="4">
      <Button>Open</Button>
    </Box>
  </Flex>
</Card>
```

### Dialog

```tsx
import { Dialog, Button, Flex, TextField } from '@radix-ui/themes';

<Dialog.Root>
  <Dialog.Trigger>
    <Button>Edit profile</Button>
  </Dialog.Trigger>
  <Dialog.Content maxWidth="450px">
    <Dialog.Title>Edit profile</Dialog.Title>
    <Flex direction="column" gap="3">
      <label>
        <Text as="div" size="2" mb="1" weight="bold">Name</Text>
        <TextField.Root defaultValue="..." />
      </label>
    </Flex>
    <Flex gap="3" mt="4" justify="end">
      <Dialog.Close><Button variant="soft" color="gray">Cancel</Button></Dialog.Close>
      <Dialog.Close><Button>Save</Button></Dialog.Close>
    </Flex>
  </Dialog.Content>
</Dialog.Root>
```

## 7. Theme customization (Themes)

```tsx
<Theme
  accentColor="indigo"          // 20+ options: indigo / violet / purple / pink / red / green / mint / etc.
  grayColor="slate"             // gray / mauve / slate / sage / olive / sand
  panelBackground="solid"       // or 'translucent'
  radius="medium"               // none / small / medium / large / full
  scaling="100%"                // 90% / 95% / 100% / 105% / 110%
  appearance="light"            // light / dark / inherit
>
```

Plus CSS variables for fine-grain overrides (`--accent-9`, `--gray-12`, etc., full 12-step palettes).

## 8. BANNED

- ❌ NEVER skip `<Theme>` wrapper for Radix Themes — components won't style
- ❌ NEVER mix Radix Themes with another styled library (MUI, antd) — conflicting tokens
- ❌ NEVER forget `@radix-ui/themes/styles.css` import
- ❌ NEVER import Radix Primitives' CSS — there is none, they're unstyled
- ❌ NEVER omit `<Dialog.Portal>` — content renders in the wrong place without portal
- ❌ NEVER use Radix Primitives without applying focus-visible / ARIA styles yourself (they provide the semantics, you provide the look)
- ❌ NEVER install all `@radix-ui/react-*` packages — install per component used

## 9. Pre-flight checklist

### For Primitives (headless)

```
- [ ] Installed only the primitives actually used
- [ ] Styles written (Tailwind or CSS) — Primitives are unstyled
- [ ] <*.Portal> used for Dialog / Popover / Select / Tooltip
- [ ] Focus-visible styling applied
- [ ] Keyboard shortcuts tested (Tab / Enter / Esc / Arrow keys)
- [ ] Animation states handled (data-state="open"|"closed")
```

### For Themes (styled)

```
- [ ] @radix-ui/themes installed
- [ ] @radix-ui/themes/styles.css imported once at root
- [ ] <Theme> wrapping app with accentColor / grayColor / radius / appearance
- [ ] Not mixing with antd / MUI / Chakra — pick one design system
- [ ] Dark mode strategy: prop-based (appearance="dark") or auto (appearance="inherit" + class on html)
```

## 10. Dial fit

Radix Themes: formality: 7 · motion: 4 · density: 4 · warmth: 4 · contrast: 7
Radix Primitives: depends on your styling (fully configurable)
