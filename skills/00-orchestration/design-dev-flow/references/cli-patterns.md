# CLI / 接口设计模式

> 借鉴:
> - [jackwener/opencli](https://github.com/jackwener/opencli) — 开放 CLI 设计原则
> - [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) — 把任意能力封装为 CLI

本文件回答:
- CLI 命令树怎么设计?
- API 路由表怎么定?
- 输入/输出/错误怎么标准化?

---

## 一、CLI 设计原则(opencli 借鉴)

### 1. 命令树结构

```
<program> <subcommand> [<sub-subcommand>] [<flags>] [<args>]
```

- **第一层**:动词(create / update / delete / list / show / run / deploy)
- **第二层**:对象(user / function / db / hosting)
- **第三层**:可选的限定(by-id / latest / staged)

**例**:
```
mycli create function --name foo --runtime node18
mycli list user --filter active
mycli deploy hosting --env prod --dry-run
```

### 2. 命令树深度
- 1 层:玩具项目
- 2 层:80% 的项目应该停在这里
- 3 层:复杂项目最大深度
- 4 层及以上:**不要**(用户记不住)

### 3. 命令命名规则
- 动词用**最常见的英语单词**:list 而非 enumerate,delete 而非 destroy
- 对象用**单数**:`create user` 而非 `create users`
- 别名要谨慎:`ls` ≠ `list`(用户期望的输出格式不同)

---

## 二、Flag 设计

### 必备 flag(每个 CLI 都该有)
- `--help, -h`:帮助
- `--version, -v`:版本
- `--verbose`:详细日志
- `--quiet, -q`:静默
- `--json`:机器可读输出
- `--dry-run`:不实际执行,只显示会做什么
- `--yes, -y`:跳过确认(用于脚本)
- `--config <path>`:指定配置文件
- `--no-color`:禁用颜色

### 反模式
- ❌ 一个命令 10+ 个 flag(拆子命令或用配置文件)
- ❌ 同一个简称对应多个长名(例如 `-f` 既是 `--force` 又是 `--file`)
- ❌ 默认值改变行为(用户不写 `--strict` 时也是严格模式 = 反直觉)

---

## 三、输入 / 输出 / 错误

### 输入约定
- **优先级**:flags > 环境变量 > 配置文件 > 默认值
- **从 stdin 读**:支持 `cat input.json | mycli create user --stdin`
- **位置参数**:必填项放位置,可选项放 flag

### 输出约定
- **人类可读**:默认彩色、有 emoji、有进度
- **机器可读**(`--json`):标准 JSON,无颜色码,无 emoji
- **退出码**:
  - 0 = 成功
  - 1 = 通用错误
  - 2 = 用法错误(参数错)
  - 3-127 = 业务错误(自定义,文档化)
  - 128+ 信号码 = 中断

### 错误约定
错误信息必须包含:
1. **错了什么**(简短)
2. **为什么错**(原因)
3. **怎么办**(具体建议)

例:
```
❌ 部署失败:目标环境不存在
   原因: env "prod" 不在 ~/.mycli/config.json 中
   建议:
     - 运行 mycli list env 查看可用环境
     - 或运行 mycli config add-env prod --url https://...
```

---

## 四、CLI-Anything 模式:把任意能力 CLI 化

任何"输入 → 处理 → 输出"流程都能 CLI 化。但要先想清楚:

### 适合 CLI 化的能力
- 可批量处理(脚本友好)
- 不需要图形交互(纯逻辑)
- 在终端里使用更高效(开发者工具)

### 不适合 CLI 化
- 高频图形操作(画图、布局)
- 需要登录态/Cookie(用浏览器更顺)
- 一次性任务(写脚本不如直接跑)

### CLI 化的 5 步法
1. **找到核心动作**(动词)
2. **找到操作对象**(名词)
3. **定义最小输入**(只必填项)
4. **定义可读输出 + JSON 输出**
5. **包装为可安装包**(npm / pip / brew)

### 例:把 "OCR 一张图片" 做成 CLI

```
ocr <image-path> [--lang en|zh|auto] [--json]
```

- 必填:image-path
- 可选:lang(默认 auto)
- 输出:默认打印识别文本;`--json` 输出 `{text, confidence, lang}`
- 错误:
  - 文件不存在 → 退出码 2 + 提示
  - lang 不支持 → 退出码 2 + 列出支持列表
  - OCR 失败 → 退出码 3 + 原因

---

## 五、API 路由设计(REST)

### 路由命名
- 资源用**复数**:`/users` 而非 `/user`
- 嵌套不超过 2 层:`/users/:id/posts` ✅;`/users/:id/posts/:pid/comments` ❌(改用 query)
- 动作用 HTTP 方法:GET / POST / PUT / PATCH / DELETE,不要 `/users/create`

### 状态码
- 200 OK:成功且有响应体
- 201 Created:创建成功(返回新资源)
- 204 No Content:成功但无响应体
- 400 Bad Request:请求格式错
- 401 Unauthorized:未认证
- 403 Forbidden:已认证但无权限
- 404 Not Found:资源不存在
- 409 Conflict:状态冲突(如重复创建)
- 422 Unprocessable Entity:格式对但语义错
- 429 Too Many Requests:限流
- 500 / 502 / 503:服务端错

### 错误响应体(标准化)
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with id=123 not found",
    "details": {
      "id": "123",
      "hint": "Try /users/list to see available ids"
    },
    "request_id": "req_xxx"
  }
}
```

每个错误必须有:
- `code`:机器可识别(全大写下划线)
- `message`:人类可读
- `request_id`:便于日志追踪

---

## 六、幂等性约定

### 必须幂等
- GET / HEAD / OPTIONS
- PUT(同样的 PUT 多次效果一致)
- DELETE(删 1 次和删 N 次结果一样)

### 不一定幂等
- POST(可能创建多个资源)

### 让 POST 幂等的方法
- 客户端传 `Idempotency-Key` header
- 服务端在窗口期(如 24h)内识别同一 key,返回首次结果

例:
```
POST /orders
Idempotency-Key: client-uuid-xxx
{ ... }
```

---

## 七、命令树/路由表的产出格式

每个项目的接口设计完,输出一份 `docs/INTERFACE.md`:

```md
# Interface Specification

## CLI 命令树
mycli
├── create
│   ├── user --name <s> --email <s>
│   └── function --name <s> --runtime <node18|node20>
├── list
│   └── user [--filter active|inactive]
├── delete
│   └── user --id <s> [--yes]
└── deploy
    ├── hosting --env <s> [--dry-run]
    └── function --name <s>

## API 路由
| Method | Path | 描述 | 幂等 | 错误码 |
|--------|------|------|------|--------|
| GET | /users | 列出用户 | ✅ | 401, 500 |
| POST | /users | 创建用户 | ⚠️ Idempotency-Key | 400, 409, 500 |
| ... | ... | ... | ... | ... |

## 错误码表
| Code | HTTP | 含义 | 用户该怎么办 |
|------|------|------|------------|
| USER_NOT_FOUND | 404 | 用户不存在 | 检查 id |
| USER_DUPLICATE | 409 | 邮箱已注册 | 用其他邮箱 |
| ... | ... | ... | ... |
```
