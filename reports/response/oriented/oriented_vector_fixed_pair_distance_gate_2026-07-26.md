# Fixed-coupling independent-pair distance gate

Date: 2026-07-26T04:49:35+00:00

## Question

Does the introduced oriented-memory readout generalize from cloned
source/target states to cyclically paired independent scalar formations
under one globally fixed coupling, and does its response attenuate over
a preregistered distance ladder?

This tests one fixed phenomenological channel. The vector state,
instantaneous Gaussian readout, passive source, and width rule
`sigma_v=2.5 R_source` remain model inputs. This is a fixed
dimensionless rule, not yet one universal absolute length scale.

## Preregistered design

- cyclic independent pairs: `['1<-2', '2<-3', '3<-4', '4<-5', '5<-6', '6<-1']`;
- global `eta_v=5.079e-06` without pairwise calibration;
- distances `[2.5, 5.0, 10.0]` in `R_pair=(R_source+R_target)/2`;
- 64 random-sign controls plus channel-off, global flip, and one-step memory;
- common target/source future noise and identical random signs across
  distances and memory arms within each pair;
- tangential fraction is reported but is not a gate because the pair
  axis is arbitrary relative to independently formed source orientation.

Near pass requires response, random-sign separation, persistent-memory
gain, sign reversal, and source/target shape bounds. Distance pass requires
non-increasing response within 10% tolerance and far/near <= 0.1.
Overall pass requires at least 5 of 6 pairs.

## Decision

Gate status: **pass** (6/6 pairs).

Selected next step: **local_or_retarded_oriented_mediator_gate**.

## Pair results

| target<-source | near active/R | near active/q95 | one-step/q95 | memory gain | flip cos | tangent | far/near | monotone | shape bounded | pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1<-2 | 0.0047 | 6.7565 | 1.4638 | 4.6157 | -1.0000 | 0.8902 | 0.0028 | yes | yes | pass |
| 2<-3 | 0.0018 | 3.1582 | 1.4040 | 2.2494 | -1.0000 | 0.9469 | 9.359e-04 | yes | yes | pass |
| 3<-4 | 0.0050 | 8.1709 | 1.6556 | 4.9352 | -1.0000 | 0.3405 | 0.0025 | yes | yes | pass |
| 4<-5 | 0.0078 | 11.6973 | 1.3535 | 8.6425 | -1.0000 | 0.9996 | 0.0016 | yes | yes | pass |
| 5<-6 | 0.0024 | 4.0968 | 1.3736 | 2.9825 | -1.0000 | 0.5915 | 0.0019 | yes | yes | pass |
| 6<-1 | 0.0036 | 6.5650 | 1.5392 | 4.2654 | -1.0000 | 0.9145 | 9.967e-04 | yes | yes | pass |

## Distance-resolved results

| target<-source | distance/R_pair | distance/R_source | initial field | active/R | random q95/R | active/q95 | target shape | source spectrum |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1<-2 | 2.5000 | 2.3951 | 0.0135 | 0.0047 | 6.932e-04 | 6.7565 | 2.501e-04 | 0.0984 |
| 1<-2 | 5.0000 | 4.7902 | 0.0039 | 0.0015 | 2.223e-04 | 6.7951 | 8.374e-05 | 0.0984 |
| 1<-2 | 10.0000 | 9.5804 | 2.417e-05 | 1.313e-05 | 2.076e-06 | 6.3260 | 9.588e-07 | 0.0984 |
| 2<-3 | 2.5000 | 2.5982 | 0.0114 | 0.0018 | 5.598e-04 | 3.1582 | 2.981e-04 | 0.0858 |
| 2<-3 | 5.0000 | 5.1963 | 0.0026 | 3.569e-04 | 1.519e-04 | 2.3492 | 9.751e-05 | 0.0858 |
| 2<-3 | 10.0000 | 10.3926 | 5.890e-06 | 1.654e-06 | 5.697e-07 | 2.9040 | 5.142e-07 | 0.0858 |
| 3<-4 | 2.5000 | 2.4222 | 0.0093 | 0.0050 | 6.137e-04 | 8.1709 | 1.876e-04 | 0.0933 |
| 3<-4 | 5.0000 | 4.8445 | 0.0026 | 0.0016 | 1.902e-04 | 8.4820 | 5.878e-05 | 0.0933 |
| 3<-4 | 10.0000 | 9.6890 | 1.364e-05 | 1.265e-05 | 1.601e-06 | 7.8978 | 6.360e-07 | 0.0933 |
| 4<-5 | 2.5000 | 2.5440 | 0.0124 | 0.0078 | 6.643e-04 | 11.6973 | 5.055e-04 | 0.1033 |
| 4<-5 | 5.0000 | 5.0881 | 0.0030 | 0.0023 | 1.889e-04 | 12.0622 | 1.645e-04 | 0.1033 |
| 4<-5 | 10.0000 | 10.1762 | 8.992e-06 | 1.219e-05 | 1.364e-06 | 8.9367 | 1.035e-06 | 0.1033 |
| 5<-6 | 2.5000 | 2.4988 | 0.0079 | 0.0024 | 5.928e-04 | 4.0968 | 2.563e-04 | 0.1011 |
| 5<-6 | 5.0000 | 4.9977 | 0.0020 | 7.499e-04 | 1.748e-04 | 4.2898 | 7.813e-05 | 0.1011 |
| 5<-6 | 10.0000 | 9.9953 | 7.662e-06 | 4.665e-06 | 1.149e-06 | 4.0613 | 5.425e-07 | 0.1011 |
| 6<-1 | 2.5000 | 2.5544 | 0.0122 | 0.0036 | 5.453e-04 | 6.5650 | 3.358e-04 | 0.1323 |
| 6<-1 | 5.0000 | 5.1087 | 0.0027 | 9.052e-04 | 1.428e-04 | 6.3371 | 8.752e-05 | 0.1323 |
| 6<-1 | 10.0000 | 10.2175 | 7.235e-06 | 3.568e-06 | 7.044e-07 | 5.0655 | 3.628e-07 | 0.1323 |

## Interpretation boundary

The pass supports only cross-state reproducibility and spatial
attenuation of the deliberately introduced instantaneous oriented
Gaussian readout under its fixed coupling and width rule. It does
not establish a universal potential, reciprocity, retardation, a
conservation law, QFT, spin, charge, photons, or particles.
A local/retarded mediator is the next discriminating mechanism test.

## Figure

![Fixed-pair distance gate](../../figures/draft/response/oriented_vector_fixed_pair_distance_gate_2026-07-26.png)

## Reproducibility

- Formation config: `{"alpha": 0.01, "amplitude_att": 35.0, "amplitude_rep": 1.0, "burn_in": 0, "deposition_kernel": "delta", "deposition_sigma": 0.0, "dim": 3, "epsilon": 0.0001, "eta": 0.15, "max_memory": 800, "memory_factor": 6.0, "memory_mass": 1.0, "sample_every": 1000, "sigma_att": 3.0, "sigma_rep": 1.0, "steps": 3000000}`
- Pair 1<-2: target `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed1_steps3000000.json` SHA-256 `10c8650d40d1fff01c2bc7aa6d4661f271acff35fe9395dfc101e6448d746614`; source `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed2_steps3000000.json` SHA-256 `41e5def5bee92feebd204ac89ab2566ac2960af0d6933f09129251f12e361188`
- Pair 2<-3: target `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed2_steps3000000.json` SHA-256 `41e5def5bee92feebd204ac89ab2566ac2960af0d6933f09129251f12e361188`; source `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed3_steps3000000.json` SHA-256 `882721c56e67ed90e3c937d54223c1bdb6e4dcb970877edf3a267e9ab9919816`
- Pair 3<-4: target `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed3_steps3000000.json` SHA-256 `882721c56e67ed90e3c937d54223c1bdb6e4dcb970877edf3a267e9ab9919816`; source `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed4_steps3000000.json` SHA-256 `7e7b0949b45e14413ee6901fe5e3a9a657e4a30e2b1401679d3f7e1e08b9bc6e`
- Pair 4<-5: target `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed4_steps3000000.json` SHA-256 `7e7b0949b45e14413ee6901fe5e3a9a657e4a30e2b1401679d3f7e1e08b9bc6e`; source `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed5_steps3000000.json` SHA-256 `a3f41aebf2673c3cbffc38d163f0e448d505565605a730f41bddf269382730f1`
- Pair 5<-6: target `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed5_steps3000000.json` SHA-256 `a3f41aebf2673c3cbffc38d163f0e448d505565605a730f41bddf269382730f1`; source `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed6_2026-07-22/case_baseline_seed6_steps3000000.json` SHA-256 `ecdec2a7324bba2b2047c224b15e6ec80414b29503c927b9a94f7da73b408217`
- Pair 6<-1: target `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed6_2026-07-22/case_baseline_seed6_steps3000000.json` SHA-256 `ecdec2a7324bba2b2047c224b15e6ec80414b29503c927b9a94f7da73b408217`; source `data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed1_steps3000000.json` SHA-256 `10c8650d40d1fff01c2bc7aa6d4661f271acff35fe9395dfc101e6448d746614`
- Analysis revision: 3df1c9412b655d473b10a205ef30e5a4c14e25b3
- Worktree at start: `clean`
- Summary: reports/response/oriented/oriented_vector_fixed_pair_distance_gate_2026-07-26.json
- Command: python experiments/current/memory/synchronization/one_way/oriented_vector_fixed_pair_distance_gate.py
