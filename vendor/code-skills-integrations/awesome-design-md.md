# awesome-design-md

- **URL**: https://github.com/tiantangcao1980-web/awesome-design-md
- **License**: 见原仓库
- **类型**: 设计规范模板集 / awesome 列表

## 这是什么

收集"用 Markdown 写设计规范"的模板与最佳实践。核心理念:**设计规范不是 PDF,是版本化的 .md + tokens.json**,可以 diff、grep、PR review,跟代码一起演进。

## 在 code-skills 中的对应

- **对应 skill**:`design-templates`
- 借鉴的核心:
  - DESIGN.md 章节结构(Aesthetic / Color / Typography / Spacing / Layout / Motion / A11y / Iconography / States)
  - design-tokens.json 命名规范
  - 设计变更日志的做法(`docs/design/CHANGELOG.md`)

## 何时用

- 新项目初始化设计规范
- 已有项目反向写规范(从截图量出 token)
- 设计师 / 工程师协作时的"单一事实源"
- onboarding 新人快速理解视觉系统

## 怎么用

直接触发 `design-templates` skill,产出 `docs/DESIGN.md` + `tokens/design-tokens.json`。然后接 [Style Dictionary](https://amzn.github.io/style-dictionary/) 转多端代码。

## 不集成的部分

- awesome-design-md 收录的所有模板(只取最通用的 10 章)
- Figma / Sketch 的双向同步(那是 Tokens Studio 之类的工具的事)
- 品牌资产库管理(logo / 字体文件 / 图片 → 走对象存储,不在本 skill 范围)
