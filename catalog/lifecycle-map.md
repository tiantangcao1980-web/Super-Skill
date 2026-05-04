# Lifecycle Map

Super Skill 的核心不是简单收集技能，而是把技能放进一个“从用户期待到可验证交付”的闭环。

## 主闭环

```mermaid
flowchart LR
  Z["Intent & Context<br/>用户期待/上下文包/Token 预算"] --> A["Research<br/>市场/用户/竞品"]
  A --> B["Analysis<br/>JTBD/需求/数据"]
  B --> C["Product<br/>PRD/MVP/指标"]
  C --> D["Design<br/>DesignDNA/文案/设计系统"]
  D --> E["Interface<br/>API/CLI/契约"]
  E --> F["Development<br/>前端/后端/数据库/Agent"]
  F --> G["Quality<br/>测试/审查/安全/浏览器验证"]
  G --> H["Delivery<br/>部署/GitHub/演示视频/增长素材"]
  H --> I["Operations<br/>文档/知识沉淀/持续学习"]
  I --> Z
```

## 横切能力

- `intent-contract`: 把用户期待变成验收契约。
- `context-engineering`: 为大上下文和长任务构造最小充分上下文包。
- `token-budgeting`: 保留高信号上下文，减少重复和噪声。
- `auto-flow`: 串联主闭环。
- `ralph-loop`: 对长任务执行小步循环和验证。
- `verification-loop`: 在完成声明前强制证据优先。
- `output-quality-gate`: 在最终交付前检查输出是否满足用户期待。
- `agent-routing`: 在直接编辑、工具、MCP、浏览器和子任务之间选择轻量路径。
- `cross-tool-packaging`: 将技能适配到不同 agent 生态。

## 领域生态

`vendor/cowork/` 覆盖法律、财务、营销、销售、客服、企业搜索、数据、生物科研、生产力等领域。它们目前以 vendor form 保留，后续可以按 `domain-skill-name` 命名空间化后纳入 installable skills。
