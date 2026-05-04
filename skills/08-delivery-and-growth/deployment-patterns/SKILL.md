---
name: deployment-patterns
description: 设计、实现或排查通用部署与 DevOps 流程，涵盖 Docker, Kubernetes, CI/CD, serverless, observability, and IaC. Use when the platform is generic or mixed; use render-deploy specifically for Render hosting.
---

# 部署与 DevOps 模式

## Docker

### 多阶段构建模板

```dockerfile
# Node.js 应用
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
WORKDIR /app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
USER app
EXPOSE 3000
HEALTHCHECK CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/main.js"]
```

```dockerfile
# Python 应用
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Docker Compose
```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
volumes:
  pgdata:
```

## CI/CD

### GitHub Actions
```yaml
name: CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t app .
      - run: docker push $REGISTRY/app:latest
```

### GitLab CI
```yaml
stages: [lint, test, build, deploy]
lint:
  stage: lint
  script: npm run lint
test:
  stage: test
  script: npm test
build:
  stage: build
  script: docker build -t $CI_REGISTRY_IMAGE .
```

## Kubernetes

```yaml
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels: { app: myapp }
  template:
    spec:
      containers:
        - name: app
          image: myapp:latest
          ports: [{ containerPort: 3000 }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 512Mi }
          livenessProbe:
            httpGet: { path: /health, port: 3000 }
          readinessProbe:
            httpGet: { path: /ready, port: 3000 }
```

## 监控与告警

| 层级 | 工具 | 指标 |
|------|------|------|
| 基础设施 | Prometheus + Grafana | CPU、内存、磁盘、网络 |
| 应用性能 | OpenTelemetry | 响应时间、错误率、吞吐量 |
| 日志 | ELK / Loki | 错误日志、审计日志 |
| 业务指标 | 自定义 Metrics | 注册数、订单量、转化率 |
| 告警 | Alertmanager / PagerDuty | 5xx > 1%、P99 > 2s |

## 回滚策略

1. 保留最近 5 个版本的镜像/制品
2. 数据库迁移支持回退
3. 功能开关（Feature Flag）控制新功能
4. 蓝绿部署 / 金丝雀发布 / 滚动更新
5. 回滚命令: `kubectl rollout undo deployment/app`

## 云平台对照

| 服务 | AWS | Azure | GCP | 国内 |
|------|-----|-------|-----|------|
| 计算 | EC2/ECS | VM/AKS | GCE/GKE | 阿里云ECS/ACK |
| 数据库 | RDS | Azure SQL | Cloud SQL | 阿里云RDS |
| 存储 | S3 | Blob | GCS | OSS |
| CDN | CloudFront | Front Door | Cloud CDN | CDN |
| Serverless | Lambda | Functions | Cloud Functions | FC |

## 环境管理

| 环境 | 用途 | 数据 | 部署方式 |
|------|------|------|----------|
| dev | 本地开发 | 模拟数据 | docker-compose |
| staging | 预发布 | 脱敏数据 | 自动部署 |
| production | 生产 | 真实数据 | 审批后部署 |
