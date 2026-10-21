# Finite-memory stationarity and the weak-noise gap

Date: 2026-10-21. Internal analytical note against `e608c0c`, with synthetic
kernel/density checks. No production trajectories, orbit search or new
model rule. This refines one prerequisite of the
[nonlinear research calculation](pre_reassessment_2026-10-19.md); it is not
an independent referee review or a claim of mathematical priority.

## Result and scope

For **fixed finite history length and fixed positive Gaussian noise**, the
translation-reduced nonlinear Gaussian-memory process has a unique
stationary distribution with all polynomial moments finite. A global
minorization gives uniform convergence in total variation. Its bound is
generally far too weak to certify a practical burn-in and is not uniform
as noise vanishes or history length grows.

This minorization does **not** establish the stationary weak-noise expansion
around the collapsed state. A separate
[global-contraction argument](weak_noise_validity_2026-10-21.md) now does so
for quadratic moments in a stricter domain, including untruncated memory,
but does not cover any active archived Paper-I cell. An explicit
two-point-history example below has a stable collapsed state and a stable
nonzero period-two orbit while its local
linear gain still satisfies $0<g<1$. This demonstrates coexistence, not
which attractor dominates the stationary small-noise limit.

## Relative-state proposition

Take the filled finite-history rule with point deposition,
$H\geq2$, $k=H-1$, fixed weights $\gamma_j\geq0$ and
fixed $\varepsilon>0$. The innovations $\xi_n\sim\mathcal N(0,I_d)$ are
independent of one another and of the initial history:

$$
x_{n+1}-x_n=-\eta\sum_{j=1}^{H-1}\gamma_j
\nabla K(x_n-x_{n-j})+\varepsilon\xi_{n+1}.
$$

The age-zero term vanishes for the radial manuscript kernel. In the
canonical convention $\gamma_j=\alpha q^j$, $0<\alpha<1$, $q=1-\alpha$, with total
retained mass $M_H=1-q^H$; a fixed mass scale only rescales the weights.
This proposition concerns the filled buffer with fixed weights, not the
transient startup or an untruncated memory measure.
It is a statement about the real-valued stochastic equation, not the exact
finite-precision transition law of a particular PRNG and floating-point runner.

Let $v_n=x_n-x_{n-1}$ and
$V_n=(v_n,v_{n-1},\ldots,v_{n-k+1})$. Cumulative sums recover every lag
$L_{j,n}=x_n-x_{n-j}$, so this is an invertible parametrization of the
translation-reduced history. Its transition is

$$
v_{n+1}=F(V_n)+\varepsilon\xi_{n+1},\qquad
V_{n+1}=(v_{n+1},v_n,\ldots,v_{n-k+2}).
$$

For $H=2$ the retained suffix is empty. Assume $F$ is measurable and
globally bounded by $B<\infty$. For the two Gaussian scales a sufficient
bound is

$$
B=|\eta|\sum_{j=1}^{H-1}\gamma_j\,e^{-1/2}
\left(\frac{|A_r|}{s_r}+\frac{|A_a|}{s_a}\right).
$$

Indeed, the maximum gradient norm of $A\exp(-|u|^2/(2s^2))$ is
$|A|e^{-1/2}/s$. This uses the full bounded force, not its unbounded cubic
Taylor polynomial. No local-gain stability assumption is needed here.

### Proof of existence and uniqueness

Write $\varphi_\sigma$ for the centered $d$-dimensional Gaussian density
with covariance $\sigma^2 I_d$. For every $|m|\leq B$,
$|z-m|^2\leq2|z|^2+2B^2$ implies

$$
\varphi_\varepsilon(z-m)
\geq c\,\varphi_{\varepsilon/\sqrt2}(z),\qquad
c=2^{-d/2}\exp(-B^2/\varepsilon^2)>0.
$$

After $k$ updates, all increments in $V$ are fresh. Their joint density
in chronological order is the product of conditional Gaussian densities;
each conditional mean is bounded by the same $B$, independently of the
old state and earlier fresh increments. Reversing their order has unit
Jacobian. Hence, for the relative-state transition kernel $P$,

$$
P^k(V,\cdot)\geq\delta\nu(\cdot),\qquad
\delta=c^k,
\qquad
\nu=\mathcal N\bigl(0,(\varepsilon^2/2)I_{dk}\bigr).
$$

Subtracting this common positive measure shows that $P^k$ contracts the
total-variation distance between probability laws by at most $1-\delta$.
The space of probability measures is complete in total variation. The
contraction therefore has a unique fixed point $\pi$. Since
$(\pi P)P^k=(\pi P^k)P=\pi P$, uniqueness also gives $\pi P=\pi$.
Thus existence is established, not assumed. With
$\|\mu-\nu\|_{\rm TV}=\sup_A|\mu(A)-\nu(A)|$,

$$
\sup_V\|P^n(V,\cdot)-\pi\|_{\rm TV}
\leq (1-\delta)^{\lfloor n/k\rfloor}.
$$

This is a direct specialization of the standard whole-state-space
minorization argument. See Roberts and Rosenthal,
[Theorem 8 and Section 4.3](https://www.probability.ca/jeff/ftpdir/probsurv.pdf),
author version revised August 2004, corrected August 2023, inspected
2026-10-21. Their stated theorem assumes an invariant law; the contraction
argument above separately supplies its existence in this model.

### Moments and limits

For every $p>0$, bounded drift and Gaussian innovations uniformly bound
the next increment's $p$th moment. Integrating against $\pi$ gives finite
moments of every coordinate and every finite lag. In particular,

$$
\mathbb E_\pi|v|^2\leq B^2+d\varepsilon^2,\qquad
\mathbb E_\pi|L_j|^2\leq j^2(B^2+d\varepsilon^2).
$$

The cross term in the first bound is zero by innovation independence;
the second uses Cauchy--Schwarz for a sum of $j$ increments. Thus both
relative radius observables have finite stationary second moments.
The proposition already applies to the zero-feedback Brownian control;
relative stationarity alone is not evidence of self-localization.
This is not an $O(\varepsilon^2)$ bound and proves no concentration near
the collapsed state. The absolute position is not included in $V$;
its stationarity or localization does not follow.

The log minorization constant is
$\log\delta=-k[d\log2/2+B^2/\varepsilon^2]$. It deteriorates as
$\varepsilon\to0$ when $B>0$, and as $H\to\infty$ even at $B=0$.
It does not justify a practical mixing time, stationarity of the archived
terminal blocks, interchange of limits, a nonlinear diffusion coefficient
or an untruncated-memory theorem. The actual mixing may be much faster;
failure of this bound to be useful is not evidence of slow mixing.

## An exact coexistence check

Set $d=1$, $H=2$, $\alpha=1/2$, $\eta=4$, $s_r=1$, $s_a=3$ and
$\varepsilon=0$. Then $\eta\gamma_1=1$. Define

$$
a=\frac{1-\tfrac14e^{-9/2}}{e^{-1/2}-e^{-9/2}},\qquad
b=a-\tfrac14,\qquad A_r=b,\quad A_a=9a.
$$

The exact relative map of the full Gaussian kernel is

$$
v_{n+1}=F(v_n),\qquad
F(v)=-\left(ae^{-v^2/18}-be^{-v^2/2}\right)v.
$$

It has $F(0)=0$ and $F'(0)=-1/4$, so the collapsed relative state is
locally attracting. Moreover,
$\kappa=A_a/9-A_r=1/4$, $M_H=3/4$ and $g=\eta M_H\kappa=3/4$,
inside the gain range of the linear reference.

By construction $F(3)=-3$ and $F(-3)=3$. At both points,

$$
F'(3)=F'(-3)=-8b e^{-9/2}.
$$

Since $0<b<2$ and $16e^{-9/2}<1$, the two-step multiplier is
$(8b e^{-9/2})^2<1$. This is a locally attracting period-two orbit of the
relative map, in addition to the collapsed attractor. Absolute translation
remains neutral. The coefficients were constructed algebraically; no root
search, parameter scan or stochastic orbit simulation is involved.

At positive noise the proposition still gives a unique relative invariant
law for this example. Nothing above calculates its small-noise weights
near the competing attractors. The example therefore does not falsify the
formal coefficient for a correctly justified local branch, but it does
prevent using local linear stability as a proof that the global stationary
law is that branch.

## Consequence for Paper I

The finite-$H$, positive-noise existence prerequisite is now supported by
an explicit argument. Without an additional global condition, the
stationary weak-noise expansion and uniform remainder estimates remain
open. The separate contraction note supplies a sufficient domain for
moments, not the transport-limit interchange or a theorem at the archived
active parameters. A next validation must distinguish a globally stationary
prediction from a conditional or finite-time local-branch prediction before
choosing data.
Neither a theorem valid at each fixed noise nor a long-looking trajectory
settles that distinction.

[Synthetic checks](../scripts/test_finite_memory_stationarity.py) compare
the Gaussian density lower bound with independent SciPy log densities,
the force bound with the production kernel, and the exact coexistence map
and derivatives with the production gradient/Hessian. They check the
algebraic implementation, not the theorem's generality or a stationary
small-noise distribution. At the original stationarity commit, nine new
checks and the existing 21 local-response, eight baseline and 14
documentation/claim checks passed locally (52 total), with
NumPy 2.3.5, SciPy 1.16.3 and pytest 8.4.2. The dedicated research CI includes
the new test file. Frozen manuscript PDFs and evidence are unchanged.
The missing full-text aging-paper comparison remains open: the official
SSRN abstract and download endpoints again returned HTTP 403 on
2026-10-21; accessible abstracts do not establish coefficient-level novelty.
