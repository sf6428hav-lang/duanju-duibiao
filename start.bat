@echo off
cd /d "%~dp0"
echo ----------------------------------------------------
echo  Starting Backend Server (http://localhost:8000)...
echo ----------------------------------------------------
python -m pip install fastapi uvicorn python-docx python-multipart aiohttp -q
python -m uvicorn server:app --port 8000 --reload
pause
