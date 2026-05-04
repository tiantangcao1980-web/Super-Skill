# Test Plan 模板 + Quality Gate 配置

## test-plan.md 标准结构

```md
# <项目> Test Plan

## 1. 项目类型与覆盖率基线
项目类: 个人产品
基线:
  - 单元: ≥ 70%
  - 集成: 关键 API 100%
  - E2E: 3 条关键路径

## 2. 测试金字塔分配

| 层 | 工具 | 频率 | 触发 |
|----|------|------|------|
| 单元 | vitest / pytest | 每次保存 | 本地 + CI |
| 集成 | vitest / pytest | 每次提交 | CI |
| 视觉 | Playwright trace | PR | CI |
| E2E | Playwright | merge to main | CI nightly |
| 安全 | semgrep / trivy | 周期 + 敏感改动 | CI weekly |

## 3. 用例清单(从 PRD User Story 反推)

### Story 1.1 · 拖入出图
- TC-001 happy: 拖入合法 PNG → 5 秒出图
- TC-002 边界: 文件 0 字节 → 错态文案
- TC-003 边界: 文件 11MB(超限)→ 错态文案
- TC-004 错态: Canvas API 不支持 → 降级提示
- TC-005 错态: 网络断(虽然纯前端但 CDN 加载)→ 离线提示

### Story 1.3 · 复制剪贴板
- TC-006 happy: 出图后点复制 → 剪贴板有图
- TC-007 边界: 浏览器不支持 Clipboard API → 提示手动保存
- TC-008 边界: 用户拒绝剪贴板权限 → 提示手动保存

(每条 Story × 3 类 ≥ 用例)

## 4. Quality Gate

merge to main 必过:
□ pnpm test 退出 0
□ pnpm coverage ≥ 70%
□ pnpm e2e 关键 3 条全过
□ pnpm lint 0 error
□ pnpm typecheck 0 error
□ semgrep 无 high/critical
□ Bundle size ≤ 300KB

## 5. 缺陷管理
- 用 GitHub Issues + label: bug, P0/P1/P2/P3
- P0 24h 内修;P1 1 周;P2 下版本
- bug 必填:复现步骤 + 期望 vs 实际 + 环境 + 截图

## 6. Test Data
- fixtures: tests/fixtures/
- 边界值: 0 / 1 / max-1 / max / max+1 / null / undefined
```

---

## CI 配置范例 · `.github/workflows/quality.yml`

```yaml
name: Quality Gate

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test --coverage
      - name: Coverage Gate
        run: |
          cov=$(jq -r '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$cov < 70" | bc -l) )); then
            echo "coverage $cov < 70%"
            exit 1
          fi
      - run: pnpm build
      - name: Bundle size gate
        run: pnpm size-limit

  e2e:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec playwright install --with-deps chromium
      - run: pnpm e2e

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: p/owasp-top-ten
```

---

## 反例 / 常见错误

❌ **没 coverage gate**:测试随便写写,过了 lint 就上(bug 没拦住)
❌ **E2E 跑全量功能**:CI 30 分钟 + flaky 高 → 改成只跑关键路径
❌ **bug 写"不能用了"**:必填字段没填,没法复现
❌ **手动测试报告做主**:每周末熬夜跑一遍,无法持续
✅ 所有 Gate 自动化,人只看 dashboard
