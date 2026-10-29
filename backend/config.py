import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FALLBACK_DATA_DIR = DATA_DIR / "fallback"
MODELS_DIR = DATA_DIR / "models"

# Specific File Paths
MASTER_DATA_PATH = PROCESSED_DATA_DIR / "master_multivariate.csv"
FALLBACK_BASELINE_PATH = FALLBACK_DATA_DIR / "seasonal_baseline.csv"

# Geographic Defaults (Sri Lanka - Western Province / Colombo Market baseline)
DEFAULT_LATITUDE = 6.9271
DEFAULT_LONGITUDE = 79.8612
DEFAULT_LOCATION_NAME = "Pettah Wholesale Market, Colombo"

# Open-Meteo Weather API
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"

# Central Bank of Sri Lanka (CBSL) & Public Data Portal Defaults
CBSL_DATA_URL = "https://www.cbsl.gov.lk/en/statistics"
DATA_GOV_LK_URL = "https://data.gov.lk"

# Trust & Uncertainty Parameters (Section 6 & 7.3 in Proposal)
# If confidence falls below 50%, recommendations are suppressed
SAFE_CONFIDENCE_THRESHOLD = 0.50
EXTREME_RAINFALL_THRESHOLD_MM = 35.0  # mm/day precipitation threshold causing severe foot traffic drop

# Commodities tracked (Essential food staples from CBSL)
TRACKED_COMMODITIES = [
    "Samba Rice",
    "Nadu Rice",
    "Red Dhal",
    "Potatoes (Local)",
    "Big Onions (Imported)",
    "Sugar (White)",
    "Diesel (Auto)",
]
