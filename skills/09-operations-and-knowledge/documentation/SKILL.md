---
name: documentation
description: "技术文档专家。当用户需要写技术文档、README、API 文档、代码注释、JSDoc 时触发。Use when asked to write docs, README, API documentation, code comments, JSDoc, or docstrings. Keywords: docs, README, documentation, comment, JSDoc, 文档, 注释"
---

# 技术文档

好的文档不是"有"，而是"有用"。

## 注释原则：解释 Why，而非 What

```typescript
// ❌ 无用：描述显而易见的事
// 循环遍历用户
for (const user of users) {

// ✅ 有用：解释非显而易见的决策
// 必须按 createdAt 升序，批处理 API 要求幂等顺序
// 见：https://internal-wiki/batch-api#ordering
users.sort((a, b) => a.createdAt - b.createdAt)
```

## JSDoc 最佳实践

```typescript
/**
 * 创建新用户并发送欢迎邮件
 *
 * @param userData - 用户注册信息
 * @param options.skipEmail - 跳过欢迎邮件（用于测试/批量导入）
 * @returns 创建成功的用户对象
 * @throws {ValidationError} email 格式不合法时
 * @throws {ConflictError} email 已被注册时
 * @example
 * const user = await createUser({ email: 'test@example.com' }, { skipEmail: true })
 */
async function createUser(userData: UserInput, options?: Options): Promise<User>
```

## README 结构

```markdown
# 项目名
> 一句话描述：解决什么问题

## 快速开始（立即可用的代码示例）
## 功能特性
## 安装与配置
## 使用文档（常见场景）
## API 参考
## 开发指南
## 贡献 / 许可证
```

## 文档质量检查

- [ ] 代码示例可直接运行？
- [ ] 没有"假设读者已知"的跳跃？
- [ ] 错误处理在文档中有说明？
- [ ] 有版本信息（适用于哪个版本）？
