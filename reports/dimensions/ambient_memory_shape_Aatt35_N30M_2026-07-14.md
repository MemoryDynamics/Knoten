# Ambient-Dimension Memory-Shape Check

Date: 2026-07-14T05:55:04Z.

## Scope

This report tests whether the current `D_mem ~= 3` scalar reference
candidate remains a local memory-shape feature beyond the originally
chosen 3D embedding. It is not a dimension-selection theorem and not a
macroscopic spacetime claim.

Fixed target slice: `A_att=35`, `epsilon=1e-4`, corrected q=3 scalar
kernel, `baseline` versus matched `eta_zero`, same co-moving dynamic
center observables as the Paper-I N30M reference. The report also
tracks unweighted point-cloud spectral dimensions `D_spec` for the sampled path and
the memory cloud as Paper-II geometry reconciliation metrics.

## Provenance

- Source dirs: `data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d10_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d13_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d20_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d4_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d5_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d7_seed1-5_eps1em4_2026-07-13`
- Machine-readable summary: `reports/dimensions/ambient_memory_shape_Aatt35_N30M_summary_2026-07-14.json`
- Git revision while building this report: `c1e8c79b4521531f6bf0eef9f0502045f246f988`
- Git status while building this report: `?? reports/dimensions/ambient_memory_shape_Aatt35_N30M_summary_2026-07-14.json`

## Dimension Summary

| dim | condition | seeds | N | radius median [q1,q3] | drift/r median [q1,q3] | D_mem median [q1,q3] | D_spec sample median [q1,q3] | D_spec memory median [q1,q3] | roundness median [q1,q3] |
| ---: | --- | ---: | ---: | --- | --- | --- | --- | --- | --- |
| `4` | `baseline` | `5` | `30,000,000` | `2.421e-04` [`2.418e-04`, `2.449e-04`] | `0.039` [`0.037`, `0.040`] | `3.805` [`3.771`, `3.863`] | `1.263` [`1.258`, `1.354`] | `2.095` [`2.081`, `2.114`] | `0.741` [`0.739`, `0.770`] |
| `4` | `eta_zero` | `5` | `30,000,000` | `0.001` [`0.001`, `0.001`] | `0.301` [`0.259`, `0.304`] | `2.420` [`2.020`, `2.420`] | `1.263` [`1.258`, `1.354`] | `1.340` [`1.288`, `1.366`] | `0.286` [`0.258`, `0.310`] |
| `5` | `baseline` | `5` | `30,000,000` | `2.695e-04` [`2.690e-04`, `2.702e-04`] | `0.045` [`0.042`, `0.050`] | `4.849` [`4.826`, `4.851`] | `1.326` [`1.304`, `1.342`] | `2.233` [`2.194`, `2.240`] | `0.784` [`0.763`, `0.784`] |
| `5` | `eta_zero` | `5` | `30,000,000` | `0.001` [`0.001`, `0.001`] | `0.326` [`0.287`, `0.346`] | `2.055` [`1.917`, `2.244`] | `1.325` [`1.304`, `1.342`] | `1.304` [`1.304`, `1.309`] | `0.195` [`0.190`, `0.196`] |
| `7` | `baseline` | `5` | `30,000,000` | `3.191e-04` [`3.191e-04`, `3.192e-04`] | `0.050` [`0.048`, `0.052`] | `6.618` [`6.450`, `6.626`] | `1.303` [`1.265`, `1.304`] | `2.424` [`2.395`, `2.522`] | `0.671` [`0.659`, `0.678`] |
| `7` | `eta_zero` | `5` | `30,000,000` | `0.002` [`0.002`, `0.002`] | `0.373` [`0.318`, `0.373`] | `3.107` [`2.523`, `4.180`] | `1.303` [`1.264`, `1.304`] | `1.286` [`1.266`, `1.289`] | `0.184` [`0.113`, `0.239`] |
| `10` | `baseline` | `5` | `30,000,000` | `3.826e-04` [`3.807e-04`, `3.829e-04`] | `0.048` [`0.047`, `0.050`] | `8.999` [`8.857`, `9.204`] | `1.294` [`1.276`, `1.348`] | `2.713` [`2.697`, `2.761`] | `0.592` [`0.576`, `0.603`] |
| `10` | `eta_zero` | `5` | `30,000,000` | `0.002` [`0.002`, `0.002`] | `0.322` [`0.320`, `0.335`] | `2.434` [`2.273`, `2.917`] | `1.293` [`1.276`, `1.347`] | `1.288` [`1.286`, `1.292`] | `0.093` [`0.090`, `0.108`] |
| `13` | `baseline` | `5` | `30,000,000` | `4.359e-04` [`4.358e-04`, `4.365e-04`] | `0.049` [`0.047`, `0.050`] | `11.485` [`11.389`, `11.489`] | `1.295` [`1.271`, `1.309`] | `2.906` [`2.811`, `2.960`] | `0.550` [`0.543`, `0.577`] |
| `13` | `eta_zero` | `5` | `30,000,000` | `0.002` [`0.002`, `0.002`] | `0.371` [`0.363`, `0.374`] | `2.908` [`2.456`, `3.224`] | `1.295` [`1.270`, `1.309`] | `1.283` [`1.270`, `1.317`] | `0.083` [`0.070`, `0.087`] |
| `20` | `baseline` | `5` | `30,000,000` | `5.393e-04` [`5.391e-04`, `5.404e-04`] | `0.051` [`0.047`, `0.053`] | `16.778` [`16.634`, `16.839`] | `1.284` [`1.277`, `1.286`] | `3.074` [`3.049`, `3.172`] | `0.474` [`0.461`, `0.480`] |
| `20` | `eta_zero` | `5` | `30,000,000` | `0.003` [`0.003`, `0.003`] | `0.366` [`0.351`, `0.373`] | `3.100` [`2.389`, `3.330`] | `1.284` [`1.277`, `1.285`] | `1.282` [`1.241`, `1.285`] | `0.049` [`0.042`, `0.055`] |

## Baseline/Control Separation

| dim | radius gain eta0/baseline | drift separation eta0/baseline | D_mem delta | D_spec memory delta | roundness delta |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `4` | `5.119` | `7.643` | `1.385` | `0.755` | `0.456` |
| `5` | `5.107` | `7.230` | `2.794` | `0.928` | `0.589` |
| `7` | `5.207` | `7.531` | `3.510` | `1.138` | `0.487` |
| `10` | `5.350` | `6.761` | `6.565` | `1.425` | `0.499` |
| `13` | `5.277` | `7.605` | `8.577` | `1.624` | `0.467` |
| `20` | `5.444` | `7.239` | `13.678` | `1.792` | `0.425` |

## Reading Rules

- A robust extension of the current 3D finding requires compact active
  memory clouds, low radius-normalized drift, and `D_mem` near three
  with roundness separated from `eta_zero` across ambient dimensions.
- If `D_mem` rises with ambient dimension, the old phrase `chosen 3D
  embedding` remains necessary and Paper II must treat 3D as open.
- `D_spec` is an unweighted point-cloud spectral-geometry check. Agreement with
  `D_mem` near three strengthens the Paper-II geometry reading;
  disagreement flags estimator or scale sensitivity rather than a direct
  failure of the memory-shape claim.
- If `D_mem` stays near three while roundness and compactness remain
  controlled, the phrase can be upgraded to a local 3D memory-shape
  phenomenon that is not tied to the original embedding.
