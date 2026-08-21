# Critical review: scalar-memory rotating-wave interval certificate

Date: 2026-08-21.

Verdict: **the registered Krawczyk gate certifies existence and uniqueness of
one exact zero of the two finite-\(H\) rotating-wave balance equations in the
registered neighborhood.** This upgrades the previous floating-point
existence witness within the stated mathematical model. It does not upgrade
the separate numerical stability result to a spectral theorem.

## 1. Prospective integrity

The exact function, analytic Jacobian, dependency version, precision panels,
Newton count, outer and inner boxes, consistency checks and decision rule
were committed and pushed at clean revision
8ce6c00713cbac24ebaec337bd339f1944dbcc35 before either candidate box was
evaluated. The execution began from that clean revision.

The fixed panels were 80 and 120 decimal digits. Both used eight analytic
Newton iterations, an outer half-width \(10^{-10}\) around the published
decimal candidate and an inner half-width \(10^{-40}\) around the resulting
panel center. No width, precision, iteration count or native parameter was
changed after seeing the result.

## 2. Certified statement

Both outer and inner boxes satisfy

\[
K(X)\subset\operatorname{int}X
\]

for the two-dimensional Krawczyk operator. The interval representation of
the point inverse is nonsingular, both components of \(F(X)\) contain zero,
and the registered physical signs and gain are enclosed:

\[
A_H(X)>0,\qquad S_H(X)<0,\qquad
0.15\in\eta_R(X)\cap\eta_T(X).
\]

The intersection of the two inner Krawczyk images is displayed as

\[
R\in[
0.946517504804223960990626662735384935160072399313332184824852189820406142783002142586023842,
\]

\[
0.946517504804223960990626662735384935160072399313332184824852189820406142784193122682623404],
\]

with width \(1.19\,10^{-75}\), and

\[
\theta\in[
0.0157703817171349919012689641413413231316321140980062507765923663663284306507079108072871631,
\]

\[
0.0157703817171349919012689641413413231316321140980062507765923663663284306507540453408303073],
\]

with width \(4.61\,10^{-77}\). These long decimal strings are readability
renderings. The machine summary retains each exact binary endpoint tuple,
which is the authoritative certificate record.

The 80- and 120-digit refined centers differ by only
\(3.86\,10^{-69}\) in radius and \(4.31\,10^{-70}\) in angle. Their point
residual maxima are \(3.29\,10^{-83}\) and \(6.05\,10^{-123}\).

## 3. Independent controls and remaining trust base

Before execution, unrelated tests established:

- equality of the multiprecision balance and the native finite-\(H\)
  residual convention;
- analytic-Jacobian agreement with a centered finite difference at \(H=17\);
- enclosure of independent point function and Jacobian values;
- correct Krawczyk inclusion for a known two-dimensional polynomial root.

The two precision panels are convergence controls, not independent software
implementations. The certificate still trusts `mpmath.iv` version 1.3.0 and
the correctness of its directed-rounding elementary functions. Exact binary
endpoint serialization prevents decimal formatting from becoming part of
the proof, but it does not formally verify the interval library itself.

## 4. What is now stronger

The phrase "floating-point-exact root" can now be replaced by the narrower
and stronger statement:

> For the exact decimal parameters
> \(\alpha=0.01,H=1200,M_0=1,\eta=0.15,\sigma_{\rm rep}=1,
> \sigma_{\rm att}=3,A_{\rm rep}=1,A_{\rm att}=3.5\), the two analytic
> finite-memory rotating-wave balance equations possess exactly one zero in
> the registered outer box, with the tighter enclosed coordinates reported
> above.

This is an existence-and-local-uniqueness theorem for the reduced exact
balance. Because the rotating history is substituted algebraically into the
native update, that zero defines an exact rotating relative equilibrium of
the deterministic finite-history model.

## 5. What remains numerical or open

1. The prior ARPACK panels do not enclose all 2400 co-rotating multipliers.
   Local source stability remains strong numerical evidence, not an interval
   spectral proof.
2. Uniqueness is only within the registered neighborhood. Other roots
   elsewhere in \((R,\theta)\) are neither excluded nor counted.
3. The theorem fixes \(H=1200\), \(\alpha=0.01\), \(\eta=0.15\) and the kernel
   amplitudes. It says nothing yet about a continuum family or structural
   robustness.
4. No generic initial history has formed the circle, and no noise has been
   applied.
5. The continuous \(S^1\) remains the ambient spatial rotation group orbit;
   after \(SO(2)\) reduction it is a point.
6. The balance contains no work ledger and establishes no inertia or mass.

## 6. Sequential consequence

The registered certificate authorizes the design of one matched refinement
ladder with \(H\alpha=12\), \(\eta/\alpha=15\), fixed kernel parameters and no
amplitude retuning. That ladder must distinguish continuation of certified
roots from mere small residuals and must freeze its cells, root transfer rule
and failure semantics before execution. Formation, noise, the
\(A_{\rm att}=7\) holdout and mechanics remain sealed.
