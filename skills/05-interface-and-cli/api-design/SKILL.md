---
name: api-design
description: 设计或修订 REST, GraphQL, gRPC, or WebSocket 接口契约，包括资源建模、分页、错误响应、版本控制和 OpenAPI。Use when defining API shapes or specs, not routine endpoint implementation.
---

# API 设计

## REST API

### URL 规范
```
GET    /api/v1/users          # 列表
POST   /api/v1/users          # 创建
GET    /api/v1/users/:id      # 详情
PATCH  /api/v1/users/:id      # 部分更新
DELETE /api/v1/users/:id      # 删除
GET    /api/v1/users/:id/orders  # 子资源
POST   /api/v1/users/:id/actions/activate  # 操作
```

### 分页

**Cursor-Based（推荐，适合大数据集）：**
```json
{ "data": [...], "meta": { "hasMore": true, "cursor": "abc123" } }
```

**Offset-Based（简单场景）：**
```json
{ "data": [...], "meta": { "page": 1, "pageSize": 20, "total": 150 } }
```

### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "输入验证失败",
    "details": [{ "field": "email", "message": "邮箱格式不正确" }]
  }
}
```

### 状态码

| 码 | 含义 | 场景 |
|----|------|------|
| 200 | OK | GET/PATCH 成功 |
| 201 | Created | POST 创建成功 |
| 204 | No Content | DELETE 成功 |
| 400 | Bad Request | 参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突 |
| 422 | Unprocessable | 业务规则违反 |
| 429 | Too Many | 限流 |
| 500 | Server Error | 内部错误 |

## GraphQL

```graphql
# Schema 定义
type Query {
  """获取用户列表"""
  users(first: Int, after: String): UserConnection!
  """获取单个用户"""
  user(id: ID!): User
}

type Mutation {
  """创建用户"""
  createUser(input: CreateUserInput!): User!
}

type User {
  id: ID!
  """用户昵称"""
  name: String!
  email: String!
  orders: [Order!]!
}
```

### GraphQL 最佳实践
- 使用 Connection 模式分页（Relay 规范）
- Mutation 输入用 Input 类型
- 错误用 Union 类型而非异常
- 避免 N+1: 使用 DataLoader
- 限制查询深度和复杂度

## gRPC

```protobuf
// proto 定义
syntax = "proto3";

// 用户服务
service UserService {
  // 获取用户详情
  rpc GetUser(GetUserRequest) returns (User);
  // 用户列表（服务端流）
  rpc ListUsers(ListUsersRequest) returns (stream User);
}

message User {
  string id = 1;
  string name = 2;    // 用户昵称
  string email = 3;   // 邮箱地址
}
```

### gRPC 适用场景
- 微服务间通信（低延迟、高吞吐）
- 实时数据流（双向流）
- 移动端到服务端（节省带宽）

## WebSocket

```typescript
/** WebSocket 消息协议 */
interface WSMessage {
  type: 'subscribe' | 'unsubscribe' | 'message' | 'error';
  channel: string;
  data?: unknown;
  timestamp: number;
}
```

### WebSocket 适用场景
- 实时通知/聊天
- 协同编辑
- 实时数据推送（股票、监控）

## API 文档

### OpenAPI/Swagger
```yaml
openapi: 3.0.3
info:
  title: 用户服务 API
  version: 1.0.0
paths:
  /users:
    get:
      summary: 获取用户列表
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
      responses:
        '200':
          description: 成功
```

### 文档工具

| 类型 | 工具 |
|------|------|
| REST | Swagger UI, Redoc |
| GraphQL | GraphQL Playground, Apollo Studio |
| gRPC | grpcurl, BloomRPC |

## 版本策略

- URL 路径: `/api/v1/`, `/api/v2/`
- 向后兼容: 新增字段不破坏旧客户端
- 废弃流程: 标记 → 通知 → 过渡期（3个月） → 移除
