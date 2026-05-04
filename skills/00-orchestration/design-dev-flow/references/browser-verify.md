# 浏览器验证模式

> 借鉴:
> - [browser-use/browser-use](https://github.com/browser-use/browser-use) — agent 驱动的浏览器自动化
> - [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) — 在 agent 上下文里跑端到端验证

本文件**不是 Playwright 教程**,而是回答:
- 什么时候用什么工具?
- 一份合格的验证清单长什么样?
- 验证报告怎么呈现给用户?

---

## 工具选型

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
| 看一眼当前页面什么样 | `mcp__Claude_Preview__preview_screenshot` | 最轻,无需启动浏览器 |
| 跑端到端测试,可重复 | Playwright + 集成到 CI | 工业标准,有完整 trace |
| 需要操作真实浏览器(登录/插件) | claude-in-chrome MCP | 用户自己的会话状态 |
| 需要 agent 自主探索页面 | browser-use 模式 | LLM + DOM 的高层操作 |
| 需要在 CI 里跑稳定的 E2E | Playwright | mature ecosystem |

**默认推荐**:
- 开发期 → **Claude Preview MCP**(快速看效果)
- PR 提交前 → **Playwright**(进入 CI)
- 需要操作真实状态 → **claude-in-chrome MCP**(用户授权)

---

## 标准验证清单(7 个层级)

### 层级 1 · 加载验证(秒级)
- [ ] 页面 200,无 5xx
- [ ] HTML 渲染成功(不是白屏)
- [ ] 关键 DOM 节点存在(标题、主 CTA、导航)

### 层级 2 · 控制台验证
- [ ] 无 `console.error`(白名单除外)
- [ ] 无未捕获的 Promise rejection
- [ ] 无明显的 React/Vue warning(key 重复、prop 类型等)

### 层级 3 · 网络验证
- [ ] 所有请求 200/300,无 4xx/5xx(预期错误除外)
- [ ] 关键 API 调用响应时间 < 1s
- [ ] 无重复请求(同一接口 3 次以上调用 = 信号)

### 层级 4 · 视觉回归
- [ ] 截图 vs 设计稿(用 pixelmatch / Resemble)
- [ ] 关键页面在 desktop / tablet / mobile 三个断点都正常
- [ ] 暗黑模式(若有)切换无错位
- [ ] 字体加载完成(无 FOUT/FOIT 闪烁过大)

### 层级 5 · 关键路径 E2E
按用户故事跑一遍,例如:
- [ ] 注册 → 登录 → 进入主功能 → 完成核心操作 → 退出
- [ ] 异常流:错密码、断网、超时

### 层级 6 · 微交互
- [ ] 按钮 hover / active / disabled 三态都有反馈
- [ ] 表单校验提示及时(不只是提交后才提示)
- [ ] 加载态有 loading 指示
- [ ] 空态、错态、成功态都到位

### 层级 7 · 可访问性(A11y)
- [ ] tab 键能走通所有交互
- [ ] 焦点可见
- [ ] 主要图片有 alt
- [ ] WCAG 对比度达标

**最少必做层级**:1-5。层级 6-7 是 nice-to-have,但电商/政府/医疗类项目必须做完 7 个。

---

## 端到端脚本结构(Playwright 示例)

```ts
import { test, expect } from '@playwright/test';

test.describe('核心路径', () => {
  test('登录 → 主操作 → 退出', async ({ page }) => {
    // 加载验证
    await page.goto('/');
    await expect(page).toHaveTitle(/MyApp/);

    // 登录
    await page.click('text=登录');
    await page.fill('input[name=email]', 'test@example.com');
    await page.fill('input[name=password]', 'xxx');
    await page.click('button[type=submit]');

    // 控制台无 error
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    // 主操作
    await expect(page.locator('text=控制台')).toBeVisible();
    await page.click('text=新建项目');
    await page.fill('input[name=name]', '测试项目');
    await page.click('text=保存');
    await expect(page.locator('text=测试项目')).toBeVisible();

    // 视觉回归
    await expect(page).toHaveScreenshot('dashboard.png', {
      maxDiffPixels: 200
    });

    // 退出
    await page.click('text=退出');
    await expect(page.locator('text=登录')).toBeVisible();

    // 控制台 assert
    expect(errors).toHaveLength(0);
  });
});
```

---

## browser-use 模式(LLM 驱动验证)

不写死脚本,而是给 LLM 一个目标:"完成下单流程,给我截图证明每步成功"。

适用:
- 探索性测试(用户路径未知)
- 第三方网站验证(无法控制 DOM)
- 演示性截图(给老板看的)

不适用:
- CI 里的稳定回归(LLM 不稳定)
- 高频测试(token 成本)

**实战建议**:
- 用 browser-use 模式**首次跑通**关键路径,记录 LLM 操作步骤
- 把成功的步骤序列**翻译成 Playwright 脚本**,后续用 Playwright 跑

---

## 验证报告模板

每次验证完输出给用户:

```
【浏览器验证报告】
环境: <URL / 本地 / 预发 / 生产>
浏览器: Chrome 130 / Firefox 132 / WebKit
断点: 1440 / 768 / 375

层级 1 加载: ✅
层级 2 控制台: ⚠️ 1 个 warning(详情见下)
层级 3 网络: ✅
层级 4 视觉: ❌ /home 截图差异 8000 像素(超过阈值)
层级 5 E2E: ✅ 3/3 关键路径全通
层级 6 微交互: ⚠️ 退出按钮 hover 无变化
层级 7 A11y: 未做(本次跳过)

详情:
- 控制台 warning: "React key prop missing in <List>"(src/components/List.tsx:42)
- 视觉差异: /home 顶部主图字体大小不一致(设计稿 64px / 实际 56px)
- 退出按钮 hover: src/components/Header.tsx 缺少 hover 样式

建议:
- [P0] 修 React key warning
- [P0] 调整 /home 主图字号
- [P1] 补 hover 样式
- [P2] 下次加 A11y 检查
```

---

## 与其他工具的协作

| 工具 | 与本验证的关系 |
|------|---------------|
| Claude Preview MCP | 开发期快速截图,层级 1-4 |
| Playwright | CI 里的稳定回归,所有层级 |
| claude-in-chrome MCP | 需要用户登录态时的真实操作 |
| pixelmatch / Resemble | 视觉回归像素对比 |
| axe-core / Lighthouse | 自动 A11y / 性能扫描 |

---

## 何时跳过浏览器验证(诚实清单)

可以跳过的场景:
- 纯后端任务,无 UI 改动
- 文档/配置修改
- 内部 CLI 工具(无 web UI)

**不能跳过**的场景:
- 任何 UI 改动 → 至少做层级 1-4
- 上线前 → 至少做层级 1-5
- 涉及支付/账号/敏感操作 → 全 7 层 + 多浏览器
