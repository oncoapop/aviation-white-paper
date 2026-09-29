"""
Module 05: Altitude Distribution and Context
Generates white_paper/altitude_band_summary.csv.
Stratifies August 2025 and August 2026 traffic by 6 standardized altitude bands:
<1,000 ft, 1,000-2,000 ft, 2,000-3,000 ft, 3,000-5,000 ft, 5,000-10,000 ft, ≥10,000 ft (MSL).
"""
import pandas as pd
from pathlib import Path

PASSES_FILE = Path("white_paper/capitol_hill_passes_classified.csv")
OUT_CSV = Path("white_paper/altitude_band_summary.csv")

ALT_BANDS = [
    "<1,000 ft",
    "1,000-2,000 ft",
    "2,000-3,000 ft",
    "3,000-5,000 ft",
    "5,000-10,000 ft",
    "≥10,000 ft"
]

def run():
    print("Executing Module 05: Altitude Distribution...")
    df_passes = pd.read_csv(PASSES_FILE)
    
    aug25 = df_passes[df_passes["date"].str.startswith("2025-08")].copy()
    aug26 = df_passes[df_passes["date"].str.startswith("2026-08")].copy()
    
    rows = []
    
    for band in ALT_BANDS:
        b25 = aug25[aug25["alt_band"] == band]
        b26 = aug26[aug26["alt_band"] == band]
        
        # Breakdown by class in 2025
        n25_total = len(b25)
        n25_non_vamp = len(b25[b25["parent_class"] == "non_vamp"])
        n25_heli = len(b25[b25["op_class"] == "helicopter"])
        n25_ga = len(b25[b25["op_class"] == "light_fixed_wing_ga"])
        n25_float = len(b25[b25["op_class"] == "floatplane"])
        n25_biz = len(b25[b25["op_class"] == "business_aviation"])
        n25_vamp = len(b25[b25["op_class"] == "vamp_compatible_commercial"])
        n25_other = len(b25[b25["parent_class"] == "other_unknown"])
        
        # Breakdown by class in 2026
        n26_total = len(b26)
        n26_non_vamp = len(b26[b26["parent_class"] == "non_vamp"])
        n26_heli = len(b26[b26["op_class"] == "helicopter"])
        n26_ga = len(b26[b26["op_class"] == "light_fixed_wing_ga"])
        n26_float = len(b26[b26["op_class"] == "floatplane"])
        n26_biz = len(b26[b26["op_class"] == "business_aviation"])
        n26_vamp = len(b26[b26["op_class"] == "vamp_compatible_commercial"])
        n26_other = len(b26[b26["parent_class"] == "other_unknown"])
        
        # Rates (per valid day, N=30 for each)
        r25_total = n25_total / 30.0
        r26_total = n26_total / 30.0
        r25_non_vamp = n25_non_vamp / 30.0
        r26_non_vamp = n26_non_vamp / 30.0
        r25_vamp = n25_vamp / 30.0
        r26_vamp = n26_vamp / 30.0
        
        pct_change_non_vamp = ((r26_non_vamp - r25_non_vamp) / r25_non_vamp * 100.0) if r25_non_vamp > 0 else (np.nan if r26_non_vamp == 0 else 999.0)
        pct_change_total = ((r26_total - r25_total) / r25_total * 100.0) if r25_total > 0 else np.nan
        
        rows.append({
            "altitude_band_msl": band,
            "aug2025_total_count": n25_total,
            "aug2025_total_rate": round(r25_total, 2),
            "aug2026_total_count": n26_total,
            "aug2026_total_rate": round(r26_total, 2),
            "abs_change_total_rate": round(r26_total - r25_total, 2),
            "pct_change_total": round(pct_change_total, 1),
            "aug2025_non_vamp_count": n25_non_vamp,
            "aug2025_non_vamp_rate": round(r25_non_vamp, 2),
            "aug2026_non_vamp_count": n26_non_vamp,
            "aug2026_non_vamp_rate": round(r26_non_vamp, 2),
            "aug2025_vamp_commercial_count": n25_vamp,
            "aug2025_vamp_commercial_rate": round(r25_vamp, 2),
            "aug2026_vamp_commercial_count": n26_vamp,
            "aug2026_vamp_commercial_rate": round(r26_vamp, 2),
            "aug2025_heli_count": n25_heli,
            "aug2026_heli_count": n26_heli,
            "aug2025_ga_count": n25_ga,
            "aug2026_ga_count": n26_ga,
            "aug2025_float_count": n25_float,
            "aug2026_float_count": n26_float,
            "aug2025_biz_count": n25_biz,
            "aug2026_biz_count": n26_biz,
            "aug2025_other_count": n25_other,
            "aug2026_other_count": n26_other
        })
        
    df_result = pd.DataFrame(rows)
    df_result.to_csv(OUT_CSV, index=False)
    print(f"Saved altitude band summary to {OUT_CSV}")
    print(df_result[["altitude_band_msl", "aug2025_non_vamp_count", "aug2026_non_vamp_count", "aug2025_vamp_commercial_count", "aug2026_vamp_commercial_count", "aug2025_total_count", "aug2026_total_count"]].to_string(index=False))

if __name__ == "__main__":
    run()
