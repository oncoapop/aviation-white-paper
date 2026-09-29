"""
Module 04: August Matched Comparison (Aug 2025 vs Aug 2026)
Generates:
1. white_paper/aug2025_vs_aug2026.csv
2. Simple day-level bootstrap 95% intervals for rate changes.
"""
import numpy as np
import pandas as pd
from pathlib import Path

PASSES_FILE = Path("white_paper/capitol_hill_passes_classified.csv")
OUT_CSV = Path("white_paper/aug2025_vs_aug2026.csv")

def run():
    print("Executing Module 04: August Matched Comparison...")
    df_passes = pd.read_csv(PASSES_FILE)
    
    aug25 = df_passes[df_passes["date"].str.startswith("2025-08")].copy()
    aug26 = df_passes[df_passes["date"].str.startswith("2026-08")].copy()
    
    dates_25 = sorted(aug25["date"].unique())
    dates_26 = sorted(aug26["date"].unique())
    n_days_25 = len(dates_25)
    n_days_26 = len(dates_26)
    
    print(f"August 2025 valid days: {n_days_25} | August 2026 valid days: {n_days_26}")
    
    classes_to_compare = [
        ("Helicopters", "helicopter"),
        ("Light Fixed-Wing GA", "light_fixed_wing_ga"),
        ("Floatplanes / Seaplanes", "floatplane"),
        ("Business Aviation", "business_aviation"),
        ("All Non-VAMP Aviation", "all_non_vamp"),
        ("Non-VAMP Sub-5,000 ft", "non_vamp_sub5k"),
        ("VAMP-Compatible Commercial Passages", "vamp_compatible_commercial"),
        ("Other / Unknown Traffic", "all_other_unknown"),
        ("Total All Passages", "all_total")
    ]
    
    np.random.seed(42)
    rows = []
    
    for label, ckey in classes_to_compare:
        # Filter 2025 and 2026 subsets
        if ckey == "all_non_vamp":
            sub25 = aug25[aug25["parent_class"] == "non_vamp"]
            sub26 = aug26[aug26["parent_class"] == "non_vamp"]
        elif ckey == "non_vamp_sub5k":
            sub25 = aug25[(aug25["parent_class"] == "non_vamp") & (aug25["alt_baro"] < 5000)]
            sub26 = aug26[(aug26["parent_class"] == "non_vamp") & (aug26["alt_baro"] < 5000)]
        elif ckey == "all_other_unknown":
            sub25 = aug25[aug25["parent_class"] == "other_unknown"]
            sub26 = aug26[aug26["parent_class"] == "other_unknown"]
        elif ckey == "all_total":
            sub25 = aug25
            sub26 = aug26
        else:
            sub25 = aug25[aug25["op_class"] == ckey]
            sub26 = aug26[aug26["op_class"] == ckey]
            
        n25 = len(sub25)
        n26 = len(sub26)
        
        r25 = n25 / n_days_25
        r26 = n26 / n_days_26
        
        abs_diff_count = n26 - n25
        abs_diff_rate = r26 - r25
        pct_change = ((r26 - r25) / r25 * 100.0) if r25 > 0 else np.nan
        
        # Medians and IQRs for altitude (MSL ft)
        med_alt_25 = sub25["alt_baro"].median() if n25 > 0 else np.nan
        iqr_alt_25 = (sub25["alt_baro"].quantile(0.75) - sub25["alt_baro"].quantile(0.25)) if n25 > 0 else np.nan
        
        med_alt_26 = sub26["alt_baro"].median() if n26 > 0 else np.nan
        iqr_alt_26 = (sub26["alt_baro"].quantile(0.75) - sub26["alt_baro"].quantile(0.25)) if n26 > 0 else np.nan
        
        # Simple day-level bootstrap for rate difference (4000 resamples)
        # Daily counts
        daily_25 = sub25.groupby("date").size().reindex(dates_25, fill_value=0).values
        daily_26 = sub26.groupby("date").size().reindex(dates_26, fill_value=0).values
        
        boot_diffs = []
        for _ in range(4000):
            b25 = np.random.choice(daily_25, size=n_days_25, replace=True)
            b26 = np.random.choice(daily_26, size=n_days_26, replace=True)
            boot_diffs.append(np.mean(b26) - np.mean(b25))
            
        ci_low = float(np.percentile(boot_diffs, 2.5))
        ci_high = float(np.percentile(boot_diffs, 97.5))
        
        # Stability warning
        is_unstable = (n25 < 30) or (n26 < 30)
        
        rows.append({
            "traffic_class": label,
            "aug2025_count": n25,
            "aug2025_daily_rate": round(r25, 2),
            "aug2026_count": n26,
            "aug2026_daily_rate": round(r26, 2),
            "abs_change_count": abs_diff_count,
            "abs_change_daily_rate": round(abs_diff_rate, 2),
            "pct_change": round(pct_change, 1) if pd.notna(pct_change) else "N/A",
            "rate_diff_boot_95ci": f"[{ci_low:.2f}, {ci_high:.2f}]",
            "aug2025_median_alt_msl": round(med_alt_25, 0) if pd.notna(med_alt_25) else "N/A",
            "aug2025_iqr_alt": round(iqr_alt_25, 0) if pd.notna(iqr_alt_25) else "N/A",
            "aug2026_median_alt_msl": round(med_alt_26, 0) if pd.notna(med_alt_26) else "N/A",
            "aug2026_iqr_alt": round(iqr_alt_26, 0) if pd.notna(iqr_alt_26) else "N/A",
            "small_sample_warning": "Unstable (N < 30)" if is_unstable else "Robust"
        })
        
    df_result = pd.DataFrame(rows)
    df_result.to_csv(OUT_CSV, index=False)
    print(f"Saved August matched comparison to {OUT_CSV}")
    print(df_result[["traffic_class", "aug2025_count", "aug2026_count", "pct_change", "aug2025_median_alt_msl", "aug2026_median_alt_msl"]].to_string(index=False))

if __name__ == "__main__":
    run()
