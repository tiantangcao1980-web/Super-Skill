# 排版准则（brand-agnostic）

## P0 规则

- **Display 字号必须用 `var(--font-display)`**，不能硬写 `Inter` / `Roboto` / `sans-serif`。
- **行高合规**：body 文本 `line-height` 在 `1.4`–`1.7` 之间；H1 在 `1.0`–`1.2`；H2 在 `1.1`–`1.3`。
- **字号阶梯遵循模数**：相邻字号之比 ∈ {1.125, 1.2, 1.25, 1.333, 1.414, 1.5, 1.618} 之一，不要"+2px"逐级。
- **同屏字号 ≤ 5 个**：超过通常是 hierarchy 失败。
- **段宽 (measure) 50–80 字符**：超出做多列或拉边距。

## P1 指导

- 标点遵循语言惯例：中文用 `「」`、`，`、`。`；英文用 `"`、`,`、`.`。
- 数字与单位之间用细空格（thin space）。
- 长 url / 长代码块用 `overflow-wrap: anywhere`，不挤行。

## 与 anti-ai-slop 的边界

排版相关的 P0 反模式在 `anti-ai-slop.md` § "display 文本用 sans-serif" 处声明，避免规则重复。
