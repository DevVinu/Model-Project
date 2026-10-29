import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from backend.config import MASTER_DATA_PATH, FALLBACK_BASELINE_PATH

logger = logging.getLogger(__name__)


class CommodityPriceForecaster:
    """Multivariate time-series forecaster for essential commodity wholesale prices

    in Sri Lankan wholesale markets. Uses Ridge Regression with lag features,
    rolling-average momentum, and fuel tariff elasticity to project 14-day curves.
    """

    def __init__(self, data_path: str = str(MASTER_DATA_PATH)):
        self.data_path = data_path
        self.models: Dict[str, Ridge] = {}
        self.feature_cols: Dict[str, List[str]] = {}
        self.std_errors: Dict[str, float] = {}

    def _prepare_features(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Engineers lag terms, momentum, day-of-week, and diesel elasticity."""
        df_feat = pd.DataFrame(index=df.index)
        y = df[target_col]

        # Lags
        df_feat["lag_1"] = y.shift(1)
        df_feat["lag_7"] = y.shift(7)
        df_feat["lag_14"] = y.shift(14)

        # Rolling statistics
        df_feat["roll_mean_7"] = y.shift(1).rolling(7, min_periods=1).mean()
        df_feat["roll_std_7"] = y.shift(1).rolling(7, min_periods=1).std().fillna(0)

        # Exogenous macro indicators (Diesel tariff)
        if "diesel_auto_lkr" in df.columns:
            df_feat["diesel_price"] = df["diesel_auto_lkr"].shift(1)
        if "freight_cost_multiplier" in df.columns:
            df_feat["freight_multiplier"] = df["freight_cost_multiplier"].shift(1)

        # Temporal signals
        df_feat["day_of_week"] = df["date"].dt.dayofweek
        df_feat["month"] = df["date"].dt.month

        # Drop NaNs from shifts
        valid_mask = ~df_feat.isna().any(axis=1)
        return df_feat[valid_mask], y[valid_mask]

    def train_models(self):
        """Trains Ridge regression models for all tracked commodities."""
        df = pd.read_csv(self.data_path)
        df["date"] = pd.to_datetime(df["date"])

        price_cols = [c for c in df.columns if c.startswith("price_") and not c.endswith("_smooth_7d")]
        logger.info("Training price forecasting models for %d commodities...", len(price_cols))

        for col in price_cols:
            X, y = self._prepare_features(df, col)
            if len(X) < 30:
                continue
            model = Ridge(alpha=1.0)
            model.fit(X, y)
            preds = model.predict(X)
            residual_std = float(np.std(y - preds))

            self.models[col] = model
            self.feature_cols[col] = list(X.columns)
            self.std_errors[col] = max(residual_std, 1.5)

        logger.info("Completed model training. Trained: %s", list(self.models.keys()))

    def forecast_14_days(self) -> Dict[str, Any]:
        """Produces 14-day forecasts with 95% confidence intervals for each commodity."""
        if not self.models:
            self.train_models()

        df = pd.read_csv(self.data_path)
        df["date"] = pd.to_datetime(df["date"])
        last_date = df["date"].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, 15)]

        forecasts = {}

        for col, model in self.models.items():
            recent_vals = df[col].tail(30).tolist()
            std_err = self.std_errors[col]
            preds = []
            lower_bounds = []
            upper_bounds = []

            # Step-by-step autoregressive 14-day projection
            for i in range(14):
                curr_date = future_dates[i]
                lag_1 = recent_vals[-1]
                lag_7 = recent_vals[-7] if len(recent_vals) >= 7 else recent_vals[0]
                lag_14 = recent_vals[-14] if len(recent_vals) >= 14 else recent_vals[0]
                roll_mean_7 = float(np.mean(recent_vals[-7:]))
                roll_std_7 = float(np.std(recent_vals[-7:]))
                diesel = float(df["diesel_auto_lkr"].iloc[-1])
                freight = float(df["freight_cost_multiplier"].iloc[-1])

                feat_dict = {
                    "lag_1": lag_1,
                    "lag_7": lag_7,
                    "lag_14": lag_14,
                    "roll_mean_7": roll_mean_7,
                    "roll_std_7": roll_std_7,
                    "diesel_price": diesel,
                    "freight_multiplier": freight,
                    "day_of_week": curr_date.dayofweek,
                    "month": curr_date.month,
                }
                X_step = pd.DataFrame([feat_dict])[self.feature_cols[col]]
                pred_val = float(model.predict(X_step)[0])

                # Accumulate uncertainty over projection horizon
                horizon_penalty = 1.0 + (i * 0.05)
                conf_margin = 1.96 * std_err * horizon_penalty

                preds.append(round(pred_val, 2))
                lower_bounds.append(round(max(pred_val - conf_margin, 0), 2))
                upper_bounds.append(round(pred_val + conf_margin, 2))
                recent_vals.append(pred_val)

            forecasts[col] = {
                "commodity_key": col,
                "dates": [d.strftime("%Y-%m-%d") for d in future_dates],
                "predictions": preds,
                "lower_bound_95": lower_bounds,
                "upper_bound_95": upper_bounds,
                "expected_change_pct": round(((preds[-1] - preds[0]) / preds[0]) * 100, 2),
            }

        return forecasts


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    forecaster = CommodityPriceForecaster()
    forecaster.train_models()
    res = forecaster.forecast_14_days()
    sample_key = list(res.keys())[0]
    print(f"Sample 14-day projection for {sample_key}:")
    print("Dates:", res[sample_key]["dates"][:5])
    print("Predicted LKR/kg:", res[sample_key]["predictions"][:5])
    print("Upper 95% Bound:", res[sample_key]["upper_bound_95"][:5])
    print("Expected Change %:", res[sample_key]["expected_change_pct"])
