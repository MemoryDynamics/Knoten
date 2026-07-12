# Epsilon Sensitivity for Dynamic-Center Knot Benchmarks

Date: 2026-07-12.

## Scope

This sweep varies only `epsilon` around the corrected-sign compact scalar-memory
candidate. It is a short diagnostic run to estimate the stochastic-noise scale
at which co-moving knot observables and spin proxies separate from matched
`eta_zero` controls.

Raw data root: `data/processed/long_run_metastability/epsilon_confirm_q3_Aatt_35_N1M_seed1-5_2026-07-12`.
Case rows: `30`.

## Median Summary

| epsilon | condition | score | dyn radius | drift/radius/memtime | memory dim | memory roundness | internal spin amp | lab spin amp | spin omega | axis pol | axis dephase | raw L dephase | raw L <=dt frac |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1.650e-06` | `baseline` | `0.857` | `3.470e-06` | `0.102` | `2.867` | `0.772` | `5.394e-10` | `5.421e-10` | `45.682` | `0.016` | `0.010` | `0.010` | `1.000` |
| `1.650e-06` | `eta_zero` | `n/a` | `1.610e-05` | `0.624` | `1.639` | `0.331` | `3.234e-09` | `3.250e-09` | `8.851` | `0.009` | `0.010` | `0.010` | `1.000` |
| `1.000e-04` | `baseline` | `0.857` | `2.103e-04` | `0.102` | `2.867` | `0.772` | `1.981e-06` | `1.991e-06` | `45.682` | `0.016` | `0.010` | `0.010` | `1.000` |
| `1.000e-04` | `eta_zero` | `n/a` | `9.760e-04` | `0.624` | `1.639` | `0.331` | `1.188e-05` | `1.194e-05` | `8.851` | `0.009` | `0.010` | `0.010` | `1.000` |
| `0.015` | `baseline` | `0.857` | `0.032` | `0.102` | `2.868` | `0.772` | `0.045` | `0.045` | `45.686` | `0.016` | `0.010` | `0.010` | `1.000` |
| `0.015` | `eta_zero` | `n/a` | `0.146` | `0.624` | `1.639` | `0.331` | `0.267` | `0.269` | `8.851` | `0.009` | `0.010` | `0.010` | `1.000` |

## Reading

The strongest short-run baseline score in this sweep occurs near `epsilon=1.650e-06` with median score `0.857`.
The `score >= 0.75` band spans approximately `epsilon=1.650e-06` to `1.500e-02` in this 100k pilot.

Use this sweep as a threshold finder, not as final evidence. The relevant
signal is a band where radius and radius-normalized center drift improve
against `eta_zero` without creating only a deterministic zero-start artifact.
Spin quantities use `r = x - c_memory` and the co-moving velocity
`d(x - c_memory)/dt`; the adjacent laboratory-frame amplitude reports the
translation removed by that correction. Persistent internal circulation would
require amplitude, axis polarization, raw normalized `L` autocorrelation, and
dephasing bounds to separate from controls. A large angular-speed proxy alone
is insufficient.

## Figures

- `figures/draft/epsilon_confirm_Aatt35/epsilon_dynamic_center_knot_score_2026-07-12.png`
- `figures/draft/epsilon_confirm_Aatt35/epsilon_dynamic_center_spin_proxy_2026-07-12.png`
- `figures/draft/epsilon_confirm_Aatt35/epsilon_dynamic_center_seedwise_timeseries_2026-07-12.png`

## Machine Output

- `reports/long_runs/epsilon/epsilon_confirm_q3_Aatt35_N1M_summary_2026-07-12.json`
