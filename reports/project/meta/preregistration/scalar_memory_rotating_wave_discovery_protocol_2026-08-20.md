# Prospective analytic-guided discovery: scalar-memory rotating wave

Date: 2026-08-20.

Status: prospective deterministic discovery protocol. This protocol may
identify one candidate for a later S1 P0 freeze. It does not itself open D0,
inspect topology, run stochastic target trajectories or establish a stable
orbit.

## 1. Question and claim boundary

The question is whether the unchanged deterministic K0-H scalar-memory map in
two spatial dimensions admits a co-rotating history

\[
x_n=R e^{in\theta},
\qquad R>0,\quad 0<\theta<\pi.
\]

The primary object is a rotating relative equilibrium of the native discrete
map. Rotational equivariance generates a continuous group orbit, but that
group orbit must not yet be called an internal S1 mode: its phase may be only
the ambient spatial orientation. Topological interpretation remains sealed
until a separate P0-S and D0 contract pass.

Numerical root finding can construct and test this solution to a declared
tolerance. It is not a mathematical existence proof unless followed by an
interval-Newton or equivalent enclosure. Stability is a separate downstream
question.

## 2. Frozen native model

The discovery uses

\[
x_{n+1}
=x_n-\eta\sum_{j=0}^{H-1}w_j
\nabla K(x_n-x_{n-j}),
\qquad
w_j=\alpha M_0(1-\alpha)^j,
\]

with

\[
K(r)
=A_{\rm rep}e^{-r^2/(2\sigma_{\rm rep}^2)}
-A_{\rm att}e^{-r^2/(2\sigma_{\rm att}^2)}.
\]

No noise, external force, oriented memory, conjugate momentum, angular state,
normal-form term or saturation is added. Deposition is delta deposition.
The present-point term \(j=0\) vanishes exactly.

The radial gradient factor is

\[
\nabla K(d)=\phi(|d|)d,
\]

\[
\phi(r)
=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
e^{-r^2/(2\sigma_{\rm rep}^2)}
+
\frac{A_{\rm att}}{\sigma_{\rm att}^2}
e^{-r^2/(2\sigma_{\rm att}^2)}.
\]

## 3. Exact finite-H balance

On the rotating history,

\[
x_n-x_{n-j}
=x_n(1-e^{-ij\theta}),
\qquad
r_j=2R\left|\sin\frac{j\theta}{2}\right|.
\]

Define

\[
A_H(R,\theta)
=\sum_{j=1}^{H-1}
w_j\phi(r_j)(1-\cos j\theta),
\]

\[
S_H(R,\theta)
=\sum_{j=1}^{H-1}
w_j\phi(r_j)\sin j\theta.
\]

The complex update is equivalent to the two real equations

\[
1-\cos\theta=\eta A_H,
\qquad
\sin\theta=-\eta S_H.
\]

For positive \(\eta\) and \(0<\theta<\pi\), every admissible circle must
therefore satisfy

\[
A_H>0,
\qquad
S_H<0.
\]

Eliminating the gain gives the geometry-only compatibility equation

\[
\mathcal C_H(R,\theta)
=A_H\sin\theta+(1-\cos\theta)S_H=0,
\]

followed by the independently agreeing gains

\[
\eta_R=\frac{1-\cos\theta}{A_H},
\qquad
\eta_T=-\frac{\sin\theta}{S_H}.
\]

This is an identity in the native update, not a fitted oscillator equation.

## 4. Analytic parameter restriction

Fix the repository scale convention

\[
\sigma_{\rm rep}=1,\quad
\sigma_{\rm att}=3,\quad
A_{\rm rep}=1,\quad M_0=1.
\]

For \(0<A_{\rm att}<9\), the force factor is negative at the origin and
positive at large radius. It has one crossing

\[
r_\ast
=\sqrt{
\frac{2\log(9/A_{\rm att})}{1-1/9}
}.
\]

Thus recent short chords can provide forward repulsion while older longer
chords provide radial attraction. A necessary radial condition is

\[
\max_{1\leq j<H}r_j>r_\ast;
\]

in particular \(2R>r_\ast\).

At \(A_{\rm att}=0\), \(\phi<0\) everywhere and \(A_H>0\) is impossible. At
\(A_{\rm att}\geq9\), \(\phi\geq0\) everywhere. For a fundamental
\(\theta=2\pi/P\) orbit and a history containing complete periods, pairing
ages \(j\) and \(P-j\) gives

\[
\sum_j q^j\phi(r_j)\sin(j\theta)>0,
\]

so \(S_H<0\) is impossible. The \(A_{\rm att}=35\) compact reference is
therefore an explicit no-propulsion control for this mechanism. This finite
pairing theorem is not extrapolated to arbitrarily truncated, aliased
histories.

## 5. Matched continuum guide

Use

\[
t=\alpha j,\qquad
\theta=\Omega\alpha,\qquad
H=\lceil C/\alpha\rceil,\qquad
\eta=\widehat\eta\,\alpha.
\]

As \(\alpha\to0\), define

\[
I_R(R,\Omega)
=M_0\int_0^C
e^{-t}
\phi\!\left(2R\left|\sin\frac{\Omega t}{2}\right|\right)
(1-\cos\Omega t)\,dt,
\]

\[
I_T(R,\Omega)
=M_0\int_0^C
e^{-t}
\phi\!\left(2R\left|\sin\frac{\Omega t}{2}\right|\right)
\sin\Omega t\,dt.
\]

The leading circle conditions are

\[
I_R=0,\qquad I_T<0,\qquad
\widehat\eta=-\frac{\Omega}{I_T}>0.
\]

The first-order continuum skeleton therefore needs zero net radial velocity
and memory-powered tangential drift. This is not mechanical centripetal
acceleration and does not establish inertia.

## 6. Frozen discovery panel

The continuum discovery panel is fixed before execution:

| quantity | fixed value |
| --- | --- |
| architecture | native K0-H |
| dimension | \(d=2\) |
| noise and external force | \(\varepsilon=0\), none |
| deposition | delta |
| \(M_0,A_{\rm rep},\sigma_{\rm rep},\sigma_{\rm att}\) | \(1,1,1,3\) |
| primary tail extent | \(C=12\) |
| mechanism amplitudes | \(A_{\rm att}\in\{3.5,5.5,6.5,7.5,8.0,8.5\}\) |
| analytic controls | \(A_{\rm att}\in\{0,9,35\}\) |
| angular-frequency grid | 161 logarithmic points on \([0.05,8]\) |
| radius bracket grid | 241 logarithmic points on \([0.05,6]\) |
| primary quadrature | 512-point Gauss-Legendre |
| convergence quadrature | 256-point Gauss-Legendre |
| radial root refinement | Brent bracket root, absolute tolerance \(10^{-12}\) |

Every sign-changing radial bracket is refined. Every refined row records
\(R,\Omega,I_R,I_T,\widehat\eta,r_\ast\), the bracket and the 256-versus-512
quadrature discrepancy. No plot or hand-selected subwindow is used for
candidate selection.

An admissible continuum row must have

\[
|I_R|\leq10^{-10},\qquad
I_T<0,\qquad
\widehat\eta>0,
\]

and a componentwise quadrature discrepancy at most \(10^{-8}\).

## 7. Candidate selection and finite-H refinement

The native reference scaling \(\alpha=0.01,\eta=0.15\) fixes the target

\[
\widehat\eta_{\rm ref}=\eta/\alpha=15.
\]

Admissible continuum rows are ordered by

\[
\left|\log(\widehat\eta/15)\right|,
\]

then by increasing \(A_{\rm att}\), \(\Omega\) and \(R\). In that fixed order,
at most the first 20 rows initialize a two-variable finite-H root solve with

\[
\alpha=0.01,\quad
H=1200,\quad
\eta=0.15,\quad
\theta=\alpha\Omega.
\]

The solve variables are \(\log R\) and \(\log\Omega\). The first solution
inside the registered radius/frequency box, with

\[
\left|\mathcal R_H\right|_2\leq10^{-11},
\quad A_H>0,\quad S_H<0,
\]

is the sole discovery candidate. The solver may not retune \(\eta\),
\(\alpha\), \(H\), kernel scales or amplitudes. If no row succeeds, discovery
ends without a candidate.

The sensitivity extent \(C=6\) is evaluated only after selection and cannot
change which row wins.

## 8. Seals and downstream boundary

The amplitude \(A_{\rm att}=7.0\) is an untouched parameter holdout and is not
evaluated by this discovery. No random seeds or trajectories are used.
Historical amplitude scans and their seeds are discovery-only context and
cannot count as confirmation.

If a finite-H root is found, its full tuple and generated artifact hashes must
be committed into a new P0-S manifest before:

- full FIFO-map perturbation trajectories;
- Jacobian or Floquet evaluation targeted at that candidate;
- basin-of-attraction tests;
- noisy runs;
- topology, winding or phase analysis;
- opening the \(A_{\rm att}=7.0\) holdout.

A residual pass establishes only an invariant rotating-wave solution to
floating-point tolerance. It does not establish stability, spontaneous
formation, a non-symmetry internal phase, physical work or mass.
