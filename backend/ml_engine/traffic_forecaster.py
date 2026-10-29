import logging
from typing import Dict, Any, List
import numpy as np
import pandas as pd

from backend.ingestion.weather_client import WeatherClient

logger = logging.getLogger(__name__)


class FootTrafficForecaster:
    """Estimates hyper-local retail foot-traffic reduction indices based on

    meteorological precipitation intensity, rain probability, and wind velocity.
    """

    def __init__(self, weather_client: WeatherClient = None):
        self.weather_client = weather_client or WeatherClient()

    def predict_foot_traffic_reduction(self) -> pd.DataFrame:
        """Projects 14-day daily foot traffic multiplier and qualitative risk status.

        1.00 = Normal 100% foot-traffic.
        0.35 = 65% drop due to severe localized flooding/downpour.
        """
        weather_df = self.weather_client.get_forecast_dataframe()

        traffic_multipliers = []
        reduction_percentages = []
        traffic_status = []

        for _, row in weather_df.iterrows():
            rain_mm = float(row["precipitation_sum_mm"])
            prob_pct = float(row["precipitation_probability_pct"])
            wind_kmh = float(row.get("wind_speed_kmh", 10.0))

            # Base elasticity calculation
            # Expected rain impact weighted by precipitation probability
            effective_rain = rain_mm * (prob_pct / 100.0)

            if effective_rain < 3.0:
                mult = 1.0 - (effective_rain * 0.02)
                status = "Normal Traffic"
            elif effective_rain < 12.0:
                mult = 0.94 - ((effective_rain - 3.0) * 0.015)
                status = "Slight Foot Traffic Dip"
            elif effective_rain < 28.0:
                mult = 0.80 - ((effective_rain - 12.0) * 0.018)
                status = "Moderate Rain Disruption"
            else:
                # Severe downpour / waterlogging
                mult = max(0.25, 0.50 - ((effective_rain - 28.0) * 0.01))
                status = "Severe Foot Traffic Slump"

            # High wind penalty (> 25 km/h)
            if wind_kmh > 25.0:
                mult = max(0.20, mult - 0.08)

            mult = round(float(np.clip(mult, 0.20, 1.00)), 2)
            drop_pct = round((1.0 - mult) * 100.0, 1)

            traffic_multipliers.append(mult)
            reduction_percentages.append(drop_pct)
            traffic_status.append(status)

        result_df = weather_df.copy()
        result_df["foot_traffic_multiplier"] = traffic_multipliers
        result_df["foot_traffic_reduction_pct"] = reduction_percentages
        result_df["weather_disruption_level"] = traffic_status

        return result_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    forecaster = FootTrafficForecaster()
    df = forecaster.predict_foot_traffic_reduction()
    print("14-Day Foot Traffic Projections:")
    print(df[["date", "precipitation_sum_mm", "foot_traffic_multiplier", "foot_traffic_reduction_pct", "weather_disruption_level"]].head(7))
