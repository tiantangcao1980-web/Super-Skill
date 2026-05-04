# Leonxlnx/taste-skill

- **URL**: https://github.com/Leonxlnx/taste-skill
- **License**: 见原仓库
- **类型**: Claude Code Skill(审美/品味维度)

## 这是什么

把"产品审美"做成可复用 skill:用一组维度(独特性/对比度/留白/字号差/动效克制)给 UI 打分,识别"通用 AI 美学"的反模式,推动设计走向有记忆点的方向。

## 在 code-skills 中的对应

- **不重做** —— taste-skill 已是 skill 形式
- **借鉴的核心**(吸纳进 `design-dev-flow/references/design-taste.md`):
  - **审美自检清单 10 条**(5 秒能记住一个特征?logo 遮住能否认出?...)
  - **"通用 AI 美学"反模式**(顶部 logo + 居中 hero + 三列卡片)
  - 与 `huashu-design`、`awesome-design-md` 共同构成 design-dev-flow ② 设计幕的判定基准

## 何时用

- 设计稿出来后做"独特性体检"
- 审 AI 生成的 UI(几乎一定踩反模式)
- 设计师内部 review 时统一标准
- 给非设计师同学一个"能不能上线"的简单判断

## 怎么用

```bash
git clone https://github.com/Leonxlnx/taste-skill ~/taste-skill
ln -s ~/taste-skill ~/.claude/skills/taste-skill
```

或在 `design-dev-flow` ② 设计幕里直接走我们的 `design-taste.md` 自检清单。

## 不集成的部分

- 不把 taste-skill 内容复制(直接装即可)
- 不替代 ui-design / designdna(它们是更大的设计 skill,taste 是其中一个评估维度)
