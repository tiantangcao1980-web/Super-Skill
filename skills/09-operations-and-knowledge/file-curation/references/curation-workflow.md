# File Curation 4 步法 · 详细操作指南

## 触发示例

用户:"我下载了 200 个跟竞品有关的 PDF/截图/网页,在 `~/Downloads/competitor-research/`,帮我整理一下。"

## Step 1 · 盘点

```bash
# 列全部文件 + 大小
find ~/Downloads/competitor-research -type f -not -name '.DS_Store' \
  -not -path '*__MACOSX*' \
  -exec ls -lh {} \;

# 按类型统计
find ~/Downloads/competitor-research -type f | \
  awk -F. '{print $NF}' | sort | uniq -c | sort -rn
```

输出例:
```
  87 pdf
  45 png
  23 docx
  18 mp4
  12 xlsx
   8 html
   5 txt
   2 mp3
```

198 文件 → 进 Step 2。

## Step 2 · 分类(切桶)

### 类型分桶(基于扩展名 + 内容)
- 文档类: pdf, docx, txt
- 表格类: xlsx, csv
- 视觉类: png, jpg, gif
- 多媒体: mp4, mp3
- 网页类: html, mhtml

### 主题分桶(需要内容理解,先快速扫读)
- 用户访谈 / 评测
- 财务 / 商业模式 / 估值
- 产品 demo / 截图
- 媒体报道 / 公关
- 法务 / 政策

### 重要性分桶(主观但有迹可循)
| 信号 | 重要性 |
|------|-------|
| 客户/老板/法务直接给的 | ⭐⭐⭐ |
| 含具体数据 / 决策依据 | ⭐⭐⭐ |
| 多次出现的同类(取代表) | ⭐⭐ |
| 情绪/讨论/截屏聊天 | ⭐ 或 ❌ |
| 重复 / 旧版 / 测试文件 | ❌ |

## Step 3 · 摘要(只对 ⭐⭐+)

模板严格 3 段,每段 1-3 句:
```
**<文件名>**(类型, 大小)
- 是什么: 客观描述
- 关键点: 2-3 条核心
- 为什么重要: 1 句关联当前项目
```

### 工具调度
```
用户:"`Q3_market_report.pdf` 摘要一下"
本 skill: 触发 `anthropic-skills:pdf` 提取文本
       → 阅读
       → 写 3 段摘要
       → 落到 _summary/Q3_market_report.md
```

### 多文件批处理(避免疲劳)
- 一次最多处理 10 个,每个不超过 3 分钟
- 同主题的合并到一个 summary 文件,标"集中文件 5 份"

## Step 4 · 索引(双视图)

`_index.md` 必须有这两张表:

```md
# Competitor Research · Index

> 198 个文件,2025-04-29 整理。⭐⭐⭐ 7 份必读, ⭐⭐ 22 份参考, 其余归档。

## 视图 A · 按主题(便于发散思考)

### 用户访谈与评测
- ⭐⭐⭐ [user_interview_5_synthesis.docx](./files/...) — 5 个高频痛点
- ⭐⭐ [G2 review snapshot.png](./files/...) — 综合评分 4.3

### 商业模式 / 财务
- ⭐⭐⭐ [Q3_market_report.pdf](./files/...) — 市场规模 1200 亿
- ⭐⭐⭐ [pricing_comparison.xlsx](./files/...) — 主流玩家定价对比

(其他主题省略)

## 视图 B · 按重要性(便于决策)

### ⭐⭐⭐ 必读(7 份)
| 文件 | 主题 | 一句话 |
|-----|------|--------|
| user_interview_5.docx | 调研 | 5 个高频痛点 |
| Q3_market_report.pdf | 市场 | 市场规模 1200 亿,集中度高 |
| ...

### ⭐⭐ 参考(22 份)
(只列文件名 + 主题 + 一句话)

### ⭐ 归档(168 份)
(只列文件名)

### ❌ 删除候选(列出删除理由)
- duplicate_meeting_notes_v2.pdf — 与 v3 内容重叠 95%
- ...
```

## Step 5 · 去重(常见模式)

### 模式 1 · 同事件多份截图 → 取最清晰的一张
### 模式 2 · 同文档多版本 → 取最新 + 删旧版(确认无人在用旧版)
### 模式 3 · 转发邮件链 → 取最末一封,前面摘要
### 模式 4 · 多媒体的转录 + 原文件 → 都留(转录更可搜索,原文件保真)

## Step 6 · 沉淀

询问用户:
- "整理结果存哪里:本目录 / 项目 docs / hierarchical-memory(跨项目)?"
- "需要导出 PPT / Word / PDF 报告吗?"

按选择执行:
- 项目 docs → 移动到 `<project>/docs/research/<date>/`
- hierarchical-memory → 调用 `add-feature` / `save-session`
- 报告 → 调 Cowork `pptx` / `docx` / `pdf` skill

## Step 7 · "看这 3 个就够了"建议

最后一段必给:
```
如果你只看 3 个文件,看这 3 个:
1. user_interview_5_synthesis.docx — 真用户怎么说
2. Q3_market_report.pdf — 市场盘子有多大
3. pricing_comparison.xlsx — 大家怎么收钱

其他的可以等你具体卡到某点再回去查 _index.md。
```

## 红线

- ✅ 只读不改原文件
- ✅ 摘要不抄原文(降到 3 句)
- ✅ 重要性必须分级(全 ⭐⭐⭐ = 等于没分)
- ✅ 必须给"看这 3 个就够了"建议
- ❌ 不要把整理后的目录丢着不收尾
- ❌ 不要在 _index 里放敏感原始数据(用引用链接)
