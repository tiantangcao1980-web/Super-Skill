# vendor/cowork · Cowork knowledge-work plugins(本仓库镜像)

> 把 Anthropic Cowork(Claude Desktop)的 **19 个领域专家插件 / 67+ 个 skill** 镜像到本仓库,
> 让没装 Cowork 的用户也能直接用,装了 Cowork 的用户可以选择"上游版"或"vendor 版"。

## 为什么 vendor

Cowork 的领域 skill(legal/finance/data/...)只在 Claude Desktop 内激活,
**别人 git clone 这个仓库** 就不一定能用上 —— 这违背了"复用"目标。

参考 ralph-loop / code-simplifier 两个 plugin 的做法(已 verbatim 嵌入到对应
skill 子目录),我们把 19 个领域插件也 vendor 进来。
**保留 LICENSE / 注明出处 / 不修改源 / 改进反馈上游**。

## 一览(完整清单见 [VERSIONS.lock](VERSIONS.lock))

| Plugin | 状态 | 作者 | License | Skills |
|--------|------|------|---------|--------|
| apollo | ✅ vendored | Apollo.io | MIT | 3 |
| bio-research | ✅ vendored | Anthropic | Apache-2.0 | 5 |
| brand-voice | ✅ vendored | Tribe AI | MIT | 3 |
| common-room | ✅ vendored | Common Room | Apache-2.0 | 6 |
| cowork-plugin-management | ✅ vendored | Anthropic | Apache-2.0 | 2 |
| customer-support | ✅ vendored | Anthropic | Apache-2.0 | 5 |
| data | ✅ vendored | Anthropic | Apache-2.0 | 7 |
| **design** | 📋 placeholder | Anthropic | (no LICENSE)| - |
| **engineering** | 📋 placeholder | Anthropic | (no LICENSE)| - |
| enterprise-search | ✅ vendored | Anthropic | Apache-2.0 | 3 |
| finance | ✅ vendored | Anthropic | Apache-2.0 | 6 |
| **human-resources** | 📋 placeholder | Anthropic | (no LICENSE)| - |
| legal | ✅ vendored | Anthropic | Apache-2.0 | 6 |
| marketing | ✅ vendored | Anthropic | Apache-2.0 | 5 |
| **operations** | 📋 placeholder | Anthropic | (no LICENSE)| - |
| product-management | ✅ vendored | Anthropic | Apache-2.0 | 6 |
| productivity | ✅ vendored | Anthropic | Apache-2.0 | 3 |
| sales | ✅ vendored | Anthropic | Apache-2.0 | 6 |
| slack-by-salesforce | ✅ vendored | Salesforce | MIT | 2 |

**4 个 placeholder**:Anthropic 但缺 LICENSE 文件。法律保守,只 vendor 描述,
不分发实际内容。详见 [NOTICE](NOTICE)。

## 怎么用

### 列出 vendor 内容
```bash
bin/code-skills vendor list                  # 19 个 plugin
bin/code-skills vendor list --json           # 机器可读
bin/code-skills vendor status                # 哪些已激活
```

### 激活某 plugin(装到 ~/.claude/plugins/code-skills-vendor/)
```bash
bin/code-skills vendor install legal         # 激活 legal 6 skill
bin/code-skills vendor install finance       # 激活 finance 6 skill
bin/code-skills vendor install --all-vendored  # 激活全部 15 个完整 vendor 版
```

激活后:slash 命令(如 `/contract-review`)和 agent skill(如 `Agent(subagent_type="financial-statements")`)在 Claude Code 会话里可用。

### 从 Cowork 上游同步(diff & sync)
```bash
bin/code-skills vendor diff                  # 对比 vendor vs 用户 Cowork cache
bin/code-skills vendor sync                  # 把上游更新拉到 vendor/(只对已 LICENSE 的)
```

`sync` 会:
1. 检查每个 plugin 在 `~/Library/Application Support/Claude/.../knowledge-work-plugins/<plugin>/` 是否有更新
2. 如果有,且仍有 LICENSE → cp -R 覆盖 vendor/
3. 更新 VERSIONS.lock
4. 打印改动摘要

## 升级 / 反馈上游流程

```
[code-skills 用户发现 bug 或改进点]
      ↓
[在 vendor/cowork/<plugin>/.../<skill>/SKILL.md 改]
      ↓
[文件顶部加修改注释:"Modified by code-skills on YYYY-MM-DD: <reason>"]
      ↓
[提交 PR 到 Anthropic claude-plugins-official(或对应作者仓库)]
      ↓
[上游接受 → 我们跑 vendor sync 拉回]
```

**永远不长期保留 divergent fork** —— 改进必须回流上游。

## 不集成的部分

- 不修改 LICENSE 文件
- 不剥除上游 attribution
- 不二次打包成自己的"产品"
