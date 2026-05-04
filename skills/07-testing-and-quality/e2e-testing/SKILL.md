---
name: e2e-testing
description: 设计和实现 Playwright/Cypress 端到端测试套件，包括 Page Object、fixture、测试组织和关键用户流程覆盖。Use when building maintainable E2E tests; use the playwright skills for ad hoc browser automation/debugging.
---

# E2E 测试

## 框架选择

- **Playwright**: 推荐，跨浏览器，速度快
- **Cypress**: 适合 React/Vue，调试体验好

## Page Object 模式

```typescript
class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('邮箱');
    this.passwordInput = page.getByLabel('密码');
    this.submitButton = page.getByRole('button', { name: '登录' });
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

## 测试编写原则

1. 每个测试独立，无相互依赖
2. 使用用户可见的选择器（role, label, text）
3. 避免 CSS 选择器和 XPath
4. 等待断言而非固定延时
5. 测试数据独立管理

## 关键用户流程

优先覆盖：
- 注册/登录流程
- 核心业务流程
- 支付流程
- 权限验证

## 测试组织

```
tests/
  e2e/
    pages/           # Page Objects
    fixtures/        # 测试数据
    auth.spec.ts     # 认证相关
    checkout.spec.ts # 结账流程
```
