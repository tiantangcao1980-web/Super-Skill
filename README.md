# Super Skill

Super Skill 是一个面向 AI coding agent 的全流程技能集合：从用户意图、上下文工程、市场/用户调研，到需求分析、产品规格、设计系统、接口与开发、测试验证、交付增长、运维知识沉淀，形成一套可安装、可验证、可继续扩展的 skills 生态。

它的目标不是简单增加技能数量，而是提升 LLM 输入和输出质量：把用户期待转成可验收契约，把大上下文压缩成高信号上下文包，把 agent 输出重新拉回用户目标、证据和质量门。

本仓库整合并重新编排了：

- `code-skills` 的端到端工作流、调研、产品、设计、测试、交付和工具型技能
- `DesignDNA-Skills` 的 DesignDNA 主技能、47 个设计/组件库子技能、58 套品牌设计系统和 CLI
- 本机 Codex 技能体系中的工程能力层：API、前端、后端、数据库、调试、安全、部署、GitHub、Docker、文档等
- Codex/插件经验沉淀：技能编写、验证闭环、工具路由、跨工具打包
- `everything-claude-code` 的选择性安装、能力面划分、适配政策、安全审计思路
- `obra/superpowers` 的 TDD、系统化调试、技能演进、完成前验证方法
- Cowork 领域生态作为 `vendor/cowork/` 保留：法律、财务、销售、营销、客服、数据、HR/ops 等领域插件素材

## 能力闭环

| 阶段 | 目录 | 代表技能 |
| --- | --- | --- |
| 编排/输入质量 | `skills/00-orchestration` | `intent-contract`, `context-engineering`, `auto-flow`, `design-dev-flow`, `ralph-loop` |
| 调研 | `skills/01-research` | `user-research`, `market-research` |
| 分析 | `skills/02-analysis` | `requirement-analysis`, `data-analysis` |
| 产品 | `skills/03-product` | `product-spec` |
| 设计 | `skills/04-design-system` | `designdna`, `design-templates`, 47 个 UI/组件库技能 |
| 接口/CLI | `skills/05-interface-and-cli` | `api-design`, `api-gateway`, `cli-design`, `create-cli` |
| 开发 | `skills/06-development` | `frontend-patterns`, `backend-patterns`, `database-patterns`, `ai-agent-frameworks`, `chatgpt-apps` |
| 测试/输出质量 | `skills/07-testing-and-quality` | `qa-strategy`, `output-quality-gate`, `browser-automation`, `code-review`, `security-review`, `debugging` |
| 交付/增长 | `skills/08-delivery-and-growth` | `deployment-patterns`, `docker`, `git`, `github`, `programmatic-video` |
| 运维/知识 | `skills/09-operations-and-knowledge` | `file-curation`, `documentation`, `continuous-learning` |
| Codex/上下文模式 | `skills/90-codex-patterns` | `token-budgeting`, `skill-authoring-system`, `verification-loop`, `agent-routing`, `cross-tool-packaging` |

当前清单：

- 97 个可安装生命周期技能
- profile/component manifest 支持只读安装预案
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

# 安装完整集合到 Codex skills 目录，默认软链
bin/super-skill install --profile all --target ~/.codex/skills

# 只安装开发相关能力
bin/super-skill install --profile dev --target ~/.codex/skills

# 安装到 Claude Code
bin/super-skill install --profile core --target ~/.claude/skills

# 生成索引
bin/super-skill catalog
```

Profiles:

- `core`: 从调研到交付的主流程，不强调具体开发栈扩展
- `dev`: 接口、前后端、数据库、测试、交付、运维
- `design`: DesignDNA、设计系统、UI 库与质量约束
- `all`: 所有可安装技能

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
bin/super-skill audit --json
bin/super-skill install --profile core --dry-run --json
python3 -m unittest discover -s tests
npm --prefix packages/designdna-cli test
```

CI 会运行 `doctor`、`validate`、`plan`、`audit`、Python CLI 测试，以及 DesignDNA CLI 测试，确保结构、兼容、安全和基础工具链可用。

## 文档

- [生命周期地图](catalog/lifecycle-map.md)
- [技能索引](catalog/skill-index.md)
- [研究与编排分析](catalog/source-audit.md)
- [ECC/Superpowers 深度分析](catalog/ecc-superpowers-analysis.md)
- [端到端工作流](workflows/research-to-delivery.md)
- [Agentic 上下文到交付工作流](workflows/agentic-context-to-delivery.md)
- [Agentic Development Model](docs/agentic-development-model.md)
- [LLM 输入/输出质量](docs/llm-io-quality.md)
- [兼容性说明](docs/compatibility.md)
- [选择性安装](docs/selective-install.md)
- [可靠性与安全](docs/reliability-and-security.md)
- [维护指南](docs/maintenance.md)
