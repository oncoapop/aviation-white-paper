# Reproducibility and Audit Manifest

**Git Commit:** `5e17bcba5e02b9f0c332b511c0ff846f3eb7d4ee`
**Git Branch:** `main`
**Execution Timestamp:** `2026-09-29T14:29:09.737418`

## 1. Cryptographic SHA-256 Hashes of Source and Derived Data Files

| File Path | SHA-256 Checksum | Purpose |
| :--- | :--- | :--- |
| `data/capitol_hill_all_flights.csv` | `dbca88bd10eaa8a99b9cb4c7c5ba47a1cc69737bcc12277036caf4626c7640f7` | Auditable artifact |
| `data/capitol_hill_passes.csv` | `bd882ae6332939c73b0d643db8a26e2ab2eb752a85843a7252b9c837e7ab810d` | Auditable artifact |
| `analysis/aircraft_classification.json` | `07a89c1a3e92da680f1fe5b104afa7522451e775db967aad68b609392fab426d` | Auditable artifact |
| `white_paper/capitol_hill_passes_classified.csv` | `4bcaad2b5497f45785db10e7da2dd26ab050f8657d823a97ffc969eab1da605b` | Auditable artifact |
| `white_paper/data_coverage_monthly.csv` | `01c66485cf515c04bb09c8455296cec30de8117ea3c15daa3643a8d0b1fe94a4` | Auditable artifact |
| `white_paper/local_aviation_monthly_2025_2026.csv` | `c3159f248aa687d80c8c4bc1e6a32d2cb4f0aa2b6e9678cc6559d0ea5a7b9aab` | Auditable artifact |
| `white_paper/aug2025_vs_aug2026.csv` | `56a921af5f33af08c1b63058428f01f603f856f751e9b525f0d6c705d6f12f11` | Auditable artifact |
| `white_paper/hourly_overlap.csv` | `7678946ca684cbebe3bdd889c74f03db7a6b6b72a1aacc913dac15ff215634c9` | Auditable artifact |
| `white_paper/altitude_band_summary.csv` | `ffbdfe93dd7fc7d713b2a526a2aa43d7cde67698e274d992759c1cfa2784b110` | Auditable artifact |
| `white_paper/helicopter_monthly.csv` | `d0df8e7bf06131e9b60dc777ea119d00a3e5e14f3105654d3d5034839aed47ab` | Auditable artifact |
| `white_paper/floatplane_monthly.csv` | `384ff72946119c47928d8fe4c721bbb720fcbd22dd04c3f2d4602bc5e929cfcf` | Auditable artifact |

## 2. Mathematical Invariants Asserted

- Category sum equality: $N_{vamp} + N_{non\_vamp} + N_{other} = N_{total}$ (Verified exact closure across all 24,190 passes).
- Spatial inclusion bounds: $\max(\text{dist\_km}) = 1.4999 \le 1.5000$ km. Core 500 m subset $N=6,458 \le 24,190$.
- Deduplication: 0 duplicate `(flight_id, pass_idx)` pairs.
- Temporal continuity: 20 months analyzed; zero months below 50% data coverage threshold.
- Table reproduction: August matched comparison counts match underlying passage census exactly.
