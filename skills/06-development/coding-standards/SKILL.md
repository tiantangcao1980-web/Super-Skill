---
name: coding-standards
description: 定义或应用多语言编码规范，包括命名、文件组织、类型安全和错误处理。Use when establishing standards, enforcing consistency, or doing broad cleanup/refactors; not for ordinary implementation tasks.
---

# 编码标准（多语言）

## 通用原则

- 不可变性优先: `const` / `final` / `readonly` / `let`（非 `var`）
- 类型安全: 避免 `any`、`interface{}`、`object`，使用严格类型
- 单一职责: 每个文件一个主要导出，函数不超过 40 行
- 文件长度不超过 300 行，超出则拆分模块
- 所有新文件使用 UTF-8 编码

## 各语言命名规范

### Python
| 类型 | 规范 | 示例 |
|------|------|------|
| 文件/模块 | snake_case | `user_service.py` |
| 类 | PascalCase | `UserService` |
| 函数/变量 | snake_case | `get_user_by_id` |
| 常量 | UPPER_SNAKE | `MAX_RETRY` |
| 私有成员 | 前缀 `_` | `_internal_cache` |

工具链: `ruff`(lint+format) / `mypy`(类型) / `pytest`(测试)

### TypeScript / JavaScript
| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | kebab-case | `user-service.ts` |
| 类/接口 | PascalCase | `UserService` |
| 函数/变量 | camelCase | `getUserById` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| 布尔值 | is/has/can 前缀 | `isActive` |

工具链: `eslint`(lint) / `prettier`(format) / `vitest`/`jest`(测试)

### Go
| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | snake_case | `user_service.go` |
| 导出类型/函数 | PascalCase | `UserService` |
| 非导出 | camelCase | `getUserByID` |
| 包名 | 全小写单词 | `userservice` |
| 接口 | 动词+er | `Reader`, `Writer` |

工具链: `gofmt`(format) / `golangci-lint`(lint) / `go test`(测试)

### Java / Kotlin
| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | PascalCase | `UserService.java` |
| 类/接口 | PascalCase | `UserService` |
| 方法/变量 | camelCase | `getUserById` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| 包名 | 全小写点分 | `com.example.user` |

### Rust
| 类型 | 规范 | 示例 |
|------|------|------|
| 文件/模块 | snake_case | `user_service.rs` |
| 结构体/枚举 | PascalCase | `UserService` |
| 函数/变量 | snake_case | `get_user_by_id` |
| 常量 | UPPER_SNAKE | `MAX_RETRY` |
| Trait | PascalCase | `Serialize` |

### C# / .NET
| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | PascalCase | `UserService.cs` |
| 类/接口 | PascalCase (接口加 I) | `IUserService` |
| 方法/属性 | PascalCase | `GetUserById` |
| 参数/局部变量 | camelCase | `userId` |
| 私有字段 | `_camelCase` | `_userRepo` |

## 错误处理

```python
# Python: 自定义异常 + 上下文
class UserNotFoundError(Exception):
    def __init__(self, user_id: str):
        super().__init__(f"用户不存在: {user_id}")
        self.user_id = user_id
```

```typescript
// TypeScript: 自定义错误类
class AppError extends Error {
  constructor(public code: string, message: string, public statusCode = 500) {
    super(message);
  }
}
```

```go
// Go: 错误包装
fmt.Errorf("获取用户失败: %w", err)
```

## 项目结构

```
project/
├── src/              # 源代码
│   ├── models/       # 数据模型
│   ├── services/     # 业务逻辑
│   ├── routes/       # API 路由（后端）
│   ├── components/   # UI 组件（前端）
│   └── utils/        # 工具函数
├── tests/            # 测试
├── docs/             # 文档
├── scripts/          # 脚本
└── config/           # 配置
```

## Git 工作流

- 提交格式: `type(scope): 中文描述`
- type: feat, fix, refactor, docs, test, chore, perf, ci
- 分支: `feature/xxx`, `bugfix/xxx`, `hotfix/xxx`
- PR 不超过 400 行变更

## 反模式清单

- 过度使用继承（优先组合）
- God Object / God Function
- 硬编码配置值（用环境变量或配置文件）
- 吞掉异常（空 catch/except）
- 文件编码不一致
- 缺少模块级中文注释
