from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DailyForecastItem(BaseModel):
    day_index: int = Field(..., description="Day 1 to 14 in the forecast horizon")
    date: str = Field(..., description="YYYY-MM-DD")
    projected_cash_lkr: float
    daily_revenue_lkr: float
    daily_outflow_lkr: float
    precipitation_mm: float
    foot_traffic_multiplier: float
    wholesale_cost_multiplier: float
    stress_score: int = Field(..., ge=0, le=100, description="0=Stable, 100=Severe stress")
    risk_level: str = Field(..., description="GREEN, YELLOW, or RED")
    status_description: str


class TrustMetadata(BaseModel):
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    confidence_percentage: int = Field(..., ge=0, le=100)
    is_suppressed: bool
    safe_threshold: float
    safe_message: str
    is_weather_live: bool
    is_cbsl_live: bool


class RecommendationCard(BaseModel):
    action_type: str
    headline: str
    detail: str
    recommended_order_adjustment_pct: int
    urgency: str
    suggested_actions: List[str]


class ForecastResponse(BaseModel):
    location: str
    currency: str = "LKR"
    generated_at: str
    trust: TrustMetadata
    recommendation: RecommendationCard
    timeline: List[DailyForecastItem]
    summary_metrics: Dict[str, Any]


class CommodityForecastSeries(BaseModel):
    commodity_key: str
    display_name: str
    dates: List[str]
    predictions: List[float]
    lower_bound_95: List[float]
    upper_bound_95: List[float]
    expected_change_pct: float


class HealthResponse(BaseModel):
    status: str
    version: str = "2.0.0"
    mode: str = "LIVE"
    timestamp: str
    cbsl_data_status: str
    weather_data_status: str
