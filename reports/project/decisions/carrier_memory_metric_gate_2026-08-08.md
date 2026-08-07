# Carrier-memory metric gate

Date: 2026-08-08.

## Decision

The next reciprocal-memory step compares covariance, predictive and kernel
metrics before any nonlinear reciprocal simulation. All three metrics act on
the same reduced feature

\[
h_n=p_n\in\mathbb R^3,
\]

the persistent carrier. This is not the full Markov memory state
\((x_n,\rho_n,p_n,m_n)\). A pass may nominate an effective carrier metric; it
cannot establish a microscopic memory geometry.

## Why prediction uses a probe

In the implemented passive source, oriented memory does not affect its own
visible trajectory. Its self-observability Gramian is therefore exactly zero.
Using a reciprocal self-response here would assume the backchannel that the
metric is meant to constrain.

The predictive metric instead uses the previously fixed one-way response of an
independent probe knot:

\[
G_{\rm pred}(T)
=
\sum_{\tau\le T}w_\tau
J_\tau^\mathsf T J_\tau/R_T^2,
\qquad
J_\tau=
\frac{\partial x^{(T)}_{n+\tau}}{\partial p_n}.
\]

The Jacobian is measured by paired central finite differences with common
source and target noise. A second perturbation amplitude is a linearity control.

## Compared metrics

The covariance metric is

\[
G_{\rm cov}=\operatorname{Cov}(p_n)^+.
\]

It uses a truncated pseudoinverse. Unsupported directions remain null; no ridge
may turn an unobserved direction into a stiff one.

The kernel metric propagates one carrier perturbation through the passive
carrier and vector-memory updates and measures the emitted Gaussian field in
the associated normalized RKHS:

\[
G_{\rm kernel}(T)
=
\sum_{\tau\le T}w_\tau
\lVert\delta m_{n+\tau}\rVert_{\mathcal H_K}^2 I.
\]

It inherits the already fixed Gaussian readout width and is not a kernel-free
result.

For all metrics, exact exponential block masses

\[
w_{[a,b]}=q^a-q^b
\]

make different observation cadences comparable without renormalizing every
finite horizon to unit mass.

## Fixed design

- mature d=3 formation seeds 1 through 6;
- cyclic independent pairs \(1\leftarrow2,\ldots,6\leftarrow1\);
- two non-overlapping segment starts separated by ten memory times;
- horizons 1, 2, 5 and 10 memory times;
- cadences 1, 5 and 10 updates;
- carrier perturbations \(10^{-4}\) and \(5\times10^{-5}\);
- inherited global `vector_eta=5.079e-6`;
- distance `2.5 R_pair` and Gaussian width `2.5 R_source`, fixed from the
  original pair state and not recomputed for the second segment;
- no seedwise gain, metric, cutoff, distance or kernel retuning.

## Gates

Per pair:

1. finite-difference linearity error at most 5%;
2. predictive metric scale drift across cadences at most 20%;
3. predictive pullback shape drift across cadences at most 10%;
4. maximum pullback shape drift across two segments at most 25%;
5. metric-trace drift from five to ten memory times at most 25%;
6. supported pullback-subspace overlap across metrics at least 0.90;
7. reciprocal classifications stable across both segments;
8. covariance, predictive and kernel metrics give the same final reciprocal
   classification signature.

At least five of six pairs must pass. The last criterion is deliberately
strong: agreement only after trace normalization would leave the unresolved
overall metric scale untouched.

## Interpretation rules

A pass authorizes one nonlinear holdout pilot with the selected reduced metric.
It does not prove inertia, oscillation, spin or physical parameter selection.

A fail means that the Euclidean eligibility result is representation- or
normalization-sensitive. No gain sweep follows. The next decision must then be
whether to retain the metric as an explicit effective constitutive choice or to
enlarge the measured memory feature beyond the carrier.

The normalized-direction Jacobian always has one longitudinal null and two
transverse directions in d=3. High subspace overlap can therefore be structural
and is not sufficient evidence for an emergent three-dimensional geometry.
