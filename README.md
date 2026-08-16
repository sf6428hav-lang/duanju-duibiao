# 短剧对标与创作工坊

包含短剧拆解分析、剧本创作、分集集纲、人物小传、智能排版与可视化预览等全套功能。

## 本地/服务器启动指南

`ash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn server:app --host 0.0.0.0 --port 8000
`

打开浏览器访问 http://localhost:8000 或 http://服务器IP:8000 即可使用。
