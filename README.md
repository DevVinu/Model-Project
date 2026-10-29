# ModelX 2.0: Automated Micro-Liquidity & Cash-Flow Stress Forecaster

> **Competition:** IEEE Computational Intelligence Society Student Chapter (IIT) — Model-X 2.0  
> **Domain:** 01 — Cost of Living and Everyday Economics  
> **Team:** Vinudana Dissanayake & Stephani Fernando (NIBM)

---

## 📌 Executive Summary

Informal shopkeepers, roadside vendors, and small grocery managers operate on razor-thin week-to-week margins. When unexpected external shocks occur simultaneously—**wholesale commodity price inflation**, **fuel/transport tariff revisions**, and **heavy monsoon rains suppressing walk-in foot traffic**—retailers fall into cascading micro-liquidity traps.

**ModelX 2.0** is an end-to-end, multivariate time-series working-capital forecaster designed specifically for informal retail in developing economies (Sri Lankan wholesale market baseline). It ingests multi-source economic and atmospheric telemetry to deliver:
1. **14-Day Micro-Liquidity Stress Timeline:** Color-coded daily risk scoring (**Green** = Stable, **Yellow** = Caution, **Red** = Cash Squeeze Risk).
2. **Actionable Restocking Advice:** Quantified recommendations (e.g., *"Cut bulk restocking orders by 20% prior to Day 8 to preserve operating cash"*).
3. **Automated Trust & Safe-Failure Layer:** Quantifies forecast uncertainty and suppresses risky purchasing advice when data confidence drops below 50%.

---

## 🏛️ System Architecture

```
                    ┌────────────────────────────────────────────────────────┐
                    │                DATA INGESTION ENGINE                   │
                    │  • CBSL Weekly Wholesale Market Statistics (Pettah)    │
                    │  • Open-Meteo REST API (14-Day Precipitation Telemetry)│
                    │  • Public Transport & Fuel Tariffs (data.gov.lk)       │
                    └──────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │             ML ANALYTICS & TRUST ENGINE                │
                    │  • Preprocessor: Forward-Fill & 7-Day Smoothing        │
                    │  • Ridge Commodity Forecaster: 14-Day Wholesale Curves │
                    │  • XGBoost/Elasticity: Rainfall -> Foot-Traffic Index  │
                    │  • 14-Day Liquidity Stress Scorer (Daily Cash Flow)    │
                    │  • Safe-Failure Layer: Auto-Suppression if Conf < 50%  │
                    └──────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │               APPLICATION & UI LAYER                   │
                    │  • FastAPI REST Endpoints (/api/v1/forecast/14-day)    │
                    │  • React + Tailwind CSS Interactive Dashboard          │
                    │  • Standalone Zero-Dependency Browser Dashboard        │
                    └────────────────────────────────────────────────────────┘
```

---

## 🧪 Evaluation & Backtest Results (Section 9 Compliance)

Evaluated across historical seasonal windows (monsoon and macroeconomic price shocks):

| Metric | Measured Result | Proposal Target | Status |
| :--- | :--- | :--- | :--- |
| **Wholesale Price Forecasting MAPE** | **1.51%** | $< 8.0\%$ | ✅ **Exceeded** |
| **Liquidity Squeeze Precision** | **80.0%** | High precision | ✅ **Exceeded** |
| **Liquidity Squeeze Recall** | **90.9%** | High recall | ✅ **Exceeded** |
| **F1-Score** | **0.8511** | $> 0.80$ | ✅ **Exceeded** |
| **Safe-Failure Auto-Suppression** | **Verified Functional** | Trigger on low confidence | ✅ **Verified** |

---

## 🚀 Quickstart Guide

### 1. Prerequisites & Installation
Ensure Python 3.10+ is installed:
```powershell
# Install backend dependencies
python -m pip install -r backend/requirements.txt
```

### 2. Run the Data Pipeline (Ingestion & Preprocessing)
```powershell
python -m backend.ingestion.preprocessor
```
*Outputs: `data/processed/master_multivariate.csv` and `data/fallback/seasonal_baseline.csv`*

### 3. Run the Backtest & Evaluation Suite
```powershell
python -m evaluation.backtest_runner
```
*Outputs: `evaluation/reports/evaluation_summary.json`*

### 4. Start the FastAPI Server & Interactive Dashboard
```powershell
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
* **Interactive Dashboard:** [http://localhost:8000/dashboard](http://localhost:8000/dashboard) (or [http://localhost:8000](http://localhost:8000))
* **Swagger API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **14-Day Stress API:** [http://localhost:8000/api/v1/forecast/14-day](http://localhost:8000/api/v1/forecast/14-day)
* **Health Check API:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 📂 Repository File Structure

```
Model-Project/
├── README.md                           # Documentation & quickstart
├── backend/
│   ├── requirements.txt                # Python dependencies
│   ├── config.py                       # Coordinates, thresholds, URLs
│   ├── main.py                         # FastAPI application entrypoint
│   ├── ingestion/                      # MODULE 1: Ingestion Engine
│   │   ├── cbsl_scraper.py             # CBSL weekly prices & baseline archive
│   │   ├── weather_client.py           # Open-Meteo REST API live & cached client
│   │   ├── tariff_loader.py            # Transport tariffs & fuel price revisions
│   │   └── preprocessor.py             # Forward-fill, smoothing, baseline fallback
│   ├── ml_engine/                      # MODULE 2: ML Analytics & Trust Engine
│   │   ├── price_forecaster.py         # Ridge 14-day wholesale price forecaster
│   │   ├── traffic_forecaster.py       # Rainfall-to-foot-traffic impact model
│   │   ├── liquidity_scorer.py         # 14-day micro-liquidity cash-flow simulator
│   │   ├── trust_layer.py              # Confidence scoring & safe-failure engine
│   │   └── advisor.py                  # Plain-language actionable inventory advice
│   └── api/                            # MODULE 3: FastAPI REST Server
│       ├── schemas.py                  # Pydantic data contracts
│       └── routes/
│           ├── forecast.py             # GET /api/v1/forecast/14-day
│           ├── commodities.py          # GET /api/v1/commodities/prices
│           └── health.py               # GET /api/v1/health
├── data/
│   ├── raw/                            # CBSL history, weather cache, tariffs
│   ├── processed/                      # master_multivariate.csv (1399 daily rows)
│   └── fallback/                       # seasonal_baseline.csv (30-day moving avg)
├── evaluation/                         # SECTION 9: Evaluation Suite
│   ├── backtest_runner.py              # Seasonal rolling cross-validation
│   ├── metrics.py                      # MAPE, Precision, Recall, F1
│   └── reports/evaluation_summary.json # Verified backtest results
└── frontend/                           # MODULE 3 UI: Dashboard
    ├── dashboard.html                  # Standalone interactive browser dashboard
    ├── package.json                    # React + Vite dependencies
    ├── vite.config.js                  # Vite configuration
    ├── tailwind.config.js              # Tailwind theme configuration
    └── src/
        ├── main.jsx                    # React entrypoint
        ├── App.jsx
        ├── api/forecastApi.js          # API client with offline demo fallback
        ├── components/
        │   ├── StressCalendar14Day.jsx # 14-day color-coded calendar widget
        │   ├── SafeFailureBanner.jsx   # Dynamic safety alert banner
        │   ├── ActionCard.jsx          # Plain-language recommendation card
        │   ├── PriceWeatherChart.jsx   # Cash, rainfall, and foot-traffic breakdown
        │   └── ShopProfileSelector.jsx # Shopkeeper parameter controls
        └── pages/
            └── Dashboard.jsx           # Main shopkeeper view
```
