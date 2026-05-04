# Dev Tool, Model, and Memory Adaptation

Super Skill 的可移植策略是：技能只写一次，运行时只做适配；模型只换能力档案，不换质量契约；记忆只沉淀经过验证的经验，不把历史全部塞进上下文。

## Tool Adapter Matrix

| Tool | Native Surface | Super Skill Strategy | Risk |
| --- | --- | --- | --- |
| Codex | `AGENTS.md`, `.agents/skills`, plugins | 根规则放 `AGENTS.md`，技能用 canonical `SKILL.md`，可分发集合再打包成插件。 | 技能数量过多会挤占初始技能列表，需要短描述和 profile。 |
| Claude Code | `CLAUDE.md`, `.claude/skills`, user skills | 直接安装 `SKILL.md` 技能，`CLAUDE.md` 只放项目级协议。 | 命名冲突和 supporting files 路径需要检查。 |
| Cursor | `.cursor/rules/*.mdc`, `AGENTS.md` | 把 always-on 约束压缩成 rules，把长流程保持为可引用技能文档。 | rules 常驻上下文，过长会稀释任务信号。 |
| Trae | `.rules`, MCP config | 把协作规范、模型约束、工具边界写入 rules，把外部工具交给 MCP。 | `.rules` 语法和 UI 支持仍需跟随官方更新验证。 |
| OpenCode | `opencode.json`, `.opencode/agents`, `.opencode/skills` | 用 JSON 管模型、权限和默认 agent；用 skills 放可复用流程。 | 权限矩阵若过宽，会破坏 harness 的最小工具原则。 |
| OpenClaw | `~/.openclaw/skills`, workspace `skills`, plugins | 安装 canonical skill folder，项目覆盖放 workspace。 | 社区技能安全风险高，必须审计来源和工具权限。 |

## Model Adaptation Contract

每个模型或运行时都必须通过同一份质量约束：

- 输入包含目标、用户期待、当前状态、上下文来源、限制、验收标准、输出结构、验证要求和 token 预算。
- 输出必须映射回交付结果、变更文件、证据、风险和已知缺口。
- 工具调用、结构化输出、长上下文、低成本任务分别用独立 eval 检查。
- 模型切换不自动视为升级；只有通过兼容门和回归样例后才能成为默认路由。

## Memory And Dreaming

记忆系统分为五层：

- episodic traces: 原始会话、命令、diff、错误和评审记录，按需检索。
- semantic memory: 经验证的事实和决策，带日期、来源和适用范围。
- procedural memory: 已验证的技能、runbook、脚本和清单。
- evaluation memory: 回归样例、rubric、benchmark 和失败模式。
- negative memory: 被拒绝方案和已知反模式，短小、可检索、不过度加载。

Dream loop 是离线学习机制：

1. 收集 trace。
2. 脱敏和分类。
3. 压缩为候选记忆。
4. 离线 replay 或 simulation。
5. 修改 skill、prompt、工具配置或 eval。
6. 和基线比较。
7. 只把有证据提升的内容提升为 durable memory。

## Harness Closure

这套适配最终服务一个闭环：

```text
Intent -> Context -> Tool Adapter -> Model Contract -> Build -> Verify -> Observe -> Memory -> Dream Replay -> Skill Evolution -> Intent
```

如果 agent 失败，修复对象优先级是：

1. 缺失的验收契约。
2. 缺失或过载的上下文。
3. 错误的工具/权限/运行时适配。
4. 错误的模型路由。
5. 缺失的测试、eval 或观测信号。
6. 应沉淀但没有沉淀的记忆。

这让“记忆力”变成工程能力，而不是越来越长的 prompt。
