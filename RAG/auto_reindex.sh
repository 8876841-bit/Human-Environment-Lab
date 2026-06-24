#!/bin/bash
# RAG 自动索引更新
# 用法：./RAG/auto_reindex.sh
# Claude/Codex 在写入新文件后调用此脚本

curl -s -X POST http://127.0.0.1:8765/reindex
echo ""
