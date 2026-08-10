# Eta-Zero Raw-Mode Null Audit

Date: 2026-07-31T22:29:18.439582+00:00.

## Question

Are the archived complex AR pairs eigenmodes of scalar eta-zero memory,
or are they introduced by moving-center features and finite fitting?

## Exact result

For p_k=exp(-i k x_n), Gaussian eta-zero increments give a real phase
multiplier exp(-epsilon^2 k^2/2). Forgetting and heat give the second
real multiplier (1-lambda)exp(-nu k^2). Both are repeated for real and
imaginary components. Sampling raises the real map to a power and cannot
create a complex eigenpair.

## Gate

- Exact raw operator has complex modes: False.
- Pooled raw fits have complex rows: False.
- Seedwise raw fits have complex rows: False.
- Archived active/eta-zero separation: False.
- Archived complex segment identity: False.
- Physical complex mode supported: False.
- P2 classification complete: True.

![Eta-zero raw-mode null audit](../../figures/draft/memory/eta_zero_raw_mode_null_audit_2026-07-31.png)

## Finite-fit summary

| scope | rows | complex | fraction | max frequency | median error | median condition |
|---|---:|---:|---:|---:|---:|---:|
| pooled | 15 | 0 | 0 | 0 | 0.00548 | 4.9e+04 |
| seed | 75 | 0 | 0 | 0 | 0.00917 | 1.44e+05 |
| segment | 375 | 27 | 0.072 | 0.000725 | 0.0225 | 9.62e+04 |

## Interpretation

The raw operator is analytically real. Full traces test this result at the
same N=1M cadence as the archived closure run. Segment-only leakage is
reported because tiny epsilon excites a narrow phase arc and yields
ill-conditioned fits. The archived larger pairs occur after moving-center
alignment and force/relative-position projection; active and eta-zero
subspaces overlap above 0.9999. They remain representation/fit modes, not
physical oscillations.

The long-run work remains a separate evidence lane. N=30M/300M runs,
parameter heatmaps, and D_occ-near-three locations are observations about
asymptotic geometry. They do not establish mode identity. New long runs
must freeze code revision, cadence, fit window, and estimator.

## Memory action and observables

- Direct rho observables: mass, centroid, covariance tensor, radius,
  anisotropy, participation dimension, Fourier power/phase, autocorrelation,
  and pathwise contraction.
- Readout observables require rho plus K: Phi, gradient at x, and Hessian.
- Feedback loop: rho -> grad Phi(x) -> x -> deposition -> rho.
  Residence, D_occ, D_cov, drift, angular momentum, and spin proxies depend
  on x and are not intrinsic rho-only observables.
- Original scalar rho has no spatial rho-rho self-coupling beyond optional
  linear smoothing. Active fields require additional spectrum, energy,
  PDE-residual, source-field phase, and saturation observables.

## Limits

- The exact closure is eta-zero, Gaussian, scalar, periodic, and unaligned.
- No photon, spin, quantization, or physical-time claim follows.

## Reproduction

    python experiments/current/memory/closure/eta_zero_raw_mode_null_audit.py

Git revision: 5ee46b105cb0a2ada259e87b9443574daeca23f0.
Git status at generation: M docs/reference/THEORETICAL_CONTEXT.md
 M docs/reference/experiment_catalog.md
 M docs/reference/repository_map.md
 M docs/status/current_status.md
 M docs/status/project_priorities.md
 M reports/README.md
 M src/emergenz_knoten/__init__.py
 M src/emergenz_knoten/markov/__init__.py
 M src/emergenz_knoten/markov/closure.py
 M src/emergenz_knoten/spectral_memory_trace.py
 M tests/test_markov_closure.py
 M tests/test_spectral_memory_trace.py
?? experiments/current/memory/closure/eta_zero_raw_mode_null_audit.py
?? figures/draft/memory/eta_zero_raw_mode_null_audit_2026-07-31.png
?? reports/memory/closure/eta_zero_raw_mode_null_audit_2026-07-31.json
?? reports/memory/closure/eta_zero_raw_mode_null_audit_2026-07-31.md
?? tests/test_eta_zero_raw_mode_null_audit.py.
