#!/bin/bash

# Cozlive 开发环境停止脚本

echo "🛑 停止 Cozlive 开发环境..."

# 颜色定义
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# 如果存在 PID 文件，读取并停止
if [ -f logs/all.pids ]; then
    PIDS=$(cat logs/all.pids)
    for PID in $PIDS; do
        if kill -0 $PID 2>/dev/null; then
            echo -e "${YELLOW}  - 停止进程 $PID${NC}"
            kill $PID 2>/dev/null
        fi
    done
    rm logs/all.pids
fi

# 停止特定服务
SERVICES="postgres redis mongodb user-service ai-engine web"

for SERVICE in $SERVICES; do
    PID_FILE="logs/${SERVICE}.pid"
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo -e "${YELLOW}  - 停止 $SERVICE (PID: $PID)${NC}"
            kill $PID 2>/dev/null
        fi
        rm "$PID_FILE"
    fi
done

echo -e "${GREEN}✅ 所有服务已停止${NC}"

# 清理日志
read -p "是否清理日志文件? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf logs/*.log
    echo "🗑️  日志文件已清理"
fi
