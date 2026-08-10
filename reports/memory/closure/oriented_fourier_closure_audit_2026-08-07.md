# Passive oriented-memory Fourier closure audit

Date: 2026-08-07T04:26:43.911943+00:00

## Question

After subtracting the exact new directed deposit and finite-horizon tail,
does the full retained vector memory contain any wave-number-dependent
homogeneous feedback beyond the known forgetting factor?

## Exact null

For every Fourier vector mode, the finite update predicts

\[
m_{n+1,k}-J_{n+1,k}+T_{n,k}=(1-\lambda_v)m_{n,k}.
\]

The audit separates longitudinal and transverse components over four
dimensionless wave numbers and two time segments for six mature sources.

## Decision

Status: **pass** (6/6 seeds).

A pass here confirms the homogeneous passive null. It is evidence against,
not for, emergent active spatial feedback in the implemented update.

## Seed results

| seed | max abs(q_hat-q) | max normalized residual | max abs(b_hat,c_hat) | pass |
| ---: | ---: | ---: | ---: | --- |
| 1 | 4.219e-15 | 0.000e+00 | 1.685e-15 | pass |
| 2 | 4.885e-15 | 0.000e+00 | 1.879e-15 | pass |
| 3 | 6.550e-15 | 0.000e+00 | 1.531e-15 | pass |
| 4 | 4.774e-15 | 0.000e+00 | 1.253e-15 | pass |
| 5 | 5.329e-15 | 0.000e+00 | 1.743e-15 | pass |
| 6 | 3.775e-15 | 0.000e+00 | 1.871e-15 | pass |

## Interpretation

The complete passive memory is exactly source plus exponential forgetting
within floating-point error. No longitudinal/transverse splitting or
k-squared/k-fourth coefficient is selected by these continuations.

Consequently, coefficients of an active covariant field cannot be read
from this passive law as microscopic constants. They must either arise
in a separately validated coarse-graining that omits resolved source
variables, or be declared as a new model increment. Longer runs cannot
change this exact source-conditioned identity.

The result does not exclude nonlinear feedback after adding a new field
law. It prevents calling such a law parameter-free or already emergent.

## Figure

![Fourier closure](../../figures/draft/memory/oriented_fourier_closure_audit_2026-08-07.png)

## Reproducibility

- Analysis revision: 3ca5d0f44246ed803d70b2f5cba6136272ff367c
- Worktree at start: clean
- Memory times: 20.0
- kR values: [0.5, 1.0, 2.0, 4.0]
- Command: python experiments/current/memory/closure/oriented_fourier_closure_audit.py
- Seed 1: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed1_steps3000000.json, SHA-256 10c8650d40d1fff01c2bc7aa6d4661f271acff35fe9395dfc101e6448d746614
- Seed 2: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed2_steps3000000.json, SHA-256 41e5def5bee92feebd204ac89ab2566ac2960af0d6933f09129251f12e361188
- Seed 3: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed3_steps3000000.json, SHA-256 882721c56e67ed90e3c937d54223c1bdb6e4dcb970877edf3a267e9ab9919816
- Seed 4: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed4_steps3000000.json, SHA-256 7e7b0949b45e14413ee6901fe5e3a9a657e4a30e2b1401679d3f7e1e08b9bc6e
- Seed 5: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed5_steps3000000.json, SHA-256 a3f41aebf2673c3cbffc38d163f0e448d505565605a730f41bddf269382730f1
- Seed 6: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed6_2026-07-22/case_baseline_seed6_steps3000000.json, SHA-256 ecdec2a7324bba2b2047c224b15e6ec80414b29503c927b9a94f7da73b408217
