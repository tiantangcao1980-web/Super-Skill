# 循环节奏与场景

## 节奏 A · 自适应(默认)

**特征**:每轮立即开始,无固定间隔。下一轮的 PLAN 由上一轮的 VERIFY 决定。

**适用**:
- 代码迭代、调试、PR 打磨
- 测试驱动修复
- 视觉回归到设计稿
- 文档逐段精修

**节奏控制**:
- 单轮内不要塞太多,5-15 分钟为佳
- 连续 N 轮无进展 → 主动 ABORT 让用户介入

**模板**:
```
契约 → 第1轮(PLAN/EXEC/VERIFY/DECIDE=CONTINUE)
     → 第2轮(基于第1轮的 VERIFY 输出)
     → ...
     → 第K轮(DECIDE=DONE)
     → 退出报告
```

---

## 节奏 B · 固定间隔

**特征**:每 N 秒/分钟检查一次,不一定每次都有动作。

**适用**:
- 等待 CI 跑完
- 监控部署状态
- 等远端任务完成
- 定期触发数据收集

**节奏控制**:用 `ScheduleWakeup` 或 `/loop <interval>`。
- 5 分钟内的等待:用 `ScheduleWakeup delaySeconds=270`(保持缓存命中)
- 5 分钟以上的等待:用 `delaySeconds=1200..1800`(20-30 分钟一次,避免烧 token)
- **永远不要** 用 `delaySeconds=300`(刚好失缓存,最差选择)

**模板**:
```
契约 → 第1轮检查 → 未达成 → ScheduleWakeup(N 秒)
     → 第2轮检查 → 未达成 → ScheduleWakeup(N 秒)
     → ...
     → 第K轮 → DONE → 报告并不再 schedule
```

---

## 节奏 C · 触发式

**特征**:不主动循环,等外部事件再跑下一轮。

**适用**:
- 多 agent 协作(等同事产出)
- 用户 review 反馈循环
- 文件变更监听
- Webhook / Hook 驱动

**节奏控制**:由 hook / 用户 / 上游 agent 触发。本 skill 只规定单轮怎么走。

**模板**:
```
契约 → 等待信号
     → 信号到 → 第N轮(PLAN/EXEC/VERIFY/DECIDE)
     → DECIDE=CONTINUE → 等待下一个信号
     → DECIDE=DONE → 报告
```

---

## 节奏选择决策树

```
要等外部信号吗?
├─ 是 → 节奏 C
└─ 否 → 任务一次能跑完吗?
        ├─ 不能,要重试,但每次跑很快(秒级) → 节奏 A
        └─ 不能,要等远端结果(分钟级以上) → 节奏 B
```

---

## 单轮时间预算

每轮 PLAN+EXECUTE+VERIFY 的总耗时建议:

| 任务类型 | 单轮预算 | 总轮数上限 |
|---------|---------|-----------|
| 代码修复 | 3-8 分钟 | 6-10 |
| 视觉回归 | 5-10 分钟 | 4-6 |
| 文档打磨 | 2-5 分钟 | 5-8 |
| CI/部署等待 | 1-3 分钟 | 不限轮数,但有总时长上限 |

**超预算就 ABORT,不要硬撑**。卡 30 分钟还没产出 = 方向错了。

---

## 进度可视化

每轮输出 emoji 状态条,让用户一眼看到进度:

```
🔁 Iter 3/8 ── EXECUTE ─ 改了 src/api/user.ts
              VERIFY  ─ 32 passed, 4 failed
              DECIDE  ─ CONTINUE (4→2 失败,有进展)
```

```
🔁 Iter 5/8 ── EXECUTE ─ 修复 race condition
              VERIFY  ─ 36 passed, 0 failed ✅
              DECIDE  ─ DONE
```

---

## 卡住时怎么办

连续 2-3 轮 VERIFY 输出**完全相同** = 卡住信号。处理:

1. **先 ABORT 这一轮**,不要继续
2. **总结卡点**:具体卡在哪个 case、哪个错误信息
3. **给用户三选项**:
   - A. 换思路(描述新方向,等用户确认)
   - B. 缩小目标(把退出条件放宽)
   - C. 升级人工(让用户接管)
4. **不要假装有进展**:输出"差不多了"是 Ralph Loop 最大的失败

---

## 与 ScheduleWakeup / CronCreate 的搭配

- **本 skill 是单会话内的循环结构**
- **跨会话/天的循环** → 用 `/schedule` 或 `CronCreate`
- **会话内定时唤醒** → 用 `ScheduleWakeup`(节奏 B)

不要把这三个混淆。
