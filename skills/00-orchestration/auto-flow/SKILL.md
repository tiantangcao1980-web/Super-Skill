---
name: auto-flow
description: |
  端到端工作流自动化:用户给一句需求,本 skill 串联 9 个 skill + 2 个 plugin,从需求澄清一直跑到交付。
  Phase 0 强制做需求"完整性 + 可行性" gate(11 项必填,缺一项就回问用户,**不放行**);通过后自动进 7 幕,每个开发幕用 ralph-loop(默认 20 轮)+ code-simplifier 配合;最终交付。
  中间默认不打扰用户,**仅在 6 个预设触发点停下来**:需求不全 / Ralph 超 20 轮 / 卡住 / 付费决策 / 破坏性操作 / 验证 ❌。
  触发词:「全自动开发」「auto-flow」「从需求到交付」「自动化全流程」「我只想提需求」「auto pilot」「自动跑」「全流程自动」「一条龙」「端到端开发」。
  本 skill 是 design-dev-flow 的**驱动器**:design-dev-flow 是声明式 7 幕,auto-flow 让它真的跑起来。
---

# Auto Flow · 端到端自动工作流

> 一句话:**用户提需求 → Phase 0 gate → 7 幕自动跑 → 交付**。
> 中间默认不打扰用户,除非命中 6 个预设触发点。

## 调度全图(9 幕版)

```
        ┌────────────────────────────────────┐
        │ Phase 0: 需求 Gate(必过,11 项)   │
        └────────────────────────────────────┘
                          │
  ① 调研 ─→ ② 分析 ─→ ③ 产品 ─→ ④ 设计 ─→ ⑤ 接口 ─→ ⑥ 前端 ─→ ⑦ 后端 ─→ ⑧ 测试 ─→ ⑨ 交付
  user-     req-       product-   design-   cli-/api-  Ralph     Ralph     qa-       Cowork
  research  analysis   spec       templates  design    +simp     +simp     strategy  pptx/docx
            +spec-     +spec-     +copy-                                              /pdf/xlsx
            workflow   workflow   writing                                             +simp 全量
                                  +ui-design                                          +deploy
                                  +designdna                                          +demo
```

**辅助/工具型 skill**(任一幕都能调):
- `file-curation`:用户给一堆文件 → 整理成可检索索引
- `claude-code-resources`:找现成的 Claude Code 资源
- `programmatic-video`:做 demo 视频(主要在 ⑨ 幕)
- `browser-automation`:浏览器自动验证(主要在 ⑧ 幕)

---

## Phase 0 · 需求 Gate(**必过,且强制 11 项**)

**未通过 Gate 绝不进 Phase 1**。Gate 由两道关卡组成:

### 关卡 A · 完整性(11 项必填,缺一项就追问)

| # | 项 | 用户没说时怎么问 |
|---|---|----------------|
| 1 | 项目名 + 一句话价值主张 | "这个项目你打算叫什么,一句话介绍它解决什么" |
| 2 | 用户人群 | "谁会用?(独立开发者 / 团队 / 学生 / 企业 ...)" |
| 3 | 核心场景 | "用户从打开到完成主任务,3 步描述一下" |
| 4 | 平台/端 | "Web / Mobile App / 微信小程序 / CLI / 后端 API,哪个?" |
| 5 | 技术栈偏好 | "前端 React/Vue/原生?后端 Node/Python/Go?有没有硬约束" |
| 6 | 不做清单 | "**这一版明确不做的功能**?(避免范围爬升)" |
| 7 | 验收标准 | "什么状态算'做完了'?(具体可验证,不是'好用')" |
| 8 | 部署目标 | "部署到哪?(本地跑 / Vercel / CloudBase / 自己的服务器)" |
| 9 | 时间预算 | "希望几小时 / 几天内见到结果?" |
| 10 | 外部依赖 | "需要 API key / 设计稿 / 第三方账号 / 品牌资产 吗?谁提供" |
| 11 | 视觉/品牌方向 | (UI 项目必填)"参考竞品 / 期望氛围(瑞士主义/杂志风/赛博...)" |

### 关卡 B · 可行性(一票否决)

通过 A 后,做 4 项可行性检查:
- **技术可行**:用户期望能力是否存在(模型/库/服务)
- **平台可行**:平台限制是否冲突(小程序无 Node、原生 App 无 SDK 等)
- **资源可行**:外部依赖是否齐(没有设计稿就别指望 pixel-perfect)
- **时间可行**:时间预算是否合理(1 小时不能做完整电商)

任一项不可行 → **直接回报用户,不开工**:

```
【可行性 ❌】
具体冲突: <一句话说清>
建议方案: 方案 A / 方案 B / 方案 C(每个含取舍)
请用户选: 选哪个 / 调整需求 / 取消项目
```

### Gate 通过标志

输出**需求快照**给用户,等用户**明确说一句"OK 开干"**(或同义,如"行""开始"),才进 Phase 1。

详细模板见 [references/requirement-checklist.md](references/requirement-checklist.md)。

---

## 9 幕(Gate 后中间不打扰)

| 幕 | 调用的 skill | 强制产出 | Ralph 介入? |
|----|------------|---------|-------------|
| **①** 调研 | **user-research** + (可选 file-curation 整理调研材料)| `docs/1-research-report.md` | 否 |
| **②** 分析 | **requirement-analysis** + spec-workflow | `docs/2-requirements.md`(JTBD + Story + 旅程 + 优先级) | 否 |
| **③** 产品(PRD) | **product-spec** + spec-workflow | `docs/3-PRD.md`(11 章) | 否 |
| **④** 设计规范 | ui-design + designdna + design-templates + copywriting-design + taste-skill 自检 | `docs/4-DESIGN.md` + `design-tokens.json` + `copy.json` | 否 |
| **⑤** 接口契约 | cli-design / api-design | `docs/5-INTERFACE.md` | 否 |
| **⑥** 前端实现 | frontend-patterns + 平台 skill(web-development / miniprogram-development / 各 UI 库) | 可运行前端 | ✅ |
| **⑦** 后端实现 | backend-patterns + cloud-functions / cloudrun-development | 可运行后端 | ✅ |
| **⑧** 测试 | **qa-strategy** 编排 → tdd-workflow / e2e-testing / browser-automation / code-review / security-review / verification-loop | `docs/8-test-plan.md` + Quality Gate config + 7 层验证报告 | 否 |
| **⑨** 交付 | **code-simplifier** 全量 + deployment-patterns + Cowork(`pptx`/`docx`/`pdf`)+ programmatic-video(可选) | 简化代码 + README + 部署链接 + 汇报材料 + 30s demo(可选) | 否 |

每一幕**进下一幕前**必须有显式产出落盘 —— 没文件 = 没做完。

---

## 幕间目标重投(Input Injection)⭐

> 灵感:OpenMythos / Recurrent-Depth Transformer 的 input injection —— 每轮把原始输入重新喂回去防漂移。
> 9 幕一字排开,**很容易在第 6-7 幕忘了 ① 调研发现的真实痛点**,做出和原始价值主张失联的代码。

### 幕间硬约束(进下一幕前必做)

每个幕的 exit 阶段必须**重投**:

```
进 Phase N+1 之前:
  1. 重新读 docs/0-requirements-snapshot.md(11 项需求快照)
  2. 重新读 docs/1-research-report.md 的"决定 / 未决定"段(若已存在)
  3. 用一句话**重述**项目的"价值主张"(从 0-snapshot 取)
  4. 检查 Phase N 的产出是否仍在该价值主张轨道上
  5. 如果有偏离 → 标 ⚠️ 并回报用户,不直接进 N+1
```

### 输出格式(进下一幕前打印)

```
【幕间目标重投 · Phase N → N+1】
价值主张(重投): "<一句话从 0-snapshot 抄过来>"
本幕产出: <文件名 + 一句话总结>
轨道检查: ✅ 在轨 / 🔄 微偏 / ⚠️ 偏离 / ❌ 漂移
偏离说明(若不在轨): <具体哪里偏 + 怎么纠>
进入 Phase N+1: 是 / 否(若否,等用户决策)
```

### 为什么必须

实战观察:不做幕间重投,第 ⑦ 幕(后端)经常会:
- 实现了 ① 调研根本没发现的功能(范围爬升)
- 漏了 ② 分析里 Must-have 的某条 Story(目标偏移)
- 用了和 ④ 设计规范矛盾的组件(规范丢弃)

幕间重投 = **每个 transition 都对齐原始 e**,把这些堵在 phase boundary。

### 何时跳过

- 9 幕全跑下来 < 4 小时的小项目:可以跳过(漂移概率低)
- 其他情况:**强制必做**

---

## Ralph + Simplifier 协作模式(⑥⑦ 幕)

```
Ralph 启动(契约 + max=20)
  ↓
PLAN → EXEC → VERIFY → DECIDE
  ↑                       │
  └──── CONTINUE ─────────┘
       │
       └─ DONE ──→ 立刻跑 code-simplifier P0 微清扫
                   (只清这一幕新改的文件,不全量)
                       │
                       └──→ 进下一幕

异常路径:
- 卡住(3 轮 VERIFY 不变)→ ABORT + 报告 → 等用户决策
- 满 20 轮未 DONE → ABORT + 续轮申请书 → 等用户回复
```

**为什么 simplifier 在 Ralph DONE 后跑而不是循环里跑**:
- 循环中 simplifier 可能删掉 ralph 这一轮临时埋的 console.log / 验证脚手架
- DONE 后再清扫,临时品已经完成使命

详见 [references/ralph-simplifier-loop.md](references/ralph-simplifier-loop.md)。

整个 ⑦ 交付幕末尾再跑一次 **simplifier 全量 P0+P1**(不跑 P2,避免引入新风险)。

---

## 6 个强制人工干预触发点(且仅这 6 个)

中间默认不打扰用户。但**这些情况必须停下来报告,不许偷偷继续**:

| # | 触发点 | 报告内容 |
|---|-------|----------|
| 1 | Phase 0 需求不全 | 列缺失项 + 样板问句 |
| 2 | Ralph 超 20 轮 | 续轮申请书(见 ralph-loop SKILL.md) |
| 3 | Ralph 连续 3 轮 VERIFY 不变 | 卡点报告 + 三选项(换思路/缩目标/接管) |
| 4 | 涉及付费决策 | 域名/CDN/付费 API,**不替用户付钱**,告诉用户去哪付 |
| 5 | 涉及破坏性操作 | 删数据库/删生产/`rm -rf` 等,必须用户确认 |
| 6 | ⑧ 验证报告含 ❌ | 等用户决定:继续修 / 接受现状 / 改需求 |

**例外:账号/凭据始终让用户自己输入**,不替用户存(不在 6 触发点之列,但是恒定红线)。

---

## 工作流状态机(每 phase enter / exit / artifact)

详见 [references/workflow-states.md](references/workflow-states.md)。

每个 phase 都有:
- **enter 条件**:上一 phase 的 artifact 已落盘
- **exit 条件**:本 phase 的 artifact 已落盘 + 自检通过
- **artifact**:文件名 + 必填字段

不满足 exit 条件就**不能**前进 —— 哪怕用户催。

---

## 反模式

- ❌ Phase 0 没过就开工("用户大概是想做 X" = 在赌)
- ❌ 中间幕没产出就跳下一幕(你以为自己记住了,其实没有)
- ❌ Ralph 跑满 20 轮还假装"差不多了"(必须申请,不许偷偷续)
- ❌ Simplifier 在 Ralph 还没 DONE 时跑(把临时品当成冗余删掉)
- ❌ 跳过 ⑧ 测试幕(类型检查 + 单测 ≠ 功能 OK)
- ❌ 用户没同意就部署到生产
- ❌ 触发 6 个干预点其中之一却不停(等于偷跑)

---

## 与其他 skill 的关系

| 关系 | 说明 |
|------|------|
| 驱动 | 调用 `design-dev-flow`(7 幕声明)、`ralph-loop`(④⑤ 循环引擎)、`code-simplifier`(每幕末尾 + ⑦ 全量) |
| 调用(各幕内部) | `spec-workflow / ui-design / designdna / cli-design / browser-automation / programmatic-video / 平台 skill` |
| 被替代场景 | 如果用户**只**想跑某一幕(只设计 / 只验证),不要触发本 skill,直接调对应 skill |

---

## References

- [需求 Gate 完整性清单 + 样板问句](references/requirement-checklist.md)
- [Ralph + Simplifier 协作详细规则](references/ralph-simplifier-loop.md)
- [工作流状态机(7 phase enter/exit/artifact)](references/workflow-states.md)
