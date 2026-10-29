import React from "react";

export default function PriceWeatherChart({ timeline, selectedDayIndex, onSelectDay, baseCash = 80000, lang = "en" }) {
  if (!timeline || timeline.length === 0) return null;

  const selectedItem = timeline.find((t) => t.day_index === selectedDayIndex) || timeline[0];
  const safeBuffer = baseCash * 0.40;

  // Chart scaling calculations
  const maxCash = Math.max(...timeline.map((t) => t.projected_cash_lkr), baseCash * 1.1);
  const minCash = Math.min(...timeline.map((t) => t.projected_cash_lkr), safeBuffer * 0.8, 0);
  const cashRange = maxCash - minCash || 1;

  const maxRain = Math.max(...timeline.map((t) => t.precipitation_mm), 45);

  const chartWidth = 700;
  const chartHeight = 200;
  const paddingX = 40;
  const paddingY = 25;
  const plotWidth = chartWidth - paddingX * 2;
  const plotHeight = chartHeight - paddingY * 2;

  // Convert points
  const points = timeline.map((item, idx) => {
    const x = paddingX + (idx / (timeline.length - 1)) * plotWidth;
    const y = paddingY + plotHeight - ((item.projected_cash_lkr - minCash) / cashRange) * plotHeight;
    return { x, y, item };
  });

  const pathD = points.reduce((acc, pt, i) => `${acc} ${i === 0 ? "M" : "L"} ${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`, "");
  const areaD = `${pathD} L ${points[points.length - 1].x.toFixed(1)} ${paddingY + plotHeight} L ${points[0].x.toFixed(1)} ${paddingY + plotHeight} Z`;

  // Safe buffer reference line Y
  const bufferY = paddingY + plotHeight - ((safeBuffer - minCash) / cashRange) * plotHeight;

  const labels = {
    en: {
      chartTitle: "14-Day Dual-Axis Forecast Curves",
      chartSubtitle: "Cash reserves vs. Safe buffer threshold overlayed with precipitation",
      cashLine: "Projected Cash (LKR)",
      safeLine: "Safe Buffer Line (40%)",
      rainBars: "Precipitation (mm)",
      closingCash: "Closing Cash Balance",
      footTraffic: "Rainfall & Walk-In Traffic",
      dailyRev: "Weather-Adjusted Revenue",
      dailyOutflow: "Restock Outflow & Index",
      diagnostics: "Detailed Stress Diagnostics",
    },
    si: {
      chartTitle: "දින 14 කාරක ප්‍රාග්ධන සහ වර්ෂාපතන ප්‍රස්තාරය",
      chartSubtitle: "අතැති මුදල් සහ අවම ආරක්ෂිත සීමාව (40%) වර්ෂාපතනය සමග සංසන්දනය",
      cashLine: "අපේක්ෂිත මුදල් (රු.)",
      safeLine: "අවම ආරක්ෂිත සීමාව (40%)",
      rainBars: "වර්ෂාපතනය (mm)",
      closingCash: "අවසාන මුදල් ශේෂය",
      footTraffic: "වර්ෂාව සහ පාරිභෝගික පැමිණීම",
      dailyRev: "වර්ෂාවට අනුව ආදායම",
      dailyOutflow: "තොග වියදම සහ මිල දර්ශකය",
      diagnostics: "දෛනික මූල්‍ය විග්‍රහය",
    },
    ta: {
      chartTitle: "14-நாள் பணப்புழக்கம் மற்றும் மழைப்பொழிவு வரைபடம்",
      chartSubtitle: "பண இருப்பு மற்றும் குறைந்தபட்ச பாதுகாப்பு வரம்பு (40%)",
      cashLine: "எதிர்பார்க்கப்படும் பணம் (ரூ.)",
      safeLine: "பாதுகாப்பு வரம்பு (40%)",
      rainBars: "மழைப்பொழிவு (மிமீ)",
      closingCash: "இறுதி பண இருப்பு",
      footTraffic: "மழை மற்றும் வாடிக்கையாளர் வருகை",
      dailyRev: "மழைக்கேற்ற வருவாய்",
      dailyOutflow: "கொள்முதல் செலவு & குறியீடு",
      diagnostics: "விரிவான பகுப்பாய்வு",
    },
  }[lang] || labels.en;

  return (
    <div className="neu-panel p-6 mb-6">
      {/* Chart Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-300/80 dark:border-slate-800 gap-2">
        <div>
          <h3 className="text-base font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span>📈</span> {labels.chartTitle}
          </h3>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400">
            {labels.chartSubtitle}
          </p>
        </div>
        <div className="flex items-center space-x-3 text-xs font-bold">
          <span className="flex items-center gap-1.5 text-blue-600 dark:text-blue-400">
            <span className="w-3 h-0.5 bg-blue-500"></span> {labels.cashLine}
          </span>
          <span className="flex items-center gap-1.5 text-red-600 dark:text-red-400">
            <span className="w-3 h-0.5 border-t border-dashed border-red-500"></span> {labels.safeLine}
          </span>
          <span className="flex items-center gap-1.5 text-sky-500">
            <span className="w-2.5 h-2.5 bg-sky-400/40 rounded-sm"></span> {labels.rainBars}
          </span>
        </div>
      </div>

      {/* SVG Dual Axis Curve */}
      <div className="mt-4 overflow-x-auto">
        <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="w-full h-48 select-none">
          <defs>
            <linearGradient id="cashGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Safe Buffer Reference Line */}
          <line
            x1={paddingX}
            y1={bufferY}
            x2={chartWidth - paddingX}
            y2={bufferY}
            stroke="#ef4444"
            strokeDasharray="4 4"
            strokeWidth="1.5"
          />
          <text
            x={chartWidth - paddingX - 4}
            y={bufferY - 4}
            fill="#ef4444"
            fontSize="9"
            fontWeight="bold"
            textAnchor="end"
          >
            Safe Buffer: LKR {(safeBuffer / 1000).toFixed(0)}k
          </text>

          {/* Rainfall Background Bars */}
          {timeline.map((item, idx) => {
            const barW = (plotWidth / timeline.length) * 0.45;
            const barH = (item.precipitation_mm / maxRain) * (plotHeight * 0.85);
            const x = paddingX + (idx / (timeline.length - 1)) * plotWidth - barW / 2;
            const y = paddingY + plotHeight - barH;
            return (
              <rect
                key={idx}
                x={x}
                y={y}
                width={barW}
                height={barH}
                fill="#38bdf8"
                opacity="0.3"
                rx="2"
              />
            );
          })}

          {/* Cash Area & Curve Line */}
          <path d={areaD} fill="url(#cashGradient)" />
          <path d={pathD} fill="none" stroke="#3b82f6" strokeWidth="2.5" strokeLinecap="round" />

          {/* Interactive Data Dots */}
          {points.map((pt, idx) => {
            const isSel = pt.item.day_index === selectedDayIndex;
            const isSqueeze = pt.item.risk_level === "RED";
            return (
              <g key={idx} onClick={() => onSelectDay && onSelectDay(pt.item.day_index)} className="cursor-pointer">
                <circle
                  cx={pt.x}
                  cy={pt.y}
                  r={isSel ? "6" : "3.5"}
                  fill={isSqueeze ? "#ef4444" : "#3b82f6"}
                  stroke="#ffffff"
                  strokeWidth={isSel ? "2" : "1"}
                />
                <text
                  x={pt.x}
                  y={chartHeight - 6}
                  fill="#94a3b8"
                  fontSize="9"
                  textAnchor="middle"
                  fontWeight={isSel ? "bold" : "normal"}
                >
                  D{pt.item.day_index}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Selected Day Diagnostic Breakdown */}
      <div className="mt-5 pt-4 border-t border-slate-300/80 dark:border-slate-800">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-xs font-black uppercase tracking-wider text-slate-700 dark:text-slate-300">
            Day {selectedItem.day_index} ({selectedItem.date}) {labels.diagnostics}
          </h4>
          <span className={`neu-btn px-2.5 py-0.5 text-xs font-black uppercase rounded-lg ${
            selectedItem.risk_level === "RED" ? "text-red-600 dark:text-red-400" : "text-emerald-600 dark:text-emerald-400"
          }`}>
            {selectedItem.risk_level} (Stress: {selectedItem.stress_score}/100)
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="neu-card p-3.5">
            <span className="text-[10px] font-bold uppercase text-slate-500 dark:text-slate-400 block">{labels.closingCash}</span>
            <div className="text-base font-black text-emerald-600 dark:text-emerald-400 mt-1">
              LKR {Math.round(selectedItem.projected_cash_lkr).toLocaleString()}
            </div>
          </div>
          <div className="neu-card p-3.5">
            <span className="text-[10px] font-bold uppercase text-slate-500 dark:text-slate-400 block">{labels.footTraffic}</span>
            <div className="text-base font-black text-blue-600 dark:text-blue-400 mt-1">
              {selectedItem.precipitation_mm} mm ({Math.round(selectedItem.foot_traffic_multiplier * 100)}%)
            </div>
          </div>
          <div className="neu-card p-3.5">
            <span className="text-[10px] font-bold uppercase text-slate-500 dark:text-slate-400 block">{labels.dailyRev}</span>
            <div className="text-base font-black text-slate-900 dark:text-slate-100 mt-1">
              LKR {Math.round(selectedItem.daily_revenue_lkr).toLocaleString()}
            </div>
          </div>
          <div className="neu-card p-3.5">
            <span className="text-[10px] font-bold uppercase text-slate-500 dark:text-slate-400 block">{labels.dailyOutflow}</span>
            <div className="text-base font-black text-rose-600 dark:text-rose-400 mt-1">
              LKR {Math.round(selectedItem.daily_outflow_lkr).toLocaleString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
