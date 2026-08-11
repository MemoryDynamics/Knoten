# Preregistration: inertial reversible vector-field analytic gate

Date: 2026-08-11.

## Question

Can the existing parity-even local vector energy be extended by one conjugate
field state so that its linear dynamics is O(d)-covariant, energy-consistent
and capable of stable damped oscillations?

This is a mechanism-consistency audit. It does not infer coefficients from
the passive memory, simulate a knot, or test a particle, spin or photon claim.

## Proposed extension

Let \(m(x,t)\) be the vector field, \(\pi(x,t)\) its conjugate momentum, and
\(I>0\) an inertia density. The proposed homogeneous dynamics is

\[
\partial_t m=\frac{\pi}{I},
\qquad
\partial_t\pi=-\frac{\delta\mathcal F}{\delta m}
-\frac{\gamma}{I}\pi.
\]

A directed trajectory source would enter the second equation as \(+J\), but
source and trajectory readout are deliberately excluded from this analytic
gate.

For Helmholtz channel \(q\in\{L,T\}\),

\[
D_q(k)=a+b_qk^2+ck^4,
\qquad
I s^2+\gamma s+D_q(k)=0.
\]

The exact roots are

\[
s_\pm=\frac{-\gamma\pm\sqrt{\gamma^2-4ID_q(k)}}{2I}.
\]

## Fixed interpretation

- \(D_q(k)<0\): restoring instability; reversible coupling must not be called
  stabilizing.
- \(D_q(k)>0,\gamma=0\): bounded conservative oscillation, not asymptotic
  relaxation.
- \(D_q(k)>0,\gamma>0,4ID_q(k)>\gamma^2\): asymptotically stable damped
  oscillation.
- \(D_q(k)>0,\gamma>0,4ID_q(k)\le\gamma^2\): critical or overdamped return.

With \(a,c,u,I>0\), natural units are

\[
\ell_0=(c/a)^{1/4},
\quad
m_0=\sqrt{a/u},
\quad
t_I=\sqrt{I/a},
\quad
\zeta=\frac{\gamma}{2\sqrt{Ia}}.
\]

The new irreducible inputs are at least \(\zeta\), \(b_L/\sqrt{ac}\) and
\(b_T/\sqrt{ac}\). Nondimensionalization does not derive them.

## Fixed analytic gates

The implementation must pass all of the following at tolerance \(10^{-12}\):

1. numerical eigenvalues of each channel operator match the quadratic roots;
2. the full \((m,\pi)\) Fourier generator transforms covariantly under the
   block action `diag(O,O)` for dimensions 1, 2, 3 and 5;
3. at \(\gamma=0\), \(A^T G_E+G_EA=0\) in the quadratic energy metric;
4. at \(\gamma>0\), the homogeneous energy rate equals
   \(-\gamma\lvert\pi/I\rvert^2\);
5. a fixed negative-curvature control has a positive real eigenvalue even at
   positive damping;
6. the universal dimensionless classification agrees with the exact
   boundaries \(\widehat D=0\) and \(\widehat D=\zeta^2\).

The visual witness uses \(\widehat D=1\) and
\(\zeta\in\{0,0.05,1,1.5\}\). These values illustrate conservative,
underdamped, critical and overdamped regimes; they are not fitted parameters.

## Decision rule

- **Fail:** do not implement a field pilot.
- **Structural pass:** the proposed extension is mathematically coherent and
  may proceed to a separate source/readout and energy-accounting design.

Even a structural pass does not authorize parameter fitting or a nonlinear
knot simulation. The source \(J[x]\), reciprocal force on \(x\), discretized
energy balance and independent time-domain observables must be specified and
preregistered next.
