import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class InventoryAdvisor:
    """Translates multivariate mathematical stress projections into clear,

    actionable inventory advice for small shopkeepers.
    """

    @staticmethod
    def generate_recommendation(
        timeline: List[Dict[str, Any]],
        trust_status: Dict[str, Any],
        price_forecasts: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Produces primary recommendation card text and actionable steps."""
        if trust_status.get("is_suppressed", False):
            return {
                "action_type": "SUPPRESSED",
                "headline": "Recommendation Suppressed (Safe-Failure Mode)",
                "detail": trust_status.get("safe_message"),
                "recommended_order_adjustment_pct": 0,
                "urgency": "LOW",
                "suggested_actions": [
                    "Rely on conservative historical inventory moving averages.",
                    "Avoid speculative bulk orders until market feeds re-stabilize.",
                    "Check back once live wholesale pricing updates are restored.",
                ],
            }

        # Find earliest squeeze day
        squeeze_days = [t for t in timeline if t.get("risk_level") == "RED"]
        caution_days = [t for t in timeline if t.get("risk_level") == "YELLOW"]

        if squeeze_days:
            first_squeeze = squeeze_days[0]
            day_idx = first_squeeze["day_index"]
            date_str = first_squeeze["date"]
            rain_mm = first_squeeze["precipitation_mm"]
            projected_cash = first_squeeze["projected_cash_lkr"]

            headline = f"Cash Squeeze Expected in {day_idx} Days ({date_str})"
            detail = (
                f"Severe micro-liquidity risk detected. Anticipated rainfall of {rain_mm:.1f}mm will suppress walk-in "
                f"customer revenue, while rising wholesale restocking requirements risk depleting working capital down to "
                f"LKR {projected_cash:,.0f}. Cut orders by 20% to 25% this week to protect your operating reserves."
            )
            adj_pct = -20
            urgency = "HIGH"
            suggested_actions = [
                f"Cut bulk non-perishable restocking orders by 20% prior to {date_str}.",
                f"Avoid supplier credit purchases with short repayment terms during Day {day_idx-2} to Day {day_idx+2}.",
                "Prioritize high-turnover staples (Rice, Dhal) and delay secondary inventory restocks.",
            ]
        elif caution_days:
            first_caution = caution_days[0]
            day_idx = first_caution["day_index"]
            date_str = first_caution["date"]

            headline = f"Moderate Working-Capital Pressure in {day_idx} Days ({date_str})"
            detail = (
                f"Mild liquidity pressure anticipated due to moderate wholesale price revisions. "
                f"Maintain tight cash tracking and review purchase orders."
            )
            adj_pct = -10
            urgency = "MEDIUM"
            suggested_actions = [
                "Trim inventory reorders by 10% on slower-moving goods.",
                "Verify live wholesale market rates at Pettah before placing large bulk commitments.",
            ]
        else:
            headline = "Liquidity Stable Over Next 14 Days"
            detail = (
                "Cash inflows and projected foot traffic remain balanced against expected wholesale commodity costs. "
                "Operating capital is projected to remain healthy across the 14-day forecast window."
            )
            adj_pct = 0
            urgency = "LOW"
            suggested_actions = [
                "Proceed with regular weekly inventory restocking schedule.",
                "Take advantage of stable wholesale prices on Samba and Nadu rice.",
            ]

        return {
            "action_type": urgency,
            "headline": headline,
            "detail": detail,
            "recommended_order_adjustment_pct": adj_pct,
            "urgency": urgency,
            "suggested_actions": suggested_actions,
        }
