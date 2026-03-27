# Cozlive 部署指南

## 环境要求

### 开发环境

- **Node.js**: >= 18.0.0
- **Python**: >= 3.11
- **pnpm**: >= 8.0.0
- **Docker**: >= 20.0
- **Docker Compose**: >= 2.0

### 生产环境

- **Kubernetes**: >= 1.25
- **Helm**: >= 3.0
- **Terraform**: >= 1.5

---

## 本地开发部署

### 1. 克隆代码

```bash
git clone https://github.com/chenliulian/cozlive.git
cd cozlive
```

### 2. 安装依赖

```bash
# 安装前端依赖
pnpm install

# 安装 AI Agent Engine 依赖
cd services/ai-agent-engine
pip install -r requirements.txt

# 安装测试依赖
cd ../../tests
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp infrastructure/docker/.env.example .env

# 编辑 .env 文件，配置以下变量
```

**必需配置**:
```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/cozlive
MONGODB_URL=mongodb://localhost:27017/cozlive
REDIS_URL=redis://localhost:6379/0

# AI 服务
OPENAI_API_KEY=your_openai_api_key

# JWT
JWT_SECRET=your_jwt_secret
JWT_EXPIRATION=7d
```

### 4. 启动基础设施

```bash
# 使用 Docker Compose 启动数据库和缓存
docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d
```

这将启动:
- PostgreSQL (端口 5432)
- MongoDB (端口 27017)
- Redis (端口 6379)
- Kafka (端口 9092)

### 5. 运行数据库迁移

```bash
# User Service 迁移
pnpm --filter @cozlive/user-service migration:run
```

### 6. 启动服务

#### 方式一：使用脚本（推荐）

```bash
# 启动所有服务
./scripts/start-dev.sh

# 停止所有服务
./scripts/stop-dev.sh
```

#### 方式二：手动启动

```bash
# 终端 1: 启动 Web 前端
pnpm dev:web

# 终端 2: 启动 AI Agent Engine
pnpm dev:ai-engine

# 终端 3: 启动 User Service
pnpm dev:user-service
```

### 7. 验证部署

```bash
# 检查服务状态
curl http://localhost:3000/api/health      # Web
curl http://localhost:8000/health          # AI Agent Engine
curl http://localhost:3001/api/health      # User Service
```

### 8. 运行测试

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 运行单元测试
python3 -m pytest tests/unit/ -v

# 运行集成测试
python3 -m pytest tests/integration/ -v
```

---

## Docker 部署

### 构建镜像

```bash
# 构建所有镜像
docker-compose -f infrastructure/docker/docker-compose.yml build

# 构建特定服务
docker-compose build web
docker-compose build ai-agent-engine
```

### 启动服务

```bash
# 生产环境启动
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 环境变量配置

创建 `infrastructure/docker/.env`:

```env
# 应用配置
NODE_ENV=production
DEBUG=false

# 数据库
POSTGRES_USER=cozlive
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=cozlive

# Redis
REDIS_PASSWORD=secure_password

# JWT
JWT_SECRET=your_production_jwt_secret

# AI
OPENAI_API_KEY=your_production_api_key
```

---

## Kubernetes 部署

### 1. 准备镜像

```bash
# 构建镜像
docker build -t cozlive/web:latest ./apps/web
docker build -t cozlive/ai-agent-engine:latest ./services/ai-agent-engine
docker build -t cozlive/user-service:latest ./services/user-service

# 推送镜像到仓库
docker push cozlive/web:latest
docker push cozlive/ai-agent-engine:latest
docker push cozlive/user-service:latest
```

### 2. 配置命名空间

```bash
kubectl apply -f infrastructure/kubernetes/namespace.yaml
```

### 3. 部署服务

```bash
# 部署 Web 服务
kubectl apply -f infrastructure/kubernetes/web-deployment.yaml

# 部署 AI Agent Engine
kubectl apply -f infrastructure/kubernetes/ai-engine-deployment.yaml

# 部署 User Service
kubectl apply -f infrastructure/kubernetes/user-service-deployment.yaml
```

### 4. 配置 Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cozlive-ingress
  namespace: cozlive
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt
spec:
  tls:
  - hosts:
    - api.cozlive.com
    - ws.cozlive.com
    secretName: cozlive-tls
  rules:
  - host: api.cozlive.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ai-agent-engine
            port:
              number: 8000
```

### 5. 验证部署

```bash
# 查看 Pod 状态
kubectl get pods -n cozlive

# 查看服务状态
kubectl get svc -n cozlive

# 查看日志
kubectl logs -f deployment/web -n cozlive
```

---

## Terraform 云部署

### 1. 配置 Terraform

```bash
cd infrastructure/terraform

# 初始化
terraform init

# 配置变量
cp terraform.tfvars.example terraform.tfvars
```

### 2. 配置云提供商凭证

**AWS**:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=ap-southeast-1
```

**阿里云**:
```bash
export ALICLOUD_ACCESS_KEY=your_access_key
export ALICLOUD_SECRET_KEY=your_secret_key
export ALICLOUD_REGION=cn-hangzhou
```

### 3. 部署基础设施

```bash
# 查看执行计划
terraform plan

# 应用配置
terraform apply

# 销毁资源（如需）
terraform destroy
```

---

## 生产环境最佳实践

### 1. 安全配置

```bash
# 生成强密码
openssl rand -base64 32

# 配置 HTTPS
# 使用 Let's Encrypt 自动证书

# 配置防火墙
# 仅开放 80, 443 端口
```

### 2. 监控配置

```bash
# 部署 Prometheus + Grafana
kubectl apply -f monitoring/prometheus.yaml
kubectl apply -f monitoring/grafana.yaml

# 配置告警
kubectl apply -f monitoring/alerts.yaml
```

### 3. 日志收集

```bash
# 部署 ELK Stack
kubectl apply -f logging/elasticsearch.yaml
kubectl apply -f logging/logstash.yaml
kubectl apply -f logging/kibana.yaml
```

### 4. 备份策略

```bash
# 数据库备份脚本
#!/bin/bash
pg_dump -h localhost -U cozlive cozlive > backup_$(date +%Y%m%d).sql

# 自动备份（Cron）
0 2 * * * /path/to/backup.sh
```

---

## 常见问题

### 问题 1: 端口冲突

**现象**: `Error: listen EADDRINUSE: address already in use`

**解决**:
```bash
# 查找占用端口的进程
lsof -i :3000

# 终止进程
kill -9 <PID>
```

### 问题 2: 数据库连接失败

**现象**: `Error: connect ECONNREFUSED`

**解决**:
```bash
# 检查数据库状态
docker-compose ps

# 重启数据库
docker-compose restart postgres

# 检查连接字符串
# 确保 host 是 localhost 而不是 127.0.0.1
```

### 问题 3: AI Agent Engine 启动失败

**现象**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 检查 Python 版本
python3 --version  # 需要 >= 3.11
```

### 问题 4: 内存不足

**现象**: `Error: Out of memory`

**解决**:
```bash
# 增加 Docker 内存限制
docker-compose -f docker-compose.yml up -d --memory=4g

# 或减少服务实例数
# 修改 docker-compose.yml 中的 replicas
```

---

## 性能调优

### 数据库优化

```sql
-- 添加索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at);

-- 分析查询性能
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### Redis 优化

```bash
# 配置最大内存
maxmemory 2gb
maxmemory-policy allkeys-lru
```

### Node.js 优化

```bash
# 增加内存限制
NODE_OPTIONS="--max-old-space-size=4096" pnpm dev:web
```

### Python 优化

```bash
# 使用 Gunicorn 多进程
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

---

## 扩展部署

### 水平扩展

```bash
# 增加服务实例
docker-compose up -d --scale web=3 --scale ai-agent-engine=3

# Kubernetes 自动扩缩容
kubectl autoscale deployment web --min=2 --max=10 --cpu-percent=70
```

### 多区域部署

```bash
# 部署到多个区域
kubectl apply -f k8s/region-us.yaml
kubectl apply -f k8s/region-eu.yaml
kubectl apply -f k8s/region-asia.yaml
```

---

## 维护操作

### 更新部署

```bash
# 滚动更新
kubectl set image deployment/web web=cozlive/web:v1.1.0

# 查看更新状态
kubectl rollout status deployment/web

# 回滚更新
kubectl rollout undo deployment/web
```

### 查看日志

```bash
# 实时日志
kubectl logs -f deployment/web

# 查看历史日志
kubectl logs deployment/web --since=24h

# 查看所有服务日志
stern cozlive
```

### 调试容器

```bash
# 进入容器
kubectl exec -it <pod-name> -- /bin/sh

# 查看资源使用
kubectl top pod
kubectl top node
```

---

## 联系支持

如有部署问题，请联系:

- **技术支持**: support@cozlive.com
- **文档**: https://docs.cozlive.com
- **社区**: https://community.cozlive.com
