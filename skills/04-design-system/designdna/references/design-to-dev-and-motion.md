# DesignDNA References · Design-to-Dev Workflow, Advanced Integration & Motion (Parts 11–12A)

> Loaded on demand from the `designdna` skill. See [SKILL.md](../SKILL.md) for the operating core.

{% raw %}

## Part 11: Integrated Design-to-Development Workflow

This is the complete workflow that combines design resources, DESIGN.md, and tech stack into a seamless pipeline.

### Phase 0: Project Initialization

```
1. Identify project type and platform
2. Select tech stack from Part 10 matrix
3. Choose design archetype from Part 2
4. Initialize project with Quick Commands from Part 10
5. Install offline resources (icons, fonts, animation)
```

### Phase 1: Design System Setup

```
1. Generate DESIGN.md (9-section format from Part 1)
2. In Section 2 (Colors):
   - Derive from archetype palette OR use Realtime Colors to preview
   - Define ALL as CSS variables or Tailwind theme
3. In Section 3 (Typography):
   - Install chosen fonts via Fontsource (offline)
   - Define hierarchy table with exact values
4. In Section 4 (Components):
   - Map to chosen component library's components
   - Document which library component implements each design element
5. Create theme configuration file matching DESIGN.md to library
```

### Phase 2: Asset Preparation

```
0. Inspiration research: extract principles, never clone assets
   - Sources: Dribbble, Awwwards, Page Flows, Muzli, ZCOOL, Alibaba UED
   - Extract: grid, density, image treatment, component rhythm, motion intent
   - Convert the useful parts into DESIGN.md tokens/rules before implementation

1. Core asset protocol for named brands/products
   - Verify current product/company facts before collecting assets
   - Ask/search/download/verify/freeze assets into brand-spec.md or equivalent notes
   - Priority: logo → product render/photo → UI screenshot → colors → fonts → mood words
   - For important non-logo visuals, use the 5-10-2-8 gate:
     5 source/search passes → 10 candidates → keep 2 → each should score 8/10+
   - Score by resolution, provenance, brand fit, composition consistency, narrative usefulness
   - If no asset reaches 8/10, ask for assets, use an honest placeholder, or generate with references

2. Icons: Import from chosen icon library (npm installed, offline)
   - List ALL icons needed by name: <Search />, <Settings />, <User />, etc.
   - NEVER use placeholder text for icons

3. Illustrations: Source from unDraw/Storyset
   - Download SVGs for: empty states, error pages, onboarding, features
   - Customize SVG colors to match DESIGN.md palette
   - Store locally in /public/illustrations/ or /src/assets/

4. Images & videos: Follow the source ladder
   - Tier 1: use Pexels + Huaban first
   - Tier 2: use Unsplash / Pixabay / Coverr / Mixkit only if Tier 1 cannot satisfy the brief
   - Tier 3: use specialized sources only for domain-specific needs (FoodiesFeed, Hippopx, UI Faces, etc.)
   - Use Pexels as the default source for stock photos and background videos
   - Use Huaban for Chinese-market inspiration, localized materials, and downloadable image/video assets
   - Optimize still images to WebP and videos to MP4/WebM
   - Generate responsive srcset versions for still images
   - Store images in /public/images/ and videos in /public/videos/

5. AI-generated assets: Use GPT Image 2 only when curated sources cannot satisfy the brief
   - Load skills/gpt-image-2/SKILL.md
   - For visual-risk work, generate clear section/detail references before implementation
   - Draft with quality=low at the target aspect ratio
   - Finalize with quality=medium/high and WebP/JPEG/PNG based on destination
   - Never request transparent backgrounds with gpt-image-2
   - Store prompt/provenance notes next to the generated asset

6. Avatars: Use DiceBear for programmatic generation
   - No network dependency, consistent across reloads
```

### Phase 3: Component Implementation

```
1. Build from library primitives (shadcn/ui, Ant Design, etc.)
2. Apply DESIGN.md tokens via theme configuration
3. Verify: every component uses tokens, never inline values
4. Add all 4 states (default, hover, focus, disabled)
5. Screenshot each component → compare against DESIGN.md specs
```

### Phase 4: Page Assembly & Polish

```
1. Assemble pages from components
2. Populate with real content (not Lorem ipsum)
3. Insert illustrations and images from Phase 2
4. Add animations from chosen library (Framer Motion, etc.)
5. Responsive check at all breakpoints
6. Accessibility audit (contrast, focus, touch targets)
7. Visual regression: does it match the DESIGN.md intent?
```

### Consistency Verification Checklist

```
Before marking any page complete:
□ All colors come from CSS variables / theme tokens
□ All icons come from ONE icon library (npm installed)
□ All fonts installed via Fontsource (no CDN dependency)
□ All illustrations are real SVGs, not placeholder text
□ All images are optimized WebP with srcset
□ All components come from ONE library (no mixing)
□ All spacing on 8px grid
□ All interactive elements have hover + focus + disabled states
□ All text meets WCAG AA contrast (4.5:1 body, 3:1 heading)
□ All touch targets ≥ 44px on mobile
□ Dark mode works (if supported)
□ No inline styles with hardcoded color/size values
```

---

## Part 12: Advanced Integration — A2UI, Pretext & Automation

> Open-source projects that take AI-driven UI generation from "approximate" to "verifiable".

### 12.1 Google A2UI — Agent-to-User Interface Protocol

**What**: An open-source declarative protocol by Google for AI agents to generate structured, renderable UI — purpose-built for LLMs.
**Repo**: https://github.com/google/A2UI (13.9k stars, Apache 2.0)
**Site**: https://a2ui.org/

**Why it matters for this skill**:
A2UI solves the fundamental fragility of LLM-generated UI. Instead of asking a model to produce raw HTML/CSS (which can be subtly broken), A2UI defines a **JSON component schema** that renderers on each platform convert to native widgets. The model outputs data, not code.

**Core architecture**:
```
AI Agent → A2UI JSON (declarative components) → Platform Renderer → Native UI
                                                  ├─ React renderer
                                                  ├─ Angular renderer
                                                  ├─ Flutter renderer
                                                  ├─ Lit (Web Components)
                                                  └─ Markdown fallback
```

**When to use A2UI**:
- Building AI agent products that need to render dynamic UI based on LLM output
- When you need **guaranteed valid** UI output (no broken HTML/CSS)
- When targeting **multiple platforms** from a single agent (web + mobile + desktop)
- Streaming UI generation (A2UI's incremental `updateComponents` model matches token-by-token LLM output)

**When NOT to use A2UI**:
- Traditional web/app development (use standard frameworks)
- Static websites, marketing pages, blogs
- Projects where the developer writes all UI manually

**Integration with this skill**:
When building an A2UI-based agent:
1. Use DESIGN.md to define the visual system (colors, typography, spacing)
2. Map DESIGN.md tokens to A2UI component properties
3. The agent generates A2UI JSON referencing design tokens
4. Platform renderers apply the DESIGN.md styles
5. Result: consistent, cross-platform UI driven by both design system AND agent intelligence

**A2UI component example**:
```json
{
  "type": "card",
  "id": "product-card-1",
  "properties": {
    "title": "Product Name",
    "subtitle": "Description text",
    "image": "https://...",
    "actions": [
      { "type": "button", "label": "Add to Cart", "variant": "primary" }
    ]
  }
}
```

**Install**:
```bash
npm i @anthropic-ai/sdk  # or any LLM SDK
# + A2UI renderer for your platform:
npm i @anthropic-ai/a2ui-react   # React
npm i @anthropic-ai/a2ui-angular # Angular
# See https://a2ui.org/ for latest packages
```

### 12.2 Pretext — Verifiable Text Layout

**What**: A pure TypeScript library (by the creator of React Motion) for multiline text measurement and layout WITHOUT DOM access. 300-1,242x faster than `getBoundingClientRect()`.
**Repo**: https://github.com/chenglou/pretext (42.8k stars, MIT)

**Why it matters for this skill**:
The #1 layout bug in AI-generated UI is **text overflow** — the LLM designs a container assuming text fits in 2 lines, but real text wraps to 4 lines and breaks the layout. Pretext lets you **mathematically verify** text will fit before rendering.

**When to use Pretext**:
- Canvas / SVG / WebGL rendering (no DOM available)
- Design-time validation: "Will this heading fit in one line at 375px width?"
- Performance-critical text layout (dashboards with thousands of labels)
- Building design preview tools that need accurate text measurement

**Integration with this skill**:
```typescript
import { prepare, layout } from 'pretext';

// Verify text fits in designed container
const font = await prepare('Inter', { size: 16, weight: 400 });
const result = layout(font, 'Your long product description text here...', {
  maxWidth: 280,  // container width from DESIGN.md
});

if (result.lines.length > 2) {
  console.warn('Text overflows designed 2-line container!');
  // → truncate, reduce font size, or expand container
}
```

**Install**:
```bash
npm i pretext
```

### 12.3 Material Symbols — Variable Icon Font (Parametric Icon System)

**What**: Google's next-gen icon system. Unlike static SVG icons (Lucide, Heroicons), Material Symbols are a **variable font** with 4 adjustable axes — one set of icons transforms into dozens of visual variants.
**Repo**: https://github.com/google/material-design-icons (53k stars, Apache 2.0)
**Browser**: https://fonts.google.com/icons

#### The 4 Axes Explained

```
┌─────────────────────────────────────────────────────────────────┐
│                 MATERIAL SYMBOLS — 4 AXES                       │
├──────────────┬──────────┬───────────────────────────────────────┤
│ Axis         │ Range    │ What it controls                     │
├──────────────┼──────────┼───────────────────────────────────────┤
│ FILL         │ 0 — 1    │ 空心(0) ↔ 实心(1)                    │
│              │          │ Outlined vs Filled                    │
│              │          │ 0 = line icon, 1 = solid fill         │
├──────────────┼──────────┼───────────────────────────────────────┤
│ wght (Weight)│ 100—700  │ 图标笔画粗细                          │
│              │          │ 100 = ultra-thin hairline             │
│              │          │ 400 = regular (default)               │
│              │          │ 700 = bold heavy strokes              │
├──────────────┼──────────┼───────────────────────────────────────┤
│ GRAD (Grade) │ -25—200  │ 图标强调度/胖瘦                       │
│              │          │ -25 = thinner (de-emphasized)         │
│              │          │ 0 = normal                            │
│              │          │ 200 = thicker (high emphasis)         │
│              │          │ Adjusts stroke WITHOUT changing size  │
├──────────────┼──────────┼───────────────────────────────────────┤
│ opsz         │ 20—48    │ 光学尺寸（小图标更简化，大图标更细节） │
│ (Optical Size)│         │ 20 = simplified for small use         │
│              │          │ 48 = detailed for large display       │
└──────────────┴──────────┴───────────────────────────────────────┘
```

#### CSS Implementation — Base Setup

```css
/* Step 1: Import the variable font */
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* Step 2: Base class */
.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  /* Default: outlined, regular weight, normal grade, 24px optical */
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

/* Step 3: HTML usage */
/* <span class="material-symbols-outlined">search</span>  */
/* <span class="material-symbols-outlined">home</span>    */
/* <span class="material-symbols-outlined">settings</span> */
```

#### Offline Installation (npm, no CDN dependency)

```bash
npm i material-symbols
```
```javascript
// In your entry file (main.ts / app.tsx / main.js)
import 'material-symbols';
```

#### 实际场景 — 图标形态变换

**场景 1: 金刚区（Feature Grid / Quick Action Zone）**

金刚区需要图标醒目、有重量感，通常用实心 + 较粗：

```css
/* 金刚区图标 — 大尺寸、实心、加粗 */
.icon-hero-zone {
  font-variation-settings: 'FILL' 1, 'wght' 600, 'GRAD' 0, 'opsz' 40;
  font-size: 40px;
  color: var(--accent);
}

/* 金刚区背景圆 */
.hero-zone-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.hero-zone-icon-bg {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: var(--accent-light);  /* 浅色品牌背景 */
  display: flex;
  align-items: center;
  justify-content: center;
}
```

```html
<!-- 金刚区 HTML -->
<div class="hero-zone-item">
  <div class="hero-zone-icon-bg">
    <span class="material-symbols-outlined icon-hero-zone">shopping_cart</span>
  </div>
  <span class="hero-zone-label">购物车</span>
</div>
```

**场景 2: 导航栏（Tab Bar）— 选中实心/未选中空心**

```css
/* 未选中：空心、常规粗细 */
.tab-icon {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  font-size: 24px;
  color: var(--text-tertiary);
  transition: font-variation-settings 0.2s ease;
}

/* 选中：实心、加粗 —— 同一图标，不同形态 */
.tab-icon.active {
  font-variation-settings: 'FILL' 1, 'wght' 600, 'GRAD' 0, 'opsz' 24;
  color: var(--accent);
}
```

**场景 3: 按钮内图标 — 匹配文字粗细**

```css
/* 轻量按钮（ghost/text button）*/
.btn-ghost .icon {
  font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' -25, 'opsz' 20;
  font-size: 18px;
}

/* 主按钮（primary CTA）*/
.btn-primary .icon {
  font-variation-settings: 'FILL' 0, 'wght' 500, 'GRAD' 0, 'opsz' 20;
  font-size: 20px;
}

/* 强调按钮（加粗实心）*/
.btn-emphasis .icon {
  font-variation-settings: 'FILL' 1, 'wght' 600, 'GRAD' 200, 'opsz' 24;
  font-size: 20px;
}
```

**场景 4: Hover 动态变换 — 空心变实心**

```css
/* 交互式图标：hover 从空心变实心 */
.icon-interactive {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  transition: font-variation-settings 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}
.icon-interactive:hover {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
```

**场景 5: 暗色/亮色模式适配**

```css
/* 亮色模式：正常 grade */
.icon { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }

/* 暗色模式：提高 grade 补偿暗背景上的视觉减弱 */
@media (prefers-color-scheme: dark) {
  .icon { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 200, 'opsz' 24; }
}
```

**场景 6: 不同尺寸自动适配**

```css
/* 小图标（侧边栏、列表项）— 简化细节 */
.icon-sm {
  font-size: 18px;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 20;
}

/* 中图标（工具栏、卡片）— 标准 */
.icon-md {
  font-size: 24px;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

/* 大图标（金刚区、空状态、引导页）— 丰富细节 */
.icon-lg {
  font-size: 40px;
  font-variation-settings: 'FILL' 1, 'wght' 500, 'GRAD' 0, 'opsz' 40;
}

/* 超大图标（Hero、空状态插图替代）— 最大细节 */
.icon-xl {
  font-size: 64px;
  font-variation-settings: 'FILL' 1, 'wght' 300, 'GRAD' 0, 'opsz' 48;
}
```

#### 与 DESIGN.md 集成

在 DESIGN.md 的 Section 4 (Component Stylings) 中，为图标定义标准化的变体：

```markdown
### Icon Variants

| Variant | FILL | wght | GRAD | opsz | Use Case |
|---------|------|------|------|------|----------|
| Outlined Light | 0 | 300 | -25 | 20 | 辅助文字旁、ghost 按钮、弱化场景 |
| Outlined Regular | 0 | 400 | 0 | 24 | 默认 UI 图标、工具栏、列表 |
| Outlined Bold | 0 | 600 | 0 | 24 | 强调操作、重要提示 |
| Filled Regular | 1 | 400 | 0 | 24 | 选中状态、活跃 Tab |
| Filled Bold | 1 | 600 | 0 | 40 | 金刚区、功能入口、大图标 |
| Filled Hero | 1 | 500 | 0 | 48 | 空状态、引导页、特大展示 |
```

#### 在 React/Vue/小程序中使用

**React**:
```tsx
import 'material-symbols';

// 基础组件
function Icon({ name, fill = false, weight = 400, grade = 0, size = 24, className = '' }) {
  return (
    <span
      className={`material-symbols-outlined ${className}`}
      style={{
        fontVariationSettings: `'FILL' ${fill ? 1 : 0}, 'wght' ${weight}, 'GRAD' ${grade}, 'opsz' ${size}`,
        fontSize: size,
      }}
    >
      {name}
    </span>
  );
}

// 金刚区用法
<Icon name="shopping_cart" fill size={40} weight={600} />
// 导航未选中
<Icon name="home" size={24} />
// 导航选中
<Icon name="home" fill weight={600} />
```

**Vue**:
```vue
<template>
  <span
    class="material-symbols-outlined"
    :style="{ fontVariationSettings: settings, fontSize: size + 'px' }"
  >
    {{ name }}
  </span>
</template>

<script setup>
const props = defineProps({
  name: String,
  fill: { type: Boolean, default: false },
  weight: { type: Number, default: 400 },
  grade: { type: Number, default: 0 },
  size: { type: Number, default: 24 },
});
const settings = computed(() =>
  `'FILL' ${props.fill ? 1 : 0}, 'wght' ${props.weight}, 'GRAD' ${props.grade}, 'opsz' ${props.size}`
);
</script>
```

**微信小程序（WXSS + WXML）**:
```css
/* app.wxss — 引入字体（需要下载到本地或使用CDN） */
@font-face {
  font-family: 'Material Symbols Outlined';
  src: url('https://fonts.gstatic.com/s/materialsymbolsoutlined/v200/kJEhBvYX7BgnkSrUwT8OhrdQw4oELdPIeeII9v6oFsI.woff2') format('woff2');
}
.ms-icon {
  font-family: 'Material Symbols Outlined';
  font-size: 24px;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
.ms-icon-filled { font-variation-settings: 'FILL' 1, 'wght' 600, 'GRAD' 0, 'opsz' 24; }
```
```html
<!-- index.wxml -->
<text class="ms-icon">search</text>
<text class="ms-icon ms-icon-filled">favorite</text>
```

**Flutter**:
```dart
// Flutter 原生支持 Material Symbols
Icon(
  Icons.shopping_cart,  // 自动跟随 Theme
  size: 40,
  fill: 1.0,           // Flutter 3.16+ 支持 fill 参数
  weight: 600,
  grade: 0,
  opticalSize: 40,
)
```

#### 何时选择 Material Symbols vs Lucide

| 需求 | 选 Material Symbols | 选 Lucide |
|------|-------------------|-----------|
| 需要同一图标多种形态（空心/实心/粗/细） | ✅ | ❌ 需要切换不同 SVG |
| 金刚区、Tab 栏选中/未选中切换 | ✅ 动态 FILL 轴 | ❌ 需要准备两套 SVG |
| hover 时图标变实心的交互 | ✅ CSS transition | ❌ 需要 JS 切换组件 |
| 暗色模式图标加粗补偿 | ✅ GRAD 轴 | ❌ 无此能力 |
| 图标与文字粗细精确匹配 | ✅ wght 轴 100-700 | ❌ 固定粗细 |
| 轻量级、Tree-shaking 友好 | ❌ 字体文件约 2MB | ✅ 按需导入单个 SVG |
| Tailwind 生态原生集成 | ❌ 需额外配置 | ✅ Lucide 原生支持 |
| React/Vue 组件化使用 | 需自建 Icon 组件 | ✅ 官方 React/Vue 包 |

### 12.4 Google zx — Design Asset Automation

**What**: Write shell scripts in JavaScript/TypeScript with `await $\`command\`` syntax. 45k stars.
**Repo**: https://github.com/google/zx (Apache 2.0)

**How it enhances this skill**:
zx enables scriptable design asset pipelines — automating the tedious parts of design-to-development:

**Use case 1 — Icon export automation**:
```javascript
#!/usr/bin/env npx zx
// Export all used icons from Lucide to optimized SVGs
const icons = ['search', 'settings', 'user', 'menu', 'x'];
for (const icon of icons) {
  await $`npx lucide-static export ${icon} --format svg --output ./public/icons/`;
}
await $`npx svgo ./public/icons/*.svg --multipass`;
echo`Exported and optimized ${icons.length} icons.`;
```

**Use case 2 — Font subset for performance**:
```javascript
#!/usr/bin/env npx zx
// Subset font to only include characters actually used in the project
const text = await $`grep -roh '[^\x00-\x7F]' src/ | sort -u | tr -d '\n'`;
await $`npx glyphhanger --whitelist="${text}" --subset=fonts/Inter.woff2`;
echo`Font subsetted to project's actual character set.`;
```

**Use case 3 — Visual regression check**:
```javascript
#!/usr/bin/env npx zx
// Screenshot before/after UI changes for comparison
await $`npx playwright screenshot http://localhost:3000 --output=before.png`;
echo('Make your UI changes, then press Enter...');
await question('');
await $`npx playwright screenshot http://localhost:3000 --output=after.png`;
await $`npx pixelmatch before.png after.png diff.png --threshold 0.1`;
echo`Diff saved to diff.png`;
```

**Install**:
```bash
npm i -g zx    # Global CLI
# Or per-project:
npm i -D zx
```

### 12.5 Architecture Reference — Closure Templates Safety Pattern

**From**: google/closure-templates (686 stars)

While not a direct dependency, Closure Templates demonstrates a critical pattern for AI-generated UI: **contextual auto-escaping**.

**The pattern**: When a template (or LLM) generates UI markup, the engine automatically applies the correct escaping based on context:
- Inside HTML attributes → HTML attribute escaping
- Inside `<script>` tags → JavaScript escaping
- Inside CSS `style` blocks → CSS escaping
- Inside URLs → URL encoding

**Apply this to our skill**:
When generating UI code, the AI agent should:
1. Never inject raw user-provided strings into HTML without escaping
2. Use framework-native binding (React JSX, Vue templates) which auto-escape by default
3. Never use `dangerouslySetInnerHTML` / `v-html` with dynamic content
4. Always sanitize URLs before binding to `href` or `src`

This is captured as a new rule in the consistency checklist:
```
□ No raw string injection — all dynamic content uses framework binding (auto-escaped)
```

---

## Part 12A: Motion Design System — Animation as Communication Language

> Animation is NOT decoration. Every motion communicates an INTENT or EMOTION.
> This section provides a complete, reusable motion design system.

### 12A.1 Standard Easing Curve Library

Define these as CSS variables in EVERY project:

```css
:root {
  /* Standard — most UI interactions (button clicks, toggles, hover) */
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);

  /* Enter — elements appearing (fade in, slide in, scale up) */
  --ease-enter: cubic-bezier(0, 0, 0.2, 1);

  /* Exit — elements disappearing (fade out, slide out, scale down) */
  --ease-exit: cubic-bezier(0.4, 0, 1, 1);

  /* Spring — bouncy, needs attention (success, favorite, delight) */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Elegant — slow, luxurious (brand pages, hero animations, premium feel) */
  --ease-elegant: cubic-bezier(0.16, 1, 0.3, 1);

  /* Linear — ONLY for loading spinners and progress bars */
  --ease-linear: linear;

  /* Duration scale */
  --duration-instant: 100ms;   /* micro-feedback: button press, toggle */
  --duration-fast: 200ms;      /* standard transitions: hover, focus */
  --duration-normal: 300ms;    /* modal open/close, slide transitions */
  --duration-slow: 500ms;      /* complex animations, page transitions */
  --duration-elegant: 800ms;   /* brand/luxury animations */
}
```

### 12A.2 Animation Emotion Map

When choosing an animation, START from the emotion you want to convey:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ANIMATION EMOTION MAP                                    │
├──────────────┬──────────┬──────────────────┬───────────────────────────────┤
│ Emotion      │ Duration │ Easing           │ Effect                        │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Confirmation │ 200-300ms│ ease-spring      │ Scale bounce, checkmark draw  │
│ "成功了！"    │          │                  │ Green color + bounce          │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Warning      │ 300-400ms│ ease-standard    │ Horizontal shake, red flash   │
│ "出错了"      │          │                  │ Shake 3-4 times + red border  │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Attention    │ 400-600ms│ ease-standard    │ Pulse breathing, gentle slide │
│ "看这里"      │          │                  │ Scale 1→1.1→1 loop           │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Waiting      │ 1-2s     │ linear           │ Spin, skeleton shimmer        │
│ "请稍等"      │          │                  │ Infinite loop until done      │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Delight      │ 300-500ms│ ease-spring      │ Bouncy pop, confetti, sparkle │
│ "太棒了！"    │          │                  │ Overshoot + settle            │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Calm         │ 200-400ms│ ease-enter/exit  │ Fade, gentle slide            │
│ "自然过渡"    │          │                  │ Opacity + translateY(16px)    │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Urgency      │ 100-200ms│ ease-standard    │ Fast flash, countdown pulse   │
│ "快！"        │          │                  │ Rapid opacity toggle          │
├──────────────┼──────────┼──────────────────┼───────────────────────────────┤
│ Premium      │ 500-800ms│ ease-elegant     │ Slow reveal, parallax scroll  │
│ "高级感"      │          │                  │ Long duration + subtle motion │
└──────────────┴──────────┴──────────────────┴───────────────────────────────┘
```

### 12A.3 Icon State Machine (8 States)

Every interactive icon in a UI goes through these states. Define ALL of them in your DESIGN.md:

```css
/* === ICON STATE MACHINE — 8 STATES === */

/* 1. Default — idle, waiting for interaction */
.icon-state-default {
  font-variation-settings: 'FILL' 0, 'wght' 400;
  color: var(--text-tertiary);
  transition: all var(--duration-fast) var(--ease-standard);
}

/* 2. Hover — mouse over, inviting interaction */
.icon-state-default:hover {
  font-variation-settings: 'FILL' 0, 'wght' 500;
  color: var(--text-primary);
  transform: scale(1.05);
}

/* 3. Pressed — actively being clicked */
.icon-state-default:active {
  font-variation-settings: 'FILL' 1, 'wght' 500;
  color: var(--accent);
  transform: scale(0.95);
}

/* 4. Selected / Active — current state */
.icon-state-selected {
  font-variation-settings: 'FILL' 1, 'wght' 600;
  color: var(--accent);
}

/* 5. Disabled — not available */
.icon-state-disabled {
  font-variation-settings: 'FILL' 0, 'wght' 300;
  color: var(--text-quaternary);
  opacity: 0.5;
  pointer-events: none;
}

/* 6. Success — operation completed */
.icon-state-success {
  font-variation-settings: 'FILL' 1, 'wght' 500;
  color: var(--color-success);
  animation: bounce-in var(--duration-normal) var(--ease-spring);
}

/* 7. Error — operation failed */
.icon-state-error {
  font-variation-settings: 'FILL' 1, 'wght' 600;
  color: var(--color-error);
  animation: shake var(--duration-normal) var(--ease-standard);
}

/* 8. Loading — waiting for result */
.icon-state-loading {
  font-variation-settings: 'FILL' 0, 'wght' 400;
  color: var(--accent);
  animation: spin 1s var(--ease-linear) infinite;
}
```

### 12A.4 Interaction Intent Expression Framework

Use this table when designing ANY interactive element:

```
USER ACTION          → UI RESPONSE                    → EMOTION CONVEYED
─────────────────────────────────────────────────────────────────────────
Tap button           → Scale 0.95 → 1.0               → "Received"
Submit success       → ✓ icon bounces in + green       → "Done!"
Input error          → Input shakes + red border       → "Fix this"
Loading data         → Skeleton shimmer / spinner      → "Working on it"
Drag item            → Shadow deepens + follows cursor → "You control this"
Delete item          → Slide left + fade out           → "It's gone"
New notification     → Bell pulses + red dot appears   → "Something for you"
Favorite / Like      → Heart: outline → filled + bounce→ "Loved!"
Tab switch           → Icon: outline → filled + slide  → "You are here"
Page enter           → Content fades in from below     → "Welcome"
Page leave           → Content fades up and out        → "Goodbye"
Pull to refresh      → Spinner → ✓ bounce              → "Fresh data"
Long press           → Scale up slowly + haptic        → "Extra options"
Swipe card           → Card follows finger + tilt      → "Your choice"
Scroll to section    → Element fades in when visible   → "Discover more"
Empty state          → Illustration + subtle float     → "Nothing yet, but..."
Error page           → Sad illustration + shake        → "Oops, let's fix this"
```

### 12A.5 Standard Keyframe Library

Copy these into every project:

```css
/* Success — bouncy entrance */
@keyframes bounce-in {
  0%   { transform: scale(0); opacity: 0; }
  60%  { transform: scale(1.15); }
  100% { transform: scale(1); opacity: 1; }
}

/* Error — horizontal shake */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%      { transform: translateX(-4px); }
  40%      { transform: translateX(4px); }
  60%      { transform: translateX(-3px); }
  80%      { transform: translateX(3px); }
}

/* Loading — rotation */
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Attention — pulse breathing */
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50%      { transform: scale(1.08); opacity: 0.85; }
}

/* Content enter — fade in up */
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Content exit — fade out up */
@keyframes fade-out-up {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(-16px); }
}

/* Skeleton loading shimmer */
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Notification dot — pop in */
@keyframes dot-pop {
  0%   { transform: scale(0); }
  60%  { transform: scale(1.3); }
  100% { transform: scale(1); }
}

/* Slide in from right */
@keyframes slide-in-right {
  from { transform: translateX(100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}

/* Slide out to left (for delete) */
@keyframes slide-out-left {
  from { transform: translateX(0); opacity: 1; }
  to   { transform: translateX(-100%); opacity: 0; }
}
```

### 12A.6 Skeleton Component Template

Every loading state should use skeleton screens, not spinners (unless the area is < 100px):

```css
.skeleton {
  background: linear-gradient(90deg,
    var(--bg-elevated) 25%,
    color-mix(in srgb, var(--bg-elevated) 85%, var(--text-quaternary)) 50%,
    var(--bg-elevated) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s var(--ease-linear) infinite;
  border-radius: var(--radius-subtle);
}
.skeleton-text   { height: 16px; width: 80%; margin-bottom: 8px; }
.skeleton-title  { height: 24px; width: 60%; margin-bottom: 12px; }
.skeleton-avatar { height: 48px; width: 48px; border-radius: 50%; }
.skeleton-image  { height: 200px; width: 100%; border-radius: var(--radius-standard); }
.skeleton-button { height: 40px; width: 120px; border-radius: var(--radius-subtle); }
```

---


{% endraw %}
