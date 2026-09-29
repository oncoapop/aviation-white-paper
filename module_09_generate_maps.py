"""
Module 09: Generate Trajectory Track Maps
Generates Maps 1 through 4 in white_paper/figures/:
- Map 1: August 2025 non-VAMP tracks
- Map 2: August 2026 non-VAMP tracks
- Map 3: August 2026 VAMP-compatible commercial tracks
- Map 4: Combined August 2026 aviation environment
"""
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

FIG_DIR = Path("white_paper/figures")
ALL_FLIGHTS_FILE = Path("data/capitol_hill_all_flights.csv")
PASSES_CLASSIFIED = Path("white_paper/capitol_hill_passes_classified.csv")

# Capitol Hill Reference Center
CH_LAT = 49.2869
CH_LON = -122.9853
RADIUS_KM = 1.5

def get_circle_coords(lat, lon, r_km, n_points=100):
    # 1 deg lat ~ 111.139 km
    # 1 deg lon ~ 111.139 * cos(lat) km
    dlat = r_km / 111.139
    dlon = r_km / (111.139 * np.cos(np.radians(lat)))
    angles = np.linspace(0, 2*np.pi, n_points)
    circle_lats = lat + dlat * np.sin(angles)
    circle_lons = lon + dlon * np.cos(angles)
    return circle_lons, circle_lats

def prepare_trajectories():
    print("Loading trajectory data for maps...")
    df_all = pd.read_csv(ALL_FLIGHTS_FILE)
    df_passes = pd.read_csv(PASSES_CLASSIFIED)
    
    # Map flight_id to primary op_class and parent_class
    id_to_op = dict(zip(df_passes["flight_id"], df_passes["op_class"]))
    id_to_parent = dict(zip(df_passes["flight_id"], df_passes["parent_class"]))
    
    df_all["op_class"] = df_all["id"].map(id_to_op).fillna("other_unclassifiable")
    df_all["parent_class"] = df_all["id"].map(id_to_parent).fillna("other_unknown")
    
    # Filter August 2025 and August 2026
    aug25 = df_all[df_all["date"].str.startswith("2025-08")].copy()
    aug26 = df_all[df_all["date"].str.startswith("2026-08")].copy()
    
    def extract_lines(df_sub):
        lines = []
        for _, row in df_sub.iterrows():
            pts_raw = row["matched_points_json"]
            if not isinstance(pts_raw, str):
                continue
            pts = json.loads(pts_raw)
            if len(pts) < 2:
                continue
            lats = [p["lat"] for p in pts]
            lons = [p["lon"] for p in pts]
            lines.append({
                "flight_id": row["id"],
                "lats": lats,
                "lons": lons,
                "op_class": row["op_class"],
                "parent_class": row["parent_class"],
                "type_code": row["type_code"],
                "callsign": row["callsign"]
            })
        return lines
        
    lines_25 = extract_lines(aug25)
    lines_26 = extract_lines(aug26)
    
    return lines_25, lines_26

def plot_base_map(ax, title):
    # Capitol Hill 1.5 km study cylinder
    c_lons, c_lats = get_circle_coords(CH_LAT, CH_LON, RADIUS_KM)
    ax.plot(c_lons, c_lats, color="black", linestyle="--", linewidth=1.5, label="1.5 km Study Cylinder")
    
    # Summit marker
    ax.plot(CH_LON, CH_LAT, marker="*", color="black", markersize=10, label="Capitol Hill Summit (49.2869°N, 122.9853°W)")
    
    # Bounding box
    ax.set_xlim(-123.015, -122.955)
    ax.set_ylim(49.268, 49.308)
    
    ax.set_aspect(1.0 / np.cos(np.radians(CH_LAT)))
    ax.set_xlabel("Longitude (° W)", fontsize=10)
    ax.set_ylabel("Latitude (° N)", fontsize=10)
    ax.set_title(title, fontweight="bold", pad=12, fontsize=11)
    ax.grid(True, linestyle=":", alpha=0.5)

def run():
    lines_25, lines_26 = prepare_trajectories()
    
    color_map = {
        "light_fixed_wing_ga": "#2ca02c",  # Green
        "helicopter": "#9467bd",           # Purple
        "floatplane": "#17becf",           # Cyan
        "business_aviation": "#e377c2",    # Pink
        "vamp_compatible_commercial": "#d62728", # Red
        "other_commercial": "#7f7f7f",     # Gray
        "other_unclassifiable": "#bcbd22"  # Olive
    }
    
    # ---------------- MAP 1: August 2025 Non-VAMP Tracks ----------------
    print("Generating Map 1: August 2025 Non-VAMP Tracks...")
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    plot_base_map(ax, "Map 1: August 2025 Non-VAMP Trajectories (Baseline)\n"
                      "Pre-Existing Multi-Directional General Aviation, Helicopters & Floatplanes")
    
    n_plotted = 0
    legend_added = set()
    for l in lines_25:
        if l["parent_class"] == "non_vamp":
            c = color_map.get(l["op_class"], "#333333")
            lbl = l["op_class"].replace("_", " ").title() if l["op_class"] not in legend_added else ""
            if lbl:
                legend_added.add(l["op_class"])
            ax.plot(l["lons"], l["lats"], color=c, alpha=0.4, linewidth=1.2, label=lbl)
            n_plotted += 1
            
    ax.text(0.03, 0.03, f"Total Trajectories: {n_plotted}", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8), fontsize=9)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9, fontsize=8)
    
    out1 = FIG_DIR / "map1_aug2025_non_vamp_tracks.png"
    plt.savefig(out1, bbox_inches="tight")
    plt.close()
    print(f"Saved {out1}")
    
    # ---------------- MAP 2: August 2026 Non-VAMP Tracks ----------------
    print("Generating Map 2: August 2026 Non-VAMP Tracks...")
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    plot_base_map(ax, "Map 2: August 2026 Non-VAMP Trajectories\n"
                      "Evolving Background Aviation Including Concentrated Helicopter Activity")
    
    n_plotted = 0
    legend_added = set()
    for l in lines_26:
        if l["parent_class"] == "non_vamp":
            c = color_map.get(l["op_class"], "#333333")
            lbl = l["op_class"].replace("_", " ").title() if l["op_class"] not in legend_added else ""
            if lbl:
                legend_added.add(l["op_class"])
            ax.plot(l["lons"], l["lats"], color=c, alpha=0.4, linewidth=1.2, label=lbl)
            n_plotted += 1
            
    ax.text(0.03, 0.03, f"Total Trajectories: {n_plotted}", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8), fontsize=9)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9, fontsize=8)
    
    out2 = FIG_DIR / "map2_aug2026_non_vamp_tracks.png"
    plt.savefig(out2, bbox_inches="tight")
    plt.close()
    print(f"Saved {out2}")
    
    # ---------------- MAP 3: August 2026 VAMP-Compatible Commercial Tracks ----------------
    print("Generating Map 3: August 2026 VAMP-Compatible Commercial Tracks...")
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    plot_base_map(ax, "Map 3: August 2026 VAMP-Compatible Commercial Trajectories\n"
                      "Concentrated Linear Jet Transport Downwind Arrival Stream (<10k ft)")
    
    n_plotted = 0
    for l in lines_26:
        if l["op_class"] == "vamp_compatible_commercial":
            ax.plot(l["lons"], l["lats"], color="#d62728", alpha=0.15, linewidth=1.0)
            n_plotted += 1
            
    # Dummy handle for legend
    ax.plot([], [], color="#d62728", alpha=0.8, linewidth=1.5, label=f"VAMP Commercial Passages (N={n_plotted})")
    ax.text(0.03, 0.03, f"Total Trajectories: {n_plotted}", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8), fontsize=9)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9, fontsize=8)
    
    out3 = FIG_DIR / "map3_aug2026_vamp_commercial_tracks.png"
    plt.savefig(out3, bbox_inches="tight")
    plt.close()
    print(f"Saved {out3}")
    
    # ---------------- MAP 4: Combined August 2026 Aviation Environment ----------------
    print("Generating Map 4: Combined August 2026 Aviation Environment...")
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    plot_base_map(ax, "Map 4: Combined August 2026 Neighbourhood Aviation Environment\n"
                      "Superimposition of Concentrated Commercial Arrivals on Local Background")
    
    n_vamp = 0
    n_non_vamp = 0
    
    # Plot non-vamp first (in blue/green/purple)
    for l in lines_26:
        if l["parent_class"] == "non_vamp":
            ax.plot(l["lons"], l["lats"], color="#2ca02c", alpha=0.35, linewidth=1.0)
            n_non_vamp += 1
            
    # Plot vamp on top (in red)
    for l in lines_26:
        if l["op_class"] == "vamp_compatible_commercial":
            ax.plot(l["lons"], l["lats"], color="#d62728", alpha=0.12, linewidth=0.8)
            n_vamp += 1
            
    # Legend handles
    ax.plot([], [], color="#2ca02c", alpha=0.8, linewidth=1.5, label=f"Non-VAMP Aviation (N={n_non_vamp})")
    ax.plot([], [], color="#d62728", alpha=0.8, linewidth=1.5, label=f"VAMP Commercial Stream (N={n_vamp})")
    
    ax.text(0.03, 0.03, f"Non-VAMP: {n_non_vamp} | VAMP Commercial: {n_vamp}\nCombined: {n_non_vamp + n_vamp}",
            transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8), fontsize=9)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9, fontsize=8)
    
    out4 = FIG_DIR / "map4_aug2026_combined_tracks.png"
    plt.savefig(out4, bbox_inches="tight")
    plt.close()
    print(f"Saved {out4}")
    print("All Maps 1-4 successfully generated.")

if __name__ == "__main__":
    run()
