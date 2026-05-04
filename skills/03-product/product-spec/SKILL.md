---
name: product-spec
description: |
  产品规格(PRD)skill:把 requirement-analysis 的 User Story 矩阵展开成完整 PRD,含 MVP 切片、roadmap、成功指标(North Star + 输入 / 输出指标)、上线 / 回滚预案。
  与 spec-workflow 协作:本 skill 偏"产品视角",spec-workflow 偏"工程 spec";二者都要写,不重叠。
  触发词:「PRD」「产品规格」「产品文档」「product spec」「MVP」「roadmap」「North Star」「成功指标」「上线计划」「回滚」。
  适用阶段:auto-flow ③ 产品幕(在 requirement-analysis 之后,设计幕之前)。
---

# Product Spec · 产品规格(PRD)

> 把"做什么"沉淀到一份**所有角色都能对齐**的文档。设计师看视觉、工程师看流程、运营看指标、老板看预算。

> 💡 **优先调用 Cowork 专家版**(若已激活):
> - `pm/feature-spec` —— 标准化 PRD 模板(问题陈述 / 用户故事 / 验收 / 指标)
> - `pm/roadmap-management` —— Now/Next/Later + 季度路线图
> - `pm/metrics-tracking` —— OKR 设定、仪表盘、NSM 选取
> - `pm/stakeholder-comms` —— 周报/月报/启动公告/风险沟通
>
> 本 skill 是**通用 fallback** —— Cowork 没装时使用;**额外贡献**:11 章 PRD 把"产品 + 工程 + 风险 + 上线 + FAQ"集成在一份,适合一人项目或小团队。

## 核心心法

PRD 不是给自己看的笔记,是**5 个角色的对齐文档**:

| 角色 | 看 PRD 找什么 |
|------|--------------|
| 设计师 | 信息架构、关键状态、限制条件 |
| 前端/后端 | 数据结构、状态机、接口 |
| QA | 验收标准、边界 case、预期错态 |
| 运营/客服 | 上线时间、FAQ、用户教育 |
| 老板/投资人 | 价值、成本、风险、指标 |

PRD 没把这 5 视角写全 = 上线后会被骂。

---

## PRD 标准模板(11 章)

```md
# <项目名> PRD v0.1

## 1. 一句话价值
<谁,在什么场景,得到什么结果>

## 2. 背景与目标
- 来自调研的关键洞察(链接 research-report.md)
- 本版本要达到的目标(可量化)

## 3. 核心场景(用户旅程)
[嵌入 requirement-analysis 的用户旅程图]

## 4. 功能列表(MVP 切片)
- ✅ MVP(v0.1):Must have 5 条
- 🔵 v0.2:Should have
- ⚪️ v0.3+:Could have
- ❌ Won't:这个版本不做的(护栏)

## 5. 详细需求(每条 User Story 一节)
### 5.1 Story 名
- JTBD: ...
- 验收: Given/When/Then
- 设计草图: 链接 Figma 或 ASCII 图
- 状态机: 5 种状态以内
- 边界 case: 列 ≥3 条
- 预期错态文案: (引用 copywriting-design)

## 6. 数据结构 / 接口契约(链 cli-design / api-design 输出)

## 7. 成功指标
- North Star: 1 个核心指标(7 日留存 / WAU / GMV ...)
- 输入指标: 3 条(我们能直接动的)
- 输出指标: 3 条(滞后但说明价值的)

## 8. 非功能需求
- 性能: 首屏 / 主操作 / API p95
- 可用性: SLA
- 安全 / 合规: GDPR / 等保 / 数据出境
- 兼容: 浏览器 / 设备 / 操作系统

## 9. 风险登记册(Risk Register)
| 风险 | 影响 | 概率 | 缓解措施 | 责任人 |

## 10. 上线计划
- 灰度方案(10% → 50% → 100% / 内部 → 外部)
- 监控点 (5 个核心指标 alert)
- 回滚条件 (出现什么就回滚)

## 11. FAQ(给客服 / 用户教育用)
- Q1: 为什么没有 X 功能? A: ...
- Q2: 数据存在哪里? A: ...
- (写 5-10 条最可能被问的)
```

---

## MVP 切片心法

### "MVP" 不是"最小可发布",是"**最小可学习**"

- ❌ MVP = "把所有功能砍一半还能跑"
- ✅ MVP = "用最小成本验证一个假设"

### 切片 3 问
1. **核心假设是什么**?(写下来一句,如:"用户愿意付 50/月")
2. **最小验证路径**?(不需要登录、不需要支付,先跑通核心动作)
3. **失败信号**?(什么数据出现说明假设挂了 → 不做了)

### 切片反模式
- 把 v1 全功能的"小一号"作为 MVP(不是切片,是阉割)
- MVP 没设 kill switch(失败了也不停)

---

## North Star Metric

每个项目**只能有 1 个 NSM**,3 条标准:

1. **能量化用户从产品获得的价值**(不是公司 KPI)
2. **领先指标**(早于收入)
3. **能拆**(可以分解到具体 feature)

| 项目类 | NSM 范例 |
|-------|---------|
| 社交 | 周活跃发帖人数 |
| 电商 | 周下单 GMV(扣退货) |
| 内容/工具 | 7 日留存 × 周使用频次 |
| SaaS | 周活账户数 × 主功能调用 |

---

## 工作流(本 skill 触发后)

1. **读输入**:requirements.md 来自 requirement-analysis
2. **填模板**:11 章每章都填,不能跳
3. **MVP 切片**:用 3 问筛掉 80% 需求
4. **NSM**:确定 1 个,3 个输入指标 + 3 个输出指标
5. **风险登记册**:至少列 5 条风险
6. **上线 + 回滚**:写到具体百分比 / 时间 / 责任人
7. **FAQ**:5-10 条
8. **落盘** → `docs/3-PRD.md`

---

## 反模式

- ❌ PRD 没"不做清单"(无护栏 → 范围爬升)
- ❌ NSM 不可量化("提升用户体验")
- ❌ MVP 是"小一号 v1"(不是切片)
- ❌ 没风险登记册(出问题就抓瞎)
- ❌ 没上线灰度(直接 100% → 出问题影响所有人)
- ❌ 没 FAQ(客服周一炸)

---

## 与其他 skill 关系

| skill | 关系 |
|-------|------|
| `requirement-analysis` | 上游,提供 requirements.md |
| `spec-workflow` | 协作 — 本 skill 是产品 PRD,spec-workflow 是工程 spec,两份都要写 |
| `design-templates` | 下游,从本 PRD 抽视觉规范 |
| `cli-design` / `api-design` | PRD 第 6 章引用其输出 |

---

## References

- [PRD 完整范例(SnapMatte)](references/prd-example.md)
