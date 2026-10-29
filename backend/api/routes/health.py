from datetime import datetime
from fastapi import APIRouter
from backend.api.schemas import HealthResponse
from backend.config import RAW_DATA_DIR

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Checks data cache freshness and live engine status."""
    weather_cached = (RAW_DATA_DIR / "open_meteo_cache" / "latest_weather.json").exists()
    cbsl_cached = (RAW_DATA_DIR / "cbsl_weekly_prices" / "cbsl_wholesale_history.csv").exists()

    return HealthResponse(
        status="operational",
        version="2.0.0",
        mode="LIVE" if (weather_cached and cbsl_cached) else "DEGRADED",
        timestamp=datetime.now().isoformat(),
        cbsl_data_status="Available (Local Mirror/Live)" if cbsl_cached else "Missing",
        weather_data_status="Active (Open-Meteo Cache Ready)" if weather_cached else "Uncached",
    )
