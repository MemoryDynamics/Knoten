# Finite-memory stationarity and an attractive-kernel weak-noise domain

Date: 2026-10-21. Internal analytical note against `e608c0c`, with synthetic
kernel/density checks. No production trajectories, orbit search or new
model rule. This refines one prerequisite of the
[nonlinear research calculation](pre_reassessment_2026-10-19.md); it is not
an independent referee review or a claim of mathematical priority.
The positive-averaging extension below follows the transport note at
commit 50d4307.

## Result and scope

For **fixed finite history length and fixed positive Gaussian noise**, the
translation-reduced nonlinear Gaussian-memory process has a unique
stationary distribution with all polynomial moments finite. A global
minorization gives uniform convergence in total variation. Its bound is
generally far too weak to certify a practical burn-in and is not uniform
as noise vanishes or history length grows.

This minorization alone does **not** establish the stationary weak-noise
expansion around the collapsed state. An additional positive-averaging
argument below establishes that expansion for quadratic moments at fixed
finite $H$ in a domain containing the archived Paper-I model coefficients.
Its constants do not give a useful finite-noise error tolerance there.
A separate [global-contraction argument](weak_noise_validity_2026-10-21.md)
covers both moments and transport, including untruncated memory, but its
stricter sufficient condition excludes all active archived cells. An explicit
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

## Positive averaging at fixed finite history

Suppose in addition that $\eta\geq0$, $A_r,A_a\geq0$,
$s_a\geq s_r>0$ and $A_a/s_a^2\geq A_r/s_r^2$. Then

$$
\nabla K(u)=c(|u|)u,\qquad
c(r)=\frac{A_a}{s_a^2}e^{-r^2/(2s_a^2)}
     -\frac{A_r}{s_r^2}e^{-r^2/(2s_r^2)},\qquad
0\leq c(r)\leq c_{\max}:=\frac{A_a}{s_a^2}.
$$

The sign follows by comparing both the amplitudes and the exponential
factors. This is a global radial-force condition, not positive definiteness
of the Hessian. With $\Gamma_H=\sum_{j=1}^{H-1}\gamma_j$, require

$$
\chi=\eta c_{\max}\Gamma_H<1,\qquad \delta_{\rm a}=1-\chi>0.
$$

Here $\delta_{\rm a}$ is a self-weight bound, distinct from the
noise-dependent minorization constant above. In the canonical convention
$\Gamma_H=q-q^H=M_H-\alpha$. No memory renormalization is introduced.

### A pathwise diameter bound

Write $X_n=(x_n,x_{n-1},\ldots,x_{n-k})$ and
$a_{j,n}=\eta\gamma_j c(|x_n-x_{n-j}|)$ for $1\leq j\leq k$.
The update is exactly

$$
x_{n+1}=a_{0,n}x_n+\sum_{j=1}^k a_{j,n}x_{n-j}
             +\varepsilon\xi_{n+1},\qquad
a_{0,n}=1-\sum_{j=1}^k a_{j,n}\geq\delta_{\rm a}.
$$

All coefficients are nonnegative and sum to one. Thus
$X_{n+1}=P_nX_n+\varepsilon e_0\xi_{n+1}$, with a row-stochastic
companion matrix $P_n$: its first row is $(a_{0,n},\ldots,a_{k,n})$
and its remaining rows shift the history.

Let $\mathcal D(X)=\max_{i,j}|X_i-X_j|$ using Euclidean distance.
A stochastic matrix cannot increase this diameter. After $k$ steps
every row of $P_{n+k-1}\cdots P_n$ has coefficient at least
$\delta_{\rm a}^k$ on the initial current position $x_n$: successive
new positions retain this contribution through their self-weight, and
the oldest retained position is $x_n$ itself. Subtract that common
column contribution. The residual rows have common mass
$1-\delta_{\rm a}^k$, so their convex combinations have diameter at most
$(1-\delta_{\rm a}^k)\mathcal D(X_n)$.

Each propagated noise injection is a stochastic-matrix column times
$\varepsilon\xi$; its diameter is at most $\varepsilon|\xi|$.
Expanding the exact matrix recursion therefore gives, pathwise,

$$
\mathcal D(X_{n+k})\leq
(1-\delta_{\rm a}^k)\mathcal D(X_n)
       +\varepsilon\sum_{\ell=1}^k|\xi_{n+\ell}|.
$$

The matrices depend on the noisy history. No independence of those
matrices and the innovations was used. This common-column argument is
a specialization of standard stochastic-matrix contraction methods,
not a new general method. For historical context see Mott and Schneider,
[Matrix Norms applied to Weakly Ergodic Markov Chains (1957)](https://people.math.wisc.edu/hans/paper_archive/scanned_papers/hs010.pdf),
pp. 331--333, inspected 2026-10-21. The model-specific proof is given
above; no stochastic concentration result is attributed to that paper.

At positive noise the relative invariant law already exists and has
finite moments by the first proposition. Since $\mathcal D$ is
translation invariant, stationarity and Minkowski's inequality yield
for every $1\leq p<\infty$,

$$
\boxed{\|\mathcal D\|_{L^p(\pi_\varepsilon)}
 \leq \varepsilon\,B_H\|\xi\|_{L^p},\qquad
B_H=\frac{k}{\delta_{\rm a}^k}.}
$$

All finite relative lags and increments consequently are
$O_{L^p}(\varepsilon)$. At zero noise the diameter decreases geometrically
in $k$-step blocks, excluding nonzero recurrent relative states in this
domain. Neither statement proves absolute-position stationarity.

### Stationary moment expansion

For $V=(v_0,\ldots,v_{k-1})$ let $L_0=0$,
$L_j=\sum_{i=0}^{j-1}v_i$, and use the norm
$\|V\|_{\mathcal D}=\max_{i,j}|L_i-L_j|$ on relative histories.
It equals the position-history diameter. Write the noise-free map as
$T_0(V)=AV+Q(V)+R(V)$, where $A$ includes the shift and

$$
Q(V)_0=-\eta\lambda\sum_{j=1}^k\gamma_j|L_j|^2L_j,\qquad
\lambda=\frac{A_r}{2s_r^4}-\frac{A_a}{2s_a^4}.
$$

All other coordinates of $Q$ and $R$ vanish. At collapse the linear
position update has the same averaging structure, with
$c(0)=\kappa\in[0,c_{\max}]$. Hence

$$
\|A^m\|_{\mathcal D}\leq
(1-\delta_{\rm a}^k)^{\lfloor m/k\rfloor},
\qquad \sum_{m\geq0}\|A^m\|_{\mathcal D}\leq B_H.
$$

If $\chi=0$, interpret the bound directly: $A^k=0$ in relative
coordinates and the sum is at most $k$.
The global Gaussian Taylor bounds give
$\|T_0(V)-AV\|_{\mathcal D}\leq
\eta c_3\Gamma_H\|V\|_{\mathcal D}^3$ and
$\|R(V)\|_{\mathcal D}\leq
\eta c_5\Gamma_H\|V\|_{\mathcal D}^5$, where
$c_3=A_r/(2s_r^4)+A_a/(2s_a^4)$ and
$c_5=A_r/(8s_r^6)+A_a/(8s_a^6)$.

Realize the invariant Markov chain on two-sided time with its iid
Gaussian innovations. This is available from its stationary transition
law: for $\varepsilon>0$, reconstruct
$\xi_{n+1}=(v_{n+1}-F(V_n))/\varepsilon$; its conditional law given
the entire past is always the standard Gaussian. A causal nonlinear
solution from the infinite innovation past is not assumed. On the same
probability space define the stationary filters

$$
W_{n+1}=AW_n+e_0\xi_{n+1},\qquad
Z_{n+1}=AZ_n+Q(W_n).
$$

The summable linear propagator defines both filters and all their
finite moments. They are jointly stationary with $V^\varepsilon$.
Backward iteration of
$U_{n+1}=AU_n+[T_0(V^\varepsilon_n)-AV^\varepsilon_n]$ for
$U=V^\varepsilon-\varepsilon W$ gives $U=O_{L^p}(\varepsilon^3)$:
the old initial term tends to zero in $L^p$ and the forcing is bounded
by the established $L^{3p}$ moment estimate.
For $E=V^\varepsilon-\varepsilon W-\varepsilon^3 Z$ the forcing is
$Q(V^\varepsilon)-Q(\varepsilon W)+R(V^\varepsilon)$.
The cubic difference bound and Holder's inequality give
$O_{L^p}(\varepsilon^5)$ forcing. Summing the same propagator yields

$$
V^\varepsilon=\varepsilon W+\varepsilon^3 Z+
                   O_{L^p}(\varepsilon^5).
$$

Consequently every fixed quadratic relative observable has its
$\varepsilon^2$ and $\varepsilon^4$ terms with
$O(\varepsilon^6)$ remainder at fixed $H$ and model coefficients.
Odd drift and uniqueness make the relative invariant law symmetric,
so these second-moment coefficients also give covariances. The
[existing Lyapunov/Wick calculation](pre_reassessment_2026-10-19.md)
identifies them wherever its linear matrix is stable, as established here.
The numerical helper retains its narrower input range $0\leq g<1$;
the averaging proposition does not rely on that software restriction.
This is a moment result only: the diameter argument
is not a contraction between two different noisy histories, and supplies
no summable all-lag Taylor remainder or nonlinear transport expansion.

### Archived parameters and the limits of this bound

The [frozen manifest](../evidence/trace_manifest.json) and its
[extraction assertions](../scripts/finalize_evidence.py) use
$H=600$, $\alpha=0.01$, $s_r=1$, $s_a=3$, $A_r=1$, unit deposited
mass and point deposition; active $\eta=0.15$. Their two attractive
amplitudes satisfy the global sign assumptions:

| $A_a$ | $\chi$ | $\delta_{\rm a}$ | $\log_{10} B_H$ |
| --- | --- | --- | --- |
| 20 | 0.3291983302 | 0.6708016698 | 106.64754 |
| 35 | 0.5760970779 | 0.4239029221 | 226.04485 |

Thus the model coefficients of all 45 active cases, as well as the
40 zero-feedback controls, lie in this **fixed-$H$ asymptotic moment
domain**. They do not pass the separate global-Hessian contraction
condition: its active budgets remain 47.85 and 72.6, not below one.
The enormous $B_H$ values already make the moment bound impractical;
they are not measured relaxation times or estimates of the actual
remainder. This result does not certify the archived finite noise,
terminal-block stationarity, radius-error tolerance, transport or
interchange with $H\to\infty$.

It also does not settle the separate FIFO orbit program. The prepared
[P4-RS anchor](../../../reports/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_2026-08-30.json)
uses $(A_r,A_a)=(1,3.5)$ with the same widths, giving
$c(0)=3.5/9-1<0$, outside this positive-averaging domain. No orbit
was recomputed or reclassified. The coexistence example below instead
violates $\chi<1$, since its $\chi=a>1$.

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

The finite-$H$, positive-noise existence prerequisite and an additional
positive-averaging domain for stationary weak-noise moments now have
explicit arguments. The latter includes the archived model coefficients,
but supplies no practical error tolerance at their finite noise. The
separate contraction note controls untruncated moments and transport
under a different, stricter sufficient condition that those active cases
fail. A next validation must distinguish a globally stationary
prediction from a conditional or finite-time local-branch prediction before
choosing data.
Neither a theorem valid at each fixed noise nor a long-looking trajectory
settles that distinction.

[Synthetic checks](../scripts/test_finite_memory_stationarity.py) compare
the Gaussian density lower bound with independent SciPy log densities,
the force bound with the production kernel, and the exact coexistence map
and derivatives with the production gradient/Hessian. The averaging
extension adds 31 checks of state-dependent stochastic-matrix blocks,
propagated-noise bounds, the production convex update (including zero
curvature), its linear quotient, the archived parameter audit and invalid
diagnostic inputs. They check the algebraic implementation, not the
theorem's generality or a sampled stationary small-noise distribution.
Verification of the averaging extension on 2026-10-21: 102 research
checks, eight frozen-reference checks and ten documentation/claim checks
pass locally (120 total); Ruff and the strict documentation build pass.
No independent mathematical review is implied.
At the original stationarity commit, nine new
checks and the existing 21 local-response, eight baseline and 14
documentation/claim checks passed locally (52 total), with
NumPy 2.3.5, SciPy 1.16.3 and pytest 8.4.2. The dedicated research CI includes
the new test file. Frozen manuscript PDFs and evidence are unchanged.
The missing full-text aging-paper comparison remains open: the official
SSRN abstract and download endpoints again returned HTTP 403 on
2026-10-21; accessible abstracts do not establish coefficient-level novelty.
