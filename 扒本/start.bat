@echo off
chcp 65001 >nul
title VideoScript Backend
echo ========================================================
echo 视频转剧本 FastAPI 本地代理后端服务启动中...
echo 服务地址: http://localhost:8080
echo 功能说明: 解决前端 CORS 跨域拦截与大视频 FFmpeg 音画切片
echo ========================================================
python main.py
pause
