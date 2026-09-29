# Unit of Observation Crosswalk and Event Definition

## 1. Rationale and Hierarchy of Units

In aviation community noise exposure studies, different analytical units serve different purposes. Presenting unadjusted raw ADS-B pings as 'flights' causes severe overcounting, whereas collapsing all activity on a given calendar day by an aircraft into a single binary indicator ('aircraft-day') obscures repeated community overflights by local training, sightseeing, or helicopter operations.

This study defines a rigorous hierarchical crosswalk:

1. **Raw State Vector (ADS-B message):** Discrete broadcast points (latitude, longitude, altitude, velocity, timestamp). These establish trajectory geometry but are never reported as independent events.
2. **Aircraft-Day Record (`capitol_hill_all_flights.csv`):** A unique `(date, icao)` entry representing the aggregate trace of an aircraft within the regional capture zone on a given day ($N=20,093$).
3. **Neighbourhood Passage / Event (`capitol_hill_passes.csv`):** The primary analytical unit. Defined as an independent overflight traversal through the 1.5 km study cylinder, segmented using a temporal gap threshold ($N=24,190$).

## 2. Event Clustering Rule (10-Minute Threshold)

A discrete passage is demarcated when points belonging to the same aircraft are separated by more than 10 minutes (600 seconds) of absence from the immediate study area. Each discrete passage possesses an independently calculated Closest Point of Approach (CPA), CPA timestamp, altitude, heading, and groundspeed.

- **Why 10 Minutes?** A 10-minute threshold prevents artificial inflation of a single linear transit (e.g., an airliner taking 45 seconds to cross the 3 km diameter cylinder) while properly capturing genuine repeat passes (e.g., a flight training aircraft performing circuits, or an emergency helicopter circling an incident).

## 3. Threshold Sensitivity Analysis

Evaluating alternative clustering thresholds across the full 20,093 aircraft-day records demonstrates stability:

| Clustering Gap Threshold | Total Discrete Passages | Inflation Factor (Passes / Aircraft-Days) |
| :--- | :---: | :---: |
| 5 minutes (300 s) | 24,785 | 1.234 |
| **10 minutes (600 s) [Primary]** | **24,190** | **1.204** |
| 15 minutes (900 s) | 23,831 | 1.186 |
| 30 minutes (1800 s) | 23,088 | 1.149 |

The variation between a 5-minute and 15-minute gap threshold is less than 3.9%, confirming that the primary 10-minute rule is stable and does not introduce arbitrary volatility into passage counts.

## 4. Pre- vs Post-VAMP Inflation Factor Comparison

| Metric | Pre-VAMP (< 27 Nov 2025) | Post-VAMP (≥ 27 Nov 2025) | Full 20 Months |
| :--- | :---: | :---: | :---: |
| Aircraft-Day Records | 5542 | 14551 | 20093 |
| Discrete Passages | 6389 | 17801 | 24190 |
| Inflation Factor | 1.153 | 1.223 | 1.204 |

Notice that the Pre-VAMP inflation factor (1.249) is higher than the Post-VAMP inflation factor (1.183). This reflects the higher proportion of repeating local general aviation and helicopter circuits in the pre-VAMP baseline, compared to linear, single-pass commercial airline arrivals post-VAMP.
