# Data Coverage and Ingestion Audit (Task 0)

**Study Period:** 1 January 2025 – 31 August 2026 (608 calendar days, 20 calendar months)
**Primary Geographic Focus:** Capitol Hill, Burnaby (49.2869° N, 122.9853° W, 1.5 km study radius)
**Total Valid Observation Days:** 573 / 608 (94.2%)
**Total Absent Days:** 35 days

## 1. Executive Disclosure on Normalization Denominators

Per regulator-facing transparency standards, raw message counts or uncorrected passage totals across calendar months can introduce bias if receiver uptime fluctuates. ADS-B receiver archives record aircraft state vectors when aircraft are within reception range, but do not log continuous independent ping or heartbeat telemetry per minute. Consequently, a minute-level completeness filter (e.g., ≥90% covered minutes) cannot be reliably reconstructed without circular reliance on aircraft presence.

Therefore, following the approved methodological specification (Execution Clarification #3), **validated full observation days ($T_{valid}$)** are adopted as the authoritative primary normalizing denominator for all longitudinal rates ($R = N / T_{valid}$). Hourly profiles are restricted strictly to validated observation periods.

## 2. Monthly Coverage Summary Table

| Month | Period | Calendar Days | Valid Days ($T_{valid}$) | Missing Days | Coverage % | Total Passages | Rate (Passages/Valid Day) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 2025-01 | Pre-VAMP | 31 | 31 | 0 | 100.0% | 525 | 16.94 |
| 2025-02 | Pre-VAMP | 28 | 28 | 0 | 100.0% | 465 | 16.61 |
| 2025-03 | Pre-VAMP | 31 | 31 | 0 | 100.0% | 515 | 16.61 |
| 2025-04 | Pre-VAMP | 30 | 30 | 0 | 100.0% | 557 | 18.57 |
| 2025-05 | Pre-VAMP | 31 | 31 | 0 | 100.0% | 670 | 21.61 |
| 2025-06 | Pre-VAMP | 30 | 30 | 0 | 100.0% | 792 | 26.4 |
| 2025-07 | Pre-VAMP | 31 | 28 | 3 | 90.3% | 707 | 25.25 |
| 2025-08 | Pre-VAMP | 31 | 30 | 1 | 96.8% | 744 | 24.8 |
| 2025-09 | Pre-VAMP | 30 | 26 | 4 | 86.7% | 549 | 21.12 |
| 2025-10 | Pre-VAMP | 31 | 27 | 4 | 87.1% | 487 | 18.04 |
| 2025-11 | Transition | 30 | 29 | 1 | 96.7% | 639 | 22.03 |
| 2025-12 | Post-VAMP | 31 | 29 | 2 | 93.5% | 1990 | 68.62 |
| 2026-01 | Post-VAMP | 31 | 31 | 0 | 100.0% | 2138 | 68.97 |
| 2026-02 | Post-VAMP | 28 | 25 | 3 | 89.3% | 1639 | 65.56 |
| 2026-03 | Post-VAMP | 31 | 29 | 2 | 93.5% | 1622 | 55.93 |
| 2026-04 | Post-VAMP | 30 | 29 | 1 | 96.7% | 1489 | 51.34 |
| 2026-05 | Post-VAMP | 31 | 28 | 3 | 90.3% | 1627 | 58.11 |
| 2026-06 | Post-VAMP | 30 | 25 | 5 | 83.3% | 1532 | 61.28 |
| 2026-07 | Post-VAMP | 31 | 26 | 5 | 83.9% | 2400 | 92.31 |
| 2026-08 | Post-VAMP | 31 | 30 | 1 | 96.8% | 3103 | 103.43 |

## 3. Matched Comparison Period Coverage: August 2025 vs August 2026

- **August 2025 (Baseline):** 30 valid days out of 31 (96.8% coverage, 1 absent day: 2025-08-18).
- **August 2026 (Post-VAMP):** 30 valid days out of 31 (96.8% coverage, 1 absent day: 2026-08-05).
- **Coverage Symmetry:** Both primary comparison months possess identical valid observation periods ($N=30$ days), ensuring that comparison of counts and daily normalized rates are not confounded by differential sampling duration.

## 4. Comprehensive Audit of Absent Days

All 35 absent calendar days across the 20-month census have been audited against the extraction pipeline logs:

| Date | Reason / Processing Status | Technical Detail |
| :--- | :--- | :--- |
| 2025-07-14 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-07-18 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-07-22 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-08-18 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-09-04 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-09-05 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-09-11 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-09-22 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-10-21 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-10-23 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-10-24 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-10-30 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-11-03 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-12-17 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2025-12-25 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-02-12 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-02-26 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-02-27 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-03-20 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-03-21 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-04-16 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-05-05 | Zero extracted flights in raw crawl | Upstream data provider archive defect |
| 2026-05-06 | Archive date absent from ingestion batch | Upstream data provider archive defect |
| 2026-05-12 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-06-05 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-06-11 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-06-17 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-06-20 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-06-21 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-07-03 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-07-06 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-07-12 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-07-13 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-07-26 | Archive download truncation (tar.gz) | Upstream data provider archive defect |
| 2026-08-05 | Archive download truncation (tar.gz) | Upstream data provider archive defect |

## 5. Audit Conclusion

- **Threshold Verification:** All 20 study months exhibit $\ge 83.3\%$ valid day coverage (lowest month: June 2026 with 83.3%, 25/30 days). No month triggers the pre-registered 50% halt condition.
- **Methodological Status:** **VERIFIED**. Daily rates normalized by valid observation days provide a robust, defensible foundation for subsequent descriptive analysis.
