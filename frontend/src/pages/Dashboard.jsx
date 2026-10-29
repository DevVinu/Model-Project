import React, { useState, useEffect } from "react";
import { fetch14DayForecast } from "../api/forecastApi";
import SafeFailureBanner from "../components/SafeFailureBanner";
import ActionCard from "../components/ActionCard";
import StressCalendar14Day from "../components/StressCalendar14Day";
import PriceWeatherChart from "../components/PriceWeatherChart";
import ShopProfileSelector from "../components/ShopProfileSelector";

export default function Dashboard() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [lang, setLang] = useState("en"); // "en", "si", "ta"
  const [startingCash, setStartingCash] = useState(80000);
  const [dailySales, setDailySales] = useState(45000);
  const [dailyRestock, setDailyRestock] = useState(34000);
  const [orderReductionPct, setOrderReductionPct] = useState(0);
  const [simulateLowConfidence, setSimulateLowConfidence] = useState(false);

  const [forecastData, setForecastData] = useState(null);
  const [selectedDayIndex, setSelectedDayIndex] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const loadForecast = async () => {
    setIsLoading(true);
    try {
      const data = await fetch14DayForecast({
        starting_cash: startingCash,
        daily_sales: dailySales,
        daily_restock: dailyRestock,
        order_reduction_pct: orderReductionPct,
        simulate_low_confidence: simulateLowConfidence,
      });
      setForecastData(data);
    } catch (err) {
      console.error("Failed to load forecast:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadForecast();
  }, [simulateLowConfidence, orderReductionPct]);

  return (
    <div className="min-h-screen bg-[#e8ecf4] dark:bg-[#1c2028] text-slate-800 dark:text-slate-100 transition-colors duration-300 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Neumorphic Header */}
        <header className="neu-panel p-6 mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3">
              <span className="text-xl font-black tracking-tight text-blue-600 dark:text-blue-400">
                ModelX 2.0
              </span>
              <span className="neu-inset px-3 py-0.5 text-xs font-black uppercase text-slate-600 dark:text-slate-300">
                Phase 1 Prototype · Domain 01
              </span>
            </div>
            <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight mt-1.5">
              Automated Micro-Liquidity & Cash-Flow Stress Forecaster
            </h1>
            <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 mt-0.5">
              IEEE Computational Intelligence Society Student Chapter (IIT) · NIBM
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Trilingual Language Selector */}
            <div className="neu-card p-1 rounded-xl flex items-center space-x-1 text-xs font-black">
              <button
                onClick={() => setLang("en")}
                className={`px-2.5 py-1 rounded-lg transition-all ${lang === "en" ? "neu-inset text-blue-600 dark:text-blue-400" : "text-slate-600 dark:text-slate-400"}`}
              >
                EN
              </button>
              <button
                onClick={() => setLang("si")}
                className={`px-2.5 py-1 rounded-lg transition-all ${lang === "si" ? "neu-inset text-blue-600 dark:text-blue-400" : "text-slate-600 dark:text-slate-400"}`}
              >
                සිංහල
              </button>
              <button
                onClick={() => setLang("ta")}
                className={`px-2.5 py-1 rounded-lg transition-all ${lang === "ta" ? "neu-inset text-blue-600 dark:text-blue-400" : "text-slate-600 dark:text-slate-400"}`}
              >
                தமிழ்
              </button>
            </div>

            {/* Theme Toggle Button */}
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className="neu-btn px-4 py-2 text-xs font-black uppercase tracking-wider text-slate-800 dark:text-slate-200"
              title="Toggle Light / Dark Neumorphism"
            >
              <span>{isDarkMode ? "☀️ Light" : "🌙 Dark"}</span>
            </button>
          </div>
        </header>

        {/* Safe Failure Banner */}
        {forecastData && <SafeFailureBanner trust={forecastData.trust} />}

        {/* Actionable Recommendation Card with Trilingual Localization */}
        {forecastData && <ActionCard recommendation={forecastData.recommendation} lang={lang} />}

        {/* 14-Day Calendar Timeline */}
        {forecastData && (
          <StressCalendar14Day
            timeline={forecastData.timeline}
            selectedDayIndex={selectedDayIndex}
            onSelectDay={(day) => setSelectedDayIndex(day)}
          />
        )}

        {/* Dual-Axis Visual Chart & Detailed Diagnostics */}
        {forecastData && (
          <PriceWeatherChart
            timeline={forecastData.timeline}
            selectedDayIndex={selectedDayIndex}
            onSelectDay={(day) => setSelectedDayIndex(day)}
            baseCash={startingCash}
            lang={lang}
          />
        )}

        {/* Shopkeeper Input Simulation & What-If Order Slider */}
        <ShopProfileSelector
          startingCash={startingCash}
          setStartingCash={setStartingCash}
          dailySales={dailySales}
          setDailySales={setDailySales}
          dailyRestock={dailyRestock}
          setDailyRestock={setDailyRestock}
          orderReductionPct={orderReductionPct}
          setOrderReductionPct={setOrderReductionPct}
          simulateLowConfidence={simulateLowConfidence}
          setSimulateLowConfidence={setSimulateLowConfidence}
          onRefresh={loadForecast}
          isLoading={isLoading}
          lang={lang}
        />
      </div>
    </div>
  );
}
