"""
Module 07: Special Categories Analysis (Helicopters and Floatplanes)
Generates:
1. white_paper/helicopter_monthly.csv
2. white_paper/floatplane_monthly.csv
3. Registration concentration and airframe analysis.
"""
import pandas as pd
from pathlib import Path

PASSES_FILE = Path("white_paper/capitol_hill_passes_classified.csv")
ALL_FLIGHTS_FILE = Path("data/capitol_hill_all_flights.csv")
COVERAGE_FILE = Path("white_paper/data_coverage_monthly.csv")

OUT_HELI_CSV = Path("white_paper/helicopter_monthly.csv")
OUT_FLOAT_CSV = Path("white_paper/floatplane_monthly.csv")
OUT_HELI_REG_CSV = Path("white_paper/helicopter_registrations_august.csv")

def run():
    print("Executing Module 07: Special Categories Analysis...")
    df_passes = pd.read_csv(PASSES_FILE)
    df_all = pd.read_csv(ALL_FLIGHTS_FILE)
    df_cov = pd.read_csv(COVERAGE_FILE)
    
    # Merge registration from df_all onto passes via flight_id
    id_to_reg = dict(zip(df_all["id"], df_all["registration"]))
    id_to_callsign = dict(zip(df_all["id"], df_all["callsign"]))
    df_passes["registration"] = df_passes["flight_id"].map(id_to_reg).fillna("UNKNOWN")
    df_passes["callsign"] = df_passes["flight_id"].map(id_to_callsign).fillna("")
    
    df_passes["month"] = df_passes["date"].str.slice(0, 7)
    months = sorted(df_cov["month"].unique())
    
    # 1. Monthly Helicopters
    heli_passes = df_passes[df_passes["op_class"] == "helicopter"].copy()
    heli_rows = []
    
    for m in months:
        cov_row = df_cov[df_cov["month"] == m].iloc[0]
        vdays = cov_row["valid_days"]
        
        m_h = heli_passes[heli_passes["month"] == m]
        n_h = len(m_h)
        r_h = n_h / vdays if vdays > 0 else 0.0
        
        # Sub-2000 ft helicopters
        n_low = len(m_h[m_h["alt_baro"] < 2000])
        r_low = n_low / vdays if vdays > 0 else 0.0
        
        # Specific dominant types
        n_s76 = len(m_h[m_h["type_code"] == "S76"])
        n_r44 = len(m_h[m_h["type_code"] == "R44"])
        n_a139 = len(m_h[m_h["type_code"] == "A139"])
        n_as50 = len(m_h[m_h["type_code"] == "AS50"])
        n_b06 = len(m_h[m_h["type_code"] == "B06"])
        
        med_alt = m_h["alt_baro"].median() if n_h > 0 else None
        
        heli_rows.append({
            "month": m,
            "valid_days": vdays,
            "helicopter_total_passages": n_h,
            "helicopter_daily_rate": round(r_h, 2),
            "sub_2000ft_passages": n_low,
            "sub_2000ft_daily_rate": round(r_low, 2),
            "count_S76": n_s76,
            "count_R44": n_r44,
            "count_A139": n_a139,
            "count_AS50": n_as50,
            "count_B06": n_b06,
            "median_alt_msl": round(med_alt, 0) if med_alt is not None else "N/A"
        })
        
    df_heli_out = pd.DataFrame(heli_rows)
    df_heli_out.to_csv(OUT_HELI_CSV, index=False)
    print(f"Saved helicopter monthly metrics to {OUT_HELI_CSV}")
    
    # 2. Monthly Floatplanes
    float_passes = df_passes[df_passes["op_class"] == "floatplane"].copy()
    float_rows = []
    
    for m in months:
        cov_row = df_cov[df_cov["month"] == m].iloc[0]
        vdays = cov_row["valid_days"]
        
        m_f = float_passes[float_passes["month"] == m]
        n_f = len(m_f)
        r_f = n_f / vdays if vdays > 0 else 0.0
        
        n_dhc2 = len(m_f[m_f["type_code"] == "DHC2"])
        n_dhc3 = len(m_f[m_f["type_code"] == "DHC3"])
        n_dhc6 = len(m_f[m_f["type_code"] == "DHC6"])
        n_dh2t = len(m_f[m_f["type_code"] == "DH2T"])
        n_dh3t = len(m_f[m_f["type_code"] == "DH3T"])
        
        med_alt = m_f["alt_baro"].median() if n_f > 0 else None
        
        float_rows.append({
            "month": m,
            "valid_days": vdays,
            "floatplane_total_passages": n_f,
            "floatplane_daily_rate": round(r_f, 2),
            "count_DHC2_Beaver": n_dhc2,
            "count_DHC3_Otter": n_dhc3,
            "count_DHC6_TwinOtter": n_dhc6,
            "count_DH2T_TurboBeaver": n_dh2t,
            "count_DH3T_TurboOtter": n_dh3t,
            "median_alt_msl": round(med_alt, 0) if med_alt is not None else "N/A"
        })
        
    df_float_out = pd.DataFrame(float_rows)
    df_float_out.to_csv(OUT_FLOAT_CSV, index=False)
    print(f"Saved floatplane monthly metrics to {OUT_FLOAT_CSV}")
    
    # 3. Helicopter Registration Analysis (August 2025 vs August 2026)
    h25 = heli_passes[heli_passes["date"].str.startswith("2025-08")]
    h26 = heli_passes[heli_passes["date"].str.startswith("2026-08")]
    
    reg25 = h25["registration"].value_counts().reset_index()
    reg25.columns = ["registration", "aug2025_count"]
    
    reg26 = h26["registration"].value_counts().reset_index()
    reg26.columns = ["registration", "aug2026_count"]
    
    reg_comp = pd.merge(reg26, reg25, on="registration", how="outer").fillna(0)
    reg_comp["aug2025_count"] = reg_comp["aug2025_count"].astype(int)
    reg_comp["aug2026_count"] = reg_comp["aug2026_count"].astype(int)
    reg_comp["abs_change"] = reg_comp["aug2026_count"] - reg_comp["aug2025_count"]
    reg_comp.sort_values(by="aug2026_count", ascending=False, inplace=True)
    
    reg_comp.to_csv(OUT_HELI_REG_CSV, index=False)
    print(f"Saved helicopter registration comparison to {OUT_HELI_REG_CSV}")
    print("\nTop 10 Helicopter Registrations in August 2026 vs August 2025:")
    print(reg_comp.head(10).to_string(index=False))

if __name__ == "__main__":
    run()
