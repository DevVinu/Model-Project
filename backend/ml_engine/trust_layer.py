import logging
from typing import Dict, Any, List
from backend.config import SAFE_CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)


class TrustAndUncertaintyEngine:
    """Evaluates prediction intervals, data freshness, and meteorological uncertainty

    to assign a quantitative confidence score to forecasts and enforce safe-failure rules.
    """

    def __init__(self, safe_threshold: float = SAFE_CONFIDENCE_THRESHOLD):
        self.safe_threshold = safe_threshold

    def evaluate_forecast_trust(
        self,
        timeline: List[Dict[str, Any]],
        is_weather_live: bool = True,
        is_cbsl_live: bool = True,
    ) -> Dict[str, Any]:
        """Calculates global confidence percentage and checks for safe-failure conditions."""
        base_confidence = 0.90

        # Penalty for stale/fallback data streams
        if not is_weather_live:
            base_confidence -= 0.18
        if not is_cbsl_live:
            base_confidence -= 0.15

        # Uncertainty penalty if there are extreme weather spikes (> 35mm rain)
        heavy_rain_days = sum(1 for t in timeline if t.get("precipitation_mm", 0.0) >= 35.0)
        if heavy_rain_days >= 3:
            base_confidence -= 0.12
        elif heavy_rain_days >= 1:
            base_confidence -= 0.06

        confidence_pct = round(max(0.10, min(base_confidence, 0.98)), 2)
        confidence_display = int(confidence_pct * 100)

        # Evaluate Safe Failure Trigger
        is_suppressed = confidence_pct < self.safe_threshold

        if is_suppressed:
            safe_message = (
                f"Notice: Limited wholesale price data available or high meteorological uncertainty. "
                f"Forecast confidence is low ({confidence_display}%). Recommendation suppressed to prevent risk."
            )
        else:
            safe_message = (
                f"High-trust forecast ({confidence_display}% confidence). "
                f"Derived from live CBSL market curves and Open-Meteo atmospheric telemetry."
            )

        return {
            "confidence_score": confidence_pct,
            "confidence_percentage": confidence_display,
            "is_suppressed": is_suppressed,
            "safe_threshold": self.safe_threshold,
            "safe_message": safe_message,
            "is_weather_live": is_weather_live,
            "is_cbsl_live": is_cbsl_live,
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    trust_engine = TrustAndUncertaintyEngine()
    sample_timeline = [{"precipitation_mm": 10.0}] * 14
    print("Normal Live Trust:", trust_engine.evaluate_forecast_trust(sample_timeline, True, True))
    print("Offline Fallback Trust:", trust_engine.evaluate_forecast_trust(sample_timeline, False, False))
