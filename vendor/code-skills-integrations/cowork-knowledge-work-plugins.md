# Cowork Knowledge-Work Plugins · 完整集成索引

> **重大发现**:Cowork 除了 17 个 `anthropic-skills:*` 通用 skill,还有 **19 个领域专家插件 / 81 个 skill**,覆盖 legal / finance / engineering / design / product-management / data / marketing / operations / HR / sales / customer-support 等几乎所有知识工作场景。
>
> 路径:`~/Library/Application Support/Claude/.../cowork_plugins/cache/knowledge-work-plugins/`
>
> **本仓库与它们的关系**:**互补 + 路由**,不重做。

## 📦 19 个领域 Plugin · 81 个 Skill 全表

### 🏛️ legal · v1.1.0(6 skill,⭐ 与本仓库无重叠,直接调)
| skill | 用途 |
|-------|------|
| `contract-review` | 合同条款 vs 公司 playbook 比对,生成 redline 建议(LoL / 赔偿 / 终止 / IP / 数据 等条款专项分析) |
| `nda-triage` | NDA 三色分诊(GREEN 标准 / YELLOW 复审 / RED 重大问题),含 8 项标准化检查清单 |
| `legal-risk-assessment` | 5×5 风险矩阵(severity × likelihood),含升级触发条件 |
| `compliance` | GDPR / CCPA / LGPD / POPIA / PIPEDA / PDPA 合规 + 数据主体请求(DSR)处理 |
| `canned-responses` | 法律邮件模板库管理(数据请求 / 供应商问询 / NDA 请求 / 取证保全等) |
| `meeting-briefing` | 法律相关会议简报(交易复盘 / 董事会 / 监管约谈 / 诉讼策略) |

**红线**:全部 skill 顶部都标注"not legal advice",输出仅为律师工作底稿。

### 💰 finance · v1.1.0(6 skill,⭐ 无重叠,直接调)
| skill | 用途 |
|-------|------|
| `financial-statements` | 出 P&L / Balance Sheet / Cash Flow,含 GAAP 格式 + flux 分析 |
| `journal-entry-prep` | 月底凭证录入(应付应收 / 折旧 / 摊销 / 收入确认) |
| `reconciliation` | 账户调节(GL→subledger / bank rec / 跨公司调节 / 阶龄分析) |
| `variance-analysis` | 预算 vs 实际方差分析(价量分解 / 率组合分解 / 瀑布图) |
| `close-management` | 月度结账流水线(T-3 到 T+5 每日任务 + 依赖跟踪) |
| `audit-support` | SOX 404 控制测试方法、抽样、缺陷分级、审计准备 |

**红线**:全部 skill 标注"not financial advice / not audit opinion"。

### 🚀 product-management · v1.1.0(6 skill,⚠️ 与本仓库 `requirement-analysis` / `product-spec` 重叠)
| skill | 与本仓库关系 |
|-------|-------------|
| `feature-spec` | **替代** `product-spec` 的简版功能 spec(用 Cowork 这个) |
| `roadmap-management` | RICE / MoSCoW / ICE 排序(本仓库 `requirement-analysis` 已含 RICE/MoSCoW,可互补) |
| `user-research-synthesis` | **替代** `user-research` 的访谈合成部分 |
| `competitive-analysis` | 与 `marketing/competitive-analysis` 类似(2 个角度,产品向与营销向) |
| `metrics-tracking` | OKR / 仪表盘 / NSM(本仓库 `product-spec` 包含 NSM,这里更细) |
| `stakeholder-comms` | 周报 / 月报 / 启动公告 / 风险沟通 |

### 🔧 engineering · v1.1.0(6 skill,⚠️ 与本仓库 `qa-strategy` / `code-simplifier` 部分重叠)
| skill | 与本仓库关系 |
|-------|-------------|
| `code-review` | 与 Claude Code 已装的 `code-review` 重叠(选其一) |
| `system-design` | 系统架构(API / 数据建模 / 服务边界,与 `cli-design` 互补) |
| `documentation` | API doc / 架构 doc / runbook |
| `incident-response` | 生产故障应急 |
| `tech-debt` | 与 `code-simplifier` 互补(后者偏精简,前者偏识别盘点) |
| `testing-strategy` | **替代** `qa-strategy`(Cowork 这个更深入) |

### 🎨 design · v1.1.0(6 skill,⚠️ 与本仓库 `copywriting-design` / `design-templates` 部分重叠)
| skill | 与本仓库关系 |
|-------|-------------|
| `accessibility-review` | WCAG 2.1 AA 审计(本仓库无,直接用) |
| `design-critique` | 设计 review(本仓库无,直接用) |
| `design-handoff` | 给开发的实现规格(本仓库 `cli-design` ↔ API 角度) |
| `design-system-management` | **替代** `design-templates` 的 token 管理部分 |
| `user-research` | **替代** `user-research`(从设计角度做调研规划) |
| `ux-writing` | **替代** `copywriting-design` 的微文案部分(按钮 / 错态 / 空态) |

### 📊 data · v1.0.0(7 skill,⭐ 无重叠)
| skill | 用途 |
|-------|------|
| `data-context-extractor` | 抽数据集语义 |
| `data-exploration` | 新数据集探查(分布 / 空值 / 异常) |
| `data-validation` | 分析前 QA(方法论 / 偏差检测) |
| `data-visualization` | matplotlib / seaborn / plotly |
| `interactive-dashboard-builder` | Chart.js HTML 仪表盘 |
| `sql-queries` | Snowflake/BigQuery/Databricks/PostgreSQL 多方言 |
| `statistical-analysis` | 描述统计 / 趋势 / 异常 / 假设检验 |

### 📣 marketing · v1.1.0(5 skill,⭐ 无重叠)
brand-voice / campaign-planning / competitive-analysis / content-creation / performance-analytics

### ⚙️ operations · v1.1.0(6 skill,⭐ 无重叠)
change-management / compliance-tracking / process-optimization / resource-planning / risk-assessment / vendor-management

### 👥 human-resources · v1.1.0(6 skill,⭐ 无重叠)
compensation-benchmarking / employee-handbook / interview-prep / org-planning / people-analytics / recruiting-pipeline

### 💼 sales · v1.1.0(6 skill,⭐ 无重叠)
account-research / call-prep / competitive-intelligence / create-an-asset / daily-briefing / draft-outreach

### 🤝 customer-support · v1.1.0(5 skill,⭐ 无重叠)
customer-research / escalation / knowledge-management / response-drafting / ticket-triage

### 🎤 brand-voice · v1.0.0(3 skill,⚠️ 与 `copywriting-design` 部分重叠)
brand-voice-enforcement / discover-brand / guideline-generation

### 🔍 enterprise-search · v1.1.0(3 skill,⚠️ 与 `file-curation` 部分重叠)
knowledge-synthesis / search-strategy / source-management

### 🤖 common-room · v1.0.0(6 skill,无重叠 — CRM/sales)
account-research / call-prep / compose-outreach / contact-research / prospect / weekly-prep-brief

### ⏱️ productivity · v1.1.0(3 skill,⚠️ 与 `hierarchical-memory` 部分重叠)
dashboard.html / memory-management / task-management

### 🧬 bio-research · v1.0.0(5 skill,⭐ 无重叠 — 生物信息学)
instrument-data-to-allotrope / nextflow-development / scientific-problem-selection / scvi-tools / single-cell-rna-qc

### 🔮 apollo · v0.1.0(3 skill,无重叠 — Apollo.io 集成)
enrich-lead / prospect / sequence-load

### 🛠️ cowork-plugin-management · v0.2.2(2 skill,元)
cowork-plugin-customizer / create-cowork-plugin

### 💬 slack-by-salesforce · v1.0.0(2 skill,集成)
slack-messaging / slack-search

---

## 🎯 在 auto-flow 9 幕中的位置

| 幕 | Cowork 优先调用 | 本仓库 fallback |
|----|----------------|----------------|
| ① 调研 | `pm/user-research-synthesis` + `design/user-research` | `user-research` |
| ② 分析 | `pm/user-research-synthesis` + `pm/competitive-analysis` | `requirement-analysis` |
| ③ 产品 PRD | `pm/feature-spec` + `pm/roadmap-management` + `pm/metrics-tracking` | `product-spec` |
| ④ 设计 | `design/design-system-management` + `design/ux-writing` + `design/accessibility-review` + `design/design-critique` | `design-templates` + `copywriting-design` |
| ⑤ 接口 | `engineering/system-design` | `cli-design` |
| ⑥ 前端 | `engineering/code-review` + `engineering/tech-debt` | (Ralph + simplifier) |
| ⑦ 后端 | 同上 + `engineering/incident-response` | 同上 |
| ⑧ 测试 | `engineering/testing-strategy` | `qa-strategy` |
| ⑨ 交付 | `engineering/documentation` + `pm/stakeholder-comms` + `marketing/content-creation` | (simplifier + Cowork pptx/docx/pdf) |

---

## 🎯 法律 / 财务专项工作流(用户问的)

### 法律案件分析(50 个 PDF/Word + Excel)
```
1. 整理:    file-curation 4 步法 → _index.md
            (用 anthropic-skills:pdf / docx / xlsx 提取)
2. 合同:    cowork legal/contract-review(对照 playbook)
3. NDA:     cowork legal/nda-triage(三色分诊)
4. 风险:    cowork legal/legal-risk-assessment(5×5 矩阵)
5. 合规:    cowork legal/compliance(GDPR / CCPA / 等)
6. 模板:    cowork legal/canned-responses(法律邮件模板)
7. 输出:    anthropic-skills:docx 出 Word 工作底稿
            或 anthropic-skills:pptx 出汇报
8. 沉淀:    hierarchical-memory(跨案件经验复用)
```

### 财务资料分析(月度结账 / 审计 / 三表)
```
1. 整理:    file-curation 4 步 → 按科目 / 期间 / 子公司分桶
2. 录入:    cowork finance/journal-entry-prep
3. 调节:    cowork finance/reconciliation
4. 三表:    cowork finance/financial-statements
5. 方差:    cowork finance/variance-analysis
6. 月度:    cowork finance/close-management(完整 T-3 到 T+5 流水线)
7. 审计:    cowork finance/audit-support(SOX 404 + 抽样 + 缺陷分级)
8. 数据:    cowork data/sql-queries + statistical-analysis(若需 OLAP 分析)
9. 报告:    anthropic-skills:xlsx + docx + pptx
```

---

## ⚠️ Plugin 激活检查

Cowork knowledge-work-plugins **缓存在本地但默认未必加载**。激活方法:
1. 打开 Claude Desktop
2. 找到 Cowork 插件管理面板
3. 启用所需 plugin(legal / finance / 等)

未加载时,本仓库的 fallback skill 接管(基础版能用,但深度不及 Cowork)。

---

## 📊 与本仓库 skill 的协作矩阵

| 本仓库 skill | Cowork 优先版 | 关系 |
|-------------|--------------|------|
| `user-research` | `design/user-research` + `pm/user-research-synthesis` | **fallback** |
| `requirement-analysis` | `pm/user-research-synthesis` | **fallback** |
| `product-spec` | `pm/feature-spec` + `pm/roadmap-management` | **fallback** |
| `qa-strategy` | `engineering/testing-strategy` | **fallback** |
| `copywriting-design` | `design/ux-writing` + `brand-voice/*` | **协作**(本仓库定调,Cowork 细化) |
| `design-templates` | `design/design-system-management` | **协作**(本仓库初始化,Cowork 维护) |
| `cli-design` | `engineering/system-design`(部分) | **协作**(本仓库 CLI 专精) |
| `code-simplifier` 📦 | `engineering/tech-debt`(部分) | **协作**(后者识别 / 前者删除) |
| `file-curation` | `enterprise-search/knowledge-synthesis` | **互补**(前者文件向 / 后者搜索向) |
| `auto-flow` | `pm/stakeholder-comms` 等 | **编排器**(本仓库调它们) |

**没有重做** —— 本仓库 fallback 只在 Cowork 没装时启用。

---

## 🚫 不集成的部分

- **不复制** Cowork 任何 plugin 文件到本仓库(它们由 Anthropic 维护,会更新)
- **不重做** Cowork 的领域 skill(我们不可能在简短 SKILL.md 里超越 SOX/GDPR/三表勾稽这类深度)
- **不替代** Cowork 的运行时(它们在 Claude Desktop 里激活,我们只是引用 + 路由)
