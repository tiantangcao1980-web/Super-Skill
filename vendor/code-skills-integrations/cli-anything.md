# CLI-Anything

- **URL**: https://github.com/HKUDS/CLI-Anything
- **License**: 见原仓库
- **类型**: CLI 方法论 / "把任意能力 CLI 化"

## 这是什么

由 HKUDS 提出的方法论:**任何"输入 → 处理 → 输出"流程都能 CLI 化**,前提是按一致的命令命名、退出码、JSON schema 暴露能力。本质上是把 LLM 能力(或任意服务)封装为标准 CLI,从而让 agent / pipeline 能编排。

## 在 code-skills 中的对应

- **对应 skill**:`cli-design` skill 的"CLI-Anything 5 步法"章节
  1. 抽离核心动作(动词)
  2. 确定操作对象(名词)
  3. 最小输入(只必填)
  4. 双输出(人 + 机)
  5. 可分发包装(npm/pip/brew/installer)
- **`bin/code-skills cli-init` 命令**:把 5 步法的产出 scaffold 成代码骨架

## 何时用

- 想把一个 LLM agent / 服务暴露给非 AI pipeline
- 想让某个能力可以被脚本编排(cron / Makefile / GitHub Action)
- 已有 web UI / 库,要补一个 CLI 入口

## 怎么用

```bash
bin/code-skills cli-init my-llm-tool
cd my-llm-tool
# 参考 INTERFACE.md 填命令树,实现 scripts/<verb>.py
```

## 不集成的部分

- 框架级 LLM 包装层(那是 `claude-api` skill / `cloudbase-agent-ts` skill 的事)
- 具体 LLM 选型决策(参见 `ai-model-*` skill)
