# Prospective matched-refinement ladder: scalar-memory rotating wave

Date: 2026-08-21.

Status: prospective deterministic continuation protocol. It is frozen after
the unique-root interval certificate and before evaluating any non-anchor
ladder cell.

## 1. Question and claim boundary

The gate asks whether the certified finite-\(H\) rotating relative
equilibrium belongs to a discretization-consistent family when the native
small-step scaling is refined without retuning the kernel:

\[
H\alpha=12,
\qquad
\frac{\eta}{\alpha}=15.
\]

A pass supports a matched discrete root family approaching the already
registered continuum guide. Five cells cannot prove convergence for every
\(\alpha\to0\). The gate does not test stability of the non-anchor roots,
formation, noise, topology, work or mass.

## 2. Frozen model and cells

Every cell uses

\[
d=2,\quad\varepsilon=0,\quad M_0=1,\quad
\sigma_{\rm rep}=1,\quad\sigma_{\rm att}=3,\quad
A_{\rm rep}=1,\quad A_{\rm att}=3.5,
\]

with delta deposition and the exact finite-age sum. No amplitude, width,
tail extent or deposition rule may be adjusted.

| cell | \(\alpha\) | \(H\) | \(\eta\) | role |
| --- | ---: | ---: | ---: | --- |
| L0 | 0.04 | 300 | 0.60 | coarse stress cell |
| L1 | 0.02 | 600 | 0.30 | scaling cell |
| L2 | 0.01 | 1200 | 0.15 | certified anchor |
| L3 | 0.005 | 2400 | 0.075 | refinement cell |
| L4 | 0.0025 | 4800 | 0.0375 | finest registered cell |

The \(A_{\rm att}=7.0\) discovery holdout remains sealed.

## 3. Frozen transfer rule

The common initial geometry is taken from the certified anchor:

\[
R_{\rm start}
=0.946517504804223960990626662735384935160072399313332184824852,
\]

\[
\Omega_{\rm start}
=1.577038171713499190126896414134132313163211409800625077659236.
\]

For every cell independently, initialize

\[
(R,\theta)
=(R_{\rm start},\alpha\Omega_{\rm start})
\]

and perform exactly eight analytic Newton iterations. Cells are not seeded
from the result of a neighboring cell; this prevents an execution-order
choice from becoming a hidden branch selector.

All Newton iterates must stay in the predeclared branch corridor

\[
|R-R_{\rm start}|<0.15,
\qquad
|\theta/\alpha-\Omega_{\rm start}|<0.15.
\]

Leaving this corridor is a cell failure, even if Newton later returns.

## 4. Cellwise interval certificates

Each cell is evaluated at 80 and 120 decimal digits. After the fixed Newton
iterations, certify two boxes centered on the panel result:

\[
X_{\rm outer}:
\quad |\Delta R|\le10^{-6},
\quad |\Delta\theta|\le\alpha10^{-6},
\]

\[
X_{\rm inner}:
\quad |\Delta R|\le10^{-35},
\quad |\Delta\theta|\le\alpha10^{-35}.
\]

Both boxes must pass every existing Krawczyk, physical-domain, sign and
required-gain control. The two panel centers must agree within \(10^{-55}\)
in both \(R\) and \(\Omega=\theta/\alpha\). Each point residual must be at
most \(10^{-(p-20)}\) at precision \(p\). Inner Krawczyk-image widths must
be below \(10^{-33}\) in \(R\) and \(\alpha10^{-33}\) in \(\theta\).

The L2 anchor enclosure must overlap the previously committed unique-root
certificate. No failed cell may be repaired by changing its start, box,
precision or iteration count.

## 5. Frozen continuum guide and scaling observables

The continuum guide was recorded before this ladder by the original
prospective discovery at tail extent \(C=12\):

\[
R_\infty^{\rm guide}=0.9430108292781663,
\qquad
\Omega_\infty^{\rm guide}=1.5868166272376472.
\]

It is a high-order quadrature/root result, not an interval theorem. For
\(y\in\{R,\Omega\}\), define

\[
e_y(\alpha)=|y(\alpha)-y_\infty^{\rm guide}|.
\]

The frozen scaling gates are:

1. both \(e_R\) and \(e_\Omega\) decrease strictly at every successive
   halving from L0 through L4;
2. a least-squares log-log slope on L1--L4 lies in \([0.8,1.2]\) for both
   observables;
3. the L4 error is at most \(0.35\) times the L2 anchor error for both;
4. the last-pair first-order Richardson estimate

   \[
   y_{\rm Rich}=2y(0.0025)-y(0.005)
   \]

   differs from the continuum guide by at most \(0.1e_y(0.0025)\).

The coarse L0 cell contributes to monotonicity but not to the slope fit.

## 6. Decisions

Decision is **matched-refinement-pass** only if every cell certificate,
cross-precision control, corridor control, anchor-overlap control and every
scaling gate passes.

Decision is **certified-roots-nonconvergent** if all five cells possess
certified roots on the registered branch corridor but at least one scaling
gate fails. This is negative evidence for the proposed matched continuum
interpretation, not for existence at the anchor.

Any missing cell certificate, arithmetic exception or failed anchor overlap
is **matched-refinement-inconclusive**.

## 7. Sequential consequence

A pass establishes a certified five-cell root ladder with numerical
first-order approach to the pre-existing continuum guide. It may motivate a
separate preregistered stability-robustness ladder. It does not open noise,
formation, internal-\(S^1\), the amplitude holdout or mechanics automatically.
