# ModelX 2.0: Automated Micro-Liquidity & Cash-Flow Stress Forecaster

> **Competition:** IEEE Computational Intelligence Society Student Chapter (IIT) — Model-X 2.0  
> **Domain:** 01 — Cost of Living and Everyday Economics  
> **Team:** Vinudana Dissanayake & Stephani Fernando (NIBM)

---

## 📌 Executive Summary

Informal shopkeepers, roadside vendors, and small grocery managers in developing cities operate on razor-thin week-to-week margins. When external shocks hit simultaneously—**wholesale commodity price inflation**, **fuel/transport tariff revisions**, and **heavy monsoon rains cutting walk-in customer foot traffic**—retailers fall into cascading micro-liquidity traps.

**ModelX 2.0** is an end-to-end, multivariate time-series working-capital forecaster designed specifically for informal retail (Sri Lankan wholesale market baseline). It ingests multi-source economic and atmospheric telemetry to deliver:
1. **14-Day Micro-Liquidity Stress Timeline:** Color-coded daily risk scoring (**Green** = Stable, **Yellow** = Caution, **Red** = Cash Squeeze Risk).
2. **Dual-Axis Interactive Forecast Curves:** Visualizes daily cash reserves vs. the 40% safe capital buffer line, overlayed with daily precipitation (mm).
3. **Interactive "What-If" Restocking Slider:** Allows vendors to test order cuts (0% to 35%) and observe real-time cash squeeze resolution.
4. **Trilingual Localization (English, සිංහල, தமிழ்):** Tailored for local Sri Lankan informal retailers.
5. **Explainable AI (XAI) Attribution:** Breaks down why a squeeze was triggered (monsoon rainfall footfall slump vs. wholesale rice price jumps).
6. **Automated Safe-Failure Layer:** Suppresses risky purchasing advice when data confidence drops below 50%.

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
                    │  • Foot-Traffic Impact Model: Rainfall -> Walk-in Drop │
                    │  • 14-Day Liquidity Stress Scorer (Daily Cash Flow)    │
                    │  • Safe-Failure Layer: Auto-Suppression if Conf < 50%  │
                    │  • Trilingual Advisory: English / Sinhala / Tamil      │
                    └──────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
                    ┌────────────────────────────────────────────────────────┐
                    │               APPLICATION & UI LAYER                   │
                    │  • FastAPI REST Endpoints (/api/v1/forecast/14-day)    │
                    │  • React + Tailwind CSS Neumorphic (Soft UI) Dashboard │
                    │  • Interactive Light (White/Black) & Dark Theme Modes  │
                    │  • Dual-Axis Cash vs. Rain SVG Curves                  │
                    │  • Interactive "What-If" Restocking Adjustment Slider  │
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

## 🚀 Quickstart & 1-Click Launch

### Option A: 1-Click Launcher (Windows)
Double-click [start_demo.bat](file:///c:/project/Model-Project/start_demo.bat) (or run `./run_demo.ps1` in PowerShell). This automatically starts the backend and opens the dashboard in your default browser.

### Option B: Manual Startup
```powershell
# 1. Start the FastAPI server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 2. Open in browser
# Dashboard: http://localhost:8000/dashboard (or http://localhost:8000)
# API Docs:  http://localhost:8000/docs
```

---

## 📂 Repository File Structure

```
Model-Project/
├── start_demo.bat                      # 1-Click Windows demo launcher
├── run_demo.ps1                        # 1-Click PowerShell launcher
├── README.md                           # Documentation & evaluation summary
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
│   │   └── advisor.py                  # Trilingual advice generator (EN, SI, TA)
│   └── api/                            # MODULE 3: FastAPI REST Server
│       ├── schemas.py                  # Pydantic data contracts
│       └── routes/
│           ├── forecast.py             # GET /api/v1/forecast/14-day (with What-If)
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
    ├── dashboard.html                  # Neumorphic browser dashboard (standalone)
    ├── package.json                    # React + Vite dependencies
    ├── vite.config.js                  # Vite configuration
    ├── tailwind.config.js              # Neumorphic Tailwind theme configuration
    └── src/
        ├── main.jsx                    # React entrypoint
        ├── App.jsx
        ├── index.css                   # Neumorphic soft-shadow utility classes
        ├── api/forecastApi.js          # API client with offline demo fallback
        ├── components/
        │   ├── StressCalendar14Day.jsx # 14-day color-coded calendar widget
        │   ├── SafeFailureBanner.jsx   # Dynamic safety alert banner
        │   ├── ActionCard.jsx          # Trilingual advice card with XAI attribution
        │   ├── PriceWeatherChart.jsx   # Dual-axis SVG curve (Cash vs. Rain vs. Safe line)
        │   └── ShopProfileSelector.jsx # Shopkeeper controls + What-If Slider
        └── pages/
            └── Dashboard.jsx           # Main shopkeeper view with theme/lang toggle
```
