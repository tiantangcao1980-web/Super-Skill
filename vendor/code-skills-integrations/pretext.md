# chenglou/pretext · 前端文本测量与性能

- **URL**: https://github.com/chenglou/pretext
- **Stars**: 45k+
- **License**: MIT
- **作者**: Cheng Lou(原 React 核心团队 / ReasonReact 作者)
- **类型**: TypeScript 库 —— 多行文本测量与布局,纯 JS 实现

## 这是什么

**核心能力**:在**不触碰 DOM** 的情况下,精确测量文本宽度、高度、行数,支持任何语言(中文 / 阿拉伯 / 表情 / 多脚本混排)。

**关键洞察**:`getBoundingClientRect()` / `offsetHeight` 这些 DOM 读操作会**触发 layout reflow**,是浏览器最贵的操作之一。Pretext 用 canvas 测字符宽度 + 自实现段落布局规则,**完全绕开 reflow**。

```ts
import { prepare, layout } from '@chenglou/pretext'

const prepared = prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')
const { height, lineCount } = layout(prepared, 320, 20)  // 纯算术,无 DOM
```

## 在 code-skills 中的对应

- **不做成单独 skill**(避免与已装的 `frontend-patterns` 重叠)
- **作为前端性能优化的"具体技术"被 frontend-patterns / 各 UI 库 skill 引用**
- 升级写代码时遇到下面场景就考虑接 pretext:

## 何时用(决策清单)

| 场景 | 用 pretext? | 替代方案 |
|------|------------|---------|
| 列表虚拟化要算每项高度 | ✅ 强烈推荐(避免边渲染边量) | react-virtual + 估高(不准) |
| 多语言 UI 标签可能被截断 | ✅ 开发期校验"按钮文案是否换行" | 上线后用户截图 |
| 长文档 reflow 跳动 | ✅ 提前算好 layout | 纸糊 `min-height` 凑合 |
| 文本输入实时显示行数 | ✅ 不引入 hidden div 测量 | 隐藏 textarea + scrollHeight(慢) |
| Canvas / SVG 富文本布局 | ✅ 唯一选择 | 自己造轮子 |
| 简单按钮里固定 1 行字 | ❌ 杀鸡用牛刀 | CSS truncate |
| 用户不可能换语言/字体 | ❌ 复杂度过剩 | DOM measure 也够 |

## 我们要学的"思想"(可迁移到无 pretext 的场景)

### 思想 1 · 区分"DOM 写"和"DOM 读"操作

**写**(setStyle / appendChild)便宜。
**读**(offsetHeight / getBoundingClientRect / scrollTop)**贵 100 倍**,因为强制浏览器先 flush pending layout。

**实战规则**:
- 同一帧内**先批量读,再批量写**(避免 read→write→read→write 这种"读写交替触发反复 reflow")
- 把 measure 移出关键路径(预测量 / 缓存 / canvas 替代)

### 思想 2 · "AI 友好的迭代方法"(README 原话)

Pretext 的实现自己用 canvas 测,但**把浏览器字体引擎当 ground truth**。这种 "**外部引擎当真理 + 自实现快速近似**" 的模式可以迁移到:
- 类型推断(把 TS compiler 当 ground truth,自己做缓存)
- 布局测算(把 DOM 当 ground truth,canvas 做近似)
- 验证(把 production 行为当 ground truth,unit test 做覆盖)

### 思想 3 · 让"开发期校验"成为可能

Pretext 让你在 CI 里就能跑"按钮文案是否在所有语言下都不溢出"这种检查 —— 因为不需要真实浏览器。

**类比**:把肉眼检查的事,变成代码可断言的事。

## 与本仓库 skill 的协作

| skill | 协作点 |
|-------|--------|
| `frontend-patterns`(已装 91 skill 之一) | 性能优化建议里加"用 pretext 替代 DOM measure" |
| `qa-strategy`(本仓库) | 测试策略里加"开发期文本溢出校验"用 pretext |
| `design-templates`(本仓库) | 设计 token 校验时,可用 pretext 验证关键字号在主流字体下都不溢出 |
| `auto-flow ⑥ 前端实现`(本仓库) | Ralph 循环里若遇到"列表虚拟化 / 多语言 UI",建议接 pretext |
| `programmatic-video`(本仓库) | Canvas 渲染视频字幕时用 pretext 算文本布局 |

## 不集成的部分

- 不把 pretext 复制进本仓库(它是 npm 库,直接装即可)
- 不强制使用(只在符合"决策清单"的场景才推荐)
- 不替代 CSS / Tailwind(它解决的是 DOM 测量问题,不是样式问题)

## 后续项目怎么用

```bash
# 1. 在前端项目里
npm i @chenglou/pretext

# 2. 触发 frontend-patterns skill 时,如果遇到"虚拟化 / 多语言溢出 / canvas 文本",
#    主动建议引入 pretext

# 3. CI 里加文本溢出校验(开发期防范)
```

## 一句话价值

> **避开 reflow 比"加 will-change"更根本** —— Pretext 是这个理念的具体落地。
