# Ralph + Simplifier 协作详细规则

> 在 ④ 前端实现 / ⑤ 后端实现 两幕里,Ralph 和 Simplifier 怎么配合。

## 基本节奏

```
进入开发幕 (④ 或 ⑤)
   │
   ▼
[1] 写循环契约
   │
   ▼
[2] Ralph PLAN → EXEC → VERIFY → DECIDE  (≤ 20 轮)
   │
   ├─── DECIDE = DONE ──────┐
   │                         ▼
   │                    [3] simplifier P0 微清扫(只清本幕新改文件)
   │                         │
   │                         ▼
   │                    [4] 进下一幕
   │
   ├─── DECIDE = ABORT (卡住) ──→ 报告 + 等用户决策(不进 simplifier)
   │
   └─── 第 20 轮仍未 DONE ──→ 续轮申请书(不进 simplifier)
```

---

## 关键规则

### 1. Simplifier 必须在 Ralph DONE **之后**跑

**不要在 Ralph 循环中跑**。理由:
- Ralph 当前轮埋的临时 console.log / debug 输出 / 验证脚手架,**下一轮可能还要用**
- Simplifier 不知道哪些是"临时品",会按 P0 清单删掉,**让 Ralph 下一轮回到坏状态**

### 2. 单幕 simplifier 只跑 **P0 微清扫**

只做最安全、最确定的:
- 删未使用 import / 变量 / 参数
- 删本幕引入的死分支
- 删本幕的墓碑注释 / `// TODO removed` / `console.log("debug")`

**不跑 P1/P2** —— 抽函数 / 改循环结构 / 收敛类型断言这些,留到 ⑦ 交付幕。

### 3. 范围严格限定:本幕新改的文件

```
git diff --name-only <ralph-loop 启动时的 commit>..HEAD
```

只对这个列表跑 simplifier。**不要全量** —— 全量风险大,留到 ⑦。

### 4. simplifier 跑完必须重跑 VERIFY

simplifier 删的东西可能误伤(罕见但发生)。必须重跑本幕的 VERIFY:
- ④ 前端:dev server 起得来 + 主页面渲染 + 主交互可用
- ⑤ 后端:服务起得来 + 健康检查 + 主路由 200

VERIFY ❌ → 回滚本次 simplifier,进下一幕(把 P1/P2 留给 ⑦)。

---

## ⑦ 交付幕的 simplifier 全量

到了交付幕,跑 **P0 + P1 全量**(不跑 P2):

| 级别 | 跑不跑 | 原因 |
|------|------|------|
| P0 | ✅ 跑 | 安全,几乎无风险 |
| P1 | ✅ 跑 | 收益大,风险可控(单实现 interface / 空壳包装等) |
| P2 | ❌ **不跑** | 改循环结构 / 类型收敛 / 拆合并函数 → 引入新 bug 概率太高,留给后续迭代 |

**全量 simplifier 后必须**:
- 重跑全量测试
- 重跑 ⑥ 浏览器验证
- 都过 → 提交;有任一不过 → 回滚 simplifier

---

## 常见错误

### 错误 1:Ralph 没 DONE 就跑 simplifier
**症状**:跑完 simplifier 后 Ralph 验证回到 fail 状态。
**原因**:把 ralph 当前轮的临时品当冗余删了。
**解法**:严格遵守"DONE 后才跑"。

### 错误 2:单幕 simplifier 跑全量
**症状**:本幕产出物变化 + 其他幕的代码也被改 + 难以 review。
**解法**:`git diff` 限定范围。

### 错误 3:simplifier 跑完不重 VERIFY
**症状**:进下一幕后才发现验证坏了,但已不知道是哪一步坏的。
**解法**:每次 simplifier 后必跑 VERIFY,5 分钟成本。

### 错误 4:⑦ 交付幕跑 P2
**症状**:发布前最后一刻引入回归。
**解法**:P2 永远不在自动流程里,只手动跑 + review。

---

## 与 ralph-loop SKILL.md 的关系

- ralph-loop 管"循环本身"(契约 / 节奏 / 卡住 / 续轮)
- 本文档管"循环之外"(谁先跑,谁后跑,跑什么范围)
- 两者**不重复**也**不矛盾**
