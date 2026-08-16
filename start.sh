#!/bin/bash
cd "$(dirname "$0")"
echo "📦 检查依赖..."
python -m pip install fastapi uvicorn python-docx python-multipart aiohttp -q
echo "🚀 启动后端服务 -> http://localhost:8000"
python -m uvicorn server:app --port 8000 --reload
