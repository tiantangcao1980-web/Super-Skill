# 可访问性基线

## P0 规则

- 所有交互元素有可见 `:focus-visible` 状态，且对比度 ≥ 3:1。
- `<img>` 必须有 `alt`（装饰图用 `alt=""`，但属性必须在）。
- 表单 `<input>` 必须有可关联的 `<label>`，不能只靠 placeholder。
- 颜色不是唯一信息载体（红色错误必须同时有图标/文字）。
- 语义化标签：导航用 `<nav>`、主内容用 `<main>`、章节用 `<section>` 配 `aria-labelledby`。

## P1 指导

- 键盘导航顺序与视觉顺序一致。
- 弹层（modal/dialog）必须 trap focus 并在关闭时归还焦点。
- 动效尊重 `prefers-reduced-motion`：超过 200ms 的过渡都要兜底。
- 文案不写 "click here"、"点这里"——链接文本要自包含。

## P2 指导

- live region 用 `aria-live="polite"`（异步反馈）或 `assertive`（错误）。
- 长表单加进度指示和 step 标题。
- ARIA 属性优先选 native HTML 能表达的语义；多余 `role` 是反模式。

## 检测建议

- 自动：axe-core / Lighthouse / pa11y。
- 手动：键盘 Tab 走一遍、screen reader (VoiceOver/NVDA) 听一遍。
