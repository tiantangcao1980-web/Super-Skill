# Hermes Engineering Analysis

本分析基于用户指定的 NousResearch `hermes-agent` 项目与其官方文档。这里的 "Hermes engineering" 不是照搬 Hermes 产品，而是提炼可迁移的 agent 系统工程思想，用来升级 Super Skill 的技能、工作流和验证工具。

## 核心判断

Hermes 的关键价值不是某一个模型、某一个 UI 或某个工具清单，而是把 agent 做成一个会积累经验的运行系统：

- 技能是按需加载的程序性记忆，而不是一次性提示词。
- 记忆是有容量、有安全扫描、有分层边界的长期状态，而不是聊天记录堆积。
- 上下文被分成稳定层和临时层，以减少 token 浪费并保护缓存稳定性。
- 工具按 toolset 和执行环境分层，任务只拿到它需要的能力。
- 长任务从一次性子代理升级为可恢复、可审计、可阻塞/恢复的任务队列。
- 安全不是靠提醒模型小心，而是靠审批、沙箱、上下文扫描、会话隔离和回滚。

## 可迁移能力

| Hermes 能力 | Super Skill 转化 |
| --- | --- |
| Progressive disclosure skills | `skill-evolution-loop`, `skill-authoring-system`, compact SKILL.md pattern |
| Agent-managed procedural memory | `persistent-memory-curation`, `continuous-learning` |
| Frozen memory and prompt layer separation | `prompt-cache-layering`, `context-engineering`, `token-budgeting` |
| Toolsets and terminal backends | `toolset-sandbox-routing`, `agent-routing` |
| Kanban durable agent board | `durable-agent-board`, orchestration workflows |
| Cron and scheduled agent sessions | `observability-triage-loop`, delivery/ops workflows |
| Security approvals and blocklists | `checkpoint-rollback-safety`, `security-review`, `audit` |
| Context compression and session search | `prompt-cache-layering`, `context-engineering` |
| Provider and auxiliary routing | `agent-routing`, future model-selection checks |

## What We Borrowed

1. **Skills are live procedural memory**  
   Super Skill should not only collect skills; it should teach agents when to create, update, archive, or merge skills.

2. **Memory must be curated**  
   Durable facts, searchable history, project context, and skills should be separate stores. If everything enters always-on memory, the agent gets slower and less reliable.

3. **Context stability is an engineering target**  
   Stable prompt layers should change rarely. Logs, diffs, task-specific evidence, and temporary goals should stay late and ephemeral.

4. **Tool access is a safety boundary**  
   The best workflow gives an agent the smallest toolset that can finish the job, with sandboxing and rollback for risky operations.

5. **Long-running work needs durable state**  
   A subagent call is useful for short fork/join work. Multi-role work, retries, human unblock, and audit trails need a board or queue.

6. **Rollback is part of velocity**  
   If agents can edit fast, restoring fast is not optional. Checkpoints, worktrees, dry runs, and explicit rollback contracts are part of quality.

## Upgrade Decisions In This Repo

- Added six installable skills for memory curation, skill evolution, prompt layering, tool routing, durable boards, and rollback safety.
- Added `bin/super-skill hermes --json` to assess Hermes-inspired agent-system readiness.
- Added a `hermes` install profile that excludes those Hermes-native mirror skills when installing into Hermes Agent, avoiding duplicate procedural guidance.
- Added a Hermes engineering workflow for turning task experience into memory, skills, tools, queues, and verification.
- Kept the adaptation vendor-neutral: no dependency on Hermes runtime, Honcho, specific providers, or any one messaging platform.

## Source Notes

- [Hermes README](https://github.com/NousResearch/hermes-agent) emphasizes built-in learning loop, multi-platform continuity, scheduled automations, delegation, terminal backends, and research trajectory support.
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) describes progressive disclosure, slash-command skill loading, secure setup-on-load, external skill directories, and agent-managed skills.
- [Hermes memory documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) separates compact persistent memory from searchable session history.
- [Hermes context compression documentation](https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching) explains compression, protected tails, structured summaries, and cache pressure.
- [Hermes prompt assembly documentation](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) explains stable prompt layers, frozen memory snapshots, skills index, context files, and ephemeral layers.
- [Hermes security documentation](https://hermes-agent.nousresearch.com/docs/user-guide/security) shows the value of approval modes, hardline blocklists, sandboxing, context scanning, session isolation, and input sanitization.
- [Hermes Kanban documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban) distinguishes short subagent delegation from durable work queues with audit trails and retry/reclaim behavior.

## Implementation Principle

When a Hermes idea improves Super Skill, encode it in this order:

1. skill trigger and procedure
2. workflow handoff
3. CLI assessment or validation
4. CI gate
5. docs explaining the adaptation

Avoid adding broad prose where an enforceable check, compact skill, or deterministic workflow can carry the behavior.
