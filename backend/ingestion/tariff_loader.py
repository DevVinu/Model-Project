import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd

from backend.config import RAW_DATA_DIR

logger = logging.getLogger(__name__)

TARIFF_DIR = RAW_DATA_DIR / "transport_tariffs"
TARIFF_DIR.mkdir(parents=True, exist_ok=True)
TARIFF_CACHE_FILE = TARIFF_DIR / "fuel_tariff_history.csv"


class TariffLoader:
    """Ingests and structures Sri Lanka public utilities, fuel revisions,

    and freight/transport tariff schedules.
    """

    def __init__(self):
        self._ensure_seed_tariff_history()

    def _ensure_seed_tariff_history(self):
        """Seeds historical monthly fuel and freight revisions if no local file exists."""
        if not TARIFF_CACHE_FILE.exists():
            records = [
                {"effective_date": "2024-01-01", "diesel_auto_lkr": 358.0, "petrol_92_lkr": 368.0, "freight_cost_multiplier": 1.00},
                {"effective_date": "2024-04-01", "diesel_auto_lkr": 340.0, "petrol_92_lkr": 371.0, "freight_cost_multiplier": 0.98},
                {"effective_date": "2024-07-01", "diesel_auto_lkr": 328.0, "petrol_92_lkr": 344.0, "freight_cost_multiplier": 0.95},
                {"effective_date": "2024-10-01", "diesel_auto_lkr": 283.0, "petrol_92_lkr": 311.0, "freight_cost_multiplier": 0.90},
                {"effective_date": "2025-01-01", "diesel_auto_lkr": 295.0, "petrol_92_lkr": 325.0, "freight_cost_multiplier": 0.92},
                {"effective_date": "2025-06-01", "diesel_auto_lkr": 310.0, "petrol_92_lkr": 335.0, "freight_cost_multiplier": 0.94},
                {"effective_date": "2025-12-01", "diesel_auto_lkr": 315.0, "petrol_92_lkr": 340.0, "freight_cost_multiplier": 0.95},
                {"effective_date": "2026-01-01", "diesel_auto_lkr": 320.0, "petrol_92_lkr": 345.0, "freight_cost_multiplier": 0.96},
                {"effective_date": "2026-05-01", "diesel_auto_lkr": 325.0, "petrol_92_lkr": 350.0, "freight_cost_multiplier": 0.97},
                {"effective_date": "2026-10-01", "diesel_auto_lkr": 330.0, "petrol_92_lkr": 355.0, "freight_cost_multiplier": 0.98},
            ]
            df = pd.DataFrame(records)
            df.to_csv(TARIFF_CACHE_FILE, index=False)
            logger.info("Created seed fuel and transport tariff schedule at %s", TARIFF_CACHE_FILE)

    def get_tariff_history(self) -> pd.DataFrame:
        df = pd.read_csv(TARIFF_CACHE_FILE)
        df["effective_date"] = pd.to_datetime(df["effective_date"])
        df = df.sort_values("effective_date").reset_index(drop=True)
        return df

    def get_current_freight_multiplier(self) -> float:
        """Returns the most recent freight cost multiplier relative to base."""
        df = self.get_tariff_history()
        return float(df.iloc[-1]["freight_cost_multiplier"])

    def get_current_diesel_price(self) -> float:
        df = self.get_tariff_history()
        return float(df.iloc[-1]["diesel_auto_lkr"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loader = TariffLoader()
    print("Latest Diesel (Auto) Price: LKR", loader.get_current_diesel_price())
    print("Current Freight Multiplier:", loader.get_current_freight_multiplier())
