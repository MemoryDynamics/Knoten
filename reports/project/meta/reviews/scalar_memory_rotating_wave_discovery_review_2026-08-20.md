# Critical review: scalar-memory rotating-wave discovery

Date: 2026-08-20.

Verdict: **the preregistered deterministic discovery found one
floating-point-exact rotating history of the native K0-H map.** This is a
nontrivial existence witness at numerical precision. It is not yet a
stability result, a formation result, an internal-phase result or a mass
result.

## 1. Prospective status

The analytic equations, amplitude panel, radius/frequency grids, quadrature
orders, selection rule, finite-\(H\) target and untouched holdout were
committed at clean revision
\(ed98a8872fec3478f3c0c996dec22fd88e1c1bb9\) before execution.

The discovery opened no random seed, trajectory, topology statistic or
\(A_{\rm att}=7.0\) holdout. It evaluated only deterministic balance
integrals and the native one-update residual.

## 2. Analytic mechanism check

For a positive rotation angle, the exact history must satisfy

\[
A_H>0,\qquad S_H<0,
\]

where \(A_H\) is the radial binding sum and \(S_H\) the tangential history
sum. The compact reference \(A_{\rm att}=35\) has
\(\phi(r)>0\) at every radius and supplies no recent-trail propulsion.

All three controls behaved accordingly:

- \(A_{\rm att}=0\): no radial root because the force is outward everywhere;
- \(A_{\rm att}=9\): no radial continuum root at the force-sign boundary;
- \(A_{\rm att}=35\): no radial continuum root in the purely attractive
  reference.

Every registered sign-changing amplitude \(3.5\) through \(8.5\) produced
admissible continuum roots. Thus the positive result is not an isolated
grid accident; the selection of one row was instead controlled by proximity
to the pre-existing native scaling \(\eta/\alpha=15\).

## 3. Selected finite-H solution

The first registered finite refinement converged in four function evaluations
without changing any native parameter:

\[
\alpha=0.01,\quad H=1200,\quad\eta=0.15,\quad
A_{\rm att}=3.5,
\]

\[
R=0.946517504804225,
\qquad
\Omega=1.5770381717135,
\qquad
\theta=0.015770381717135.
\]

The two independently inferred gains are

\[
\eta_R=0.149999999999945,
\qquad
\eta_T=0.15.
\]

The registered residual norm is \(4.53\,10^{-17}\). A separate direct call
to the production double-Gaussian gradient on the explicitly constructed
1200-point circular history gives a one-step state residual

\[
\lVert x_{n+1}-\mathcal R(\theta)x_n\rVert
=7.98\,10^{-17}.
\]

This independent path verifies that the compact analytic sum uses the same
sign, weight, age and kernel conventions as the native implementation.

The period is \(398.4168\) updates or \(3.98417\) memory times. The retained
history covers \(3.01192\) turns. The force crossing is
\(r_\ast=1.45775\), while the orbit diameter is \(2R=1.89304\), so the
history genuinely samples both the recent repulsive and outer attractive
force sectors.

## 4. Important negative evidence

At the nonselecting shorter extent \(C=6\), the same geometry has radial
integral \(8.65\,10^{-4}\), not zero. Its tangentially inferred gain remains
near the reference value, \(\widehat\eta=14.9735\), but the radial mismatch
means the \(C=12\) solution cannot simply be called horizon-independent.
A new circle could be re-solved at \(C=6\), but doing so would be a different
parameter cell.

The historical noisy \(d=3\), \(A_{\rm att}=3.5\) branch was dispersive. That
does not algebraically contradict this prepared noiseless \(d=2\) solution,
but it is a strong prior warning that the exact circle may be transversely
unstable or possess a negligible basin.

The discovery inventory contains hundreds of continuum roots. This is
expected for a one-equation continuum geometry family and is not evidence for
hundreds of physical phases. Fixing \(\eta/\alpha=15\) and then requiring both
finite-\(H\) residual components selected the reported point.

## 5. What has and has not been shown

Evidence:

- the analytic sign-changing-force mechanism is internally consistent;
- the native finite-memory update has one self-consistent rotating history to
  approximately machine precision;
- the result is reproduced by the production kernel path.

Not established:

- an interval-certified mathematical root;
- transverse spectral stability;
- return after perturbation;
- formation from a non-orbit initial history;
- robustness to noise, horizon or parameter change;
- topology after quotienting translation and ambient rotation;
- an internal rather than symmetry-generated phase;
- a physical energy source, work port or mass.

The only authorized next action is to freeze this discovery and initial-state
specification in a new P0-S manifest. Candidate-targeted Jacobian, trajectory
or topology work remains sealed until that provenance gate passes.
