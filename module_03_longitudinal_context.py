"""
Module 03: Longitudinal Context (20-Month Time-Series)
Generates:
1. white_paper/local_aviation_monthly_2025_2026.csv
2. white_paper/vamp_compatible_commercial_monthly.csv
3. Monthly composition of aviation activity over Capitol Hill.
"""
import pandas as pd
from pathlib import Path

PASSES_FILE = Path("white_paper/capitol_hill_passes_classified.csv")
COVERAGE_FILE = Path("white_paper/data_coverage_monthly.csv")
OUT_LOCAL_CSV = Path("white_paper/local_aviation_monthly_2025_2026.csv")
OUT_VAMP_CSV = Path("white_paper/vamp_compatible_commercial_monthly.csv")

def run():
    print("Executing Module 03: Longitudinal Context...")
    df_passes = pd.read_csv(PASSES_FILE)
    df_cov = pd.read_csv(COVERAGE_FILE)
    
    # Month string
    df_passes["month"] = df_passes["date"].str.slice(0, 7)
    
    months = sorted(df_cov["month"].unique())
    records = []
    vamp_records = []
    
    for m in months:
        cov_row = df_cov[df_cov["month"] == m].iloc[0]
        vdays = cov_row["valid_days"]
        cdays = cov_row["calendar_days"]
        
        m_passes = df_passes[df_passes["month"] == m]
        n_total = len(m_passes)
        
        # Operational classes
        n_vamp = len(m_passes[m_passes["op_class"] == "vamp_compatible_commercial"])
        n_ga = len(m_passes[m_passes["op_class"] == "light_fixed_wing_ga"])
        n_heli = len(m_passes[m_passes["op_class"] == "helicopter"])
        n_float = len(m_passes[m_passes["op_class"] == "floatplane"])
        n_biz = len(m_passes[m_passes["op_class"] == "business_aviation"])
        n_non_vamp = n_ga + n_heli + n_float + n_biz
        
        # Non-VAMP sub-5,000 ft
        m_non_vamp = m_passes[m_passes["parent_class"] == "non_vamp"]
        n_non_vamp_sub5k = len(m_non_vamp[m_non_vamp["alt_baro"] < 5000])
        
        # Other/Unknown
        n_other_comm = len(m_passes[m_passes["op_class"] == "other_commercial"])
        n_unclass = len(m_passes[m_passes["op_class"] == "other_unclassifiable"])
        n_other_unknown = n_other_comm + n_unclass
        
        # Normalization (rate per valid observation day)
        r_total = n_total / vdays if vdays > 0 else 0.0
        r_vamp = n_vamp / vdays if vdays > 0 else 0.0
        r_non_vamp = n_non_vamp / vdays if vdays > 0 else 0.0
        r_non_vamp_sub5k = n_non_vamp_sub5k / vdays if vdays > 0 else 0.0
        r_ga = n_ga / vdays if vdays > 0 else 0.0
        r_heli = n_heli / vdays if vdays > 0 else 0.0
        r_float = n_float / vdays if vdays > 0 else 0.0
        r_biz = n_biz / vdays if vdays > 0 else 0.0
        r_other = n_other_unknown / vdays if vdays > 0 else 0.0
        
        # Proportions
        pct_non_vamp = (n_non_vamp / n_total * 100.0) if n_total > 0 else 0.0
        pct_vamp = (n_vamp / n_total * 100.0) if n_total > 0 else 0.0
        pct_other = (n_other_unknown / n_total * 100.0) if n_total > 0 else 0.0
        
        # Era
        if m < "2025-11":
            era = "Pre-VAMP"
        elif m == "2025-11":
            era = "Transition"
        else:
            era = "Post-VAMP"
            
        records.append({
            "month": m,
            "era": era,
            "calendar_days": cdays,
            "valid_days": vdays,
            "total_passages": n_total,
            "rate_total_per_day": round(r_total, 2),
            "non_vamp_passages": n_non_vamp,
            "rate_non_vamp_per_day": round(r_non_vamp, 2),
            "non_vamp_sub5k_passages": n_non_vamp_sub5k,
            "rate_non_vamp_sub5k_per_day": round(r_non_vamp_sub5k, 2),
            "vamp_commercial_passages": n_vamp,
            "rate_vamp_commercial_per_day": round(r_vamp, 2),
            "helicopter_passages": n_heli,
            "rate_helicopter_per_day": round(r_heli, 2),
            "light_ga_passages": n_ga,
            "rate_light_ga_per_day": round(r_ga, 2),
            "floatplane_passages": n_float,
            "rate_floatplane_per_day": round(r_float, 2),
            "business_passages": n_biz,
            "rate_business_per_day": round(r_biz, 2),
            "other_unknown_passages": n_other_unknown,
            "rate_other_unknown_per_day": round(r_other, 2),
            "pct_share_non_vamp": round(pct_non_vamp, 1),
            "pct_share_vamp_commercial": round(pct_vamp, 1),
            "pct_share_other_unknown": round(pct_other, 1)
        })
        
        # VAMP detailed breakdown (Eastbound vs Westbound)
        m_vamp = m_passes[m_passes["op_class"] == "vamp_compatible_commercial"]
        n_eb = len(m_vamp[(m_vamp["track"] >= 60) & (m_vamp["track"] <= 120)])
        n_wb = len(m_vamp[(m_vamp["track"] >= 240) & (m_vamp["track"] <= 300)])
        r_eb = n_eb / vdays if vdays > 0 else 0.0
        r_wb = n_wb / vdays if vdays > 0 else 0.0
        
        med_alt = m_vamp["alt_baro"].median() if len(m_vamp) > 0 else None
        iqr_alt = (m_vamp["alt_baro"].quantile(0.75) - m_vamp["alt_baro"].quantile(0.25)) if len(m_vamp) > 0 else None
        
        vamp_records.append({
            "month": m,
            "era": era,
            "valid_days": vdays,
            "vamp_commercial_total": n_vamp,
            "vamp_commercial_daily_rate": round(r_vamp, 2),
            "eastbound_downwind_passages": n_eb,
            "eastbound_daily_rate": round(r_eb, 2),
            "westbound_downwind_passages": n_wb,
            "westbound_daily_rate": round(r_wb, 2),
            "median_alt_ft_msl": round(med_alt, 1) if med_alt is not None else "N/A",
            "iqr_alt_ft": round(iqr_alt, 1) if iqr_alt is not None else "N/A"
        })
        
    df_out = pd.DataFrame(records)
    df_out.to_csv(OUT_LOCAL_CSV, index=False)
    print(f"Saved monthly local aviation context to {OUT_LOCAL_CSV}")
    
    df_vamp_out = pd.DataFrame(vamp_records)
    df_vamp_out.to_csv(OUT_VAMP_CSV, index=False)
    print(f"Saved monthly VAMP commercial context to {OUT_VAMP_CSV}")

if __name__ == "__main__":
    run()
