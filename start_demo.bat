@echo off
echo ======================================================================
echo    ModelX 2.0: Retail Micro-Liquidity Stress Forecaster Launcher
echo    IEEE Computational Intelligence Society Student Chapter (IIT)
echo ======================================================================
echo.
echo [1/3] Verifying Python Environment...
python --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.10+
    pause
    exit /b
)

echo.
echo [2/3] Starting FastAPI Server on port 8000...
start cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo [3/3] Opening Interactive Neumorphic Dashboard...
timeout /t 2 >nul
start http://localhost:8000/dashboard

echo.
echo ======================================================================
echo System is running at: http://localhost:8000/dashboard
echo API Documentation at: http://localhost:8000/docs
echo ======================================================================
pause

