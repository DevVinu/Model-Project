import React from "react";

export default function SafeFailureBanner({ trust }) {
  if (!trust) return null;

  if (trust.is_suppressed) {
    return (
      <div className="neu-panel p-5 mb-6 border-l-4 border-amber-500 transition-all">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center space-x-3">
            <span className="neu-btn px-3 py-1.5 text-xs font-black tracking-wider uppercase bg-amber-500/20 text-amber-700 dark:text-amber-400 border border-amber-500/40 rounded-lg">
              ⚠️ SAFE-FAILURE ACTIVE
            </span>
            <span className="text-sm font-bold text-slate-800 dark:text-slate-100">
              Confidence Below Threshold ({trust.confidence_percentage}% &lt; 50%)
            </span>
          </div>
          <span className="neu-inset px-3 py-1 text-xs font-semibold text-amber-800 dark:text-amber-300">
            Automated Protection Triggered
          </span>
        </div>
        <p className="text-sm text-slate-700 dark:text-slate-300 mt-2.5 leading-relaxed font-medium">
          {trust.safe_message}
        </p>
      </div>
    );
  }

  return (
    <div className="neu-panel p-4 mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div className="flex items-center space-x-3">
        <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981] animate-pulse"></span>
        <span className="text-xs uppercase font-extrabold tracking-wider text-slate-500 dark:text-slate-400">
          System Confidence:
        </span>
        <span className="neu-inset px-3 py-0.5 text-xs font-black text-emerald-600 dark:text-emerald-400">
          {trust.confidence_percentage}% HIGH TRUST
        </span>
      </div>
      <div className="text-xs font-medium text-slate-600 dark:text-slate-400">
        CBSL Weekly Pettah Market Bulletin · Open-Meteo 14-Day Atmospheric Radar
      </div>
    </div>
  );
}
