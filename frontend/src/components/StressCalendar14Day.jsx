import React from "react";

export default function StressCalendar14Day({ timeline, onSelectDay, selectedDayIndex }) {
  if (!timeline || timeline.length === 0) return null;

  const getRiskDetails = (level) => {
    switch (level) {
      case "RED":
        return {
          dot: "bg-red-500 shadow-[0_0_6px_#ef4444]",
          badge: "text-red-700 dark:text-red-400 bg-red-500/10",
          border: "border-red-500/50",
        };
      case "YELLOW":
        return {
          dot: "bg-amber-400 shadow-[0_0_6px_#f59e0b]",
          badge: "text-amber-700 dark:text-amber-400 bg-amber-500/10",
          border: "border-amber-500/50",
        };
      default:
        return {
          dot: "bg-emerald-500 shadow-[0_0_6px_#10b981]",
          badge: "text-emerald-700 dark:text-emerald-400 bg-emerald-500/10",
          border: "border-emerald-500/40",
        };
    }
  };

  return (
    <div className="neu-panel p-6 mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-300/80 dark:border-slate-800 gap-3">
        <div>
          <h3 className="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span>📅</span> 14-Day Micro-Liquidity Stress Timeline
          </h3>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400">
            Click any day to inspect simulated cash reserves, rainfall, and foot traffic
          </p>
        </div>
        <div className="flex items-center space-x-3 text-xs font-bold text-slate-700 dark:text-slate-300">
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_6px_#10b981]"></span> Stable</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-[0_0_6px_#f59e0b]"></span> Caution</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-[0_0_6px_#ef4444]"></span> Squeeze</span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3 mt-5">
        {timeline.map((item) => {
          const isSelected = selectedDayIndex === item.day_index;
          const { dot, badge, border } = getRiskDetails(item.risk_level);

          return (
            <button
              key={item.day_index}
              onClick={() => onSelectDay(item.day_index)}
              className={`p-3.5 rounded-xl text-left transition-all relative ${
                isSelected
                  ? "neu-inset border-2 border-blue-500 dark:border-blue-400 scale-[0.98]"
                  : `neu-card border ${border}`
              }`}
            >
              <div className="flex justify-between items-center">
                <span className="text-xs font-black text-slate-800 dark:text-slate-200">
                  Day {item.day_index}
                </span>
                <span className={`w-2.5 h-2.5 rounded-full ${dot}`}></span>
              </div>
              
              <div className="text-[11px] font-semibold text-slate-500 dark:text-slate-400 mt-1">
                {item.date.slice(5)}
              </div>

              <div className="mt-3 space-y-1">
                <div className="text-xs font-black text-slate-900 dark:text-white">
                  LKR {(item.projected_cash_lkr / 1000).toFixed(1)}k
                </div>
                <div className="text-[11px] font-medium text-slate-600 dark:text-slate-400 flex items-center justify-between">
                  <span>🌧️ {item.precipitation_mm}mm</span>
                  <span>👥 {Math.round(item.foot_traffic_multiplier * 100)}%</span>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
