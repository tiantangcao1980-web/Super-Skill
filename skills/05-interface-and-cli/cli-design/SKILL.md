---
name: cli-design
description: |
  CLI 设计规范 skill:对齐 opencli + CLI-Anything,把"做命令行工具"这件事工业化。
  覆盖命令树结构、flag 命名、输入输出、退出码、错误码、JSON schema 暴露,以及"任意能力 CLI 化"的 5 步法。
  触发词:「设计 CLI」「命令行接口」「opencli」「CLI-Anything」「命令树」「子命令」「CLI 规范」「scaffold CLI」「CLI 化」。
  适用阶段:开发者工具立项、给 LLM/agent 暴露能力、把已有逻辑封装为可调用 CLI。
---

# CLI Design · 命令行规范

> 一个 CLI 的命运,在它写第一行 main 之前就决定了 —— 命令树设计错,后面再多加 flag 也救不回来。

## 灵感来源

- [opencli](https://github.com/jackwener/opencli) —— Open CLI Specification(机器可发现的 CLI)
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) —— 把任意能力封装为 CLI 的方法论

本 skill 把两者的精华提炼成可执行规范,**不复制原文**。

---

## 核心规范(7 条铁律)

### 1. 命令树:`<verb> <noun>` 或 `<noun> <verb>`,不超过 3 层
```
mycli create function --name foo    # ✅ verb-first(git/kubectl 风格)
mycli function create --name foo    # ✅ noun-first(aws/gcloud 风格)
mycli foo bar baz qux create        # ❌ 4 层用户记不住
```

### 2. 通用 flag(每个 CLI 都该有)
- `--help / -h` 帮助
- `--version / -V` 版本
- `--json` 机器可读输出
- `--quiet / -q` / `--verbose / -v` 噪声控制
- `--no-color` 禁用 ANSI(CI 友好)
- `--dry-run` 演练
- `--yes / -y` 跳过确认

### 3. 退出码标准化
| Code | Meaning |
|------|---------|
| 0    | success |
| 1    | runtime error |
| 2    | usage error(参数错) |
| 3    | missing dependency(外部工具不在 PATH) |
| 130  | interrupted(Ctrl-C) |

### 4. 错误响应固定 schema(JSON 模式)
```json
{
  "ok": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with id=123 not found",
    "hint": "Try /users/list",
    "request_id": "req_abc"
  }
}
```
错误码全大写下划线,`hint` 必填,`message` 说人话。

### 5. **暴露 schema**(opencli 的核心要求)
每个 CLI 必须支持 `<cli> describe --json`,输出整个命令树。让 agent 能一次发现所有能力。本仓库的 `bin/code-skills describe` 是参考实现。

### 6. 优先级:flag > env > config > default
```
--port=8080         # 最高
PORT=8080 ./mycli   # 次之
~/.mycli.yaml port  # 再次
默认 3000           # 最低
```

### 7. 输入支持 stdin
```
cat input.json | mycli create user --stdin
```
让 CLI 在 pipeline 里也能用。

---

## CLI-Anything 5 步法 · 把任意能力 CLI 化

### Step 1:抽离核心动作(一个动词)
"OCR 这张图" → 动词 `ocr`

### Step 2:确定操作对象(一个名词)
"OCR 一张图片" → 名词 `image`

### Step 3:最小输入(只必填)
```
ocr <image-path>
```
其他都用 flag 表示,有默认值。

### Step 4:双输出(人 + 机)
```
ocr file.jpg              # 默认彩色文本
ocr file.jpg --json       # {"text": "...", "confidence": 0.92, "lang": "zh"}
```

### Step 5:可分发包装(npm / pip / brew / shell installer)
```
brew install yourorg/tap/ocr
# or
curl -sf https://yourorg.com/install.sh | sh
```

---

## 工作流(本 skill 被触发后)

### 触发场景 A · 从零设计新 CLI
1. 跑 5 步法,写出命令树草图
2. 列必备 flag 表
3. 列错误码表
4. 写一份 INTERFACE.md(命令树 + schema)
5. (可选)用 `bin/code-skills cli-init <name>` scaffold 骨架

### 触发场景 B · 审查/对齐已有 CLI
按 7 条铁律逐条 check,输出红黄绿报告:
```
✅ 命令树深度: 2 层
🟡 flag 命名: --output 在不同子命令含义不同(歧义)
❌ 退出码: 失败一律返回 1,无法区分用法错和运行时错
✅ JSON schema: describe 已实现
❌ stdin: 不支持(管道场景挂)
```

### 触发场景 C · 把已有库 CLI 化
1. 跑 5 步法
2. 选语言:Python(argparse/typer)/ Node(commander/yargs)/ Rust(clap)/ Go(cobra)
3. scaffold(`bin/code-skills cli-init`)
4. 实现 + 加 `describe` 命令
5. 加 `--json` 输出
6. 加退出码 + 错误码
7. 写 README + man page(可选)

---

## 反模式

- ❌ **一个命令 10+ 个 flag**:拆子命令或用 config 文件
- ❌ **`--force` 默认开启**:危险操作必须显式
- ❌ **错误信息只说"failed"**:必须含原因 + 建议
- ❌ **退出码全是 0 或 1**:用细分码区分错误类型
- ❌ **不给 `--json`**:agent 接不上你的 CLI
- ❌ **命令名故弄玄虚**:`mycli incarcerate` < `mycli stop`

---

## 与其他 skill 的关系

- `design-dev-flow` 的 ③ 接口设计幕,涉及 CLI 时调本 skill
- `programmatic-video` / `browser-automation` 等工具型 skill 在自身 CLI 设计时也参考本 skill
- 输出 INTERFACE.md 后,可被 `code-simplifier` 检查冗余命令

---

## References

- [opencli 规范精华](references/opencli-spec.md)
- [CLI-Anything 5 步法详解](references/cli-anything-5-steps.md)
