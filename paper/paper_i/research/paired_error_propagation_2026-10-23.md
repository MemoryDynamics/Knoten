# Conditional error propagation for the paired residual coordinates

Date: 2026-10-23. Continuation of `077f3b0`. Deterministic numerical
analysis, not new transport data, a whole-simulator certificate or a
production-run authorization. The scientific decision is summarized in
the [Paper-I decision brief](paper_i_decision_brief_2026-10-23.md).

## Result and limits

The [exact split coordinates](paired_residual_precision_2026-10-23.md)
avoid subtracting the common physical linear background. Here a positive
error recursion shows that, inside the strict contraction domain,
bounded local numerical defects need not produce a state error growing
linearly with the total number of updates. The conclusion REQUIRES
validated local defects and bounds on the computed normalized lags.
Neither is supplied by a short high-precision trajectory comparison.

Separately, an explicit balanced binary64 reduction returns an absolute
sum/mean error bound relative to its supplied binary64 inputs. It does
not bound errors already present in those inputs. These two results do
not close the arithmetic part of the finite-noise statistical budget.

## Positive lag-state recursion

Use $j=1,\ldots,H-1$, $\gamma_j=\alpha(1-\alpha)^j$ and the previous
note's lag sums $W_j,R_j$, with $t=\varepsilon^2$. Tildes denote computed
quantities. Let $e^W_j,e^R_j$ bound the Euclidean errors in each lag, and
let $b_j\geq|\widetilde W_j+t\widetilde R_j|$. A local defect $d^W_j$
or $d^R_j$ bounds the difference between the computed next state and the
EXACT split update applied to the computed input state. This definition
includes coefficient evaluation, force evaluation and lag-shift additions;
it is not just the error in the new first increment.

Put

$$
g_\ell=|\eta\kappa|,\qquad
g_f=|\eta|G_2,\qquad
a_3=|\eta|\left(\frac{|A_r|}{2s_r^4}+\frac{|A_a|}{2s_a^4}\right).
$$

The full-force Hessian bound and its Taylor remainder give the componentwise
envelopes, with $e^W_0=e^R_0=0$,

$$
e^{W,+}_j\leq e^W_{j-1}+g_\ell\sum_k\gamma_k e^W_k+d^W_j,
$$

$$
e^{R,+}_j\leq e^R_{j-1}+g_f\sum_k\gamma_k e^R_k
+3a_3\sum_k\gamma_k(b_k+e^W_k)^2e^W_k+d^R_j.
$$

The residual bound preserves an important cancellation. In its force
map first change $R$ at fixed exact $W$, then change $W$ at fixed
computed $\widetilde R$. The first derivative contains

$$
\kappa I+t\,DN_\varepsilon(W+tR)
=\nabla^2K(\varepsilon(W+tR)),
$$

whose norm is at most $G_2$. For the second change,
$\|DN_\varepsilon(u)\|\leq3c_3|u|^2$, where $c_3=a_3/|\eta|$
for nonzero $\eta$, with its amplitude formula defining it also at zero.
The segment's norm is at most $b_k+e^W_k$. Thus this cross term needs
no extra $e^R_k$ and no division by $\varepsilon^2$. The continuous
$\varepsilon=0$ limit obeys the same bounds. The underlying Hessian
estimates are derived in the [validity note](weak_noise_validity_2026-10-21.md).

### Constant-defect envelope

For $(B_gE)_j=E_{j-1}+g\sum_k\gamma_kE_k$, define
$\mu_H=\sum_jj\gamma_j$ and require $g\mu_H<1$. Given nonnegative
defects $d_j$, the exact positive resolvent is

$$
c_j=\sum_{i=1}^j d_i,\qquad
F=\frac{g\sum_j\gamma_jc_j}{1-g\mu_H},\qquad
E_j=c_j+jF.
$$

Direct substitution gives $E=B_gE+d$. Positivity then proves invariance:
initial errors below $E$ and subsequent defects below $d$ stay below $E$.
For completeness, the weighted maximum norm $\max_j|E_j|/j$ gives
$\|B_g\|\leq1-(1-g\mu_H)/(H-1)<1$, since $(B_gj)_j=j-1+g\mu_H$.

For the coupled split map, first compute $E^W$ from $d^W,g_\ell$. If
$B_j$ bounds every computed normalized lag in the period considered, set
$C=3a_3\sum_j\gamma_j(B_j+E^W_j)^2E^W_j$ and compute $E^R$ from
$d^R+C,g_f$. Initial errors must lie inside both envelopes.
Gaussian innovations do NOT have a deterministic bounded support. A
finite-run cap must be justified or monitored under a declared failure
policy; it cannot be inferred for future steps from an observed maximum.
Discarding cap failures would change the sampling protocol. The one-step
recursion also permits a varying envelope without a constant cap.

At the existing candidate $\alpha=0.01,H=600$,
$\eta=0.5\alpha/[q(1+35/9)]$, kernel $(1,35,1,3)$, the deterministic
audit gives:

| Quantity | Floating-point evaluation |
| --- | --- |
| $g_\ell\mu_H$ | 0.2904374841 |
| $g_f\mu_H$ | 0.4915095884 |
| First-lag gain for a unit defect at every lag, linear map | 1.4093190910 |
| First-lag gain for a unit defect at every lag, residual map alone | 1.9666054211 |
| Largest-lag gains for those two uncoupled maps | 844.1821355; 1177.9966472 |

The residual numbers EXCLUDE the cross error from $W$. A unit-defect gain
is not an estimate of the actual local rounding defect. The state-envelope
helpers evaluate real-arithmetic inequalities in ordinary floating point;
they do not outward-enclose coefficients, norms or their own evaluation.

## Transfer to the paired observable

For computed block sums $W,R^a,R^b$ of length $m$, let $E_W,E_a,E_b$
bound their errors, INCLUDING accumulation of the individual increments.
For the exact normalized raw-block expression

$$
f=\frac{2W\cdot(R^b-R^a)+t(|R^b|^2-|R^a|^2)}{2dm},
$$

input perturbation is at most

$$
E_f=\frac{2\{E_W|R^b-R^a|+(|W|+E_W)(E_a+E_b)\}
+t\{2|R^a|E_a+E_a^2+2|R^b|E_b+E_b^2\}}{2dm}.
$$

This follows by expanding the polynomial and applying Cauchy--Schwarz;
it requires no independence between input errors. For one two-length
superblock use $2E_{f,2L}+(E_{f,L,1}+E_{f,L,2})/2$, then average these
bounds. Evaluation of $f$, block-vector sums, the two-length combination
and the final reduction require their own arithmetic bounds. In
particular, a time-uniform state envelope does not make a block sum
automatically exact or uniformly bounded in block length.

## A reduction with an explicit arithmetic contract

The standard pairwise summation model and depth-dependent error bound are
described by [Higham (1993), Sections 1--3, especially Eq. (3.6)](https://nhigham.com/wp-content/uploads/2023/10/high93s.pdf),
inspected on 2026-10-23. The method is not new and does not guarantee small
relative error for strongly cancelling inputs.

`bounded_pairwise_mean` explicitly adds adjacent pairs, carries an odd
last value unchanged, and repeats. For $N$ inputs its maximum tree depth
is $k=\lceil\log_2N\rceil$. Under IEEE binary64 round-to-nearest,
without fast-math/reassociation or underflow/overflow,

$$
|\widehat S-S|\leq\Gamma_k A,\qquad
\Gamma_k=\frac{k u}{1-ku},\quad u=2^{-53},\quad A=\sum_i|x_i|.
$$

The code computes an upward-rounded $\Gamma_k$ from an exact rational.
Applying the same tree to $|x_i|$ gives $\widehat A$ and the upper bound
$A\leq\widehat A/(1-\Gamma_k)$. That quotient and subsequent positive
error arithmetic are rounded outward using `nextafter`. The denominator
is rounded downward. The returned mean-error bound also includes
$\Gamma_1|\widehat S/N|$ for the final division. Counts are at most
$2^{53}$ so their binary64 conversion is exact. All input values,
tree results, mean and bound arithmetic must remain in the checked
normal-or-zero domain; unresolved positive-bound underflow fails closed.
The returned bounds concern the converted binary64 inputs, not any
higher-precision values a caller might have intended.

For a million values $k=20$ and $\Gamma_k<2.23\,10^{-15}$. This
multiplies the ABSOLUTE input sum, not the signed sum. A deliberately
adversarial fixture repeats $[10^{16},1,-10^{16},2,-0.5]$ 200 times:
its exact sum is 500, while this tree returns 400. The absolute bound is
4440.8921 and encloses the actual error 100. The computed mean is 0.4,
not the exact 0.5. This is a valid but uninformative bound, explicitly not
an accuracy success. The tests retain this counterexample.

## Verification and decision

[paired_error_propagation.py](../scripts/paired_error_propagation.py)
and its [52 tests](../scripts/test_paired_error_propagation.py) cover a
dense-matrix resolvent cross-check; positive-recursion invariance; the
linear-to-residual cross error; full Gaussian 100-digit one-step references
at three fixed noise values for both kernels; block-polynomial input
errors; exact-rational binary64 sum/mean comparisons; and rejected domains.
The high-precision tests calculate local defects only for their stated
inputs. They are not uniform library error bounds. Run the deterministic
summary with `python paper/paper_i/scripts/paired_error_propagation.py`
after installing `requirements-research.txt`.

**Remaining contract:** validated per-update defects including weights,
`exprel`, vector reductions and shifts; validated propagation arithmetic;
finite-run lag caps or a monitored varying envelope; block-statistic
evaluation bounds; and a declared innovation-generation contract.
Pathwise comparison for the same supplied innovations does not establish
sampling from the theorem's ideal iid Gaussian law. No numerical tests
here upgrade that assumption to a proof about a finite-state PRNG.

This bounded audit establishes a route for propagation and reduction,
not a cheap complete certificate. The decision brief therefore recommends
assessing the theorem's scientific value before further runner
optimization or billion-update execution. No production code, frozen
manuscript, radius dataset, FIFO or P5 authorization changes follow.

Local verification: all 52 new tests pass without an installed project
package. The combined research, frozen-reference, documentation and
claim suite passes 346 tests. Ruff, formatting and the strict documentation
build pass. The existing target-free Paper-I CI job now includes this
test file; these local results are not a claim about an unobserved CI run.
