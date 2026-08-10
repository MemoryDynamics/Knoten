# Full oriented-memory source eligibility gate

Date: 2026-08-07T03:59:58.138593+00:00

## Question

Does the persistent directed deposition history of six mature scalar
sources carry a source-local polar or circulation-bivector moment that
remains bounded and exceeds a depositwise random-sign null?

This is an eligibility test for an explicitly added passive vector fibre.
It is not a spin, charge, flavor, particle, phase, or QFT test.

## Preregistered design

- six independent d=3, N=3M scalar formation states;
- 20 memory times with 100 linear trace intervals;
- all retained deposits, not reduced carrier-only features;
- 256 deposit-sign randomizations and q=0.99 at every sample;
- late-half median observed/null >= 2, axis cosine >= 0.8,
  amplitude CV <= 0.5, and the existing source shape bounds;
- each channel is decided separately and requires at least 5/6 seeds.

## Decision

Polarization eligibility: **fail** (0/6 seeds).

Circulation-bivector eligibility: **fail** (0/6 seeds).

All six polarization traces clear the random-sign separation and all six
sources remain shape-bounded. Five fail axis identity; seed 2 additionally
fails the amplitude-CV gate. All six circulation traces fail random-sign
separation before any physical interpretation is considered.
## Seed results

| seed | polar/null | polar axis | polar CV | polar | circ/null | circ axis | circ CV | circ | radius drift | spectrum drift |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: |
| 1 | 4.4864 | 0.6844 | 0.3513 | fail | 0.6160 | 0.9237 | 0.4742 | fail | 0.2224 | 0.1047 |
| 2 | 3.4175 | 0.8552 | 0.6719 | fail | 0.6626 | -0.3622 | 0.5376 | fail | 0.1216 | 0.0977 |
| 3 | 3.5684 | -0.8846 | 0.3743 | fail | 0.7631 | 0.6535 | 0.3911 | fail | 0.0969 | 0.0893 |
| 4 | 3.8485 | -0.2491 | 0.2933 | fail | 0.5496 | -0.8175 | 0.4724 | fail | 0.1495 | 0.1151 |
| 5 | 4.0234 | -0.5149 | 0.3216 | fail | 0.6509 | 0.7681 | 0.4563 | fail | 0.0889 | 0.1160 |
| 6 | 3.7216 | 0.7562 | 0.3413 | fail | 0.5409 | 0.0642 | 0.4531 | fail | 0.1049 | 0.0799 |

## Interpretation boundary

A polar pass would mainly validate that the inserted persistent carrier
survives its own sign-randomized control; persistence is a model input.
A circulation pass would make the antisymmetric full-memory moment an
eligible observable for a later interaction test. In d dimensions it
is a bivector; calling it spin, especially quantized or half-integer
spin, would be unsupported.

The state contains no rotationally invariant signed scalar or internal
species index. Charge and flavor are therefore undefined in this model,
not merely unmeasured. A later extension would need an explicit source
law, conservation/flux test, or internal representation.

The oriented source is passive: vector memory does not feed back on its
own trajectory in this gate. No self-consistent vector-knot mechanism
has yet been established.

## Figure

![Source eligibility](../../figures/draft/response/oriented_memory_source_eligibility_gate_2026-08-07.png)

## Reproducibility

- Analysis revision: a82e66bc0e69e161bd8673b7f59f0b716f11b382
- Worktree at start: clean
- Command: python experiments/current/memory/synchronization/one_way/oriented_memory_source_eligibility_gate.py
- Seed 1: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed1_steps3000000.json, SHA-256 10c8650d40d1fff01c2bc7aa6d4661f271acff35fe9395dfc101e6448d746614
- Seed 2: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed2_steps3000000.json, SHA-256 41e5def5bee92feebd204ac89ab2566ac2960af0d6933f09129251f12e361188
- Seed 3: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed3_steps3000000.json, SHA-256 882721c56e67ed90e3c937d54223c1bdb6e4dcb970877edf3a267e9ab9919816
- Seed 4: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed4_steps3000000.json, SHA-256 7e7b0949b45e14413ee6901fe5e3a9a657e4a30e2b1401679d3f7e1e08b9bc6e
- Seed 5: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/case_baseline_seed5_steps3000000.json, SHA-256 a3f41aebf2673c3cbffc38d163f0e448d505565605a730f41bddf269382730f1
- Seed 6: data/processed/long_run_metastability/raw_memory_snapshot_retest_Aatt35_N3M_d3_seed6_2026-07-22/case_baseline_seed6_steps3000000.json, SHA-256 ecdec2a7324bba2b2047c224b15e6ec80414b29503c927b9a94f7da73b408217
