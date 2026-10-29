import React from "react";

export default function PriceWeatherChart({ timeline, selectedDayIndex }) {
  if (!timeline || timeline.length === 0) return null;

  const selectedItem = timeline.find((t) => t.day_index === selectedDayIndex) || timeline[0];

  const getRiskBadge = (level) => {
    switch (level) {
      case "RED":
        return "text-red-700 dark:text-red-400 bg-red-500/15 border-red-500/40";
      case "YELLOW":
        return "text-amber-700 dark:text-amber-400 bg-amber-500/15 border-amber-500/40";
      default:
        return "text-emerald-700 dark:text-emerald-400 bg-emerald-500/15 border-emerald-500/40";
    }
  };

  return (
    <div className="neu-panel p-6 mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-300/80 dark:border-slate-800">
        <div>
          <h3 className="text-base font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span>📊</span> Day {selectedItem.day_index} ({selectedItem.date}) Detailed Stress Diagnostics
          </h3>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400">
            Localized cash reserve projections, wholesale price shocks, and foot-traffic disruption
          </p>
        </div>
        <div className="mt-2 sm:mt-0">
          <span className={`neu-btn px-3 py-1 text-xs font-black tracking-wider uppercase border rounded-lg ${getRiskBadge(selectedItem.risk_level)}`}>
            {selectedItem.risk_level} (Stress Score: {selectedItem.stress_score}/100)
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-5">
        <div className="neu-card p-4">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            Closing Cash Balance
          </span>
          <div className="text-xl font-black text-emerald-600 dark:text-emerald-400 mt-1.5">
            LKR {Math.round(selectedItem.projected_cash_lkr).toLocaleString()}
          </div>
          <span className="text-[11px] font-medium text-slate-500 mt-1 block">
            End of day liquidity buffer
          </span>
        </div>

        <div className="neu-card p-4">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            Precipitation & Foot Traffic
          </span>
          <div className="text-xl font-black text-blue-600 dark:text-blue-400 mt-1.5">
            {selectedItem.precipitation_mm} mm
          </div>
          <span className="text-[11px] font-medium text-slate-500 mt-1 block">
            {Math.round(selectedItem.foot_traffic_multiplier * 100)}% normal customer walk-in rate
          </span>
        </div>

        <div className="neu-card p-4">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            Weather-Adjusted Revenue
          </span>
          <div className="text-xl font-black text-slate-900 dark:text-slate-100 mt-1.5">
            LKR {Math.round(selectedItem.daily_revenue_lkr).toLocaleString()}
          </div>
          <span className="text-[11px] font-medium text-slate-500 mt-1 block">
            Foot-traffic scaled sales
          </span>
        </div>

        <div className="neu-card p-4">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            Restock Outflow & Index
          </span>
          <div className="text-xl font-black text-rose-600 dark:text-rose-400 mt-1.5">
            LKR {Math.round(selectedItem.daily_outflow_lkr).toLocaleString()}
          </div>
          <span className="text-[11px] font-medium text-slate-500 mt-1 block">
            Wholesale factor: {(selectedItem.wholesale_cost_multiplier * 100).toFixed(0)}% base
          </span>
        </div>
      </div>
    </div>
  );
}
