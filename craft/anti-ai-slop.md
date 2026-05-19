# Anti-AI-slop 反套路规则

把"明显是 LLM 默认产出"的视觉/文案模式列成可机检黑名单。
本文件的 **P0** 规则由 `bin/super-skill design-audit` 强制扫描；命中即 fail-on-findings。
**P1 / P2** 是给 reviewer 和 agent 的指导。

> 灵感：[`nexu-io/open-design`](https://github.com/nexu-io/open-design) 的 `craft/anti-ai-slop.md` 和 [`refero_skill`](https://github.com/referodesign/refero_skill)（MIT），按 Super Skill 的 lint 表面收紧。

## P0 — 必须修复（机器扫描）

### 1. 默认 Tailwind indigo 当 accent
**反模式**：`#6366f1` / `#4f46e5` / `#4338ca` / `#3730a3` / `#8b5cf6` / `#7c3aed` / `#a855f7`
作为 solid accent 出现在 css/inline style/Tailwind class（`bg-indigo-*` / `text-indigo-*` / `from-indigo-*`）。这是 AI 输出的最大 tell。
**修复**：用 `var(--accent)` 或 design system 已声明的品牌色。

### 2. 两段渐变 "trust" hero
**反模式**：`linear-gradient(... , purple, blue)` / `from-blue to-cyan` / `from-indigo via-purple to-pink` 出现在 hero 区域背景。
**修复**：纯色 surface + 有意识的 typography hierarchy 比这个强。

### 3. emoji 当 feature icon
**反模式**：`✨` / `🚀` / `🎯` / `⚡` / `🔥` / `💡` / `🌟` 出现在 `<h*>` / `<button>` / `<li>` / `class*="icon"` 内部。
**修复**：用 1.6–1.8px stroke 的单色 SVG + `currentColor`。

### 4. display 文本用 sans-serif（当 DESIGN.md 绑了 serif）
**反模式**：`h1` / `h2` 的 font-family 是硬写 `Inter` / `Roboto` / `system-ui` / `sans-serif`，但项目 `DESIGN.md` 声明了 `--font-display` 是衬线。
**修复**：使用 `var(--font-display)`。

### 5. AI dashboard tile（圆角 + 左色边）
**反模式**：`border-radius: ≥8px` 同时 `border-left: 3-4px solid <colored>`，在 `.card` / `[role="article"]` 上。
**修复**：去掉 radius 或去掉 left-border，二选一。

### 6. 编造指标
**反模式**：`10× faster` / `99.9% uptime` / `3× more productive` / `50% increase` 出现在 marketing 文案，且不附引用源。
**修复**：要么有 footnote / data source，要么用 placeholder 占位文案 `<metric-placeholder>`。

### 7. Filler 占位文案
**反模式**：`lorem ipsum` / `feature one` / `feature two` / `placeholder text` / `sample content` / `Your text here` 进入最终交付物。
**修复**：空区块是设计问题，用 composition 解决，不是用编造文字补。

## P1 — 应该修复（指导，部分可扫）

- **标准 Hero → Features → Pricing → FAQ → CTA 顺序** 完全没变体 *(指导)*：至少有一节用非常规结构（横向 comparison、内嵌 mini-demo、用户语录全屏 quote 等）。
- **外部 placeholder 图片 CDN**：`unsplash.com` / `placehold.co` / `placekitten.com` / `picsum.photos`。脆弱且明显，用 `.ph-img` 占位 class 或本地 svg。
- **超过 12 个原始 hex 出现在 `:root` 之外**：说明 token 没被 honor。
- **`var(--accent)` 在渲染 body 里超过 6 次**：限制单屏视觉占用 ≤ 2 次。

## P2 — 锦上添花（多为指导）

- 区块缺 `data-od-id` / `data-section-id`：评审模式无法定位。
- 装饰性 blob / wave svg 背景 *(指导)*：无意义的几何形状。
- 完全对称布局 *(指导)*：交替密度（紧—松—紧）读起来更有意图。

## 不计入 slop 的"加分项"

- ~80% 经过验证的设计模式 + ~20% 一处明显的有意识选择（一个手绘装饰、一个非常规字号跳跃、一段反向 copy）。
- 真实有引用源的数据 / 真实截图 / 真实客户语录。
- 显式的 empty state（带插画或 instructional copy）替代占位文字。
