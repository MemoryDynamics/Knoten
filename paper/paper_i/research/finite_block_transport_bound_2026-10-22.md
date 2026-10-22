# Finite-block sampling bound for the leading paired transport coefficient

Date: 2026-10-22. Continuation of the
[paired transport reference](paired_transport_feasibility_2026-10-22.md).
Internal derivation and deterministic checks, not an independent human
review. No target trajectories or production benchmarks were generated.

**Result:** the leading paired coefficient now has a conservative variance
bound at finite block length and finite sample count. It allows arbitrary
dependence between nearby blocks and between coordinate products. It does
not use the earlier long-block Gaussian approximation. At the previously
discussed count of 400 million steps per seed and five paired seeds, its
Chebyshev sampling radius is about 8.14% of the long-time coefficient;
adding the conservative coefficient bias gives less than 8.8%.

This is a bound for the stationary Gaussian-polynomial **coefficient
process**, not the full nonlinear estimator at nonzero noise. The missing
step is now quantitative transfer of both mean and sampling error to that
estimator, together with initialization and numerical error. The panel
remains on hold. The mathematical bound is evaluated in ordinary floating
point; numerical roundoff has not been interval-certified.

## Contract

Use the same fixed finite $H$, common innovations and nested two-length
estimator as in the preceding note. Let $P$ be the number of length-$2L$
superblocks per seed, and $S$ the number of independent seeds. The leading
coefficient of the paired difference is

$$
\widehat\Delta^{\rm TL}
=\varepsilon^4\Delta\beta\,\overline Q
 +O_{L^2}(\varepsilon^6),\qquad
\overline Q=\frac1{SP}\sum_{s=1}^S\sum_{j=0}^{P-1}Q_{s,j},
$$

where the expansion is initially at fixed sample sizes. In one superblock,

$$
Q_j=\frac{W_1\cdot Z_1+W_2\cdot Z_2
             +2W_1\cdot Z_2+2W_2\cdot Z_1}{2dL}.
$$

$W_i,Z_i$ are the two length-$L$ block sums of the common linear increment
and the cubic response per unit $\beta$. The target is still
$D_{4,H}^{(2)}-D_{4,H}^{(1)}=\Delta\beta\,m_\infty$, not a newly chosen
short-time observable. The finite-block mean $m_L=\mathbb E Q_j$ and its
bias relative to $m_\infty$ are calculated by the earlier response and
two-length tail formulas. Counts here are mathematical inputs, not a
simulation authorization or a wall-clock cost estimate.

## Block Moments Without a Gaussian Block Approximation

Write $K=H-1$, $w_j=\alpha q^j/(1-q^H)$, $v_j=C_{jj}(0)$ and
$C_{jk}(t)=[A^tC]_{jk}$. The cubic forcing is
$F_n=-\sum_jw_j|L_j(n)|^2L_j(n)$. Its first- and third-chaos
per-coordinate covariance sequences are exactly

$$
\gamma_1(t)=f^T C(t)f,\quad f_j=(d+2)w_jv_j,
\qquad
\gamma_3(t)=2(d+2)\sum_{j,k}w_jw_k C_{jk}(t)^3.
$$

The existing covariance recursion now returns both sequences, retaining
their signs. No Gaussian closure is used. Each chaos is then passed through
the same signed linear response filter $h$:
$Z_n=\sum_{a\geq0}h_a F_{n-1-a}$. The time shift does not change a
stationary block variance.

### Truncation With an Explicit Remainder

For the positive impulse envelope use the preceding notation

$$
b=qg_\infty,\quad r=q+b<1,\quad
\bar h_0=1,\quad\bar h_a=br^{a-1}\ (a\geq1),\quad
a_0=\frac{b(1-qr)}{1-r^2},\quad A_j=\frac{1-r^j}{1-r}.
$$

Truncate the signed filter after $T_h$. Its omitted absolute sum is at
most $e_h=br^{T_h}/(1-r)$. For either forcing chaos, calculate the finite
filtered block variance from its Toeplitz covariance matrix, or equivalently
from the autocorrelation of the convolution of $h_{0:T_h}$ with the
length-$L$ all-ones sequence. This only needs forcing covariances through
$T_h+L-1$.

If $K_a$ bounds $\sum_{t\in\mathbb Z}|\gamma_a(t)|$, then the omitted
filter changes the block standard deviation by at most

$$
e_h\sqrt{L K_a}.
$$

Indeed, every shifted forcing block has variance at most $LK_a$; apply
the $L^2$ triangle inequality to the omitted signed filter. Squaring
$\sqrt{V_a^{\rm trunc}}\pm e_h\sqrt{LK_a}$, with the lower endpoint
clipped at zero before squaring, brackets the true block variance $V_a$.

For completeness, when $T\geq K$, the first-chaos omitted absolute
covariance sum is bounded by

$$
\frac{2a_0r^{T+1-K}}{1-r}
 \left(\sum_j f_j A_jr^{K-j}\right)
 \left(\sum_j f_j A_j\right).
$$

The third-chaos tail is the cubic bound already derived in the preceding
note. Add these tails to $\gamma_a(0)+2\sum_{t=1}^T|\gamma_a(t)|$ to
obtain $K_a$. These are bounds on mathematical truncation, not roundoff.

### A Fourth-Moment Bound for One Superblock

Let $s_W^2$ be the exact per-coordinate variance of a length-$L$ linear
block, and let $V_1^+,V_3^+$ be the preceding variance upper bounds.
With $m_4=[d(d+2)]^{1/4}$, define

$$
W_4=m_4s_W,\qquad
Z_4=m_4\sqrt{V_1^+}+\sqrt d\,3^{3/2}\sqrt{V_3^+}.
$$

These bound the $L^4$ norms of the Euclidean block norms. The first chaos
is an isotropic Gaussian vector. For the third chaos, apply the scalar
bound $\|T\|_4\leq3^{3/2}\|T\|_2$ to each coordinate and then use
Minkowski on the sum of squared coordinates. This does **not** assume
coordinate independence. The explicit homogeneous-chaos constant is
recorded in
[Douissi, Es-Sebaiy and Viens (2019), Section 2.3, Eq. (2.3) and the following paragraph](https://alea.math.cnrs.fr/articles/v16/16-23.pdf).
Only this standard moment inequality is used from that paper, not its
Gaussian-estimation limit theorems.

Holder and the six weighted products defining $Q_j$ imply

$$
\|Q_j\|_2\leq A_Q:=\frac{3W_4Z_4}{dL},\qquad
\operatorname{Var}(Q_j)\leq V_Q:=A_Q^2-m_L^2.
$$

This sacrifices sharpness to obtain an actual upper bound at finite $L$.

## Dependence Between Superblocks

Place the last innovation used by $Q_0$ at time zero. Replace the entire
past through zero by an independent copy, keeping future innovations
unchanged; stars denote this coupled process. Then $Q_\ell^*$ is independent
of $Q_0$, with the same marginal law as $Q_\ell$. Therefore

$$
|\operatorname{Cov}(Q_0,Q_\ell)|
\leq\sqrt{V_Q}\,\|Q_\ell-Q_\ell^*\|_2.
$$

There is no claim that the actual $Q_\ell$ are independent. For nearby
blocks we simply use $|\operatorname{Cov}(Q_0,Q_\ell)|\leq V_Q$.

### Explicit Remote Coupling

Put $u=b\sqrt{2/(1-r^2)}$ and
$m_{12}^3=[\prod_{i=0}^5(d+2i)]^{1/4}$. The Gaussian past replacement
gives, per coordinate, a standard-deviation difference for $W_n$ bounded
by $ur^{n-1}$ for $n\geq1$. Consequently, for $n\geq K$,

$$
\|F_n-F_n^*\|_4\leq D_F r^{n-K},\qquad
D_F=3m_{12}^3u\sum_j w_jv_j A_jr^{K-j}.
$$

For all earlier times use the bound
$B_F=2m_{12}^3\sum_jw_jv_j^{3/2}$.
The cubic estimate follows from
$\||x|^2x-|y|^2y\|\leq(|x|^2+|x||y|+|y|^2)|x-y|$
and Holder with twelfth moments. The lag-difference Gaussian norm is
bounded using the impulse envelope; no independence between that
difference and the lag vector is needed.

Convolving these bounds with $\bar h$ gives, for $n\geq K+1$ and
$N=n-1-K$,

$$
\|Z_n-Z_n^*\|_4\leq r^N(C_0+C_1N),\qquad
C_0=D_F+\frac{bB_F}{1-r},\qquad C_1=\frac{bD_F}{r}.
$$

The term proportional to $N$ is necessary: both response and forcing
carry a memory tail. Dropping it would not give the stated bound.

For a length-$L$ block starting at $n$, sum these increment bounds. With
$B_L=\sum_{i=0}^{L-1}ir^i$, the bounds are

$$
\|\delta W^{[L]}\|_4\leq m_4u A_Lr^{n-1},\qquad
\|\delta Z^{[L]}\|_4\leq
 r^N[C_0A_L+C_1(NA_L+B_L)].
$$

Use $J=\lceil K/(2L)\rceil$ nearby superblock lags without decay.
Every remaining lag $\ell>J$ starts at $n=2(\ell-1)L+1\geq K+1$.
Summing over both blocks of each remote superblock gives closed geometric
series. Set $p=r^L$, $x=p^2$, $N_0=2LJ-K$ and

$$
U_Z=(1+p)(C_0A_L+C_1B_L)+pC_1LA_L,\qquad
V_Z=(1+p)C_1A_L.
$$

Then the sums of the two block-difference bounds over all remote lags are

$$
T_W=\frac{m_4u A_L(1+p)r^{2LJ}}{1-x},\qquad
T_Z=r^{N_0}\left[
 \frac{U_Z+V_ZN_0}{1-x}+
 \frac{2LV_Zx}{(1-x)^2}\right].
$$

Applying Holder to differences of the six products in $Q$ yields

$$
\sum_{\ell>J}\|Q_\ell-Q_\ell^*\|_2
\leq R_Q:=\frac{3}{2dL}(Z_4T_W+W_4T_Z).
$$

The factor $1/2$ is retained here because $T_W,T_Z$ already sum both
elementary blocks. This coupling calculation includes correlations between
successive superblocks, rather than assigning an effective sample count.

## Finite-Sample Variance and Coverage

Let $J_P=\min(J,P-1)$. The exact stationary variance identity, Cauchy
bounds for nearby lags and the remote coupling bound imply

$$
\operatorname{Var}(\overline Q)\leq\mathcal V_{P,S}:=
\frac{1}{SP}\left[
 \left(1+2J_P-\frac{J_P(J_P+1)}{P}\right)V_Q
 +2\sqrt{V_Q}R_Q\,\mathbf1_{P>J+1}
\right].
$$

Only the seed average uses independence. In the remote tail, finite-sample
weights bounded by one have been discarded conservatively. Chebyshev
then gives the finite-sample statement

$$
\Pr\left(|\overline Q-m_L|\geq
 \sqrt{\mathcal V_{P,S}/\delta}\right)\leq\delta.
$$

Add the deterministic bound on $|m_L-m_\infty|$ to target the long-time
coefficient. Neither a Gaussian confidence approximation nor a limit in
$L$ or $P$ is needed. This controls a **reference-coefficient statistic**;
it does not convert the original nonlinear trajectories into that process.

## Fixed-Cell Calculation

The model parameters and $L=1000$ diagnostic are unchanged from the
preceding note. Use $P=200000$, $S=5$, hence 400 million steps per seed,
as in the reviewed count. The filter cutoff is $T_h=2400$, and forcing
covariances are evaluated through lag 3399.

| Quantity | Deterministic evaluation |
| --- | --- |
| Linear block variance per coordinate | 630.21315097 |
| First-chaos cubic-response block variance upper bound | $1.5205720\,10^{12}$ |
| Third-chaos cubic-response block variance upper bound | $2.2825749\,10^{11}$ |
| $m_L$ | approximately -31479.23412787 |
| $m_\infty$ | approximately -31479.23556051 |
| Nearby covariance lags retained without decay | 1 |
| $R_Q$ | less than 3.783738 |
| $\mathcal V_{P,S}$ | less than 328350 |
| Sampling standard-deviation bound, divided by $|m_\infty|$ | less than 1.821% |
| Chebyshev radius at $\delta=0.05$, same normalization | less than 8.141% |
| Additional conservative finite-lag coefficient bias | less than 0.643% |

The displayed upper bounds are rounded upward from the floating-point
calculation. The omitted filter absolute sum is below $1.791\,10^{-8}$;
its two block standard-deviation error bounds are about 0.0298 and 0.0114.
The forcing first-chaos omitted covariance sum is about 0.309 and the
third-chaos one below $1.781\,10^{-21}$. These numerical truncation bounds
are included; interval rounding is not.

At the level of the analytic reference, sampling plus the conservative
block bias therefore has a relative radius below 8.8% at 95% coverage.
This is not a measured confidence interval, an estimate of actual variance,
or an 8.8% error bound for the proposed $\varepsilon=0.007$ experiment.
The latter noise has deliberately not entered this reference calculation.
Two paired kernels would already require four billion updates at these
counts; controls add cost. Runtime and numerical reliability have not been
benchmarked or authorized.

## Countercheck and Remaining Gate

For $H=2$, zero curvature and one-dimensional unit-noise increments,
$W_n=\xi_n$ and $Z_n=-w_1\xi_{n-1}^3$. At $L=1$ exact Gaussian moments
give $\operatorname{Var}(Q_j)=118.5w_1^2$ and zero adjacent covariance.
The long-block variance would be $60w_1^2$ per superblock. Thus even this
simple example is almost a factor two away from the limiting variance;
the preceding long-block formula must not be used as an exact finite-$L$
power formula. Five-point Gauss--Hermite quadrature reproduces this
countercheck exactly for the relevant polynomial degrees.

The new bound bypasses that approximation rather than proving it accurate.
It closes a conservative finite-sample sampling bound for the leading
coefficient. Remaining requirements are:

- An explicit finite-noise bound for the normalized paired estimator's
  remainder, controlling its random error as well as its mean. A bound
  on $D_H$ alone does not automatically transfer this sampling guarantee.
- A compatible finite-noise transport remainder for the scientific
  long-time prediction and a stationary-to-initialized coupling bound.
- A declared total-error allocation, numerical precision/cost check,
  novelty comparison and author-approved prospective protocol.

There is no new statement about FIFO orbit transfer, formation, gravity,
quantum mechanics or publication novelty. The methods used here are
standard covariance, coupling and Gaussian-moment tools. Their role is
to prevent a spurious transport validation of the proposed Paper-I result.

Reproduce with [finite_block_transport.py](../scripts/finite_block_transport.py).
The [tests](../scripts/test_finite_block_transport.py) compare Toeplitz
quadratic forms, exact $H=2$ two-state covariance solutions, independently
summed coupling tails, finite-sample covariance weights, exact polynomial
quadrature, the fixed comparison cell and invalid domains. They do not
constitute an independent review of the general derivation.

Local verification on 2026-10-22: 34 new checks pass. The combined run
passes 197 research checks and 18 frozen-reference/documentation/claim
checks, 215 in total. Ruff, formatting and the strict documentation build
pass. The research CI job includes the new test file. Frozen manuscripts,
archived data and production code remain unchanged.
