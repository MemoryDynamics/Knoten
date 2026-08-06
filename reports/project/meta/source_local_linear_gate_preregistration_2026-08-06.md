# Source-local linear emission gate: preregistration

Date: 2026-08-06.

## Purpose

P3.2 used a local Telegraph transport update, but its source value was the
gradient of the emitting memory evaluated at the current target position. The
transport was local; the emission rule was not. This stoptest asks whether a
strictly source-local emission and target-local readout can support a stable,
observable reciprocal mode before another nonlinear full-knot simulation is
allowed.

This is an architecture test. It cannot identify a physical field, charge,
spin, photon, spatial dimension, or propagation law.

## Fixed local reduction

For one coordinate, define the knot displacement from its scalar memory
centre

```text
d_n = x_n - m_n,
q = 1 - lambda,
a = q (1 - g).
```

Without cross-coupling, `d_(n+1) = a d_n`. The inherited values are
`lambda=0.01` and `g=0.432291`; they are not refitted.

The channel is the already registered finite-grid Telegraph update from P3.2:

```text
p_(n+1) = p_n + dt [c_f^2 Delta u_n - 2 gamma p_n - omega_0^2 u_n]
             + dt B s_n,
u_(n+1) = u_n + dt p_(n+1),
y_n = C u_n.
```

Its grid, boundary conditions, correlation length, relaxation time, time step,
source location, target location, and exact DC normalization remain fixed.
No channel gain or kernel width is searched.

## Emission candidates

All candidates are computed from the emitter only.

1. `mass`: `s_n=M0`. This is the negative dynamic control. Its perturbation is
   zero, so it cannot make an internal linear pole observable.
2. `offset`: `s_n=d_n`. This is the primary translation-invariant source-local
   emission rule.
3. `current`: `s_n=x_n-x_(n-1)=d_n/q-d_(n-1)`. This is a secondary oriented
   source-local rule with one explicit delay state.

The target enters only through the local readout `y_n` at its channel endpoint.
No source term may depend on target position, target memory, pair distance, or
an instantaneous cross-gradient.

## Fixed comparison arms

- `channel_off`: uncoupled scalar-memory relaxation;
- `one_way`: source-local emission and target-local readout without feedback to
  the emitter;
- `reciprocal`: two identical local knots connected by two identical directed
  channels;
- `mass`: constant-emission dynamic negative control.

The inherited dimensionless reciprocal DC coupling is `c=0.02`. Both coupling
signs may be reported as symmetry controls, but neither is tuned.

## Pole and observability definitions

Translation is removed before analysis. For every linear state matrix `A`, a
multiplier `mu` is stable when `|mu|<1`. Its generator in memory-time units is

```text
s = log(mu) / lambda = -Gamma + i omega.
```

A non-real channel pole is not evidence by itself. For a diagonalizable
matrix, let `v_j` and `w_j` be right and reciprocal left eigenvectors. The
residue from an initial knot displacement to the observed knot displacement is

```text
R_j = (e_d^T v_j) (w_j^T e_d).
```

Conjugate-pair residue is normalized by the sum of absolute residues of all
stable poles. This metric is invariant to reciprocal eigenvector rescaling.
Matrices with eigenvector condition number above `1e8` are inconclusive.

## Preregistered pass gate

The primary `offset` candidate passes only if all conditions hold:

1. the reciprocal matrix is stable;
2. it has a conjugate pole pair with `omega >= 0.05` per memory time;
3. the pair carries at least `10%` normalized knot-to-knot residue;
4. the pair generator differs from its nearest one-way channel pole by at
   least `10%`, normalized by the larger generator magnitude;
5. the same conclusion holds for both the exact finite-grid calculation and
   at least two of the three source/readout-informed channel reductions with
   retained orders `{8,16,32}`;
6. the constant-mass control has zero dynamic knot residue.

The `current` candidate is secondary. It can motivate a separate registered
test but cannot rescue failure of the primary offset rule in this gate.

## Decision rule

- **pass:** the primary gate passes; preregister a nonlinear confirmation of
  at least 500,000 updates and at least five independent formation states;
- **fail:** the exact calculation is stable and numerically resolved but no
  primary pole satisfies the gate; do not run the same mechanism longer;
- **inconclusive:** instability, ill-conditioning, or reduction disagreement
  prevents interpretation; repair the formulation without gain searching.

The 500,000-update horizon is a confirmation minimum, not a discovery method.
Earlier project runs indicate that self-entanglement below this horizon is
often not repeatable, but long duration cannot make a nonlocal or unobservable
mechanism valid.
