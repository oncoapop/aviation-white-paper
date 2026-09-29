"""
Module 08: Generate Publication-Quality White Paper Figures
Generates Figures 1 through 5 in white_paper/figures/.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

FIG_DIR = Path("white_paper/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

LOCAL_CSV = Path("white_paper/local_aviation_monthly_2025_2026.csv")
AUG_CSV = Path("white_paper/aug2025_vs_aug2026.csv")
DIURNAL_CSV = Path("white_paper/diurnal_hourly_rates.csv")
ALT_CSV = Path("white_paper/altitude_band_summary.csv")

def set_style():
    plt.rcParams.update({
        'font.sans-serif': 'Helvetica, Arial, DejaVu Sans',
        'font.family': 'sans-serif',
        'figure.titlesize': 14,
        'axes.titlesize': 12,
        'axes.labelsize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.autolayout': True,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--'
    })

def generate_figure1():
    print("Generating Figure 1: Monthly Aviation Activity...")
    df = pd.read_csv(LOCAL_CSV)
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    
    x = np.arange(len(df))
    months = df["month"].tolist()
    
    # Rates
    r_total = df["rate_total_per_day"]
    r_non_vamp = df["rate_non_vamp_per_day"]
    r_vamp = df["rate_vamp_commercial_per_day"]
    
    # Plot lines with markers
    ax.plot(x, r_total, color="#1f77b4", marker="o", linewidth=2.5, label="Combined Total Aviation (Passages/Day)")
    ax.plot(x, r_non_vamp, color="#2ca02c", marker="s", linewidth=2, linestyle="-", label="Non-VAMP Aviation (GA, Heli, Float, Biz)")
    ax.plot(x, r_vamp, color="#d62728", marker="^", linewidth=2.2, linestyle="-", label="VAMP-Compatible Commercial Passages (<10k ft)")
    
    # Highlight 27 Nov 2025 changepoint
    nov_idx = months.index("2025-11")
    ax.axvspan(nov_idx - 0.4, nov_idx + 0.4, color="#ff7f0e", alpha=0.18, label="Transition Month (Nov 2025)")
    ax.axvline(nov_idx, color="#d62728", linestyle="--", linewidth=1.5, alpha=0.8)
    ax.text(nov_idx, ax.get_ylim()[1]*0.92, " 27 Nov 2025\n VAMP Implementation", color="#900C3F", fontweight="bold", fontsize=9)
    
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.set_ylabel("Normalized Rate (Discrete Passages / Valid Day)")
    ax.set_xlabel("Month (Jan 2025 – Aug 2026)")
    ax.set_title("Figure 1: Monthly Aviation Activity Over Capitol Hill (Jan 2025 – Aug 2026)\n"
                 "Baseline Non-VAMP Aviation vs. Superimposed VAMP-Compatible Commercial Arrival Stream", fontweight="bold", pad=12)
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    
    out_file = FIG_DIR / "fig1_monthly_aviation_activity.png"
    plt.savefig(out_file, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file}")

def generate_figure2():
    print("Generating Figure 2: Monthly Composition...")
    df = pd.read_csv(LOCAL_CSV)
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    x = np.arange(len(df))
    months = df["month"].tolist()
    
    # Calculate percentage shares of total passages
    tot = df["total_passages"]
    p_vamp = df["vamp_commercial_passages"] / tot * 100.0
    p_ga = df["light_ga_passages"] / tot * 100.0
    p_heli = df["helicopter_passages"] / tot * 100.0
    p_float = df["floatplane_passages"] / tot * 100.0
    p_biz = df["business_passages"] / tot * 100.0
    p_other = df["other_unknown_passages"] / tot * 100.0
    
    # Stacked bar
    b_vamp = np.zeros(len(df))
    ax.bar(x, p_vamp, bottom=b_vamp, color="#d62728", label="VAMP-Compatible Commercial", width=0.7)
    
    b_ga = p_vamp
    ax.bar(x, p_ga, bottom=b_ga, color="#2ca02c", label="Light Fixed-Wing GA", width=0.7)
    
    b_heli = b_ga + p_ga
    ax.bar(x, p_heli, bottom=b_heli, color="#9467bd", label="Helicopters", width=0.7)
    
    b_float = b_heli + p_heli
    ax.bar(x, p_float, bottom=b_float, color="#17becf", label="Floatplanes / Seaplanes", width=0.7)
    
    b_biz = b_float + p_float
    ax.bar(x, p_biz, bottom=b_biz, color="#e377c2", label="Business Aviation", width=0.7)
    
    b_other = b_biz + p_biz
    ax.bar(x, p_other, bottom=b_other, color="#7f7f7f", label="Other / Unknown", width=0.7)
    
    # Changepoint line
    nov_idx = months.index("2025-11")
    ax.axvline(nov_idx, color="black", linestyle="--", linewidth=1.8)
    ax.text(nov_idx + 0.1, 102, "VAMP Effective (27 Nov 2025)", color="black", fontweight="bold", fontsize=9)
    
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.set_ylabel("Share of Total Discrete Passages (%)")
    ax.set_xlabel("Month (Jan 2025 – Aug 2026)")
    ax.set_ylim(0, 108)
    ax.set_title("Figure 2: Changing Composition of Lower-Altitude Aviation Over Capitol Hill\n"
                 "Pre-VAMP Diversity vs. Post-VAMP Commercial Stream Concentration", fontweight="bold", pad=12)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=True)
    
    out_file = FIG_DIR / "fig2_monthly_composition.png"
    plt.savefig(out_file, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file}")

def generate_figure3():
    print("Generating Figure 3: August Matched Comparison...")
    df = pd.read_csv(AUG_CSV)
    
    # Filter classes of interest
    classes_show = [
        "Helicopters",
        "Light Fixed-Wing GA",
        "Floatplanes / Seaplanes",
        "Business Aviation",
        "All Non-VAMP Aviation",
        "VAMP-Compatible Commercial Passages"
    ]
    sub = df[df["traffic_class"].isin(classes_show)].copy()
    # Sort in specified order
    sub["sort_order"] = sub["traffic_class"].apply(lambda c: classes_show.index(c))
    sub.sort_values(by="sort_order", inplace=True)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    y = np.arange(len(sub))
    height = 0.35
    
    r25 = sub["aug2025_daily_rate"]
    r26 = sub["aug2026_daily_rate"]
    labels = sub["traffic_class"]
    
    bars1 = ax.barh(y - height/2, r25, height, label="August 2025 (Baseline, N=30 days)", color="#4682b4")
    bars2 = ax.barh(y + height/2, r26, height, label="August 2026 (Post-VAMP, N=30 days)", color="#e41a1c")
    
    # Add values at bar tips
    for b in bars1:
        val = b.get_width()
        ax.text(val + 0.8, b.get_y() + b.get_height()/2, f"{val:.1f}/d", va="center", fontsize=8, color="#2b5c8f")
    for b in bars2:
        val = b.get_width()
        ax.text(val + 0.8, b.get_y() + b.get_height()/2, f"{val:.1f}/d", va="center", fontsize=8, color="#b30000", fontweight="bold")
        
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Daily Rate (Passages per Valid Observation Day)")
    ax.set_title("Figure 3: August Season-Matched Comparison (Aug 2025 vs Aug 2026)\n"
                 "Quantifying Local Baseline Evolution Alongside New Commercial Stream", fontweight="bold", pad=12)
    ax.legend(loc="lower right", frameon=True)
    ax.set_xlim(0, max(r26)*1.15)
    
    out_file = FIG_DIR / "fig3_aug2025_vs_aug2026_comparison.png"
    plt.savefig(out_file, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file}")

def generate_figure4():
    print("Generating Figure 4: 24-Hour Diurnal Profile...")
    df = pd.read_csv(DIURNAL_CSV)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True, dpi=300)
    
    hours = df["hour"]
    
    # August 2025
    ax1.bar(hours - 0.2, df["aug25_non_vamp_mean"], width=0.4, label="Non-VAMP Aviation", color="#2ca02c")
    ax1.bar(hours + 0.2, df["aug25_vamp_mean"], width=0.4, label="VAMP Commercial (<10k ft)", color="#d62728")
    ax1.set_title("August 2025 (Baseline Pre-VAMP)", fontweight="bold")
    ax1.set_xlabel("Local Hour of Day (00:00 – 23:00 PDT)")
    ax1.set_ylabel("Average Passages per Hour")
    ax1.set_xticks(range(0, 24, 2))
    ax1.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], rotation=45)
    ax1.legend(loc="upper left")
    
    # August 2026
    ax2.bar(hours - 0.2, df["aug26_non_vamp_mean"], width=0.4, label="Non-VAMP Aviation", color="#2ca02c")
    ax2.bar(hours + 0.2, df["aug26_vamp_mean"], width=0.4, label="VAMP Commercial (<10k ft)", color="#d62728")
    ax2.set_title("August 2026 (Post-VAMP Superimposition)", fontweight="bold")
    ax2.set_xlabel("Local Hour of Day (00:00 – 23:00 PDT)")
    ax2.set_xticks(range(0, 24, 2))
    ax2.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], rotation=45)
    ax2.legend(loc="upper left")
    
    fig.suptitle("Figure 4: 24-Hour Diurnal Activity Profiles Over Capitol Hill\n"
                 "Demonstrating Extensive Daytime Temporal Overlap and Evening Superimposition", fontweight="bold", y=1.03)
    
    out_file = FIG_DIR / "fig4_diurnal_24hr_profile.png"
    plt.savefig(out_file, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file}")

def generate_figure5():
    print("Generating Figure 5: Altitude Band Distribution...")
    df = pd.read_csv(ALT_CSV)
    
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    
    bands = df["altitude_band_msl"].tolist()
    x = np.arange(len(bands))
    width = 0.2
    
    # Plot 4 bars per band:
    # 1. Aug 25 Non-VAMP
    # 2. Aug 26 Non-VAMP
    # 3. Aug 25 VAMP Commercial
    # 4. Aug 26 VAMP Commercial
    b1 = ax.bar(x - 1.5*width, df["aug2025_non_vamp_rate"], width, label="Aug 2025 Non-VAMP", color="#74c476")
    b2 = ax.bar(x - 0.5*width, df["aug2026_non_vamp_rate"], width, label="Aug 2026 Non-VAMP", color="#238b45")
    b3 = ax.bar(x + 0.5*width, df["aug2025_vamp_commercial_rate"], width, label="Aug 2025 VAMP Commercial", color="#fb6a4a")
    b4 = ax.bar(x + 1.5*width, df["aug2026_vamp_commercial_rate"], width, label="Aug 2026 VAMP Commercial", color="#cb181d")
    
    ax.set_xticks(x)
    ax.set_xticklabels(bands, fontsize=10)
    ax.set_ylabel("Daily Rate (Passages per Valid Day)")
    ax.set_xlabel("Altitude Band (Mean Sea Level, Barometric)")
    ax.set_title("Figure 5: Stratified Altitude Distribution (Aug 2025 vs Aug 2026)\n"
                 "Pre-Existing Lower-Altitude Traffic (<3k ft) vs Superimposed Arrival Stream (5k–10k ft)", fontweight="bold", pad=12)
    ax.legend(loc="upper left", frameon=True)
    
    out_file = FIG_DIR / "fig5_altitude_band_distribution.png"
    plt.savefig(out_file, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file}")

def run():
    set_style()
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    generate_figure5()
    print("All Figures 1-5 successfully generated.")

if __name__ == "__main__":
    run()
