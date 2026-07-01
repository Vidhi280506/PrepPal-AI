@echo off
title PrepPal AI
echo.
echo  =========================================
echo   PrepPal AI - Interview Prep Concierge
echo  =========================================
echo.

if not exist .env (
    echo [ERROR] .env file not found!
    echo Please copy .env.example to .env and set your GOOGLE_API_KEY
    pause & exit /b 1
)

if not exist data mkdir data

echo [1/4] Installing dependencies...
pip install -r requirements.txt -q

echo [2/4] Initializing database...
python database/seed.py

echo [3/4] Starting MCP server on port 8001...
start "PrepPal MCP" cmd /c "python -m mcp.server"
timeout /t 3 /nobreak >nul

echo [4/4] Starting FastAPI backend on port 8000...
start "PrepPal API" cmd /c "uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul

echo.
echo  Open http://localhost:8501 in your browser
echo.
streamlit run frontend/app.py --server.port 8501
