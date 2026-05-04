# Claude Code · 97 个本地 skill 在 9 幕中的位置

> `~/.claude/skills/` 已装的 97 个 skill。本文件给"哪个幕调哪些"的速查表。
> **不重复造轮子** —— 已经有的就直接调,不在本仓库重做。

## 速查矩阵

### ① 调研幕(本仓库 `user-research` 主导)
| 协作 skill | 用途 |
|-----------|------|
| `iterative-retrieval` | 大量资料检索 |
| `hierarchical-memory` | 跨项目复用调研结果 |

### ② 分析幕(本仓库 `requirement-analysis` 主导)
| 协作 skill | 用途 |
|-----------|------|
| `spec-workflow` | 标准 spec 流程,与本仓库 PRD 互补 |
| `hierarchical-memory` | 复用同类项目的需求模式 |

### ③ PRD 幕(本仓库 `product-spec` 主导)
| 协作 skill | 用途 |
|-----------|------|
| `spec-workflow` | 写工程 spec |
| `huashu-nuwa` | 文案/话术做品牌定调(如需) |

### ④ 设计幕
| 协作 skill | 用途 |
|-----------|------|
| `ui-design` | 设计原则与方法 |
| `designdna` | 58 品牌设计 DNA 库 |
| `apple-hig` | iOS/macOS 项目用 |
| `huashu-nuwa` | 文案/话术 |
| `guizang-ppt-skill` | 杂志风 PPT(若 PRD 需要演示稿) |

**UI 库 skill(选其一,看技术栈)**:
| 框架 | 选项 |
|------|------|
| React 桌面 | `ant-design` / `mui-material` / `chakra-ui` / `fluent-ui` / `radix-ui` / `shadcn-ui` / `mantine-ish via mui-base` / `tdesign-react` |
| React 移动 | `ant-design-mobile` / `nutui-react` |
| React Native | `react-native-paper` / `tamagui` |
| Vue 3 桌面 | `element-plus` / `ant-design-vue` / `arco-design-vue` / `naive-ui` / `tdesign-vue-next` |
| Vue 移动 | `nutui-vue` / `tdesign-mobile` |
| Flutter | `material-components-flutter`(已迁移到 Flutter SDK)/ `flutter-material` / `tdesign-flutter` |
| Android | `material-components-android` |
| iOS | `material-components-ios`(归档,新项目改 SwiftUI) |
| Web Components | `material-web` |
| MiniProgram | `vant-weapp` / `tdesign-miniprogram` / `weui` |
| 跨端 | `taro` + `taro-ui` 或 `nutui-react` / `uniapp` + `nutui-uniapp` |
| AI 对话 UI | `ant-design-x` / `tdesign-chat` |

**专业**:`mui-x`(企业级 DataGrid/Charts)、`nutui-icons`、`nutui-templates`、`react-bits`、`bootstrap`、`tailwindcss`、`vuetify`

### ⑤ 接口幕(本仓库 `cli-design` 主导)
| 协作 skill | 用途 |
|-----------|------|
| `api-design` | REST / GraphQL / gRPC / WebSocket |
| `data-model-creation` | 复杂数据模型 |
| `cli-toolkit` | CLI 集成模板 |

### ⑥ 前端幕(`frontend-patterns` 主导)
| 协作 skill | 用途 |
|-----------|------|
| `frontend-patterns` | React/Vue/Angular/RN/Flutter 模式 |
| `coding-standards` | 命名/类型/错误处理标准 |
| `web-development` | Web 静态托管/SDK 集成 |
| `miniprogram-development` | 微信小程序 |
| **平台-CloudBase**:`ai-model-web`/`auth-web`/`relational-database-web`/`no-sql-web-sdk`/`cloud-storage-web`/`http-api`/`auth-http-api` | CloudBase 各模块 |

### ⑦ 后端幕(`backend-patterns` 主导)
| 协作 skill | 用途 |
|-----------|------|
| `backend-patterns` | Node/Python/Go/Java 模式 |
| `database-patterns` | SQL/NoSQL/ORM/迁移 |
| `cloud-functions` | Serverless 函数 |
| `cloudrun-development` | 容器服务 |
| `cloudbase-platform` | CloudBase 平台知识 |
| `cloudbase-agent-ts` | TypeScript agent SDK |
| `auth-nodejs` | Node 鉴权 |
| `auth-tool` | 鉴权 provider 配置 |
| `relational-database-tool` | MySQL 工具操作 |
| `systems-programming` | Rust/C/嵌入式(若需要) |
| `ai-model-nodejs` | Node 端 AI 模型 |
| `ai-model-wechat` | 小程序端 AI |
| `ai-agent-frameworks` | Agent 框架(LangChain/AutoGen/CrewAI) |

### ⑧ 测试幕(本仓库 `qa-strategy` 编排)
| 协作 skill | 用途 |
|-----------|------|
| `tdd-workflow` | 单元 + 集成 |
| `e2e-testing` | Playwright / Cypress |
| `code-review` | PR 审查 |
| `security-review` | OWASP / 漏洞扫描 |
| `verification-loop` | 多语言 verify 命令 |
| `coding-standards` | 二次验证编码规范 |

### ⑨ 交付幕(本仓库 `code-simplifier` + Cowork)
| 协作 skill | 用途 |
|-----------|------|
| `deployment-patterns` | Docker / K8s / CI/CD / 云平台 |
| `web-development`(部署部分) | 静态托管部署 |
| `cloud-functions`(部署部分) | 云函数部署 |
| `cloudrun-development`(部署部分) | 容器部署 |
| `wechat-miniprogram-docs` | 小程序发布 |

### 元 / 工具型(任一幕都可调)
| skill | 用途 |
|-------|------|
| `agent-teams` | 多 agent 协调(复杂任务) |
| `iterative-retrieval` | 渐进式检索 |
| `hierarchical-memory` | 跨会话记忆 |
| `continuous-learning` | 会话结束沉淀经验 |
| `strategic-compact` | 长对话压缩 |
| `skill-authoring` | 写新 skill |
| `claude-code-resources`(本仓库) | 找现成资源 |
| `file-curation`(本仓库) | 一堆文件整理 |

## 项目模板(立项加速)
- `uniapp-template` —— UniApp 跨平台模板
- `nutui-templates` —— NutUI 页面模板

## 重叠/冲突说明

| 看似重叠 | 实际分工 |
|---------|---------|
| `coding-standards` × `code-simplifier` | 前者写代码时遵守,后者写完后清扫 |
| `tdd-workflow` × `qa-strategy` | 前者是层(单元),后者是策略编排 |
| `spec-workflow` × `product-spec` | 前者偏工程 spec,后者偏产品 PRD,两份都要写 |
| `auto-flow` × `design-dev-flow` | 前者是引擎(执行),后者是蓝图(声明) |
| Cowork `pdf/docx/xlsx` × 本仓库 `file-curation` | 前者提取内容,后者分类索引 |

## 工作流推荐(精简版)

```
触发 auto-flow → 走 9 幕
  ├─ 各幕主 skill 来自本仓库(自定义流程)
  ├─ 各幕的 UI/技术栈 skill 来自 ~/.claude/skills(已装)
  ├─ 各幕的文档/汇报来自 Cowork(自动加载)
  └─ Ralph + simplifier 在 ⑥⑦ 幕由本仓库的 plugin 驱动
```

**不要** 在 SKILL.md 里复述其他 skill 的内容 —— 用链接引用即可。
