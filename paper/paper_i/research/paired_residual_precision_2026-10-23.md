# Exact residual coordinates for the paired transport test

Date: 2026-10-23. Continuation of `fcdf94c`. Target-free algebra and
precision checks, not stationary transport data or a production release.
The [finite-noise budget](finite_noise_transport_budget_2026-10-23.md)
made the leading contrast about a billion times smaller than its common
linear background at the sufficient interval's upper endpoint. This note
tests whether subtracting that background is an avoidable numerical loss.

## Exact force and state transformation

For $K(u)=A_r e^{-|u|^2/(2s_r^2)}-A_a e^{-|u|^2/(2s_a^2)}$, put
$\kappa=A_a/s_a^2-A_r/s_r^2$, $t=\varepsilon^2$, and
$E(x)=\operatorname{exprel}(x)=(e^x-1)/x$ with $E(0)=1$. Define

$$
N_\varepsilon(u)=|u|^2u\left[
\frac{A_r}{2s_r^4}E\!\left(-\frac{t|u|^2}{2s_r^2}\right)
-\frac{A_a}{2s_a^4}E\!\left(-\frac{t|u|^2}{2s_a^2}\right)\right].
$$

The identity
$\nabla K(\varepsilon u)=\varepsilon\kappa u+
\varepsilon^3N_\varepsilon(u)$ is exact. At zero noise
$N_0(u)=\lambda|u|^2u$; positive noise uses the full exponentials, not a
cubic approximation. The reference implementation uses
[SciPy's cancellation-aware `exprel`](https://docs.scipy.org/doc/scipy-1.16.2/reference/generated/scipy.special.exprel.html),
whose documentation was inspected on 2026-10-23; the tested dependency is
SciPy 1.16.3. This elementary rescaling is not a novelty claim.

For matched-curvature kernels $a$, use the SAME linear increments $W_n$
and define $v_n^a=\varepsilon W_n+\varepsilon^3R_n^a$. Let $W_{j,n}$
and $R^a_{j,n}$ denote their $j$-increment lag sums. The exact recurrences
are

$$
W_{n+1}=\xi_{n+1}-\eta\kappa\sum_{j=1}^{H-1}\gamma_jW_{j,n},
$$

$$
R^a_{n+1}=-\eta\kappa\sum_{j=1}^{H-1}\gamma_jR^a_{j,n}
-\eta\sum_{j=1}^{H-1}\gamma_j
N^a_\varepsilon(W_{j,n}+tR^a_{j,n}).
$$

Update the lag sums by $W_{1,n+1}=W_{n+1}$ and
$W_{j,n+1}=W_{n+1}+W_{j-1,n}$ for $j\geq2$, and likewise for $R$.
All $\gamma_j=\alpha(1-\alpha)^j$ are present from the first update;
they are not renormalized at finite $H$. Zero initial lag arrays represent
a full memory of coincident points. Arbitrary consistent nonzero lag
histories are also covered by the identity. This is a coordinate change
of the existing force law, not a new dynamics or an empty-memory start.
The code's floating curvature equality check is not a symbolic proof for
arbitrary parameters; the fixed pair has the exact common $\kappa=26/9$.

## Exact paired observable

Let $W_b,R^a_b$ be vector sums in one block of $m$ increments, and set
$\delta R_b=R_b^2-R_b^1$, $\Sigma R_b=R_b^2+R_b^1$. Then

$$
\frac{|Y_b^2|^2-|Y_b^1|^2}{2dm\varepsilon^4}
=\frac{2W_b\cdot\delta R_b+t\,\delta R_b\cdot\Sigma R_b}{2dm}.
$$

The right side does not subtract two $O(\varepsilon^2)$ squared
displacements to recover an $O(\varepsilon^4)$ difference. Apply it to
adjacent length-$L$ blocks and their sums for $2\widehat D_{2L}-\widehat
D_L$. The estimator is unchanged, including its finite-noise term.
At $\varepsilon=0$ the code returns the continuous response limit,
not a physical zero-noise diffusion measurement. Statistical uncertainty
and nonlinearity bounds still come from the preceding notes; this
algebra alone proves no coverage or signal detection.

## Independent numerical checks

[paired_residual_precision.py](../scripts/paired_residual_precision.py)
has two distinct implementations: binary64 lag updates in split
coordinates, and a direct absolute-position history recurrence using
the full Gaussian gradients at 80 and 110 decimal digits. The latter
does not call `exprel` or the split update. It subtracts its linear
reference or physical squared displacements only at high precision.
The 80/110 comparisons are made before conversion to binary64.

The small-history fixture uses $H=5$, $d=3$, $\alpha=0.25$, $\eta=0.02$,
48 deterministic innovation vectors
$\xi_{n,c}=((17n+5c)\bmod13-6)/8$, and $L=4$. They are not sampled
from a Gaussian law. The four noise values were fixed as arithmetic
stress cases; none is selected by a transport outcome. Errors below are
$\max|\mathrm{computed}-\mathrm{reference}|/\max|\mathrm{reference}|$
over the six superblocks, not a coordinatewise relative-error guarantee.

| $\varepsilon$ | Split paired-statistic error | Error after rounding physical increments first |
| --- | --- | --- |
| $10^{-12}$ | $3.49\,10^{-16}$ | 1.0; contrast erased |
| $4.4\,10^{-6}$ | $2.62\,10^{-16}$ | 0.00723 |
| 0.007 | $2.62\,10^{-16}$ | $1.40\,10^{-9}$ |
| 0.2 | $6.24\,10^{-16}$ | $2.39\,10^{-12}$ |

The split residual-increment error is below $4.4\,10^{-16}$ in these
fixtures. The relative 80/110 differences for both residuals and paired
statistics are below $4.5\,10^{-55}$ across these cases. The second
column is not a full-runtime bound. The last column rounds exact
high-precision physical increments before summation/subtraction; it is
not a benchmark of every possible native trajectory implementation.

A separate single-step check uses $H=600$, $d=3$, $\alpha=0.01$ and the
previously discussed weak coupling, with an explicitly constructed
nonzero lag state. It compares the full-force physical update to the
split residual update at $\varepsilon=10^{-12},4.4\,10^{-6},0.007$.
Residual-increment relative errors are below $2.0\,10^{-15}$; 80/110
differences are below $1.2\,10^{-56}$. This is one arbitrary state, not
an equilibrium sample, long trajectory or stationary transport test.

The [tests](../scripts/test_paired_residual_precision.py) additionally
check the force against a direct 100-digit expression and the existing
production gradient, nonzero-history shift order, canonical mass versus
incorrect renormalization, zero-feedback and identical-kernel nulls,
reflection/coordinate permutation, exact square-difference factors,
the cubic limit and invalid domains. In particular, preserving an
arbitrarily chosen nonzero history guards against only testing a trivial
zero-state update.

## Cost measurement and remaining gate

On 2026-10-23, the unoptimized reference code was measured by five groups
of 500 evaluations of the SAME unchanged $H=600$, $d=3$ state, with two
kernels per call. Outputs were discarded, never fed into another update.
This was a microbenchmark, not 2500 trajectory steps. Environment:
Windows, Python 3.12.14, NumPy 2.3.5, SciPy 1.16.3, one BLAS thread.
Times per paired call were approximately
$0.263,0.259,0.255,0.271,0.261$ ms; median $0.261$ ms.

The previously discussed count is **two billion paired updates**
($5\times400$ million), equivalently four billion kernel updates before
controls. Naively multiplying that count by this median gives about
145 serial hours. This excludes RNG, estimator accumulation and output,
but includes Python validation, array allocations and repeated weight
construction. It is neither a lower/upper bound nor a forecast for an
optimized implementation; parallel execution has not been benchmarked.
The existing eight-billion-kernel-update proposal remains unauthorized.

**Decision:** the small signal is not by itself a numerical no-go.
An exact cancellation-safe representation passes the declared controls,
so high-precision arithmetic for every production step is not established
as necessary. Conversely, a one-step/small-history check does not certify
errors accumulated across billions of steps. A bounded accumulation and
summation check, a practical cost decision and the scientific novelty
assessment are still required. Any optimized backend must preserve the
full force and be checked against this independent reference; do not
replace it silently by the cubic response to make a faster test.

Reproduce the fixed precision checks with
`python paper/paper_i/scripts/paired_residual_precision.py`.
The optional `benchmark_split_step()` function repeats only fixed-state
calls; its times are machine/load dependent and excluded from test pass
criteria. No radius data, manuscript PDFs or production code were changed.
These numerical checks supply no evidence for interactions, quantum
mechanics, gravity or publication novelty.

Local verification on 2026-10-23: 33 new checks pass, including standalone
execution without an installed project package. The combined run passes
276 research checks and 18 frozen-reference/documentation/claim checks,
294 total. Ruff, formatting and the strict documentation build pass.
The research dependency list now pins mpmath 1.3.0, and the target-free
CI job includes this test file. The preceding `fcdf94c` commit's Paper-I
and general repository CI jobs have all completed successfully.
