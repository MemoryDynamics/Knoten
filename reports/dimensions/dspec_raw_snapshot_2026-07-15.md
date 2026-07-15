# Raw Memory Snapshot D_spec Audit

Date: 2026-07-15T21:22:34Z.

## Scope

This report reruns spectral-geometry diagnostics on persisted raw
`memory_cloud.snapshot` coordinates from long-run case JSONs. It is the
direct replacement for covariance-surrogate checks when snapshots are available.
The first 2026-07-15 run is a short `N=200k` pipeline pilot, not a
long-run dimension-selection result.

## Provenance

- Source dirs: `data/processed/long_run_metastability/raw_memory_snapshot_pilot_Aatt35_N200k_d3_seed1-3_2026-07-15, data/processed/long_run_metastability/raw_memory_snapshot_pilot_Aatt35_N200k_d10_seed1-3_2026-07-15`
- Machine-readable summary: `reports/dimensions/dspec_raw_snapshot_summary_2026-07-15.json`
- Git revision while building this report: `ed64133beeaba9cb63e031bb400f0f9b478e3343`
- Git status while building this report: `?? experiments/current/dynamics/dspec_raw_snapshot_report.py; ?? figures/draft/dimensions/dspec_raw_snapshot_2026-07-15/; ?? reports/dimensions/dspec_raw_snapshot_2026-07-15.md; ?? reports/dimensions/dspec_raw_snapshot_summary_2026-07-15.json; ?? tests/test_dspec_raw_snapshot_report.py`
- Snapshot cases found: `12`

## Figures

- [raw_snapshot_dspec_by_dimension](../../figures/draft/dimensions/dspec_raw_snapshot_2026-07-15/raw_snapshot_dspec_by_dimension.png)
- [raw_snapshot_dspec_validity](../../figures/draft/dimensions/dspec_raw_snapshot_2026-07-15/raw_snapshot_dspec_validity.png)

## Main Summary

| N | dim | condition | seeds | points | stored D_spec | weighted D_cov | shape D | heat median | heat range | near-3 heat fraction | valid heat windows |
| ---: | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `200,000` | `3` | `baseline` | `3` | 400.000 [400.000, 400.000] | 1.420 [1.420, 1.421] | 2.949 [2.894, 2.956] | 2.949 [2.894, 2.956] | 1.574 [1.574, 1.652] | 1.013 [0.897, 1.203] | 0.000 [0.000, 0.000] | 7.000 [6.000, 7.000] |
| `200,000` | `3` | `eta_zero` | `3` | 400.000 [400.000, 400.000] | 1.095 [1.018, 1.131] | 2.122 [1.680, 2.125] | 2.122 [1.680, 2.125] | 1.102 [1.041, 1.133] | 0.042 [0.039, 0.066] | 0.000 [0.000, 0.000] | 6.000 [4.500, 7.000] |
| `200,000` | `10` | `baseline` | `3` | 400.000 [400.000, 400.000] | - | 9.173 [8.860, 9.175] | 9.173 [8.860, 9.175] | - | - | - | 0.000 [0.000, 0.000] |
| `200,000` | `10` | `eta_zero` | `3` | 400.000 [400.000, 400.000] | 0.911 [0.903, 0.931] | 3.100 [2.883, 3.444] | 3.100 [2.883, 3.444] | 0.917 [0.891, 0.933] | 0.092 [0.052, 0.119] | 0.000 [0.000, 0.000] | 6.000 [4.500, 6.000] |

## Interpretation

- `weighted D_cov` and `shape D` use the stored memory weights; `heat median`
  is still unweighted point-cloud spectral geometry on the raw snapshot.
- `heat range` is the spread across bandwidth factors and neighbor counts;
  large values mean the diagnostic is not yet scale-robust.
- A near-three heat median is only meaningful when valid heat windows are
  common and the range is small across seeds and conditions.
- In the first `N=200k` pilot, raw Heat-Trace `D_spec` does not reproduce
  a robust near-three signal; the `d=10` baseline has no accepted
  scaling window under the conservative estimator.

## Decision

Treat the raw-snapshot path as validated, but treat the short pilot as
non-evidential for dimension selection. The next gate is a longer
raw-snapshot retest on the established long-run slice. If raw snapshot
`D_spec` remains scale-sensitive there, Paper II should prioritize
relational response rank rather than an isolated geometry claim.
