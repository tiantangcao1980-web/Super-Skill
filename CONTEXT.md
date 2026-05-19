# Super Skill

Super Skill 是一个面向 AI coding agent 的 **lifecycle 技能集合 + 可安装 CLI + 跨工具适配器**。本文件只钉项目级领域语言，避免对话和 PR 中术语漂移。实现细节请看 `AGENTS.md`、`docs/`、`README.md`。

## 语言（术语表）

**Skill**：
一个独立的能力单元，承载形态固定为 `<skill-root>/SKILL.md`（带 YAML frontmatter）+ 可选 `references/` `scripts/` `assets/`。
_Avoid_：plugin、module、prompt-template。

**Installable Skill**：
位于 `skills/<stage>/<name>/` 下、名称在仓库内全局唯一的 skill；可被 `bin/super-skill install` 平铺到目标 agent 目录。121 个。
_Avoid_：vendor skill、profile、catalog entry。

**Vendor Skill**：
位于 `vendor/cowork/<domain>/<version>/skills/<name>/` 的领域 skill 源材料；不能直接 install，必须经 `cowork-<domain>-<name>` 别名 promote。
_Avoid_：installable skill、third-party plugin。

**Profile**：
`manifests/install-profiles.json` 里声明的一组 installable skills 安装预案：`ultra-lite`、`core`、`dev`、`design`、`hermes`、`all`。
_Avoid_：preset、bundle、collection。

**Atom**：
不可再分的能力原语，是 autopilot/auto-flow 里 phase 由 skill 组合的最小单位。例：`intent-contract-form`、`ralph-attempt`、`critique-jury`、`memory-candidate-emit`。声明在 `manifests/atoms.json`，由 `skills/00-orchestration/atom-catalog/SKILL.md` 描述合成规则。
_Avoid_：skill（更粗）、tool call（更细）、phase（更粗）。

**Phase**：
autopilot 12 阶段中的一格（`00-research` … `11-ops-retrospective`），每个 phase 由若干 atom 组合而成，落盘一个 markdown/json 检查点。
_Avoid_：step、stage（"stage" 在 install profile 上下文里另有含义）。

**Stage**：
`manifests/install-profiles.json` 里的目录分组（`00-orchestration` / `01-research` / …）。Profile 通过 `stages: [...]` 选择该分组下所有 installable skills。
_Avoid_：phase、lifecycle layer。

**Run**：
一次 `bin/super-skill autopilot` 的执行实例，由 `run-id`（`YYYYMMDD-HHMMSS-ms-hash`）唯一标识，所有产物落 `<project>/.super-skill/autopilot/<run-id>/`。
_Avoid_：session、job、task。

**Ralph Attempt**：
Phase 4 (impl) 内由 `ralph-loop` 驱动的一次尝试：写候选代码 → 跑测试 → 反馈 stderr → 决定再来一轮或退出。落盘 `05-impl-sandbox/attempt-<n>/`。
_Avoid_：retry、iteration（"iteration" 是 atom 信号词，含义不同）。

**Critique Jury / Output Quality Gate**：
Phase 6 的输出质量门，由 5 个 panelist（Critic / Brand / A11y / Copy / Designer）独立打分 + 加权合成 composite。Composite ≥ 阈值（默认 8.0/10）才放行；否则触发 `revise` 或落 `ship_best`。
_Avoid_：reviewer、QA、judge（单评审者语义已被占用）。

**Memory Candidate**：
Phase 8 / memory hook 产出的 reviewable 经验条目（episodic / semantic / negative / skill-evolution），默认不自动 promote 到 durable memory；通过 `manifests/skill-lifecycle-policy.json` 的 rubric review 才入库。**绝不存 raw prompt / raw response**。
_Avoid_：transcript、log、durable memory（已 promote 的才叫 durable）。

**Protected Skill**：
`manifests/skill-lifecycle-policy.json` 中标记为 critical / important 的 18 个 skill，**不可被自动 archive、自动 delete、自动重写**；演化必须经人审。
_Avoid_：core skill（"core" 已被 profile 用走）、locked skill。

**Risky Pattern**：
`bin/super-skill audit` 在 skills 文件里发现的、可能造成破坏性操作的命令模式（`rm -rf`、`curl ... | sh`、`git reset --hard`…）。被分类为 `governed`（在 `safe-command-governance` 白名单内）或 `ungoverned`（必须修复）。
_Avoid_：vulnerability、security finding（已被 `security-review` 占用）。

**Trigger Phrase**：
一个 skill 在 SKILL.md frontmatter `triggers:` 或 description 里声明的、用来让 agent 隐式触发本 skill 的自然语言短语。**全局不可与其它 skill 的 trigger 重叠**，由 `bin/super-skill audit` 检查。
_Avoid_：keyword、prompt hook。

**Compatibility Symlink**：
仓库根的 6 个软链（`assets` / `design-md` / `designdna` / `playground` / `showcase` / `packages/cli`），存在仅为兼容上游 DesignDNA CLI 和测试，**不是工作目录**。
_Avoid_：alias、shortcut。

## 关系

- 一个 **Profile** 等于若干 **Stage** 下所有 **Installable Skill** 的并集，减去显式排除项。
- 一个 **Run** 由 12 个 **Phase** 组成；每个 Phase 调用若干 **Skill**，每个 Skill 由若干 **Atom** 组合实现。
- 一个 **Phase 5 (impl)** 包含 ≥ 1 个 **Ralph Attempt**。
- 一个 **Phase 6 (gate)** 产生恰好 1 个 **Critique Jury** 结果。
- 一个 **Run** 产生 0..N 个 **Memory Candidate**；只有通过 review 的才 promote 为 durable memory。
- **Protected Skill** 不会出现在自动 archive/delete 提案里，但仍可出现在所有 **Profile** 中。
- **Risky Pattern** 在 audit 中必须全部 governed；任何 ungoverned 都使 `audit` 失败。

## 示例对话

> **Dev**：autopilot 跑完了为什么 phase 6 还没 ship？
> **Domain**：因为 **Critique Jury** 的 **composite** 没到 8.0，触发了一轮 revise；这不是 fail，是收敛中。最多 3 轮，仍不过会 fallback 到 `ship_best`。run.json 的 phase-6 字段里能看到每轮 panelist 分数。

> **Dev**：这条经验记到 memory 了吗？
> **Domain**：当前只是 **memory candidate**，没自动 promote。要让它成为 durable memory，得先过 `skill-lifecycle-policy.json` 的 rubric review，并且确认没有 raw prompt 泄漏。

## 已标记歧义

- "**stage**" 之前在 profile 上下文（目录分组）和 autopilot 上下文（执行格子）都被使用；本文件正式拆分为 **Stage**（profile）+ **Phase**（autopilot）。
- "**iteration**" 既是 ralph-loop 的尝试数也是 critique jury 的轮次；本文件用 **Ralph Attempt** 和 **Critique Round** 分别命名。
