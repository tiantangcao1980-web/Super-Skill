---
name: ralph-loop
description: |
  Ralph Wiggum 迭代循环引擎:明确退出条件 → 小步执行 → 自动验证 → 决定继续或停止。
  适用场景:长任务自动迭代、构建/测试反复跑、PR 反复打磨、批量修复、任何"做完一遍还要再做一遍"的工作。
  触发词:「Ralph」「循环」「迭代」「跑直到」「自动重试」「持续做 X 直到 Y」「loop」「until」。
  与 /loop 命令的区别:/loop 是节奏调度(跨会话);本 skill 是一次会话内的循环工作模式 + 退出判定 + 单步质量门。
---

# Ralph Loop · 拉尔夫循环

> 命名梗源自 obra/superpowers:Ralph Wiggum 一遍又一遍说同样的话,但每遍都更接近答案。
> 工程化之后,它是一种**带退出条件、带验证门、带进度报告**的迭代工作模式。

## 核心模式

```
PLAN → EXECUTE → VERIFY → DECIDE
  ↑                          │
  └──── continue ────────────┘
       └──── done ────────── EXIT
```

每个迭代必须包含四步:

| 步骤 | 内容 | 产出 |
|------|------|------|
| **PLAN** | 本轮做什么、做完什么样算"过" | 一段待办 + 一句过关标准 |
| **EXECUTE** | 最小步骤完成本轮目标 | 代码/配置改动 |
| **VERIFY** | 跑构建、测试、类型、lint、截图比对 | 命令输出 + pass/fail |
| **DECIDE** | 根据 VERIFY 三选一 | DONE / CONTINUE / ABORT |

**没有 VERIFY 的循环不是 Ralph Loop,是无脑重试。**

---

## 三种节奏

按场景选,详见 [references/loop-patterns.md](references/loop-patterns.md):

- **节奏 A · 自适应**(默认):每轮根据上一轮状态决定下一轮内容
- **节奏 B · 固定间隔**:每 N 分钟跑一次(配合 ScheduleWakeup 或 /loop 命令)
- **节奏 C · 触发式**:等外部信号(hook、文件变更、上游依赖完成)再跑

---

## 启动前必填:循环契约

**没有契约不准开循环**。契约模板:

```
【Ralph Loop 契约】
目标: <一句话,客观可判定>
退出条件: <可机器验证的指标,例如 "npm test 全过 + 类型检查无错">
单步耗时上限: <例如 5 分钟>
最大迭代数: <例如 8 轮>
卡住判定: <例如 "连续 3 轮 VERIFY 输出无变化">
验证手段: <bash 命令 / 测试套件 / 截图比对>
```

契约写完直接复述给用户,得到默认 OK 才开始。

---

## 默认上限:20 轮(硬规则)

**未指定 `--max-iterations` 时,默认上限就是 20。** 这不是建议,是工程经验下来的硬数:

| 任务难度 | 通常落点 |
|---------|---------|
| 简单 bug / 单测试通过 | 1-3 轮 |
| 中等(1 个新功能 + 测试) | 4-8 轮 |
| 复杂(多文件、跨层) | 9-15 轮 |
| **>20 轮 = 强信号:方向错了** | 必须停下重新评估 |

### 早停(达成即退,不准跑满)
- 测试全绿 → DONE,**第 3 轮退也行**
- 退出条件命中 → DONE,**第 5 轮退也行**
- 跑越多轮 ≠ 越好。**多余的轮次 = 多余的代码 + 多余的回归风险**

### 卡住保护
- 连续 **3 轮** VERIFY 输出**完全相同** → 自动 ABORT
- 连续 2 轮 NEXT 字段一字不变 → 也算卡住
- 卡住 = 立即退出 + 报告,**不准再赌**

### 超 20 轮:强制申请书

到第 20 轮还没 DONE,**禁止自动续命**。必须 ABORT 当前循环,向用户提交一份**续轮申请书**(没申请书 = 不准继续):

```
【Ralph Loop 续轮申请】
当前进度: 已完成 X / 还差 Y
卡点: <具体卡在哪>(贴第 20 轮 VERIFY 输出)
已尝试方案: [A 试过失败因 ___, B 试过失败因 ___, C 试过失败因 ___]
需要追加: 建议 N 轮(N ≤ 10)
理由: 因为 <具体原因>,本次问题需要 <具体粒度> 的迭代,前 20 轮已经 <具体进展>
风险评估: 如果再 N 轮还不够,意味着方向错了,建议人工介入
人工选项: [A. 同意续 N 轮 / B. 同意但只续 M 轮 / C. 改方向(请描述) / D. 拒绝,我手动接管]
```

**只有用户明确选 A/B/C 后,才能继续。** 用户没回复 = 视为 D,收摊。

不准:
- ❌ 不申请就续(直接死)
- ❌ 申请书理由含糊("还差一点点")
- ❌ 一次申请 N > 10(说明方向错了,不是轮数问题)
- ❌ 申请被拒后偷偷继续

---

## 防漂移铁律(Input Injection)⭐

> 灵感:OpenMythos / Recurrent-Depth Transformer 的 input injection 机制 —— 每轮把原始输入 `e` 重新注入 hidden state,**防止迭代过程中"忘了原本要做什么"**。
> 详见 [`references/openmythos-inspirations.md`](references/openmythos-inspirations.md)。

### 4 项硬约束

每一轮都必须做,**做不到 = 这一轮不算数,自动重做**:

1. **每轮 PLAN 阶段必须 quote 原始契约的"目标 + 退出条件"** —— 不能凭记忆写,必须从契约里读
2. **每轮 VERIFY 阶段必须算"目标距离"** —— 当前产出离原始目标多远(具体差几个 case / 几条需求)
3. **连续 2 轮目标距离扩大 → 自动 ABORT** —— 类比 spectral radius ρ(A) ≥ 1 发散,**不许硬撑**
4. **DECIDE 之前最后一行必须写"是否仍在原始轨道"** —— ✅/🔄/⚠️/❌

### 为什么必须

迭代到第 5-10 轮时,模型会:
- 修一个 case 顺手"优化"另一处(范围爬升)
- 把临时品当成主线(目标偏移)
- 改测试让它过(目标妥协)
- 解决了次要问题但忘了主问题(轨道偏离)

**Input Injection** 强约束每轮重新对齐原始 e,把这些都堵掉。

### 单轮输出格式(升级版)

每轮输出必须含 6 段(原 5 段 + 新增"目标距离"和"轨道检查"):

```
🔁 Iteration <N>/<MAX>
ANCHOR: <quote 原始契约的目标 + 退出条件,不超过 50 字>
PLAN: <这轮要做什么 + 为什么这是离 ANCHOR 最短路径>
EXECUTE: <做了哪些事 / 改了哪些文件>
VERIFY: <命令 + 结果摘要,失败用例最多 3 条>
DISTANCE: <当前距离 ANCHOR 多远;格式:"X/Y 项达成,差: a,b,c">
DECIDE: ✅ DONE | 🔁 CONTINUE | ⛔ ABORT
ON_TRACK: ✅ 在轨 | 🔄 微偏(<10%) | ⚠️ 偏离 | ❌ 漂移(立即 ABORT)
NEXT (if CONTINUE): <下一轮要做什么 + 为什么这么做>
```

**DECIDE 必须三选一,不能模糊**;**ON_TRACK 出 ❌ 必须 ABORT,不接受 CONTINUE**。

---

## 单轮执行(简版,无防漂移要求时)

如果是非常短的循环(≤3 轮),可以省去 ANCHOR/DISTANCE/ON_TRACK,用简版:

```
🔁 Iteration <N>
PLAN: <这轮要做什么>
EXECUTE: <做了哪些事 / 改了哪些文件>
VERIFY: <命令 + 结果摘要,失败用例最多 3 条>
DECIDE: ✅ DONE | 🔁 CONTINUE | ⛔ ABORT
NEXT (if CONTINUE): <下一轮要做什么 + 为什么这么做>
```

**默认用上面的升级版**,简版仅用于"已知 ≤3 轮就完"的场景。

---

## 退出与收尾

退出时输出:

```
【Ralph Loop 退出报告】
退出原因: DONE / ABORT(原因)
实际迭代轮数: N
最终验证结果: <pass/fail 摘要>
改动文件: <列表>
遗留问题: <未解决的,给出建议>
建议下一步: <用户视角>
```

---

## 典型场景示例

### 场景 1:把测试跑绿
```
目标: 让 packages/api 全部测试通过
退出条件: pnpm --filter api test 退出码 = 0
最大迭代数: 6
卡住判定: 连续 2 轮失败用例集合不变
验证手段: pnpm --filter api test
```

### 场景 2:首页视觉回归到设计稿
```
目标: /home 页面截图与 designs/home.png 视觉差 < 5%
退出条件: pixelmatch 输出 diff < 5000 像素
最大迭代数: 5
验证手段: playwright screenshot + pixelmatch
```

### 场景 3:批量修复 lint 错误
```
目标: ESLint 0 error 0 warning
退出条件: pnpm lint 输出 "0 problems"
最大迭代数: 4
卡住判定: 单轮修复后 error 数不下降
验证手段: pnpm lint
```

---

## 反模式 · 不要这样

- ❌ **闷头跑不报告**:每轮都要给用户看 DECIDE 状态
- ❌ **改了再改不验证**:VERIFY 是循环的灵魂
- ❌ **退出条件含糊**:「直到代码 OK」不是退出条件,「直到 npm test 全过」才是
- ❌ **滥用循环**:一次能搞定就别循环,Ralph 解决"必须多轮"的问题
- ❌ **改测试让验证过**:验证手段一旦定了就不能为了"过"去改它(用户授权的真 bug 修复除外)
- ❌ **吞掉错误继续跑**:VERIFY 失败要么修要么 ABORT,不能假装看不见

---

## 与其他 skill 的关系

- **被 `design-dev-flow` 调用**:在前/后端实现幕里负责循环到 done
- **退出后调 `code-simplifier`**:循环过程中难免堆冗余,退出后做一次清扫
- **配合 `verification-loop`**:对方提供具体语言的验证命令清单,本 skill 提供循环结构

---

## 内置 Plugin(可执行机制 ≠ 文档)

本 skill 不仅是文档,**还内置了一份可运行的 Plugin**(`plugin/` 子目录),
源自 Anthropic 官方 [`claude-plugins-official/ralph-loop`](https://github.com/anthropics/claude-plugins-official),Apache 2.0,attribution 见仓库根 `NOTICE`。

Plugin 用 **Stop hook 拦截会话退出 + 重写 prompt 反馈**实现真正的循环 ——
比"由模型自己自觉循环"可靠得多。状态写在项目的 `.claude/ralph-loop.local.md`。

### 安装(独立于 skill 安装)

```bash
ralph-loop/scripts/install-plugin.sh install     # 软链到 ~/.claude/plugins/code-skills/ralph-loop
ralph-loop/scripts/install-plugin.sh status      # 查看状态
ralph-loop/scripts/install-plugin.sh uninstall   # 卸载
```

或用统一入口:`bin/code-skills plugin install ralph-loop`(见 README)。

### 使用(plugin 装好之后)

```
/ralph-loop "Build X. Output <promise>DONE</promise> when complete." --max-iterations 20 --completion-promise "DONE"
/cancel-ralph        # 取消活跃循环
```

### Plugin 与 SKILL.md 的关系

| 内容 | 来源 | 角色 |
|------|------|------|
| 工作流 / 反模式 / 退出条件 | 本 SKILL.md(原创) | **怎么思考**(给模型读) |
| Stop hook + 状态文件 + 命令解析 | `plugin/`(Anthropic 官方移植) | **怎么执行**(给系统跑) |

skill 单独使用 → 你**手动**遵循 Ralph 模式;plugin 装上 → 系统**强制**循环。两层互补。

依赖:`bash`、`jq`、`perl`(macOS / Linux 默认就有,Windows 见 `plugin/PLUGIN-README.md`)。

---

## References

- [循环节奏与场景](references/loop-patterns.md)
- [obra/superpowers 模式借鉴](references/obra-superpowers.md)
- [OpenMythos 思想类比(Input Injection / 收敛性 / ACT)](references/openmythos-inspirations.md) ⭐
- [内置 Plugin 原始 README](plugin/PLUGIN-README.md)
