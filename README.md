# Super Skill

[![CI](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/ci.yml/badge.svg)](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/ci.yml)
[![Quality](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/quality.yml/badge.svg)](https://github.com/tiantangcao1980-web/Super-Skill/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-122-blue)](catalog/skill-index.md)
[![Profiles](https://img.shields.io/badge/profiles-ultra--lite%20%7C%20core%20%7C%20dev%20%7C%20design%20%7C%20hermes%20%7C%20all-green)](manifests/install-profiles.json)

> **Thesis.** AI coding agents fail in four predictable ways: they don't do what the user actually wanted (input quality), they ramble (output quality), the code doesn't run (verification), and yesterday's lesson never reaches today's session (memory). Super Skill is a 121-skill collection plus a runnable harness CLI built around exactly those four failure modes — every skill front-loads its trigger condition, every loop has a hard quality gate, and the autonomous closed loop (`bin/super-skill autopilot`) drives one prompt through **research → intent → business case → spec → design → ralph-loop implementation (Python/JS/Bash/Go) → simplifier → quality gate → launch readiness → pilot → commercial delivery → ops & retrospective** — all 12 phases mapped 1:1 to the standard 10-stage commercial project lifecycle (需求 → 商业交付). Every artifact is checkpointed on disk with cross-run iteration via `--based-on / --feedback` and parallel multi-agent fanout via `bin/super-skill fanout --tracks`.

## ⚡ Quick start (autonomous closed loop)

```bash
# Offline deterministic stub — CI safe, no API key needed:
bin/super-skill autopilot --provider stub --prompt "Build a TODO list API with tests"

# Real LLM:
ANTHROPIC_API_KEY=sk-... bin/super-skill autopilot --provider anthropic \
    --prompt "Build a TODO list API with tests" --project ./build
```

Each phase loads the canonical SKILL.md as its system prompt, calls the LLM (or stub), and writes a checkpoint under `<project>/.super-skill/autopilot/<run-id>/`. Phases 1 (intent contract) and 6 (output quality gate) are hard exits. Phase 4 wraps `ralph-loop` for iterative implementation and **actually runs the generated Python via unittest / bare-tests / py-compile**, feeding stderr back into the next attempt. Phase 7 produces a delivery plan (Dockerfile + CI workflow + kill switch + rollback). Phase 8 produces a Hermes-style reviewable memory candidate without ever echoing the raw prompt.

## What's inside

Super Skill 是一个面向 AI coding agent 的全流程技能集合：从用户意图、上下文工程、市场/用户调研，到需求分析、产品规格、设计系统、接口与开发、测试验证、交付增长、运维知识沉淀，形成一套可安装、可验证、可继续扩展的 skills 生态。

它的目标不是简单增加技能数量，而是提升 LLM 输入和输出质量：把用户期待转成可验收契约，把大上下文压缩成高信号上下文包，把 agent 输出重新拉回用户目标、证据和质量门。

最新一层能力是 AI-first harness engineering + Hermes-style self-improving agent engineering：让项目架构、CI/CD、代码评审、实验发布、可观测性、长期记忆、技能演进、工具路由、模型约束、开发工具适配和回滚安全都变得 agent 可读、可执行、可验证。

本仓库整合并重新编排了：

- `code-skills` 的端到端工作流、调研、产品、设计、测试、交付和工具型技能
- `DesignDNA-Skills` 的 DesignDNA 主技能、47 个设计/组件库子技能、58 套品牌设计系统和 CLI
- `pbakaus/impeccable` 的上下文门禁、设计命令词汇和确定性反套路检测理念，以 Super Skill 原生方式吸收为 `design-craft-gate` 与 `design-audit`
- 本机 Codex 技能体系中的工程能力层：API、前端、后端、数据库、调试、安全、部署、GitHub、Docker、文档等
- Codex/插件经验沉淀：技能编写、验证闭环、工具路由、跨工具打包
- `everything-claude-code` 的选择性安装、能力面划分、适配政策、安全审计思路
- `obra/superpowers` 的 TDD、系统化调试、技能演进、完成前验证方法
- `forrestchang/andrej-karpathy-skills` 的思考先行、简单优先、外科手术式改动和目标驱动验证原则
- `mattpocock/skills` 的 CONTEXT.md、ADR、领域语言、docs-backed review 和架构维护经验
- `NousResearch/hermes-agent` 的渐进式技能加载、长期记忆分层、上下文缓存、工具集路由、持久任务队列、定时任务和安全回滚理念
- Cowork 领域生态作为 `vendor/cowork/` 保留：法律、财务、销售、营销、客服、数据、HR/ops 等领域插件素材

## 能力闭环

| 阶段 | 目录 | 代表技能 |
| --- | --- | --- |
| 编排/输入质量 | `skills/00-orchestration` | `intent-contract`, `goal-driven-workflow`, `context-engineering`, `prompt-cache-layering`, `toolset-sandbox-routing`, `durable-agent-board`, `ralph-loop` |
| 调研 | `skills/01-research` | `user-research`, `market-research` |
| 分析 | `skills/02-analysis` | `requirement-analysis`, `data-analysis` |
| 产品 | `skills/03-product` | `product-spec`, `agentic-product-iteration` |
| 设计 | `skills/04-design-system` | `design-craft-gate`, `designdna`, `design-templates`, `anti-slop`, 47 个 UI/组件库技能 |
| 接口/CLI | `skills/05-interface-and-cli` | `api-design`, `api-gateway`, `cli-design`, `create-cli` |
| 开发 | `skills/06-development` | `agent-legible-architecture`, `frontend-patterns`, `backend-patterns`, `database-patterns`, `ai-agent-frameworks` |
| 测试/输出质量 | `skills/07-testing-and-quality` | `agent-eval-harness`, `ai-review-gates`, `checkpoint-rollback-safety`, `qa-strategy`, `output-quality-gate`, `browser-automation`, `security-review` |
| 交付/增长 | `skills/08-delivery-and-growth` | `experiment-driven-delivery`, `deployment-patterns`, `docker`, `git`, `github` |
| 运维/知识 | `skills/09-operations-and-knowledge` | `observability-triage-loop`, `agent-memory-dream-loop`, `persistent-memory-curation`, `file-curation`, `documentation`, `continuous-learning` |
| Codex/Hermes/上下文模式 | `skills/90-codex-patterns` | `harness-engineering`, `dev-tool-adapter`, `model-adaptation-contract`, `skill-evolution-loop`, `token-budgeting`, `skill-authoring-system`, `verification-loop`, `agent-routing` |

当前清单：

- 122 个可安装生命周期技能（含新增的 `atom-catalog`）
- 1 个 Codex 插件：`super-skill-memory-harness`
- profile/component manifest 支持只读安装预案
- automatic trigger / skill lifecycle manifest 支持自动触发、可控记忆、技能去重和可逆归档
- 7 个验证性项目 eval fixtures，覆盖端到端交付、goal-driven delivery、ultra-lite 工程纪律、跨工具记忆、设计前端质量、事故学习闭环和 token-efficient LLM I/O
- 4 个 live eval projects，在临时目录生成小型交付物并运行本地 grader、单测和 memory hook probe
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

# 安装少而强的工程纪律 profile：目标契约、TDD、review、验证、ADR、危险命令治理和记忆卫生
bin/super-skill install --profile ultra-lite --target ~/.codex/skills --dry-run --json

# 审计去重、manifest、兼容软链、入口文件、疑似密钥和风险命令
bin/super-skill audit --json

# UI 变更前检查 PRODUCT/DESIGN、shape brief、tokens、视觉参考和反套路门禁
bin/super-skill design-preflight --project ./app --strict --json

# 从现有前端提取设计 token、组件和 utility-class 信号，可写入 sidecar / DESIGN 草案
bin/super-skill design-extract --project ./src \
  --write-sidecar .super-skill/design/design.json \
  --write-design .super-skill/design/DESIGN.generated.md --json

# 生成浏览器设计现场面板：overlay、computed styles、对比度探针、CSS 变量 live variant
bin/super-skill design-live --project ./src \
  --target-url http://localhost:3000 \
  --output .super-skill/design/live.html --json

# 同步生成可加载的 Chrome/Chromium unpacked extension
bin/super-skill design-live --project ./src \
  --write-extension .super-skill/design/extension --json

# 生成/运行真实浏览器注入截图链路；dry-run 不要求安装 Playwright
bin/super-skill design-capture --project . \
  --backend playwright \
  --url http://localhost:3000 \
  --screenshot .super-skill/design/live.png \
  --report .super-skill/design/capture.json \
  --runner .super-skill/design/capture.mjs --dry-run --json

# 已安装/可安装 Playwright 后，可去掉 --dry-run 执行真实截图
npm install
npm run playwright:install

# 需要复用 CLI/真实会话探索时，也可以使用 browser-use 后端
bin/super-skill design-capture --project . \
  --backend browser-use \
  --url http://localhost:3000 \
  --screenshot .super-skill/design/browser-use.png \
  --report .super-skill/design/browser-use.json --json

# 扫描前端文件中的 AI 设计套路和可机器发现的设计质量风险
bin/super-skill design-audit --project ./src --json

# 评估项目的 AI-first harness readiness
bin/super-skill harness --json

# 评估 Hermes-style self-improving agent readiness
bin/super-skill hermes --json

# 评估 agent memory / dream replay readiness
bin/super-skill memory --json

# 校验自动触发策略、技能自我进化约束、protected skills 和去重门
bin/super-skill triggers --json

# 生成审计友好的 Codex /goal: Scope + Constraints + Done when + Stop if + token budget
bin/super-skill goal \
  --objective 'Implement openspec/changes/add-rerank exactly as specified' \
  --sdd-path openspec/changes/add-rerank \
  --scope 'openspec/changes/add-rerank; src/retrieval; tests/retrieval' \
  --done 'Each task in openspec/changes/add-rerank/tasks.md is checked off with file evidence' \
  --done '`npm test` exits 0 and summary is pasted' \
  --done 'Each SHALL has a passing test name cited in tests/retrieval' \
  --stop-if 'A SHALL conflicts with another SHALL in specs/' \
  --stop-if 'A new dependency requires npm install' \
  --stop-if 'git diff touches auth/ or billing/ outside scope' \
  --budget 120000

# 运行验证性项目，证明 skills 集合是否覆盖初衷和预期
bin/super-skill evals --json

# 运行可执行 live eval 项目，验证临时项目交付物、测试和 memory hook
bin/super-skill live-evals --json

# 预览安装 Codex 记忆/做梦自动插件，不修改本机配置
bin/super-skill memory-plugin --dry-run --json

# 安装完整集合到 Codex skills 目录，默认软链
bin/super-skill install --profile all --target ~/.codex/skills

# 安装 ultra-lite 最小工程闭环
bin/super-skill install --profile ultra-lite --target ~/.codex/skills

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
# Phase 4 真跑生成的 Python（unittest / bare-tests / py-compile），失败 stderr 回喂 ralph-loop

# 续跑被中断的 run（默认最新；--list 只看 pending vs completed 不重跑）
bin/super-skill resume --project ./build --list
bin/super-skill resume --project ./build

# 把 run.json 渲染成单页 HTML 时间线（自包含、无依赖）
bin/super-skill visualize --project ./build
# 输出：<project>/.super-skill/autopilot/<run-id>/timeline.html
# 如果该 run 是 iterate-mode 的子代，timeline 顶部会渲染 Lineage 链

# 跨 run 迭代：把上一次 run 的全部产物 + 你的反馈喂给新 run，每阶段产 UPDATED 版本
# parent_run_id / lineage / feedback 全部进 run.json 留底
bin/super-skill autopilot --based-on <parent-run-id> --project ./build \
    --feedback "Reviewers say the error message is too terse; expand it and add a 4xx error code"

# 多智能体并行 (fanout): 一个 prompt 拆 N 个 track，每 track 独立 autopilot，并行跑
# 每 track 的 run.json 反指 fanout_id；汇总写到 .super-skill/fanout/<id>/fanout.json
bin/super-skill fanout --provider stub --project ./build \
    --prompt "Build BayGo ride matching" \
    --tracks "frontend-miniapp,backend-api,docs"
bin/super-skill visualize --project ./build --fanout-id <fanout-id>  # 多 track 汇总 HTML

# MCP server 化：让 Claude Desktop / Cursor 直接像调函数一样触发
python3 plugins/super-skill-mcp-server/scripts/mcp_server.py
# 配置参考：plugins/super-skill-mcp-server/README.md
```

### 完整 demo（含 sample 产物）

`examples/autopilot-demo/` 内含：

- `run-real-autopilot.sh` — 设了 `ANTHROPIC_API_KEY` 走真实 API；没设自动 fallback 到 stub
- `sample-run/` — 一次 stub 跑出来的 7 阶段产物 + run.json + timeline.html，作为"成品长什么样"的参考

Profiles:

- `ultra-lite`: 少而强的工程纪律闭环，只安装目标契约、TDD、review、验证、ADR/领域语言、安全命令治理、token 和记忆卫生核心技能
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

`evals/projects/` 中保留 7 个验证性项目：

- `ai-first-saas-launch`: 验证从调研、产品、设计、开发、测试、交付到运维/记忆的全链路覆盖。
- `goal-driven-delivery`: 验证 Codex `/goal`、OpenSpec/SDD、Ralph Loop、code-simplifier、完成审计和记忆复盘能组成长任务闭环。
- `ultra-lite-engineering-discipline`: 验证 Superpowers、Karpathy-style guardrails 和 Matt Pocock CONTEXT/ADR 经验被压缩成少而强、可安装、可验证的工程纪律 profile。
- `cross-runtime-memory`: 验证 Codex plugin/hook 与 Claude Code、Cursor、Trae、OpenCode、OpenClaw fallback 的一致性。
- `design-to-frontend-quality`: 验证 design-craft-gate、DesignDNA、UI 框架、前端质量、PRODUCT/DESIGN 上下文、反套路审计与品牌系统同步。
- `incident-to-learning-loop`: 验证可观测性、调试、安全评审、回归 eval、负面记忆和技能演化门。
- `token-efficient-llm-io`: 验证 intent/context/token/model/output quality 的 LLM 输入输出质量闭环。

`bin/super-skill evals --json` 会机器检查每个项目的 required skills、生命周期阶段、验收语言、hook-only 插件、防 raw prompt 写入、自动触发策略和技能生命周期策略。

`evals/live-projects/` 中保留 4 个可执行 live eval 项目：

- `autopilot-end-to-end`: 验证 12 阶段 autopilot stub 闭环、run journal、质量门、商业交付与 ops retrospective。
- `mini-saas-feedback-loop`: 在临时项目中验证 feature flag、kill switch、metrics、rollback、release note、observability 和 memory hook。
- `cross-runtime-memory-adapter`: 验证 Codex、Cursor、Trae、OpenCode、OpenClaw、Claude Code 的记忆策略映射和安全默认值。
- `design-frontend-quality-gate`: 验证 design-craft-gate、DesignDNA token、PRODUCT/DESIGN 上下文、可访问性、响应式布局、前端质量和 deterministic anti-pattern 约束。

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

Cowork 领域生态保留在 `vendor/cowork/` 而不是强行塞进 `skills/`，因为它包含有意复用的通用名称，例如 `call-prep` 和 `competitive-analysis`。CLI 会为每个 vendor skill 生成确定性的安全别名：`vendor/cowork/<domain>/<version>/skills/<name>` → `cowork-<domain>-<name>`，例如 `cowork-sales-call-prep` 和 `cowork-common-room-call-prep`。`bin/super-skill audit` 会检查这些别名是否重复或撞上正式技能，`bin/super-skill vendor --write-namespace catalog/vendor-namespace.json` 可以落盘完整映射。

DesignDNA 被保留为主技能和资源库：主技能在 `skills/04-design-system/designdna/`，品牌系统在 `resources/design-md/`，CLI 在 `packages/designdna-cli/`。

## 验证

```bash
bin/super-skill doctor
bin/super-skill validate
bin/super-skill plan --profile core --json
bin/super-skill plan --profile ultra-lite --json
bin/super-skill plan --profile hermes --json
bin/super-skill audit --json
bin/super-skill design-preflight --project evals/live-projects/design-frontend-quality-gate/files --json
bin/super-skill design-extract --project evals/live-projects/design-frontend-quality-gate/files/src --json
bin/super-skill design-live --project evals/live-projects/design-frontend-quality-gate/files/src --output /tmp/super-skill-design-live.html --json
bin/super-skill design-live --project evals/live-projects/design-frontend-quality-gate/files/src --write-extension /tmp/super-skill-design-live-extension --force --json
bin/super-skill design-capture --project evals/live-projects/design-frontend-quality-gate/files --url http://localhost:3000 --runner /tmp/super-skill-design-capture.mjs --dry-run --force --json
bin/super-skill design-audit --project evals/live-projects/design-frontend-quality-gate/files/src --fail-on-findings --json
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

CI 会运行 `doctor`、`validate`、`plan`、ultra-lite profile plan、Hermes profile plan、`audit`、`design-preflight`、`design-extract`、`design-live`、`design-capture` dry-run、`design-audit`、`harness`、`hermes`、`memory`、`triggers`、`evals`、`live-evals`、`memory-plugin` dry-run、Python CLI 测试，以及 DesignDNA CLI 测试，确保结构、兼容、安全、自动触发、设计上下文门禁、设计提取、浏览器现场面板、扩展包、浏览器注入截图链路、设计反套路扫描、验证性项目、live 项目 grader、harness readiness、self-improving agent readiness、agent memory readiness 和基础工具链可用。

## 文档

- [领域词汇表 (CONTEXT.md)](CONTEXT.md)
- [通用设计 / 工程准则 (craft/)](craft/README.md)
- [Atom Catalog (manifests/atoms.json)](skills/00-orchestration/atom-catalog/SKILL.md)
- [Living specs (specs/current/)](specs/README.md)
- [生命周期地图](catalog/lifecycle-map.md)
- [技能索引](catalog/skill-index.md)
- [研究与编排分析](catalog/source-audit.md)
- [ECC/Superpowers 深度分析](catalog/ecc-superpowers-analysis.md)
- [Source Benchmark Analysis](docs/source-benchmark-analysis.md)
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
