# Super Skill

[![CI](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/ci.yml/badge.svg)](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/ci.yml)
[![Quality](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/quality.yml/badge.svg)](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-114-blue)](catalog/skill-index.md)
[![Profiles](https://img.shields.io/badge/profiles-core%20%7C%20dev%20%7C%20design%20%7C%20hermes%20%7C%20all-green)](manifests/install-profiles.json)

> **Thesis.** AI coding agents fail in four predictable ways: they don't do what the user actually wanted (input quality), they ramble (output quality), the code doesn't run (verification), and yesterday's lesson never reaches today's session (memory). Super Skill is a 114-skill collection plus a runnable harness CLI built around exactly those four failure modes — every skill front-loads its trigger condition, every loop has a hard quality gate, and the autonomous closed loop (`bin/super-skill autopilot`) drives one prompt through intent → spec → design → ralph-loop implementation → simplifier → quality gate → reviewable memory candidate, with every artifact checkpointed on disk.

## ⚡ Quick start (autonomous closed loop)

```bash
# Offline deterministic stub — CI safe, no API key needed:
bin/super-skill autopilot --provider stub --prompt "Build a TODO list API with tests"

# Real LLM:
ANTHROPIC_API_KEY=sk-... bin/super-skill autopilot --provider anthropic \
    --prompt "Build a TODO list API with tests" --project ./build
```

Each phase loads the canonical SKILL.md as its system prompt, calls the LLM (or stub), and writes a checkpoint under `<project>/.super-skill/autopilot/<run-id>/`. Phases 1 (intent contract) and 6 (output quality gate) are hard exits. Phase 4 wraps `ralph-loop` for iterative implementation. Phase 7 produces a Hermes-style reviewable memory candidate without ever echoing the raw prompt.

## What's inside

Super Skill 是一个面向 AI coding agent 的全流程技能集合：从用户意图、上下文工程、市场/用户调研，到需求分析、产品规格、设计系统、接口与开发、测试验证、交付增长、运维知识沉淀，形成一套可安装、可验证、可继续扩展的 skills 生态。

它的目标不是简单增加技能数量，而是提升 LLM 输入和输出质量：把用户期待转成可验收契约，把大上下文压缩成高信号上下文包，把 agent 输出重新拉回用户目标、证据和质量门。

最新一层能力是 AI-first harness engineering + Hermes-style self-improving agent engineering：让项目架构、CI/CD、代码评审、实验发布、可观测性、长期记忆、技能演进、工具路由、模型约束、开发工具适配和回滚安全都变得 agent 可读、可执行、可验证。

本仓库整合并重新编排了：

- `code-skills` 的端到端工作流、调研、产品、设计、测试、交付和工具型技能
- `DesignDNA-Skills` 的 DesignDNA 主技能、47 个设计/组件库子技能、58 套品牌设计系统和 CLI
- 本机 Codex 技能体系中的工程能力层：API、前端、后端、数据库、调试、安全、部署、GitHub、Docker、文档等
- Codex/插件经验沉淀：技能编写、验证闭环、工具路由、跨工具打包
- `everything-claude-code` 的选择性安装、能力面划分、适配政策、安全审计思路
- `obra/superpowers` 的 TDD、系统化调试、技能演进、完成前验证方法
- `NousResearch/hermes-agent` 的渐进式技能加载、长期记忆分层、上下文缓存、工具集路由、持久任务队列、定时任务和安全回滚理念
- Cowork 领域生态作为 `vendor/cowork/` 保留：法律、财务、销售、营销、客服、数据、HR/ops 等领域插件素材

## 能力闭环

| 阶段 | 目录 | 代表技能 |
| --- | --- | --- |
| 编排/输入质量 | `skills/00-orchestration` | `intent-contract`, `context-engineering`, `prompt-cache-layering`, `toolset-sandbox-routing`, `durable-agent-board`, `ralph-loop` |
| 调研 | `skills/01-research` | `user-research`, `market-research` |
| 分析 | `skills/02-analysis` | `requirement-analysis`, `data-analysis` |
| 产品 | `skills/03-product` | `product-spec`, `agentic-product-iteration` |
| 设计 | `skills/04-design-system` | `designdna`, `design-templates`, 47 个 UI/组件库技能 |
| 接口/CLI | `skills/05-interface-and-cli` | `api-design`, `api-gateway`, `cli-design`, `create-cli` |
| 开发 | `skills/06-development` | `agent-legible-architecture`, `frontend-patterns`, `backend-patterns`, `database-patterns`, `ai-agent-frameworks` |
| 测试/输出质量 | `skills/07-testing-and-quality` | `agent-eval-harness`, `ai-review-gates`, `checkpoint-rollback-safety`, `qa-strategy`, `output-quality-gate`, `browser-automation`, `security-review` |
| 交付/增长 | `skills/08-delivery-and-growth` | `experiment-driven-delivery`, `deployment-patterns`, `docker`, `git`, `github` |
| 运维/知识 | `skills/09-operations-and-knowledge` | `observability-triage-loop`, `agent-memory-dream-loop`, `persistent-memory-curation`, `file-curation`, `documentation`, `continuous-learning` |
| Codex/Hermes/上下文模式 | `skills/90-codex-patterns` | `harness-engineering`, `dev-tool-adapter`, `model-adaptation-contract`, `skill-evolution-loop`, `token-budgeting`, `skill-authoring-system`, `verification-loop`, `agent-routing` |

当前清单：

- 113 个可安装生命周期技能
- 1 个 Codex 插件：`super-skill-memory-harness`
- profile/component manifest 支持只读安装预案
- automatic trigger / skill lifecycle manifest 支持自动触发、可控记忆、技能去重和可逆归档
- 5 个验证性项目 eval fixtures，覆盖端到端交付、跨工具记忆、设计前端质量、事故学习闭环和 token-efficient LLM I/O
- 3 个 live eval projects，在临时目录生成小型交付物并运行本地 grader、单测和 memory hook probe
- 58 套 DesignDNA 品牌系统，位于 `resources/design-md/`
- 67 个 Cowork 领域技能文件，位于 `vendor/cowork/`
- 0 个 installable skill 命名冲突

## 快速使用

```bash
# 查看技能
bin/super-skill list

# 校验结构、命名、链接、资源计数
bin/super-skill validate

# 预览安装计划，不修改目标目录
bin/super-skill plan --profile core --json

# 审计去重、manifest、兼容软链、入口文件、疑似密钥和风险命令
bin/super-skill audit --json

# 评估项目的 AI-first harness readiness
bin/super-skill harness --json

# 评估 Hermes-style self-improving agent readiness
bin/super-skill hermes --json

# 评估 agent memory / dream replay readiness
bin/super-skill memory --json

# 校验自动触发策略、技能自我进化约束、protected skills 和去重门
bin/super-skill triggers --json

# 运行验证性项目，证明 skills 集合是否覆盖初衷和预期
bin/super-skill evals --json

# 运行可执行 live eval 项目，验证临时项目交付物、测试和 memory hook
bin/super-skill live-evals --json

# 预览安装 Codex 记忆/做梦自动插件，不修改本机配置
bin/super-skill memory-plugin --dry-run --json

# 安装完整集合到 Codex skills 目录，默认软链
bin/super-skill install --profile all --target ~/.codex/skills

# 安装 core skills 时一并安装 Codex 记忆/做梦插件和 hooks
bin/super-skill install --profile core --target ~/.codex/skills --with-memory-plugin

# 只安装开发相关能力
bin/super-skill install --profile dev --target ~/.codex/skills

# 安装到 Claude Code
bin/super-skill install --profile core --target ~/.claude/skills

# 安装到 Hermes Agent，自动排除 Hermes 原生能力镜像，避免重复
bin/super-skill install --profile hermes

# 生成索引
bin/super-skill catalog

# 生成跨工具适配 wrapper（Cursor/Trae/Windsurf/OpenCode/Claude Code/OpenClaw）
bin/super-skill adapt --tool cursor --project .
bin/super-skill adapt --tool windsurf --project .
bin/super-skill adapt --tool opencode --project .
bin/super-skill adapt --tool claude-code --project .
# Codex / Hermes 通过 install 命令落地，adapt 仅打印对应安装指令
bin/super-skill adapt --tool codex
bin/super-skill adapt --tool hermes

# 跑真实 LLM 端到端循环：intent-contract → implementation → output-quality-gate
bin/super-skill llm-eval --provider stub                    # 离线 stub，CI 安全
ANTHROPIC_API_KEY=sk-... bin/super-skill llm-eval --provider anthropic --prompt "建一个待办列表 API"

# 自主闭环 (autopilot): intent → spec → design → ralph-loop → simplifier → gate → memory
# 每阶段写产物到 <project>/.super-skill/autopilot/<run-id>/，可中断可恢复
bin/super-skill autopilot --provider stub --prompt "Build a Python add(a,b)"
ANTHROPIC_API_KEY=sk-... bin/super-skill autopilot --provider anthropic --project ./build \
    --prompt "Build a TODO list API with tests" --max-ralph-rounds 20
# 跳过某阶段：--skip 03-design,07-memory；强制重跑：--force；指定运行 id：--run-id ...
```

Profiles:

- `core`: 从调研到交付的主流程，不强调具体开发栈扩展
- `dev`: 接口、前后端、数据库、测试、交付、运维
- `design`: DesignDNA、设计系统、UI 库与质量约束
- `hermes`: 面向 Hermes Agent 的完整生命周期集合，默认目标 `~/.hermes/skills`，排除 Hermes 原生能力镜像
- `all`: 所有可安装技能

## 自动记忆/做梦闭环

Codex 路径使用 `plugins/super-skill-memory-harness/`：它把记忆/做梦闭环做成可安装插件，并通过 `SessionStart`/`Stop` hook 记录轻量 metadata 和 review candidate。安装命令会把 hook 命令改成绝对脚本路径，避免插件缓存或启动目录变化导致脚本找不到。

不支持插件的开发工具使用同一个 canonical skill：`agent-memory-dream-loop`。它的描述和 `manifests/auto-trigger-policy.json` 会让 Cursor、Trae、OpenCode、OpenClaw、Claude Code 等工具通过规则/技能隐式触发，而不是再复制一套重复技能。

自动触发是可控的：

- `SUPER_SKILL_MEMORY_DISABLED=1` 可以关闭 hook/fallback。
- 不捕获 raw prompt、raw response、密钥、私人数据或未验证结论。
- 默认只生成候选，不自动提升为 durable memory 或 skill patch。
- 技能自我进化必须经过 `manifests/skill-lifecycle-policy.json`：rubric-first、先找最近已有技能、保护 critical/important 技能、可逆 archive、不自动删除、catalog/audit 后再推广。

## 能力验证项目

`evals/projects/` 中保留 5 个验证性项目：

- `ai-first-saas-launch`: 验证从调研、产品、设计、开发、测试、交付到运维/记忆的全链路覆盖。
- `cross-runtime-memory`: 验证 Codex plugin/hook 与 Claude Code、Cursor、Trae、OpenCode、OpenClaw fallback 的一致性。
- `design-to-frontend-quality`: 验证 DesignDNA、UI 框架、前端质量与品牌系统同步。
- `incident-to-learning-loop`: 验证可观测性、调试、安全评审、回归 eval、负面记忆和技能演化门。
- `token-efficient-llm-io`: 验证 intent/context/token/model/output quality 的 LLM 输入输出质量闭环。

`bin/super-skill evals --json` 会机器检查每个项目的 required skills、生命周期阶段、验收语言、hook-only 插件、防 raw prompt 写入、自动触发策略和技能生命周期策略。

`evals/live-projects/` 中保留 3 个可执行 live eval 项目：

- `mini-saas-feedback-loop`: 在临时项目中验证 feature flag、kill switch、metrics、rollback、release note、observability 和 memory hook。
- `cross-runtime-memory-adapter`: 验证 Codex、Cursor、Trae、OpenCode、OpenClaw、Claude Code 的记忆策略映射和安全默认值。
- `design-frontend-quality-gate`: 验证 DesignDNA token、可访问性、响应式布局、前端质量和 anti-slop 约束。

`bin/super-skill live-evals --json` 会复制 fixture 到临时目录，运行 recipe 中定义的 code-based graders 和单测，并探测记忆/做梦 hook 是否只写 reviewable candidate 而不保存 raw prompt。

## 目录结构

```text
Super Skill/
├── bin/super-skill
├── scripts/super_skill.py
├── skills/
├── resources/
│   ├── design-md/
│   ├── designdna-assets/
│   ├── designdna-playground/
│   └── designdna-showcase/
├── packages/designdna-cli/
├── vendor/
│   ├── cowork/
│   └── code-skills-integrations/
├── catalog/
├── workflows/
└── docs/
```

The root-level `design-md`, `designdna`, `assets`, `playground`, `showcase`, and `packages/cli` entries are compatibility symlinks for the original DesignDNA CLI and tests.

## 重要设计决策

Installable skills 使用唯一扁平命名，方便 Codex/Claude 等 agent 目录直接加载。仓库内部仍按生命周期分组，方便人类维护。

Cowork 领域生态保留在 `vendor/cowork/` 而不是强行塞进 `skills/`，因为它包含有意复用的通用名称，例如 `call-prep` 和 `competitive-analysis`。这部分作为领域插件素材与未来命名空间化来源。

DesignDNA 被保留为主技能和资源库：主技能在 `skills/04-design-system/designdna/`，品牌系统在 `resources/design-md/`，CLI 在 `packages/designdna-cli/`。

## 验证

```bash
bin/super-skill doctor
bin/super-skill validate
bin/super-skill plan --profile core --json
bin/super-skill plan --profile hermes --json
bin/super-skill audit --json
bin/super-skill harness --json
bin/super-skill hermes --json
bin/super-skill memory --json
bin/super-skill triggers --json
bin/super-skill evals --json
bin/super-skill live-evals --json
bin/super-skill memory-plugin --dry-run --json
bin/super-skill install --profile core --dry-run --json
bin/super-skill install --profile core --dry-run --with-memory-plugin --json
python3 -m unittest discover -s tests
npm --prefix packages/designdna-cli test
```

CI 会运行 `doctor`、`validate`、`plan`、Hermes profile plan、`audit`、`harness`、`hermes`、`memory`、`triggers`、`evals`、`live-evals`、`memory-plugin` dry-run、Python CLI 测试，以及 DesignDNA CLI 测试，确保结构、兼容、安全、自动触发、验证性项目、live 项目 grader、harness readiness、self-improving agent readiness、agent memory readiness 和基础工具链可用。

## 文档

- [生命周期地图](catalog/lifecycle-map.md)
- [技能索引](catalog/skill-index.md)
- [研究与编排分析](catalog/source-audit.md)
- [ECC/Superpowers 深度分析](catalog/ecc-superpowers-analysis.md)
- [AI-first Harness Analysis](docs/ai-first-harness-analysis.md)
- [Harness Engineering Validation](docs/harness-engineering-validation.md)
- [Hermes Engineering Analysis](docs/hermes-engineering-analysis.md)
- [Dev Tool, Model, and Memory Adaptation](docs/dev-tool-model-memory-adaptation.md)
- [端到端工作流](workflows/research-to-delivery.md)
- [Agentic 上下文到交付工作流](workflows/agentic-context-to-delivery.md)
- [Harness Engineering Operating Loop](workflows/harness-engineering-operating-loop.md)
- [Hermes Engineering Learning Loop](workflows/hermes-engineering-learning-loop.md)
- [Adaptive Agent Memory Harness Loop](workflows/adaptive-agent-memory-harness-loop.md)
- [Agentic Development Model](docs/agentic-development-model.md)
- [LLM 输入/输出质量](docs/llm-io-quality.md)
- [兼容性说明](docs/compatibility.md)
- [选择性安装](docs/selective-install.md)
- [可靠性与安全](docs/reliability-and-security.md)
- [维护指南](docs/maintenance.md)
