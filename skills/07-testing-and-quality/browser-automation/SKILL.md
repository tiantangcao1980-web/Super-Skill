---
name: browser-automation
description: |
  浏览器自动化 skill:LLM 探索 + Playwright 稳定回归 + Chrome MCP 真实交互三档,按场景选最轻量的。
  覆盖 browser-use(Python LLM 驱动)、agent-browser(Vercel agent + 浏览器)、Playwright(工业级 E2E)、claude-in-chrome MCP(用户真实会话)。
  触发词:「浏览器自动化」「E2E 测试」「agent 操作浏览器」「browser-use」「agent-browser」「Playwright」「视觉回归」「网页自动化」「填表机器人」。
  适用阶段:design-dev-flow ⑥ 验证幕、写爬虫、做 E2E 回归、需要登录态的真实交互。
---

# Browser Automation · 浏览器自动化

> 灵感:[browser-use](https://github.com/browser-use/browser-use) + [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)。
> 核心心法:**先用 LLM 探索找路径,再用 Playwright 固化为稳定脚本**。

## 三档选型表

| 场景 | 推荐工具 | 一句话 |
|------|---------|-------|
| 看一眼当前页面 | Claude Preview MCP | 最轻,无需启浏览器 |
| 探索性测试(路径未知) | browser-use(Python + LLM) | 给目标,LLM 自己点 |
| Agent 在 Vercel/Edge 上跑 | agent-browser | Serverless 友好 |
| 稳定 E2E 回归(进 CI) | Playwright | 工业标准,有 trace |
| 需要用户真实登录态 | claude-in-chrome MCP | 用现有 Cookie/会话 |

**默认推荐**:开发期 → Preview MCP;PR 前 → Playwright;探索 → browser-use。

---

## 工作流

### 模式 A · LLM 探索(browser-use 风格)

适合"路径未知,先摸清楚怎么走":

```python
# 伪代码,实际接 browser-use API
from browser_use import Agent, Browser
agent = Agent(task="在 GitHub 上找 obra/superpowers 仓库,star 它", llm=...)
result = await agent.run()
# 结果包含每一步的 DOM action,导出后翻译成 Playwright
```

**关键**:每次成功跑完后,把 LLM 的步骤序列**翻译成 Playwright 脚本**,后续走稳定回归。

### 模式 B · Playwright 稳定回归

```ts
test('登录 → 主操作 → 退出', async ({ page }) => {
  await page.goto('/');
  await page.click('text=登录');
  await page.fill('input[name=email]', 'test@example.com');
  await page.fill('input[name=password]', 'xxx');
  await page.click('button[type=submit]');
  await expect(page.locator('text=控制台')).toBeVisible();
  await expect(page).toHaveScreenshot('dashboard.png', { maxDiffPixels: 200 });
});
```

### 模式 C · Chrome MCP(用户真实会话)

需要用户真实登录态时(已扫码、已登录、有 Cookie),用 `mcp__Claude_in_Chrome__*` 工具。LLM 可以点击、填表、读 console。

---

## 7 层验证清单(对接 design-dev-flow ⑥)

1. 加载验证:200 OK,DOM 渲染
2. 控制台:无 error / 关键 warning(白名单除外)
3. 网络:无非预期 4xx/5xx
4. 视觉回归:截图 vs 设计稿(pixelmatch)
5. 关键路径 E2E:登录 → 主操作 → 退出
6. 微交互:hover / loading / 空错成态
7. A11y:tab 键、焦点、对比度

最少必做 1-5;电商/政府/医疗类项目必须 1-7。

---

## 安装

```bash
# browser-use(Python LLM 驱动)
pip install browser-use

# Playwright
npm i -D @playwright/test && npx playwright install

# 用本仓库 CLI 检测
bin/code-skills doctor
```

也可通过 `bin/code-skills browser <task>` 调用 browser-use(passthrough,见 README)。

---

## 反模式

- ❌ **CI 里用 LLM 跑 E2E**:不稳定 + 烧 token。LLM 用来探索,Playwright 用来回归
- ❌ **每个 case 都点界面**:能调 API 的不要走 UI(测 API 用 fetch / curl)
- ❌ **不验证视觉**:CSS 改坏了类型检查发现不了
- ❌ **不验证 console**:react warning 累积到生产爆炸
- ❌ **跳过验证**:跑了构建 + 单测就上线 = 押宝
- ❌ **录制脚本无人维护**:Playwright codegen 录的脚本要 review,不能直接 commit

---

## 与其他 skill 的关系

- `design-dev-flow` ⑥ 验证幕直接调本 skill
- `e2e-testing` skill(已装)处理纯 Playwright 工程问题,本 skill 提供"先 LLM 探索再 Playwright 固化"的混合策略
- `code-skills browser <task>` CLI 命令是 browser-use 的 passthrough

---

## References

- [验证清单与报告模板](references/verification-checklist.md)
- [LLM 探索 → Playwright 翻译模板](references/llm-to-playwright.md)
