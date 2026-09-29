# Vancouver Airspace Modernization Project (VAMP) Community-Noise Exposure-Context White Paper Analysis

This repository contains the empirical, reproducible, and regulator-defensible descriptive analysis of aviation overflights over Capitol Hill, Burnaby, covering the 20-month period from **January 2025 through August 2026**.

The study evaluates the community-noise exposure context surrounding NAV CANADA's implementation of VAMP on **27 November 2025**, comparing the pre-existing baseline aviation environment against the post-VAMP arrival stream.

---

## Central Research Question

> **What aviation activity already existed over or near Capitol Hill before VAMP, how did that local aviation environment vary over time and change between 2025 and 2026, and what new concentrated commercial-arrival traffic stream was subsequently superimposed on it after VAMP implementation?**

The airspace route structure established under VAMP is treated as operationally fixed and is outside the scope of critique. This analysis prioritizes descriptive accuracy, data provenance, and conservative interpretation.

---

## Key Reports and Documentation

- **[WHITE_PAPER_SAFE_FINDINGS.md](WHITE_PAPER_SAFE_FINDINGS.md):** Main technical report presenting findings labeled with epistemic status (`[VERIFIED]`, `[ASSUMPTION-BOUND]`, `[NOT ESTABLISHED]`).
- **[RED_TEAM_VULNERABILITIES.md](RED_TEAM_VULNERABILITIES.md):** Antagonistic 5-column technical defense addressing potential counterarguments from NAV CANADA / YVR analysts.
- **[INTERNAL_PROVENANCE_RECONCILIATION.md](INTERNAL_PROVENANCE_RECONCILIATION.md):** Internal provenance reconciliation detailing the technical resolution of earlier exploratory query discrepancies (legacy unpublished Figure 9H).
- **[DATA_COVERAGE_AUDIT.md](DATA_COVERAGE_AUDIT.md):** Task 0 coverage audit documenting receiver health, absent days, and daily normalization denominators.
- **[UNIT_OF_OBSERVATION_CROSSWALK.md](UNIT_OF_OBSERVATION_CROSSWALK.md):** Mathematical crosswalk connecting raw messages, 20,093 aircraft-days, and 24,190 discrete passes (10-minute gap rule).
- **[AIRCRAFT_CLASSIFICATION_RULES.md](AIRCRAFT_CLASSIFICATION_RULES.md):** Tri-partite operational classification definitions and materiality thresholds.
- **[REPRODUCIBILITY_MANIFEST.md](REPRODUCIBILITY_MANIFEST.md):** Cryptographic SHA-256 checksums of all input and output datasets.

---

## Headline Findings (August 2025 Baseline vs. August 2026 Post-VAMP)

Both August 2025 and August 2026 possess exactly **30 validated observation days** ($T_{valid}=30$), ensuring perfect comparison symmetry:

| Traffic Category | Aug 2025 Count ($N_{25}$) | Aug 2025 Rate (/day) | Aug 2026 Count ($N_{26}$) | Aug 2026 Rate (/day) | % Change | Median Alt 2025 (ft MSL) | Median Alt 2026 (ft MSL) | Epistemic Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Helicopters** | 54 | 1.8 | 262 | 8.7 | **+385.2%** | 1,325 | 2,000 | **[VERIFIED]** |
| **Light Fixed-Wing GA** | 319 | 10.6 | 408 | 13.6 | **+27.9%** | 2,050 | 2,050 | **[VERIFIED]** |
| **Floatplanes / Seaplanes** | 50 | 1.7 | 68 | 2.3 | **+36.0%** | 1,500 | 1,500 | **[VERIFIED]** |
| **Business Aviation** | 61 | 2.0 | 162 | 5.4 | **+165.6%** | 7,375 | 7,588 | **[VERIFIED]** |
| **All Non-VAMP Aviation** | **484** | **16.1** | **900** | **30.0** | **+86.0%** | **1,975** | **2,200** | **[VERIFIED]** |
| *Non-VAMP Sub-5,000 ft* | *444* | *14.8* | *735* | *24.5* | *+65.5%* | *1,900* | *2,000* | **[VERIFIED]** |
| **VAMP Commercial Passages** | **12** | **0.4** | **1,989** | **66.3** | **+16,475%** | **1,388** | **7,675** | **[ASSUMPTION-BOUND]** |
| **Other / Unknown Traffic** | 248 | 8.3 | 214 | 7.1 | **-13.7%** | 7,350 | 7,375 | **[VERIFIED]** |
| **Total All Passages** | **744** | **24.8** | **3,103** | **103.4** | **+317.1%** | **2,175** | **5,825** | **[VERIFIED]** |

---

## Core Visualizations (`figures/`)

- **Figure 1 ([figures/fig1_monthly_aviation_activity.png](figures/fig1_monthly_aviation_activity.png)):** 20-month time series of daily rates (Non-VAMP vs. VAMP Commercial vs. Combined).
- **Figure 2 ([figures/fig2_monthly_composition.png](figures/fig2_monthly_composition.png)):** Monthly percentage share of neighbourhood overflights.
- **Figure 3 ([figures/fig3_aug2025_vs_aug2026_comparison.png](figures/fig3_aug2025_vs_aug2026_comparison.png)):** August matched comparison horizontal bar chart.
- **Figure 4 ([figures/fig4_diurnal_24hr_profile.png](figures/fig4_diurnal_24hr_profile.png)):** 24-hour diurnal profile demonstrating extensive daytime temporal overlap.
- **Figure 5 ([figures/fig5_altitude_band_distribution.png](figures/fig5_altitude_band_distribution.png)):** Altitude distribution stratified across 6 standardized altitude bands.
- **Map 1 ([figures/map1_aug2025_non_vamp_tracks.png](figures/map1_aug2025_non_vamp_tracks.png)):** August 2025 baseline non-VAMP trajectories.
- **Map 2 ([figures/map2_aug2026_non_vamp_tracks.png](figures/map2_aug2026_non_vamp_tracks.png)):** August 2026 non-VAMP trajectories.
- **Map 3 ([figures/map3_aug2026_vamp_commercial_tracks.png](figures/map3_aug2026_vamp_commercial_tracks.png)):** August 2026 linear commercial downwind arrival stream.
- **Map 4 ([figures/map4_aug2026_combined_tracks.png](figures/map4_aug2026_combined_tracks.png)):** Combined August 2026 aviation environment.

---

## Reproducibility

The entire pipeline executes deterministically from source records in under 15 seconds:
```bash
python run_all.py
```
This runs Modules 01 through 10 in sequence, re-computes all CSV tables, regenerates all 300 DPI figures and maps, and executes all 10 mathematical verification assertions.
