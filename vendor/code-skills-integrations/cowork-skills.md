# Cowork(Claude Desktop)skills 集成

- **来源**:`~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/.../skills/`
- **运行时暴露**:系统提示里的 `anthropic-skills:*` 一组(已自动加载,无需安装)
- **类型**:Anthropic 官方,产品级 skill

> 我们**不复制**这些 skill 到本仓库 —— 它们已经被 Claude Desktop 自动加载,直接调即可。
> 本文件给"何时调谁 + 怎么和 9 幕配合"的速查表。

## 17 个 skill 清单 + 在 9 幕中的位置

| Cowork skill | 9 幕位置 | 何时触发 |
|--------------|---------|---------|
| `anthropic-skills:pdf` | 任意幕 + ⑨ | 读外部 PDF / 出 PDF 报告 |
| `anthropic-skills:docx` | 任意幕 + ⑨ | 读 Word / 出文档 |
| `anthropic-skills:pptx` | ⑨ 交付 | 出汇报 PPT / 路演用 |
| `anthropic-skills:xlsx` | ① 调研 + ⑧ 测试 | 处理调研问卷数据 / 测试矩阵 |
| `anthropic-skills:canvas-design` | ④ 设计 | 静态艺术海报 / 视觉素材 |
| `anthropic-skills:brand-guidelines` | ④ 设计 | Anthropic 风格(套用模板) |
| `anthropic-skills:theme-factory` | ④ 设计 + ⑨ 交付 | 给 artifact 套预设主题 |
| `anthropic-skills:web-artifacts-builder` | ⑥ 前端 + ⑨ 交付 | 复杂 React + Tailwind + shadcn 单页 |
| `anthropic-skills:internal-comms` | ⑨ 交付 | 内部沟通(发布通告 / leadership update / FAQ / 项目更新) |
| `anthropic-skills:doc-coauthoring` | ②③⑨ | 协作式写作(需求/PRD/汇报) |
| `anthropic-skills:slack-gif-creator` | ⑨ 交付 | Slack 演示动图 |
| `anthropic-skills:algorithmic-art` | ④ 设计 (可选) | 生成式视觉(landing 装饰) |
| `anthropic-skills:mcp-builder` | 工具型 | 给项目做 MCP server(高级) |
| `anthropic-skills:skill-creator` | 元 skill | 给 code-skills 仓库新建 skill |
| `anthropic-skills:consolidate-memory` | 任意幕末 | 跟 hierarchical-memory 配合做记忆整理 |
| `anthropic-skills:setup-cowork` | 元 skill | 配置 Cowork 本身 |
| `anthropic-skills:schedule` | 任意幕 | 排定时任务(定期跑 Ralph) |

## 与本仓库重叠 / 冲突 / 互补

| 重叠点 | 我们的 skill | Cowork skill | 怎么协作不冲突 |
|--------|------------|--------------|---------------|
| Demo 视频 | `programmatic-video` (Remotion) | `slack-gif-creator` | 长视频用前者,Slack 短动图用后者 |
| 设计资源 | `design-templates` | `brand-guidelines` / `theme-factory` | 我们的偏自定义,Anthropic 的偏品牌套用 |
| 文档协作 | (无) | `doc-coauthoring` | ②③ 写需求/PRD 时直接调用 |
| Skill 创作 | (无) | `skill-creator` | 给本仓库新建第 N 个 skill 时调用 |
| 文件整理 | `file-curation` | `pdf/docx/xlsx` 提取 | 我们的负责"如何分类索引",Cowork 负责"如何提取内容" |

## 推荐编排(在 auto-flow 9 幕里)

```
① 调研:        user-research  +  anthropic-skills:pdf/docx/xlsx(读资料)
              + (可选)file-curation 整理一堆文件
② 分析:        requirement-analysis + anthropic-skills:doc-coauthoring(协作写需求)
③ PRD:         product-spec + anthropic-skills:doc-coauthoring
④ 设计:        ui-design / design-templates / copywriting-design
              + anthropic-skills:theme-factory(若要 Anthropic 风格)
              + anthropic-skills:canvas-design(若要海报/视觉)
⑤ 接口:        cli-design / api-design
⑥ 前端:        Ralph + simplifier
              + anthropic-skills:web-artifacts-builder(若是单页 artifact)
⑦ 后端:        Ralph + simplifier
⑧ 测试:        qa-strategy 编排
⑨ 交付:        simplifier 全量 + 部署
              + anthropic-skills:pptx(汇报 PPT)
              + anthropic-skills:docx(Word 报告)
              + anthropic-skills:pdf(发出可分享 PDF)
              + anthropic-skills:internal-comms(发布通告)
              + anthropic-skills:slack-gif-creator(Slack 演示)
              + programmatic-video(若要 30s demo)
```

## 不集成的部分

- 不把 Cowork 的 skill 文件**复制**进本仓库(它们由 Claude Desktop 管理,会自动更新)
- 不替代它们的能力(尊重官方实现)
- 不在本仓库的 CLI 里 passthrough(它们没有命令行入口,只在 Claude 会话里激活)
