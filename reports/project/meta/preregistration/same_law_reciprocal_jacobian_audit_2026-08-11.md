# Preregistration: same-law reciprocal Jacobian audit

Date: 2026-08-11.

## Question

Can the canonical scalar self/readout law, used unchanged as a reciprocal
cross law, place a mature two-knot state in a stable complex relative-mode
regime without fitting a trajectory frequency or introducing a new field?

## Fixed state and notation

For each available checksum-validated mature checkpoint, define

\[
Y_-=(x_-,\bar x_-^\rho),
\qquad
G=\eta\nabla^2\Phi_{\rm self}(x),
\qquad
C(R)=\eta\nabla^2\Phi_{\rm cross}(x+R\hat u).
\]

The same kernel, deposition convention and coupling gain are used for self and
cross readout. No cross normalization or frequency fit is permitted. The full
matrix operator is

\[
A_-=
\begin{pmatrix}
I-G-C & G-C\\
\lambda(I-G-C) & (1-\lambda)I+\lambda(G-C)
\end{pmatrix}.
\]

The scalar symbols \(g,c\) are only directional Rayleigh quotients of \(G,C\).

## Fixed geometry

For every eigenvector of the symmetric self-gain matrix \(G\), place an
identical source clone along that direction at exactly:

1. \(2.5R_{\rm mem}\), matching the previous reciprocal pilot;
2. \(10R_{\rm mem}\), a separated near-field control;
3. \(0.1\sigma_{\rm rep}\);
4. \(1.0\sigma_{\rm rep}\);
5. \(1.0\sigma_{\rm att}\).

The target retains the same internal visible-point offset from its memory
centroid. This makes the zero-separation limit exactly comparable to the self
Hessian without evaluating an unphysical coincident pair as a primary row.

## Primary diagnostics

For every checkpoint, distance and direction, record:

- directional \(g=\hat u^T G\hat u\) and \(c=\hat u^T C\hat u\);
- \(c/g\) where defined;
- the largest eigenvalue of \(C-G\), testing whether any direction has
  cross-return larger than self-return;
- all eigenvalues of the full \(2d\times2d\) operator;
- spectral radius, maximum imaginary part and stable-complex classification.

## Decision rule

- **same-law eligible:** at least one preregistered geometry has a stable
  complex full-matrix mode and positive cross-over-self excess, with no fitted
  gain.
- **same-law negative:** every geometry has \(C\preceq G\) within numerical
  tolerance and no stable complex full-matrix mode. A common rescaling of
  self and cross gain is then not an admissible route to the scalar complex
  branch.
- **inconclusive:** mixed matrix ordering, unstable/noncommuting modes or
  insufficient state coverage prevents either conclusion.

The repository currently contains one mature formation checkpoint in each of
\(d=3\) and \(d=10\). Therefore any result is a structural case study, not a
seed-robust physical claim. A positive result would authorize a five-formation-
seed \(N=500\,000\) pilot. A negative result would require a separately stated
cross-enhancement, self-screening, channel-geometry or retardation mechanism.

## Controls

- analytic Hessians must match central finite differences of the existing
  gradient implementation;
- isotropic matrix gains must reproduce the existing scalar reciprocal poles;
- rotating \(G,C\) together must preserve the full spectrum;
- generated reports must state that a stable complex pole is a damped local
  mode, not a persistent orbit, quantum state or dimension-selection result.
