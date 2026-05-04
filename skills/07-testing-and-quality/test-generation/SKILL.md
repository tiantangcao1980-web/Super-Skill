---
name: test-generation
description: 生成单元测试和集成测试，包括 mock、fixture、边界条件和覆盖率补全。Use when asked to write or extend tests around specific code paths; use e2e-testing for full browser/user-flow suites and test-driven-development for explicit test-first development.
---

# 测试生成

好的测试不只追求覆盖率数字，而是真正捕获 bug，作为活文档存在。

## 必须覆盖的场景

1. **Happy Path**：最典型的成功场景
2. **Edge Cases**：空值/null、空数组、边界值
3. **Error Cases**：无效输入、依赖服务异常、超时
4. **Business Rules**：每个重要业务约束

## 测试结构（AAA 模式）

```typescript
describe('UserService', () => {
  it('should create user with hashed password', async () => {
    // Arrange
    const userData = { email: 'test@example.com', password: 'plain123' }
    mockHashService.hash.mockResolvedValue('hashed123')

    // Act
    const result = await userService.createUser(userData)

    // Assert
    expect(result.password).toBe('hashed123')
  })
})
```

## Mock 原则

```typescript
// ✅ Mock 外部依赖（DB、API、文件系统）
jest.mock('../services/email.service')

// ✅ 使用 factory 创建测试数据
const createUser = (overrides = {}) => ({
  id: 'user-123', email: 'test@example.com', ...overrides
})

// ❌ 不要 Mock 被测单元本身
// ❌ 不要在测试间共享可变状态
```

## 输出流程

1. 分析被测代码，识别所有场景
2. 列出测试计划（用例清单）
3. 生成完整测试代码（含 mock 配置）
4. 说明覆盖率预期
