# 色彩准则（brand-agnostic）

## P0 规则

- **token 优先**：业务代码里不出现原始 hex，只用 `var(--*)` 或 design system 定义的 utility。
- **accent 占比 ≤ 2 处可视使用**（同一屏内）：accent 不是底色，是焦点。
- **对比度**：正文 + 背景 ≥ WCAG AA（4.5:1）；大字 ≥ 3:1；UI 控件状态色对比 ≥ 3:1。
- **禁止 indigo 默认色作为 accent**（见 anti-ai-slop.md P0 §1）。

## P1 指导

- 单色 hue 系列 ≤ 9 阶（50/100/.../900），并且每阶 ΔL* > 5。
- 状态色（success/warning/danger）保持 hue 不动、L 拉开。
- 暗色模式不是反色：要重新调对比度。

## 检测建议

- `bin/super-skill design-audit` 扫 `var(--*)` 缺失 → 命中 P0。
- 视觉对比可用 axe-core / Lighthouse 跑一遍。
