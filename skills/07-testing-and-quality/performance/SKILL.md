---
name: performance
description: "性能优化专家。当用户遇到性能问题、程序慢、内存使用高、需要优化时触发。Use when user has performance issues, slow code, high memory usage, or needs optimization. Keywords: performance, slow, optimize, memory, CPU, profiling, bottleneck, 性能, 慢, 优化"
---

# 性能优化专家

**黄金法则：先测量，再优化。** 没有数据的优化是猜测。

## 分析流程

```
1. 测量现状 → 基准测试
2. 找瓶颈 → Profiling（通常 20% 代码用 80% 时间）
3. 分析原因
4. 实施优化（最高 ROI 优先）
5. 验证效果 → 重新测量
```

## 常见性能问题

### N+1 查询（最常见杀手）
```typescript
// ❌ 每个用户单独查询订单 = N+1
for (const user of users) {
  user.orders = await db.orders.findMany({ where: { userId: user.id } })
}

// ✅ 一次 JOIN
const users = await db.users.findMany({ include: { orders: true } })
```

### 不必要重渲染（React）
```typescript
// ✅ 缓存昂贵计算
const sortedList = useMemo(() => items.sort(...), [items])
// ✅ 稳定函数引用
const handleClick = useCallback((id) => ..., [dispatch])
// ✅ 防止子组件重渲染
const UserCard = React.memo(({ user }) => <div>{user.name}</div>)
```

### 缓存策略
```typescript
// Redis 缓存
async function getCachedUser(id: string) {
  const cached = await redis.get(`user:${id}`)
  if (cached) return JSON.parse(cached)
  const user = await db.users.findById(id)
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user))
  return user
}
```

## 性能指标参考

| 指标 | 优秀 | 需优化 |
|------|------|--------|
| API 响应 | < 100ms | > 1s |
| 数据库查询 | < 10ms | > 500ms |
| 页面首次加载 | < 2s | > 6s |
| Bundle 大小 | < 200KB | > 1MB |

## 分析工具

```bash
node --inspect app.js          # Node.js（连 Chrome DevTools）
EXPLAIN ANALYZE SELECT ...     # PostgreSQL 慢查询分析
# 前端：Chrome DevTools Performance Tab, Lighthouse
```
