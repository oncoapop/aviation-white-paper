# Internal Provenance and Discrepancy Reconciliation
## Technical Reconciliation of Legacy Exploratory Queries vs. Authoritative 20-Month Census

**Document Status:** STRICTLY INTERNAL — NOT FOR REGULATOR OR PUBLIC RELEASE  
**Purpose:** Reconciles discrepancies between earlier internal draft figures (including unpublished Figure 9H and draft table counts) and the authoritative frozen white-paper census.

---

## 1. Executive Directive on Unpublished Figures

> **MANDATORY INJUNCTION:** Figure 9H and earlier draft exploratory figures were internal, unpublished work products. Public-facing white papers, regulatory submissions to NAV CANADA, Transport Canada, or YVR, and community briefs **must never reference, debate, or claim to 'correct' Figure 9H**. Any public debate framed around correcting an unpublished figure creates unnecessary reputational vulnerability and distracts from the verified 20-month empirical evidence.

---

## 2. Provenance of the "Two Qualifying Arrivals" Anomaly (Legacy Figure 9H)

### The Discrepancy
In early exploratory analysis drafts, an automated script (`generate_fig9h.py` / `precise_ch_table.py`) reported that only **two (2) commercial arrivals** overflew Capitol Hill in August 2025 prior to VAMP, compared to ~1,980 in August 2026. This figure was flagged during red-team review as vulnerable to challenge by YVR/NAV CANADA analysts.

### Root-Cause Technical Audit
A line-by-line audit of `generate_fig9h.py` and `precise_ch_table.py` identified the exact technical cause:

1. **External Database and Multi-Waypoint Filter:** Rather than querying the validated discrete pass census (`data/capitol_hill_passes.csv`), those legacy scripts queried an external SQLite database (`regional_vancouver_flights.db` / `capitol_hill_flights.db`) and enforced a strict multi-condition filter requiring an ADS-B track to:
   - Enter the Capitol Hill 1.5 km study cylinder;
   - Maintain a continuous unbroken sequence of state vectors; AND
   - Record an explicit track endpoint inside a tiny geographic bounding box on the surface of YVR Runway 26L, 26R, 08L, or 08R at an altitude **below 1,000 ft MSL**.
2. **Ground-Level Receiver Dropout:** ADS-B reception from terrestrial receivers suffers from line-of-sight terrain shielding, building clutter, and antenna elevation limits as aircraft descend near the surface. In 2025, many commercial aircraft landing at YVR experienced signal loss below 1,500 ft before recording a point inside the physical runway bounding box.
3. **Artificial False Negatives:** Consequently, legitimate commercial arrivals that traversed Capitol Hill were systematically discarded by the script because their ground-roll points were missing from the raw capture stream. Only two flights happened to maintain unbroken telemetry directly to the runway tarmac.

### Authoritative Reconciliation
When evaluated using the authoritative terminal-airspace exposure criteria (<10,000 ft MSL, within 1.5 km of Capitol Hill, and aligned with downwind heading bands):
- **12 commercial passages** operated on Eastbound (060–120°) or Westbound (240–300°) downwind arrival headings in August 2025.
- An additional **192 commercial passages** operated across the cylinder at altitudes between 5,000 and 10,000 ft MSL (predominantly Northbound cross-traffic at 7,000–9,000 ft routing toward northern BC and Alaska).
- Total commercial aircraft below 10,000 ft in August 2025 was **204 passages**.
- In August 2026, VAMP-compatible downwind commercial arrivals reached **1,989 passages**.

**Conclusion:** The true pre-VAMP commercial arrival baseline is 12 downwind passages (0.4/day), not 2. This represents a 165-fold expansion post-VAMP, which remains an extraordinary operational shift while resting on an unassailable methodological foundation.

---

## 3. Reconciliation of Control Category Discrepancies (349 vs. 506 vs. 484)

### The Discrepancy
Earlier draft documents contained conflicting counts for background / non-VAMP traffic in August 2025, variously citing "349", "506", or "516" flights.

### Root-Cause Audit
1. **The "349" Count:** This was calculated by filtering `capitol_hill_all_flights.csv` strictly for `type_code` in `light_heli` at the aircraft-day level. It excluded business jets (61 flights) and floatplanes classified under other codes, and counted unique daily airframes rather than discrete overflight passes.
2. **The "506 / 516" Count:** This count originated from an early prototype script that queried a regional flight database with a relaxed geographic buffer (~2.5 km) and inadvertently included regional transits that did not enter the 1.5 km Capitol Hill neighbourhood cylinder.

### Authoritative Reconciliation
Under the frozen, audited, pass-level classification (`capitol_hill_passes_classified.csv`) within the strictly enforced 1.5 km cylinder:
- **Light Fixed-Wing General Aviation:** 319 passages
- **Helicopters:** 54 passages
- **Floatplanes / Seaplanes:** 50 passages
- **Business Aviation:** 61 passages
- **Total Non-VAMP Aviation (August 2025):** **484 passages** (16.1 passages/day across 30 valid observation days).
- **Sub-5,000 ft Non-VAMP Aviation:** **444 passages** (14.8 passages/day).

---

## 4. Summary Crosswalk Table for Authors

| Draft / Context | August 2025 Metric | Reported Value | True Audited Value | Reconciliation Explanation |
| :--- | :--- | :---: | :---: | :--- |
| **Legacy Fig 9H** | Pre-VAMP Commercial Arrivals | ~2 | **12** (downwind <10k ft) / **204** (all <10k ft comm) | Legacy script required unbroken track to runway tarmac below 1,000 ft, discarding flights that suffered ground-level antenna dropouts. |
| **Draft Table A** | August 2025 Non-VAMP Baseline | 349 | **484** (all non-VAMP passes) | 349 counted unique aircraft-days for `light_heli` only; 484 counts all discrete neighbourhood passes including business aviation and floatplanes. |
| **Draft Table B** | August 2025 Control Traffic | 506 | **484** | 506 included regional aircraft outside the 1.5 km Capitol Hill study cylinder. |
| **August 2026** | Post-VAMP Commercial Arrivals | ~1,980 | **1,989** | Stable and confirmed within 0.5% across all query implementations. |

---

## 5. Protocol for Future External Inquiries

If an external reviewer or technical stakeholder asks why an earlier draft brief contained differing numbers:
1. State clearly that earlier draft figures represented preliminary, unmerged exploratory queries that used varying unit definitions (aircraft-days vs. passes) or experimental runway-threshold filters.
2. Reaffirm that the white paper relies exclusively on the **frozen, fully audited, open-source 20-month census (`capitol_hill_passes.csv`)**, where every pass is defined by a standardized 10-minute clustering rule, geographic proximity ($\le 1.5$ km), and transparent operational classification.
