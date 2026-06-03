# DesignDNA References · Resource Integration & Tech-Stack Catalog (Parts 9–10)

> Loaded on demand from the `designdna` skill. See [SKILL.md](../SKILL.md) for the operating core.

{% raw %}

## Part 9: Design Resource Integration & Consistency Enforcement

> **Core Problem**: LLMs often produce inconsistent colors, missing icons, and ugly placeholder graphics because they lack concrete resource anchoring. This section solves that by binding every design decision to a specific, accessible resource.
>
> See `RESOURCES.md` for the complete resource catalog.

### The 5 Consistency Killers (and How to Fix Them)

| # | Problem | Root Cause | Solution |
|---|---------|-----------|----------|
| 1 | **Colors drift across pages** | Colors defined inline, not as tokens | ALL colors MUST be CSS variables or theme tokens. NEVER use inline hex values in components. |
| 2 | **Icons inconsistent** | Mixing icon sets, or using emoji/text as icons | Choose ONE icon library per project. Install via npm for offline reliability. |
| 3 | **Illustrations missing or ugly** | LLM generates placeholder text instead of real assets | Specify exact illustration source + search term in DESIGN.md. Use SVG illustrations from unDraw/Storyset. |
| 4 | **Typography breaks on different OS** | Using system fonts without fallbacks | Always specify font via Fontsource (npm install) + proper fallback stack. |
| 5 | **Components look different across pages** | Not using a component library consistently | Choose ONE component library. Import from it. Never hand-code what the library provides. |

### Consistency Enforcement Rules (MANDATORY)

**Rule C1 — One Icon Library Per Project**
```
BEFORE writing any UI code, declare the icon library:
  "This project uses [Lucide/Heroicons/Tabler/etc.]"

Then ALWAYS import from that library. NEVER:
  ❌ Mix Lucide icons with Heroicons
  ❌ Use emoji as icons (🔍 ← never this)
  ❌ Use Unicode symbols as icons (→ ← never this in UI)
  ❌ Use text characters as icons ("X" for close ← never this)

Install offline:
  npm i lucide-react          # React
  npm i @heroicons/react       # React + Tailwind
  npm i @tabler/icons-react    # React (largest set)
  npm i lucide-vue-next        # Vue
  npm i @iconify/react          # Universal (200k+ icons)

LOCAL FALLBACK (no npm needed):
  DesignDNA includes 750 pre-downloaded SVG icons in assets/icons/:
  - assets/icons/lucide/     → 436 icons, 20 categories
  - assets/icons/material/   → 314 icons, 16 categories
  - assets/ICON-INDEX.md     → searchable catalog with quick lookup table

  Copy SVGs directly into your project:
    cp designdna/assets/icons/lucide/actions/search.svg src/assets/icons/
    cp -r designdna/assets/icons/lucide/navigation/ src/assets/icons/
```

**Rule C2 — One Color Source of Truth**
```
ALL colors MUST flow from ONE source:
  Option A: DESIGN.md → CSS custom properties → components
  Option B: Component library theme (Tailwind config / Ant Design theme / etc.)

NEVER:
  ❌ Use inline color values: style={{ color: '#3b82f6' }}
  ❌ Use unnamed colors in CSS: color: #666;
  ❌ Approximate colors: "use a blue similar to..."

ALWAYS:
  ✅ color: var(--text-secondary);
  ✅ className="text-gray-600"  (Tailwind)
  ✅ Use theme tokens from chosen component library
```

**Rule C3 — Font Installation via npm (Offline-First)**
```
NEVER rely on Google Fonts CDN in production code.
ALWAYS install via Fontsource for offline reliability:

  npm i @fontsource-variable/inter
  npm i @fontsource-variable/jetbrains-mono
  npm i @fontsource/plus-jakarta-sans

Then import in your entry file:
  import '@fontsource-variable/inter';

Fallback stacks MUST include system fonts:
  font-family: 'Inter Variable', 'Inter', -apple-system,
    BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
```

**Rule C4 — Illustration Strategy (Never Leave Blank)**
```
For EVERY section that needs an illustration or image, specify:
  1. Source: which resource to use (Pexels, Huaban, GPT Image 2, unDraw, Storyset, etc.)
  2. Search terms: exact keywords to find the right asset
  3. Format: SVG for illustrations, WebP/JPEG/PNG for images
  4. Fallback: CSS gradient or pattern if image fails to load

Example in DESIGN.md:
  "Empty state illustration: unDraw 'no_data' in brand primary color #3b82f6"
  "Hero image: Pexels search 'minimal workspace laptop' → WebP 1920x1080"
  "Localized campaign asset: Huaban search '科技 蓝色 UI 背景' → JPG/PNG, verify asset license"
  "Generated product hero: GPT Image 2 prompt in skills/gpt-image-2 → WebP 1536x1024, no embedded body text"
  "User avatars: UI Faces API or DiceBear generative avatars"

For programmatic avatar generation (no network needed):
  npm i @dicebear/core @dicebear/collection
```

**Rule C5 — Component Library Discipline**
```
Choose ONE primary component library at project start.
NEVER hand-build what the library already provides.
NEVER mix component libraries on the same page.

If the library lacks a specific component:
  1. Check if a headless version exists (Radix, Headless UI)
  2. Build it using the library's design tokens
  3. Style it consistently with the library's patterns
```

### Offline Resource Checklist

For production reliability, install these locally at project initialization:

```bash
# Icons (choose ONE)
npm i lucide-react                    # or lucide-vue-next

# Fonts (choose as needed)
npm i @fontsource-variable/inter
npm i @fontsource-variable/jetbrains-mono

# Animation
npm i framer-motion                   # React
npm i @vueuse/motion                  # Vue

# Illustrations (for generative avatars/placeholders)
npm i @dicebear/core @dicebear/collection

# Component library (choose ONE, see Tech Stack Matrix below)
npm i @radix-ui/themes                # or ant-design, etc.
```

---

## Part 10: Design-Driven Tech Stack Catalog & Recommendation

> **📦 Fresh catalog (2026-05 audit):** The authoritative, regularly-updated inventory of 70+ component libraries lives in **[`designdna/components/`](./components/)** with health indicators (🟢 active / 🟡 maintenance / 🔴 deprecated), GitHub stars, last-commit dates, and migration paths:
> - Master index: [components/INDEX.md](./components/INDEX.md)
> - By ecosystem: [tencent](./components/by-ecosystem/tencent.md) · [alibaba](./components/by-ecosystem/alibaba.md) · [jd](./components/by-ecosystem/jd.md) · [google-material](./components/by-ecosystem/google-material.md) · [modern-web](./components/by-ecosystem/modern-web.md) · [miniprogram-native](./components/by-ecosystem/miniprogram-native.md)
> - By platform: [web](./components/by-platform/web.md) · [mobile](./components/by-platform/mobile.md) · [miniprogram](./components/by-platform/miniprogram.md) · [cross-platform](./components/by-platform/cross-platform.md) · [desktop](./components/by-platform/desktop.md)
> - What to avoid: [DEPRECATED.md](./components/DEPRECATED.md)
>
> **Load these files first when the user asks for a tech-stack recommendation** — they supersede any stale data in the tables below. The tables here are narrative guidance; the `components/` folder is the source of truth.
>
> **2026 audit — platform guidance:**
> - For **new iOS** projects prefer SwiftUI + Apple HIG. `material-components-ios` is archived but still usable for existing projects (migrate on your cadence).
> - For **new Flutter** projects use the SDK-bundled `package:flutter/material`. The standalone `material-components-flutter` has been consolidated into the SDK.
> - `material-web` (Lit) is in maintenance mode — safe for existing projects, evaluate alternatives (MUI / Shoelace) for greenfield.
> - For **new React + Microsoft** work use `@fluentui/react-components` v9, not the v8 Fabric branch.
> - For **WeChat MiniProgram** native use **Vant Weapp** or **TDesign MiniProgram**. Older iView Weapp / Wuss Weapp / TouchWX have been dormant 5-8 years.
> - For **multi-MP vendor** use **Taro + NutUI**. Remax stopped in 2022.
> - **Bootstrap v4** is security-only — v5.3 is the current version.
> - **Chakra v2** is still widely deployed; v3 (Panda CSS) is the modern path.

> **Scope**: This section recommends tech stacks from a **design expression** perspective — "which library best expresses this design intent?" For framework architecture, state management, build tools, and implementation patterns, defer to `frontend-patterns`, `web-development`, and `coding-standards` skills.
>
> **User Choice Protocol**:
> 1. When the user has NOT specified a tech stack → present the top 2-3 options with **design-focused** reasons, then ask "Which would you prefer?"
> 2. When the user HAS already chosen a stack → respect their choice, NEVER suggest switching. Adapt all design resource selections to match.
> 3. When the user's choice differs from recommendation → acknowledge, adapt, proceed. Design advice remains valid regardless of framework.
> 4. When another skill (e.g. `frontend-patterns`) recommends a different framework for engineering reasons → BOTH recommendations are valid. Present both perspectives, let user decide.

### 10.1 Web UI Frameworks — Complete Catalog

#### React Ecosystem

| Framework | Meta-Framework | Component Library Options | Best For |
|-----------|---------------|--------------------------|----------|
| **React** | — | Radix, shadcn/ui, Ant Design v6, Ant Design X, TDesign React, Mantine, Chakra, MUI | Interactive SPAs, complex state |
| **Next.js** | React SSR/SSG/RSC | shadcn/ui (recommended), Ant Design v6, TDesign React, Mantine | Full-stack web apps, SEO-critical |
| **Remix** | React SSR | shadcn/ui, Mantine, Chakra | Data-heavy apps, nested routing |
| **Gatsby** | React SSG | MUI, Chakra, Theme UI | Content sites, blogs, marketing |

**React Component Libraries — Full List**:

| Library | GitHub | Styling | Strength | Stars |
|---------|--------|---------|----------|-------|
| shadcn/ui | shadcn-ui/ui | Tailwind | Copy-paste, full control, best DX | 80k+ |
| Radix UI Primitives | radix-ui/primitives | Unstyled | Accessibility-first headless | 16k+ |
| Radix Themes | radix-ui/themes | Built-in | Pre-styled Radix | 5k+ |
| Ant Design | ant-design/ant-design | CSS variables / token API | Enterprise CN, data-dense | 97k+ |
| Ant Design X | ant-design/x | antd tokens | React AI chat / copilot UI | 3k+ |
| MUI (Material UI) | mui/material-ui | Emotion/Styled | Material Design, largest component set | 95k+ |
| Mantine | mantinedev/mantine | CSS Modules | 100+ hooks, batteries-included | 27k+ |
| Chakra UI | chakra-ui/chakra-ui | Emotion | Accessible, great theming API | 38k+ |
| NextUI | nextui-org/nextui | Tailwind | Modern, beautiful defaults | 22k+ |
| Headless UI | tailwindlabs/headlessui | Tailwind | Official Tailwind unstyled | 26k+ |
| React Aria | adobe/react-spectrum | Any | Adobe's accessibility primitives | 13k+ |
| Arco Design | arco-design/arco-design | Less | ByteDance enterprise | 4k+ |
| Semi Design | DouyinFE/semi-design | SCSS | ByteDance modern enterprise | 8k+ |
| Geist UI | geist-org/geist-ui | CSS-in-JS | Vercel-style minimalist | 4k+ |
| Park UI | park-ui/park-ui | Tailwind | Ark UI + Park styling | 2k+ |
| DaisyUI | saadeghi/daisyui | Tailwind | Tailwind component classes | 34k+ |
| Flowbite React | themesberg/flowbite-react | Tailwind | Tailwind pre-built | 2k+ |

#### Vue Ecosystem

| Framework | Meta-Framework | Component Library Options | Best For |
|-----------|---------------|--------------------------|----------|
| **Vue 3** | — | TDesign, Element Plus, Naive UI, Vuetify, PrimeVue | Progressive web apps |
| **Nuxt 3** | Vue SSR/SSG | Naive UI, TDesign, Element Plus, PrimeVue | Full-stack Vue, SEO |

**Vue Component Libraries — Full List**:

| Library | GitHub | Styling | Strength | Stars |
|---------|--------|---------|----------|-------|
| Element Plus | element-plus/element-plus | SCSS | Most popular CN Vue3, forms | 25k+ |
| TDesign Vue Next | Tencent/tdesign-vue-next | Less/CSS variables | Tencent design, bilingual, Starter templates | 2.1k+ |
| TDesign Chat | Tencent/tdesign-vue-next chat | CSS variables | Vue 3 AI chat with custom SSE / AG-UI | monorepo |
| Naive UI | tusen-ai/naive-ui | CSS-in-JS | TypeScript-first, 90+ components | 16k+ |
| Vuetify | vuetifyjs/vuetify | SASS | Material Design Vue, complete | 40k+ |
| PrimeVue | primefaces/primevue | CSS | 90+ components, enterprise | 10k+ |
| Ant Design Vue | vueComponent/ant-design-vue | Less | Ant Design in Vue | 20k+ |
| Arco Design Vue | arco-design/arco-design-vue | Less | ByteDance Vue | 2k+ |
| Vant 4 | vant-ui/vant | Less | Mobile-first Vue | 23k+ |
| NutUI | jd-opensource/nutui | SCSS | JD mobile Vue | 6k+ |
| Radix Vue | radix-vue/radix-vue | Unstyled | Radix primitives for Vue | 3k+ |
| shadcn-vue | radix-vue/shadcn-vue | Tailwind | shadcn/ui ported to Vue | 4k+ |
| Headless UI Vue | tailwindlabs/headlessui | Tailwind | Official Tailwind Vue unstyled | — |
| Flowbite Vue | themesberg/flowbite-vue | Tailwind | Tailwind pre-built Vue | 800+ |

#### Angular Ecosystem

| Framework | Component Library Options | Best For |
|-----------|--------------------------|----------|
| **Angular** | Angular Material, PrimeNG, NG-ZORRO, Clarity, Kendo UI | Large enterprise, strict structure |

**Angular Component Libraries**:

| Library | Styling | Strength |
|---------|---------|----------|
| Angular Material | SCSS | Google official Material Design |
| PrimeNG | CSS | 90+ components, enterprise |
| NG-ZORRO | Less | Ant Design for Angular, CN enterprise |
| Clarity | SCSS | VMware design system, data-heavy |
| Kendo UI | SCSS | Telerik commercial, powerful grids |
| Nebular | SCSS | Auth/theming/layout framework |
| Taiga UI | CSS | Tinkoff open-source, modern |

#### Svelte Ecosystem

| Framework | Meta-Framework | Component Library Options | Best For |
|-----------|---------------|--------------------------|----------|
| **Svelte** | — | Skeleton, shadcn-svelte, Flowbite Svelte | Lightweight, compiler-driven |
| **SvelteKit** | Svelte SSR/SSG | Skeleton, shadcn-svelte, Bits UI | Full-stack Svelte |

**Svelte Component Libraries**:

| Library | Styling | Strength |
|---------|---------|----------|
| shadcn-svelte | Tailwind | shadcn/ui ported to Svelte |
| Skeleton | Tailwind | Full design system, theming |
| Bits UI | Unstyled | Headless Svelte primitives |
| Flowbite Svelte | Tailwind | Pre-built Tailwind Svelte |
| DaisyUI + Svelte | Tailwind | Via DaisyUI classes |

#### Other Web Frameworks

| Framework | Type | Component Ecosystem | Best For |
|-----------|------|---------------------|----------|
| **Solid.js** | Reactive UI | Solid UI, Kobalte (headless) | Maximum performance, fine-grained reactivity |
| **SolidStart** | Solid meta-framework | Same as Solid.js | Full-stack Solid |
| **Qwik** | Resumable | Qwik UI | Instant page loads, O(1) startup |
| **Astro** | Content-first SSG | Any (React/Vue/Svelte islands) | Content sites, docs, blogs, marketing |
| **Lit** | Web Components | Shoelace (now Web Awesome) | Framework-agnostic, design system sharing |
| **Alpine.js** | Lightweight interactivity | + Tailwind/DaisyUI | Simple sites, progressive enhancement |
| **HTMX** | Hypermedia | + Tailwind/Bootstrap | Server-rendered interactivity, minimal JS |
| **Preact** | Lightweight React | Most React libraries | Size-critical React alternative |

### 10.2 Mobile Development — Complete Catalog

| Platform | Framework | UI Library | Best For |
|----------|-----------|-----------|----------|
| **React Native** | Expo (recommended) | React Native Paper, NativeBase, Tamagui, Gluestack | Cross-platform iOS + Android |
| **React Native** | Bare RN | Same + custom native modules | When Expo limits are hit |
| **Flutter** | Flutter SDK | Material 3, Cupertino, FluentUI | High-fidelity custom UI, both platforms |
| **iOS Native** | SwiftUI | Native components | Apple-exclusive, best iOS UX |
| **iOS Native** | UIKit | Native + third-party | Legacy iOS, complex custom UI |
| **Android Native** | Jetpack Compose | Material 3 Compose | Modern Android-exclusive |
| **Android Native** | XML Views | Material Components | Legacy Android |
| **Kotlin Multiplatform** | Compose Multiplatform | Material 3 | Kotlin across iOS + Android + Desktop |
| **Ionic** | Capacitor + React/Vue/Angular | Ionic Framework | Web-based hybrid mobile |
| **.NET MAUI** | XAML | .NET MAUI controls | C#/.NET cross-platform |
| **HarmonyOS** | ArkUI (ArkTS) | HarmonyOS components | Huawei HarmonyOS devices |

**React Native UI Libraries**:

| Library | Style | Strength |
|---------|-------|----------|
| React Native Paper | Material Design | Google Material, widely used |
| Tamagui | Optimizing compiler | Universal (web + native), fast |
| Gluestack UI | NativeWind/Tailwind | Tailwind-like for RN |
| NativeBase | Styled System | Accessible, themeable |
| React Native Elements | Customizable | Easy to start |
| RNUI (by Wix) | Customizable | Production-tested at Wix |
| Kitten UI | Eva Design | Design system with dark mode |

### 10.3 Mini Program — Complete Catalog

| Platform | Framework Options | UI Library | Best For |
|----------|-------------------|-----------|----------|
| **WeChat Mini** | Native WXML | TDesign Mini, Vant Weapp, WeUI, Lin UI | Single-platform WeChat |
| **Alipay Mini** | Native AXML | Ant Design Mini | Alipay ecosystem |
| **ByteDance Mini** | Native TTML | Arco Design Mini | Douyin/TikTok ecosystem |
| **UniApp** | Vue-based cross-platform | uView, TuniaoUI, uni-ui | Multi-platform mini + H5 + App |
| **Taro** | React/Vue cross-platform | NutUI, Vant Weapp, TDesign | Multi-platform from React/Vue |
| **mpx** | Vue-enhanced WXML | Any WeChat library | Enhanced native mini program |

**UniApp UI Libraries**:

| Library | Strength |
|---------|----------|
| uni-ui | Official, lightweight |
| uView | Popular, comprehensive |
| TuniaoUI | Modern, well-documented |
| tmui | Theme-powered, rich |
| FirstUI | Commercial quality, free tier |

### 10.4 Desktop Application — Complete Catalog

| Framework | Language | Web Engine | UI Options | Best For |
|-----------|---------|------------|-----------|----------|
| **Electron** | JS/TS | Chromium | Any React/Vue/Svelte lib | Feature-rich, large community |
| **Tauri** | Rust + JS/TS | System WebView | Any web lib | Small binary, secure, modern |
| **Wails** | Go + JS/TS | System WebView | Any web lib | Go developers |
| **Neutralino** | JS/TS | System WebView | Any web lib | Ultra-lightweight |
| **.NET MAUI** | C# | Native | MAUI controls | .NET enterprise |
| **WPF** | C# | Native | WPF controls | Windows-only enterprise |
| **SwiftUI Mac** | Swift | Native | Native macOS | Apple-native Mac apps |
| **Compose Desktop** | Kotlin | Skia | Material 3 | Kotlin cross-platform |
| **Qt** | C++/Python | Native | Qt Widgets/QML | Industrial, cross-platform |
| **GTK** | C/Rust/Python | Native | GTK4 widgets | Linux-native |
| **Flutter Desktop** | Dart | Skia | Material 3, Cupertino | From mobile to desktop |

### 10.5 CSS Strategy — Complete Catalog

| Approach | Library | Philosophy | Best Paired With |
|----------|---------|-----------|------------------|
| **Utility-First** | Tailwind CSS | Utility classes in HTML | shadcn/ui, Headless UI, DaisyUI, any headless |
| **Utility-First** | UnoCSS | Atomic, instant, extensible | Naive UI, Vue ecosystem |
| **Utility-First** | Windi CSS | Tailwind alternative (deprecated) | Legacy projects |
| **Component Classes** | Bootstrap | Pre-built component classes | jQuery, HTMX, traditional web |
| **Component Classes** | Bulma | Modern, no JS dependency | Simple sites, prototyping |
| **CSS Modules** | Built-in (CRA/Vite) | Scoped per-component | Mantine, custom design systems |
| **CSS-in-JS** | Styled Components | Tagged template literals | Chakra, custom React |
| **CSS-in-JS** | Emotion | Performant CSS-in-JS | MUI, Chakra |
| **CSS-in-JS** | Vanilla Extract | Zero-runtime, type-safe | High-performance, SSR |
| **CSS-in-JS** | Panda CSS | Zero-runtime utility | Modern type-safe styling |
| **CSS-in-JS** | StyleX | Facebook's atomic CSS-in-JS | Large-scale React apps |
| **CSS Variables** | Open Props | Pre-made custom properties | Any framework, progressive |
| **Pre-processor** | SASS/SCSS | Nesting, variables, mixins | Angular Material, Bootstrap |
| **Pre-processor** | Less | Simpler than SASS | Ant Design, Element Plus |

### 10.6 Special Scenario — Complete Catalog

| Scenario | Framework | UI Approach | Recommended Stack |
|----------|-----------|-----------|-------------------|
| **Chrome Extension** | React/Vue + Manifest V3 | shadcn/ui or Tailwind | Plasmo + React + Tailwind |
| **VS Code Extension** | VS Code Webview API | VS Code Toolkit | @vscode/webview-ui-toolkit |
| **Figma Plugin** | React in iframe | Figma Plugin DS | React + Figma DS tokens |
| **CLI UI** | Node.js | Ink (React for CLI) | Ink + Pastel |
| **Terminal TUI** | Node.js/Rust/Go | Blessed, Bubbletea, Ratatui | Go: Bubbletea; Rust: Ratatui |
| **Email Template** | React Email / MJML | Inline CSS | React Email + Resend |
| **PDF Generation** | React-PDF | In-document styling | @react-pdf/renderer |
| **3D / WebGL** | Three.js | React Three Fiber | R3F + Drei + Tailwind overlay |
| **Game UI** | Phaser / PixiJS | Canvas-based | Phaser 3 + custom UI |
| **Slideshows** | Reveal.js / Slidev | Markdown + themes | Slidev (Vue) for dev talks |
| **Documentation** | VitePress/Docusaurus/Nextra | Built-in themes | VitePress (Vue), Nextra (React) |
| **Blog/CMS** | Astro/Next.js/Nuxt | Content-focused | Astro + Tailwind + MDX |
| **Landing Page** | Next.js/Astro | Animation-heavy | Next.js + Tailwind + Framer Motion |
| **Admin/Dashboard** | Next.js/Nuxt | Data-dense | Ant Design / TDesign / Tremor |
| **E-commerce** | Next.js/Nuxt | Product-focused | Medusa + Next.js + shadcn/ui |
| **Real-time / Chat** | Next.js/Nuxt | Stream-based | shadcn/ui + Socket.io/WebSocket |
| **Map / GIS** | Any + Mapbox/Leaflet | Overlay UI | Tailwind + Mapbox GL JS |
| **PWA** | Any SSR framework | Service Worker | Next.js + next-pwa |
| **TV / Large Screen** | React Native TV / Compose TV | Focus-based navigation | Expo for TV |
| **Watch / Wearable** | SwiftUI / Wear Compose | Ultra-compact UI | Native per platform |

### 10.7 Design-Driven Recommendation Engine

> **Note**: This recommendation is from a DESIGN perspective — "which stack best expresses the target aesthetic?"
> If `frontend-patterns` or `web-development` skills are also active, their engineering perspective may differ. Present both and let the user decide.

**When the user asks to build something, follow this decision flow:**

```
Step 1: Ask "What platform?" (if not obvious from context)
   ├─ Web app       → Step 2a
   ├─ Mobile app    → Step 2b
   ├─ Mini program  → Step 2c
   ├─ Desktop app   → Step 2d
   ├─ Cross-platform → Step 2e
   └─ Special       → Step 2f

Step 2a (Web): Ask "What type of web app?"
   ├─ SaaS / Tool         → Next.js + shadcn/ui + Tailwind + Lucide
   ├─ Admin / Dashboard    → Next.js + Ant Design (or TDesign for CN)
   ├─ Landing page         → Astro or Next.js + Tailwind + Framer Motion
   ├─ Blog / Documentation → Astro + Tailwind (or VitePress for Vue)
   ├─ E-commerce           → Next.js + shadcn/ui + Commerce SDK
   ├─ Real-time / Chat     → Next.js + shadcn/ui + WebSocket
   ├─ Data visualization   → Next.js + Tremor or Recharts + Tailwind
   ├─ Chinese enterprise   → Vue 3 + Element Plus or TDesign
   └─ Portfolio / Creative → Astro or Next.js + Tailwind + GSAP

Step 2b (Mobile): Ask "Which platforms?"
   ├─ iOS + Android   → Expo (React Native) + Paper or Tamagui
   ├─ iOS only         → SwiftUI (native)
   ├─ Android only     → Jetpack Compose (native)
   ├─ High-fidelity UI → Flutter + Material 3
   └─ HarmonyOS        → ArkUI (ArkTS)

Step 2c (Mini Program): Ask "Which platform?"
   ├─ WeChat only       → Native + TDesign Mini or Vant Weapp
   ├─ Multi-platform    → UniApp + uView or Taro + NutUI
   ├─ Alipay            → Native + Ant Design Mini
   └─ ByteDance         → Native + Arco Design Mini

Step 2d (Desktop): Ask "Main language?"
   ├─ TypeScript/JS → Tauri + React/Vue + shadcn/ui + Tailwind
   ├─ Go            → Wails + Vue + Naive UI
   ├─ Rust          → Tauri native or Tauri + web frontend
   ├─ C#/.NET       → WPF or MAUI
   ├─ Kotlin        → Compose Desktop
   ├─ Swift         → SwiftUI macOS
   └─ C++/Python    → Qt or GTK

Step 2e (Cross-platform): Ask "Which surfaces?"
   ├─ Web + Mobile         → Next.js (web) + Expo (mobile) + shared Tailwind tokens
   ├─ Mobile + Desktop     → Flutter (all) or Compose Multiplatform
   ├─ Web + Mobile + Mini  → UniApp (Vue) or Taro (React)
   └─ All platforms        → Flutter or separate best-of-breed per platform

Step 2f (Special):
   ├─ Chrome extension → Plasmo + React + Tailwind
   ├─ VS Code extension → @vscode/webview-ui-toolkit
   ├─ CLI tool         → Ink (React for CLI)
   ├─ Email template   → React Email + Resend
   └─ 3D / Game        → Three.js + React Three Fiber
```

### 10.8 User Choice Override Protocol

**When the user has already chosen a stack that differs from our recommendation:**

```
User says: "I want to use [X]"

AI response pattern:
  1. Acknowledge: "Great, I'll build this with [X]."
  2. (Optional brief note ONLY if there's a significant trade-off):
     "Quick note: [X] works well for this. [Y] is also popular for this type of project
      due to [reason], but [X] is a solid choice. Let's proceed with [X]."
  3. Adapt ALL selections to match:
     - Icon set → pick the best match for [X]
     - CSS approach → pick what's native to [X]
     - Animation → pick compatible library
     - Fonts → same (universal)
  4. Proceed without further questioning.
```

**Adaptation table — when user picks a specific framework, automatically pair:**

| User Chooses | Auto-Pair Icons | Auto-Pair CSS | Auto-Pair Animation |
|-------------|----------------|---------------|---------------------|
| React + any | Lucide React | Tailwind CSS | Framer Motion |
| Next.js | Lucide React | Tailwind CSS | Framer Motion |
| Vue + any | Iconify Vue | UnoCSS or Tailwind | @vueuse/motion |
| Nuxt | Iconify Vue | UnoCSS or Tailwind | @vueuse/motion |
| Angular | Angular Material Icons | SCSS | Angular Animations |
| Svelte / SvelteKit | Lucide Svelte | Tailwind CSS | Svelte transitions |
| Solid.js | Lucide (generic SVG) | Tailwind CSS | Solid Transition Group |
| Flutter | Material Icons | Flutter ThemeData | Flutter built-in |
| React Native / Expo | Expo Vector Icons | StyleSheet / NativeWind | Reanimated |
| UniApp | uni-icons | UniApp built-in | uni.animation |
| Taro | @tarojs/icons | Taro CSS | Taro animation API |
| Electron + React | Lucide React | Tailwind CSS | Framer Motion |
| Tauri + Vue | Iconify Vue | UnoCSS | @vueuse/motion |
| Wails + Vue | Iconify Vue | UnoCSS | @vueuse/motion |
| HTMX | Lucide (SVG) | Tailwind CSS | CSS transitions |
| Astro | Astro Icon | Tailwind CSS | View Transitions |

### 10.9 Project Bootstrap Quick Commands

**React / Next.js (Most Common)**:
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app && npx shadcn@latest init
npm i lucide-react @fontsource-variable/inter framer-motion
```

**Vue / Nuxt**:
```bash
npx nuxi@latest init my-app
cd my-app && npm i naive-ui @iconify/vue @vueuse/motion
npm i @fontsource-variable/inter unocss -D
```

**Angular**:
```bash
ng new my-app --style=scss --routing
cd my-app && ng add @angular/material
npm i @fontsource-variable/inter
```

**Svelte / SvelteKit**:
```bash
npx sv create my-app
cd my-app && npx shadcn-svelte@latest init
npm i lucide-svelte @fontsource-variable/inter
```

**Astro**:
```bash
npm create astro@latest my-app -- --template minimal
cd my-app && npx astro add tailwind
npm i astro-icon @fontsource-variable/inter
```

**Expo (React Native)**:
```bash
npx create-expo-app my-app --template blank-typescript
cd my-app && npm i react-native-paper react-native-safe-area-context
npx expo install react-native-reanimated
```

**Flutter**:
```bash
flutter create my_app --platforms=android,ios
cd my_app
# Material 3 is built-in, enable in ThemeData
```

**Tauri (Desktop)**:
```bash
npm create tauri-app@latest my-app -- --template react-ts
cd my-app && npx shadcn@latest init
npm i lucide-react @fontsource-variable/inter framer-motion
```

**WeChat Mini Program + TDesign**:
```bash
# In mini program project root:
npm i tdesign-miniprogram
# Build npm in WeChat DevTools → Tools → Build npm
```

**UniApp**:
```bash
npx degit dcloudio/uni-preset-vue#vite-ts my-app
cd my-app && npm i uview-plus
```

**Chrome Extension**:
```bash
npm create plasmo@latest my-ext -- --with-tailwindcss
cd my-ext && npm i lucide-react @fontsource-variable/inter
```

---


{% endraw %}
