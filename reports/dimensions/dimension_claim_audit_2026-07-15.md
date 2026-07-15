# 3D Dimension Claim Audit

Date: 2026-07-15T13:39:17Z.

## Scope

This audit turns the current 3D evidence into an explicit claim ladder.
It reuses existing `A_att=35`, `epsilon=1e-4`, corrected q=3 scalar
case JSONs and does not introduce a new long run.

The audit separates four diagnostics:

- `D_mem`: covariance participation dimension of the weighted memory cloud.
- `D_p90`/`D_p95`: number of covariance axes needed for 90%/95% memory variance.
- `D_spec memory`: unweighted point-cloud spectral geometry of the memory cloud.
- `D_center`: low-pass dynamic-center trace geometry, thinned to one memory time.

## Provenance

- Source dirs: `data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_rerun_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d4_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d5_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d7_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d10_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d13_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d20_seed1-5_eps1em4_2026-07-13`
- Machine-readable summary: `reports/dimensions/dimension_claim_audit_summary_2026-07-15.json`
- Git revision while building this report: `ac25363ecb7273e71880c02a4d8dab70301ca0d1`
- Git status while building this report: `M docs/reference/experiment_catalog.md;  M docs/status/current_status.md;  M docs/status/paper_claims.md;  M docs/status/project_priorities.md; ?? experiments/current/dynamics/dimension_claim_audit.py; ?? figures/draft/dimensions/dimension_claim_audit_2026-07-15/; ?? reports/dimensions/dimension_claim_audit_2026-07-15.md; ?? reports/dimensions/dimension_claim_audit_summary_2026-07-15.json; ?? tests/test_dimension_claim_audit.py`

## Figures

- [baseline_dimensions](../../figures/draft/dimensions/dimension_claim_audit_2026-07-15/dimension_claim_audit_baseline_dimensions.png)
- [control_separation](../../figures/draft/dimensions/dimension_claim_audit_2026-07-15/dimension_claim_audit_control_separation.png)

## Claim Ladder

| level | statement | current status |
| --- | --- | --- |
| Paper I | Co-moving compact memory clouds exist in the corrected scalar reference slice. | Supported by radius, drift/radius, roundness and control separation. |
| Paper I teaser | In a chosen 3D embedding, the scalar reference cloud has near-3 local memory-shape geometry. | Supported for `d=3`: `D_mem ~=2.95` at `A_att=35`; still a chosen-embedding statement. |
| Paper II hypothesis | A coarse/external sector may be near three-dimensional. | Plausible but unresolved: `D_spec memory` approaches 3 at high ambient `d`, while center-trace geometry remains a separate observable. |
| strong dimension claim | The model selects macroscopic 3D independent of ambient dimension. | Not supported by this audit: `D_mem` rises with ambient dimension. |

## Ambient-Dimension Summary

| N | dim | condition | seeds | radius | drift/r | D_mem | D_p90 | D_p95 | D_spec memory | D_center cov | D_center spec | roundness |
| ---: | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `30,000,000` | `3` | `baseline` | `5` | `2.087e-04` [`2.075e-04`, `2.088e-04`] | `0.044` [`0.039`, `0.045`] | `2.941` [`2.920`, `2.944`] | `3.000` [`3.000`, `3.000`] | `3.000` [`3.000`, `3.000`] | `n/a` [`n/a`, `n/a`] | `1.144` [`1.075`, `1.246`] | `1.270` [`1.080`, `1.287`] | `0.843` [`0.814`, `0.847`] |
| `30,000,000` | `3` | `eta_zero` | `5` | `0.001` [`0.001`, `0.001`] | `0.320` [`0.265`, `0.336`] | `1.903` [`1.480`, `2.411`] | `3.000` [`2.000`, `3.000`] | `3.000` [`2.000`, `3.000`] | `n/a` [`n/a`, `n/a`] | `1.145` [`1.075`, `1.245`] | `1.270` [`1.080`, `1.288`] | `0.453` [`0.223`, `0.577`] |
| `30,000,000` | `4` | `baseline` | `5` | `2.421e-04` [`2.418e-04`, `2.449e-04`] | `0.039` [`0.037`, `0.040`] | `3.805` [`3.771`, `3.863`] | `4.000` [`4.000`, `4.000`] | `4.000` [`4.000`, `4.000`] | `2.095` [`2.081`, `2.114`] | `1.095` [`1.039`, `1.273`] | `1.170` [`1.086`, `1.315`] | `0.741` [`0.739`, `0.770`] |
| `30,000,000` | `4` | `eta_zero` | `5` | `0.001` [`0.001`, `0.001`] | `0.301` [`0.259`, `0.304`] | `2.420` [`2.020`, `2.420`] | `3.000` [`3.000`, `3.000`] | `4.000` [`3.000`, `4.000`] | `1.340` [`1.288`, `1.366`] | `1.095` [`1.039`, `1.273`] | `1.169` [`1.085`, `1.315`] | `0.286` [`0.258`, `0.310`] |
| `30,000,000` | `5` | `baseline` | `5` | `2.695e-04` [`2.690e-04`, `2.702e-04`] | `0.045` [`0.042`, `0.050`] | `4.849` [`4.826`, `4.851`] | `5.000` [`5.000`, `5.000`] | `5.000` [`5.000`, `5.000`] | `2.233` [`2.194`, `2.240`] | `1.083` [`1.062`, `1.114`] | `1.087` [`1.086`, `1.096`] | `0.784` [`0.763`, `0.784`] |
| `30,000,000` | `5` | `eta_zero` | `5` | `0.001` [`0.001`, `0.001`] | `0.326` [`0.287`, `0.346`] | `2.055` [`1.917`, `2.244`] | `3.000` [`3.000`, `3.000`] | `4.000` [`4.000`, `4.000`] | `1.304` [`1.304`, `1.309`] | `1.083` [`1.062`, `1.114`] | `1.087` [`1.086`, `1.096`] | `0.195` [`0.190`, `0.196`] |
| `30,000,000` | `7` | `baseline` | `5` | `3.191e-04` [`3.191e-04`, `3.192e-04`] | `0.050` [`0.048`, `0.052`] | `6.618` [`6.450`, `6.626`] | `6.000` [`6.000`, `6.000`] | `7.000` [`7.000`, `7.000`] | `2.424` [`2.395`, `2.522`] | `1.086` [`1.084`, `1.108`] | `1.090` [`1.083`, `1.092`] | `0.671` [`0.659`, `0.678`] |
| `30,000,000` | `7` | `eta_zero` | `5` | `0.002` [`0.002`, `0.002`] | `0.373` [`0.318`, `0.373`] | `3.107` [`2.523`, `4.180`] | `4.000` [`3.000`, `5.000`] | `6.000` [`5.000`, `6.000`] | `1.286` [`1.266`, `1.289`] | `1.086` [`1.084`, `1.108`] | `1.090` [`1.083`, `1.092`] | `0.184` [`0.113`, `0.239`] |
| `30,000,000` | `10` | `baseline` | `5` | `3.826e-04` [`3.807e-04`, `3.829e-04`] | `0.048` [`0.047`, `0.050`] | `8.999` [`8.857`, `9.204`] | `9.000` [`9.000`, `9.000`] | `10.000` [`10.000`, `10.000`] | `2.713` [`2.697`, `2.761`] | `1.080` [`1.077`, `1.161`] | `1.230` [`1.093`, `1.233`] | `0.592` [`0.576`, `0.603`] |
| `30,000,000` | `10` | `eta_zero` | `5` | `0.002` [`0.002`, `0.002`] | `0.322` [`0.320`, `0.335`] | `2.434` [`2.273`, `2.917`] | `4.000` [`4.000`, `4.000`] | `5.000` [`5.000`, `6.000`] | `1.288` [`1.286`, `1.292`] | `1.080` [`1.077`, `1.161`] | `1.230` [`1.092`, `1.233`] | `0.093` [`0.090`, `0.108`] |
| `30,000,000` | `13` | `baseline` | `5` | `4.359e-04` [`4.358e-04`, `4.365e-04`] | `0.049` [`0.047`, `0.050`] | `11.485` [`11.389`, `11.489`] | `11.000` [`11.000`, `11.000`] | `12.000` [`12.000`, `12.000`] | `2.906` [`2.811`, `2.960`] | `1.067` [`1.054`, `1.126`] | `1.086` [`1.070`, `1.234`] | `0.550` [`0.543`, `0.577`] |
| `30,000,000` | `13` | `eta_zero` | `5` | `0.002` [`0.002`, `0.002`] | `0.371` [`0.363`, `0.374`] | `2.908` [`2.456`, `3.224`] | `5.000` [`5.000`, `5.000`] | `7.000` [`7.000`, `7.000`] | `1.283` [`1.270`, `1.317`] | `1.067` [`1.054`, `1.125`] | `1.086` [`1.070`, `1.234`] | `0.083` [`0.070`, `0.087`] |
| `30,000,000` | `20` | `baseline` | `5` | `5.393e-04` [`5.391e-04`, `5.404e-04`] | `0.051` [`0.047`, `0.053`] | `16.778` [`16.634`, `16.839`] | `17.000` [`17.000`, `17.000`] | `18.000` [`18.000`, `18.000`] | `3.074` [`3.049`, `3.172`] | `1.088` [`1.082`, `1.121`] | `1.073` [`1.072`, `1.110`] | `0.474` [`0.461`, `0.480`] |
| `30,000,000` | `20` | `eta_zero` | `5` | `0.003` [`0.003`, `0.003`] | `0.366` [`0.351`, `0.373`] | `3.100` [`2.389`, `3.330`] | `5.000` [`5.000`, `6.000`] | `8.000` [`8.000`, `9.000`] | `1.282` [`1.241`, `1.285`] | `1.088` [`1.082`, `1.121`] | `1.073` [`1.072`, `1.110`] | `0.049` [`0.042`, `0.055`] |

## Baseline/Control Separation

| dim | radius gain eta0/baseline | drift/r gain eta0/baseline | D_mem delta | D_spec memory delta | roundness delta |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `3` | `4.959` | `7.327` | `1.038` | `n/a` | `0.391` |
| `4` | `5.119` | `7.643` | `1.385` | `0.755` | `0.456` |
| `5` | `5.107` | `7.230` | `2.794` | `0.928` | `0.589` |
| `7` | `5.207` | `7.531` | `3.510` | `1.138` | `0.487` |
| `10` | `5.350` | `6.761` | `6.565` | `1.425` | `0.499` |
| `13` | `5.277` | `7.605` | `8.577` | `1.624` | `0.467` |
| `20` | `5.444` | `7.239` | `13.678` | `1.792` | `0.425` |

## Interpretation

- Paper I can use this as a stronger teaser: the scalar reference is not
  just compact, it has a clear local memory-geometry signal in the
  chosen 3D slice.
- The strong ambient-independent 3D claim fails in the strict `D_mem`
  sense: `D_mem`, `D_p90`, and `D_p95` grow with supplied dimension.
- The interesting Paper-II opening is spectral/coarse geometry:
  `D_spec memory` moves toward about three while `D_mem` keeps rising.
- `D_center` is an external/coarse trace observable, but a single drifting
  knot still need not sample the full external interaction sector.
- The next decisive test is relational: a weak second knot or external
  field should see an effective response rank near three if the
  external-sector interpretation is correct.

## Next Checks

1. Add D_spec bandwidth/kNN sensitivity before treating `D_spec ~=3` as robust.
2. Run the same audit on any completed higher-N d10/d13 cases once case JSONs exist.
3. Add a response-rank experiment with a second knot or weak external probe.
4. Keep Paper I wording at `local memory-shape evidence in a chosen 3D embedding`.
