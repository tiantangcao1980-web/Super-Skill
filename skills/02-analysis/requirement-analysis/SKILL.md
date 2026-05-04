---
name: requirement-analysis
description: |
  需求分析 skill:把 research-report.md 的"洞察"转成可执行的"需求"。覆盖 JTBD(Jobs To Be Done)、User Story、用户旅程、优先级矩阵(MoSCoW + RICE)。
  与 spec-workflow 协作:本 skill 输出"做什么 + 为什么",spec-workflow 把"做什么"展开成工程 spec。
  触发词:「需求分析」「JTBD」「User Story」「用户故事」「用户旅程」「优先级」「MoSCoW」「RICE」「需求拆分」「需求评审」。
  适用阶段:auto-flow ② 分析幕(在 user-research 之后,product-spec 之前)。
---

# Requirement Analysis · 需求分析

> 调研给的是**洞察**,产品给的是**功能**。本 skill 是中间那一步:**把洞察压成可决策的需求矩阵**。

> 💡 **优先调用 Cowork 专家版**(若已激活):
> - `pm/user-research-synthesis` —— 访谈/数据合成成主题 + 机会点
> - `pm/roadmap-management` —— RICE / MoSCoW / ICE / Now-Next-Later 排序
>
> 本 skill 是**通用 fallback** —— Cowork 没装时用,且把 JTBD + Story + 用户旅程 + 双视图优先级**串成一份完整文档**。

## 输入 / 输出

```
输入: docs/1-research-report.md (来自 user-research)
输出: docs/2-requirements.md
       含 JTBD + User Story + 用户旅程 + 优先级矩阵
```

---

## JTBD(Jobs To Be Done)模板

每个核心洞察 → 1 条 JTBD,**不写功能,写动机**:

```
当我 <情境>,
我想 <动机/目标>,
这样我可以 <预期结果>。
```

### 例(SnapMatte)
```
当我 截图发文档时,
我想 自动加优雅留白和水印,
这样我可以 不用打开 Photoshop,5 秒就能贴进 README。
```

### 反例
```
❌ "用户需要一个截图工具"  → 这是功能,不是 Job
❌ "提升用户体验" → 太泛,无可执行性
```

---

## User Story 拆分

每条 JTBD → N 条 User Story:

```
作为 <角色>,
我想要 <能力>,
这样我可以 <价值>。

验收标准:
- Given 前置条件
- When 操作
- Then 期望结果
```

### 切分规则
- **INVEST**:Independent / Negotiable / Valuable / Estimable / Small / Testable
- **每个 Story ≤ 1 天工作量**(超过就拆)
- **必有验收标准**(没有 = 不可估)

---

## 用户旅程(User Journey)

主要场景画一张图,横轴时间,纵轴 4 行:

```
| 阶段     | 发现 | 注册 | 首次使用 | 重复使用 | 推荐他人 |
| 用户行为 | ... | ... | ... | ... | ... |
| 用户情绪 | 😐  | 😀  | 🤔  | 😀  | 🥳  |
| 痛点     | _   | 表单太长 | 不知道怎么开始 | _ | _ |
| 机会     | _   | OAuth 一键 | 引导步骤 1-2-3 | _ | 推荐奖励 |
```

每个**痛点**对应一条新需求,放进优先级矩阵。

---

## 优先级矩阵(双视图)

### 视图 A · MoSCoW(粗排)

| 类 | 含义 | 数量上限 |
|----|------|---------|
| **M**ust have | 不做就不能上 | ≤ 5 |
| **S**hould have | 该有,可挪到下版本 | ≤ 8 |
| **C**ould have | 锦上添花 | 不限 |
| **W**on't have | 这版本明确不做 | 越多越好(收敛) |

### 视图 B · RICE(细排)

每条 Story 打 RICE 分:

```
RICE = (Reach × Impact × Confidence) / Effort

Reach:     影响多少用户(人/月)
Impact:    单用户影响(0.25 / 0.5 / 1 / 2 / 3)
Confidence: 我们对前两项的把握(50% / 80% / 100%)
Effort:    工程预算(人月)
```

按 RICE 排序,**前 5 条进 v0.1**,其余下版本。

---

## 工作流(本 skill 触发后)

### Step 1 · 读 research-report
找出**共性洞察**(≥3 人提到)和**异常洞察**(1 人但有价值)。

### Step 2 · 转 JTBD
共性 1-1 对应到 JTBD 1 条。异常洞察先记到"探索池"。

### Step 3 · 拆 User Story
每条 JTBD 拆 2-5 条 Story。每条配验收标准。

### Step 4 · 画用户旅程
至少 1 个核心场景。识别痛点 → 补 Story。

### Step 5 · 优先级双视图
MoSCoW 粗筛 + RICE 细排。给出 v0.1 必做清单(≤ 5 条 Must)。

### Step 6 · 输出
落盘 `docs/2-requirements.md`,交给 product-spec 做 PRD。

---

## 反模式

- ❌ JTBD 写成"用户需要 X 工具"(不是 Job 是 Want)
- ❌ User Story 没验收标准
- ❌ MoSCoW 里 Must have 写 20 条(等于没排)
- ❌ RICE 拍脑袋打分(Reach 没数据 → confidence 低,要标出来)
- ❌ 跳过用户旅程(只看功能列表会漏掉过程痛点)
- ❌ 上来就开始拆功能,跳过 JTBD(失去动机层抽象)

---

## 与其他 skill 关系

| skill | 关系 |
|-------|------|
| `user-research` | 上游,提供 research-report.md |
| `product-spec` | 下游,把需求矩阵展开成 PRD |
| `spec-workflow` | 协作 — 本 skill 给"做什么",spec-workflow 给"工程 spec" |
| `hierarchical-memory` | 把高频 JTBD 沉淀,跨项目复用 |

---

## References

- [JTBD + User Story 完整示例](references/jtbd-examples.md)
