import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import requests
import pandas as pd

from backend.config import (
    OPEN_METEO_FORECAST_URL,
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE,
    RAW_DATA_DIR,
)

logger = logging.getLogger(__name__)

CACHE_DIR = RAW_DATA_DIR / "open_meteo_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_DIR / "latest_weather.json"


class WeatherClient:
    """Client for fetching live 14-day weather forecasts and historical atmospheric data

    via the Open-Meteo REST API, with disk caching and graceful offline fallback.
    """

    def __init__(self, latitude: float = DEFAULT_LATITUDE, longitude: float = DEFAULT_LONGITUDE):
        self.latitude = latitude
        self.longitude = longitude

    def fetch_14day_forecast(self, timeout_sec: int = 10) -> Dict[str, Any]:
        """Fetch 14-day precipitation, temperature, and wind speed forecast.

        Caches result to disk. Falls back to cache on network failure.
        """
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "daily": [
                "precipitation_sum",
                "precipitation_probability_max",
                "temperature_2m_max",
                "temperature_2m_min",
                "wind_speed_10m_max",
            ],
            "forecast_days": 14,
            "timezone": "Asia/Colombo",
        }

        try:
            response = requests.get(OPEN_METEO_FORECAST_URL, params=params, timeout=timeout_sec)
            response.raise_for_status()
            data = response.json()
            # Save raw cache
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Successfully fetched and cached live 14-day weather forecast.")
            return {"source": "live", "data": data}
        except Exception as e:
            logger.warning("Failed to fetch live weather forecast: %s. Falling back to local cache.", e)
            if CACHE_FILE.exists():
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                return {"source": "cache", "data": cached_data}
            else:
                # Synthetic fallback if no cache exists yet
                logger.warning("No weather cache file exists. Generating synthetic seasonal baseline weather.")
                synthetic = self._generate_synthetic_baseline()
                return {"source": "synthetic_baseline", "data": synthetic}

    def get_forecast_dataframe(self) -> pd.DataFrame:
        """Returns clean pandas DataFrame indexed by date."""
        raw_result = self.fetch_14day_forecast()
        daily = raw_result["data"].get("daily", {})
        if not daily or "time" not in daily:
            raise ValueError("Malformed weather payload.")

        df = pd.DataFrame({
            "date": pd.to_datetime(daily["time"]),
            "precipitation_sum_mm": daily.get("precipitation_sum", [0.0] * len(daily["time"])),
            "precipitation_probability_pct": daily.get("precipitation_probability_max", [0.0] * len(daily["time"])),
            "temp_max_c": daily.get("temperature_2m_max", [30.0] * len(daily["time"])),
            "temp_min_c": daily.get("temperature_2m_min", [24.0] * len(daily["time"])),
            "wind_speed_kmh": daily.get("wind_speed_10m_max", [10.0] * len(daily["time"])),
        })
        df["is_weather_cached"] = (raw_result["source"] != "live")
        return df

    def _generate_synthetic_baseline(self) -> Dict[str, Any]:
        """Generates seasonal baseline 14-day weather pattern for Western Province."""
        dates = pd.date_range(start=datetime.now(), periods=14, freq="D").strftime("%Y-%m-%d").tolist()
        return {
            "daily": {
                "time": dates,
                "precipitation_sum": [4.5, 12.0, 38.0, 42.0, 15.0, 2.0, 0.0, 0.0, 5.0, 8.0, 22.0, 31.0, 10.0, 3.0],
                "precipitation_probability_max": [40, 65, 90, 95, 70, 20, 10, 10, 30, 45, 80, 85, 50, 25],
                "temperature_2m_max": [31.0] * 14,
                "temperature_2m_min": [25.0] * 14,
                "wind_speed_10m_max": [15.0] * 14,
            }
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = WeatherClient()
    df = client.get_forecast_dataframe()
    print("Fetched 14-day weather forecast preview:")
    print(df.head(7))
