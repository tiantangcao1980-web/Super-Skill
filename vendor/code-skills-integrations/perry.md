# PerryTS/perry

- **URL**: https://github.com/PerryTS/perry
- **Stars**: 2k+
- **License**: 见原仓库
- **类型**: TypeScript 原生编译器(Rust + SWC + LLVM)

## 这是什么

把 TypeScript 直接编译为**原生可执行文件**,不要 Node.js / Electron / 浏览器引擎。输出单个二进制,跨 macOS / Windows / Linux / iOS / tvOS / Android / Web。生态里已经有真实项目在用(Bloom Engine 游戏引擎、Mango MongoDB GUI、Hone 编辑器、dB Meter)。

## 在 code-skills 中的对应

- **不做成 skill** —— Perry 是构建工具,不是开发模式 / 设计模式
- **被引用的位置**:
  - `cli-design` skill 的"分发包装"步骤,可把 TS 写的 CLI 用 Perry 打包成原生二进制(替代 pkg / nexe / bun build)
  - `design-dev-flow` ⑦ 交付幕,如果项目要发原生应用,Perry 是 Electron 的轻量替代

## 跨端方案选型决策表(本仓库给出建议时用)

| 项目类型 | 首选方案 | 备选方案 | 备注 |
|---------|---------|---------|------|
| 桌面 GUI(macOS+Win+Linux),已有 React 代码 | **Tauri**(Rust 后端) | Electron(成熟但包大) | 包小、性能好、Web 前端复用 |
| 桌面 GUI,愿意 Go 后端 | **Wails** | Tauri | Go 生态用户偏爱 |
| **要发 iOS/tvOS/Android 原生** | **Perry** ⭐ | React Native / Flutter | TS 直接编 native,无 RN bridge |
| **CLI 工具发单二进制** | Perry / Bun build / pkg | nexe(过时) | Perry 的输出最小 |
| 跨平台游戏引擎 | Bloom Engine(用 Perry) | Unity / Godot | TS 写游戏 |
| 网页应用嵌入桌面 | **Electron**(成熟生态) | Tauri | 启动速度比包大小重要时 |
| Web 端运行 | **不用 Perry**,直接 Web | - | Perry 是编 native 的 |
| 微信/支付宝小程序 | uniapp / Taro / 原生 | - | 平台限制,Perry 不适用 |

## 何时用

- 写 TS 但要发原生 app(macOS/iOS/Android)
- 不想给桌面工具背 Electron 几百 MB 的包
- CLI 工具要发布单二进制(替代 pkg / Bun build)
- 跨平台原生 app,只想维护一份 TS 代码
- **学习目的**:理解"TS → 原生"链路怎么搭(SWC + LLVM 是教材级实现)

## 何时**不**用

- 项目大量依赖 npm 包的运行时反射 / eval(可能编译不过)
- 重度依赖 Node 内置模块的服务端代码(Perry 的覆盖在演进中)
- 已在 Tauri / Wails 上跑得好(没必要切)
- v0.5.x 还在快速演进,生产慎用核心路径

## 我们要学的"思想"

### 思想 1 · TS 不必绑死 Node runtime
长期以来,TS 项目意味着"得装 Node + 一堆 npm"。Perry 证明 **TS 可以是一种通用语法层**,后端可以是 native binary。这个范式扩散后会改变前端工程师的"部署思维"。

### 思想 2 · 编译到底比解释到底更可控
Electron / RN 都依赖**运行时**,Perry 走 AOT 编译。运行时少一层 = 调试简单 + 包小 + 启动快。

### 思想 3 · SWC + LLVM 是可复用的"编译工具链"
你做语言工具(linter / 自定义 DSL / transformer)时可以参考这个链路:**用 SWC 解析,中间表示,后端用 LLVM 生成代码**。

## 怎么用

```bash
# 安装(看上游 README 最新方式)
brew install perryts/tap/perry   # 假设有 tap;以 perryts.com 为准

perry compile src/main.ts -o myapp
./myapp                            # 单个原生二进制
```

## 不集成的部分

- 不把 Perry 包装为本仓库的 CLI 子命令(它是构建工具,场景太具体,passthrough 价值低)
- 不在本仓库提供 Perry 项目模板(用 Perry 自己的 starter 即可)
- 不做"该用 Perry / Tauri / Bun / Electron" 决策树(那是构建工具选型 skill 的事 —— 后续可加)
