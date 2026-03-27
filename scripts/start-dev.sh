#!/bin/bash

# Cozlive 开发环境启动脚本
# 用于在没有 Docker 的环境下启动模拟服务进行测试

set -e

echo "🚀 启动 Cozlive 开发环境..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 创建日志目录
mkdir -p logs

echo -e "${BLUE}📦 启动模拟基础设施服务...${NC}"

# 启动模拟 PostgreSQL 服务
echo -e "${YELLOW}  - 启动模拟 PostgreSQL (端口: 5432)${NC}"
python3 scripts/mock-services/mock-postgres.py > logs/postgres.log 2>&1 &
POSTGRES_PID=$!
echo $POSTGRES_PID > logs/postgres.pid

# 启动模拟 Redis 服务
echo -e "${YELLOW}  - 启动模拟 Redis (端口: 6379)${NC}"
python3 scripts/mock-services/mock-redis.py > logs/redis.log 2>&1 &
REDIS_PID=$!
echo $REDIS_PID > logs/redis.pid

# 启动模拟 MongoDB 服务
echo -e "${YELLOW}  - 启动模拟 MongoDB (端口: 27017)${NC}"
python3 scripts/mock-services/mock-mongodb.py > logs/mongodb.log 2>&1 &
MONGODB_PID=$!
echo $MONGODB_PID > logs/mongodb.pid

echo -e "${BLUE}🔧 启动后端服务...${NC}"

# 启动用户服务
echo -e "${YELLOW}  - 启动用户服务 (端口: 3001)${NC}"
python3 scripts/mock-services/mock-user-service.py > logs/user-service.log 2>&1 &
USER_SERVICE_PID=$!
echo $USER_SERVICE_PID > logs/user-service.pid

# 启动 AI Agent 引擎
echo -e "${YELLOW}  - 启动 AI Agent 引擎 (端口: 8000)${NC}"
python3 scripts/mock-services/mock-ai-engine.py > logs/ai-engine.log 2>&1 &
AI_ENGINE_PID=$!
echo $AI_ENGINE_PID > logs/ai-engine.pid

echo -e "${BLUE}🎨 启动前端应用...${NC}"

# 启动 Web 应用
echo -e "${YELLOW}  - 启动 Web 应用 (端口: 3000)${NC}"
cd apps/web && npm run dev > ../../logs/web.log 2>&1 &
WEB_PID=$!
echo $WEB_PID > ../../logs/web.pid
cd ../..

echo ""
echo -e "${GREEN}✅ Cozlive 服务已启动!${NC}"
echo ""
echo "📋 服务状态:"
echo "  - Web 应用:     http://localhost:3000"
echo "  - 用户服务:     http://localhost:3001"
echo "  - AI 引擎:      http://localhost:8000"
echo "  - 模拟 PostgreSQL:  端口 5432"
echo "  - 模拟 Redis:       端口 6379"
echo "  - 模拟 MongoDB:     端口 27017"
echo ""
echo "📁 日志文件:"
echo "  - logs/postgres.log"
echo "  - logs/redis.log"
echo "  - logs/mongodb.log"
echo "  - logs/user-service.log"
echo "  - logs/ai-engine.log"
echo "  - logs/web.log"
echo ""
echo "🛑 停止服务: ./scripts/stop-dev.sh"
echo ""

# 保存所有 PID
echo "$POSTGRES_PID $REDIS_PID $MONGODB_PID $USER_SERVICE_PID $AI_ENGINE_PID $WEB_PID" > logs/all.pids
