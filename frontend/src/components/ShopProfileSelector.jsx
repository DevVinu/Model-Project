import React from "react";

export default function ShopProfileSelector({
  startingCash,
  setStartingCash,
  dailySales,
  setDailySales,
  dailyRestock,
  setDailyRestock,
  orderReductionPct,
  setOrderReductionPct,
  simulateLowConfidence,
  setSimulateLowConfidence,
  onRefresh,
  isLoading,
  lang = "en",
}) {
  const labels = {
    en: {
      params: "Shopkeeper Simulation Parameters",
      baseline: "Pettah & Colombo Wholesale Baseline",
      cash: "Current Cash on Hand (LKR)",
      sales: "Average Daily Sales (LKR)",
      restock: "Daily Restocking Expense (LKR)",
      whatIfTitle: "What-If Restocking Order Adjustment Slider",
      whatIfDesc: "Simulate cutting bulk restocking orders by 0% - 30% before heavy rain to prevent cash squeeze",
      cutApplied: "Order Reduction Cut",
      simLow: "Simulate Safe-Failure Mode (Confidence < 50%)",
      recalc: "Recalculate Stress Forecast",
    },
    si: {
      params: "වෙළඳසැල් පරාමිතීන් සහ සමාකරණය",
      baseline: "පිටකොටුව සහ කොළඹ තොග වෙළඳපල දත්ත",
      cash: "අතැති මුදල් ප්‍රමාණය (රු.)",
      sales: "දෛනික සාමාන්‍ය අලෙවිය (රු.)",
      restock: "දෛනික තොග වියදම (රු.)",
      whatIfTitle: "තොග ඇණවුම් වෙනස් කිරීමේ අන්තර්ක්‍රියාකාරී පාලකය (What-If Slider)",
      whatIfDesc: "මුදල් හිඟය මඟහරවා ගැනීමට තොග ඇණවුම් 0% සිට 30% දක්වා අඩු කර ප්‍රතිඵලය පරීක්ෂා කරන්න",
      cutApplied: "ඇණවුම් අඩු කිරීම",
      simLow: "ආරක්ෂිත මාදිලිය පරීක්ෂා කිරීම (විශ්වාසනීයත්වය < 50%)",
      recalc: "අනාවැකිය යාවත්කාලීන කරන්න",
    },
    ta: {
      params: "கடைக்காரர் அளவுருக்கள் மற்றும் உருவகப்படுத்துதல்",
      baseline: "புறக்கோட்டை சந்தை அடிப்படை தரவு",
      cash: "கையிருப்பு பணம் (ரூ.)",
      sales: "தினசரி சராசரி விற்பனை (ரூ.)",
      restock: "தினசரி கொள்முதல் செலவு (ரூ.)",
      whatIfTitle: "கொள்முதல் ஆர்டர் மாற்றியமைப்பான் (What-If Slider)",
      whatIfDesc: "பண நெருக்கடியைத் தவிர்க்க கொள்முதலை 0% முதல் 30% வரை குறைத்து பரிசோதிக்கவும்",
      cutApplied: "ஆர்டர் குறைப்பு",
      simLow: "பாதுகாப்பு முறையை சோதிக்கவும் (நம்பகத்தன்மை < 50%)",
      recalc: "முன்னறிவிப்பைப் புதுப்பிக்கவும்",
    },
  }[lang] || labels.en;

  return (
    <div className="neu-panel p-6 mb-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-300/80 dark:border-slate-800 mb-4">
        <h3 className="text-xs font-black text-slate-700 dark:text-slate-300 uppercase tracking-wider flex items-center gap-2">
          <span>🏪</span> {labels.params}
        </h3>
        <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
          {labels.baseline}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div>
          <label className="text-xs font-bold text-slate-600 dark:text-slate-400 block mb-2">
            {labels.cash}
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
            {labels.sales}
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
            {labels.restock}
          </label>
          <input
            type="number"
            value={dailyRestock}
            onChange={(e) => setDailyRestock(Number(e.target.value))}
            className="neu-inset w-full px-4 py-2.5 text-sm font-bold text-slate-900 dark:text-white bg-transparent focus:outline-none"
          />
        </div>
      </div>

      {/* Interactive What-If Order Reduction Slider */}
      <div className="mt-5 p-4 rounded-xl neu-card">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
          <div>
            <span className="text-xs font-black uppercase text-blue-600 dark:text-blue-400 flex items-center gap-1.5">
              <span>🎚️</span> {labels.whatIfTitle}
            </span>
            <p className="text-[11px] font-medium text-slate-500 dark:text-slate-400">
              {labels.whatIfDesc}
            </p>
          </div>
          <span className="neu-inset px-3 py-1 text-xs font-black text-blue-600 dark:text-blue-400">
            {labels.cutApplied}: -{orderReductionPct}%
          </span>
        </div>
        <input
          type="range"
          min="0"
          max="35"
          step="5"
          value={orderReductionPct}
          onChange={(e) => setOrderReductionPct(Number(e.target.value))}
          className="w-full h-2 bg-slate-300 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
        />
        <div className="flex justify-between text-[10px] font-bold text-slate-500 mt-1">
          <span>0% (Standard)</span>
          <span>-10%</span>
          <span className="text-blue-600 dark:text-blue-400 font-extrabold">-20% (Recommended)</span>
          <span>-30%</span>
          <span>-35% (Max)</span>
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
            {labels.simLow}
          </span>
        </label>

        <button
          onClick={onRefresh}
          disabled={isLoading}
          className="neu-btn px-6 py-2.5 text-xs font-black uppercase tracking-wider text-blue-600 dark:text-blue-400 hover:text-blue-700 transition-colors disabled:opacity-50"
        >
          {isLoading ? "Recalculating..." : `🔄 ${labels.recalc}`}
        </button>
      </div>
    </div>
  );
}
