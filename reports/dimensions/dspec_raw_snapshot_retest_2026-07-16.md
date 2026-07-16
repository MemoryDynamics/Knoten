# Raw Memory Snapshot D_spec Audit

Date: 2026-07-16T04:57:45Z.

## Scope

This report reruns spectral-geometry diagnostics on persisted raw
`memory_cloud.snapshot` coordinates from long-run case JSONs. It is the
direct replacement for covariance-surrogate checks when snapshots are available.
Short `N=200k` runs should be read as pipeline checks; longer retests
probe whether the same diagnostic stabilizes with history length.

## Provenance

- Source dirs: `data/processed/long_run_metastability/raw_memory_snapshot_pilot_Aatt35_N200k_d3_seed1-3_2026-07-15, data/processed/long_run_metastability/raw_memory_snapshot_pilot_Aatt35_N200k_d10_seed1-3_2026-07-15, data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16, data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d10_seed1-5_2026-07-16`
- Machine-readable summary: `reports/dimensions/dspec_raw_snapshot_retest_summary_2026-07-16.json`
- Git revision while building this report: `6f05e9d2ae662a4191ea3feae9c59d6e912b2a2a`
- Git status while building this report: `M experiments/current/dynamics/dspec_raw_snapshot_report.py; ?? figures/draft/dimensions/dspec_raw_snapshot_retest_2026-07-16/; ?? reports/dimensions/dspec_raw_snapshot_retest_2026-07-16.md; ?? reports/dimensions/dspec_raw_snapshot_retest_summary_2026-07-16.json`
- Snapshot cases found: `32`

## Figures

- [raw_snapshot_dspec_by_dimension](../../figures/draft/dimensions/dspec_raw_snapshot_retest_2026-07-16/raw_snapshot_dspec_by_dimension.png)
- [raw_snapshot_dspec_validity](../../figures/draft/dimensions/dspec_raw_snapshot_retest_2026-07-16/raw_snapshot_dspec_validity.png)

## Main Summary

| N | dim | condition | seeds | points | stored D_spec | weighted D_cov | shape D | heat median | heat range | near-3 heat fraction | valid heat windows |
| ---: | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `200,000` | `3` | `baseline` | `3` | 500.000 [500.000, 500.000] | 1.420 [1.420, 1.421] | 2.968 [2.902, 2.968] | 2.968 [2.902, 2.968] | 1.578 [1.560, 1.888] | 0.962 [0.842, 1.313] | 0.000 [0.000, 0.000] | 7.000 [5.500, 7.000] |
| `200,000` | `3` | `eta_zero` | `3` | 500.000 [500.000, 500.000] | 1.095 [1.018, 1.131] | 2.117 [1.679, 2.124] | 2.117 [1.679, 2.124] | 1.127 [1.052, 1.172] | 0.066 [0.052, 0.072] | 0.000 [0.000, 0.000] | 9.000 [7.500, 9.000] |
| `200,000` | `10` | `baseline` | `3` | 500.000 [500.000, 500.000] | - | 9.135 [8.928, 9.189] | 9.135 [8.928, 9.189] | - | - | - | 0.000 [0.000, 0.000] |
| `200,000` | `10` | `eta_zero` | `3` | 500.000 [500.000, 500.000] | 0.911 [0.903, 0.931] | 3.090 [2.876, 3.431] | 3.090 [2.876, 3.431] | 0.949 [0.907, 0.950] | 0.026 [0.022, 0.079] | 0.000 [0.000, 0.000] | 6.000 [4.500, 7.000] |
| `3,000,000` | `3` | `baseline` | `5` | 500.000 [500.000, 500.000] | 1.661 [1.588, 1.735] | 2.846 [2.839, 2.905] | 2.846 [2.839, 2.905] | 1.722 [1.704, 1.826] | 0.631 [0.239, 1.270] | 0.000 [0.000, 0.000] | 5.000 [3.000, 6.000] |
| `3,000,000` | `3` | `eta_zero` | `5` | 500.000 [500.000, 500.000] | 1.071 [1.037, 1.131] | 1.522 [1.499, 1.583] | 1.522 [1.499, 1.583] | 0.970 [0.927, 1.052] | 0.203 [0.149, 0.289] | 0.000 [0.000, 0.000] | 9.000 [7.000, 9.000] |
| `3,000,000` | `10` | `baseline` | `5` | 500.000 [500.000, 500.000] | - | 8.939 [8.903, 9.025] | 8.939 [8.903, 9.025] | - | - | - | 0.000 [0.000, 0.000] |
| `3,000,000` | `10` | `eta_zero` | `5` | 500.000 [500.000, 500.000] | 0.968 [0.967, 0.970] | 1.740 [1.729, 1.952] | 1.740 [1.729, 1.952] | 0.925 [0.909, 0.944] | 0.051 [0.030, 0.134] | 0.000 [0.000, 0.000] | 6.000 [6.000, 6.000] |

## Interpretation

- `weighted D_cov` and `shape D` use the stored memory weights; `heat median`
  is still unweighted point-cloud spectral geometry on the raw snapshot.
- `heat range` is the spread across bandwidth factors and neighbor counts;
  large values mean the diagnostic is not yet scale-robust.
- A near-three heat median is only meaningful when valid heat windows are
  common and the range is small across seeds and conditions.
- In the `N=200k` pilot, raw Heat-Trace `D_spec` does not reproduce
  a robust near-three signal.
- In the `N=3M` retest, `d=3` baseline remains shape-near-three but
  Heat-Trace `D_spec` stays well below three; `d=10` baseline remains
  high-dimensional in shape and has no accepted Heat-Trace scaling window.

## Decision

Treat the raw-snapshot path as validated, but do not use isolated
Heat-Trace `D_spec` as a dimension-selection claim. The current retest
supports moving the Paper-II gate toward relational response rank, with
any future `N=30M` raw snapshot run serving as confirmation rather than
as a prerequisite for this methodological decision.
