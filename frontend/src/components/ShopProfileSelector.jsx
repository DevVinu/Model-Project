import React from "react";

export default function ShopProfileSelector({
  startingCash,
  setStartingCash,
  dailySales,
  setDailySales,
  dailyRestock,
  setDailyRestock,
  simulateLowConfidence,
  setSimulateLowConfidence,
  onRefresh,
  isLoading,
}) {
  return (
    <div className="neu-panel p-6 mb-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-300/80 dark:border-slate-800 mb-4">
        <h3 className="text-xs font-black text-slate-700 dark:text-slate-300 uppercase tracking-wider flex items-center gap-2">
          <span>🏪</span> Shopkeeper Simulation Parameters
        </h3>
        <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
          Pettah & Colombo Wholesale Baseline
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div>
          <label className="text-xs font-bold text-slate-600 dark:text-slate-400 block mb-2">
            Current Cash on Hand (LKR)
          </label>
          <input
            type="number"
            value={startingCash}
            onChange={(e) => setStartingCash(Number(e.target.value))}
            className="neu-inset w-full px-4 py-2.5 text-sm font-bold text-slate-900 dark:text-white bg-transparent focus:outline-none"
          />
        </div>

        <div>
          <label className="text-xs font-bold text-slate-600 dark:text-slate-400 block mb-2">
            Average Daily Sales (LKR)
          </label>
          <input
            type="number"
            value={dailySales}
            onChange={(e) => setDailySales(Number(e.target.value))}
            className="neu-inset w-full px-4 py-2.5 text-sm font-bold text-slate-900 dark:text-white bg-transparent focus:outline-none"
          />
        </div>

        <div>
          <label className="text-xs font-bold text-slate-600 dark:text-slate-400 block mb-2">
            Daily Restocking Expense (LKR)
          </label>
          <input
            type="number"
            value={dailyRestock}
            onChange={(e) => setDailyRestock(Number(e.target.value))}
            className="neu-inset w-full px-4 py-2.5 text-sm font-bold text-slate-900 dark:text-white bg-transparent focus:outline-none"
          />
        </div>
      </div>

      <div className="mt-5 pt-4 border-t border-slate-300/80 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <label className="neu-card px-4 py-2 rounded-xl flex items-center space-x-3 cursor-pointer">
          <input
            type="checkbox"
            checked={simulateLowConfidence}
            onChange={(e) => setSimulateLowConfidence(e.target.checked)}
            className="w-4 h-4 text-amber-500 rounded focus:ring-0 cursor-pointer"
          />
          <span className="text-xs font-bold text-amber-700 dark:text-amber-400">
            Simulate Safe-Failure Mode (Confidence &lt; 50%)
          </span>
        </label>

        <button
          onClick={onRefresh}
          disabled={isLoading}
          className="neu-btn px-6 py-2.5 text-xs font-black uppercase tracking-wider text-blue-600 dark:text-blue-400 hover:text-blue-700 transition-colors disabled:opacity-50"
        >
          {isLoading ? "Recalculating..." : "🔄 Update Stress Forecast"}
        </button>
      </div>
    </div>
  );
}
