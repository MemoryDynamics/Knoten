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

| A_att | condition | samples | dt_mem | window_mem | valid frac | amplitude | angular speed | axis polarization | axis dephase | axis <=dt frac | raw L dephase | raw L <=dt frac | signed comp | amplitude CV |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `baseline` | `10001` | `0.010` | `100.000` | `1.000` | `0.253` | `33.081` | `0.016` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.707` |
| `20` | `eta_zero` | `10001` | `0.010` | `100.000` | `1.000` | `1.069` | `8.851` | `0.009` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.697` |
| `35` | `baseline` | `10001` | `0.010` | `100.000` | `1.000` | `0.178` | `45.701` | `0.016` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.707` |
| `35` | `eta_zero` | `10001` | `0.010` | `100.000` | `1.000` | `1.069` | `8.851` | `0.009` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.697` |

## Current Finding

The cadence-separated analysis preserves the earlier logarithmic-trend
compactness and drift values. The uniformly sampled end window resolves
the spin direction at one-update cadence: median dephasing is at or below
the sampling interval and axis polarization remains near zero in active and
`eta_zero` cases. The raw normalized `L` autocorrelation is reported beside
the axis-only correlation to avoid overreading instantaneous amplitudes.
The larger active angular-speed proxy occurs together
with a much smaller radius, while raw spin amplitude is larger in the
control. This is not evidence for a persistent scalar spin mode.

## Reading

The dynamic-center diagnostics remain the primary knot observables:
compact co-moving radius, slow normalized center drift, memory-shape
dimension/roundness, and residence controls. The spin proxy adds a
seedwise test for persistent oriented circulation around the moving
memory center.

Interpretation rules for this stage:

- The time-series figure overlays every seed per condition on a logarithmic
  update axis `N`; any undefined `N=0` point is omitted from the plot only.
- Spin observables use only the uniformly sampled end window. Logarithmic
  checkpoints alone define the reported dynamic-center trend KPIs.
- `spin_amplitude_median` measures the typical co-moving angular momentum scale.
- `spin_angular_speed_median` divides that amplitude by the squared memory radius.
- `spin_axis_polarization` near `1` means a stable oriented axis; near `0` means
  strong axis dephasing or axis wandering across the trace.
- `spin_direction_dephasing_memory_times` is the first axis-autocorrelation lag below
  `1/e`; when `spin_direction_dephasing_is_upper_bound` is `1`, the crossing
  already occurred at the first resolved lag and should be read as `<= dt_mem`.
- `spin_raw_spin_dephasing_memory_times` applies the same rule to the normalized
  untruncated spin-bivector autocorrelation, retaining sign and amplitude variation.
- `eta_zero` can still generate incidental angular momentum from random walks, so
  active conditions only become interesting if amplitude, axis stability, or
  dephasing separate seedwise from matched controls and remain stable with N.

For the current pre-long-run scale, these values should be read as observable
calibration, not as particle-spin evidence.

## Decision

Proceed to the targeted `N=30M` scalar-knot trace for `A_att=20/35`.
Acceptance remains based on logarithmic-trend radius, radius-normalized
center drift, Memory-Shape, and seedwise separation from `eta_zero`.
The terminal spin window remains a recorded negative-control observable;
it is not a Paper-I gate and is not promoted to a spin or photon claim.

## Figures

- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_compactness_drift_2026-07-12.png`
- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_residence_observables_2026-07-12.png`
- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_spin_proxy_2026-07-12.png`
- `figures/draft/dynamic_center_spin/dynamic_center_trace_q3_seedwise_timeseries_2026-07-12.png`

## Raw Rows

- Case rows: `20`.
- Machine-readable aggregate: `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N1M_summary_2026-07-12.json`.
- Raw JSON outputs remain under ignored `data/processed/long_run_metastability/`.
