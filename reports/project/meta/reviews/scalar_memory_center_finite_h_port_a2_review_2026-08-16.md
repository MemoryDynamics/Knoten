# Critical review: finite-H center-port Gate A2

Date: 2026-08-16.

Verdict: **the preregistered A2 certificate passes for every registered cell,
but it establishes only a passive effective filter port.** It removes the
finite-memory tail as an objection to that mathematical port. It does not
identify a natural microscopic actuator, a material center of mass or a
physical mass.

The target calculation was executed from the clean prospective revision
`2792ca17d076f2e00f628092790e78b188dfa18c`. Its machine-readable record has
an empty pre-run Git status and states that no stochastic trace, new seed or
sealed P0 transfer cell was opened.

## 1. Independent algebra check

Use the registered update convention

\[
x_{n+1}=(1-g)x_n+g c_n+\alpha u_n,
\qquad
c=B_H x,
\]

and output \(y_n=(c_{n+1}-c_n)/\alpha\). For the normalized finite geometric
memory,

\[
B_H(z)={\alpha\over1-q^H}{1-q^Hz^{-H}\over1-qz^{-1}},
\]

direct elimination gives

\[
{y\over u}=G_H(z)
={(z-1)B_H(z)\over z-(1-g)-gB_H(z)}.
\]

For \(H=\infty\), \(B_\infty=\alpha z/(z-q)\). The denominator factorizes
exactly because \(q=1-\alpha\):

\[
[z-(1-g)](z-q)-g\alpha z
=(z-1)[z-q(1-g)].
\]

The translational pole at one therefore cancels in the velocity transfer,
leaving

\[
G_\infty(z)={\alpha z\over z-a},
\qquad a=q(1-g).
\]

For the registered cells \(0<a<1\), so this transfer is stable and

\[
\min_{|z|=1}\Re G_\infty={\alpha\over1+a},
\qquad
\lVert G_\infty\rVert_\infty={\alpha\over1-a}.
\]

These identities agree with the protocol and executable.

## 2. Tail perturbation and the apparent singularity

Writing \(B_H=B_\infty(1+s)\) gives

\[
s={q^H(1-z^{-H})\over1-q^H},
\qquad
{G_H\over G_\infty}={1+s\over1-R},
\qquad
R={gG_\infty s\over z-1}.
\]

The factor \(s/(z-1)\) has a removable singularity at \(z=1\): it is a
finite delay polynomial times \(q^H/(1-q^H)\). Hence

\[
\left|{1-z^{-H}\over z-1}\right|\le H
\]

on the unit circle, including the limiting value at zero frequency. This
justifies the registered stable-loop bound

\[
\lVert R\rVert_\infty\le
r_H={g\alpha\over1-a}{Hq^H\over1-q^H}.
\]

If \(r_H<1\), the finite-tail feedback correction is stable. Moreover,

\[
G_H-G_\infty
=G_\infty{s+R\over1-R},
\]

which yields exactly the registered error bound \(E_H\) and therefore

\[
\Re G_H\ge {\alpha\over1+a}-E_H.
\]

No sampled-frequency inference is needed for this step.

## 3. Numerical and implementation checks

All five registered cells pass the three decisional analytic gates:

- \(r_H<1\), with the largest bound \(5.83\,10^{-5}\);
- a strictly positive certified real-part lower bound, whose smallest value
  is \(1.244\,10^{-3}\);
- a safety factor of at least 89.2 against the registered minimum of 10.

The 131073-point grids independently remain positive and stay below the
analytic transfer-error and loop-gain bounds. They are correctly labelled as
non-decisional. The implementation treats the \(z=1\) limits explicitly,
uses the finite geometric mean age for the exact DC gain and reports every
threshold and input cell in JSON.

The observed decrease of the safety factor along the alpha ladder is not a
failure: the positive-real margin scales approximately with alpha while the
fixed-tail perturbation is nearly constant on this matched
\(H=\lceil12/\alpha\rceil\) ladder. It does mean the certificate must not be
extrapolated to arbitrarily small alpha at fixed tail extent without a new
bound or run.

## 4. What the pass proves

For each registered finite-\(H\) local linear plant, the stable velocity
transfer is strictly positive real. The discrete positive-real result thus
provides a passive input/output realization. Multiplication of the output by
the positive constant alpha changes only the supply normalization, so the
same sign result applies to \(u_n\,\Delta c_n\).

A separately declared interaction \(U_{\rm ext}(c_H,Q)\), implemented with a
discrete gradient, then gives equal-and-opposite interaction work for the
center and external subsystem. This is a coherent reciprocal **effective
wrapper** and repairs the finite-\(H\) bookkeeping objection for that new
architecture.

## 5. What the pass does not prove

The following stronger readings are rejected:

- Positive realness does not select this wrapper over the equally compatible
  conditional \(x\)-work ledger \(u\,dx=u\,dc+u\,dr\).
- The wrapper is stipulated at the normalized history centroid. It is not
  derived from a force acting on a conserved microscopic constituent.
- The positive-real storage need not be the material energy of every native
  FIFO history degree of freedom.
- The registered cells couple alpha and \(H\) at tail extent 12; they do not
  establish a uniform \(H\to\infty\), \(\alpha\to0\) theorem.
- The calculation is local and linear. It does not establish nonlinear or
  global passivity, additive two-node momentum, SI calibration, S1 topology
  or an internal oscillator.
- The safety factor measures conservatism relative to this analytic tail
  bound, not an experimentally calibrated physical margin.

## 6. Downstream decision

The A2 result authorizes only a separately preregistered \(B^\ast\)
system-identification test of the filter prediction

\[
m_{\rm filter}={\tau\over\mu}.
\]

Physical Gate B remains blocked because Gate A still lacks microscopic port
selection. D0--D5 remain sealed because no S1 candidate exists. This is the
strongest inference consistent with both the analytic pass and the original
falsification charter.
