import React from "react";

export default function ActionCard({ recommendation }) {
  if (!recommendation) return null;

  const isHighUrgency = recommendation.urgency === "HIGH";
  const isSuppressed = recommendation.action_type === "SUPPRESSED";

  return (
    <div className={`neu-panel p-6 mb-6 transition-all ${
      isSuppressed 
        ? "border-l-4 border-amber-500" 
        : (isHighUrgency ? "border-l-4 border-red-500" : "border-l-4 border-emerald-500")
    }`}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <span className={`neu-btn px-3 py-1.5 text-xs font-black tracking-wider uppercase rounded-lg ${
          isSuppressed
            ? "text-amber-700 dark:text-amber-400"
            : (isHighUrgency ? "text-red-600 dark:text-red-400" : "text-emerald-700 dark:text-emerald-400")
        }`}>
          {isSuppressed ? "Safe-Failure Mode" : `Operational Insight (${recommendation.urgency} Urgency)`}
        </span>

        {recommendation.recommended_order_adjustment_pct !== 0 && (
          <span className="neu-inset px-3.5 py-1 text-xs font-black text-red-600 dark:text-red-400">
            Order Adjustment: {recommendation.recommended_order_adjustment_pct}%
          </span>
        )}
      </div>

      <h3 className="text-xl font-black text-slate-900 dark:text-white mt-3.5 tracking-tight">
        {recommendation.headline}
      </h3>

      <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mt-2 leading-relaxed">
        {recommendation.detail}
      </p>

      {recommendation.suggested_actions && recommendation.suggested_actions.length > 0 && (
        <div className="mt-5 pt-4 border-t border-slate-300/80 dark:border-slate-800">
          <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3">
            Recommended Working-Capital Actions
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {recommendation.suggested_actions.map((act, idx) => (
              <div key={idx} className="neu-inset p-3 text-xs font-semibold text-slate-800 dark:text-slate-200 flex items-start space-x-2">
                <span className="text-blue-500 font-black">•</span>
                <span>{act}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
