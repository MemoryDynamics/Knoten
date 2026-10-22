# Paired long-time transport: estimator repair and a variance reference

Date: 2026-10-22. Target-free continuation of the
[external-review audit](external_review_audit_2026-10-22.md).
This is an internal derivation with deterministic checks, not an independent
human review, a simulation result, or a panel authorization.

**Result:** the leading finite-lag bias can be removed without replacing
the long-time question by a short-time observable. Shared innovations
cancel the common linear contribution pathwise. The remaining paired
variance has a nonzero third-chaos contribution, calculated below.
Its long-block limit is available. A
[follow-up bound](finite_block_transport_bound_2026-10-22.md) now controls
sampling of the leading coefficient at finite block length and sample
count, without assuming Gaussian or independent blocks. Transfer to the
full estimator and the finite-noise transport remainder remain open.
The implementation decision remains **hold**, not a scientific no-go.

## Estimator and estimand

Keep $H$ fixed. For a stationary, zero-mean increment process, define
the per-coordinate covariance $c_k$ and diffusion coefficient

$$
D_H=\frac{c_0}{2}+\sum_{k\geq1}c_k,
\qquad D_{H,L}=\frac{\mathbb E|X_{n+L}-X_n|^2}{2dL}.
$$

The stationary mean is zero by inversion symmetry and uniqueness in the
strict contraction domain. This contract uses the known mean, not an
empirically centered or detrended trajectory. For even $M$, form $M$
consecutive elementary displacements $Y_b$ of length $L$ per seed:

$$
\widehat D_L=\frac{1}{2dLM}\sum_{b=0}^{M-1}|Y_b|^2,
\qquad
\widehat D_{2L}=\frac{1}{2dLM}
 \sum_{j=0}^{M/2-1}|Y_{2j}+Y_{2j+1}|^2,
\qquad
\widehat D^{\rm TL}=2\widehat D_{2L}-\widehat D_L.
$$

Average this estimator over independent seeds, then difference the two
matched kernels using shared innovations and the same block boundaries.
Do not treat its two lengths as independent estimates. Do not clip a
negative estimate or select a block length after inspecting target data.

This is the known-mean two-length version of the zero-lugsail batch-means
construction, not a new statistical method. Vats and Flegal give the
general linear combination and its bias/variance analysis in
[Sections 4.2--4.4, Eqs. (6)--(7), Theorems 4 and 6](https://arxiv.org/pdf/1809.04541).
Their empirical-centering and finite-sample normalization differ from the
explicit contract here. The identities below are derived directly for
this contract; no finite-sample guarantee is imported from that paper.

### Exact bias identity

If $\sum k|c_k|<\infty$, then

$$
D_{H,L}=D_H-\frac{1}{L}\sum_{k\geq1}kc_k
 +\frac{1}{L}\sum_{k\geq L}(k-L)c_k.
$$

Consequently the $1/L$ term cancels exactly:

$$
\mathbb E\widehat D^{\rm TL}-D_H
=-\sum_{k>L}\min\left(1,\frac{k-L}{L}\right)c_k.
$$

Only a tail remains. This identity applies separately to the linear and
quartic coefficients of the controlled expansion; it does not remove
the nonlinear $O(\varepsilon^6)$ remainder. Increasing the number of
blocks alone does not remove the remaining fixed-$L$ bias.

For canonical exponential memory, let $g_\infty=\eta\kappa\geq0$,
$q=1-\alpha$, $b=qg_\infty$, $r=q+b<1$, and

$$
a=\frac{b(1-qr)}{1-r^2},\qquad
F_L(g_\infty)=\frac{a r^L(1-r^L)}{L(1-r)^2}.
$$

The absolute impulse envelope is $h_0=1$, $h_k=b r^{k-1}$ for $k\geq1$.
Its positive-lag covariance is $a r^{k-1}$, and it dominates the
finite-$H$ linear impulse response. Thus the two-length linear bias
is bounded by $F_L$.

Let $C$ be the unit-noise lag covariance, $M_H=1-q^H$ and
$\beta=\eta M_H\lambda$. The derivative in $t=\beta\varepsilon^2$
has feedback weights $(d+2)w_j C_{jj}$, where
$w_j=\alpha q^j/M_H$. They are dominated by
$B\alpha q^j$, with $B=(d+2)\max_j C_{jj}/M_H$.
The absolute derivative impulse is therefore dominated by
$B\partial_{g_\infty}h_k$: differentiating the positive resolvent inserts
the dominating perturbation once between two positive impulse filters.
The same argument differentiates its covariance envelope. Hence

$$
|D^{\rm TL}_{2,H,L}-D_{2,H}|\leq F_L,
\qquad
|D^{\rm TL}_{4,H,L}/\beta-D_{4,H}/\beta|
\leq B\,\partial_{g_\infty}F_L.
$$

The second expression means the response per unit $\beta$, including
when a particular kernel has $\beta=0$. The formulas concern expansion
coefficients; neither is a finite-noise transport-error bound.

## What pairing cancels

In the strict global contraction domain, couple both stationary causal
solutions to the same entire innovation history. With common curvature,
their increment expansions have the form

$$
v^{(a)}_n=\varepsilon W_n+\varepsilon^3\beta_a Z_n
 +O_{L^p}(\varepsilon^5).
$$

Here $Z$ is the common cubic response **per unit $\beta$**. Define block
sums $W_b^{[L]}$ and $Z_b^{[L]}$. The paired raw statistic starts at

$$
\frac{|Y_b^{(2)}|^2-|Y_b^{(1)}|^2}{2dL}
=\varepsilon^4(\beta_2-\beta_1)
 \frac{W_b^{[L]}\cdot Z_b^{[L]}}{dL}+O_{L^2}(\varepsilon^6).
$$

This statement is initially for fixed $L$. Independent initial histories
or independent innovations do not give this stationary pathwise
cancellation automatically. Burn-in is a separate issue.

For the corrected estimator the leading statistic on superblock $j$ is

$$
Q_j=\frac{1}{2dL}\left[
 W_{2j}\cdot Z_{2j}+W_{2j+1}\cdot Z_{2j+1}
 +2W_{2j}\cdot Z_{2j+1}+2W_{2j+1}\cdot Z_{2j}
\right],
$$

where the block-sum superscripts are suppressed. With $P=M/2$ superblocks,
its exact stationary sampling variance is

$$
\operatorname{Var}\left(\frac1P\sum_{j=0}^{P-1}Q_j\right)
=\frac{1}{P}\left[
 \operatorname{Var}(Q_0)+2\sum_{j=1}^{P-1}
 \left(1-\frac{j}{P}\right)\operatorname{Cov}(Q_0,Q_j)
\right].
$$

Independent seeds divide this variance by their count $S$. At finite $L$,
each $Q_j$ is a fourth-degree Gaussian polynomial, not a Gaussian quadratic
form. Its covariance needs eighth-order Gaussian moments. Its coordinate
contributions are generally correlated because the cubic force couples
coordinates. For example, independent standard $X_1,X_2$ give
$\operatorname{Cov}(X_1^2|X|^2,X_2^2|X|^2)=32$.
Neither block independence nor an exact finite-$L$ factor $1/d$ is assumed.

## Cubic response in the long-block limit

Write $L_j(n)=\sum_{i=0}^{j-1}W_{n-i}$ and
$C_{jk}(t)=\operatorname{Cov}(L_j(t),L_k(0))$ in one coordinate.
The cubic forcing decomposes into first and third Gaussian chaoses:

$$
|L_j|^2L_j=(d+2)C_{jj}(0)L_j+T_j,
\qquad
\mathbb E[T_j^u(t)T_k^v(0)]
=2(d+2)C_{jk}(t)^3\delta_{uv}.
$$

All correlations of $T_j$ with a linear Gaussian variable vanish.
This is why the third chaos does not enter the first mean correction.
It nevertheless enters the variance. Define its forcing spectrum

$$
\mathcal T=2(d+2)\sum_{t\in\mathbb Z}\sum_{j,k=1}^{H-1}
 w_jw_k C_{jk}(t)^3.
$$

This is nonnegative as a zero-frequency variance; individual summands
may be negative. The calculation retains their signs. Put

$$
\tau=\left(1+g_H\sum_jjw_j\right)^{-1},\quad
g_H=M_Hg_\infty,\quad
\mathcal A=\sum_jjw_j C_{jj}(0).
$$

The limiting joint per-coordinate covariance of block sums divided by
$\sqrt L$ is

$$
\Sigma_{WW}=\tau^2,\qquad
\Sigma_{WZ}=-(d+2)\mathcal A\tau^3,
\qquad
\Sigma_{ZZ}=(d+2)^2\mathcal A^2\tau^4+\tau^2\mathcal T.
$$

The first-chaos response has zero-frequency transfer
$-(d+2)\mathcal A\tau^2$ from the innovations. Filtering the third-chaos
forcing contributes $\tau^2\mathcal T$ and has zero cross spectrum with
the first chaos. The time offset of the forcing does not change these
zero-frequency expressions. In particular,
$\Sigma_{WZ}=D_{4,H}/\beta$, independently matching the earlier Lyapunov
transport-response calculation.

### Why a Gaussian block limit is justified here

At fixed finite $H$, the stable Gaussian lag state is a linear causal
filter with exponentially decreasing influence of a resampled innovation.
Its cubic polynomial forcing has the same exponential dependence bound
in every finite $L^p$, by Gaussian moments and Holder's inequality.
Applying the stable response filter preserves summability, with at most
a polynomial prefactor. Every scalar projection of $(W,Z)$ therefore
has summable physical dependence. The invariance principle in
[Wu (2005), Theorem 3(i), using Theorem 1(i)](https://www.stat.uchicago.edu/~wbwu/papers/0506715102v1.pdf)
extends here by applying its martingale-projection argument componentwise.
The resulting vector martingale differences are stationary and ergodic;
their conditional covariance averages converge, and finite second moments
give the Lindeberg condition. The vector martingale functional limit,
with the negligible approximation remainder, gives the joint Brownian
block limit. Its covariance is the summed covariance above.
This uses the Gaussian-polynomial reference, not a finite-noise Gaussian
closure of the original dynamics.

Moment convergence also needs justification. The normalized block sums
belong to Gaussian chaoses of degrees at most three. Their second moments
are uniformly bounded by summable covariances; the finite-chaos
hypercontractivity bound recorded by
[Nourdin, Peccati and Swan (2013), Proposition 3.4](https://orbi.uliege.be/bitstream/2268/187468/1/NPS-depose-sur-arxiv.pdf)
then bounds any fixed higher moment. Thus their fourth moments are
uniformly integrable. Products used for the variance converge in moment,
not just in distribution. Different non-overlapping blocks and different
coordinates are independent in this joint Gaussian **limit**, not at
finite block length.

### Leading paired variance

For a limiting Gaussian pair $(U,V)$,
$\operatorname{Var}(UV)=\Sigma_{WW}\Sigma_{ZZ}+\Sigma_{WZ}^2$.
Define

$$
R_3=\frac{\mathcal T}{(d+2)^2\mathcal A^2\tau^2}.
$$

Relative to the squared leading kernel contrast, the raw paired mean
has limiting relative variance $(2+R_3)/(dSM)$. The nested two-length
estimator has instead

$$
\frac{5(2+R_3)}{dSM}.
$$

The factor five follows directly by applying the Gaussian product formula
to $Q_j$ on two independent limiting blocks: diagonal products contribute
$2V$ and the two cross products with coefficient two contribute $8V$,
where $V=\Sigma_{WW}\Sigma_{ZZ}+\Sigma_{WZ}^2$.
Division by four and averaging $M/2$ superblocks gives $5V/M$ per
coordinate. It also agrees with the zero-lugsail variance factor in the
literature after converting its larger batch size $b=2L$ to $L$.

The order of this statement matters: take the leading weak-noise
coefficient at fixed sample sizes, then take $L\to\infty$ at fixed even
$M$, and only then increase the block count. No uniform finite-$L$,
finite-noise or joint $L,M$ error bound has been calculated here.
The signal is order $\varepsilon^4$ and the paired standard deviation
is also order $\varepsilon^4$. Smaller noise therefore need not destroy
leading relative precision, unlike an unpaired comparison. Floating-point
cancellation and the finite-noise corrections still require a separate
implementation check; arbitrarily small noise is not a free remedy.

## Fixed-cell deterministic evaluation

The parameters are exactly the reviewed cell: $\alpha=0.01$, $H=600$,
$d=3$, $\eta=0.0010330578512396692$, widths $(1,3)$ and the matched
kernels $(0,26)$ and $(1,35)$. No parameter fit or sampled trajectory is
used. $L=100$ reproduces the proposed design; $L=1000$ is a declared
one-decade-longer analytic diagnostic, not a frozen production choice.

| Elementary $L$ | Raw relative $D_2$ bias | Raw relative $D_4$ bias | Two-length relative $D_2$ bias | Two-length relative $D_4$ bias |
| --- | --- | --- | --- | --- |
| 100 | 0.3717223 | -0.6466784 | 0.0969801 | -0.2149456 |
| 1000 | 0.0494492 | -0.0910663 | $4.4233\,10^{-8}$ | $-4.5511\,10^{-8}$ |

The last column is also the relative bias of the leading kernel contrast.
The conservative coefficient bounds at $L=1000$ are $6.111\,10^{-5}$
absolute for $D_2$, and $202.10$ for $D_4/\beta$, approximately $0.0204\%$
and $0.643\%$ of their respective long-time values. These displayed
bounds are rounded upward; their numerical evaluation is not an interval
certificate. The much smaller direct biases are numerical evaluations
of exact coefficient formulas, not bounds on the full nonlinear process.

The cubic covariance sum gives

$$
\mathcal T\simeq 402678296.5606,\quad
\Sigma_{WZ}\simeq-31479.23556051,\quad
R_3\simeq0.1465419576.
$$

Thus the raw and two-length relative variance factors multiplying
$1/(dSM)$ are $2.1465419576$ and $10.7327097880$ respectively.
Discarding the third chaos would miss about $7.33\%$ of the variance
relative to the first-chaos-only reference. This is a reference factor,
not a claimed significance or a required update budget at $L=1000$.

### Covariance-series truncation

The script uses $C(t)=A^t C$, evaluating $A$ by its common first row
and history shift, and sums through $T=2400$. For $t\geq j$,

$$
|C_{jk}(t)|\leq a r^{t-j} A_j A_k,\qquad
A_j=\frac{1-r^j}{1-r}.
$$

With $K=H-1$ and $T\geq K$, the omitted absolute contribution to
$\mathcal T$ is bounded by

$$
\frac{4(d+2)a^3 r^{3(T+1-K)}}{1-r^3}
\left(\sum_jw_j A_j^3 r^{3(K-j)}\right)
\left(\sum_kw_k A_k^3\right).
$$

It is below $2.841\,10^{-12}$ for this calculation. This tiny number
bounds only the analytic series tail, not floating-point roundoff,
finite-block variance error, horizon error or the nonlinear remainder.
Roundoff is larger than this tail, so the numerical result is not claimed
accurate to twelve absolute decimal places.

## Error Budget and Decision

| Error source | Established here | Still required before a panel |
| --- | --- | --- |
| Finite lag in the mean | Exact coefficient response and conservative two-length tail bounds | Combine with the finite-noise remainder; predeclare the accepted total bias |
| Sampling | Pathwise linear cancellation; long-block reference including third chaos; subsequent conservative finite-sample bound for the leading coefficient | Quantitative transfer to the full finite-noise estimator, including its random remainder |
| Nonlinear transport remainder | Existing asymptotic $O(\varepsilon^6)$ theorem in the strict domain | Usable constant or justified numerical error domain for chosen nonzero noise |
| Memory horizon | Estimand and reference consistently use $H=600$ | A separate transfer bound if an untruncated claim is intended; this note makes no such transfer |
| Initialization | Stationary causal coupling specified | Burn-in error for the actual paired initializer |
| Numerical implementation | Deterministic coefficient checks | Coupling, subtraction, precision and runtime contract for the eventual shared production force |

The original long-time target remains unchanged. The corrected expectation
addresses the estimator mismatch; it does not justify treating the
long-block factor as exact at finite $L$. The follow-up instead bounds
finite-sample coefficient variance conservatively. The next readiness
step is a usable remainder for the full estimator and transport prediction,
followed by an explicit total-error/cost decision. No new
FIFO/P5 evidence, gravity/quantum bridge or publication novelty follows
from this statistical repair.

Reproduction: run [paired_transport.py](../scripts/paired_transport.py).
The [dedicated tests](../scripts/test_paired_transport.py) independently
check the cubic identity by exact Gauss--Hermite quadrature, signed $H=2$
geometric sums, direct matrix powers, tail enclosure, the two-length bias
identity, Gaussian quadratic-form variance, finite-coordinate dependence,
the fixed review cell and invalid domains. These tests check algebra and
implementation, not the general proof or actual nonlinear power.

Local verification on 2026-10-22: 44 new checks pass; the combined run has
163 research checks and 18 frozen-reference/documentation/claim checks,
181 in total. Ruff, formatting and the strict documentation build pass.
The research CI job now includes this dedicated test file. Frozen PDFs,
archived data and production code are unchanged.
