# Critical foundation audit: native scalar-memory rotating waves

Generated: 2026-08-21T16:10:00.003655+00:00.

Decision: **foundation-audit-reconciliation-pass-scoped**.

The audit ran from clean prospective revision
`8e1cf13083d343cdebb0d7d315d34a017164c827`.

## Composite gates

| gate | result |
| --- | --- |
| A_provenance_parameter_closure | pass |
| B_independent_finite_sum_replay | pass |
| C_certificate_and_stability_semantics | pass |
| D_independent_continuum_replay | pass |
| E_scaling_replay | pass |

All nine immutable input hashes match, and every recorded
execution revision exists in the ancestry of this audit.

## Independent finite-sum replay

| cell | alpha | H | eta | max residual | max gain error | result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| L0 | 0.04 | 300 | 0.6 | 6.22577937e-72 | 1.05045877e-69 | pass |
| L1 | 0.02 | 600 | 0.3 | 1.69793983e-72 | 4.30144756e-70 | pass |
| L2 | 0.01 | 1200 | 0.15 | 3.9618596e-72 | 1.96055452e-69 | pass |
| L3 | 0.005 | 2400 | 0.075 | 2.9713947e-72 | 5.57490243e-69 | pass |
| L4 | 0.0025 | 4800 | 0.0375 | 7.76702455e-73 | 3.71735626e-69 | pass |

This replay uses a separate multiprecision sum and imports no
project rotating-wave evaluator. It checks signs, ages, weights,
both residual components and both inferred gains; it is not a
second interval proof.

## Independent continuum replay

| panel | method | R | Omega | max residual | target dR | target dOmega | result |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| mp-ts-70 | tanh-sinh | 0.943113307 | 1.58557008 | 1.81113582e-71 | 3.21621185e-15 | 1.49652227e-14 | pass |
| mp-gl-70 | gauss-legendre | 0.943113307 | 1.58557008 | 1.81113582e-71 | 3.21621185e-15 | 1.49652227e-14 | pass |

The two multiprecision quadratures agree to
dR=0 and dOmega=0.
They are independent numerical controls, not continuum interval
enclosures.

## Scaling replay

Radius slope: `1.00944376`; Omega slope: `1.01102362`.

Fine/anchor error ratios: R=`0.247894389`, Omega=`0.247530525`.

Richardson relative errors: R=`0.00561897699`, Omega=`0.00661529059`.


## Reviewer verdict

The evidence chain is suitable as a **scoped mathematical and
numerical foundation for prepared spatial loops**. Exact local
finite-H existence is certified in five cells, and the fixed-gain
continuum/scaling result survives a separate multiprecision
implementation.

The word *stable* remains narrower: only the anchor has strong
local numerical spectral and perturbative evidence, without a
complete spectral enclosure. No generic history has formed a
loop. D0 identifies the circle as an ambient SO(2) group orbit
that becomes a point in the symmetry quotient, not an internal
S1. No work, inertia or mass claim follows.

The next refinement cell remains sealed and was not evaluated by
this audit.
