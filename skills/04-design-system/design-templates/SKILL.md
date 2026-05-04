---
name: design-templates
description: |
  设计规范文档 skill:产出标准化的 DESIGN.md / Design Tokens / 配色卡 / 字体表 / 间距规范。
  灵感:tiantangcao1980-web/awesome-design-md —— 设计规范模板集。
  触发词:「DESIGN.md」「设计规范」「设计 token」「色板」「字体规范」「布局规范」「设计系统文档」「style guide」「设计文档模板」。
  适用阶段:项目立项后的设计规范文档化、design system 初始化、新人 onboarding、设计稿 → 代码 token 同步。
---

# Design Templates · 设计规范模板

> 灵感:[awesome-design-md](https://github.com/tiantangcao1980-web/awesome-design-md) —— 用 Markdown 把设计规范固化下来。
> 核心心法:**设计规范不是 PDF,是版本化的 Markdown + tokens**,跟代码一起 review。

> 💡 **协作 Cowork 专家**(若已激活):
> - `design/design-system-management` —— 设计 token / 组件库 / 模式文档的**持续维护**
> - `design/accessibility-review` —— 设计规范的 WCAG 2.1 AA 校验
> - `design/design-handoff` —— 给开发的实现规格补充
>
> **分工**:本 skill 出**初始 DESIGN.md + design-tokens.json 模板**,Cowork 做**长期演进 + 多端同步 + 可访问性审计**。

## 必产出物清单

每个项目至少产出 3 份文档:
1. **`docs/DESIGN.md`** — 设计规范主文档
2. **`tokens/design-tokens.json`** — 机器可读的 token(可被 Style Dictionary 转成多端代码)
3. **`docs/design/CHANGELOG.md`** — 设计变更日志

---

## DESIGN.md 标准模板

```md
# <项目名> Design Specification

## 1. Aesthetic Direction
- 主方向: <例如 "瑞士主义 + 杂志感">(具体,不是"现代简约")
- 局部偏移: <例如 "字号比典型瑞士派大一档">
- 参考: [图 1](url) / [产品 X](url)

## 2. Voice & Tone
- 语气坐标:
  - 正式度: 朋友
  - 理性度: 逻辑
  - 温度: 克制
  - 幽默度: 偶尔自嘲
- 关键 5 句文案:[由 copywriting-design 产出]

## 3. Color
| Token | Value | Usage |
|-------|-------|-------|
| color/primary | #1e293b | 主按钮、Logo |
| color/accent | #3b82f6 | 链接、强调 |
| color/bg | #fafafa | 页面底色 |
| color/fg | #0a0a0a | 正文 |
| color/success | #16a34a | 成态 |
| color/warning | #f59e0b | 警告 |
| color/error | #dc2626 | 错态 |
| color/info | #0284c7 | 提示 |

## 4. Typography
| Token | Family | Weight | Size/Line |
|-------|--------|--------|-----------|
| heading/h1 | Geist | 700 | 64/72 |
| heading/h2 | Geist | 700 | 40/48 |
| body/default | Geist | 400 | 16/24 |
| body/small | Geist | 400 | 14/20 |
| code | Geist Mono | 400 | 14/22 |

## 5. Spacing & Sizing
- 间距步长: 4px
- 圆角: 0 / 4 / 8 / 16(只用这 4 个)
- 阴影:
  - sm: 0 1px 2px rgba(0,0,0,.05)
  - md: 0 4px 12px rgba(0,0,0,.1)
  - lg: 0 12px 32px rgba(0,0,0,.15)

## 6. Layout
- 主网格: 12 列, gutter 24px
- 主页面: 2/3 + 1/3 不对称
- 移动端: 单列堆叠, padding 16px
- 最大内容宽度: 1280px

## 7. Motion
- 缓动: cubic-bezier(0.4, 0, 0.2, 1)
- 时长: 150ms 微交互 / 300ms 页面级 / 不超过 500ms

## 8. Accessibility
- 对比度: WCAG AA(正文 4.5:1,大字 3:1)
- 焦点态: 必须可见
- 键盘可达: 所有交互
- 屏幕阅读器: 主要图片有 alt,form 有 label

## 9. Iconography
- 库: <Lucide / Tabler / 自绘>
- 尺寸: 16 / 20 / 24
- 描边宽度: 1.5px
- 颜色: 跟随 currentColor

## 10. Empty / Error / Loading 状态规范
- Empty: <文案规则,引用 copywriting-design>
- Error: <文案规则>
- Loading: <Skeleton vs Spinner 选择规则>
```

---

## design-tokens.json 模板

```json
{
  "color": {
    "primary": { "value": "#1e293b", "type": "color", "comment": "主按钮、Logo" },
    "accent":  { "value": "#3b82f6", "type": "color" },
    "bg":      { "value": "#fafafa", "type": "color" },
    "fg":      { "value": "#0a0a0a", "type": "color" }
  },
  "spacing": {
    "0": { "value": "0px" },
    "1": { "value": "4px" },
    "2": { "value": "8px" },
    "3": { "value": "12px" },
    "4": { "value": "16px" },
    "6": { "value": "24px" },
    "8": { "value": "32px" }
  },
  "radius": {
    "none": { "value": "0" },
    "sm":   { "value": "4px" },
    "md":   { "value": "8px" },
    "lg":   { "value": "16px" }
  }
}
```

跑 [Style Dictionary](https://amzn.github.io/style-dictionary/) 转 CSS / Swift / Android 各端代码。

---

## 工作流

### 触发场景 A · 项目立项,从 0 写设计规范
1. 跟 `ui-design` 协作出 Aesthetic Direction
2. 跟 `copywriting-design` 协作出 Voice & Tone
3. 填 DESIGN.md 模板
4. 抽出 tokens 到 design-tokens.json
5. (可选)接 Style Dictionary 转代码

### 触发场景 B · 已有项目补规范
1. 抓 5 个核心页面截图
2. 量出实际配色 / 字体 / 间距
3. 反向写 DESIGN.md
4. 标注偏离项("现状用了 4 种灰色,建议收敛到 2 种")

### 触发场景 C · 设计变更
- 走 `docs/design/CHANGELOG.md`
- 重大变更(主色 / 字体 / 主网格)需 PR + review
- 小变更(加一个间距 token)直接提

---

## 反模式

- ❌ **PDF 设计规范**:不能 diff,不能 grep,等于死文件
- ❌ **Figma-only,无文档**:Figma 没文档化的 token,代码端会重新发明一遍
- ❌ **token 太多**:300 个间距值 = 没规范。强制收敛到 8-12 个
- ❌ **token 命名抽象**:`color-1` `color-2` 没意义,要语义化(`color-primary`)
- ❌ **设计师独写,工程师不参与**:产出后没人用 / 实现不了
- ❌ **不写状态规范**:empty/error/loading 各页面各做各的

---

## 与其他 skill 的关系

- `ui-design` 提供美学方向,本 skill 把它**固化**成文档
- `copywriting-design` 提供 Voice & Tone,本 skill 写进 DESIGN.md
- `design-dev-flow` ② 设计幕的"设计规范"产出由本 skill 产出
- `designdna` skill(已装)提供更深的方法论,本 skill 提供模板

---

## References

- [DESIGN.md 完整模板](references/design-md-template.md)
- [tokens 命名规范](references/token-naming.md)
