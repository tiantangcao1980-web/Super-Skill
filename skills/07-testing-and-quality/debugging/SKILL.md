---
name: debugging
description: "调试分析专家。当用户遇到 bug、报错、程序崩溃、异常行为时触发。Use when user has a bug, error, crash, or unexpected behavior. Keywords: debug, bug, error, exception, crash, not working, fix, 调试, 报错, 不工作"
---

# 调试分析

调试不是猜测，而是用科学方法缩小问题范围。

## 调试流程

```
重现问题 → 形成假设 → 设计验证 → 分析结果 → 修复 → 防止复发
```

## 接收错误信息时的分析步骤

1. **识别错误类型**：这是什么异常？
2. **定位来源**：Stack trace 中第一个"自己的代码"在哪一行？
3. **分析上下文**：什么操作触发了这个错误？
4. **列出可能原因**：2-3 个最可能的假设
5. **验证步骤**：如何确认是哪个原因（加什么日志？）
6. **修复方案**：具体代码改动

## 常见错误模式

**TypeError / undefined：**
- 变量是否初始化？
- 异步操作是否 await？
- 可选链 `?.` 是否遗漏？

**Promise/async 问题：**
- 所有 async 函数是否被 await？
- Promise 错误是否被 catch？
- 是否存在竞态条件？

**N+1 / 性能：**
- 是否在循环内部执行数据库查询？
- 是否使用了 `console.time()` 来定位慢点？

## 输出格式

```
## 问题分析

**错误类型**：...
**根本原因**（最可能）：...

**排查步骤**：
1. 在 XXX 处添加日志：`console.log(...)`
2. 检查 YYY 的值

**修复方案**：
[具体代码]

**防止复发**：
[测试 or 监控]
```
