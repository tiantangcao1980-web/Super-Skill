---
name: goal-driven-workflow
description: |
  Codex /goal 风格的持久目标工作流:把模糊需求转成可审计 goal contract,再用 OpenSpec/SDD、Ralph Loop、code-simplifier、completion audit 和 memory/dream replay 形成长任务闭环。
  适用场景:长程开发、跨会话任务、规格驱动实现、复杂重构、批量修复、需要 token budget/Stop if/Done when 的任务。
  触发词:「/goal」「goal」「目标模式」「持久目标」「长期任务」「OpenSpec」「SDD」「spec-driven」「Ralph loop++」「跑到完成」。
---

# Goal-Driven Workflow

这个 skill 把 Codex `/goal` 的持久目标能力、goal-prompt-builder 的审计友好提示结构、OpenSpec 的规格驱动开发、Super Skill 的 `ralph-loop` 和 `code-simplifier` 合成一条可落地工作流。

核心判断: `/goal` 不是“更长的 prompt”,而是一个 **持久目标 + 预算 + 完成审计 + 证据映射** 的运行契约。Ralph Loop 负责会话内迭代质量,`/goal` 负责跨轮持续目标和预算边界,OpenSpec 负责把需求变成可枚举规格。

## 何时使用

- 用户要求“持续做直到完成”“别停”“长任务自动推进”。
- 任务复杂到需要跨多轮、跨会话或上下文压缩。
- 用户提到 `/goal`、OpenSpec、SDD、spec-driven、Ralph loop、goal prompt。
- 需求已经有 `openspec/changes/<id>/`、PRD、tasks、design、issue checklist。
- 你担心 false completion: 看似完成,但没有逐条映射到 artifact/test/evidence。

## 先选路线

1. **简单明确任务**: 直接生成 goal contract,再执行。
2. **模糊复杂任务**: 先用 Plan/`intent-contract`/`product-spec` 明确需求,再生成 goal contract。
3. **规格驱动任务**: 先用 OpenSpec/SDD 产出 proposal/specs/design/tasks,再把规格目录作为 goal 的第一输入。

## Goal Contract 模板

每个持久目标都必须包含 6 段:

```text
/goal <one concrete objective>

First action: <optional read/report step for SDD or brownfield work>

Scope:
- <files, directories, subsystem, or explicit out-of-scope>

Constraints:
- <project rules, safety boundaries, model/tool limits>

Done when:
1. <file, command, test, metric, or artifact evidence>
2. <...>

Stop if:
- <mechanically detectable condition>

Use a token budget of <N> tokens for this goal.
```

硬规则:

- 不放过“优化、提升、全面、彻底、all、everything”这类模糊词,除非它们被转成可枚举 artifact。
- `Done when` 至少 3 条,每条必须能引用文件、命令、测试、指标或可审查产物。
- `Stop if` 至少 3 条,必须可机械检测,不要写“如果不清楚就停”。
- 涉及测试代码时,必须有“现有测试失败不能通过削弱/删除测试来修”的 guard。
- SDD/OpenSpec 目标的第一步必须读规格文件并报告 counts,暴露上下文加载失败。

## 与 Ralph Loop 的分工

`/goal` 层:

- 目标持久化
- token budget
- 跨轮 continuation
- 完成前 prompt-to-artifact audit
- budget exhausted 时收尾

`ralph-loop` 层:

- 单轮 PLAN → EXECUTE → VERIFY → DECIDE
- 每轮 anchor 原始目标
- 目标距离与防漂移
- 失败重试和硬退出

推荐组合:

```text
Goal Contract → SDD/Spec Loading → Ralph Loop implementation → Code Simplifier → Output Quality Gate → Memory/Dream Candidate
```

## OpenSpec/SDD 路线

如果项目已有 OpenSpec:

1. 读 `openspec/changes/<change>/proposal.md`、`design.md`、`tasks.md`、`specs/`。
2. 报告文件数、task 数、SHALL/GIVEN/WHEN/THEN 数。
3. 把每条 task 和 SHALL 映射到 Done when。
4. 把冲突 SHALL、MUST NOT 文件、新依赖、测试回归放进 Stop if。
5. 实现完成后 archive 或更新规格,不要只改代码。

详见 [`references/openspec-sdd.md`](references/openspec-sdd.md)。

## CLI 快速生成

本仓库提供一个轻量生成器:

```bash
bin/super-skill goal \
  --objective "Implement openspec/changes/add-rerank exactly as specified" \
  --sdd-path openspec/changes/add-rerank \
  --scope "openspec/changes/add-rerank; src/retrieval; tests/retrieval" \
  --done "Each task in openspec/changes/add-rerank/tasks.md is checked off with file evidence" \
  --done "Each SHALL has a passing test name cited in tests/retrieval" \
  --done "`npm test` exits 0 and summary is pasted" \
  --stop-if "A SHALL conflicts with another SHALL in specs/" \
  --stop-if "A new dependency requires npm install" \
  --stop-if "git diff touches auth/ or billing/ outside scope" \
  --budget 120000
```

## 完成审计

在宣布完成前,逐条做 completion audit:

1. 复述 objective 为具体交付物。
2. 建立 prompt-to-artifact checklist。
3. 对每个 Done when 找真实证据: 文件、命令输出、测试、截图、PR 状态或规格 archive。
4. 检查测试/manifest/verifier 是否真的覆盖目标,不要把“绿了”当成代理完成信号。
5. 任何一条缺证据,继续执行或明确报告未完成。

## 收尾

目标达成后再调用:

- `code-simplifier`: 删除临时适配、重复代码、死码和过度抽象,不改行为。
- `output-quality-gate`: 把最终输出映射回用户目标、证据和已知风险。
- `agent-memory-dream-loop`: 只沉淀经验证、去重、可审查的经验候选,不保存 raw prompt/response。

## References

- [Goal contract details](references/goal-contract.md)
- [OpenSpec SDD adapter](references/openspec-sdd.md)
- [Codex /goal integration notes](../../../docs/codex-goal-integration.md)
