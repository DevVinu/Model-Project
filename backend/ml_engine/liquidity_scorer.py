import logging
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from backend.ml_engine.price_forecaster import CommodityPriceForecaster
from backend.ml_engine.traffic_forecaster import FootTrafficForecaster

logger = logging.getLogger(__name__)


class LiquidityStressScorer:
    """Computes a 14-day micro-liquidity stress forecast by simulating

    a small retailer's daily operating cash reserves against incoming foot-traffic
    sales revenue and outgoing wholesale restocking costs.
    """

    def __init__(
        self,
        price_forecaster: Optional[CommodityPriceForecaster] = None,
        traffic_forecaster: Optional[FootTrafficForecaster] = None,
    ):
        self.price_forecaster = price_forecaster or CommodityPriceForecaster()
        self.traffic_forecaster = traffic_forecaster or FootTrafficForecaster()

    def calculate_14day_stress(
        self,
        starting_cash_lkr: float = 80000.0,
        avg_daily_sales_lkr: float = 45000.0,
        avg_daily_restock_lkr: float = 34000.0,
        fixed_daily_overhead_lkr: float = 4500.0,
    ) -> List[Dict[str, Any]]:
        """Simulates 14-day daily cash reserves and returns day-by-day stress indicators."""
        # 1. Fetch forecasts
        price_forecasts = self.price_forecaster.forecast_14_days()
        traffic_df = self.traffic_forecaster.predict_foot_traffic_reduction()

        # Compute aggregate wholesale inflation multiplier across commodities
        daily_price_inflation = [0.0] * 14
        commodity_count = len(price_forecasts)

        if commodity_count > 0:
            for c_data in price_forecasts.values():
                base_p = c_data["predictions"][0]
                for day_idx in range(14):
                    p_day = c_data["predictions"][day_idx]
                    daily_price_inflation[day_idx] += (p_day / base_p) / commodity_count
        else:
            daily_price_inflation = [1.0] * 14

        timeline = []
        running_cash = starting_cash_lkr
        min_safe_reserve = starting_cash_lkr * 0.40  # 40% threshold for critical restock buffer

        for day_idx in range(14):
            row = traffic_df.iloc[day_idx]
            date_str = pd.to_datetime(row["date"]).strftime("%Y-%m-%d")
            rain_mm = float(row["precipitation_sum_mm"])
            traffic_mult = float(row["foot_traffic_multiplier"])
            wholesale_mult = float(daily_price_inflation[day_idx])

            # Inflows & Outflows
            daily_revenue = avg_daily_sales_lkr * traffic_mult
            daily_restock_cost = avg_daily_restock_lkr * wholesale_mult
            daily_outflow = daily_restock_cost + fixed_daily_overhead_lkr

            net_change = daily_revenue - daily_outflow
            running_cash += net_change

            # Compute Stress Score (0 - 100)
            # Higher score = greater liquidity stress
            if running_cash >= starting_cash_lkr:
                stress_score = max(5, int(25 * (1.0 - (traffic_mult - 0.7))))
            elif running_cash > min_safe_reserve:
                cash_deficit_ratio = (starting_cash_lkr - running_cash) / (starting_cash_lkr - min_safe_reserve)
                stress_score = int(35 + (cash_deficit_ratio * 30))
            else:
                critical_deficit = max(0, min_safe_reserve - running_cash) / min_safe_reserve
                stress_score = min(100, int(66 + (critical_deficit * 34)))

            # Risk Category
            if stress_score <= 35:
                risk_level = "GREEN"
                status_desc = "Stable liquidity expected"
            elif stress_score <= 65:
                risk_level = "YELLOW"
                status_desc = "Moderate cash pressure; monitor inventory"
            else:
                risk_level = "RED"
                status_desc = "Severe liquidity squeeze expected"

            timeline.append({
                "day_index": day_idx + 1,
                "date": date_str,
                "projected_cash_lkr": round(running_cash, 2),
                "daily_revenue_lkr": round(daily_revenue, 2),
                "daily_outflow_lkr": round(daily_outflow, 2),
                "precipitation_mm": rain_mm,
                "foot_traffic_multiplier": traffic_mult,
                "wholesale_cost_multiplier": round(wholesale_mult, 3),
                "stress_score": stress_score,
                "risk_level": risk_level,
                "status_description": status_desc,
            })

        return timeline


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scorer = LiquidityStressScorer()
    timeline = scorer.calculate_14day_stress()
    print("14-Day Micro-Liquidity Stress Timeline Preview:")
    for t in timeline[:7]:
        print(f"Day {t['day_index']} ({t['date']}): Score={t['stress_score']} [{t['risk_level']}] Cash=LKR {t['projected_cash_lkr']:,.0f} Rain={t['precipitation_mm']}mm")
