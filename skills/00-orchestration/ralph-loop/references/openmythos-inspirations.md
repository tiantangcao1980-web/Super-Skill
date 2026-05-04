# OpenMythos 思想 → Ralph Loop / Auto-Flow 工程类比

> 来源:[kyegomez/OpenMythos](https://github.com/kyegomez/OpenMythos) —— Claude Mythos 架构的开源理论重构(MIT)。
> 我们**不集成代码**(它是 PyTorch 模型实现,跟应用层抽象不在一层),但**借鉴它的几个核心思想**到 Ralph Loop 的迭代结构和 auto-flow 的幕间衔接里。
> Apache-2.0 / MIT 兼容,保留出处。

## 核心类比表

| OpenMythos 概念(模型层) | 翻译到 Claude 应用层 | 落地点 |
|--------------------------|---------------------|--------|
| **Input Injection** `h_{t+1} = A·h_t + B·e + ...` 每轮重注原始输入防漂移 | 每轮 Ralph + 每个 auto-flow 幕都 quote 原始需求 | `ralph-loop` 防漂移铁律 + `auto-flow` 幕间目标重投 |
| **Spectral radius ρ(A) < 1** 数学保证收敛 | 每轮目标距离应收敛,连续扩大 = 漂移信号,立即 ABORT | Ralph DISTANCE 字段 + 连续 2 轮扩大触发 ABORT |
| **ACT 自适应停止 + 早退** 简单输入早停,复杂深算 | Ralph 默认 ≤20 轮,DONE 立即退;按任务难度估预算 | 已有(早停规则) |
| **Loop Index Embedding** 每轮做不同的事 | PLAN/EXECUTE/VERIFY/DECIDE 阶段化 + ANCHOR/DISTANCE/ON_TRACK 强约束 | 已有 + 升级版 6 段输出 |
| **Overthinking 过度思考** 更多循环 ≠ 更好 | 跑 20 轮往往 5 轮就该停;DONE 即退 | 已有(早停) |
| **MoE shared/routed experts** 永远激活 + 按需路由 | system prompt 应有 always-on skill(coding-standards / verification-loop)+ on-demand 长尾 | 触发词精准化(SKILL.md description 严格) |
| **MLA / GQA 压缩 KV cache** 减少推理内存 | 长会话历史压缩成摘要 | 已装 strategic-compact skill |
| **Continuous Depth-wise Batching** 不同 token 不同深度退出 | 不同子任务不同 Ralph 轮数,合在一个会话 | Ralph 契约支持不同 max-iterations |
| **Loop-based regularization** 推理 vs 记忆 tradeoff | 写新功能前先查 memory(避免重复实现) | 已装 hierarchical-memory(find-feature) |
| **Latent CoT 连续空间推理** 不靠 token 输出 | 鼓励"内部 plan 后只输出关键里程碑",减少冗长 CoT | Ralph PLAN 阶段(内部思考)+ NEXT 字段(只写关键决策) |

## 三个最深刻的思想 · 工程价值排序

### ⭐⭐⭐ Input Injection —— 防漂移之根

**模型层做法**(OpenMythos):
- 每个 loop step 都把 prelude 编码后的 `e`(原始输入)重新注入 hidden state
- 没有 input injection → hidden state 会在循环中"漂走"

**应用层翻译**(本仓库):
- **Ralph Loop**:每轮 PLAN 必须从原始契约里 quote "目标 + 退出条件",不能凭记忆
- **Auto Flow**:每个幕进下一幕前,重读 `docs/0-requirements-snapshot.md` 的价值主张

**为什么这个最重要**:实战中模型最容易犯的错就是**"长流程后忘了原本要做什么"**。Input Injection 是结构性堵漏,比"叮嘱模型记住"靠谱 100 倍。

### ⭐⭐⭐ Spectral Radius < 1 —— 收敛性数学保证

**模型层做法**:
- 把循环视作 LTI(线性时不变)动态系统:`h_{t+1} = A·h_t + B·e`
- 通过参数化技巧(`A = Diag(-exp(log_A))`)保证 spectral radius `ρ(A) < 1`
- **每个发散的训练 run 都有 ρ(A) ≥ 1,每个收敛的都有 ρ(A) < 1**

**应用层翻译**:
- 不只是检测"VERIFY 输出不变"(我们之前的卡住保护),还要检测"目标距离是否单调收敛"
- **目标距离扩大 2 轮 → 立即 ABORT**(类似 ρ ≥ 1 发散)

具体落地在 ralph-loop SKILL.md 的"DISTANCE"字段 + 连续 2 轮扩大触发 ABORT。

### ⭐⭐ ACT —— 自适应计算时间

**模型层做法**:
- 每个 token 位置学一个 halting scalar
- 简单位置早退,复杂位置多算几轮
- 整体 batch 中不同 token 计算深度可以不同

**应用层翻译**:
- Ralph **默认 max=20**,但实际 DONE 时立刻退(早停)
- 不同任务给不同初始预算(简单 5 / 中等 10 / 复杂 20)
- 续轮申请书 = 模型显式举手"我需要更多 ACT 步数"

我们已有早停规则,但可以加"按任务难度预设 max"。

## 我们**没有借鉴**的部分(透明记录)

| OpenMythos 概念 | 为什么不借鉴 |
|-----------------|-------------|
| Prelude / Recurrent / Coda 三段架构 | 这是模型层架构,应用层无对应概念 |
| MLA / GQA 注意力切换 | 模型推理细节,Claude 给定不可改 |
| Mixture of Experts 实现 | 模型层,我们能做的只是"触发词精准化" |
| LoRA depth-wise 适配 | 训练侧概念,与应用工作流无关 |
| 30B token Chinchilla 调整 | 训练数据预算,不适用 |

## 出处声明

OpenMythos 是 community-driven 的**理论性**重构,作者 kyegomez 明确声明它**不**关联 Anthropic。本仓库借鉴的是其**通用思想**(Input Injection / 收敛性 / ACT),这些思想本身来自更早的学术工作:
- Universal Transformer (Dehghani et al., 2018) —— ACT 起源
- Saunshi et al., 2025 —— Looped Transformer 推理理论
- Parcae (Prairie et al., 2026) —— LTI 稳定性约束
- Bae et al., 2024 —— Recursive Transformers + LoRA

我们对 OpenMythos 团队整理这些思想到一份易读 README 表示感谢。
