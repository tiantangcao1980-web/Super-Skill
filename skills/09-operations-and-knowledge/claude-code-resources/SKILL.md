---
name: claude-code-resources
description: |
  Claude Code 生态资源索引 skill:用户问"哪里找 plugin / hook 怎么写 / awesome 列表 / 教程"等问题时触发,给出具体推荐和导航。
  包含:plugin marketplace、skill 仓库、hook 范例、社区 awesome 列表、最佳实践博客、Anthropic 官方资源。
  触发词:「Claude Code 资源」「awesome claude code」「plugin 找哪里」「hook 教程」「skill 找哪里」「Claude Code 怎么入门」「Claude Code 配置」。
  适用阶段:新人入门、找现成解决方案、对标他人配置。
---

# Claude Code Resources · 生态资源索引

> 灵感:[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) —— Claude Code 资源大全。
> 本 skill **不抄袭那份列表**,而是抽出"用户场景 → 最相关资源"的映射,帮 agent 直接给出可下手的推荐。

## 资源分类 + 何时用

### 1. Plugins(插件)

| 来源 | 何时去 |
|------|--------|
| `claude-plugins-official` marketplace | 官方插件,质量高,优先看(本仓库已嵌入 ralph-loop / code-simplifier 两份) |
| `everything-claude-code` 列表 | 社区精选,功能各异,按需找 |
| GitHub `topic:claude-code-plugin` | 长尾,数量大但参差 |

### 2. Skills

| 来源 | 何时去 |
|------|--------|
| `obra/superpowers` | 高质量 skill 集合,含 plan-loop、investigate 等元 skill |
| `Leonxlnx/taste-skill` | 审美/品味 skill |
| `~/.claude/skills/` 本地装载 | 用户已安装的 90+ skill,先看本地有没有再去外面找 |

### 3. Hook 范例
- **官方文档**: `https://docs.claude.com/en/docs/claude-code/hooks`
- **本仓库 ralph-loop plugin**: 一份完整 Stop hook 实现(140 行 bash + jq + perl)
- **awesome lists**: 搜 `claude-code-hooks`

### 4. 教程 / 博客
- Geoffrey Huntley's *Ralph* article — `https://ghuntley.com/ralph/`
- Anthropic 官方 docs — `https://docs.claude.com/`
- `everything-claude-code` 的 articles 章节

### 5. CLI / SDK
- Claude Code CLI 自身
- `@anthropic-ai/claude-agent-sdk` (Node)
- `@anthropic-ai/sdk` (Node) / `anthropic` (Python)
- `Claude API` (推荐 prompt caching)

### 6. 社区
- Discord (Anthropic 官方)
- HackerNews thread on Claude Code
- Twitter/X #claudecode

---

## 工作流(本 skill 被触发后)

### Step 1:识别用户场景
按下面分流,**不要把全列表倒给用户**:

| 用户问题模式 | 推荐路径 |
|-------------|----------|
| "我想做 X 功能,有现成的吗" | 先查 `~/.claude/skills/`,再查 superpowers,最后查 awesome 列表 |
| "怎么写一个 hook" | 先看 ralph-loop plugin 的实现 → 再看官方 docs → 再仿写 |
| "Claude Code 怎么入门" | 给三个东西:CLI 安装 / 一份 CLAUDE.md / 一个简单 plugin |
| "怎么调 Claude API" | 走 `claude-api` skill,不走本 skill |
| "找一个 Claude 模型" | 给最新模型 ID 列表(opus 4.7 / sonnet 4.6 / haiku 4.5) |

### Step 2:**最多推荐 3 个资源**
不要堆链接墙。给 3 个最相关的,每个一句话说清:**这个解决你什么、装/用怎么开始、坑在哪**。

### Step 3:本地 skill 优先
用户机器上已经装的 skill > 外部仓库。先 `ls ~/.claude/skills/ | grep <keyword>`,有就推荐本地的,没有再去找外部。

---

## 反模式

- ❌ **链接墙**:抛 20 个 GitHub URL 让用户自己选
- ❌ **重复推荐**:同一个仓库提三遍
- ❌ **忽略本地**:用户本机已装的优先
- ❌ **过期链接**:推荐前简单验证还活着(GitHub 仓库可访问)
- ❌ **不区分官方/社区**:官方资源要明确标注,社区资源要说"质量参差"

---

## 与其他 skill 的关系

- `claude-api` 处理 API 调用问题,本 skill 处理"我想找一个能用的资源"问题
- `skill-authoring` 处理"我要写一个 skill",本 skill 处理"我要找一个 skill"

---

## References

- [资源场景速查表](references/scenario-map.md)
