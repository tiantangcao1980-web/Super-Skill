# 动效纪律

## P0 规则

- **尊重 `prefers-reduced-motion`**：所有 > 200ms 的非必要动效在 reduced 模式下立刻完成或换淡入。
- **GPU 友好**：只动 `transform` 和 `opacity`；避免动 `top/left/width/height`。
- **timing function 不用线性**：默认 `cubic-bezier(0.16, 1, 0.3, 1)`（"easeOutExpo"-flavored）或品牌 motion token。

## P1 指导

- 动效服务于反馈，不是装饰：每个动效问"它在告诉用户什么？"。
- 入场动效 ≤ 300ms；hover ≤ 150ms；layout transition 200–400ms。
- 列表项不要 stagger 超过 5 个（否则等待过长）。

## P2 指导

- 用 spring 物理曲线时，damping ≥ 20，避免明显回弹。
- scroll-trigger 动效在 first viewport 不要播放（已经在视野里的元素不应"出现"）。

## 反模式

- "fade in everything"——所有区块入场淡入，等待累积超过 1s。
- 鼠标 hover 卡片大幅放大（scale > 1.05），破坏布局。
- 自动播放视频含声音（同时违反 a11y baseline）。
