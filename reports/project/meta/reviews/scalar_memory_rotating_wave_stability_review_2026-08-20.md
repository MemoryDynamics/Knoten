# Critical review: scalar-memory rotating-wave source stability

Date: 2026-08-20.

Verdict: **the preregistered full-FIFO gate supports local transverse
numerical stability of one prepared, noiseless spatial rotating relative
equilibrium.** It does not yet supply a complete spectral proof, formation
from generic histories, an internal phase after spatial-symmetry reduction,
or an inertial/work claim.

## 1. Prospective integrity

The candidate, complete \(2H\)-state, quotient metric, two Arnoldi panels,
perturbation directions, amplitudes, duration and decision thresholds were
committed at clean revision
0d9fe68c4a3bddf0e1869a20f9aa9ff2989aaa6c before execution. The run began
from that clean revision after a zero-defect P0 audit and a frozen D0
contract. Noise, data-driven topology and the \(A_{\rm att}=7.0\) holdout
remained sealed.

After the result, an additional unit test compared the stability module's
native FIFO step with the pre-existing production
`double_gaussian_gradient`, production memory weights and explicit FIFO
shift on an unrelated random \(29\times2\) state. The paths agree to absolute
and relative tolerance \(2\,10^{-15}\). This post-result implementation
cross-check does not alter the registered decision, but reduces the risk that
the discovery and stability code shared a private kernel convention.

## 2. Object and terminology

For \(H=1200\), the co-rotating map

\[
\mathcal G_\theta(Y)=\mathcal R(-\theta)\mathcal F(Y)
\]

acts on \(Y\in\mathbb R^{2400}\). The prepared history is fixed by this map
to maximum component error \(2.46\,10^{-15}\).

The inferred rotation period is \(2\pi/\theta=398.4168\) updates, not an
integer number of updates. Consequently the reported eigenvalues are most
precisely called **one-step co-rotating multipliers**. They play the role of
Floquet multipliers for a relative equilibrium, but they are not monodromy
multipliers of a demonstrated finite-period discrete orbit.

The continuous set

\[
\{\mathcal R_\varphi Y_\ast:\varphi\in S^1\}
\]

is an \(S^1\) because of ambient \(SO(2)\) symmetry. In the \(SO(2)\)
quotient it is one point. The calculation therefore establishes no
additional internal phase coordinate.

## 3. Linear evidence

The analytic sparse Jacobian has shape \(2400\times2400\) and 9596 stored
entries. Before the candidate run, it was checked against a centered
finite-difference directional derivative on an unrelated \(H=17\) state.
At the candidate it reproduces the three analytic symmetry directions:

- global rotation: relative residual \(8.58\,10^{-16}\);
- common \(x\)-translation: \(2.56\,10^{-17}\);
- common \(y\)-translation: \(3.53\,10^{-17}\).

Both frozen Arnoldi panels return the same leading transverse conjugate pair,

\[
\lambda_\perp
=0.992858455252-0.020023536920i,
\qquad
|\lambda_\perp|=0.993060347711.
\]

The primary and convergence estimates differ by \(3.07\,10^{-13}\) in the
complex plane and \(2.92\,10^{-13}\) in modulus. Their normalized residuals
are \(2.94\,10^{-13}\) and \(4.96\,10^{-13}\). The numerical unit-circle
margin is \(6.94\,10^{-3}\) per update. In memory time \(t=\alpha n\), the
corresponding decay rate is

\[
-\frac{\log|\lambda_\perp|}{\alpha}=0.69638,
\]

or an e-folding time of \(1.436\) memory times.

This complex transverse pair describes damped perturbation ringing. It is
not evidence for a second internal phase. Its overlaps with the analytic
translation and rotation spaces are \(0.237\) and \(0.063\), safely below the
registered \(0.99\) symmetry label, but they also show that individual
eigenvectors need not be cleanly orthogonal physical modes in this
non-normal delayed state representation.

## 4. Nonlinear return evidence

All three nonzero registered perturbations return to the numerical floor in
5000 updates, equal to 50 memory times or \(12.55\) rotations:

| perturbation | initial quotient distance | final/initial |
| --- | ---: | ---: |
| visible radial | \(8.67\,10^{-8}\) | \(3.17\,10^{-8}\) |
| visible tangential | \(7.52\,10^{-8}\) | \(3.34\,10^{-8}\) |
| full-history transverse | \(4.14\,10^{-9}\) | \(6.03\,10^{-7}\) |

The exact control remains below \(5.63\,10^{-15}\) in absolute quotient
distance. Its tabulated growth factor near 1994 is not a physical growth
diagnostic: the denominator is only \(2.82\,10^{-18}\), below the accumulated
floating-point floor. The registered exact-control decision correctly uses
the absolute \(10^{-10}\) bound instead.

The perturbation amplitude is only \(10^{-7}R\), and the generic
full-history panel contains one deterministic direction. This establishes a
local basin at the tested scale, not its radius, prevalence or accessibility
from an unprepared memory history.

## 5. What can still falsify the interpretation

1. ARPACK returned the leading 24 and 36 largest-modulus Ritz pairs, not a
   rigorous enclosure of all 2400 eigenvalues. A publication-grade theorem
   still needs interval bounds, a certified characteristic-root argument or
   another complete spectral enclosure.
2. The same continuum geometry does not balance at the nonselecting shorter
   tail extent \(C=6\). The result is therefore not horizon-independent.
3. The historical noisy \(d=3,A_{\rm att}=3.5\) branch dispersed. It is not
   the same \(d=2\), delta-deposition, prepared-history experiment, but it is
   adverse evidence against generic formation and stochastic robustness.
4. No random or compact noncircular history has formed this orbit. Local
   return must not be relabelled spontaneous formation.
5. Writing and forgetting remain an open source/sink process. Neither the
   rotating-wave balance nor its stability supplies a work ledger or a mass.

## 6. Sequential consequence

The strongest current claim is therefore:

> At the frozen native parameter point, the deterministic finite-\(H\) map
> has a floating-point-exact spatial rotating relative equilibrium that is
> locally transversely attracting in the registered spectral and nonlinear
> panels.

The next discriminating step should be a newly frozen robustness ladder, in
this order: certified or multiprecision existence; matched
\((\alpha,H,\eta)\) continuum refinement without amplitude retuning;
deterministic basin/formation tests; only then noise. Data-driven \(S^1\)
analysis is not informative for an internal phase unless a candidate
observable survives the ambient \(SO(2)\) quotient. The center work/mass
branch remains logically separate.
