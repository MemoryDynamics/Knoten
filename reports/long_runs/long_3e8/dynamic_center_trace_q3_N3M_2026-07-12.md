# Dynamic Center Trace Validation

Date: 2026-07-12.

## Scope

This is the first validation run for the dynamic memory-center trace.
It is a measurement-methodology check, not a replacement for the
`N=300M` evidence set.

Fixed parameters: `d=3`, seeds `1..5`, `N=3,000,000`, `trace_every=10,000`,
`burn_in=0`, `sample_every=200`, `alpha=lambda_m=0.01`, `M0=1`,
`epsilon=0.03`, `eta=0.15`, `A_rep=1`, `sigma_rep=1`, `sigma_att=3`,
`memory_factor=6`, `max_memory=600`, deposition `delta`.

Axis: `A_att in {20,35}` against matched `eta_zero` controls.

## Median Summary

| A_att | condition | dyn radius | dyn drift/radius/memtime | dyn inside | dyn max run | final-center residence | voxel residence | memory dim | memory roundness |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `baseline` | `0.087` | `0.028` | `0.997` | `1.980e+04` | `36.000` | `42.867` | `2.723` | `0.655` |
| `20` | `eta_zero` | `0.344` | `0.129` | `1.000` | `3.000e+04` | `18.000` | `30.000` | `1.527` | `0.305` |
| `35` | `baseline` | `0.062` | `0.017` | `0.993` | `1.560e+04` | `46.000` | `52.235` | `2.885` | `0.786` |
| `35` | `eta_zero` | `0.344` | `0.129` | `1.000` | `3.000e+04` | `18.000` | `30.000` | `1.527` | `0.305` |

## Reading

The dynamic-center trace fixes one failure mode of the static final
memory-center residence: compact active runs can drift or re-center, so
a final absolute center is not a good global residence target.

However, `dynamic_inside_fraction` and `dynamic_max_run` are not by
themselves discriminating acceptance metrics. The `eta_zero` controls
also remain inside their own contemporaneous memory ball, because that
ball is much larger and follows the random walk.

The useful discriminants in this pilot are therefore co-moving
compactness and normalized center drift:

- `A_att=20`: median dynamic RMS radius is about `0.087` versus
  `0.344` for `eta_zero`; median drift/radius/memory-time is about
  `0.028` versus `0.129`.
- `A_att=35`: median dynamic RMS radius is about `0.062` versus
  `0.344` for `eta_zero`; median drift/radius/memory-time is about
  `0.017` versus `0.129`.
- Memory-shape dimension remains near three for the active candidates
  and near `1.5` for `eta_zero` in this pilot.

Interpretation: the co-moving-object picture is methodologically
stronger than the fixed-center picture, but the acceptance criterion
should be `compact, slowly drifting memory cloud`, not merely
`point remains inside the moving memory ball`.

## Decision

For Paper I, dynamic center diagnostics should be reported as:

- dynamic RMS radius / memory compactness;
- center drift normalized by current radius and memory time;
- memory shape dimension and roundness;
- voxel residence as a complementary but grid-sensitive observable;
- final-center residence only as a warning/drift diagnostic.

Next technical step: repeat this trace diagnostic at a longer scale
(`30M` first, not immediately `300M`) with about 100 logarithmically
spaced trace points, e.g. `--trace-points 100 --trace-spacing log`.
This resolves the early transient while still validating late-time stability.
For nonuniform traces, dynamic run durations must be interpreted through the
time-weighted fields rather than point counts.

## Figures

- `figures/draft/dynamic_center/dynamic_center_trace_q3_compactness_drift_2026-07-12.png`
- `figures/draft/dynamic_center/dynamic_center_trace_q3_residence_observables_2026-07-12.png`
- `figures/draft/dynamic_center/dynamic_center_trace_q3_seed1_timeseries_2026-07-12.png`

## Raw Rows

- Case rows: `20`.
- Raw JSON outputs remain under ignored `data/processed/long_run_metastability/`.
- Machine-readable aggregate: `reports/long_runs/long_3e8/dynamic_center_trace_q3_N3M_summary_2026-07-12.json`.
