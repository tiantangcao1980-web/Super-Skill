---
name: file-curation
description: |
  文件分析与整理 skill:用户给一堆文件(PDF / Word / Excel / 截图 / 对话记录 / 网页备份),自动按"分类 → 摘要 → 索引 → 沉淀"4 步法整理出可检索的知识库。
  调用 Cowork 已有的 pdf / docx / xlsx / pptx skill 提取内容,与 hierarchical-memory 协作做长期沉淀。
  触发词:「文件整理」「文档分析」「整理一堆文件」「knowledge curation」「file triage」「资料归档」「PDF 整理」「文档归类」「资料沉淀」。
  适用阶段:任何阶段都可独立触发(工具型 skill,不属于 9 幕流程)。
---

# File Curation · 文件分析与整理

> "桌面上 200 个 PDF,你能告诉我哪 3 个是这个项目要看的吗" —— 这就是本 skill 解决的事。

## 4 步法

```
[一堆文件] → ① 分类 → ② 摘要 → ③ 索引 → ④ 沉淀
              ↓        ↓        ↓        ↓
            按类型   每份2-3句  双视图   持久化
            主题    + 关键词   index.md  hierarchical-memory
            重要性
```

---

## ① 分类(切桶)

按 3 维度切:

### 维度 1 · 类型(文件本身)
- PDF / Word / Excel / 截图 / 视频 / 音频 / 网页 / 邮件 / 聊天记录

### 维度 2 · 主题(领域)
- 用户调研 / 竞品分析 / 财务 / 法务 / 设计 / 工程文档 / 灵感

### 维度 3 · 重要性(决策权重)
- ⭐⭐⭐ 必读(决定方向 / 直接引用 / 客户提供)
- ⭐⭐ 参考(可能用到 / 同类多份取代表)
- ⭐ 归档(留底,不主动看)
- ❌ 删除(过期 / 重复 / 无关 / 坏文件)

### 输出 · 分类表
```
| 文件 | 类型 | 主题 | 重要性 |
|-----|------|------|-------|
| Q3_report.pdf | PDF | 财务 | ⭐⭐⭐ |
| meeting_2024.png | 截图 | 沟通记录 | ⭐ |
| ...
```

---

## ② 摘要(每份 2-3 句)

**关键:不抄全文,只写"如果别人问起,3 句话能说清这是什么"**。

### 摘要模板
```
**<文件名>**
- 是什么:1 句客观描述
- 关键点:2-3 个核心结论 / 数据 / 论点
- 为什么重要:1 句关联到当前项目
```

### 例
```
**Q3_2025_market_report.pdf**(PDF, 47 页)
- 是什么: IDC 2025 Q3 中国 SaaS 市场报告
- 关键点:
  - 市场规模 ¥1200 亿,YoY +18%
  - 工具类 SaaS 占 35%(我们赛道)
  - top 5 玩家占 62%(集中度高)
- 重要: 给我们定位时引用 → 中型市场,有竞争空间
```

### 工具借力
- PDF → 调 Cowork `anthropic-skills:pdf` 提取文本
- Word → 调 Cowork `anthropic-skills:docx`
- Excel → 调 Cowork `anthropic-skills:xlsx` (含表格转 markdown)
- PPT → 调 Cowork `anthropic-skills:pptx`
- 截图 / 图片 → vision 直接读
- 视频 / 音频 → 取转录(用 Whisper),再当文本处理

---

## ③ 索引(双视图)

输出 `index.md`,**两张表**:

### 视图 A · 按主题
```
## 用户调研
- ⭐⭐⭐ [用户访谈_张三.docx](./files/...) — 5 个高频痛点
- ⭐⭐⭐ [问卷结果_2025.xlsx](./files/...) — 200 份样本
- ⭐⭐ [专家访谈_李四.mp4](./files/...) — 行业老兵观点

## 竞品分析
- ⭐⭐⭐ [竞品 A 测评.pdf](./files/...) — top1 玩家
- ...
```

### 视图 B · 按重要性
```
## ⭐⭐⭐ 必读(7 份)
| 文件 | 主题 | 一句话 |

## ⭐⭐ 参考(15 份)
...

## ⭐ 归档(40 份)
(只列文件名 + 链接,不写摘要)
```

---

## ④ 沉淀(长期可检索)

### 选择 1:进 `hierarchical-memory`
跨项目复用的洞察 / 经验 → 调 `hierarchical-memory` 的 `add-feature` / `add-bugfix` / `save-session`。

### 选择 2:留在项目里
- 项目 `docs/research/` 目录
- 命名规范:`<日期>_<类型>_<主标题>.md`
- 加 git 版本管理

### 选择 3:导出可分享
- 用 `anthropic-skills:docx` 出 Word 报告
- 用 `anthropic-skills:pdf` 出 PDF 简报
- 用 `anthropic-skills:pptx` 出 PPT 汇报

---

## 工作流(完整一遍)

### 输入
用户给 1 个目录(`~/Downloads/research/`)+ 期望产出("我要从中梳理出 v0.1 该做什么")。

### 步骤
1. **盘点**:`find <dir> -type f` 列全部文件,过滤 `.DS_Store / __MACOSX` 等
2. **分类**:按类型 / 主题 / 重要性切桶,落到 `_classification.md`
3. **摘要**:对每个 ⭐⭐+ 文件做摘要,⭐ 文件只列名
4. **索引**:输出 `index.md` 双视图
5. **去重**:相似/重复 → 标注后删(或合并保留代表)
6. **沉淀**:看用户意图,选 hierarchical-memory / 项目 docs / 导出报告
7. **总结**:输出 1 段 200 字的"如果你只看 3 个文件"建议

### 输出文件
```
<input-dir>/
├── _index.md              # 双视图索引
├── _classification.md     # 分类表
├── _summary/              # 每份重要文件的摘要 .md
│   ├── Q3_report.md
│   └── ...
└── _recommendation.md     # 给用户的 "看这 3 个就够了"
```

---

## 反模式

- ❌ 把全文抄进摘要(摘要是 2-3 句,不是 200 句)
- ❌ 不分重要性(全部 ⭐⭐⭐ = 等于没排)
- ❌ 不去重(3 份"同一份会议纪要"全留)
- ❌ 摘要没"为什么重要"(脱离项目语境的摘要等于废文)
- ❌ 不沉淀(整理完就丢,下次又得整理一遍)
- ❌ 改原始文件(只读!破坏证据链 = 没法追溯)

---

## 领域文件 → Cowork 专家 skill 路由 ⭐

整理完后,根据**文件主题**,把 ⭐⭐⭐ 必读文件路由到 Cowork 对应 plugin(假设已激活):

| 文件主题 | 路由到 Cowork plugin/skill |
|---------|---------------------------|
| 合同 / NDA / 商务条款 | `legal/contract-review` + `legal/nda-triage` |
| 法规 / GDPR / CCPA 合规 | `legal/compliance` |
| 法律风险 / 案件评估 | `legal/legal-risk-assessment`(5×5 矩阵) |
| 律师函 / 法律邮件模板 | `legal/canned-responses` |
| 财务三表 / P&L / 资产负债 | `finance/financial-statements` |
| 月底结账 / 月报 | `finance/close-management` |
| 凭证 / 应付应收 / 折旧 | `finance/journal-entry-prep` |
| 银行 / 账户调节 | `finance/reconciliation` |
| 预算 vs 实际 / 偏差 | `finance/variance-analysis` |
| SOX / 审计 / 内控 | `finance/audit-support` |
| 数据集 / SQL / 统计 | `data/sql-queries` + `data/statistical-analysis` |
| 用户访谈 / 调研 | `design/user-research` + `pm/user-research-synthesis` |
| 竞品资料 | `pm/competitive-analysis` |
| HR / 招聘 / 薪酬 | `human-resources/*` |
| 销售 / 客户资料 | `sales/*` 或 `common-room/*` |

完整 Cowork 插件索引见 [`vendor/code-skills-integrations/cowork-knowledge-work-plugins.md`](../../../vendor/code-skills-integrations/cowork-knowledge-work-plugins.md)。

**没装 Cowork 对应 plugin 时**:本 skill 仍能做基础整理,但**专业深度**(SOX 404 / GDPR 合规 / 合同 playbook 等)需要专家介入。

---

## 与其他 skill 关系

| skill | 关系 |
|-------|------|
| `anthropic-skills:pdf/docx/xlsx/pptx` | 调用其提取文本 |
| Cowork legal/finance/data/...(见上表) | 整理后路由到对应专家 skill |
| `hierarchical-memory` | 沉淀长期记忆 |
| `iterative-retrieval` | 搜索整理后的索引 |
| Cowork `enterprise-search/knowledge-synthesis` | 互补:本 skill 文件向,它搜索向 |
| `user-research` | 调研材料整理后喂给它 |
| `requirement-analysis` | 整理后的洞察转需求 |

---

## References

- [4 步法详细操作指南](references/curation-workflow.md)
