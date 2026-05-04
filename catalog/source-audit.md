# Source Audit

## code-skills

定位：工程/交付工作流骨架。

保留价值：

- `auto-flow` 和 `design-dev-flow` 提供端到端编排。
- `user-research`, `requirement-analysis`, `product-spec` 补齐上游产品链路。
- `qa-strategy`, `browser-automation`, `code-simplifier` 补齐质量链路。
- `programmatic-video` 把交付延伸到演示和增长素材。
- CLI 思路适合 Super Skill 继续沿用：可 list、validate、doctor、install、describe。

处理方式：

- 15 个核心技能按生命周期迁移到 `skills/`。
- 原集成资料迁移到 `vendor/code-skills-integrations/`。
- Cowork 领域生态迁移到 `vendor/cowork/`。

## DesignDNA-Skills

定位：设计系统和审美纠偏层。

保留价值：

- `designdna` 主技能提供 DESIGN.md 方法、品牌 DNA、反 slop 检查。
- 58 套品牌设计系统可直接作为视觉参考和 token 来源。
- 47 个设计/组件库子技能补齐多端 UI 生态。
- CLI 可继续生成 design tokens、CSS、Tailwind、TS 等产物。

处理方式：

- `designdna` 主技能和子技能迁移到 `skills/04-design-system/designdna/`。
- `design-md/` 迁移到 `resources/design-md/`。
- CLI 迁移到 `packages/designdna-cli/`。

## Codex / Plugin Lessons

归纳出的可复用经验：

- 技能需要 progressive disclosure：frontmatter 负责触发，正文负责流程，references/scripts/assets 按需加载。
- 验证必须证据优先，不能用“应该可以”替代命令结果。
- 工具路由应优先轻量、直接、可验证。
- 跨工具打包必须保持 `SKILL.md` 为 source of truth。

处理方式：

- 新增 `skills/90-codex-patterns/*` 四个原创模式技能。
- `scripts/super_skill.py` 实现嵌套发现、扁平安装、验证和目录生成。

## NousResearch/hermes-agent

定位：自进化 agent 运行系统与长期上下文工程参考。

保留价值：

- 渐进式技能加载：技能索引轻量，技能正文和 references/scripts/assets 按需加载。
- 记忆分层：长期记忆、用户画像、会话搜索、项目上下文和技能各自承担不同职责。
- 上下文缓存与压缩：稳定系统层和临时任务层分离，避免长会话持续膨胀。
- 工具集与沙箱：按任务开放最小工具能力，并使用审批、容器/远程环境和隔离边界控制风险。
- 持久任务队列：长期、多角色、人机协同任务需要 board/queue，而不只是一次性 subagent 调用。
- 安全回滚：高速 agent 编辑需要 checkpoint、worktree、dry-run 和恢复路径配套。

处理方式：

- 新增 `persistent-memory-curation`, `skill-evolution-loop`, `prompt-cache-layering`, `toolset-sandbox-routing`, `durable-agent-board`, `checkpoint-rollback-safety`。
- 新增 `docs/hermes-engineering-analysis.md` 与 `workflows/hermes-engineering-learning-loop.md`。
- 新增 `bin/super-skill hermes` readiness 检查，作为 Hermes-style self-improving agent 能力矩阵。
