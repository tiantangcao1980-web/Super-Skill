# 状态覆盖准则

任何交互组件 / 页面必须显式设计这五种状态：

1. **Empty** —— 没有数据时的样子（带 instructional copy + primary action）。
2. **Loading** —— 异步加载（skeleton 优先于 spinner，超过 500ms 才展示）。
3. **Partial** —— 数据加载了一部分（如 pagination 中、infinite scroll）。
4. **Error** —— 失败时的样子（具体原因 + 重试 action + 联系路径）。
5. **Success / Filled** —— 正常有数据的样子。

## P1 规则

- Empty 不是空白：不画 = 设计缺失。
- Error 必须可恢复：给"重试"或"联系支持"，不能是死胡同。
- Loading skeleton 要匹配最终布局的高度，避免 layout shift（CLS ≤ 0.1）。

## 与其它准则的关系

- Empty / Error 的文案遵循 `craft/anti-ai-slop.md` 的"无 lorem ipsum / 无编造指标"规则。
- Loading 动效遵循 `craft/animation-discipline.md` 的"prefers-reduced-motion"兜底。
