# BayGo (灣行) Autopilot Walkthrough

This document walks through what the Super Skill `autopilot` harness does when
pointed at the BayGo project — the 粤港澳大湾区 one-stop life service platform
(cross-border bus + business car, 生鲜, 探索 content, AI assistant) shipping as
微信小程序 + iOS + Android in Uber-style monochrome. The autopilot's 12 phases
map 1:1 to the team's 10-stage commercial lifecycle: phases 0-1 cover
**1 需求发现 + 2 需求分析**, phase 2 is **3 商业可行性**, phases 3-4 split
**4 方案** into product and design, phases 5-6 are **5 研发** (build then prune),
phase 7 is **6 测试与验证**, phase 8 is **7 上线/商业化**, phase 9 is
**8 试点/灰度**, phase 10 is **9 正式商业交付**, and phase 11 is
**10 运营/复盘**. Phases **1 (intent contract)** and **7 (output quality gate)**
are hard gates — failing either stops the run with `failed_phase` recorded in
`run.json`. Everything else is a soft phase that always proceeds; phase 5
(Ralph) has its own inner retry budget (`--max-ralph-rounds`, default 20) and
can run real Python / JS / Bash / Go in the sandbox before handing off.

The walkthrough below assumes a single run rooted at:

```
/Users/pengchengkeji/Documents/Claude project/Bay Area Life-Uber/.super-skill/autopilot/<run-id>/
```

Each phase appends one artifact and one entry into `run.json`.

---

## Phase 0 · `00-research` — 需求发现

| Item | Value |
| --- | --- |
| Skill | `requirement-analysis` (composes with `user-research`, `market-research`) |
| Stage | 1 需求发现 |
| Gate | soft |

For BayGo this phase produces a research memo that lists the five concrete user
roles from the PRD (香港跨境通勤者, 商务出行用户, 家庭用户, 绿色食品消费者,
来港/来湾区游客) plus 商家 and 平台运营 as secondary roles, the pain map
(跨城 + 跨境 + 跨语言 + 跨支付 + 跨服务商 fragmentation), and a competitor
scan covering KTB / Trip.com bus, HK Express, FreshHema, 美团 / 大众点评探索流,
plus AI concierge entrants. Output is one markdown file with sections:
**Problem / Users / Competitors / Assumptions / Open Questions / Trace**.

- **Artifact**: `00-research.md` with named JTBD rows ("帮我今晚 7 点后从香港到深圳",
  "周六上午送有机蔬菜到家", "周末带孩子去珠海一日游") and an `unknowns` list
  (e.g. *which 巴士运营商 will sign by MVP*).
- **Soft check**: must include at least 3 distinct user segments and 3
  competitor entries; otherwise phase 1 will likely fail the gate.

---

## Phase 1 · `01-intent` — 需求分析 (HARD GATE)

| Item | Value |
| --- | --- |
| Skill | `intent-contract` |
| Stage | 2 需求分析 |
| Gate | **hard** — Goal + Acceptance + Evidence all required |

This is where BayGo's vague "湾区生活操作系统" gets pinned down to a contract.
The phase produces a fixed-shape document with `Goal`, `Out-of-scope`,
`Acceptance criteria`, `Evidence`, `Trace` — for BayGo that means committing
MVP to **出行 (跨境巴士 + 商务车) + 生鲜 (含冷链) + 探索内容 + AI 任务卡 +
多语言 + 双主题**, while explicitly excluding 联程, 直播, 团购, 企业月结,
主动提醒 — these are pushed to V1.1 / V1.2 / V2.0.

- **Artifact**: `01-intent-contract.md` with acceptance bullets like
  *"用户使用繁体中文登录，购买香港到深圳巴士票，支付后查看电子票"* lifted
  from PRD §11.2.
- **Hard gate**: `run.json` records `grade.required = [Goal, Acceptance, Evidence]`.
  Missing any of the three → `failed_phase: 01-intent` and the run halts.
  This is the only place where "AI 不越权" gets encoded as a measurable
  contract clause (e.g. *"付款 / 证件 / 退改签 must require explicit user confirmation"*).
- If this phase fails, **fix the prompt and rerun without `--force`** — phases
  2-11 are not yet written, so nothing to preserve.

---

## Phase 2 · `02-business-case` — 商业可行性

| Item | Value |
| --- | --- |
| Skill | `business-case` |
| Stage | 3 商业可行性 / 立项评估 |
| Gate | soft (but go/no-go is the recommended outcome) |

For BayGo this becomes a TAM / SAM / SOM table: TAM = 大湾区 8600 万常住人口 +
香港 750 万 + 跨境年人次, SAM = 高频跨境用户 + 香港绿色食品消费 + 中产探索用户,
SOM = MVP 12 个月内可触达的 1-3 万 DAU. ROI table covers 出行 (毛利 ~8-12%
巴士, 15-20% 商务车), 生鲜 (毛利 25-35%, 履约成本高), 探索导流 (CPC + CPS),
AI 助理 (留存放大器, 直接收入低). Risks: 巴士供应商接口稳定性, 跨境合规,
冷链投入, AI 幻觉, 应用商店审核.

- **Artifact**: `02-business-case.md` with a go/no-go verdict, 12-month
  break-even chart description, and a one-line `Decision: GO with phased rollout`.
- **Soft check**: harness flags if no risk has a mitigation owner.

---

## Phase 3 · `03-spec` — 方案-产品

| Item | Value |
| --- | --- |
| Skill | `product-spec` |
| Stage | 4 方案-产品 |
| Gate | soft |

Translates phase 1 + 2 into a PRD slice that `ralph-loop` can actually consume.
For BayGo it produces an MVP slice list mirroring PRD §4.1 (账号 / 出行巴士 /
商务车 / 生鲜 / 探索 / AI / 多语言 / 主题 / 后台), a North Star metric
(**AI 任务确认率 × 出行支付成功率**) plus input/output metrics
(班次搜索→支付转化 8-15%, 生鲜 30 日复购 15-25%, 电子票核销 >98%), and a
roadmap V1.0 → V2.5.

- **Artifact**: `03-product-spec.md` with explicit MVP cuts ("V1 不做 联程 /
  团购 / 直播 / 月结 / 主动提醒"), success metrics, and a rollback plan
  ("if 巴士出票成功率 < 90% for 48h, kill switch 关闭购票入口, 退回 H5 客服流").
- **Soft check**: must include a North Star + at least one rollback condition.

---

## Phase 4 · `04-design` — 方案-设计

| Item | Value |
| --- | --- |
| Skill | `design-templates` (DESIGN.md methodology + DesignDNA) |
| Stage | 4 方案-设计 |
| Gate | soft |

Produces BayGo's design contract — Uber-style 黑白极简 explicitly committed
as Aesthetic Direction (*not* generic "modern minimal"). Tokens land as: light
mode 暖白 #FAFAFA bg + 白卡 #FFFFFF + 主 CTA #000 + 绿色生态标签 #00B36B;
dark mode 深黑 #0B0B0B + 深灰卡 #1A1A1A + 白 CTA + 同色绿点缀. Typography:
PingFang SC / TC + SF Pro Text + Inter for English; banned: Noto centered hero
+ 3-card grid AI-slop. Layout: 首页顶部 AI 主输入框, 业务卡片非对称, 底部
5 标签 (首页 / 出行 / 生鲜 / 探索 / 我的).

- **Artifact**: `04-design.md` containing `DESIGN.md` token block, copywriting
  voice samples ("一句话搞定湾区生活", 错态 / 空态 / 成态 文案 5 句), 多语言
  长文案适配规则.
- **Soft check**: must declare 3 forbidden colors / 3 forbidden fonts to dodge
  generic AI aesthetics.

---

## Phase 5 · `05-impl` — 研发 (Ralph Loop)

| Item | Value |
| --- | --- |
| Skill | `ralph-loop` (Python / JS / Bash / Go sandbox runner) |
| Stage | 5 研发 |
| Gate | inner loop, retries up to `--max-ralph-rounds` (default 20) |

This is the only phase that actually executes code. For BayGo, with
`--tracks "frontend-miniapp,backend-api,docs"` the harness fans out: a
微信小程序 track scaffolds 首页 + 出行 + 生鲜 + 探索 + 我的 with `wx.cloud` +
`auth-wechat` (OPENID in cloud functions, no separate login), a backend track
produces Cloud Functions / CloudRun handlers for `searchSchedule /
lockInventory / payOrder / coldchainStatus / aiTaskCard`, and a docs track
writes README + `cloudbaserc.json`. Tests run after each round
(`python -m unittest` for backend stubs, mini-program lint, contract tests
against intent-contract acceptance bullets).

- **Artifact**: `05-implementation.md` capturing the final round's diff
  summary, plus the actual code committed to the project tree (not inside
  `.super-skill/`). `run.json` records `rounds_used`, `tests_passed`,
  `tests_failed`, and a per-round trace.
- **Soft check**: phase exits "succeeded" only if the last sandbox round was
  green; otherwise it exits "exhausted" and phase 7 will catch it.

---

## Phase 6 · `06-simplify` — 研发精简

| Item | Value |
| --- | --- |
| Skill | `code-simplifier` |
| Stage | 5 研发 (b) |
| Gate | soft |

After Ralph finishes, the simplifier reads what landed and removes 过度抽象 /
死码 / 未来兼容垫片 / 冗余注释 — for BayGo a typical pass deletes the unused
商家入驻 / 月结 / 直播 stubs that V1.0 isn't shipping, collapses three
near-identical 列表页组件 (出行班次 / 生鲜商品 / 探索内容) into one shared
`<ListPage>`, and removes any speculative `i18n` keys without translations.
Behavior is preserved — no test deletions allowed.

- **Artifact**: `06-simplified.md` with a before/after LOC delta, list of
  deleted symbols, and a "kept because…" justification for anything that
  *looks* speculative but isn't.
- **Soft check**: phase fails if any test was removed; that condition raises
  a warning before phase 7 sees it.

---

## Phase 7 · `07-gate` — 测试与验证 (HARD GATE)

| Item | Value |
| --- | --- |
| Skill | `output-quality-gate` |
| Stage | 6 测试与验证 |
| Gate | **hard** — `verdict` must be `pass` or `warn`; `fail` halts the run |

The only phase that re-reads phase 1 (intent contract) against phase 6 (final
code) and grades them as a pair. For BayGo the gate checks each acceptance
bullet — *can a 繁体 user actually buy a 香港→深圳 巴士票 and see 电子票?
Does the AI 任务卡 path call 至少 出行/生鲜/探索 三类工具? Does 关闭定位权限
still let users 手动选城?* It also runs the deterministic checks: 支付回调
验签存在, 敏感字段脱敏, 后台操作日志, AI 不绕过二次确认.

- **Artifact**: `07-quality-gate.json` of shape
  `{"verdict": "pass" | "warn" | "fail", "score": 0-10, "missing": [...], "trace": "..."}`.
- **Hard gate**: `fail` → run stops, `failed_phase: 07-gate` in `run.json`.
  Recommended fix: do not `--force` rerun; instead delete `05-implementation.md`
  and `06-simplified.md`, adjust the prompt or contract, then re-run so phases
  0-4 are preserved.

---

## Phase 8 · `08-launch` — 上线 / 商业化准备

| Item | Value |
| --- | --- |
| Skill | `deployment-patterns` |
| Stage | 7 上线 / 商业化准备 |
| Gate | soft |

This is where "code that works on my laptop" becomes shippable. For BayGo it
produces: Dockerfile for the CloudRun container, `cloudbaserc.json` with the
queried `envId`, GitHub Actions CI that runs lint + unittest + 小程序 build,
App Store 审核资料清单 (隐私政策 / 演示账号 / AI 生成内容声明 / 跨境支付说明),
Play Console Data safety 表格, kill-switch 配置 (关 巴士购票 / 关 商务车 /
关 AI 任务卡 三个独立开关), 价格模型 (出行 GMV 抽佣 / 生鲜毛利 / 探索 CPS /
商务车服务费), 回滚剧本.

- **Artifact**: `08-launch-readiness.md` with explicit links to CloudBase 控制台
  (静态托管 / 云函数 / CloudRun / MySQL) for the actual `envId`.
- **Soft check**: warns if no kill switch or no rollback runbook is declared.

---

## Phase 9 · `09-pilot` — 试点 / 灰度

| Item | Value |
| --- | --- |
| Skill | `experiment-driven-delivery` |
| Stage | 8 试点 / 灰度 |
| Gate | soft |

Picks the smallest population that can falsify the value claim. For BayGo a
representative pilot cohort is **5 名香港-深圳高频跨境通勤者 + 3 个香港绿色
食品家庭用户 + 2 名繁体中文 / English 切换的来港游客**, all whitelisted by
微信 OpenID + 手机号 (+852 / +86). They get the 小程序 with feature flag
`pilot=true` enabling 出行 + 生鲜 + AI 任务卡; iOS / Android Beta routes
through TestFlight + 内测分发. Guardrail metrics monitored daily: 支付成功率
> 90%, 电子票核销 > 98%, AI 任务确认率 > 20%, 冷链准时率 > 95%, 客服首响
< 5 分钟.

- **Artifact**: `09-pilot.md` with the cohort definition, feature-flag plan,
  guardrail thresholds, and a stop-loss rule ("if 支付成功率 < 80% over 24h,
  halt onboarding").
- **Soft check**: warns if cohort size < 5 or no guardrail metric is defined.

---

## Phase 10 · `10-commerce` — 正式商业交付

| Item | Value |
| --- | --- |
| Skill | `deployment-patterns` (commercial framing) |
| Stage | 9 正式商业交付 |
| Gate | soft |

Closes the gap between "deployed" and "delivered". For BayGo this means:
商家结算流程 (供应商 / 司机 / 冷链承运商 / 内容商家), 财务对账 (订单单 /
支付单 / 退款单 / 结算单 四层), 发票开具规则 (出行 / 商务车 / 生鲜 分别
配置), SLA 承诺 (核心交易接口 99.5%, 客服首响 < 5 分钟工作时段), 用户协议 +
隐私政策 v1 上线, 应用商店正式版本提审, 多语言客服培训物料, 灾备 (CloudBase
多环境备份 + 数据库快照).

- **Artifact**: `10-commercial-delivery.md` listing acceptance signatures,
  SLA, billing wiring, support runbook, training docs.
- **Soft check**: warns if any of {SLA, 退款流程, 发票流程, 客服 runbook}
  is missing.

---

## Phase 11 · `11-ops` — 运营 / 复盘 / 持续迭代

| Item | Value |
| --- | --- |
| Skill | `agent-memory-dream-loop` (+ `continuous-learning`, `observability-triage-loop`) |
| Stage | 10 运营 / 复盘 / 持续迭代 |
| Gate | soft (privacy check: no raw prompt/response in memory candidate) |

Final phase distills the run into reusable knowledge. For BayGo it produces:
a 复盘 entry naming what worked (Uber 黑白极简 in 多语言 long copy, AI 任务卡
二次确认 pattern), what didn't (假设 of 巴士供应商接口实时性), patterns to
reuse on V1.1 / V1.2 (优惠券 / 会员 / 酒店 / 体检), observability dashboards
(GMV / 支付成功率 / 退款率 / AI 任务成功率 / 冷链准时率), and a memory
candidate ready for `hierarchical-memory` ingestion — but with raw user
prompts and model responses **scrubbed**.

- **Artifact**: `11-ops-retrospective.md` + a memory candidate JSON.
  `run.json` records the privacy check.
- **Soft check**: harness fails the memory write (not the run) if any raw
  prompt / response leaks into the candidate.

---

## How to actually run this on BayGo

From the Super Skill repo (`/Users/pengchengkeji/Documents/GitHub/Super Skill`):

```bash
# Stub provider — offline, deterministic, useful for trying the harness end to end.
bin/super-skill autopilot --provider stub \
  --project "/Users/pengchengkeji/Documents/Claude project/Bay Area Life-Uber" \
  --prompt "BayGo MVP: 微信小程序 + iOS + Android, 出行(跨境巴士 + 商务车) + 生鲜 + 探索 + AI 任务卡, Uber 黑白极简, 简/繁/English, 双主题. PRD at doc/BayGo_Project_Requirements_PRD.md."

# Real run with track fanout — phase 5 forks frontend / backend / docs in parallel.
ANTHROPIC_API_KEY=sk-ant-... bin/super-skill autopilot --provider anthropic \
  --project "/Users/pengchengkeji/Documents/Claude project/Bay Area Life-Uber" \
  --prompt "BayGo MVP per PRD" \
  --tracks "frontend-miniapp,backend-api,docs" \
  --max-ralph-rounds 20

# HITL: pause after the business-case phase for stakeholder review,
# then resume from where we left off.
bin/super-skill autopilot --provider anthropic --project "..." \
  --prompt "BayGo MVP per PRD" --hitl "02-business-case,07-gate"
bin/super-skill resume --project "..." --run-id <run-id>

# Resume after a hard-gate failure (phase 1 or 7) without losing earlier work.
bin/super-skill autopilot --run-id <run-id> \
  --project "/Users/pengchengkeji/Documents/Claude project/Bay Area Life-Uber"
```

Reminder — only **phase 1 (intent-contract)** and **phase 7 (output-quality-gate)**
are hard gates; failure halts the run with `failed_phase` in `run.json`. Every
other phase is soft and proceeds even with warnings — phase 7 is the single
chokepoint that re-reads the original contract against the final deliverable,
so do not skip it for speed.
