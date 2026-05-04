# everything-claude-code

- **URL**: https://github.com/affaan-m/everything-claude-code
- **License**: 见原仓库
- **类型**: Claude Code 资源 awesome 列表

## 这是什么

社区维护的 Claude Code 全家桶导航:plugins / skills / hooks / agents / 教程 / 博客 / 工具,按场景分类。核心价值是"少走弯路" —— 想做某个事,先看这里有没有现成的。

## 在 code-skills 中的对应

- **对应 skill**:`claude-code-resources`
- 借鉴的核心:**用户场景 → 最相关资源**的映射,而不是 dump 全列表。
  我们的 skill 强制"最多推荐 3 个,本地优先"。

## 何时用

- 找现成的 plugin / skill,不重复造轮子
- 学习 hook / sub-agent 怎么写(看真实例子)
- 给团队推荐"要装的几个 Claude Code 工具"
- 想看 Claude Code 社区在做什么

## 怎么用

直接触发 `claude-code-resources` skill,告诉它你的场景。例如:

> "我想写一个会自动记笔记的 hook,有现成的吗"
> → 先查 `~/.claude/skills/`,再查 superpowers,再查 awesome 列表

## 不集成的部分

- everything-claude-code 全列表的 mirror(我们只做映射,不做镜像)
- 链接质量校验(假设上游列表已审过,我们不二次审核)
- 自动同步(列表更新频率高,本仓库不订阅 — 用户问的时候我们去看)
