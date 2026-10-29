Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   ModelX 2.0: Retail Micro-Liquidity Stress Forecaster Launcher" -ForegroundColor Yellow
Write-Host "   IEEE Computational Intelligence Society Student Chapter (IIT)" -ForegroundColor Cyan
Write-Host "======================================================================"
Write-Host ""

# Check python
$pythonVersion = python --version 2>&1
Write-Host "[1/3] Python Environment: $pythonVersion" -ForegroundColor Green

# Start FastAPI server in a background job or separate process
Write-Host "[2/3] Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "-m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

# Open browser
Start-Sleep -Seconds 2
Write-Host "[3/3] Launching Neumorphic Dashboard in Browser..." -ForegroundColor Green
Start-Process "http://localhost:8000/dashboard"

Write-Host ""
Write-Host "System Active!" -ForegroundColor Cyan
Write-Host "Dashboard: http://localhost:8000/dashboard" -ForegroundColor White
Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor White

