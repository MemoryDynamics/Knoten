# D_spec Sensitivity Audit

Date: 2026-07-15T17:30:48Z.

## Scope

This audit is the next Paper-II guardrail after the 3D dimension claim audit.
The existing case JSONs do not store raw memory-cloud coordinates, so this
report does not remeasure the original clouds. Instead it separates:

- stored historical `D_spec memory` values from the case summaries;
- covariance-matched Gaussian surrogates using the saved memory covariance eigenvalues;
- symmetric heat-kernel bandwidth sensitivity;
- kNN graph-scale sensitivity.

The result is a methodological stress test, not a new dimension-selection claim.

## Provenance

- Source dirs: `data/processed/long_run_metastability/dynamic_center_trace_q3_Aatt_35_N30M_seed1-5_eps1em4_rerun_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d4_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d5_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d7_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d10_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d13_seed1-5_eps1em4_2026-07-13, data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d20_seed1-5_eps1em4_2026-07-13`
- Machine-readable summary: `reports/dimensions/dspec_sensitivity_summary_2026-07-15.json`
- Git revision while building this report: `c93664efd58fd5baacfc3fe6dd12dac52719919c`
- Git status while building this report: `M src/emergenz_knoten/diagnostics.py;  M tests/test_core.py; ?? experiments/current/dynamics/dspec_sensitivity_report.py; ?? figures/draft/dimensions/dspec_sensitivity_2026-07-15/; ?? reports/dimensions/dspec_sensitivity_summary_2026-07-15.json; ?? tests/test_dspec_sensitivity_report.py`

## Figures

- [dspec_sensitivity_by_dimension](../../figures/draft/dimensions/dspec_sensitivity_2026-07-15/dspec_sensitivity_by_dimension.png)
- [dspec_sensitivity_ranges](../../figures/draft/dimensions/dspec_sensitivity_2026-07-15/dspec_sensitivity_ranges.png)

## Main Summary

| N | dim | condition | seeds | D_mem | stored D_spec | sym heat f=0.5 | sym heat f=1 | sym heat f=2 | kNN 32 | heat range | kNN range | near-3 heat fraction |
| ---: | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `30,000,000` | `3` | `baseline` | `5` | `2.941` [`2.920`, `2.944`] | `n/a` [`n/a`, `n/a`] | `2.321` [`2.258`, `2.379`] | `1.754` [`1.731`, `1.778`] | `1.519` [`1.503`, `1.533`] | `4.758` [`4.729`, `4.781`] | `2.281` [`2.260`, `2.434`] | `15.807` [`15.452`, `15.946`] | `0` [`0`, `0`] |
| `30,000,000` | `3` | `eta_zero` | `5` | `1.903` [`1.480`, `2.411`] | `n/a` [`n/a`, `n/a`] | `2.171` [`1.916`, `2.218`] | `1.597` [`1.499`, `1.632`] | `1.342` [`1.281`, `1.386`] | `4.519` [`4.421`, `4.557`] | `1.844` [`1.694`, `2.369`] | `15.205` [`14.896`, `15.526`] | `0.200` [`0`, `0.200`] |
| `30,000,000` | `4` | `baseline` | `5` | `3.805` [`3.771`, `3.863`] | `2.095` [`2.081`, `2.114`] | `2.620` [`2.585`, `2.663`] | `1.951` [`1.918`, `1.957`] | `1.669` [`1.650`, `1.681`] | `5.035` [`4.965`, `5.052`] | `2.805` [`2.577`, `3.036`] | `13.140` [`13.094`, `13.263`] | `0` [`0`, `0`] |
| `30,000,000` | `4` | `eta_zero` | `5` | `2.420` [`2.020`, `2.420`] | `1.340` [`1.288`, `1.366`] | `2.133` [`2.096`, `2.157`] | `1.614` [`1.584`, `1.633`] | `1.382` [`1.337`, `1.384`] | `4.520` [`4.461`, `4.521`] | `2.211` [`1.774`, `2.243`] | `12.311` [`12.234`, `12.336`] | `0` [`0`, `0.200`] |
| `30,000,000` | `5` | `baseline` | `5` | `4.849` [`4.826`, `4.851`] | `2.233` [`2.194`, `2.240`] | `2.748` [`2.665`, `2.759`] | `2.026` [`2.016`, `2.034`] | `1.751` [`1.745`, `1.759`] | `5.183` [`5.091`, `5.248`] | `2.864` [`2.219`, `3.045`] | `12.010` [`11.533`, `12.054`] | `0` [`0`, `0.200`] |
| `30,000,000` | `5` | `eta_zero` | `5` | `2.055` [`1.917`, `2.244`] | `1.304` [`1.304`, `1.309`] | `2.008` [`1.997`, `2.026`] | `1.545` [`1.531`, `1.545`] | `1.320` [`1.318`, `1.336`] | `4.459` [`4.410`, `4.477`] | `1.935` [`1.905`, `1.952`] | `11.342` [`10.948`, `11.727`] | `0.200` [`0.200`, `0.200`] |
| `30,000,000` | `7` | `baseline` | `5` | `6.618` [`6.450`, `6.626`] | `2.424` [`2.395`, `2.522`] | `2.825` [`2.714`, `2.858`] | `2.191` [`2.098`, `2.209`] | `1.922` [`1.835`, `1.930`] | `5.334` [`5.185`, `5.442`] | `2.980` [`2.894`, `3.032`] | `10.190` [`10.074`, `10.769`] | `0.200` [`0`, `0.200`] |
| `30,000,000` | `7` | `eta_zero` | `5` | `3.107` [`2.523`, `4.180`] | `1.286` [`1.266`, `1.289`] | `2.130` [`2.108`, `2.233`] | `1.618` [`1.618`, `1.750`] | `1.403` [`1.389`, `1.533`] | `4.467` [`4.413`, `4.599`] | `2.188` [`2.134`, `2.209`] | `9.777` [`9.583`, `9.947`] | `0` [`0`, `0`] |
| `30,000,000` | `10` | `baseline` | `5` | `8.999` [`8.857`, `9.204`] | `2.713` [`2.697`, `2.761`] | `2.999` [`2.942`, `3.038`] | `2.366` [`2.327`, `2.390`] | `2.103` [`2.067`, `2.128`] | `5.568` [`5.492`, `5.613`] | `3.000` [`2.646`, `3.946`] | `9.623` [`9.595`, `9.796`] | `0.200` [`0.200`, `0.200`] |
| `30,000,000` | `10` | `eta_zero` | `5` | `2.434` [`2.273`, `2.917`] | `1.288` [`1.286`, `1.292`] | `1.997` [`1.993`, `2.117`] | `1.583` [`1.529`, `1.598`] | `1.376` [`1.323`, `1.391`] | `4.331` [`4.304`, `4.335`] | `2.057` [`1.801`, `2.285`] | `9.456` [`9.364`, `9.456`] | `0` [`0`, `0.200`] |
| `30,000,000` | `13` | `baseline` | `5` | `11.485` [`11.389`, `11.489`] | `2.906` [`2.811`, `2.960`] | `2.994` [`2.963`, `2.994`] | `2.443` [`2.392`, `2.466`] | `2.204` [`2.169`, `2.233`] | `5.472` [`5.404`, `5.573`] | `3.484` [`3.230`, `3.863`] | `8.702` [`8.645`, `8.989`] | `0.200` [`0.200`, `0.200`] |
| `30,000,000` | `13` | `eta_zero` | `5` | `2.908` [`2.456`, `3.224`] | `1.283` [`1.270`, `1.317`] | `2.056` [`2.042`, `2.086`] | `1.590` [`1.569`, `1.602`] | `1.384` [`1.359`, `1.396`] | `4.304` [`4.297`, `4.332`] | `1.987` [`1.882`, `2.200`] | `8.957` [`8.914`, `9.273`] | `0.200` [`0`, `0.200`] |
| `30,000,000` | `20` | `baseline` | `5` | `16.778` [`16.634`, `16.839`] | `3.074` [`3.049`, `3.172`] | `3.429` [`3.349`, `3.441`] | `2.853` [`2.803`, `2.870`] | `2.626` [`2.584`, `2.642`] | `6.015` [`5.919`, `6.043`] | `4.572` [`4.495`, `4.897`] | `8.781` [`8.366`, `9.158`] | `0.200` [`0.200`, `0.200`] |
| `30,000,000` | `20` | `eta_zero` | `5` | `3.100` [`2.389`, `3.330`] | `1.282` [`1.241`, `1.285`] | `2.009` [`1.946`, `2.060`] | `1.576` [`1.521`, `1.604`] | `1.386` [`1.322`, `1.402`] | `4.315` [`4.230`, `4.367`] | `1.996` [`1.842`, `2.119`] | `8.677` [`8.653`, `8.904`] | `0` [`0`, `0.200`] |

## Synthetic Rank Controls

These controls use known-rank Gaussian clouds embedded in 20 dimensions.
They show how strongly the current lightweight D_spec proxy depends on scale.

| true rank | D_cov | heat f=0.25 | heat f=0.5 | heat f=1 | heat f=2 | heat f=4 | kNN 32 |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| `1` | `1.000` | `2.124` | `1.901` | `1.624` | `1.382` | `1.225` | `4.404` |
| `2` | `1.998` | `2.835` | `1.970` | `1.578` | `1.389` | `1.300` | `4.568` |
| `3` | `2.978` | `4.049` | `2.385` | `1.788` | `1.546` | `1.440` | `4.801` |
| `5` | `4.974` | `4.476` | `2.886` | `2.182` | `1.893` | `1.761` | `5.395` |
| `10` | `9.823` | `5.656` | `3.453` | `2.760` | `2.463` | `2.317` | `6.334` |
| `15` | `14.509` | `7.301` | `3.680` | `3.051` | `2.797` | `2.676` | `6.465` |

## Interpretation

- The previous `D_spec memory ~=3` signal should be treated as legacy and exploratory.
  The old implementation used a row-normalized kernel with a symmetric eigenvalue solver;
  future runs should use the symmetric normalized heat kernel or an explicitly non-symmetric solver.
- The covariance-surrogate stress test is scale-sensitive: changing bandwidth or kNN scale
  moves the diagnostic by order-one amounts in several dimensions.
- Therefore `D_spec memory` remains a useful Paper-II lead, but it is not yet a robust
  external-dimension observable.
- The next data-format change should persist a small raw final memory-cloud snapshot
  so D_spec sensitivity can be run on actual clouds instead of covariance surrogates.
- The next physics-facing test remains relational response rank: if an external sector is
  effectively three-dimensional, a weak second knot or probe should see a rank-near-3 response.

## Decision

Do not use `D_spec ~=3` as a Paper-I or Paper-II claim yet. Use it only as a
hypothesis-generating diagnostic that now requires raw-cloud persistence and response-rank validation.
