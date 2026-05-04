---
name: backend-patterns
description: 规划或重构后端服务结构，涵盖 Node.js/Python/Go/Java 的服务边界、缓存、消息队列、后台任务、微服务和数据访问模式。Use when the task is about backend architecture or structural changes, not simple CRUD edits.
---

# 后端开发模式（多语言）

> **保持最新**: 使用 context7 MCP 的 `resolve-library-id` + `query-docs` 查询 FastAPI/Django/Spring/Gin 等框架最新文档。遇到不确定的 API 用法时，优先查询最新文档而非依赖记忆。

## API 设计

### RESTful 规范
- 资源路径: `/api/v1/users`, `/api/v1/users/:id/orders`
- HTTP 方法: GET(查) POST(增) PUT/PATCH(改) DELETE(删)
- 状态码: 200/201/204/400/401/403/404/409/429/500

### 多语言路由示例

```python
# Python FastAPI
@router.get("/users/{user_id}")
async def get_user(user_id: str) -> UserResponse:
    """获取用户详情"""
```

```typescript
// TypeScript Express
router.get('/users/:userId', async (req, res) => {
  /** 获取用户详情 */
});
```

```go
// Go Gin
r.GET("/users/:userId", func(c *gin.Context) {
    // 获取用户详情
})
```

```java
// Java Spring Boot
@GetMapping("/users/{userId}")
public ResponseEntity<User> getUser(@PathVariable String userId) {
    /** 获取用户详情 */
}
```

## 统一响应格式

```json
{
  "success": true,
  "data": {},
  "meta": { "page": 1, "total": 100, "pageSize": 20 },
  "error": null
}
```

## 中间件/管道架构

```
请求 → 日志 → 认证 → 授权 → 限流 → 验证 → 处理器 → 序列化 → 响应
```

## 数据库操作

### ORM 对照

| 语言 | ORM | 特点 |
|------|-----|------|
| Python | SQLAlchemy / Tortoise | 灵活 / 异步原生 |
| TypeScript | Prisma / Drizzle | 类型安全 / 轻量 |
| Go | GORM / sqlx | 全功能 / 原始SQL |
| Java | JPA/Hibernate / MyBatis | 标准 / SQL优先 |
| Rust | Diesel / SeaORM | 编译时检查 / 异步 |

### 查询优化
- 避免 N+1: 使用 JOIN/预加载/DataLoader
- 避免 SELECT *: 只查询需要的列
- 大结果集: 分页（cursor-based 优先）
- 批量操作: BULK INSERT/UPDATE

## 缓存策略

| 模式 | 适用场景 | 实现 |
|------|----------|------|
| Cache-Aside | 读多写少 | 先查缓存 → 缺失查DB → 写缓存 |
| Write-Through | 一致性要求高 | 写DB同时写缓存 |
| TTL | 可接受短暂过期 | 设置过期时间 |
| 缓存预热 | 启动时 | 提前加载热点数据 |

## 消息队列

| 场景 | 方案 |
|------|------|
| 任务异步处理 | Celery(Python) / BullMQ(Node) |
| 事件驱动 | RabbitMQ / Kafka |
| 简单队列 | Redis List / Stream |

## 微服务要点

- 服务拆分: 按业务领域，而非技术层
- API 网关: 统一入口、认证、限流、路由
- 服务发现: Consul / etcd / Kubernetes DNS
- 断路器: 防止级联故障
- 分布式追踪: Jaeger / Zipkin / OpenTelemetry
- 配置中心: Consul / etcd / Apollo

## 错误处理模式

```python
# Python: 结构化错误
class AppError(Exception):
    def __init__(self, code: str, message: str, status: int = 500):
        super().__init__(message)
        self.code = code
        self.status = status
```

```go
// Go: 错误包装
type AppError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}
func (e *AppError) Error() string { return e.Message }
```
