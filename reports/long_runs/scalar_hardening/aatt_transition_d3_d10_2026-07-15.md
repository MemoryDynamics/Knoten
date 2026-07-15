# A_att Transition: d=3 vs d=10

Date: 2026-07-15T07:23:26Z.

## Scope

This report compares matched `N=10M`, seeds `1..5`, q=3 scalar
finite-memory runs across `d=3` and `d=10`. The goal is to separate
sample/outer geometry diagnostics from internal memory-shape diagnostics.

It also closes the report-level reference gap for the `beta=0` control:
`beta=0` is represented in the current code by `M0=0` / condition
`m0_zero`; see `reports/long_runs/scalar_hardening/d10_memory_controls_2026-07-14.md`.

## Figures

- [covariance_dimension](../../../figures/draft/scalar_hardening/aatt_transition_2026-07-15/aatt_transition_covariance_dimension.png)
- [occupancy_window_dimension](../../../figures/draft/scalar_hardening/aatt_transition_2026-07-15/aatt_transition_occupancy_window_dimension.png)
- [memory_shape_dimension](../../../figures/draft/scalar_hardening/aatt_transition_2026-07-15/aatt_transition_memory_shape_dimension.png)
- [memory_spectral_dimension](../../../figures/draft/scalar_hardening/aatt_transition_2026-07-15/aatt_transition_memory_spectral_dimension.png)
- [memory_axis_ratio_min_max](../../../figures/draft/scalar_hardening/aatt_transition_2026-07-15/aatt_transition_memory_axis_ratio_min_max.png)
- [dynamic_center_rms_radius_median](../../../figures/draft/scalar_hardening/aatt_transition_2026-07-15/aatt_transition_dynamic_center_rms_radius_median.png)
- [dynamic_center_drift_radius_fraction_per_memory_time_median](../../../figures/draft/scalar_hardening/aatt_transition_2026-07-15/aatt_transition_dynamic_center_drift_radius_fraction_per_memory_time_median.png)

## Aggregated Metrics

| dim | A_att | seeds | D_cov | D_occ win | D_mem | D_spec mem | roundness | radius | drift/r |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | `7.000` | 5 | `2.584` | `2.191` | `1.486` | `1.214` | `0.002` | `0.317` | `0.199` |
| 3 | `8.000` | 5 | `1.585` | `1.094` | `1.000` | `1.190` | `0.003` | `0.133` | `1.053` |
| 3 | `9.000` | 5 | `1.795` | `1.764` | `1.557` | `1.375` | `0.292` | `9.948e-04` | `0.412` |
| 3 | `10.000` | 5 | `1.795` | `1.787` | `1.984` | `1.425` | `0.405` | `6.761e-04` | `0.255` |
| 3 | `12.000` | 5 | `1.795` | `1.814` | `2.500` | `1.582` | `0.560` | `4.821e-04` | `0.179` |
| 3 | `15.000` | 5 | `1.795` | `1.846` | `2.685` | `1.670` | `0.642` | `3.704e-04` | `0.128` |
| 3 | `20.000` | 5 | `1.796` | `1.859` | `2.819` | `1.824` | `0.728` | `2.909e-04` | `0.093` |
| 3 | `35.000` | 5 | `1.798` | `1.913` | `2.947` | `1.942` | `0.857` | `2.091e-04` | `0.057` |
| 10 | `0` | 5 | `1.111` | `1.066` | `1.000` | `1.191` | `6.375e-05` | `3.056` | `1.052` |
| 10 | `0.100` | 5 | `1.130` | `1.061` | `1.000` | `1.191` | `6.642e-05` | `2.958` | `1.052` |
| 10 | `0.350` | 5 | `1.221` | `1.080` | `1.000` | `1.191` | `7.330e-05` | `2.718` | `1.052` |
| 10 | `1.000` | 5 | `2.204` | `1.161` | `1.001` | `1.191` | `8.166e-05` | `2.138` | `1.051` |
| 10 | `3.000` | 5 | `2.057` | `1.088` | `1.928` | `1.369` | `2.479e-04` | `0.882` | `0.250` |
| 10 | `6.000` | 5 | `3.956` | `1.525` | `1.706` | `1.301` | `4.661e-04` | `0.463` | `0.127` |
| 10 | `7.000` | 5 | `4.553` | `1.851` | `1.486` | `1.213` | `5.986e-04` | `0.317` | `0.199` |
| 10 | `8.000` | 5 | `2.162` | `1.104` | `1.001` | `1.192` | `0.001` | `0.133` | `1.051` |
| 10 | `9.000` | 5 | `2.524` | `1.407` | `2.489` | `1.330` | `0.105` | `0.002` | `0.480` |
| 10 | `10.000` | 5 | `2.524` | `1.462` | `4.040` | `1.501` | `0.192` | `0.001` | `0.289` |
| 10 | `12.000` | 5 | `2.525` | `1.561` | `5.830` | `1.830` | `0.297` | `9.128e-04` | `0.189` |
| 10 | `15.000` | 5 | `2.525` | `1.490` | `7.273` | `2.113` | `0.394` | `6.947e-04` | `0.141` |
| 10 | `20.000` | 5 | `2.527` | `1.762` | `8.282` | `2.387` | `0.489` | `5.382e-04` | `0.106` |
| 10 | `35.000` | 5 | `2.532` | `1.752` | `9.156` | `2.744` | `0.614` | `3.822e-04` | `0.065` |

## Interpretation

- `D_cov` and `D_occ_window` are sample/trajectory diagnostics. They
  describe the visible point cloud, not the full memory state.
- `D_mem` is a covariance participation-ratio dimension of the weighted
  memory cloud. It is an internal state-space shape diagnostic.
- `D_spec_mem` is a point-cloud diffusion/spectral-geometry diagnostic,
  not an FFT window and not a transfer-operator spectrum.
- In d10, the compact regime has `D_cov` near 2.5 while `D_mem` keeps
  increasing from the transition region to `A_att=35`. This supports
  an inside/outside split rather than a single dimension number.
- In d3, `D_mem` approaches the embedding limit while `D_cov` remains
  below 2 for the single-knot trajectory. A single knot does not
  necessarily sample all external directions isotropically.

## Missing Checks

- Add center-trace versions of `D_cov`, `D_occ`, and `D_spec` for a
  cleaner coarse-grained external observable.
- Add cumulative-variance memory dimensions such as `D_p90`/`D_p95`
  to distinguish real internal dimensionality from small-eigenvalue tails.
- Add D_spec bandwidth or kNN-scale sensitivity.
- Add response-based tests with a second knot or weak external field;
  external dimension should ultimately be relational, not inferred
  from a single raw trajectory alone.
- Re-express A_att through a dimensionless stiffness/Hessian scale
  before making cross-dimension universality claims.

## Sources

- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_0,1_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_0,35_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_0_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_1_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_20_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_35_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_3_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_6_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_9_seed1-5_eps1em4_2026-07-14`
- `data/processed/long_run_metastability/Aatt_transition_d10_N10M_Aatt_10_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d10_N10M_Aatt_12_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d10_N10M_Aatt_15_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d10_N10M_Aatt_7_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d10_N10M_Aatt_8_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_10_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_12_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_15_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_20_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_35_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_7_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_8_seed1-5_eps1em4_2026-07-15`
- `data/processed/long_run_metastability/Aatt_transition_d3_N10M_Aatt_9_seed1-5_eps1em4_2026-07-15`
