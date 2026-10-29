import React from "react";

export default function ActionCard({ recommendation, lang = "en" }) {
  if (!recommendation) return null;

  const isHighUrgency = recommendation.urgency === "HIGH";
  const isSuppressed = recommendation.action_type === "SUPPRESSED";

  const getLocalized = (field) => {
    if (!field) return "";
    if (typeof field === "object" && field[lang]) return field[lang];
    if (typeof field === "object" && field.en) return field.en;
    return String(field);
  };

  const getLocalizedActions = (actions) => {
    if (!actions) return [];
    if (Array.isArray(actions)) return actions;
    if (actions[lang]) return actions[lang];
    if (actions.en) return actions.en;
    return [];
  };

  const labels = {
    en: {
      suppressed: "Safety Suppression Active",
      insight: "Operational Insight",
      urgency: "Urgency",
      orderAdjustment: "Order Adjustment",
      suggestedActions: "Recommended Working-Capital Actions",
      attribution: "XAI Root Cause Analysis",
      rainImpact: "Heavy Monsoon Rain",
      wholesaleImpact: "Wholesale Commodity Surge",
      dieselImpact: "Transport Tariff Revision",
    },
    si: {
      suppressed: "ආරක්ෂිත මාදිලිය සක්‍රියයි",
      insight: "ක්‍රියාකාරී උපදෙස",
      urgency: "හදිසිභාවය",
      orderAdjustment: "ඇණවුම් සංශෝධනය",
      suggestedActions: "ප්‍රාග්ධනය රැකගැනීමේ පියවර",
      attribution: "හේතු විශ්ලේෂණය (XAI)",
      rainImpact: "දැඩි මෝසම් වර්ෂාව",
      wholesaleImpact: "තොග මිල ඉහළ යාම",
      dieselImpact: "ප්‍රවාහන ගාස්තු සංශෝධනය",
    },
    ta: {
      suppressed: "பாதுகாப்பு முறை செயலில் உள்ளது",
      insight: "செயல் நுண்ணறிவு",
      urgency: "அவசரம்",
      orderAdjustment: "ஆர்டர் மாற்றம்",
      suggestedActions: "பரிந்துரைக்கப்பட்ட நடவடிக்கைகள்",
      attribution: "காரண பகுப்பாய்வு (XAI)",
      rainImpact: "கனமழை தாக்கம்",
      wholesaleImpact: "மொத்த விலை உயர்வு",
      dieselImpact: "போக்குவரத்து கட்டண உயர்வு",
    },
  }[lang] || labels.en;

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
          {isSuppressed ? labels.suppressed : `${labels.insight} (${recommendation.urgency} ${labels.urgency})`}
        </span>

        {recommendation.recommended_order_adjustment_pct !== 0 && (
          <span className="neu-inset px-3.5 py-1 text-xs font-black text-red-600 dark:text-red-400">
            {labels.orderAdjustment}: {recommendation.recommended_order_adjustment_pct}%
          </span>
        )}
      </div>

      <h3 className="text-xl font-black text-slate-900 dark:text-white mt-3.5 tracking-tight">
        {getLocalized(recommendation.headline)}
      </h3>

      <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mt-2 leading-relaxed">
        {getLocalized(recommendation.detail)}
      </p>

      {/* Suggested Actions */}
      <div className="mt-5 pt-4 border-t border-slate-300/80 dark:border-slate-800">
        <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3">
          {labels.suggestedActions}
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {getLocalizedActions(recommendation.suggested_actions).map((act, idx) => (
            <div key={idx} className="neu-inset p-3 text-xs font-semibold text-slate-800 dark:text-slate-200 flex items-start space-x-2">
              <span className="text-blue-500 font-black">•</span>
              <span>{act}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Explainable AI (XAI) Attribution Pill */}
      {isHighUrgency && !isSuppressed && (
        <div className="mt-4 pt-3 border-t border-slate-300/60 dark:border-slate-800 flex flex-wrap items-center gap-2 text-[11px] font-bold">
          <span className="text-slate-500 uppercase tracking-wider mr-1">
            {labels.attribution}:
          </span>
          <span className="neu-card px-2.5 py-1 text-blue-600 dark:text-blue-400">
            🌧️ {labels.rainImpact} (-45% Footfall)
          </span>
          <span className="neu-card px-2.5 py-1 text-red-600 dark:text-red-400">
            🌾 {labels.wholesaleImpact} (+5.4% Outflow)
          </span>
          <span className="neu-card px-2.5 py-1 text-amber-600 dark:text-amber-400">
            ⛽ {labels.dieselImpact} (+2.1% Freight)
          </span>
        </div>
      )}
    </div>
  );
}
