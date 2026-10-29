import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class InventoryAdvisor:
    """Translates multivariate mathematical stress projections into clear,

    actionable inventory advice for small shopkeepers, with trilingual support
    (English, Sinhala, Tamil) tailored for Sri Lankan informal retailers.
    """

    @staticmethod
    def generate_recommendation(
        timeline: List[Dict[str, Any]],
        trust_status: Dict[str, Any],
        price_forecasts: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Produces primary recommendation card text with trilingual localization."""
        is_suppressed = trust_status.get("is_suppressed", False)

        if is_suppressed:
            return {
                "action_type": "SUPPRESSED",
                "headline": {
                    "en": "Recommendation Suppressed (Safe-Failure Mode)",
                    "si": "නිර්දේශය අත්හිටුවා ඇත (ආරක්ෂිත මාදිලිය)",
                    "ta": "பரிந்துரை இடைநிறுத்தப்பட்டது (பாதுகாப்பு முறை)",
                },
                "detail": {
                    "en": trust_status.get("safe_message", "Forecast confidence is low. Recommendations suppressed to prevent risk."),
                    "si": "තෝරාගත් භාණ්ඩ සඳහා තොග මිල දත්ත සීමිතය. අනාවැකි විශ්වාසනීයත්වය අඩු බැවින් අවදානම වැළැක්වීමට නිර්දේශ අත්හිටුවා ඇත.",
                    "ta": "தேர்ந்தெடுக்கப்பட்ட பொருட்களுக்கான மொத்த விலை தரவு குறைவாக உள்ளது. இடர் தவிர்க்க பரிந்துரைகள் இடைநிறுத்தப்பட்டுள்ளன.",
                },
                "recommended_order_adjustment_pct": 0,
                "urgency": "LOW",
                "suggested_actions": {
                    "en": [
                        "Rely on conservative historical inventory moving averages.",
                        "Avoid speculative bulk orders until market feeds re-stabilize.",
                        "Check back once live wholesale pricing updates are restored.",
                    ],
                    "si": [
                        "ඓතිහාසික සාමාන්‍ය තොග මට්ටම් මත පමණක් තීරණ ගන්න.",
                        "වෙළඳපල මිල ස්ථාවර වන තෙක් තොග වශයෙන් මිලදී ගැනීමෙන් වළකින්න.",
                        "මිල යාවත්කාලීන වූ පසු නැවත පරීක්ෂා කරන්න.",
                    ],
                    "ta": [
                        "வரலாற்று சராசரி இருப்பு நிலைகளை மட்டும் நம்புங்கள்.",
                        "சந்தை சீராகும் வரை மொத்தமாக வாங்குவதைத் தவிர்க்கவும்.",
                        "விலை புதுப்பிக்கப்பட்ட பிறகு மீண்டும் சரிபார்க்கவும்.",
                    ],
                },
            }

        # Find earliest squeeze day
        squeeze_days = [t for t in timeline if t.get("risk_level") == "RED"]
        caution_days = [t for t in timeline if t.get("risk_level") == "YELLOW"]

        if squeeze_days:
            first_squeeze = squeeze_days[0]
            day_idx = first_squeeze["day_index"]
            date_str = first_squeeze["date"]
            rain_mm = first_squeeze["precipitation_mm"]
            projected_cash = first_squeeze["projected_cash_lkr"]

            headline = {
                "en": f"Cash Squeeze Expected in {day_idx} Days ({date_str})",
                "si": f"දින {day_idx}කින් මුදල් හිඟයක් බලාපොරොත්තු වේ ({date_str})",
                "ta": f"{day_idx} நாட்களில் பண நெருக்கடி எதிர்பார்க்கப்படுகிறது ({date_str})",
            }
            detail = {
                "en": (
                    f"Severe micro-liquidity risk detected. Anticipated rainfall of {rain_mm:.1f}mm will suppress walk-in "
                    f"customer sales, while rising wholesale restocking requirements risk depleting working capital down to "
                    f"LKR {projected_cash:,.0f}. Cut orders by 20% to 25% this week to protect your operating reserves."
                ),
                "si": (
                    f"දැඩි මුදල් හිඟ අවදානමක් පවතී. අපේක්ෂිත {rain_mm:.1f}mm වර්ෂාපතනය හේතුවෙන් පාරිභෝගික පැමිණීම අඩුවන අතර, "
                    f"තොග මිල ඉහළ යාම නිසා අතැති මුදල් රු. {projected_cash:,.0f} දක්වා අඩුවිය හැක. කාරක ප්‍රාග්ධනය රැක ගැනීමට "
                    f"මෙම සතියේ තොග ඇණවුම් 20%-25% කින් අඩු කරන්න."
                ),
                "ta": (
                    f"கடுமையான பண நெருக்கடி அபாயம் உள்ளது. எதிர்பார்க்கப்படும் {rain_mm:.1f} மி.மீ மழையால் வாடிக்கையாளர் வருகை குறையும். "
                    f"மொத்த விலை உயர்வால் கையிருப்பு பணம் ரூ. {projected_cash:,.0f} ஆக குறையலாம். பணத்தைப் பாதுகாக்க "
                    f"இந்த வாரம் கொள்முதல் ஆர்டர்களை 20%-25% குறைக்கவும்."
                ),
            }
            adj_pct = -20
            urgency = "HIGH"
            suggested_actions = {
                "en": [
                    f"Cut bulk non-perishable restocking orders by 20% prior to {date_str}.",
                    f"Avoid supplier credit purchases with short repayment terms during Day {max(1, day_idx-2)} to Day {day_idx+2}.",
                    "Prioritize high-turnover staples (Rice, Dhal) and delay secondary inventory restocks.",
                ],
                "si": [
                    f"{date_str} දිනට පෙර කල්තබාගත හැකි ද්‍රව්‍ය සඳහා වන තොග ඇණවුම් 20% කින් අඩු කරන්න.",
                    "කෙටි කාලීන ණය මත භාණ්ඩ මිලදී ගැනීමෙන් වළකින්න.",
                    "සහල් සහ පරිප්පු වැනි අත්‍යවශ්‍ය භාණ්ඩ සඳහා ප්‍රමුඛත්වය දෙන්න.",
                ],
                "ta": [
                    f"{date_str} திகதிக்கு முன் பழுதடையாத பொருட்களின் ஆர்டர்களை 20% குறைக்கவும்.",
                    "குறுகிய கால கடன் வாங்குவதைத் தவிர்க்கவும்.",
                    "அரிசி, பருப்பு போன்ற அத்தியாவசிய பொருட்களுக்கு முன்னுரிமை கொடுங்கள்.",
                ],
            }
        elif caution_days:
            first_caution = caution_days[0]
            day_idx = first_caution["day_index"]
            date_str = first_caution["date"]

            headline = {
                "en": f"Moderate Working-Capital Pressure in {day_idx} Days ({date_str})",
                "si": f"දින {day_idx}කින් මධ්‍යස්ථ මුදල් පීඩනයක් ({date_str})",
                "ta": f"{day_idx} நாட்களில் மிதமான பண அழுத்தம் ({date_str})",
            }
            detail = {
                "en": (
                    f"Mild liquidity pressure anticipated due to moderate wholesale price revisions. "
                    f"Maintain tight cash tracking and review purchase orders."
                ),
                "si": "තොග මිල සංශෝධන හේතුවෙන් සුළු මුදල් පීඩනයක් බලාපොරොත්තු වේ. වියදම් හොඳින් කළමනාකරණය කරන්න.",
                "ta": "மொத்த விலை மாற்றங்களால் லேசான பண நெருக்கடி எதிர்பார்க்கப்படுகிறது. செலவுகளை கவனமாக கண்காணிக்கவும்.",
            }
            adj_pct = -10
            urgency = "MEDIUM"
            suggested_actions = {
                "en": [
                    "Trim inventory reorders by 10% on slower-moving goods.",
                    "Verify live wholesale market rates at Pettah before placing large bulk commitments.",
                ],
                "si": [
                    "අඩුවෙන් අලෙවි වන භාණ්ඩ සඳහා ඇණවුම් 10% කින් අඩු කරන්න.",
                    "විශාල තොග මිලදී ගැනීමට පෙර පිටකොටුව තොග මිල පරීක්ෂා කරන්න.",
                ],
                "ta": [
                    "மெதுவாக விற்கும் பொருட்களின் ஆர்டர்களை 10% குறைக்கவும்.",
                    "மொத்தமாக வாங்குவதற்கு முன் புறக்கோட்டை சந்தை விலையை சரிபார்க்கவும்.",
                ],
            }
        else:
            headline = {
                "en": "Liquidity Stable Over Next 14 Days",
                "si": "ඉදිරි දින 14 තුළ මුදල් තත්ත්වය ස්ථාවරයි",
                "ta": "அடுத்த 14 நாட்களில் பணப்புழக்கம் சீராக இருக்கும்",
            }
            detail = {
                "en": "Operating capital is projected to remain healthy across the 14-day forecast window. Maintain standard restocking schedule.",
                "si": "ඉදිරි දින 14 තුළ කාරක ප්‍රාග්ධනය සතුටුදායක මට්ටමක පවතී. සාමාන්‍ය තොග ඇණවුම් ඉදිරියට ගෙන යන්න.",
                "ta": "அடுத்த 14 நாட்களில் பணப்புழக்கம் ஆரோக்கியமாக இருக்கும். வழக்கமான ஆர்டர்களை தொடரவும்.",
            }
            adj_pct = 0
            urgency = "LOW"
            suggested_actions = {
                "en": [
                    "Proceed with regular weekly inventory restocking schedule.",
                    "Take advantage of stable wholesale prices on Samba and Nadu rice.",
                ],
                "si": [
                    "සාමාන්‍ය සතිපතා තොග ඇණවුම් ඉදිරියට ගෙන යන්න.",
                    "සම්බා සහ නාඩු සහල් සඳහා පවතින ස්ථාවර මිලෙන් ප්‍රයෝජන ගන්න.",
                ],
                "ta": [
                    "வழக்கமான வாராந்திர கொள்முதலைத் தொடரவும்.",
                    "சம்பா மற்றும் நாடு அரிசியின் நிலையான விலையைப் பயன்படுத்திக் கொள்ளுங்கள்.",
                ],
            }

        return {
            "action_type": urgency,
            "headline": headline,
            "detail": detail,
            "recommended_order_adjustment_pct": adj_pct,
            "urgency": urgency,
            "suggested_actions": suggested_actions,
        }
