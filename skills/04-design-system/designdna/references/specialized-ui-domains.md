# DesignDNA References · Specialized UI Domains — 3D / Maps / Search / Knowledge Graph / Mini-Program (Parts 12B–12J)

> Loaded on demand from the `designdna` skill. See [SKILL.md](../SKILL.md) for the operating core.

{% raw %}

## Part 12B: Mini Program — Material Symbols Implementation & Performance

> Solving the challenge: Stitch prototypes using Material Symbols → mini program production code.

### 12B.1 The Core Problem

Material Symbols is a variable font (~2MB). Mini programs have strict size limits:
- WeChat: total package ≤ 2MB (main), subpackages ≤ 2MB each
- Alipay: total ≤ 4MB
- Douyin: total ≤ 4MB

**You CANNOT bundle the full Material Symbols font into a mini program.**

### 12B.2 Three Solutions (choose by scenario)

**Solution A: Font Subset (Recommended for < 50 icons)**

Extract only the glyphs you actually use, reducing ~2MB → ~20-50KB:

```bash
# Step 1: List all icon names used in your mini program
grep -roh 'icon-name="[^"]*"' pages/ | sort -u > used-icons.txt

# Step 2: Use glyphhanger or fonttools to subset
npx glyphhanger --whitelist="search,home,favorite,settings,..." \
  --subset=node_modules/material-symbols/material-symbols-outlined.woff2 \
  --output=assets/fonts/

# Result: ~20-50KB font file with only your icons
```

**Solution B: SVG Sprite (Recommended for 50-200 icons)**

Convert needed Material icons to an SVG sprite file:

```bash
# Use designdna's pre-downloaded Material SVGs
# Create sprite from needed icons
npx svg-sprite \
  --mode symbol \
  --dest assets/ \
  designdna/assets/icons/material/navigation/*.svg \
  designdna/assets/icons/material/actions/*.svg
```

```html
<!-- WXML usage -->
<svg class="icon" style="width:48rpx;height:48rpx;fill:{{color}};">
  <use href="/assets/icons-sprite.svg#search" />
</svg>
```

**Solution C: Image Component with CDN (Recommended for rapid prototyping)**

Use Google's Material Symbols CDN to generate PNG/SVG on the fly:

```javascript
// utils/icon.js — Generate icon URL
function getMaterialIconUrl(name, { fill = 0, weight = 400, grade = 0, size = 24, color = '333333' } = {}) {
  // Use Google Fonts API to render the icon as an image
  return `https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/${name}/default/${size}px.svg`;
}

// For offline: use the pre-downloaded SVGs from designdna
function getLocalIconPath(name, category = 'actions') {
  return `/assets/icons/material/${category}/${name}.svg`;
}
```

### 12B.3 Mini Program Icon Performance Checklist

```
□ Total icon assets < 200KB (for main package)
□ Icon font subsetted to only used glyphs (if using font approach)
□ SVG sprites used for repeated icons (if using SVG approach)
□ TabBar icons are PNG format, 81×81px, < 40KB each
□ Icons lazy-loaded in subpackages (not all in main package)
□ Dark mode icon variants handled via CSS filter or color property
□ Touch targets ≥ 88rpx (44px equivalent) on all icon buttons
□ Icon loading has placeholder (no blank flash)
```

### 12B.4 Mini Program Visual Design Quality Checklist

```
□ Navigation bar color matches page background
□ Safe area handled (iPhone notch / home indicator)
□ rpx units used for all sizes (not px)
□ Font loaded with wx.loadFontFace or embedded base64
□ Images use lazy-load and WebP format
□ Skeleton screens for all loading states
□ Transitions on page enter (fade-in-up)
□ Gold standard: 首屏渲染 < 1.5s, 交互响应 < 100ms
```

---

## Part 12C: Interaction Design Pattern Library & Experience Accumulation

> Solving: How to design professional interactions for Stitch prototypes, and how to accumulate interaction design experience across projects.

### 12C.1 Core Interaction Patterns (from 58-brand analysis)

These patterns were observed repeatedly across the 58 world-class brands:

**Pattern 1: Progressive Disclosure**
> Show only what's needed now; reveal more on demand.
```
Use when: Complex forms, settings pages, onboarding
How: Accordion sections, "Show more" links, stepped wizards
Brands: Stripe (checkout), Notion (slash commands), Linear (filters)
```

**Pattern 2: Optimistic Updates**
> Update the UI immediately, sync with server in background.
```
Use when: Like/favorite, toggle, drag-reorder, message send
How: Change UI state → send API → if error, revert + show toast
Brands: Twitter/X (like), Notion (drag blocks), Linear (status change)
```

**Pattern 3: Skeleton → Content**
> Show content shape before data arrives.
```
Use when: Any data-loading page, list, card grid, profile
How: Skeleton placeholder → fade-in real content
Brands: LinkedIn, YouTube, Notion, Airbnb (ALL use skeleton)
```

**Pattern 4: Contextual Actions**
> Actions appear only when relevant, near the content they affect.
```
Use when: List items, cards, table rows, text blocks
How: Hover/long-press reveals action buttons; right-click context menu
Brands: Notion (block hover), Linear (issue hover), VS Code (gutter)
```

**Pattern 5: Inline Editing**
> Edit content in-place without navigating to a form page.
```
Use when: Titles, descriptions, tags, status fields
How: Click text → transforms to input → blur/Enter saves
Brands: Notion (all text), Linear (issue title), Figma (layer names)
```

**Pattern 6: Command Palette**
> Keyboard-first search over all actions.
```
Use when: Power-user tools, developer apps, productivity software
How: Cmd/Ctrl+K opens search → fuzzy match actions/pages → execute
Brands: Linear, Raycast, VS Code, Notion, Vercel
```

**Pattern 7: Drag to Reorder**
> Direct manipulation for ordering items.
```
Use when: Lists, kanban boards, navigation items, dashboard widgets
How: Long-press/grip handle → drag with shadow → drop with animation
Brands: Trello, Notion, Linear, Miro
```

**Pattern 8: Empty State with CTA**
> Never show a blank screen. Guide the user to the first action.
```
Use when: First-time use, search no results, empty list, no data
How: Illustration + message + primary CTA button
Brands: ALL 58 brands have empty state designs
```

**Pattern 9: Toast/Snackbar for Non-Blocking Feedback**
> Confirm actions without interrupting the flow.
```
Use when: Save, copy, delete, send, any background operation
How: Bottom/top notification → auto-dismiss 3-5s → optional undo
Brands: Google (undo), Notion (saved), Vercel (deployed)
```

**Pattern 10: Pull to Refresh (Mobile/Mini Program)**
> Physical gesture to request fresh data.
```
Use when: Feed, list, dashboard on mobile/mini program
How: Pull down → loading animation → content updates → bounce back
Brands: Twitter, Instagram, any mobile-first app
```

### 12C.2 Page State Machine

Every page in your app exists in one of these states. Design ALL of them:

```
┌─────────────┐
│   Loading    │ ← Skeleton screens, NOT spinner
├─────────────┤
│   Empty      │ ← Illustration + "Get started" CTA
├─────────────┤
│   Content    │ ← Normal state with data
├─────────────┤
│   Error      │ ← Error illustration + "Retry" button
├─────────────┤
│   Partial    │ ← Some data loaded, some failed
├─────────────┤
│   Offline    │ ← Cached data + "No connection" banner
└─────────────┘
```

**In DESIGN.md, add this to Section 4 (Component Stylings):**

```markdown
### Page States

| State | Background | Content | Action |
|-------|-----------|---------|--------|
| Loading | Skeleton shimmer | Placeholder shapes | None |
| Empty | Illustration (from unDraw/Storyset) | "No [items] yet" | Primary CTA "Create first [item]" |
| Content | Normal | Real data | Normal interactions |
| Error | Error illustration | "Something went wrong" | "Try again" button |
| Offline | Yellow/orange banner at top | Cached data (grayed) | "Retry when online" |
```

### 12C.3 Form Interaction Patterns

```
Field validation timing:
  Email/Phone     → validate on blur (not every keystroke)
  Password        → strength indicator on keystroke
  Required fields → validate on submit attempt, then on blur after first error
  Real-time search→ debounce 300ms after typing stops

Error display:
  Inline error    → red text below field + red border (for specific field errors)
  Toast           → for general server errors
  Banner          → for form-level validation ("Please fix 3 errors above")

Submit states:
  Idle            → "Submit" (primary button)
  Submitting      → "Submitting..." (disabled + spinner)
  Success         → "✓ Done" (green, 1.5s) → redirect or reset
  Error           → Shake button + show error message
```

### 12C.4 Experience Accumulation System

**After each project, record interaction patterns that worked well or poorly:**

When the user completes a project with interaction design, the AI should suggest:

```
"Project completed. Should I record these interaction decisions for future reference?"

If yes, create a file: designdna/experience/[project-name]-interactions.md

## [Project Name] — Interaction Decisions Log

### What worked well
- Progressive disclosure on settings page reduced cognitive load
- Optimistic updates on favorite button felt instant
- Skeleton screens eliminated perceived loading time

### What didn't work
- Inline editing on mobile was hard to trigger (touch targets too small)
- Toast auto-dismiss was too fast (2s → increased to 4s)

### Patterns to reuse
- Card swipe-to-delete with undo toast (3s window)
- Bottom sheet for mobile actions (instead of dropdown)
- Haptic feedback on drag reorder
```

**Over time, build a project-specific interaction design knowledge base in `designdna/experience/`.**

This connects with the `hierarchical-memory` skill — when that skill is available, interaction experience automatically feeds into the long-term memory system. When it's not available, the `designdna/experience/` directory serves as a standalone knowledge base.

---

## Part 12D: Lottie Animation Integration

> Lottie renders After Effects animations in real-time as vector graphics.
> JSON format, tiny file size, infinite scalability, no quality loss at any resolution.
> Source: https://app.lottiefiles.com/ | https://github.com/airbnb/lottie-web

### 12D.1 When to Use Lottie vs CSS vs GIF

```
┌──────────────────────────────────────────────────────────────────────┐
│                 ANIMATION TECHNOLOGY DECISION                        │
├──────────────┬───────────┬──────────┬───────────┬───────────────────┤
│ Scenario     │ CSS Anim  │ Lottie   │ GIF/APNG  │ Best Choice       │
├──────────────┼───────────┼──────────┼───────────┼───────────────────┤
│ Button hover │ ✅ Best    │ Overkill │ ❌        │ CSS transition    │
│ Loading spin │ ✅ Simple  │ ✅ Rich  │ ❌        │ CSS (simple) or   │
│              │           │          │           │ Lottie (branded)  │
│ Success ✓    │ ✅ OK     │ ✅ Best  │ ❌        │ Lottie (smooth)   │
│ Empty state  │ ❌ Limited │ ✅ Best  │ OK        │ Lottie (engaging) │
│ Onboarding   │ ❌        │ ✅ Best  │ ❌        │ Lottie (complex)  │
│ Icon anim    │ ❌        │ ✅ Best  │ ❌        │ Lottie (precise)  │
│ Page trans   │ ✅ Best    │ ❌       │ ❌        │ CSS / Framer      │
│ Scroll anim  │ ✅ Best    │ ✅ OK   │ ❌        │ CSS + Intersection│
│ Brand intro  │ ❌        │ ✅ Best  │ ❌        │ Lottie (cinematic)│
│ Confetti     │ ❌        │ ✅ Best  │ ❌        │ Lottie (particles)│
└──────────────┴───────────┴──────────┴───────────┴───────────────────┘
```

**Rule: If the animation involves more than 2 elements moving independently → use Lottie.**

### 12D.2 Lottie Integration by Platform

**React**:
```bash
npm i lottie-react
```
```tsx
import Lottie from 'lottie-react';
import successAnim from './animations/success.json';

function SuccessFeedback() {
  return <Lottie animationData={successAnim} loop={false} style={{ width: 120, height: 120 }} />;
}
```

**Vue**:
```bash
npm i vue3-lottie
```
```vue
<template>
  <Vue3Lottie :animationData="loadingAnim" :loop="true" :width="80" :height="80" />
</template>
<script setup>
import { Vue3Lottie } from 'vue3-lottie';
import loadingAnim from './animations/loading.json';
</script>
```

**Mini Program (WeChat)**:
```bash
npm i lottie-miniprogram
```
```html
<!-- WXML -->
<canvas id="lottie-canvas" type="2d" style="width:200rpx;height:200rpx;" />
```
```javascript
// JS
import lottie from 'lottie-miniprogram';
Page({
  onReady() {
    const query = this.createSelectorQuery();
    query.select('#lottie-canvas').node(res => {
      const canvas = res[0].node;
      lottie.setup(canvas);
      lottie.loadAnimation({
        path: '/animations/loading.json',
        loop: true,
        autoplay: true,
        rendererSettings: { context: canvas.getContext('2d') }
      });
    }).exec();
  }
});
```

**React Native**:
```bash
npm i lottie-react-native
```
```tsx
import LottieView from 'lottie-react-native';
<LottieView source={require('./animations/success.json')} autoPlay loop={false} style={{ width: 120, height: 120 }} />
```

**Flutter**:
```yaml
# pubspec.yaml
dependencies:
  lottie: ^3.0.0
```
```dart
Lottie.asset('assets/animations/success.json', width: 120, height: 120, repeat: false)
```

### 12D.3 Lottie 使用场景与推荐动画

| UI 场景 | Lottie 动画类型 | LottieFiles 搜索词 | 时长 | 循环 |
|---------|---------------|-------------------|------|------|
| **加载等待** | 品牌化 Loading | `loading`, `spinner` | 1-2s | ✅ 循环 |
| **操作成功** | 打勾 + 庆祝 | `success`, `checkmark` | 1-1.5s | ❌ 单次 |
| **操作失败** | 叉号 + 抖动 | `error`, `failed` | 0.8-1s | ❌ 单次 |
| **空状态** | 人物 + 场景 | `empty`, `no data`, `not found` | 2-4s | ✅ 缓慢循环 |
| **欢迎引导** | 步骤演示 | `onboarding`, `welcome` | 3-5s | ❌ 单次 |
| **下拉刷新** | 品牌 Loading | `pull refresh`, `loading` | 1-2s | ✅ 循环 |
| **点赞/收藏** | 心跳 / 星星爆炸 | `like`, `heart`, `favorite` | 0.5-1s | ❌ 单次 |
| **发送消息** | 纸飞机飞出 | `send`, `paper plane` | 0.8s | ❌ 单次 |
| **支付成功** | 钱包 + 打勾 | `payment success` | 1.5s | ❌ 单次 |
| **404 页面** | 迷路/断线 | `404`, `lost`, `broken` | 3-5s | ✅ 缓慢循环 |
| **网络断开** | 断开连接 | `no connection`, `offline` | 2-3s | ✅ 循环 |
| **上传进度** | 文件飞入云端 | `upload`, `cloud upload` | 2-3s | ✅ 循环 |
| **删除确认** | 垃圾桶吞噬 | `delete`, `trash` | 0.8s | ❌ 单次 |
| **解锁/VIP** | 皇冠/星光 | `premium`, `crown`, `unlock` | 1.5s | ❌ 单次 |

### 12D.4 Lottie 性能与质量规范

```
□ JSON 文件 < 100KB（超过则简化动画或拆分）
□ 帧率 30fps（手机）或 60fps（桌面）
□ 不包含图片资源（纯矢量最优，避免嵌入位图）
□ 颜色可通过代码动态修改（设计时使用纯色填充）
□ 尺寸自适应（设置 viewBox，不用固定像素）
□ 首帧和末帧是"干净"状态（不要首帧就在动画中间）
□ 循环动画要"无缝衔接"（首尾帧一致）
□ 小程序中用 canvas 渲染（不用 SVG 渲染模式，性能更好）
□ React Native 中用 native 模式（不用 web 模式）
```

### 12D.5 Lottie 颜色动态化

Lottie 的一大优势是**可以在运行时修改颜色**，让同一个动画适配不同主题：

```tsx
// React — 修改 Lottie 颜色匹配品牌色
import Lottie from 'lottie-react';
import { useMemo } from 'react';

function BrandedAnimation({ animationData, brandColor = '#3b82f6' }) {
  // 将动画中的蓝色替换为品牌色
  const modified = useMemo(() => {
    const json = JSON.parse(JSON.stringify(animationData));
    // Lottie 颜色格式是 [r, g, b, a] 范围 0-1
    const [r, g, b] = hexToRgb01(brandColor);
    // 遍历替换所有颜色
    replaceColors(json, [r, g, b, 1]);
    return json;
  }, [animationData, brandColor]);

  return <Lottie animationData={modified} />;
}

function hexToRgb01(hex) {
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255];
}
```

---

## Part 12E: Modern UI Patterns — Canvas, AI, Collaboration, Smart Tables

> Patterns for the most complex modern UI scenarios, extracted from products like Figma, Notion, Miro, Google Docs, Airtable, and AI-native tools.

### 12E.1 Canvas Editor Pattern (Figma/Miro/Excalidraw style)

**Core architecture**:
```
Canvas Editor = Viewport + Objects + Tools + Panels

Viewport:
  - Infinite pan/zoom (wheel zoom, space+drag pan, pinch zoom)
  - Coordinate system: screen coords ↔ canvas coords transform
  - Rendering: HTML Canvas 2D / WebGL / SVG (choose by complexity)

Objects:
  - Each has: id, type, position(x,y), size(w,h), rotation, style, z-index
  - Selection: click to select, shift+click multi-select, drag to box-select
  - Transform: drag to move, handles to resize, rotate handle

Tools:
  - Selection tool (default), shape tools, text tool, pen tool, hand tool
  - Active tool changes cursor and click behavior

Panels:
  - Property panel (right): shows selected object's properties
  - Layer panel (left): z-order tree view
  - Toolbar (top/left): tool selection
```

**Performance rules for canvas UIs**:
```
□ Virtual rendering: only draw objects visible in viewport
□ Level-of-detail: simplify objects when zoomed out
□ Debounce: group rapid transform updates (60fps throttle)
□ Offscreen canvas: heavy rendering on worker thread
□ Spatial indexing: R-tree or quadtree for hit testing
```

### 12E.2 AI Content Generation UI Pattern

**Streaming text (ChatGPT/Claude style)**:
```
┌─────────────────────────────────────────────┐
│ User message          [avatar]              │
├─────────────────────────────────────────────┤
│ [avatar]  AI response                       │
│                                             │
│ Text streams in token by token...           │
│ With a blinking cursor ▌ at the end         │
│                                             │
│ [Stop] [Copy] [Regenerate]                  │
└─────────────────────────────────────────────┘

Key interaction patterns:
  - Token-by-token rendering (NOT character-by-character)
  - Blinking cursor at stream end (▌)
  - Auto-scroll follows new content
  - "Stop generating" button during stream
  - Code blocks render with syntax highlighting after complete
  - Markdown renders progressively
  - Copy button appears on hover over code blocks
  - Regenerate button after completion
```

**CSS for streaming cursor**:
```css
.streaming-cursor::after {
  content: '▌';
  animation: blink 1s step-end infinite;
  color: var(--accent);
}
@keyframes blink {
  50% { opacity: 0; }
}
```

**AI-generated UI (A2UI pattern)**:
```
Agent generates structured UI components → renderer displays them

Key patterns:
  - Progressive rendering: show components as they're generated
  - Skeleton → real component transition
  - Interactive components respond immediately (optimistic)
  - Error boundary: if component fails, show fallback not crash
  - Tool calls: show "Searching..." / "Analyzing..." status
```

### 12E.3 Real-time Collaboration Pattern (Google Docs/Notion/Figma style)

**Presence indicators**:
```
┌─────────────────────────────────────────────┐
│ [Doc Title]                    👤A 👤B 👤C  │ ← online user avatars
│                                             │
│ This is some text that user A│is editing    │ ← colored cursor
│                         ▲                   │
│                    [User A] ← name label    │
│                                             │
│ User B selected █this block█               │ ← colored selection
│               [User B]                      │
└─────────────────────────────────────────────┘

Design rules:
  - Each user gets a unique color (from a predefined palette, not random)
  - Cursor shows user name label (fade after 3s idle)
  - Selection highlight uses user's color at 15% opacity
  - Avatar stack in header (max 5 visible + "+N" overflow)
  - Online dot: green; away: yellow; offline: remove
```

**User color palette for collaboration** (max contrast, accessible):
```css
:root {
  --collab-user-1: #ef4444;  /* Red */
  --collab-user-2: #3b82f6;  /* Blue */
  --collab-user-3: #22c55e;  /* Green */
  --collab-user-4: #f59e0b;  /* Amber */
  --collab-user-5: #8b5cf6;  /* Violet */
  --collab-user-6: #ec4899;  /* Pink */
  --collab-user-7: #14b8a6;  /* Teal */
  --collab-user-8: #f97316;  /* Orange */
}
```

**Conflict resolution UI**:
```
Local edit → send to server → if conflict:
  Option A: Last-writer-wins (real-time docs, most common)
  Option B: Show conflict dialog (Git-style, for structured data)

NEVER silently discard user input. Always show what happened.
```

### 12E.4 Smart Table / Database View Pattern (Airtable/Notion style)

```
┌──────────────────────────────────────────────────────────┐
│ [🔍 Filter] [↕ Sort] [👁 Hide] [+ New Column] [⚙ View] │
├──────┬──────────────┬──────────┬─────────┬──────────────┤
│ ☐    │ Name ↕       │ Status ↕ │ Date    │ Assignee     │
├──────┼──────────────┼──────────┼─────────┼──────────────┤
│ ☐    │ Task Alpha   │ 🟢 Done  │ Apr 11  │ 👤 Alice     │
│ ☐    │ Task Beta    │ 🟡 In    │ Apr 12  │ 👤 Bob       │
│ ☐    │ Task Gamma   │ 🔴 Block │ Apr 13  │ 👤 Carol     │
├──────┼──────────────┼──────────┼─────────┼──────────────┤
│ + New Row                                                │
└──────────────────────────────────────────────────────────┘

Key interactions:
  - Click cell → inline edit (no modal, no page navigation)
  - Click column header → sort ascending/descending
  - Drag column border → resize column
  - Drag row handle → reorder rows
  - Checkbox column → batch select + bulk actions appear
  - Status column → dropdown with color-coded options
  - Date column → date picker popup
  - Assignee column → user search dropdown
  - Right-click row → context menu (duplicate, delete, move)
  - Cmd+Z → undo last edit

Performance for large datasets:
  □ Virtual scrolling (only render visible rows + buffer)
  □ Sticky header (stays visible during scroll)
  □ Column virtualization (for 50+ columns)
  □ Debounced search/filter (300ms after typing stops)
  □ Optimistic updates (show change → sync background)
```

### 12E.5 Document Editor Pattern (Notion/Google Docs style)

**Block-based editing**:
```
Every piece of content is a "block":
  - Text block (paragraph, heading 1-6)
  - List block (bullet, numbered, toggle, checklist)
  - Media block (image, video, embed, file)
  - Data block (table, database, chart)
  - Code block (with language selector + syntax highlight)
  - Divider block
  - Callout block (info, warning, error)

Block interactions:
  - Drag handle (⠿) on left → reorder blocks
  - "/" command → insert new block type (slash menu)
  - "+" button between blocks → insert here
  - Block toolbar on hover → transform, duplicate, delete, move
  - Select multiple blocks → bulk operations
  - Indent/outdent with Tab/Shift+Tab
  - Turn into → convert block type (text → heading, list → checklist)
```

**Slash command menu**:
```
Type "/" anywhere → floating menu appears:

  📝 Text
  ── Heading 1
  ── Heading 2
  ── Heading 3
  📋 To-do list
  • Bulleted list
  1. Numbered list
  ▶ Toggle list
  ── Divider
  " Quote
  ! Callout
  💻 Code
  📷 Image
  📊 Table
  🔗 Embed

Fuzzy search: type "/cod" → highlights "Code"
Keyboard: arrow keys to navigate, Enter to select, Esc to close
```

---

## Part 12F: 3D Interaction, Virtual Reality & Spatial UI

> Patterns for 3D product viewers, virtual house tours, AR try-on, WebXR, and spatial interfaces.
> Tech: Three.js, React Three Fiber (R3F), A-Frame, Babylon.js, Model Viewer.

### 12F.1 3D Interaction Scenarios & Tech Selection

| Scenario | Complexity | Recommended Tech | Why |
|----------|-----------|-----------------|-----|
| **3D 产品展示** (旋转/缩放) | Low | `<model-viewer>` | Google Web Component, zero code, accessible |
| **三维看房/全景** | Medium | A-Frame or Pannellum | 360 panorama optimized, VR-ready |
| **三维看房 (可漫游)** | High | Three.js / R3F | Full camera control, floor plan navigation |
| **AR 试穿/试戴** | High | WebXR + R3F | Camera access + 3D overlay |
| **数据可视化 3D** | Medium | R3F + Drei | React integration, declarative 3D |
| **虚拟展厅/展览** | High | Three.js / Babylon.js | Large scene management, PBR materials |
| **地图 3D 建筑** | Medium | Mapbox GL + 3D | GIS + 3D buildings + POI |
| **游戏化交互** | High | Babylon.js or PlayCanvas | Physics, advanced rendering |

### 12F.2 3D Product Viewer (最常用 — 电商/产品页)

**最简方案：Google `<model-viewer>`**
```bash
npm i @google/model-viewer
```
```html
<!-- 零代码 3D 产品展示：旋转、缩放、AR -->
<model-viewer
  src="/models/product.glb"
  alt="Product 3D view"
  camera-controls
  auto-rotate
  ar
  shadow-intensity="1"
  environment-image="neutral"
  style="width: 100%; height: 400px; background: var(--bg-elevated);"
>
  <!-- 加载占位 -->
  <div slot="poster" class="skeleton-image" style="width:100%;height:100%;"></div>
  <!-- AR 按钮 -->
  <button slot="ar-button" class="btn-primary">在现实中查看</button>
</model-viewer>
```

**UI 设计规范**：
```
3D Viewer Container:
  □ 背景色用 --bg-elevated（微妙区分页面背景）
  □ 圆角与卡片统一（--radius-standard）
  □ 阴影用 Level 1（不喧宾夺主）
  □ 加载时显示骨架屏 → 模型加载后淡入
  □ 底部显示手势提示："拖拽旋转 · 双指缩放"
  □ 移动端检测 AR 能力 → 显示"AR 查看"按钮

Controls:
  □ 旋转：单指/鼠标拖拽
  □ 缩放：双指捏合/滚轮
  □ 平移：双指拖拽/右键拖拽
  □ 重置：双击回到初始视角
  □ 自动旋转：idle 5s 后启动，触摸后停止
```

### 12F.3 Virtual House Tour (三维看房)

**方案 A：全景照片看房（720 度全景）**
```
技术：Pannellum / A-Frame / Photo-Sphere-Viewer
输入：360 全景照片（Insta360、Ricoh Theta 等设备拍摄）
体验：驻足观察 → 点击热点 → 切换房间

UI 要素：
  ┌─────────────────────────────────────────┐
  │ [返回]  客厅 (1/5)           [全屏] [VR]│ ← 顶部导航
  │                                         │
  │         ← 360 全景画面 →                │
  │              ○ 热点：厨房               │ ← 可点击热点
  │              ○ 热点：卧室               │
  │                                         │
  │ [客厅] [厨房] [卧室] [卫浴] [阳台]      │ ← 房间切换
  │ ─────●──────────────────────            │ ← 楼层/进度
  └─────────────────────────────────────────┘
```

**方案 B：可漫游 3D 看房**
```
技术：Three.js + R3F
输入：3D 建模文件（glTF/FBX）或 LiDAR 扫描（Matterport 格式）
体验：WASD 或点击地面移动 → 自由漫游

UI 交互层（HTML Overlay on 3D Canvas）：
  ┌─────────────────────────────────────────┐
  │ [返回]     楼层切换 [1F] [2F]     [🔍]  │
  │                                         │
  │         ← 3D 场景 →                     │
  │                                         │
  │                          [📏 测量]       │ ← 工具面板
  │                          [📷 截图]       │
  │                          [☀️ 日照]       │
  │                                         │
  │ ┌──────────┐                            │
  │ │  小地图   │  面积：89.3㎡              │ ← 缩略平面图
  │ │  ● 你在这 │  朝向：南                  │
  │ └──────────┘                            │
  └─────────────────────────────────────────┘
```

**3D 看房性能规范**：
```
□ 模型 < 10MB（使用 Draco/Meshopt 压缩 glTF）
□ 纹理用 KTX2/Basis 压缩（比 PNG 小 75%）
□ LOD（Level of Detail）：远处用低精度模型
□ 分步加载：先加载当前房间 → 预加载相邻房间
□ 首帧渲染 < 3s（显示加载进度条 0-100%）
□ 60fps 在中端手机（降级策略：关闭阴影/反射）
□ 触控手势流畅（惯性阻尼，不突然停止）
```

### 12F.4 AR / 虚拟现实 UI 规范

```
AR 模式设计规则：
  □ 半透明 UI 覆盖层（不遮挡现实世界）
  □ 按钮放底部（拇指可达区域）
  □ 文字用白色 + 深色投影（在任意背景上可读）
  □ 最小触控目标 56px（AR 中精度降低）
  □ 提供"退出 AR"按钮（始终可见）
  □ 引导提示："缓慢移动设备扫描地面"

VR 模式设计规则：
  □ UI 面板固定在世界空间（不跟随头部转动）
  □ UI 距离眼睛 1-2 米（避免对焦疲劳）
  □ 字号 ≥ 24px（VR 中分辨率有效降低）
  □ 避免纯白背景（VR 中刺眼）
  □ 按钮间距 ≥ 20px（控制器精度有限）
  □ 提供舒适度选项（传送 vs 平滑移动）
```

### 12F.5 3D 技术栈 Quick Reference

```bash
# 产品展示（最简）
npm i @google/model-viewer

# React 3D（最灵活）
npm i three @react-three/fiber @react-three/drei

# 全景看房
npm i pannellum   # 或 npm i aframe

# WebXR (AR/VR)
npm i @react-three/xr

# 3D 模型压缩
npx gltf-transform optimize input.glb output.glb --compress draco

# 3D 物理（碰撞、重力）
npm i @react-three/rapier
```

---

## Part 12G: Knowledge Graph Visualization UI

> Patterns for graph/network visualization, entity relationship, mind maps, and knowledge exploration interfaces.
> Tech: D3.js, Cytoscape.js, vis-network, G6/Graphin, React Flow, Sigma.js.

### 12G.1 Knowledge Graph Scenarios & Tech Selection

| Scenario | Node Count | Recommended Tech | Why |
|----------|-----------|-----------------|-----|
| **关系图谱** (人物/企业) | < 500 | G6 / Graphin (AntV) | 中文生态最佳，交互丰富 |
| **知识图谱浏览** | < 1,000 | Cytoscape.js | 学术标准，算法丰富 |
| **大规模图谱** | > 10,000 | Sigma.js (WebGL) | GPU 渲染，百万节点 |
| **流程/工作流** | < 200 | React Flow | React 原生，拖拽编排 |
| **思维导图** | < 500 | @antv/g6 或自建 | 树状布局原生支持 |
| **数据血缘** | < 1,000 | React Flow / G6 | 有向图 + 层次布局 |
| **社交网络** | < 5,000 | vis-network | 力导向布局，简单易用 |
| **D3 自定义** | Any | D3.js | 完全控制，学习曲线高 |

### 12G.2 Knowledge Graph UI Layout

```
┌─────────────────────────────────────────────────────────┐
│ [🔍 搜索实体]              [布局▾] [筛选▾] [导出]  [⛶] │ ← 工具栏
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ 图例     │          ← 图谱画布 →                        │
│ ● 人物   │                                              │
│ ● 企业   │     ┌──┐     ┌──┐                           │
│ ● 事件   │     │A │────│B │                            │
│ ● 地点   │     └──┘╲   └──┘                            │
│          │          ╲  ┌──┐                              │
│ 关系类型  │           ╲│C │                              │
│ ── 任职  │            └──┘                              │
│ ── 投资  │                                              │
│ ·· 关联  │                                              │
│          │                                              │
├──────────┤                                              │
│ 详情面板  │                                              │
│          │                                              │
│ [实体名]  │   ← 点击节点后显示                           │
│ 类型：人物│                                              │
│ 关系：15  │                                              │
│ [展开]    │                                              │
└──────────┴──────────────────────────────────────────────┘
```

### 12G.3 Graph Interaction Patterns

```
Node (节点) 交互：
  单击          → 选中，高亮关联边，显示详情面板
  双击          → 展开子图（加载关联节点）
  右键          → 上下文菜单（展开/收起/隐藏/定位/详情）
  拖拽          → 移动节点位置（其他节点力导向重排）
  Hover         → 显示 tooltip（名称 + 类型 + 关系数）

Edge (边) 交互：
  单击          → 高亮边 + 两端节点，显示关系详情
  Hover         → 显示关系类型标签

Canvas (画布) 交互：
  拖拽空白      → 平移画布
  滚轮          → 缩放画布
  框选          → 批量选中节点
  双击空白      → 重置视图（fit-to-screen）

键盘：
  Ctrl+F        → 搜索节点
  Delete        → 隐藏选中节点
  Ctrl+Z        → 撤销操作
  +/-           → 缩放
```

### 12G.4 Graph Visual Encoding Rules

```
节点大小 = f(重要性)
  重要性高 → 节点大（40-60px）
  重要性低 → 节点小（16-24px）
  公式：size = Math.max(16, Math.min(60, baseSize + connections * 2))

节点颜色 = f(类型)
  每种实体类型一个颜色（从设计系统调色板取）
  最多 8 种颜色（超过则归入"其他"灰色）
  颜色方案来自 DESIGN.md Section 2 的调色板

边粗细 = f(关系强度)
  强关系 → 粗边（3-4px）
  弱关系 → 细边（1px）
  推测/不确定 → 虚线

边颜色 = f(关系类型)
  同类关系同色，但比节点颜色浅 30%
  或统一灰色（当边类型太多时）

标签：
  节点标签 → 始终显示（缩放过小时隐藏）
  边标签   → hover 时显示（避免文字过密）
  字号 = max(10px, 14px * zoomLevel)（随缩放适配）
```

### 12G.5 Graph Performance Rules

```
□ < 500 节点：Canvas 2D 渲染足够
□ 500-5,000 节点：WebGL 渲染（Sigma.js / G6 GPU 模式）
□ > 5,000 节点：分层加载 + 聚类折叠 + WebGL
□ 布局计算放 Web Worker（不阻塞主线程）
□ 力导向布局限制迭代次数（300 次足够稳定）
□ 缩放层级切换：宏观（聚类）→ 中观（节点）→ 微观（标签+详情）
□ 鱼眼放大：焦点区域放大，周边压缩（探索大图的利器）
```

### 12G.6 Tech Quick Reference

```bash
# AntV G6（中文生态首选）
npm i @antv/g6

# React Flow（流程编排/工作流）
npm i reactflow

# Cytoscape.js（学术/复杂分析）
npm i cytoscape

# vis-network（快速社交图谱）
npm i vis-network

# Sigma.js（超大规模 WebGL）
npm i sigma graphology

# D3 Force Layout（完全自定义）
npm i d3-force d3-selection
```

---

## Part 12H: Intelligent Search UI/UX

> Patterns for search experiences: instant search, faceted filters, AI-powered semantic search,
> search suggestions, search results, and no-results states.
> Reference brands: Algolia, Elasticsearch, Google, Notion, Linear, Raycast, Spotlight.

### 12H.1 Search Complexity Levels

| Level | Type | Example | UI Pattern |
|-------|------|---------|-----------|
| **L1** | Simple keyword | Blog search | Input + results list |
| **L2** | Filter + sort | E-commerce | Search bar + faceted sidebar + sort dropdown |
| **L3** | Instant/typeahead | Spotlight/Raycast | Floating palette + instant results |
| **L4** | AI semantic | "Find meetings about budget" | NLP query + smart results + intent chips |
| **L5** | Conversational | ChatGPT + search | Chat input → structured results + follow-up |

### 12H.2 Search UI Anatomy

**Level 2-3: Standard Search Page**
```
┌─────────────────────────────────────────────────────────┐
│ ┌──────────────────────────────────────────────────┐    │
│ │ 🔍 Search products...               [Filters] [×]│    │ ← 搜索栏
│ └──────────────────────────────────────────────────┘    │
│                                                         │
│ Recent: [iPhone case] [USB-C cable] [wireless mouse]    │ ← 最近搜索
│ Trending: [summer sale] [new arrivals]                  │ ← 热门搜索
│                                                         │
│ ┌─── After typing ───────────────────────────────────┐  │
│ │ Suggestions:                                       │  │
│ │   🔍 wireless charger                             │  │ ← 搜索建议
│ │   🔍 wireless earbuds                             │  │
│ │   🔍 wireless keyboard                            │  │
│ │ Products:                                          │  │
│ │   📦 Anker Wireless Charger — $29.99              │  │ ← 即时结果
│ │   📦 MagSafe Charger — $39.00                     │  │
│ │ Categories:                                        │  │
│ │   📁 Electronics > Chargers                        │  │ ← 分类匹配
│ └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Level 3: Command Palette (Raycast/Linear/Notion style)**
```
┌──────────────────────────────────────────────┐
│ 🔍 Type a command or search...               │
├──────────────────────────────────────────────┤
│ ACTIONS                                      │
│   ▶ Create new document          ⌘N          │
│   ▶ Open settings                ⌘,          │
│ RECENT                                       │
│   📄 Q4 Budget Report           2h ago       │
│   📊 Analytics Dashboard        yesterday    │
│ PAGES                                        │
│   📄 Getting Started Guide                   │
│   📄 API Documentation                       │
└──────────────────────────────────────────────┘

交互规则：
  - Cmd/Ctrl+K 全局唤起（任何页面）
  - 输入即搜索（debounce 150ms）
  - 箭头键导航，Enter 执行，Esc 关闭
  - 模糊匹配 + 高亮匹配文字
  - 分组展示（Actions / Pages / People）
  - 记忆最近使用（下次优先显示）
```

**Level 4: AI-Powered Search**
```
┌──────────────────────────────────────────────────────┐
│ 🔍 Find all meetings about budget in the last month  │ ← 自然语言查询
├──────────────────────────────────────────────────────┤
│ AI understood: meetings + topic:budget + time:30d    │ ← 意图解析展示
│ ┌──────────────────────────────────────────────────┐ │
│ │ 🏷️ [meetings] [budget] [last 30 days] [× clear] │ │ ← 可编辑意图标签
│ └──────────────────────────────────────────────────┘ │
│                                                      │
│ Found 12 results                          [Relevance▾]│
│                                                      │
│ 📅 Q4 Budget Review — Oct 15             98% match   │ ← 相关度评分
│    "...discussed the quarterly budget allocation..."  │ ← 高亮摘要
│                                                      │
│ 📅 Team Budget Planning — Oct 8          94% match   │
│    "...team budget for next quarter..."              │
│                                                      │
│ 💡 Did you mean: [budget approval] [expense reports]  │ ← AI 建议扩展
└──────────────────────────────────────────────────────┘
```

### 12H.3 Search Interaction Patterns

```
INPUT BEHAVIOR:
  空状态（未输入）     → 显示：最近搜索 + 热门搜索 + 快捷操作
  输入 1-2 字符       → 显示：搜索建议（基于前缀匹配）
  输入 3+ 字符        → 显示：即时结果（debounce 150-300ms）
  输入中 + 等待       → 显示：加载骨架（非 spinner）
  清空输入            → 回到空状态
  按 Esc              → 关闭搜索面板

RESULTS BEHAVIOR:
  有结果              → 按相关度排序，高亮匹配文字
  无结果              → 友好提示 + 建议（拼写修正、相关词、放宽条件）
  结果过多            → 显示总数 + 建议添加筛选条件
  加载中              → 骨架屏 placeholder（不清除旧结果）

HIGHLIGHT RULES:
  匹配文字加粗        → <mark> 或 font-weight: 600
  匹配文字颜色        → var(--accent) 或 var(--text-primary)
  非匹配文字          → var(--text-secondary)
```

### 12H.4 Search Results Design Patterns

```
List View（默认）:
  ┌──────────────────────────────────────────┐
  │ 📄 Title (matched text bolded)           │
  │ Description snippet with ...highlight... │
  │ Category · Date · Author                 │
  └──────────────────────────────────────────┘

Grid View（图片类）:
  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
  │ img  │ │ img  │ │ img  │ │ img  │
  │ Title│ │ Title│ │ Title│ │ Title│
  └──────┘ └──────┘ └──────┘ └──────┘

Grouped View（分类）:
  DOCUMENTS (5)
    📄 Result 1
    📄 Result 2
  PEOPLE (3)
    👤 Result 3
  CHANNELS (2)
    # Result 4
```

### 12H.5 No-Results State Design

```
永远不要只显示 "No results found."

标准无结果页面：
  ┌──────────────────────────────────────┐
  │                                      │
  │        [🔍 插图或 Lottie]            │
  │                                      │
  │    No results for "xyzabc"           │
  │                                      │
  │    Suggestions:                      │
  │    • Check your spelling             │
  │    • Try more general keywords       │
  │    • Remove some filters             │
  │                                      │
  │    Did you mean: [xyz] [abc]         │ ← 拼写纠正
  │                                      │
  │    Popular searches:                 │ ← 热门推荐
  │    [trending 1] [trending 2]         │
  │                                      │
  └──────────────────────────────────────┘
```

### 12H.6 Faceted Filter Design

```
┌─ Filters ────────────────┐
│                          │
│ Category                 │
│ ☑ Electronics (234)      │ ← 带数量的多选
│ ☐ Books (56)             │
│ ☑ Accessories (128)      │
│ [Show more...]           │
│                          │
│ Price Range              │
│ [$10] ───●───●─── [$500] │ ← 范围滑块
│                          │
│ Rating                   │
│ ★★★★☆ & up (89)         │ ← 星级筛选
│ ★★★☆☆ & up (156)        │
│                          │
│ Color                    │
│ ⬤ ⬤ ⬤ ⬤ ⬤ ⬤           │ ← 色板选择
│                          │
│ [Clear all filters]      │
└──────────────────────────┘

交互规则：
  □ 选择筛选后即时刷新结果（不需要点"应用"）
  □ 每个筛选项显示匹配数量
  □ 已选筛选显示为可删除标签（上方汇总）
  □ "Clear all" 一键清除所有筛选
  □ 移动端：筛选收起为底部抽屉
  □ URL 同步筛选状态（可分享/书签）
```

### 12H.7 Search Performance Standards

```
□ 搜索建议响应 < 100ms（本地缓存 + 服务端预测）
□ 搜索结果响应 < 300ms（含网络延迟）
□ 输入 debounce 150-300ms（避免每个字符都请求）
□ 骨架屏保留旧结果（新结果渐入替换，不闪烁）
□ 搜索词高亮用 <mark> 标签（可被屏幕阅读器识别）
□ 键盘完全可用（Tab/Arrow/Enter/Esc）
□ 搜索历史存 localStorage（最近 20 条，可清除）
□ 热门搜索缓存 5 分钟（减少 API 调用）
```

### 12H.8 Tech Quick Reference

```bash
# 客户端即时搜索（小数据集 < 10,000 条）
npm i fuse.js           # 模糊搜索
npm i minisearch        # 轻量全文搜索

# 搜索 UI 组件
npm i @algolia/autocomplete-js    # Algolia 搜索 UI
npm i cmdk              # Command palette（shadcn 用它）
npm i kbar              # 另一个 command palette

# 服务端搜索引擎
# Elasticsearch, Meilisearch, Typesense (self-hosted)
# Algolia (SaaS)

# AI 语义搜索
# OpenAI Embeddings + pgvector
# Pinecone / Weaviate / Qdrant (vector DB)
```

---

## Part 12I: Learn from Any Website or Screenshot — Design DNA Extraction

> When the user says "I like this website" or shares a screenshot, extract its design DNA and apply it.

### 12I.1 Input Methods & What AI Can Do

| User Provides | AI Capability | How |
|---------------|--------------|-----|
| **Website URL** | Read live CSS/HTML → extract all tokens | Use WebFetch to read page, or Claude in Chrome to inspect |
| **Screenshot (image)** | Analyze visual: colors, type style, spacing, shadows, layout | Multimodal image understanding (built-in) |
| **Multiple screenshots** | Compare patterns across pages for consistency | Batch analysis |
| **"I like Notion's style"** | Look up brand in DesignDNA's 58-brand collection | Direct reference from Part 2 archetypes |

### 12I.2 Workflow: URL → Design DNA

When the user provides a URL:

```
Step 1: ACCESS
  - Use WebFetch or browser tools to load the page
  - Read HTML structure and CSS stylesheets

Step 2: EXTRACT (automated)
  Colors:
    - Extract all color values from CSS (hex, rgb, rgba, hsl, oklch)
    - Group by frequency → identify primary, secondary, accent, text, bg
    - Check: warm or cool neutrals? How many accent colors?

  Typography:
    - Extract font-family declarations → identify primary/secondary/mono
    - Extract font-size scale → build hierarchy table
    - Extract font-weight usage → identify weight system
    - Extract letter-spacing patterns → check if scaling with size
    - Extract line-height patterns → check compression at scale

  Spacing:
    - Extract padding/margin/gap → check if on 8px grid
    - Identify spacing scale

  Shadows:
    - Extract all box-shadow values → identify elevation system
    - Analyze: single-layer or multi-layer? warm or cool tinted?

  Radius:
    - Extract border-radius → identify systematic scale or random

  Components:
    - Identify button styles (primary, secondary, ghost)
    - Identify card patterns
    - Identify navigation patterns

Step 3: MATCH
  Compare extracted DNA against 10 archetypes (Part 2):
  "This website most closely matches [Archetype] — similar to [Brand]"

Step 4: REPORT
  Output a structured analysis to the user:

  ## Design DNA Analysis: [URL]

  ### Archetype Match: [Name] (like [Brand])

  ### Extracted Tokens
  | Category | Values Found |
  |----------|-------------|
  | Primary color | #xxx |
  | Text color | #xxx (warm/cool) |
  | ... | ... |

  ### What makes this design effective
  1. [Observation about color usage]
  2. [Observation about typography]
  3. [Observation about spacing/layout]

  ### Patterns worth adopting
  - [Specific technique with CSS example]

  ### Generated DESIGN.md
  [Optional: full 9-section DESIGN.md if user wants to adopt this style]

Step 5: SAVE (if user approves)
  Save the analysis to designdna/experience/references/[site-name].md
  for future cross-project reference.
```

### 12I.3 Workflow: Screenshot → Design DNA

When the user provides a screenshot:

```
Step 1: OBSERVE
  Look at the image and identify:
  - Overall color temperature (warm/cool/neutral)
  - Dominant background color (light/dark/colored)
  - Accent color and where it's used
  - Typography style (serif/sans/mono, weight range, density)
  - Spacing density (airy/standard/dense)
  - Shadow treatment (none/subtle/heavy)
  - Corner radius treatment (sharp/rounded/pill)
  - Layout pattern (centered/sidebar/asymmetric)

Step 2: MATCH
  Map observations to the closest archetype:

  Quick matching heuristics from visual observation:
    Dark + monospace + ring shadows  → Dark Instrument
    White + black type + minimal     → Precision Monochrome
    Warm tones + serif headings      → Warm Editorial
    Gradients + light weights        → Vibrant Gradient/Enterprise Trust
    Photography-dominant + minimal   → Premium Automotive
    Bright colors + rounded + icons  → Friendly Warm
    Dark + content-first + pills     → Content Stage

Step 3: DESCRIBE
  Tell the user what you see and which archetype matches:

  "From this screenshot, I can see:
   - Dark background (#0a0a0b) with a single green accent
   - Sans-serif type, likely Inter or similar, medium weight
   - Tight letter-spacing on headings
   - Multi-layer ring shadows on cards
   - 8px radius corners
   → This matches the **Dark Instrument** archetype (like Linear/Raycast)

   Want me to generate a DESIGN.md based on this style?"

Step 4: GENERATE
  Create a DESIGN.md using:
  - Approximate color values from visual analysis
  - Matched archetype's typography system as baseline
  - Archetype's shadow/spacing/radius systems
```

### 12I.4 Practical Usage Prompts

```
"Look at https://example.com and tell me what makes its design good.
 Extract the design tokens and generate a DESIGN.md for my project."

"Here's a screenshot of an app I like [attached image].
 Analyze its design and tell me which archetype it matches."

"I want my project to look like Linear but with warmer colors.
 Generate a DESIGN.md that combines Linear's layout precision
 with Claude's warm color palette."

"Compare these two screenshots and tell me which has better
 typography and why."
```

### 12I.5 Experience Library Growth

Over time, the `designdna/experience/references/` directory grows into a curated collection:

```
designdna/experience/
├── references/
│   ├── stripe-checkout-flow.md     ← design DNA + what works
│   ├── notion-block-editor.md      ← design DNA + interaction patterns
│   ├── linear-dashboard.md         ← design DNA + dark UI techniques
│   └── client-project-xyz.md       ← screenshot analysis + decisions
└── interactions/
    └── [project interaction logs from Part 12C]
```

This becomes a **personal design knowledge base** that improves every recommendation over time.

---

## Part 12J: Map & Location Services UI/UX

> Patterns for map interfaces, location selection, route navigation, geofencing,
> and location-based services (LBS).
> Reference products: Google Maps, Apple Maps, Uber, Didi, Meituan, Airbnb, Amap.

### 12J.1 Map Scenarios & Tech Selection

| Scenario | Recommended Map SDK | Why |
|----------|-------------------|-----|
| **Web (Global)** | Mapbox GL JS | Beautiful custom styling, 3D buildings, globe view |
| **Web (China)** | AMap (高德地图) JS API | China compliance, POI accuracy, Chinese address |
| **Web (Alternative)** | Leaflet + tiles | Lightweight, open-source, no vendor lock |
| **Web (Google)** | Google Maps JS API | Largest POI database, Street View |
| **React Native** | react-native-maps | Native rendering, cross-platform |
| **Flutter** | google_maps_flutter | Official Google Maps plugin |
| **Mini Program (WeChat)** | wx.map component | Native map component, built-in |
| **Mini Program (Alipay)** | my.map component | Amap-based, built-in |

### 12J.2 Map UI Layout Patterns

**Pattern A: Full-Screen Map (Uber/Didi/Navigation)**
```
┌─────────────────────────────────────────────┐
│ [←]  Where to?                    [🎤]      │ ← 搜索栏浮在地图上
│                                             │
│              ← MAP FULL SCREEN →            │
│                                             │
│                    📍                        │ ← 中心定位点
│                                             │
│                                        [◎]  │ ← 定位按钮（右下）
│                                        [+]  │ ← 缩放按钮
│                                        [-]  │
│ ┌─────────────────────────────────────────┐ │
│ │ ▔▔▔▔▔ (drag handle)                    │ │ ← 底部抽屉
│ │ 📍 Current Location                     │ │
│ │ ★ Home — 123 Main St                   │ │
│ │ ★ Work — 456 Office Ave                │ │
│ │ 🕐 Recently: Coffee Shop               │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘

底部抽屉交互：
  - 向上滑动展开（半屏 → 全屏）
  - 向下滑动收起（全屏 → 半屏 → 最小化）
  - 3 个停靠位置：peek(120px) / half(50%) / full(90%)
```

**Pattern B: Map + List Split (Airbnb/房产/外卖)**
```
桌面端（左右分屏）：
┌──────────────────────┬──────────────────────┐
│                      │                      │
│    RESULT LIST       │      MAP             │
│                      │                      │
│  ┌────────────────┐  │    📍 A              │
│  │ A. Result 1    │  │          📍 B        │
│  │ ⭐4.8 · $120  │  │    📍 C              │
│  └────────────────┘  │              📍 D    │
│  ┌────────────────┐  │                      │
│  │ B. Result 2    │  │                      │
│  │ ⭐4.5 · $95   │  │                      │
│  └────────────────┘  │                      │
│                      │                      │
└──────────────────────┴──────────────────────┘

交互联动：
  - hover 列表项 → 地图上对应标记高亮放大
  - 点击地图标记 → 列表滚动到对应项
  - 拖动地图 → 列表只显示当前视野内的结果
  - 列表筛选 → 地图标记同步增减

移动端（切换模式）：
  [列表] [地图] ← 顶部切换按钮
  或底部抽屉覆盖在地图上（Airbnb 模式）
```

**Pattern C: Route Display (导航/物流追踪)**
```
┌─────────────────────────────────────────────┐
│ 📍 Starting Point                           │
│ 📍 Destination              [Swap ⇅]       │
│ [Car] [Transit] [Walk] [Bike]               │ ← 出行方式
├─────────────────────────────────────────────┤
│                                             │
│   A ●━━━━━━━━━━━━━━━━━━━● B               │ ← 路线在地图上
│                                             │
│                                             │
├─────────────────────────────────────────────┤
│ Route 1: 25 min · 12 km          [Go]       │ ← 路线选项
│ Route 2: 32 min · 15 km (toll)   [Go]       │
│ Route 3: 40 min · 11 km          [Go]       │
└─────────────────────────────────────────────┘

路线样式：
  - 主路线：品牌色，4px 宽，100% 透明
  - 备选路线：灰色，3px 宽，50% 透明
  - 拥堵段：红色叠加
  - 已走过的段：颜色变浅
  - 动态车标：沿路线平滑移动
```

### 12J.3 Map Markers (标记点) Design

```
Standard Markers:
  ● 圆点标记（默认，最小视觉干扰）
  📍 Pin 标记（目的地，需要强调）
  💲 带内容标记（价格/评分，Airbnb 风格）
  🔢 带编号标记（路线节点，A→B→C）
  👤 用户头像标记（社交/协作场景）

标记状态：
  Default   → 品牌色，标准大小
  Hover     → 放大 1.2x + 弹出信息卡
  Selected  → 放大 1.3x + 颜色加深 + 信息卡展开
  Cluster   → 圆形 + 数字（"12+"） → 点击展开

Airbnb 价格标记样式：
  ┌─────────┐
  │ ¥128/晚  │ ← 白色背景 + 圆角 + 阴影
  └────┬────┘
       ▼      ← 底部三角指向位置

  Hover: 背景变深色，文字变白
  Selected: 黑色背景，白色文字，放大
```

### 12J.4 Location Picker (位置选择器)

```
场景：用户需要选择/确认一个地址

┌─────────────────────────────────────────────┐
│ [← 返回]  选择位置                           │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ 🔍 搜索地址、小区、商圈...              │ │ ← 搜索框
│ └─────────────────────────────────────────┘ │
│                                             │
│              ← MAP →                        │
│                                             │
│                 📍                           │ ← 中心 Pin（固定不动）
│                                             │ ← 地图在 Pin 下方移动
│                                        [◎]  │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ 📍 北京市朝阳区xxx街道xxx号              │ │ ← 逆地理编码结果
│ │    附近：xxx 大厦 (50m)                  │ │ ← 附近 POI
│ │                                         │ │
│ │         [确认位置]                       │ │ ← 确认按钮
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘

交互规则：
  - 地图拖动时中心 Pin 保持不动（视觉锚定）
  - 地图拖动停止后 300ms → 发起逆地理编码
  - 逆地理编码时显示 loading（Pin 下方小 spinner）
  - 搜索框输入 → 下拉搜索建议（地址 + POI）
  - 点击搜索建议 → 地图飞到该位置
  - "定位"按钮 → 回到用户当前位置
```

### 12J.5 Map Overlay UI Design Rules

```
浮在地图上的 UI 元素必须遵守：
  □ 半透明或磨砂背景（不完全遮挡地图）
     background: rgba(255,255,255,0.95);  /* 亮色 */
     backdrop-filter: blur(12px);          /* 磨砂 */
  □ 投影加强层次感（区分 UI 层和地图层）
     box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  □ 圆角统一（与整体设计系统一致）
  □ 按钮放右下角（不遮挡地图中心信息）
  □ 定位按钮用明确的图标（◎ 或 crosshair）
  □ 缩放按钮可选（移动端靠双指手势，可省略）
  □ 安全距离：浮动 UI 距离屏幕边缘 ≥ 16px
  □ 底部抽屉不超过屏幕 50%（peek 状态），留足地图可视区

地图内的文字必须遵守：
  □ 标记标签用白底+阴影（确保在任何瓦片上可读）
  □ 信息窗口（InfoWindow）用卡片设计系统（DESIGN.md）
  □ 距离/时间标注用半透明 pill badge
  □ 路线标注不超过 3 种颜色
```

### 12J.6 Map Accessibility & Performance

```
无障碍：
  □ 地图区域有 aria-label="Interactive map showing [context]"
  □ 标记点可键盘聚焦（Tab 顺序）
  □ 信息窗口可用 Esc 关闭
  □ 提供列表视图替代方案（不依赖纯地图浏览）

性能：
  □ 地图懒加载（不在首屏时 defer 加载 SDK）
  □ 标记点 > 100 个时使用聚类（clustering）
  □ 标记点 > 1,000 个时使用 Canvas/WebGL 渲染
  □ 自定义标记用 SVG（不用 PNG，更清晰更小）
  □ 地图交互用 passive event listeners
  □ 移动端地图使用 will-change: transform 硬件加速

中国合规：
  □ 使用合规地图 SDK（高德/百度/腾讯地图）
  □ 坐标系：GCJ-02（中国偏移坐标），不用 WGS-84
  □ 地图数据不出境存储
  □ 敏感区域标注遵守国家要求
```

### 12J.7 Map Tech Quick Reference

```bash
# Web — Mapbox GL JS（全球最佳视觉）
npm i mapbox-gl
npm i react-map-gl        # React 封装

# Web — 高德地图（中国项目首选）
npm i @amap/amap-jsapi-loader

# Web — Leaflet（开源轻量）
npm i leaflet
npm i react-leaflet        # React 封装

# Web — 腾讯地图
# Script 标签引入 + 腾讯位置服务 Key

# React Native
npm i react-native-maps

# Flutter
flutter pub add google_maps_flutter

# 小程序 — 内置 map 组件，无需安装
# <map latitude="..." longitude="..." markers="{{markers}}" />
```

---


{% endraw %}
