# 工作流状态机 · 9 phase enter/exit/artifact

> 每个 phase 都有 enter 条件 / exit 条件 / 强制 artifact。
> **不满足 exit 条件,不准前进**,哪怕用户催。

## 状态总图

```
[START]
   │
   ▼
[Phase 0: Gate]──── 11 项缺失 ───→ 回问用户(不前进)
   │ Gate 通过 + 用户 OK
   ▼
[Phase 1: 调研]── research-report 落盘 ──→ [Phase 2]
   │
   ▼
[Phase 2: 分析]── requirements 落盘 ──→ [Phase 3]
   │
   ▼
[Phase 3: 产品 PRD]── PRD 落盘 ──→ [Phase 4]
   │
   ▼
[Phase 4: 设计规范]── DESIGN+tokens+copy 落盘 ──→ [Phase 5]
   │
   ▼
[Phase 5: 接口契约]── INTERFACE 落盘 ──→ [Phase 6]
   │
   ▼
[Phase 6: 前端 (Ralph + simplifier)]── DONE + verify pass ──→ [Phase 7]
   │
   ▼
[Phase 7: 后端 (Ralph + simplifier)]── DONE + verify pass ──→ [Phase 8]
   │
   ▼
[Phase 8: 测试]── Quality Gate 全 ✅ 或用户接受 ──→ [Phase 9]
   │
   ▼
[Phase 9: 交付]── simplifier 全量 + README + 部署 + 汇报材料 ──→ [DONE]
```

---

## Phase 0 · 需求 Gate
| 字段 | 值 |
|------|---|
| enter | 用户首次发出需求 |
| exit | 11 项填齐 + 4 项可行性通过 + 用户明确"OK" |
| artifact | `docs/0-requirements-snapshot.md` |
| 触发干预 | 任一项缺失 / 可行性 ❌ |

## Phase 1 · 调研 ⭐ 新增
| 字段 | 值 |
|------|---|
| enter | Phase 0 artifact 落盘 |
| exit | research-report.md 含 5 节(画像/访谈洞察/竞品/桌面研究/决定与未决定) |
| artifact | `docs/1-research-report.md` |
| 使用 skill | **`user-research`** + (可选 `file-curation`) |
| Ralph? | 否 |

## Phase 2 · 分析 ⭐ 新增
| 字段 | 值 |
|------|---|
| enter | Phase 1 artifact 落盘 |
| exit | requirements.md 含 JTBD + User Story + 用户旅程 + MoSCoW + RICE 四件套 |
| artifact | `docs/2-requirements.md` |
| 使用 skill | **`requirement-analysis`** + `spec-workflow` |
| Ralph? | 否 |

## Phase 3 · 产品 PRD ⭐ 新增
| 字段 | 值 |
|------|---|
| enter | Phase 2 artifact 落盘 |
| exit | PRD 11 章齐全 + NSM 1 个 + 风险登记 ≥5 条 + 上线/回滚预案 |
| artifact | `docs/3-PRD.md` |
| 使用 skill | **`product-spec`** + `spec-workflow` |
| Ralph? | 否 |

## Phase 4 · 设计规范
| 字段 | 值 |
|------|---|
| enter | Phase 3 artifact 落盘 |
| exit | DESIGN.md ≥ 8 章 + tokens 是合法 JSON + copy.json 5 句无禁用词 |
| artifact | `docs/4-DESIGN.md`, `tokens/design-tokens.json`, `docs/4-copy.json` |
| 使用 skill | `ui-design` + `designdna` + `design-templates` + `copywriting-design` + `taste-skill` 自检 |
| Ralph? | 否 |

## Phase 5 · 接口契约
| 字段 | 值 |
|------|---|
| enter | Phase 4 artifact 落盘 |
| exit | INTERFACE.md 含命令树或 API 路由表 + 退出码/错误码 |
| artifact | `docs/5-INTERFACE.md` |
| 使用 skill | `cli-design` / `api-design` |
| Ralph? | 否 |

## Phase 6 · 前端实现
| 字段 | 值 |
|------|---|
| enter | Phase 5 artifact 落盘 |
| exit | Ralph DONE + 单测通过 + simplifier P0 跑完 + dev server 起 |
| artifact | 可运行前端 + `docs/6-frontend-build-log.md` |
| 使用 skill | `frontend-patterns` + 平台 skill(web/miniprogram/UI 库等) |
| Ralph? | ✅ max=20,DONE 后 simplifier P0 微清扫 |

## Phase 7 · 后端实现
| 字段 | 值 |
|------|---|
| enter | Phase 6 artifact 落盘 |
| exit | Ralph DONE + 单测通过 + simplifier P0 跑完 + 服务起 + 健康检查 200 |
| artifact | 可运行后端 + `docs/7-backend-build-log.md` |
| 使用 skill | `backend-patterns` + `cloud-functions` / `cloudrun-development` 等 |
| Ralph? | ✅ 同 Phase 6 |

## Phase 8 · 测试 ⭐ 新增
| 字段 | 值 |
|------|---|
| enter | Phase 7 artifact 落盘(后端可访问) |
| exit | Quality Gate 全 ✅ 或用户明确接受降级 |
| artifact | `docs/8-test-plan.md`(测试金字塔 + 用例清单)+ `.github/workflows/quality.yml` + 7 层验证报告 |
| 使用 skill | **`qa-strategy`** 编排 → `tdd-workflow` / `e2e-testing` / `browser-automation` / `code-review` / `security-review` / `verification-loop` |
| Ralph? | 否 |
| 触发干预 | 任一 Gate ❌ → 等用户决定 |

## Phase 9 · 交付
| 字段 | 值 |
|------|---|
| enter | Phase 8 通过(或用户接受降级) |
| exit | simplifier 全量(P0+P1)跑完 + README + 部署 URL + 汇报材料 |
| artifact | 简化后代码 + `README.md` + 部署链接 + `docs/9-report.pdf/pptx/docx`(按需) + `docs/demo/`(可选) |
| 使用 skill | `code-simplifier` 全量 + `deployment-patterns` / 平台部署 + Cowork(`anthropic-skills:pptx/docx/pdf/xlsx`) + `programmatic-video`(可选) |
| Ralph? | 否 |
| 触发干预 | 涉及付费(域名/CDN) / 部署到生产前 |

---

## 状态文件(每 phase 必写)

每个 phase 退出时,在 `docs/_state.json` 里更新:

```json
{
  "phase": 6,
  "phase_name": "frontend",
  "status": "done",
  "ralph_iterations": 6,
  "simplifier_p0_changes": 12,
  "verification_pass": true,
  "next_phase": 7,
  "intervention_required": false,
  "ts": 1747000000
}
```

---

## 异常路径

| 触发 | 行为 |
|------|------|
| 任一 phase 的 exit 不满足 | 不前进,报告 + 等用户决策 |
| Phase 0 用户长时间不回应 | 收摊,留 `docs/0-snapshot.md` 草稿 |
| Phase 6/7 Ralph 满 20 轮 | 续轮申请书 + 等用户回复 |
| Phase 8 Quality Gate ❌ | 选项:回 Phase 6/7 修复 / 接受降级 / 改需求回 Phase 0 |
| 任一时刻用户 `/cancel-ralph` 或"停" | 立即停止,留当前 phase 的 artifact |
