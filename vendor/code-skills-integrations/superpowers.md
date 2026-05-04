# obra/superpowers

- **URL**: https://github.com/obra/superpowers
- **License**: 见原仓库
- **类型**: Claude Code Skill 集合

## 这是什么

Geoffrey Huntley & contributors 的 Claude Code skill / agent 集合,内含 plan-loop、investigate、code-review 等"元 skill",用来塑造 Claude 的工作模式。是社区最有传染力的 skill 套件之一。

## 在 code-skills 中的对应

- **不重做** —— superpowers 已是 skill 形式,可直接软链到 `~/.claude/skills/`
- **借鉴的核心**:
  - **Plan-Loop 模式** → 体现在我们的 `ralph-loop` skill 的"循环契约 + PLAN 阶段"
  - **Verify Hard** → `ralph-loop` 的 VERIFY 必须机器可判定
  - **Honest Decide / Exit Loud** → DECIDE 三选一 + 强制退出报告
  - 详见 `ralph-loop/references/obra-superpowers.md`

## 何时用

- 想找一组高质量的"工作模式" skill
- 想给 Claude Code 装入更强的 plan / investigate 能力
- 学习"skill 应该怎么写"(superpowers 是范本)

## 怎么用

```bash
git clone https://github.com/obra/superpowers ~/superpowers
ln -s ~/superpowers/skills/<some-skill> ~/.claude/skills/<some-skill>
```

或挑感兴趣的 skill 单独 cherry-pick。

## 不集成的部分

- 不把 superpowers 的内容**复制**到本仓库(它就是 skill,git clone 即可装)
- 不修改 superpowers 的工作流,只在 ralph-loop/references 里**对照**说明本仓库做的本土化(契约、ABORT 路径、节奏 A/B/C)
