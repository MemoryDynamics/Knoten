# Paper I Evidence Table: N=30M Dynamic-Center Trace

Date: 2026-07-13T12:02:25Z.

## Scope

This report condenses the corrected-sign scalar long-run evidence into a
Paper-I-facing table. It is deliberately conservative: the accepted claim
is a co-moving compact memory-cloud regime, not a fixed absolute center,
not a spin/phase mode, and not a physical particle identification.

## Provenance

- Source aggregate: `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_summary_2026-07-13.json`
- Git revision while building this report: `27b8b2d4f9b068f7e740dcd08161d4ffa6057e2a`
- Git status while building this report: `?? experiments/current/dynamics/paper_i_evidence_table.py
?? experiments/current/markov/long_run_trace_ar_report.py
?? reports/long_runs/long_3e8/long_run_trace_ar_modes_N30M_eps1em4_2026-07-13.md
?? reports/long_runs/long_3e8/paper_i_evidence_table_N30M_eps1em4_2026-07-13.md
?? tests/test_long_run_trace_ar_report.py
?? tests/test_paper_i_evidence_table.py`

## Main Evidence Rows

| A_att | seeds | N | radius active | radius eta=0 | radius gain | drift/r active | drift/r eta=0 | drift separation | D_mem active | D_mem eta=0 | roundness active | roundness eta=0 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `5` | `30,000,000` | `2.916e-04` | `0.001` | `3.550` | `0.072` | `0.320` | `4.449` | `2.803` | `1.903` | `0.719` | `0.453` |
| `35` | `5` | `30,000,000` | `2.087e-04` | `0.001` | `4.959` | `0.044` | `0.320` | `7.327` | `2.941` | `1.903` | `0.843` | `0.453` |

## Residence And Spin Guardrails

| A_att | voxel residence active | voxel residence eta=0 | final-center residence active | final-center residence eta=0 | spin axis active | raw L dephasing active |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20` | `680.833` | `1540.278` | `60.000` | `10.000` | `0.011` | `<= 0.010` |
| `35` | `651.667` | `1540.278` | `140.000` | `10.000` | `0.010` | `<= 0.010` |

## Reading

- Current scalar reference candidate: `A_att=35`, `epsilon=1e-4`.
- The strongest Paper-I evidence is not raw voxel residence, because the
  `eta_zero` control can also produce long residence in its own broad
  voxelized path. The discriminating observables are co-moving radius,
  radius-normalized center drift, memory-shape dimension, and roundness.
- For `A_att=35`, the active radius is about
  `4.959` times smaller
  than the matched `eta_zero` control and the radius-normalized center
  drift is separated by about `7.327`.
- The scalar spin proxy remains negative: axis polarization is near zero
  and raw spin dephasing is only an upper bound at the first resolved lag.

## Paper-I Claim Boundary

Supported: the corrected scalar model has seed-robust co-moving compact
memory-cloud candidates in this parameter slice, strongest at `A_att=35`.

Not supported here: a fixed absolute spatial knot, a stable spin axis,
an oscillatory/photon-like mode, a physical mass claim, or a claim that
three external dimensions have been derived.
