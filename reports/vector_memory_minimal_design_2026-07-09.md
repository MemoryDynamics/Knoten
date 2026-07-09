# Minimal Vector-Memory Extension

Date: 2026-07-09.

## Motivation

The corrected scalar-memory model can generate compact memory clouds and real
relaxation modes, but the AR mode probe did not find stable slow complex modes.
A scalar gradient potential naturally supports relaxation more directly than
persistent phase dynamics. If the project needs oscillator-, photon-, or
boson-like modes, the next model should add an oriented memory channel rather
than overfit scalar amplitudes.

A cautious working split is:

- scalar memory: particle-like residence, relaxation, compactness;
- vector/phase memory: candidate route to bosonic or electromagnetic-style
  phase, polarization, and propagation;
- tensor memory: later extension for anisotropic internal structure if vector
  memory is insufficient.

This is a model-design hypothesis, not a physics claim.

## Minimal State

Keep the scalar memory density and add an oriented memory field:

```text
rho[n+1] = (1-lambda_s) rho[n] + lambda_s M_s G_s(.-x[n+1])
p[n+1]   = (1-lambda_v) p[n]   + lambda_v M_v u[n+1] G_v(.-x[n+1])
```

where `p` is vector-valued and `u[n+1]` is an orientation attached to the update.
Possible first choices:

```text
u[n+1] = normalize(x[n+1]-x[n])
```

or an explicit internal phase/orientation variable transported by the update.

The visible update should separate scalar-gradient and oriented channels:

```text
x[n+1] = x[n] + epsilon xi[n]
         - eta_s grad(K_s*rho[n])(x[n])
         + eta_v F_v[p[n]](x[n]).
```

The key requirement is that `F_v` can contribute an antisymmetric or phase-lagged
part to the local linearization. Without such a term, the reduced dynamics is
likely to remain relaxation-dominated.

## Local Mode Requirement

A slow complex mode requires an effective local block of the form

```text
Y[n+1] ~= A Y[n],
A = R + Omega,
Omega^T = -Omega,
```

or equivalently a two-dimensional subblock

```text
[a  -omega]
[omega  a]
```

with eigenvalues `a +/- i omega`. The scalar gradient channel mostly supplies
symmetric restoring/repulsive parts. The vector memory must supply the oriented
or antisymmetric contribution.

## First Implementation Target

Start with the smallest nontrivial extension:

1. Add a vector memory summary to the augmented state, not a full grid field.
2. Store `p` as a finite history of oriented deposits, analogous to the scalar
   finite-memory representation.
3. Add a switchable vector force contribution with `eta_v=0` reducing exactly
   to the scalar model.
4. Keep the corrected scalar kernel parameters fixed near the measured boundary:
   `A_rep=1`, `sigma_rep=1`, `sigma_att=3`, `A_att in [7.75,9.0]` for transition
   tests and `A_att in [9,35]` for compactness tests.
5. Fit the same AR mode probe and require complex slow modes to be stable across
   lags before using photon or wave language.

## Required Controls

- `eta_v=0`: exact scalar baseline.
- shuffled vector memory: destroys orientation while preserving scalar memory.
- zero vector mass `M_v=0`: no oriented channel.
- `lambda_v=1`: one-step vector memory, expected to lose persistent phase.
- sign-flipped or rotated vector channel: tests whether the complex mode is
  tied to orientation rather than scalar compactness.

## Success Criteria

A useful vector-memory pilot should show at least one of:

- a slow complex conjugate pair stable across lags;
- a reproducible phase/frequency estimate after coarse graining;
- polarization-like orientation persistence not present in scalar controls;
- improved closedness of a reduced Markov/AR state when vector features are
  included.

Without those signatures, vector memory may still be useful for internal
structure, but it should not be sold as photon-like.
