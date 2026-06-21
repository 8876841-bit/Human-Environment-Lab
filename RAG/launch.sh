#!/bin/bash
# HEL RAG 服务启动脚本
# 用途：构建索引 + 启动检索服务（后台常驻）
# 停止：kill $(cat RAG/rag.pid)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== HEL RAG Service ==="

# 1. 先构建索引
echo ""
echo "[1/2] 构建索引..."
python3 RAG/index_builder.py --force
if [ $? -ne 0 ]; then
    echo "❌ 索引构建失败"
    exit 1
fi

# 2. 启动服务
echo ""
echo "[2/2] 启动检索服务 (127.0.0.1:8765)..."
nohup python3 RAG/server.py > RAG/rag.log 2>&1 &
PID=$!
echo $PID > RAG/rag.pid
sleep 2

# 检查是否启动成功
if kill -0 $PID 2>/dev/null; then
    echo "✅ RAG 服务已启动"
    echo "   PID: $PID"
    echo "   日志: RAG/rag.log"
    echo "   搜索: curl 'http://127.0.0.1:8765/search?q=时间有限性&top_k=3'"
    echo "   停止: kill $PID"
else
    echo "❌ 服务启动失败，查看日志: RAG/rag.log"
    exit 1
fi
