---
name: design-dev-flow
description: |
  项目级"设计 → 开发 → 验证 → 交付"全流程编排器。从需求澄清开始,串联设计规范(taste + 文案 + UI 库)、CLI/接口设计、前后端 Ralph Loop 实现、浏览器自动验证、代码简化、Demo 录制。
  本 skill 只做编排,具体环节调用:spec-workflow / ui-design / designdna / ralph-loop / code-simplifier 以及 frontend-patterns / backend-patterns 等已有 skill。
  触发词:「全流程开发」「设计到交付」「从 0 做项目」「项目编排」「设计 + 开发 + 验证」「端到端开发」「端到端交付」。
---

# Design-Dev-Flow · 设计开发全流程编排器

> 一个项目的命运不在于哪一行代码,在于"哪一段没做"。这个 skill 的工作是**确保每一段都做了**。

> **本 skill 是声明式蓝图**(说"应该有这些幕、这些产出")。
> **要让它真的自动跑起来 → 触发 [`auto-flow`](../auto-flow/SKILL.md) skill** —— 那是驱动器,带需求 gate / 6 个干预点 / Ralph+Simplifier 协作规则。
> 简而言之:`design-dev-flow` = 蓝图,`auto-flow` = 引擎。

## 七幕流程

```
①需求 → ②设计 → ③接口 → ④前端loop → ⑤后端loop → ⑥验证 → ⑦交付
                                ↓                ↓
                            ralph-loop      ralph-loop
                                ↓                ↓
                          code-simplifier  code-simplifier
```

每一幕进入下一幕前必须有**显式产出**。没产出不准前进。

---

## ① 需求澄清

**调用**:`spec-workflow` skill。

**最少产出**:
- 一句话价值主张(VP)
- 用户故事 3-5 条核心
- 非功能需求(性能 / 合规 / 平台)
- **不做清单**(明确说"这次不做什么")

**进度门**:用户复述能复述出"这个项目要解决谁的什么问题",才算过关。

---

## ② 设计规范

**调用**:`ui-design` + `designdna` + 本 skill 的 [references/design-taste.md](references/design-taste.md)
(该文件融合 taste-skill / huashu-design / awesome-design-md 的精华)。

**最少产出**:

```
【Design Spec】
Aesthetic Direction: <具体方向,例如 "瑞士主义 + 杂志感",不是"现代简约">
配色: 主色 #xxx / 强调 #xxx / 背景 #xxx / 文本 #xxx (说明各自用途)
字体: 标题 <具体字体名> / 正文 <具体字体名>
布局策略: <例如 "非对称网格,左 1/3 大留白">
文案语气: <例如 "克制理性 + 偶尔自嘲",来自 huashu-design 模式>
关键文案 5 句:
  - 首页主标题
  - 主 CTA
  - 空态文案
  - 错态文案
  - 成功态文案
设计参考(如有): <URL 或 designs/*.png>
```

**进度门**:能在不写代码的情况下,把上面这段读给陌生人听,陌生人能脑补出页面长什么样。

---

## ③ CLI / 接口设计

**调用**:本 skill 的 [references/cli-patterns.md](references/cli-patterns.md)
(融合 opencli + CLI-Anything 的命令树规范)。

非 CLI 项目跳到 API 设计,调用 `api-design` skill。

**最少产出**:

```
【Interface Spec】
形态: CLI / REST / GraphQL / RPC / WebSocket
命令树或路由表: <一个 ASCII 树>
输入 schema: <每个命令/路由的 input>
输出 schema: <每个命令/路由的 output>
错误码表: <code → 含义 → 用户该怎么做>
幂等约定: <哪些是幂等的,哪些不是>
```

**进度门**:任何一个接口都能用一句 curl / 一行命令调用并 mock 出正确响应。

---

## ④ 前端实现(Ralph Loop)

**调用**:`ralph-loop` skill。

**契约模板**:
```
目标: 完成 <页面列表> 的前端,可点通端到端
退出条件:
  - vite build 成功
  - 单测全过(vitest run)
  - 浏览器手动跑通三个核心路径(列出来)
最大迭代数: 5
卡住判定: 连续 2 轮 vitest 失败用例集合不变
验证手段: pnpm build && pnpm test
```

**每轮迭代结束**:
- 截图当前页面给用户看(用 preview tool)
- 比对设计稿,记下偏差(下一轮修)

**幕末**:调一次 `code-simplifier` 做单幕清扫(P0 级别即可)。

---

## ⑤ 后端实现(Ralph Loop)

**调用**:`ralph-loop` skill。

**重要次序**:**前端依赖后端 → 后端先行,但本 skill 把第 ④ 幕放前面是因为通常前端 mock 接口 → 后端跟上**。

如果是 CloudBase 项目:
- 优先 SDK 直连数据库,**不要**先写云函数中间层(详见 frontend-patterns / backend-patterns)
- 必须的中间层:涉及私钥、第三方 API、复杂业务逻辑

**契约模板**:
```
目标: 实现 <接口清单> 全部端点
退出条件:
  - 所有接口可通过 curl 跑通
  - 集成测试全过
  - 部署后健康检查通过
最大迭代数: 6
验证手段: pnpm test:int && curl 健康检查
```

**幕末**:调一次 `code-simplifier`。

---

## ⑥ 浏览器自动验证

**调用**:本 skill 的 [references/browser-verify.md](references/browser-verify.md)
(融合 browser-use + agent-browser 的端到端验证模式)。

**最少验证集**:
- 关键路径 E2E:登录 → 主操作 → 退出
- 视觉回归:每个页面截图 vs 设计稿(用 pixelmatch)
- 控制台无 error/warning(允许预期 warning,需写白名单)
- 网络请求无 4xx/5xx(允许预期错误,需写白名单)
- 关键交互的微动效不卡顿(肉眼即可)

**用什么工具**:
- Claude 内置浏览器预览(轻量验证)
- Playwright(完整 E2E)
- claude-in-chrome MCP(需要真实浏览器交互时)

**进度门**:验证报告里所有 ✅,或异常项都写明"为什么可接受"。

---

## ⑦ 交付三件套

### 7.1 整项目代码简化
**调用**:`code-simplifier`,跑 P0 + P1 完整清单,**全仓库范围**。

### 7.2 README + 部署
- README 包含:项目说明、架构图、CloudBase 资源清单、部署地址、本地启动步骤
- 部署:静态 hosting / Cloud Run / 云函数,按平台 skill 做
- 部署完输出**带随机 query string** 的访问链接(刷 CDN 缓存)

### 7.3 Demo 视频(可选但强推)
**调用**:本 skill 的 [references/demo-recording.md](references/demo-recording.md)
(借鉴 remotion 的程序化视频思路)。

- 30-60 秒
- 三幕:问题 → 解法 → 效果
- 输出 mp4 / gif,放进 README

---

## 进度门检查表

每幕做完打勾,**没勾完不准过**:

```
□ ① 需求文档已写(VP / 用户故事 / 非功能 / 不做清单)
□ ② 设计规范已输出(Aesthetic / 配色 / 字体 / 布局 / 文案)
□ ③ 接口契约已定(命令树 / schema / 错误码 / 幂等)
□ ④ 前端 Ralph Loop 退出码 = DONE,截图已给用户看
□ ⑤ 后端 Ralph Loop 退出码 = DONE,接口可调通
□ ⑥ 浏览器验证全绿(或异常项有解释)
□ ⑦ code-simplifier 已跑 + README 完成 + Demo(可选)
```

---

## 反模式

- ❌ **跳幕**:没设计就开写,"边写边设计"几乎一定返工
- ❌ **一幕没完就开下一幕**:上一幕的债会复利累加
- ❌ **本 skill 重复别的 skill 内容**:不知道 UI 怎么做就读 `ui-design`,不要在这里复述
- ❌ **不让 ralph-loop 出 DONE 就过幕**:循环没收敛 = 这一幕没做完
- ❌ **跳过浏览器验证**:类型检查 + 单测都过不等于功能 OK
- ❌ **简化放在每幕都做**:每幕只做 P0 微清扫,完整简化留到 ⑦

---

## 调用其他 skill 的速查表

| 阶段 | 主调 skill | 可选辅助 |
|------|-----------|---------|
| ① | spec-workflow | hierarchical-memory(查历史项目经验) |
| ② | ui-design + designdna | nutui-vue / shadcn-ui / element-plus 等(看 UI 库) |
| ③ | api-design / cli-toolkit | swagger / openapi 工具 |
| ④ | ralph-loop + frontend-patterns | 平台 skill(web-development / miniprogram-development) |
| ⑤ | ralph-loop + backend-patterns | cloud-functions / cloudrun-development |
| ⑥ | e2e-testing | claude-in-chrome MCP / Claude Preview MCP |
| ⑦ | code-simplifier + verification-loop + security-review | deployment-patterns |

---

## References

- [设计品味整合(taste + huashu + awesome-design-md)](references/design-taste.md)
- [浏览器验证模式(browser-use + agent-browser)](references/browser-verify.md)
- [CLI / 接口设计模式(opencli + CLI-Anything)](references/cli-patterns.md)
- [Demo 录制模式(remotion)](references/demo-recording.md)
