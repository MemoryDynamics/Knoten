# Prospective fixed-gain continuum reconciliation: scalar-memory rotating wave

Date: 2026-08-21.

Status: prospective deterministic reconciliation protocol. It is frozen after
the matched-refinement ladder returned **certified-roots-nonconvergent** and
before solving the corrected continuum system.

## 1. Question and historical boundary

The five-cell ladder fixed

$$
H\alpha=12,
\qquad
\eta/\alpha=15,
$$

but its preregistered continuum guide was a discovery-grid point whose own
stored gain is $15.016345187237246$. This protocol asks a narrow falsifiable
question: does the already frozen ladder satisfy its original scaling gates
when compared with the continuum root defined at exactly the same gain
$\widehat\eta=15$?

The historical decision **certified-roots-nonconvergent** is immutable. A
successful reconciliation identifies a target-definition error and supplies
a corrected numerical comparison; it does not retroactively turn the earlier
run into a pass.

## 2. Frozen native continuum equations

No model parameter is retuned. Fix

$$
C=12,
\quad \widehat\eta=15,
\quad M_0=1,
\quad \sigma_{\rm rep}=1,
\quad \sigma_{\rm att}=3,
\quad A_{\rm rep}=1,
\quad A_{\rm att}=3.5.
$$

For $t\in[0,C]$, define

$$
u(t)=1-\cos(\Omega t),
\qquad
q(t)=R^2u(t),
$$

so the squared circular chord is $r(t)^2=2q(t)$. The native gradient factor
can then be evaluated without an absolute value or square root:

$$
\phi(q)
=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
  e^{-q/\sigma_{\rm rep}^2}
 +\frac{A_{\rm att}}{\sigma_{\rm att}^2}
  e^{-q/\sigma_{\rm att}^2}.
$$

The two history integrals are

$$
I_R(R,\Omega)
=M_0\int_0^C e^{-t}\phi(q(t))u(t)\,dt,
$$

$$
I_T(R,\Omega)
=M_0\int_0^C e^{-t}\phi(q(t))\sin(\Omega t)\,dt.
$$

The corrected fixed-gain system is

$$
F_R(R,\Omega)=I_R(R,\Omega)=0,
$$

$$
F_T(R,\Omega)
=\Omega+\widehat\eta I_T(R,\Omega)=0.
$$

These are the leading small-step limits of the two components of the native
finite-memory update. They contain no postulated mass, momentum, centripetal
force or harmonic-oscillator equation.

## 3. Frozen analytic Jacobian

Let

$$
\phi_q
=\frac{A_{\rm rep}}{\sigma_{\rm rep}^4}e^{-q/\sigma_{\rm rep}^2}
 -\frac{A_{\rm att}}{\sigma_{\rm att}^4}e^{-q/\sigma_{\rm att}^2}.
$$

Then

$$
q_R=2Ru,
\qquad
q_\Omega=R^2t\sin(\Omega t),
$$

and the code evaluates the four derivatives by differentiating the displayed
integrands under the integral sign. The Newton Jacobian is

$$
J=
\begin{pmatrix}
\partial_R I_R & \partial_\Omega I_R\\
\widehat\eta\,\partial_R I_T &
1+\widehat\eta\,\partial_\Omega I_T
\end{pmatrix}.
$$

Before execution, unit tests must compare this analytic Jacobian with a
centered finite difference at a non-target point and cross-check the balance
against the pre-existing continuum-component implementation.

## 4. Frozen solve, branch and quadrature panels

Every panel starts independently from the old pre-ladder discovery guide

$$
R_{\rm start}=0.9430108292781663,
\qquad
\Omega_{\rm start}=1.5868166272376472.
$$

The post-result ladder extrapolation is neither read nor used as a start or
target. Each panel performs exactly eight undamped analytic Newton steps; no
line search, fallback, neighbor-panel seeding or tolerance-driven early stop
is permitted. Every recorded iterate must obey

$$
|R-R_{\rm start}|<0.05,
\qquad
|\Omega-\Omega_{\rm start}|<0.05.
$$

The quadrature panels are fixed as follows:

| panel | implementation | order | role |
| --- | --- | ---: | --- |
| numpy-256 | `numpy.polynomial.legendre.leggauss` | 256 | lower-order control |
| numpy-512 | `numpy.polynomial.legendre.leggauss` | 512 | original-family control |
| scipy-1024 | `scipy.special.roots_legendre` | 1024 | independent highest-order target |

The corrected numerical target is, before seeing any result, defined as the
`scipy-1024` root. The other panels are convergence and implementation
controls.

## 5. Frozen continuum gates

Every panel must satisfy all of the following:

1. all root, residual, Jacobian, gain and conditioning values are finite;
2. all Newton iterates remain inside the registered corridor;
3. $R>0$, $\Omega>0$ and $I_T<0$;
4. $\max(|F_R|,|F_T|)\leq10^{-12}$;
5. $|(-\Omega/I_T)-15|\leq10^{-10}$;
6. the maximum discrepancy between the analytic-balance components and the
   pre-existing component evaluator is at most $5\times10^{-14}$;
7. the maximum two-norm Jacobian condition number along the fixed Newton path
   is at most $10^8$.

Across all three roots, both the radius range and frequency range must be at
most $5\times10^{-11}$. These are double-precision quadrature/root controls,
not an interval existence certificate for the continuum integrals.

## 6. Frozen provenance audit

Only after all three continuum roots have been constructed may the script
load the old discovery and ladder JSON files. It must reproduce from the
discovery source, within $2\times10^{-15}$,

$$
(R,\Omega,\widehat\eta_{\rm required})
=(0.9430108292781663,
  1.5868166272376472,
  15.016345187237246),
$$

and confirm that the source gain differs from 15 by at least $10^{-3}$.

The ladder source must retain its historical decision, clean execution
revision, five exact registered cells, five cellwise passes, all-cell
certificate flag and anchor overlap. No finite root is recomputed.

## 7. Frozen reuse of the original scaling gates

For $y\in\{R,\Omega\}$ and the corrected target $y_\infty$, define
$e_y(\alpha)=|y(\alpha)-y_\infty|$. The error values must be positive so the
registered logarithmic diagnostics are defined. Without changing any earlier
threshold, require:

1. both errors decrease strictly across every halving L0--L4;
2. the L1--L4 log-log slopes for both observables lie in $[0.8,1.2]$;
3. each L4 error is at most $0.35$ times its L2 anchor error;
4. for $y_{\rm Rich}=2y(0.0025)-y(0.005)$,
   $|y_{\rm Rich}-y_\infty|/e_y(0.0025)\leq0.1$.

Successive-difference ratios may be reported descriptively but are not added
as decision gates.

## 8. Decisions and claim boundary

Decision is **fixed-gain-continuum-reconciliation-pass** only if every
continuum, cross-panel, provenance, ladder-integrity and original scaling
gate passes.

Decision is **fixed-gain-target-ladder-mismatch** if the corrected continuum
target and all inputs pass but at least one original scaling gate still
fails.

Any continuum-panel, provenance, integrity or arithmetic failure is
**fixed-gain-continuum-inconclusive**.

A pass establishes a quadrature-converged numerical continuum root at the
same fixed gain as the certified five-cell ladder and numerical consistency
with first-order convergence under the original finite set of gates. It does
not prove continuum-root existence by interval arithmetic, convergence for
all $\alpha$, stability away from the anchor, formation, noise robustness,
an internal $S^1$ degree of freedom, work, inertia or mass. The
$A_{\rm att}=7$ holdout remains sealed.
