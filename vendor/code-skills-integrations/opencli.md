# opencli

- **URL**: https://github.com/jackwener/opencli
- **License**: 见原仓库
- **类型**: CLI 设计规范 / Open CLI Specification

## 这是什么

定义"机器可发现的 CLI"标准 —— 让 CLI 像 OpenAPI 之于 REST 一样,有可被 agent 自动消费的命令树 schema、统一退出码、统一错误响应格式。核心要求:每个 CLI 必须支持 `<cli> describe --json` 输出整树。

## 在 code-skills 中的对应

- **对应 skill**:`cli-design`(7 条铁律的前 4 条直接来自 opencli)
- **本 CLI 自身遵守**:
  - `bin/code-skills describe --json` 输出 opencli schema
  - 退出码:0 / 1 / 2 / 3 / 130
  - 错误响应固定字段:`code / message / hint / request_id`
  - 通用 flag:`--help --json --quiet --verbose --no-color --dry-run --yes`

## 何时用

- 立项一个新 CLI,先按 opencli 设计,再写代码
- 审查已有 CLI:跑 7 条铁律 check,补 `describe` 命令
- 给 LLM/agent 暴露能力:必须有 schema

## 怎么用

```bash
# 在 code-skills 里直接 scaffold 一个对齐的 CLI:
bin/code-skills cli-init my-tool

# 或参考本 CLI 自身实现:
bin/code-skills describe --json
```

## 不集成的部分

- opencli 完整规范的所有细节(本仓库只提取最高频的 ~80%)
- 多语言 SDK 适配(只提供 Python scaffold,Node/Go 后续可加)
