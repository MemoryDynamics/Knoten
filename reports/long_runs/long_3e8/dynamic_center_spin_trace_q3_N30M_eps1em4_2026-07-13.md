# Dynamic Center and Spin-Proxy Trace Validation

Date: 2026-07-13.

## Scope

This report aggregates dynamic memory-center traces and the new
seedwise spin-proxy observables for the completed `N=30M`, `epsilon=1e-4` scalar-knot rerun. It is a Paper-I evidence check, not a particle-spin or photon claim.

Run label: `N=30M`.
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
| `20` | `baseline` | `2.916e-04` | `0.072` | `1.000` | `3.239e+05` | `60.000` | `680.833` | `2.803` | `0.719` |
| `20` | `eta_zero` | `0.001` | `0.320` | `1.000` | `3.239e+05` | `10.000` | `1540.278` | `1.903` | `0.453` |
| `35` | `baseline` | `2.087e-04` | `0.044` | `1.000` | `3.239e+05` | `140.000` | `651.667` | `2.941` | `0.843` |
| `35` | `eta_zero` | `0.001` | `0.320` | `1.000` | `3.239e+05` | `10.000` | `1540.278` | `1.903` | `0.453` |

## Spin-Proxy Median Summary

| A_att | condition | samples | dt_mem | window_mem | valid frac | amplitude | angular speed | axis polarization | axis dephase | axis <=dt frac | raw L dephase | raw L <=dt frac | signed comp | amplitude CV |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `baseline` | `10001` | `0.010` | `100.000` | `1.000` | `2.807e-06` | `32.526` | `0.011` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.709` |
| `20` | `eta_zero` | `10001` | `0.010` | `100.000` | `1.000` | `1.156e-05` | `8.862` | `0.011` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.701` |
| `35` | `baseline` | `10001` | `0.010` | `100.000` | `1.000` | `1.980e-06` | `46.042` | `0.010` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.710` |
| `35` | `eta_zero` | `10001` | `0.010` | `100.000` | `1.000` | `1.156e-05` | `8.862` | `0.011` | `0.010` | `1.000` | `0.010` | `1.000` | `n/a` | `0.701` |

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

For the current `N=30M` evidence scale, these values should be read as observable
calibration, not as particle-spin evidence.

## Decision

The `N=30M`, `epsilon=1e-4` rerun materially strengthens the scalar Paper-I
candidate in the co-moving sense. Both active candidates remain much more
compact and slower-drifting than the matched `eta_zero` controls, and both
produce higher-dimensional, rounder memory clouds. The stronger current scalar
candidate is `A_att=35`: median dynamic radius `2.09e-4`, normalized center
drift `0.044`, memory dimension `2.94`, and roundness `0.843` versus the
shared `eta_zero` values `0.00104`, `0.320`, `1.90`, and `0.453`.

`A_att=20` also separates from control, but less strongly: median dynamic
radius `2.92e-4`, normalized drift `0.072`, memory dimension `2.80`, and
roundness `0.719`. Voxel residence alone remains a weak acceptance criterion:
`eta_zero` has larger raw voxel residence because its wandering memory ball can
occupy coarse voxels for long stretches. The more reliable Paper-I observables
are therefore co-moving radius, radius-normalized drift, memory shape, and
seedwise control separation.

The spin proxy remains a negative-control observable. Axis polarization stays
near `0.01`, and both axis and raw `L` dephasing are unresolved below the first
sampled lag (`<= dt_mem = 0.01`). This is not evidence for a persistent scalar
spin mode.

Working conclusion: use `A_att=35`, `epsilon=1e-4` as the current scalar
long-run reference candidate. The next scientific step is not another blind
parameter sweep, but transfer-/AR-mode analysis and a concise Paper-I evidence
table built from these co-moving observables.

## Figures

- `figures/draft/dynamic_center_spin_N30M_eps1em4/dynamic_center_trace_q3_compactness_drift_2026-07-12.png`
- `figures/draft/dynamic_center_spin_N30M_eps1em4/dynamic_center_trace_q3_residence_observables_2026-07-12.png`
- `figures/draft/dynamic_center_spin_N30M_eps1em4/dynamic_center_trace_q3_spin_proxy_2026-07-12.png`
- `figures/draft/dynamic_center_spin_N30M_eps1em4/dynamic_center_trace_q3_seedwise_timeseries_2026-07-12.png`

## Raw Rows

- Case rows: `20`.
- Machine-readable aggregate: `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_summary_2026-07-13.json`.
- Raw JSON outputs remain under ignored `data/processed/long_run_metastability/`.


