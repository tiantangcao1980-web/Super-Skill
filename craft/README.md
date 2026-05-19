# craft/ — 通用的设计/工程准则

`craft/` 放的是 **brand-agnostic、可被多个 skill opt-in 复用** 的横切准则。Skill 通过在 `SKILL.md` frontmatter 声明：

```yaml
od:
  craft:
    requires: [anti-ai-slop, typography, color, accessibility]
```

来显式吸收这些准则。`bin/super-skill audit --json` 会检查每个 `requires:` 引用都对应到本目录的一个文件，避免悬挂引用。

灵感来源：[`nexu-io/open-design`](https://github.com/nexu-io/open-design) 的 `craft/` 目录把通用规则与具体 skill 解耦，避免每个 skill 自己重写一份 a11y / typography 规则导致漂移。Super Skill 把同一思路落到自己仓库。

## 准则清单

| 文件 | 适用范围 | 严重度 |
| --- | --- | --- |
| `anti-ai-slop.md` | UI / 内容生成 / PPT / 营销 | 含 P0 lint 规则 |
| `typography.md` | 任何含可视字体的产物 | P0 + 指导 |
| `color.md` | 任何含色板的产物 | P0 + 指导 |
| `accessibility-baseline.md` | 前端 UI / 文档 / Slide | P0 + 指导 |
| `state-coverage.md` | 前端 UI / 交互稿 | P1 |
| `animation-discipline.md` | 任何含动效的产物 | P1 |
| `laws-of-ux.md` | 任何交互稿 | 指导 |
| `form-validation.md` | 含表单的前端 | P0 |

## 与现有 skill 的关系

- `skills/04-design-system/design-craft-gate/` 是 craft 准则的 **执行入口**，负责把每个文件里的可机检规则映射到 `bin/super-skill design-audit` 的扫描逻辑。
- `skills/04-design-system/anti-slop/` / `skills/04-design-system/designdna/` 是这些准则的 **应用层**：它们引用本目录的准则，不自己定义重复规则。
- 旧 skill 内嵌的 a11y / typography 段落保持不动；本次只把"可执行规则"集中到 craft/。后续可以渐进迁移到 references/ 引用。

## 维护规则

1. craft 文件只描述 **不依赖具体品牌** 的规则；品牌相关请放 `resources/design-md/`。
2. 每条 P0 规则必须有：(a) 反模式具体定义，(b) 修复路径，(c) `bin/super-skill design-audit` 里对应的检测逻辑或显式 "guidance, not auto-checked" 标记。
3. 增删 craft 文件后必须更新本 README 表格并跑 `python3 -m unittest discover -s tests`。
