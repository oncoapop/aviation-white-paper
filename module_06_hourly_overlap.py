"""
Module 06: Hourly Overlap and Diurnal Distribution
Generates white_paper/hourly_overlap.csv.
Analyzes 24-hour diurnal activity profile and temporal overlap between non-VAMP aviation
and VAMP-compatible commercial traffic in August 2025 vs August 2026.
"""
import numpy as np
import pandas as pd
from pathlib import Path

PASSES_FILE = Path("white_paper/capitol_hill_passes_classified.csv")
OUT_CSV = Path("white_paper/hourly_overlap.csv")
OUT_PROFILE_CSV = Path("white_paper/diurnal_hourly_rates.csv")

def run():
    print("Executing Module 06: Hourly Overlap and Diurnal Profiles...")
    df_passes = pd.read_csv(PASSES_FILE)
    
    # Calculate local timestamp and local hour in America/Vancouver
    ts_local = pd.to_datetime(df_passes["cpa_timestamp"], unit="s", utc=True).dt.tz_convert("America/Vancouver")
    df_passes["local_hour"] = ts_local.dt.hour
    df_passes["local_date"] = ts_local.dt.strftime("%Y-%m-%d")
    
    # Restrict to August 2025 and August 2026 based on local_date
    aug25 = df_passes[df_passes["local_date"].str.startswith("2025-08")].copy()
    aug26 = df_passes[df_passes["local_date"].str.startswith("2026-08")].copy()
    
    # Unique dates
    dates_25 = sorted(aug25["local_date"].unique())
    dates_26 = sorted(aug26["local_date"].unique())
    n_days_25 = len(dates_25)
    n_days_26 = len(dates_26)
    
    print(f"Local August 2025 days: {n_days_25} | Local August 2026 days: {n_days_26}")
    
    # Create complete grid of (date, hour) for all valid days
    def build_grid(dates):
        grid = []
        for d in dates:
            for h in range(24):
                grid.append({"date": d, "hour": h})
        return pd.DataFrame(grid)
        
    grid25 = build_grid(dates_25)
    grid26 = build_grid(dates_26)
    
    # Count passes per date-hour by stream
    def aggregate_grid(df_sub, grid):
        counts = df_sub.groupby(["local_date", "local_hour", "parent_class"]).size().unstack(fill_value=0).reset_index()
        counts.rename(columns={"local_date": "date", "local_hour": "hour"}, inplace=True)
        
        merged = pd.merge(grid, counts, on=["date", "hour"], how="left").fillna(0)
        if "non_vamp" not in merged.columns:
            merged["non_vamp"] = 0
        if "vamp_compatible_commercial" not in merged.columns:
            merged["vamp_compatible_commercial"] = 0
        if "other_unknown" not in merged.columns:
            merged["other_unknown"] = 0
            
        merged["has_non_vamp"] = merged["non_vamp"] > 0
        merged["has_vamp"] = merged["vamp_compatible_commercial"] > 0
        
        def overlap_type(r):
            nv = r["has_non_vamp"]
            vc = r["has_vamp"]
            if nv and vc:
                return "both"
            elif nv and not vc:
                return "only_non_vamp"
            elif not nv and vc:
                return "only_vamp_commercial"
            else:
                return "neither"
                
        merged["overlap_status"] = merged.apply(overlap_type, axis=1)
        merged["total"] = merged["non_vamp"] + merged["vamp_compatible_commercial"] + merged["other_unknown"]
        return merged
        
    grid25_agg = aggregate_grid(aug25, grid25)
    grid26_agg = aggregate_grid(aug26, grid26)
    
    # 1. Overall Overlap Summary
    total_hours_25 = len(grid25_agg)
    total_hours_26 = len(grid26_agg)
    
    s25 = grid25_agg["overlap_status"].value_counts()
    s26 = grid26_agg["overlap_status"].value_counts()
    
    overlap_rows = [
        {
            "category": "Hours with BOTH non-VAMP and VAMP-compatible traffic",
            "aug2025_hours": s25.get("both", 0),
            "aug2025_pct": round(s25.get("both", 0) / total_hours_25 * 100.0, 1),
            "aug2026_hours": s26.get("both", 0),
            "aug2026_pct": round(s26.get("both", 0) / total_hours_26 * 100.0, 1)
        },
        {
            "category": "Hours with ONLY non-VAMP aviation",
            "aug2025_hours": s25.get("only_non_vamp", 0),
            "aug2025_pct": round(s25.get("only_non_vamp", 0) / total_hours_25 * 100.0, 1),
            "aug2026_hours": s26.get("only_non_vamp", 0),
            "aug2026_pct": round(s26.get("only_non_vamp", 0) / total_hours_26 * 100.0, 1)
        },
        {
            "category": "Hours with ONLY VAMP-compatible commercial traffic",
            "aug2025_hours": s25.get("only_vamp_commercial", 0),
            "aug2025_pct": round(s25.get("only_vamp_commercial", 0) / total_hours_25 * 100.0, 1),
            "aug2026_hours": s26.get("only_vamp_commercial", 0),
            "aug2026_pct": round(s26.get("only_vamp_commercial", 0) / total_hours_26 * 100.0, 1)
        },
        {
            "category": "Hours with NEITHER stream (Quiet Hours)",
            "aug2025_hours": s25.get("neither", 0),
            "aug2025_pct": round(s25.get("neither", 0) / total_hours_25 * 100.0, 1),
            "aug2026_hours": s26.get("neither", 0),
            "aug2026_pct": round(s26.get("neither", 0) / total_hours_26 * 100.0, 1)
        },
        {
            "category": "Total Valid Observation Hours",
            "aug2025_hours": total_hours_25,
            "aug2025_pct": 100.0,
            "aug2026_hours": total_hours_26,
            "aug2026_pct": 100.0
        }
    ]
    df_overlap = pd.DataFrame(overlap_rows)
    df_overlap.to_csv(OUT_CSV, index=False)
    print(f"Saved hourly overlap summary to {OUT_CSV}")
    print(df_overlap.to_string(index=False))
    
    # 2. Hourly Profile (by hour 0..23)
    p25 = grid25_agg.groupby("hour").agg(
        aug25_non_vamp_mean=("non_vamp", "mean"),
        aug25_vamp_mean=("vamp_compatible_commercial", "mean"),
        aug25_total_mean=("total", "mean")
    ).reset_index()
    
    p26 = grid26_agg.groupby("hour").agg(
        aug26_non_vamp_mean=("non_vamp", "mean"),
        aug26_vamp_mean=("vamp_compatible_commercial", "mean"),
        aug26_total_mean=("total", "mean")
    ).reset_index()
    
    p_merged = pd.merge(p25, p26, on="hour").round(2)
    p_merged.to_csv(OUT_PROFILE_CSV, index=False)
    print(f"Saved 24-hour diurnal profile to {OUT_PROFILE_CSV}")

if __name__ == "__main__":
    run()
