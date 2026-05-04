---
name: code-simplifier
description: |
  代码精简收尾:在功能已工作、测试通过后,删除过度抽象、重复代码、死码、未来兼容垫片、冗余注释和过度防御。
  不引入新功能,不改变可观察行为,不删测试覆盖。
  触发词:「简化」「精简」「删冗余」「重构精简」「合并重复」「死码」「过度抽象」「YAGNI」「KISS」。
  适合阶段:feature 完成且测试绿之后、PR 提交前、Ralph Loop 退出后、code review 整理。
---

# Code Simplifier · 代码精简器

> 简化不是"看着不爽就改"。简化是**有清单、有红线、可验证**的工程动作。

## 红线 · 绝对不做

1. **不引入新功能** —— 发现缺功能 → 记下来给用户,不顺手加
2. **不改变可观察行为** —— 输入输出、副作用、错误码必须 100% 等价
3. **不删测试** —— 测试是简化的安全网,期间只能加测试不能删
4. **不动公共 API** —— 除非用户明确说"可以破坏兼容"
5. **不批量重命名** —— 除非有强信号(拼写错误、严重误导、规范统一)
6. **不混提交** —— 一次提交里只做一类简化,便于回滚和 review

---

## 简化清单(按优先级)

详见 [references/checklist.md](references/checklist.md)。

### P0 · 几乎一定要做
- 未使用的导出 / 导入 / 参数 / 局部变量
- 死代码(永不被调用的函数、永远 false 的分支)
- 重复代码块(3 次以上重复 → 抽函数;2 次保留)
- 已删除调用方的兼容垫片
- 引用已不存在代码的注释 / TODO

### P1 · 大概率要做
- 只有一个实现的 interface(可内联)
- 只有一个调用点的 helper(可内联)
- 在内部代码里校验"不可能"的输入(过度防御)
- 除了转发什么都不做的空壳包装
- `_unused` / `// removed` / `// kept for compat` 这类墓碑

### P2 · 谨慎判断
- 复杂条件简化(德摩根、提前 return、卫语句)
- 循环 → 函数式(仅在可读性确实提升时)
- 类型断言收敛(`as any` → 精确类型)
- 拆/合并函数(只有当现有粒度真的别扭时)

### 不要做(看着像简化但其实不是)
- ❌ 把 if/else 改成三元运算符(可读性变差)
- ❌ 把多行变量定义压成一行
- ❌ 删除"防御性"边界检查(那是边界,不是过度防御)
- ❌ 把所有函数都改成箭头函数(风格差异不是简化)

---

## 工作流

### Step 1 · 边界
明确简化范围,**写出来**给用户看:
```
范围: <文件/目录列表 或 "本次会话改过的文件">
跨文件改动: 允许 / 禁止
验证手段: <跑哪个测试套件>
预计 P0/P1/P2 改动数: <粗估>
```

### Step 2 · 扫描
按 P0 → P1 → P2 顺序扫描,每条候选改动单独评估:

```
候选 #N
P 级别: P0 / P1 / P2
位置: <file:line>
现状: <几行代码或一句描述>
建议: <怎么改>
风险: <调用方影响 / 测试覆盖>
决定: 改 / 保留(理由)
```

不要直接动手改,**先扫描,再决定,再动手**。

### Step 3 · 改动(分组提交)
- 每组改动 = 一个 P 级别的同类改动
- 每组改动后跑一次验证
- 验证失败 → 立即回滚那一组,继续下一组
- 不要把多组改动混在一起改

### Step 4 · 报告
```
【Code Simplifier 报告】
范围: <...>
改动统计: 删除 X 行 / 删除 Y 个文件 / 内联 Z 个函数
P0 改动: <列表,每条一句>
P1 改动: <列表>
P2 改动: <列表>
保留未改: <列表 + 理由>
验证: 改动前 <pass/fail> → 改动后 <pass/fail>
建议: <下一步,例如 "建议用户 review xx 文件"
```

---

## 典型场景

### 场景 1 · Ralph Loop 退出后
```
范围: 本次 Ralph Loop 期间改过的文件
重点: 循环里临时加的 console.log、TODO、defensive 检查
验证: 跑同一个验证手段(应该仍然全过)
```

### 场景 2 · PR 提交前
```
范围: git diff --name-only origin/main 改过的文件
重点: P0(死码、未用导入)+ 注释清理
验证: pnpm test + pnpm lint + pnpm typecheck
```

### 场景 3 · 删除某个特性后
```
范围: 全仓库
重点: 找该特性留下的兼容垫片、配置项、文档
验证: 全量测试 + 启动应用确认无报错
```

---

## 反模式

- ❌ **为了好看而改**:没有清单条目对应就别动
- ❌ **大爆炸式重构**:一次改 500 行还说"等价",没人信
- ❌ **顺手加功能**:发现 bug 也只记录,不顺手修(除非用户授权)
- ❌ **跳过验证**:简化的代价是新 bug,跑测试是底线
- ❌ **删除"用不上"的边界检查**:边界(用户输入、外部 API)的检查不是过度防御
- ❌ **追求行数最少**:可读性 > 简短

---

## 与其他 skill 的关系

- **被 `ralph-loop` 在退出后调用**:循环里不简化,出循环再扫一遍
- **被 `design-dev-flow` 在交付前调用**:整项目的最后清扫
- **配合 `code-review`**:对方做正确性审查,本 skill 做"是否冗余"审查

---

## 内置 Plugin(可调用 Agent)

本 skill 内置了一份 Anthropic 官方 [`claude-plugins-official/code-simplifier`](https://github.com/anthropics/claude-plugins-official) 的 agent 定义(`plugin/agents/code-simplifier.md`),Apache 2.0,attribution 见仓库根 `NOTICE`。

Plugin 装好后,可以用 `Agent` 工具直接调用:

```
Agent(subagent_type="code-simplifier", description="...", prompt="...")
```

### 安装

```bash
code-simplifier/scripts/install-plugin.sh install   # 软链到 ~/.claude/plugins/code-skills/code-simplifier
code-simplifier/scripts/install-plugin.sh status
code-simplifier/scripts/install-plugin.sh uninstall
```

或用统一入口:`bin/code-skills plugin install code-simplifier`。

### Plugin 与本 SKILL.md 的关系

- **SKILL.md(本文)**:面向"我作为开发者要简化代码"的工作流(P0/P1/P2、红线、报告格式)
- **plugin/agents/code-simplifier.md**:面向"自动 agent 调用"的提示词,聚焦 ES module / TypeScript 项目惯例

两份内容**互不冲突**:skill 是开发者自己用,plugin 是 agent 替你跑。可以只装其一。

---

## References

- [简化清单(详细判定标准)](references/checklist.md)
- [常见重构手法(每条配前后对比)](references/refactor-patterns.md)
- [内置 Plugin agent 定义](plugin/agents/code-simplifier.md)
