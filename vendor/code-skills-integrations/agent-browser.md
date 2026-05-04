# agent-browser (vercel-labs)

- **URL**: https://github.com/vercel-labs/agent-browser
- **License**: 见原仓库
- **类型**: Vercel 实验项目 / Agent 驱动浏览器

## 这是什么

Vercel Labs 出品的实验:在 serverless / edge 环境运行 agent + 真实 Chromium 实例,接受 HTTP 请求触发浏览器任务。比 browser-use 更工程化(部署、API、并发),但场景更窄(以"在云端跑"为前提)。

## 在 code-skills 中的对应

- **对应 skill**:`browser-automation`(serverless 模式)
- 与 `browser-use` 的区别:
  - browser-use → 本地跑、Python、LLM 自主
  - agent-browser → 云端跑、Node、HTTP API、可被外部触发

## 何时用

- 需要把"浏览器自动化"做成 SaaS 接口给客户调
- Vercel/Edge 环境
- 多用户并发的爬取/截图服务

## 何时**不**用

- 个人开发机一次性任务(用 browser-use 更轻)
- 严格回归测试(用 Playwright)
- 不想付云费用

## 怎么用

具体部署看上游 README。在本仓库里,本项目作为"了解一种部署形态"的参考,**不直接 passthrough**(因其有部署成本)。

## 不集成的部分

- agent-browser 的 API 适配 / SDK 包装
- 部署到 Vercel 的脚手架(那是 Vercel CLI 的事)
- 不收口为本仓库的 CLI 命令(命令空间留给真本地工具 browser-use)
