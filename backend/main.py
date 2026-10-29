import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.api.routes import forecast, commodities, health

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_HTML_PATH = BASE_DIR / "frontend" / "dashboard.html"

app = FastAPI(
    title="ModelX 2.0 Micro-Liquidity Stress Forecaster API",
    description="Multivariate time-series cash-flow stress forecaster for informal retailers (IEEE Model-X 2.0)",
    version="2.0.0",
)

# CORS configuration for React frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health.router, prefix="/api/v1")
app.include_router(forecast.router, prefix="/api/v1")
app.include_router(commodities.router, prefix="/api/v1")


@app.get("/")
def root():
    if DASHBOARD_HTML_PATH.exists():
        return FileResponse(DASHBOARD_HTML_PATH)
    return {
        "project": "ModelX 2.0 - Automated Micro-Liquidity & Cash-Flow Stress Forecaster",
        "documentation": "/docs",
        "health": "/api/v1/health",
        "forecast_14day": "/api/v1/forecast/14-day",
    }


@app.get("/dashboard")
def dashboard():
    return FileResponse(DASHBOARD_HTML_PATH)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
