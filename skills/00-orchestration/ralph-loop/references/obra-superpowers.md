# obra/superpowers 模式借鉴

> 我们没有复制 superpowers 的代码,只是把它**最有传染力的核心模式**抽出来落地。

## 借鉴点 1:Plan Loop · 计划循环

superpowers 强调:**先写计划,再执行;每轮执行后 update 计划。**

我们落地为 Ralph Loop 的"循环契约"+ 每轮 PLAN 阶段:
- 契约是**总计划**
- 每轮 PLAN 是**当下计划**
- 计划必须**写下来**(给用户看),不能只在脑子里想

这个机制的核心收益:**强制 agent 先思考再动手**,避免 LLM 的"边想边做边后悔"病。

---

## 借鉴点 2:Verify Hard · 强验证

superpowers 的另一个心法:**验证手段必须是机器可判定的**,人眼判断不算。

落地为 Ralph Loop VERIFY 阶段的硬要求:
- 必须有 bash 命令、测试、或脚本输出
- "看起来 OK"不算 VERIFY
- 失败用例要列具体名字,不能只说"还有些错"

---

## 借鉴点 3:Honest Decide · 诚实决策

superpowers 反对"差不多了"的暧昧汇报。

落地为 DECIDE 三选一:
- **DONE**:验证 100% 通过
- **CONTINUE**:有进展但未达成,**说出下一轮要做什么**
- **ABORT**:无进展或资源耗尽,**说出原因**

不准有第四种状态。"快了""差不多""应该 OK"——都不是合法 DECIDE。

---

## 借鉴点 4:Exit Loud · 大声退出

superpowers 强调:循环结束**必须有完整报告**,而不是悄悄停下。

落地为 Ralph Loop 退出报告:
- 改了哪些文件
- 实际跑了几轮
- 验证最终状态
- 遗留问题(必填,即使是空也要写"无")
- 建议下一步(必填)

理由:LLM 长任务最容易"跑着跑着忘了交代"。强制退出报告,把这件事变成肌肉记忆。

---

## 我们做的本土化

| superpowers 概念 | code-skills 落地 |
|-----------------|------------------|
| Plan Loop | Ralph Loop 契约 + PLAN |
| Verify | VERIFY 阶段 + 验证手段强制可机器判定 |
| Update Plan | 每轮 NEXT 字段(给下一轮的 PLAN 输入) |
| Reflect & Stop | DECIDE 三选一 + 退出报告 |
| —(superpowers 没强调) | 卡住判定 + ABORT 路径 |
| —(superpowers 没强调) | 三种节奏(A/B/C)区分 |

## 不照搬的地方

- superpowers 里很多 prompt 工程细节(如特定的 system prompt 模板)→ **不抄**,我们的运行环境不同
- superpowers 偏向"agent 自治"语境,我们偏向"agent + user 协作"语境 → 我们的契约要**反复回报给用户**,不是闷头跑
- superpowers 没硬性规定单轮预算和卡住检测 → 我们补上了,因为实战里这两个最容易翻车
