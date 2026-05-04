---
name: database-patterns
description: 设计或重构数据库层，涵盖 SQL/NoSQL、ORM、迁移策略、索引和数据模型演进。Use when the task is about schema design, persistence patterns, migration planning, or DB performance beyond a single raw query.
---

# 数据库模式

## 关系型数据库

### 表设计原则
- 主键: 自增 ID 或 UUID v7（有序）
- 时间戳: `created_at`, `updated_at` (自动维护)
- 软删除: `deleted_at` 字段（可选）
- 枚举: 使用短字符串（如 `'active'`），避免数字枚举

### PostgreSQL 特性
```sql
-- JSON 字段索引
CREATE INDEX idx_user_metadata ON users USING GIN (metadata jsonb_path_ops);

-- 全文搜索
CREATE INDEX idx_posts_search ON posts USING GIN (to_tsvector('chinese', title || content));

-- 分区表（大数据量）
CREATE TABLE orders (id BIGINT, created_at TIMESTAMPTZ)
PARTITION BY RANGE (created_at);
```

### MySQL 特性
```sql
-- 字符集（必须 utf8mb4）
CREATE TABLE users (
  name VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 覆盖索引
CREATE INDEX idx_user_email_name ON users (email, name);
```

## NoSQL 数据库

### MongoDB
```javascript
/** 用户文档结构 */
{
  _id: ObjectId("..."),
  email: "user@example.com",
  profile: { name: "张三", avatar: "..." },  // 嵌套文档
  orders: [ObjectId("...")],                   // 引用关联
  tags: ["vip", "active"],                     // 数组字段
  createdAt: ISODate("...")
}
```
- 嵌套 vs 引用: 频繁一起查的数据嵌套，独立生命周期的引用
- 索引: 复合索引、文本索引、TTL 索引

### Redis
| 数据结构 | 用途 |
|----------|------|
| String | 缓存、计数器、分布式锁 |
| Hash | 对象缓存（用户信息） |
| List | 消息队列、最新列表 |
| Set | 标签、共同好友 |
| Sorted Set | 排行榜、延迟队列 |
| Stream | 事件流、日志 |

## 索引策略

### 何时添加
- WHERE 高频条件列
- JOIN 关联列
- ORDER BY 排序列
- 基数高的列优先

### 索引类型

| 类型 | 适用场景 | 数据库 |
|------|----------|--------|
| B-tree | 等值/范围查询 | PostgreSQL/MySQL |
| GIN | 全文搜索/JSON/数组 | PostgreSQL |
| Hash | 等值查询 | PostgreSQL/Redis |
| GiST | 地理/几何数据 | PostgreSQL |
| 全文索引 | 文本搜索 | MySQL/PostgreSQL |

## ORM 最佳实践

### 通用规则
- 复杂查询: 直接写 SQL（ORM 不擅长的场景）
- N+1 问题: 使用 eager loading / JOIN
- 事务边界: 明确且最小化
- 连接池: 配置合理大小（通常 CPU 核数 * 2 + 1）

### 各语言 ORM

```python
# SQLAlchemy（Python）
async with session.begin():
    user = await session.get(User, user_id)
    user.name = "新名称"
    # 自动提交或回滚
```

```typescript
// Prisma（TypeScript）
const user = await prisma.user.findUnique({
  where: { id: userId },
  include: { orders: true },  // 预加载关联
});
```

```go
// GORM（Go）
db.Preload("Orders").First(&user, userId)
```

## 迁移管理

| 工具 | 语言 | 特点 |
|------|------|------|
| Alembic | Python | SQLAlchemy 配套 |
| Prisma Migrate | TypeScript | 声明式 schema |
| golang-migrate | Go | SQL 文件驱动 |
| Flyway | Java | 版本化 SQL |
| Knex | TypeScript | 编程式迁移 |

### 迁移规则
- 迁移文件不可修改（只追加）
- 大表 DDL 使用在线方案（pt-online-schema-change）
- 生产迁移先在 staging 验证
- 提供 down 回滚脚本

## 查询优化

1. `EXPLAIN ANALYZE` 分析执行计划
2. 避免全表扫描（确保有索引）
3. 分页: cursor-based > offset（大数据集）
4. 批量操作: INSERT ... VALUES 多行
5. 读写分离: 写主库、读从库
