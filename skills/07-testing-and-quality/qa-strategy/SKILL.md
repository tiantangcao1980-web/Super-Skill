---
name: qa-strategy
description: |
  QA 测试策略 skill:把已有的 tdd-workflow / e2e-testing / code-review / security-review / browser-automation / verification-loop **编排**成一份"项目级测试金字塔",并产出测试用例清单 + 缺陷管理流程 + 上线 quality gate。
  本 skill 不重做底层测试 skill,只是整合调度 + 测试覆盖率 baseline。
  触发词:「测试策略」「QA」「测试金字塔」「测试用例」「缺陷管理」「质量门」「quality gate」「测试覆盖率」「test plan」。
  适用阶段:auto-flow ⑧ 测试幕(在 ⑦ 后端实现之后,⑨ 交付之前)。
---

# QA Strategy · 测试策略

> 测试不是"跑一遍",是**金字塔分层** + **覆盖率基线** + **缺陷闭环** 三件套。

> 💡 **优先调用 Cowork 专家版**(若已激活):
> - `engineering/testing-strategy` —— 测试策略与计划(更深入的层级 / 工具选型 / 覆盖率)
> - `engineering/code-review`、`engineering/incident-response`、`engineering/tech-debt` —— 配套
>
> 本 skill 是**通用 fallback + 编排器** —— 把已装的 `tdd-workflow / e2e-testing / browser-automation / code-review / security-review / verification-loop` 串成一条 Quality Gate。

## 测试金字塔 · 经典 70/20/10

```
       ┌──────┐
       │ E2E  │ 10%   关键路径 / 用户主流程
       └──────┘       慢、贵、最易碎,但最接近真实
      ┌────────┐
      │ 集成   │ 20%   API / 模块边界
      └────────┘
   ┌──────────────┐
   │ 单元测试      │ 70%   函数 / 类 / 组件
   └──────────────┘     快、便宜,跑一万次都行
```

**反金字塔(冰淇淋)是病**:大量手动测试 → 少量 E2E → 几乎没单元 = CI 慢 + 无法重构 + 谁来维护谁辞职。

---

## 编排现有 skill

| 测试层 | 调用 skill | 何时跑 |
|-------|-----------|--------|
| 单元测试 | `tdd-workflow` | 写代码同时(red-green-refactor) |
| 集成测试 | `tdd-workflow` + `verification-loop` | 单元绿后,合并前 |
| 组件视觉 | `browser-automation`(Playwright trace) | PR 阶段 |
| E2E 关键路径 | `e2e-testing` + `browser-automation` | 合并到 main 之后 |
| 代码评审 | `code-review` | 每个 PR |
| 安全扫描 | `security-review` | 周期性 + 敏感改动 |
| 上线前总验证 | `verification-loop` | 部署前 |

本 skill 的工作:**给项目订制每个层的覆盖率基线 + 何时跑的频率 + 失败如何处理**。

---

## 测试用例清单(从 PRD 反推)

每条 User Story 至少 3 类用例:

| 类 | 例 |
|----|----|
| **Happy path** | 用户按预期路径操作,得到预期结果 |
| **边界 case** | 空输入 / 超长 / 极值 / 0 / 负数 / 大文件 |
| **错误恢复** | 网络断 / 服务挂 / 输入非法 / 超时 |

**3 × Story 数 = 用例数下限**。

### 用例模板
```
TC-001: <story> happy path
  Given: <前置>
  When:  <操作>
  Then:  <期望>

TC-002: <story> 空输入边界
  Given: <空状态>
  When:  <提交>
  Then:  <错态文案 X 显示,系统不崩>
```

---

## 覆盖率基线(项目类型决定)

| 项目类 | 单元 | 集成 | E2E |
|-------|------|------|-----|
| **toy / 内部工具** | 0-30% | 关键路径 | 1 个冒烟 |
| **个人产品 / SaaS** | **60-80%** | API 全测 | **3-5 关键路径** |
| **企业级 / 金融 / 医疗** | **80%+** | 100% | **完整回归套件** |
| **库 / SDK** | **90%+** | 100% | N/A |

**不要追求 100% 单元覆盖率** —— 边际收益陡降,容易测"实现"而非"行为"。

---

## 缺陷管理流程(4 状态机)

```
[Open] → [In Progress] → [Fixed] → [Verified]
            ↓
        [Won't Fix] (with reason)
```

### 4 级严重度
| 级 | 含义 | SLA |
|----|------|-----|
| **P0** | 阻塞,无解决方案 | 24h 内修 |
| **P1** | 主流程坏,有 workaround | 1 周 |
| **P2** | 次要功能或边缘 case | 下版本 |
| **P3** | 优化建议 | 待评估 |

### 必填字段
- 复现步骤(精确到点击)
- 期望 vs 实际
- 环境(浏览器 / OS / 网络)
- 截图 / 视频 / log
- 责任人

---

## Quality Gate(上线 / 合并前必过)

```
□ 单元测试通过率 100%
□ 单元覆盖率 ≥ 项目基线
□ 集成测试通过率 100%
□ E2E 关键路径通过率 100%
□ code-review 通过(至少 1 人 approve)
□ security-review:无 P0/P1 漏洞
□ Lint / 类型检查 0 error
□ Bundle 大小未超阈值(前端项目)
□ 性能预算未超阈值
□ Accessibility 检查无 critical issue
```

任一项不过 → 不许合并 / 不许上线。

---

## 工作流

### Step 1 · 读 PRD
找出所有 User Story + 验收标准。

### Step 2 · 反推用例清单
每条 Story × 3 类(happy/边界/错态)= 用例总数。

### Step 3 · 确定覆盖率基线
按项目类查表,落到 README + CI 配置。

### Step 4 · 编排测试 skill
- 单元层 → 调 `tdd-workflow`
- E2E → 调 `e2e-testing` + `browser-automation`
- 安全 → 调 `security-review`
- 收尾 → 调 `verification-loop`

### Step 5 · 设定 Quality Gate
落到 `.github/workflows/quality.yml` 或 `Makefile`。

### Step 6 · 输出
- `docs/8-test-plan.md`(测试策略 + 用例清单 + 覆盖率基线)
- `docs/8-bug-tracker.md`(缺陷登记本) 或链 GitHub Issues

---

## 反模式

- ❌ **没单元只跑 E2E**(冰淇淋反模式,CI 慢得人神共愤)
- ❌ **追求 100% 覆盖率**(测出来的是实现细节,改不动)
- ❌ **测试和代码 PR 分开提**(应该同 PR 一起 review)
- ❌ **Bug 没复现步骤**(单条"不能用了" = 没法修)
- ❌ **没 Quality Gate**(靠口头"我看了" = 靠不住)
- ❌ **手动测试当主力**(不能回归,招到测试工程师就让他自动化)

---

## 与其他 skill 的关系

本 skill 是**编排器**,真正的测试动作交给:
| skill | 角色 |
|-------|------|
| `tdd-workflow` | 单元 + 集成 |
| `e2e-testing` | E2E 工程实践 |
| `browser-automation` | LLM 探索 + Playwright 固化 |
| `verification-loop` | 多语言 verify 命令 |
| `code-review` | PR 审查 |
| `security-review` | 漏洞扫描 |

---

## References

- [测试用例模板 + Quality Gate 配置](references/test-plan-template.md)
