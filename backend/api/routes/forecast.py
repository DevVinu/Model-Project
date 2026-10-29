from datetime import datetime
from fastapi import APIRouter
from typing import Optional

from backend.config import DEFAULT_LOCATION_NAME
from backend.api.schemas import ForecastResponse, DailyForecastItem, TrustMetadata, RecommendationCard
from backend.ml_engine.liquidity_scorer import LiquidityStressScorer
from backend.ml_engine.trust_layer import TrustAndUncertaintyEngine
from backend.ml_engine.advisor import InventoryAdvisor

router = APIRouter(prefix="/forecast", tags=["Forecast"])

scorer = LiquidityStressScorer()
trust_engine = TrustAndUncertaintyEngine()


@router.get("/14-day", response_model=ForecastResponse)
def get_14day_forecast(
    starting_cash: float = 80000.0,
    daily_sales: float = 45000.0,
    daily_restock: float = 34000.0,
    fixed_overhead: float = 4500.0,
    order_reduction_pct: float = 0.0,
    simulate_low_confidence: bool = False,
):
    """Calculates 14-day cash-flow stress timeline, evaluates uncertainty,

    and delivers actionable inventory recommendations with safe-failure gating
    and interactive order-reduction simulation.
    """
    effective_restock = daily_restock * (1.0 - max(0.0, min(order_reduction_pct, 60.0)) / 100.0)

    timeline_raw = scorer.calculate_14day_stress(
        starting_cash_lkr=starting_cash,
        avg_daily_sales_lkr=daily_sales,
        avg_daily_restock_lkr=effective_restock,
        fixed_daily_overhead_lkr=fixed_overhead,
    )

    is_live = not simulate_low_confidence
    trust_dict = trust_engine.evaluate_forecast_trust(
        timeline=timeline_raw,
        is_weather_live=is_live,
        is_cbsl_live=is_live,
    )

    if simulate_low_confidence:
        trust_dict["confidence_score"] = 0.42
        trust_dict["confidence_percentage"] = 42
        trust_dict["is_suppressed"] = True
        trust_dict["safe_message"] = (
            "Notice: Limited wholesale price data available for selected goods. "
            "Forecast confidence is low (42%). Recommendation suppressed to prevent risk."
        )

    recommendation_dict = InventoryAdvisor.generate_recommendation(
        timeline=timeline_raw,
        trust_status=trust_dict,
    )

    # Summary metrics
    red_count = sum(1 for t in timeline_raw if t["risk_level"] == "RED")
    yellow_count = sum(1 for t in timeline_raw if t["risk_level"] == "YELLOW")
    min_cash = min(t["projected_cash_lkr"] for t in timeline_raw)

    return ForecastResponse(
        location=DEFAULT_LOCATION_NAME,
        currency="LKR",
        generated_at=datetime.now().isoformat(),
        trust=TrustMetadata(**trust_dict),
        recommendation=RecommendationCard(**recommendation_dict),
        timeline=[DailyForecastItem(**t) for t in timeline_raw],
        summary_metrics={
            "squeeze_days_count": red_count,
            "caution_days_count": yellow_count,
            "min_projected_cash_lkr": round(min_cash, 2),
            "safe_cash_buffer_retained": min_cash >= (starting_cash * 0.4),
            "simulated_order_reduction_pct": order_reduction_pct,
        },
    )
