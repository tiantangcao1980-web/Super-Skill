# browser-use

- **URL**: https://github.com/browser-use/browser-use
- **License**: 见原仓库
- **类型**: Python LLM 驱动浏览器自动化库 + CLI

## 这是什么

让 LLM "看见 + 操作"浏览器:给一个自然语言任务,LLM 自己规划点击/输入/滚动,完成端到端流程。核心心法是**用 DOM accessibility tree 喂给 LLM**(而不是截图),token 成本低、动作精准。

## 在 code-skills 中的对应

- **对应 skill**:`browser-automation`(三档选型表的"探索性测试"档)
- **CLI 集成**:`bin/code-skills browser run "<task>"` —— passthrough 到 browser-use,未装时退出码 3 + 安装提示
- **协作模式**:LLM 探索 → 翻译为 Playwright 脚本 → 进 CI 稳定回归

## 何时用

- 路径未知,先让 LLM 探索一遍
- 第三方网站(无法控制 DOM)
- 演示性截图(给老板看的)
- 一次性数据采集

## 何时**不**用

- CI 里跑稳定回归(不稳定 + 烧 token)
- 高频自动化(Playwright 更便宜)
- 严格幂等的批处理

## 怎么用

```bash
pip install browser-use
bin/code-skills browser doctor                       # 检查依赖
bin/code-skills browser run "find obra/superpowers and star it"
```

## 不集成的部分

- 把 browser-use 打包进本仓库依赖(保持零依赖原则)
- browser-use 的高级配置(LLM 选型 / 浏览器 profile / proxy)→ 直接调 Python API
