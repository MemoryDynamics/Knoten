# Dynamic Center and Spin-Proxy Trace Validation

Date: 2026-07-12.

## Scope

This report aggregates dynamic memory-center traces and the new
seedwise spin-proxy observables. It is a pre-long-run methodology check,
not a replacement for the `N=300M` evidence set.

Run label: `N=1M`.
Seeds: `1..5`.
A_att values: `{20,35}`.
Conditions: `{baseline,eta_zero}`.

The spin proxy is the co-moving angular-momentum bivector
`L = (x - c_mem) wedge dx/dt_mem`, where `c_mem` is the contemporaneous
memory center and `t_mem = alpha n`. It is a continuous diagnostic of
amplitude, angular speed, axis polarization, and dephasing. It is not a
claim of quantized spin.

## Dynamic-Center Median Summary

| A_att | condition | dyn radius | dyn drift/radius/memtime | dyn inside weighted | dyn max run | final-center residence | voxel residence | memory dim | memory roundness |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `baseline` | `0.088` | `0.174` | `1.000` | `1.065e+04` | `20.000` | `30.678` | `2.712` | `0.673` |
| `20` | `eta_zero` | `0.293` | `0.624` | `1.000` | `1.065e+04` | `8.000` | `26.000` | `1.639` | `0.331` |
| `35` | `baseline` | `0.063` | `0.102` | `1.000` | `1.064e+04` | `20.000` | `28.372` | `2.868` | `0.772` |
| `35` | `eta_zero` | `0.293` | `0.624` | `1.000` | `1.065e+04` | `8.000` | `26.000` | `1.639` | `0.331` |

## Spin-Proxy Median Summary

| A_att | condition | valid frac | amplitude | angular speed | axis polarization | dephase time | signed comp | amplitude CV |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `baseline` | `1.000` | `0.001` | `0.172` | `0.119` | `2.453` | `n/a` | `2.033` |
| `20` | `eta_zero` | `1.000` | `0.037` | `0.313` | `0.089` | `2.453` | `n/a` | `1.328` |
| `35` | `baseline` | `1.000` | `9.629e-04` | `0.240` | `0.118` | `2.453` | `n/a` | `2.232` |
| `35` | `eta_zero` | `1.000` | `0.037` | `0.313` | `0.089` | `2.453` | `n/a` | `1.328` |

## Reading

The dynamic-center diagnostics remain the primary knot observables:
compact co-moving radius, slow normalized center drift, memory-shape
dimension/roundness, and residence controls. The spin proxy adds a
seedwise test for persistent oriented circulation around the moving
memory center.

Interpretation rules for this stage:

- `spin_amplitude_median` measures the typical co-moving angular momentum scale.
- `spin_angular_speed_median` divides that amplitude by the squared memory radius.
- `spin_axis_polarization` near `1` means a stable oriented axis; near `0` means
  strong axis dephasing or axis wandering across the trace.
- `spin_direction_dephasing_memory_times` is the first autocorrelation lag below
  `1/e`, if that crossing occurs within the stored trace lags.
- `eta_zero` can still generate incidental angular momentum from random walks, so
  active conditions only become interesting if amplitude, axis stability, or
  dephasing separate seedwise from matched controls and remain stable with N.

For the current pre-long-run scale, these values should be read as observable
calibration, not as particle-spin evidence.

## Decision

Use this trace layer to decide whether the next expensive run has stable
co-moving compactness and stable or dephasing spin proxies. If the spin
metrics are noisy but the compactness/drift metrics remain separated from
`eta_zero`, continue the scalar-knot track. If spin-axis persistence appears
only in active cases and survives longer N, it becomes a candidate input for
a separate ModeScore or vector-memory test, not a KnotScore replacement.

## Figures

- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_compactness_drift_2026-07-12.png`
- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_residence_observables_2026-07-12.png`
- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_spin_proxy_2026-07-12.png`
- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_seed1_timeseries_2026-07-12.png`

## Raw Rows

- Case rows: `20`.
- Machine-readable aggregate: `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N1M_summary_2026-07-12.json`.
- Raw JSON outputs remain under ignored `data/processed/long_run_metastability/`.
