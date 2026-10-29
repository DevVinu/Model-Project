from fastapi import APIRouter
from typing import List

from backend.api.schemas import CommodityForecastSeries
from backend.ml_engine.price_forecaster import CommodityPriceForecaster

router = APIRouter(prefix="/commodities", tags=["Commodities"])

forecaster = CommodityPriceForecaster()


@router.get("/prices", response_model=List[CommodityForecastSeries])
def get_commodity_price_forecasts():
    """Returns 14-day wholesale price forecasts with 95% confidence intervals

    for essential Sri Lankan commodities (Samba Rice, Nadu Rice, Dhal, etc.).
    """
    forecasts = forecaster.forecast_14_days()
    display_names = {
        "price_samba_rice": "Samba Rice (LKR/kg)",
        "price_nadu_rice": "Nadu Rice (LKR/kg)",
        "price_red_dhal": "Red Dhal (LKR/kg)",
        "price_potatoes_local": "Potatoes Local (LKR/kg)",
        "price_big_onions_imported": "Big Onions Imported (LKR/kg)",
        "price_sugar_white": "White Sugar (LKR/kg)",
    }

    result = []
    for key, data in forecasts.items():
        result.append(
            CommodityForecastSeries(
                commodity_key=key,
                display_name=display_names.get(key, key.replace("price_", "").replace("_", " ").title()),
                dates=data["dates"],
                predictions=data["predictions"],
                lower_bound_95=data["lower_bound_95"],
                upper_bound_95=data["upper_bound_95"],
                expected_change_pct=data["expected_change_pct"],
            )
        )
    return result
