---
name: frontend-patterns
description: 规划或重构前端架构，涵盖 React/Vue/Angular/Svelte、Next.js/Nuxt、移动端状态管理和渲染性能。Use when the task is about frontend structure, cross-component behavior, or framework patterns, not pixel-perfect design translation.
---

# 前端开发模式

## 框架选择指南

| 框架 | 适用场景 | SSR 方案 | 最新查询 |
|------|----------|----------|----------|
| React 19+ | 大型应用、Server Components | Next.js 16 | `resolve-library-id react` |
| Vue 3 | 渐进式采用、Composition API | Nuxt 3 | `resolve-library-id vue` |
| Angular 19+ | 企业应用、Signals | Angular SSR | `resolve-library-id angular` |
| Svelte 5+ | 轻量高性能、Runes | SvelteKit 2 | `resolve-library-id svelte` |

> **保持最新**: 使用 context7 MCP 的 `resolve-library-id` + `query-docs` 查询任意框架最新文档和 API。
| Solid | 极致性能、细粒度响应 | SolidStart |

## 组件设计

### 组件分类
- **页面组件**: 路由级别，负责数据获取和布局
- **容器组件**: 管理状态和业务逻辑
- **展示组件**: 纯 UI 渲染，通过 props 驱动
- **通用组件**: 可复用原子组件（Button, Input, Modal, Table）

### 组件原则
- 单一职责: 一个组件做一件事
- Props 接口清晰: 必须有类型定义
- 组合优于继承: 使用 children / slots / render props

## 状态管理

| 层级 | React | Vue | Angular |
|------|-------|-----|---------|
| 组件局部 | useState | ref/reactive | 成员变量 |
| 跨组件共享 | Context | provide/inject | Service |
| 全局状态 | Zustand/Redux | Pinia | NgRx/Signal |
| 服务端状态 | TanStack Query | VueQuery | HttpClient+RxJS |
| 表单状态 | React Hook Form | VeeValidate | Reactive Forms |

## 性能优化

### 通用策略
- 代码分割: 按路由拆分，动态 `import()`
- 图片优化: WebP/AVIF + 懒加载 + srcset 响应式
- 虚拟列表: 大数据集渲染（react-virtuoso、vue-virtual-scroller）
- 缓存: Service Worker / HTTP Cache-Control

### React 特有
- `React.memo()` 避免不必要渲染
- `useMemo` / `useCallback` 缓存计算和回调
- `useTransition` 延迟非紧急更新

### Vue 特有
- `computed` 自动缓存计算
- `shallowRef` 减少深层响应
- `v-once` / `v-memo` 静态内容优化

## 移动端开发

### React Native
```typescript
/** 用户列表页面组件 */
const UserListScreen: FC = () => {
  const { data, isLoading } = useUsers();
  return (
    <FlatList
      data={data}
      renderItem={({ item }) => <UserCard user={item} />}
    />
  );
};
```

### Flutter (Dart)
```dart
/// 用户列表页面
class UserListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemBuilder: (context, index) => UserCard(user: users[index]),
    );
  }
}
```

## CSS 架构

| 方案 | 适用场景 |
|------|----------|
| Tailwind CSS | 快速开发、原子化 |
| CSS Modules | 组件隔离、传统 CSS |
| styled-components | CSS-in-JS、动态样式 |
| UnoCSS | 极致性能、可定制 |

## 可访问性 (a11y)

- 语义化 HTML: `<nav>`, `<main>`, `<article>`
- ARIA 属性: `role`, `aria-label`, `aria-expanded`
- 键盘导航: Tab 顺序、焦点管理
- 颜色对比度: WCAG 2.1 AA 级（4.5:1）
- 屏幕阅读器: alt 文本、live region

## 国际化 (i18n)

- React: `react-intl` / `i18next`
- Vue: `vue-i18n`
- 日期时间: `dayjs` / `date-fns` (locale)
- 数字格式: `Intl.NumberFormat`
