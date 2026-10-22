# External transport-panel review: verified coefficients, unresolved readiness

Date: 2026-10-22. Audit against commit c935fdf and
[PR8 review 5606957081](https://github.com/MemoryDynamics/Knoten/pull/8#pullrequestreview-5606957081),
posted 2026-10-21 at 22:22 UTC. The author referred to this as the Mistral
review; the comment describes itself as a Vibe/GLM second-model review.
It is an external model assessment, not a human referee report. Its
reported independent derivation is distinguished below from calculations
reproduced here.

**Decision:** retain the proposed cell as an unapproved design candidate.
Do not freeze or execute the proposed eight-billion-update panel yet.
The coefficient checks are reproducible, but the proposed estimator and
power calculation do not measure the same quantity. The finite-noise
transport remainder and paired precision remain open. This audit does not
prove that no affordable test exists.

## Findings

| Priority | Finding | Consequence |
| --- | --- | --- |
| P1 | The proposed raw block-MSD at $L=100$ has a 37.17% linear bias relative to the stationary long-time coefficient at $H=600$. | The stated linear-null acceptance rule fails even in its exact reference model. More blocks do not remove this fixed-lag bias. |
| P1 | The leading kernel difference at that block length is only 35.33% of its long-time value. | Common linear bias cancels between matched kernels, but this does not make the nonlinear difference a long-time transport estimator. |
| P1 | A Gaussian weighted fifth-order **force-norm** diagnostic was treated as a bound on the nonlinear **transport** error. | The claimed remainder margin and finite-noise sign robustness do not follow. The stationary law and summed correlations also change. |
| P1 | The proposed decision rule sends every positive contrast to inconclusive. | A statistically resolved opposite sign must be allowed to contradict the scoped prediction once validity and estimator checks pass. Otherwise the test protects the prediction from an adverse outcome. |
| P2 | Independent-kernel sizing omits the $\sqrt2$ difference-error factor and uses the infinite-lag signal with a finite-lag noise scale. Non-overlapping blocks are also correlated. | The corrected linear-Gaussian sizing is about $2.32\sigma$, not $13.5\sigma$. Actual paired-kernel precision needs its own calculation. |

These are design findings, not failures of the underlying weak-noise
coefficient theorem. No nonlinear target trajectories were generated.

## What was reproduced

At $\alpha=0.01$, $q=0.99$, $d=3$, $\varepsilon=0.007$ and

$$
\eta=\frac{\alpha}{2q(1+35/9)}
     =0.0010330578512396692,
$$

the two kernels $(A_r,A_a)=(0,26)$ and $(1,35)$ with widths $(1,3)$
have equal $\kappa=26/9$ and respectively
$\lambda=-13/81$ and $23/81$. Their global contraction budgets are
$0.2954545$ and $0.5$. The reviewed noise does not affect this condition;
passing it establishes the asymptotic expansion, not its accuracy at a
particular nonzero noise.

The untruncated formulas reproduce the review's leading relative
corrections $+0.0893326\%$ and $-0.1580499\%$. Their ratio is $-23/13$.
The review correctly requires the actual finite-$H$ reference:
at $H=600$, $\mu_H=97.3188985054$, versus $\mu_\infty=99$.

The cloud recursion quoted in the review is valid for the normalized
untruncated exponential measure. Its radius relation
$R_Q^2=R_r^2/q$ additionally uses stationary finite second moments.
It is not a pathwise identity or an exact finite-FIFO radius relation.

## Match the observable before calculating power

Write $D_H(\varepsilon)=\varepsilon^2 D_{2,H}
+\varepsilon^4 D_{4,H}+O(\varepsilon^6)$ for long-time transport.
For the reviewed raw block estimator define instead

$$
D_{H,L}(\varepsilon)=
\frac{\mathbb E|x_{n+L}-x_n|^2}{2dL}.
$$

These are distinct expectations, even at stationarity. The exact linear
and leading perturbative coefficients are:

| Quantity | Linear $D_2$ | $D_4$, kernel $(0,26)$ | $D_4$, kernel $(1,35)$ |
| --- | --- | --- | --- |
| Untruncated long time | 0.2979378270 | 5.4317456818 | -9.6100115909 |
| $H=600$, long time | 0.3002590214 | 5.2066863099 | -9.2118296252 |
| $H=600$, $L=100$ block | 0.4118720006 | 1.8396345106 | -3.2547379804 |

Thus $D_{2,H,L}/D_{2,H}-1=0.3717223172$. At the reviewed noise,
the linear block expectation is approximately $2.01817\,10^{-5}$,
not the long-time $1.47127\,10^{-5}$ per coordinate. A null rule
requiring raw block-MSD to agree with the latter within a $0.018\%$
floor cannot pass in the infinite-sample limit.

The block kernel contrast is still negative at leading order, but its
coefficient is only $0.3533215564$ times the long-time contrast.
The $-23/13$ ratio holds for both observables because their first
corrections are proportional to the common cubic-response coefficient.
That ratio alone therefore cannot establish that the long-time
transport limit has been measured.

### Independent calculation

For unit-noise relative lag covariance $C$, transition $A$ and Wick
perturbation $A_1$, use the existing Lyapunov response $C_1$ and

$$
c_k=e_1^T A^k C e_1,\qquad
\dot c_k=e_1^T\left[
 A^k C_1+\sum_{\ell=0}^{k-1}A^\ell A_1 A^{k-1-\ell}C
\right]e_1.
$$

The dot denotes differentiation in $t=\beta\varepsilon^2$,
$\beta=\eta M_H\lambda$, at zero. Then

$$
D_{2,H,L}=\frac{Lc_0+2\sum_{k=1}^{L-1}(L-k)c_k}{2L},\qquad
D_{4,H,L}=\beta\frac{L\dot c_0+
2\sum_{k=1}^{L-1}(L-k)\dot c_k}{2L}.
$$

The new fixed-lag response helper evaluates this recursion. Tests
independently differentiate perturbed matrix-Lyapunov solutions using
a fourth-order difference stencil, including the zero-gain case.
The old linear MSD API returns the unchanged first component.

## Correct the Gaussian sizing calculation

Let $Y_b=x_{(b+1)L}-x_{bL}$ in one coordinate of the **stationary linear
Gaussian reference**. With its unit-noise MSD $m(n)$,

$$
\gamma_0=m(L),\qquad
\gamma_k=\tfrac12[m((k+1)L)+m((k-1)L)-2m(kL)].
$$

For $M=N/L$ blocks per seed and $S$ independent seeds, Wick's identity
$\operatorname{Cov}(Y_0^2,Y_k^2)=2\gamma_k^2$ gives the relative variance
of the coordinate-averaged raw block estimator:

$$
\frac{\operatorname{Var}(\widehat D_{H,L})}{D_{2,H,L}^2}
=\frac{2}{dSM}\left[
1+2\sum_{k=1}^{M-1}\left(1-\frac{k}{M}\right)
\left(\frac{\gamma_k}{\gamma_0}\right)^2\right].
$$

Here unit noise is used; relative variance is unchanged by restoring
$\varepsilon$. The formula assumes independent Gaussian coordinates
and seeds, not independent adjacent blocks. At the reviewed cell:

- adjacent block correlation is $-0.100145$;
- variance inflation over independent blocks is $1.0216084$;
- the single-condition relative standard error is $0.0184536\%$ of
  the **linear block mean**;
- the leading kernel contrast is $-0.0606072\%$ of that same mean;
- independent kernels have difference standard error $\sqrt2$ times
  the single-condition value, giving a sizing ratio $2.32235$.

This is not a significance result from data, a nonlinear precision
guarantee, or a paired-kernel power calculation.

The calculation sums 50 block covariances and bounds the omitted squares.
For the linear absolute impulse envelope, put
$b=q|\eta\kappa|$, $r=q+b<1$ and
$a_h=b(1-qr)/(1-r^2)$. Its positive-lag covariance is $a_h r^{k-1}$.
Consequently

$$
|\gamma_m|\leq J_L r^{(m-1)L},\qquad
J_L=a_h\left(\frac{1-r^L}{1-r}\right)^2,\qquad
\sum_{m>K}\gamma_m^2\leq
\frac{J_L^2 r^{2KL}}{1-r^{2L}}.
$$

At $K=50$ this upper bound is $8.89\,10^{-29}$ in unit-noise covariance
squares (rounded upward). Finite-$H$ signed impulse coefficients are
dominated by this untruncated positive envelope. Floating-point
evaluation is not an interval certificate. A full correlated Gaussian
quadratic-form test independently checks the variance expression.

## What the force diagnostic does and does not show

The finite-$H$ Gaussian reference reproduces weighted fifth-to-cubic
force-norm ratios of $0.1267\%$ and $2.1048\%$. These use

$$
\frac{c_5}{|\lambda|}\varepsilon^2(d+3)
\frac{\sum_j\gamma_j C_{jj}^{5/2}}
     {\sum_j\gamma_j C_{jj}^{3/2}}.
$$

The denominator is a sum of expected cubic force norms, not the norm of
the summed force; cancellations are not controlled by this ratio.
More importantly, the ratio is not the relative error of $D_4$:
it neither changes the Gaussian expectation into the nonlinear invariant
law nor controls the all-lag covariance response. Products of cubic
responses also enter at order $\varepsilon^6$. The existing research note
explicitly separates these issues. The review's inference of a robust
finite-noise transport sign from this diagnostic is unsupported.

## Repair before any panel authorization

Keep the original long-time transport question visible. A finite-lag
contrast can be a secondary test, but must not silently replace it.
An acceptable design must match its analytic prediction to the actual
estimator and bound or expose the remaining long-lag error.

Paired innovations are promising because the common linear contribution
cancels pathwise. The variance of the paired difference, its serial
correlation and its nonlinear remainder must be derived together; the
independent-kernel floor cannot be relabelled as paired precision.
No conclusion of practical impossibility follows from the $2.32$ sizing.

Use an adverse-outcome rule: after validity and estimator checks pass,
a confidence interval incompatible with the allowed negative prediction,
including a resolved positive sign, contradicts the scoped claim.
Insufficient precision or a failed prerequisite is inconclusive.
No supportive sign by itself confirms the magnitude or the expansion.

For a noise-scaling check, specify the normalized observable: changing
$0.005$ to $0.007$ gives factor $1.96$ in a correction normalized by
$\varepsilon^2$, but factor $3.8416$ in the raw quartic correction.
The requested runtime, burn-in and stopping rule still need a validated
implementation contract. Update counts alone do not establish affordability.

## Reproduction and status

Run the deterministic
[review audit script](../scripts/review_transport_audit.py) with the pinned
research environment. It fixes the reviewed cell, evaluates exact
linear covariances and perturbative coefficients, and prints its full
diagnostic record. It performs no parameter scan, sampled trajectory,
production rehearsal or panel authorization.

The new helper and statistical checks are included in the existing
research test file and CI job. Local verification on 2026-10-22:
119 research checks and 18 frozen-reference/documentation/claim checks
pass (137 total), including 17 new fixed-lag and variance checks.
Ruff and the strict documentation build pass. These tests check formulas
and implementation, not the general theorem or actual nonlinear power.
A second-model review has been received
and critically assessed; an independent human mathematical review and
the missing full-text aging-paper comparison are still outstanding.
Frozen PDFs, archived data and FIFO/P5 gates are unchanged.
