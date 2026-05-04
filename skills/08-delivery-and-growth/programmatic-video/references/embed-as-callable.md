# Remotion 作为底层能力被调用 · 4 种模式

> 不只是做 demo,而是把"用 React 写视觉时间线"当成可被任意 skill 调用的能力。

## 模式 A · 生成静态 mp4 / gif(经典)

**场景**:产品 demo / README hero / ProductHunt 启动 / 营销素材

**调用方**:用户 / `auto-flow ⑨ 交付幕` / `internal-comms`(发布通告)

**实现**:

```bash
bin/code-skills demo init my-demo
bin/code-skills demo render Main out.mp4
```

**关键**:这是已有用法,不展开。

---

## 模式 B · 嵌入 React 组件做产品内动画 ⭐

**场景**:产品里需要复杂动画(loading 序列 / 引导教程 / 数据可视化过场 / hero animation)

**调用方**:`frontend-patterns` 或具体平台 skill(`web-development` / `react-bits` / `tailwindcss`)

**实现**:用 [Remotion Player](https://www.remotion.dev/player) —— 把 Remotion composition 当成普通 React 组件嵌入产品

```tsx
// MyApp.tsx
import { Player } from '@remotion/player'
import { OnboardingAnimation } from './remotion/Onboarding'

function App() {
  return (
    <div>
      <h1>Welcome to SnapMatte</h1>
      <Player
        component={OnboardingAnimation}
        inputProps={{ userName: 'Cheng' }}
        durationInFrames={150}
        fps={30}
        compositionWidth={800}
        compositionHeight={450}
        controls
        autoPlay
        loop
      />
    </div>
  )
}
```

**何时用 vs 何时不用**:

| 场景 | 推荐 |
|------|------|
| 简单 hover / fade / slide | CSS animation(更轻) |
| 中等复杂(timeline / parallax) | Framer Motion(已是 React 生态王者) |
| **数据驱动 + 时间线 + 可批量出图** | **Remotion** |
| 跨页面 / 全屏过场 | View Transitions API + Framer Motion |
| 需要 ServerSide 渲染同一动画做封面 | **Remotion**(同一份 React 组件既能播也能渲染成 mp4/gif) |

**Remotion 不可替代的优势**:**同一个 React 组件,既能在浏览器里实时播,也能服务端渲染成视频文件**。

---

## 模式 C · 数据驱动批量生成 ⭐

**场景**:
- N 个用户 → 每用户一个个性化视频(姓名 / 头像 / 数据)
- 财报数据 → 每周自动出"周报视频"
- A/B 测试 → 同模板出 4 个变体跑实验

**调用方**:`marketing/campaign-planning` / `sales/create-an-asset` / `finance/financial-statements` 等 Cowork 领域 skill

**实现**:

```ts
// build-personalized.ts
import { renderMedia } from '@remotion/renderer'

const users = await fetchUsers()
for (const user of users) {
  await renderMedia({
    composition: 'PersonalizedThankYou',
    serveUrl: 'https://my-remotion-bundle.example.com',
    inputProps: { name: user.name, achievements: user.achievements },
    codec: 'h264',
    outputLocation: `out/${user.id}.mp4`,
  })
}
```

**与本仓库 skill 的连接点**:

```
[user-research]/[financial-analysis] 产数据
          ↓
[programmatic-video]:模式 C 批量出视频
          ↓
[anthropic-skills:internal-comms] 发出去
```

---

## 模式 D · 教学 / 解释性动效

**场景**:
- 复杂算法演示(树遍历 / 排序可视化)
- 流程图动画(状态机过渡)
- 数据故事(金额从 X 涨到 Y 的视觉化)

**调用方**:`engineering/documentation`(已 vendor)/ `internal-comms`(已加载)/ 文档贡献者

**实现**:把要教的概念用 React 组件搭出来,Remotion 控制时间线 fade-in 各步骤。导出 mp4 嵌入文档。

---

## 配合本仓库其他 skill 的具体流程

### 1. `auto-flow ⑨ 交付幕` 调本 skill

```
[⑨ 交付幕]
  ├─ code-simplifier 全量
  ├─ deployment-patterns 部署
  ├─ programmatic-video 模式 A:出 30s demo  ⭐
  ├─ programmatic-video 模式 B:把 hero animation 嵌入产品  ⭐
  └─ anthropic-skills:internal-comms 出发布通告
```

### 2. `marketing/campaign-planning` 调本 skill

```
[campaign-planning]
  ├─ 定义受众分群(N 个 segment)
  ├─ programmatic-video 模式 C:批量出 N 个变体视频  ⭐
  └─ marketing/performance-analytics 监控转化
```

### 3. 产品内引导动画

```
用户点击"新用户引导"
  ├─ App 加载 Remotion <Player>
  ├─ 播放 OnboardingAnimation (Remotion composition)
  └─ 用户跟着走
```

---

## 不要这样

- ❌ **简单 fade-in 用 Remotion**:CSS 一行能搞定的别上 Remotion(开销大)
- ❌ **每秒 60fps 实时交互**:Remotion 是基于"时间线"的,不适合用户输入响应类动画
- ❌ **服务端 renderMedia 没用 caching**:同一组件渲染 1000 次会很慢
- ❌ **嵌入 Player 后忘了 autoPlay / muted policy**:浏览器会拒绝自动播放有声内容

---

## 安装入口(如果项目没装 Remotion)

```bash
# 模式 A:用本仓库 CLI 入口
bin/code-skills demo init my-project

# 模式 B/C:在已有 React 项目里加
npm i remotion @remotion/player @remotion/renderer
```

---

## 与 frontend-patterns 的边界

- 用户问"做一个 hover 动画" → frontend-patterns(CSS / Framer Motion)
- 用户问"30 秒产品 demo" → 本 skill 模式 A
- 用户问"产品内播放复杂引导动画" → 本 skill 模式 B
- 用户问"给 1000 个用户每人一个个性化视频" → 本 skill 模式 C
- 用户问"算法可视化教学" → 本 skill 模式 D

**互不替代**,各司其职。
