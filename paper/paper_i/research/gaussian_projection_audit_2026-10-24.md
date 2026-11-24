# The transport coefficient and Gaussian statistical linearization

Date: 2026-10-24. Internal novelty countercheck against `1280c42`, not
a new model, parameter panel or external referee report. The question is
whether the proposed kernel-sensitive transport coefficient distinguishes
our calculation from an established Gaussian approximation.

**Result:** it does not, at order $\varepsilon^4$. Gaussian statistical
linearization reproduces the entire coefficient, not just its sign. The
possible added value is the controlled asymptotic validity and treatment
of memory and long-time limits, whose significance still needs assessment.
This is not proof that our exact model theorem was previously published.

## Primary-source boundary

| Source and material checked | Supported statement | Not established by that source |
| --- | --- | --- |
| [Caughey, Equivalent Linearization Techniques (1963), Caltech institutional record](https://authors.library.caltech.edu/records/f23pf-p3a49) | Equivalent linearization for randomly excited nonlinear dynamics is longstanding. | The PDF download failed; no equation-level claim is attributed to this unread full text. |
| [Katayama, Equivalent Linearization Kalman Filter with Application to Cubic Sensor Problems (ECC 2013), Section III, Proposition 1, Eq. (11), Table I](https://skoge.folk.ntnu.no/prost/proceedings/ecc-2013/data/papers/0306.pdf) | For a Gaussian input the optimal linear gain is the expected Jacobian; a cubic example retains cross-covariance but loses output variance under linear projection. | This filtering paper does not prove our stationary memory-transport expansion. |
| [Bernard and Wu, Stochastic linearization: the theory (1998), publisher abstract](https://doi.org/10.1239/jap/1032265219) | The authors report rigorous linearization principles using entropy and large deviations. | The full theorem assumptions and their relation to our small-noise limit have not been inspected. A generic claim to the first rigorous justification would already be inappropriate. |

The first two sources were rechecked on 2026-10-24; the Bernard--Wu
abstract was inspected in the preceding 2026-10-23/24 research session.
Below is our explicit specialization of the established projection,
not an assertion that these papers contain this particular kernel formula.

## Exact Gaussian force projection

Let $U\sim\mathcal N(0,vI_d)$ with $v>0$, and use the two-Gaussian
kernel of the [validity note](weak_noise_validity_2026-10-21.md).
Minimizing $\mathbb E|\nabla K(U)-BU|^2$ over matrices gives

$$
B=\mathbb E[\nabla K(U)U^T]/v
=\mathbb E[\nabla^2K(U)]=b_K(v)I_d.
$$

There is no intercept because the force is odd and $U$ is centered.
For one Gaussian factor,

$$
\frac1v\mathbb E\left[U_i^2
e^{-|U|^2/(2s^2)}\right]
=\left(1+\frac v{s^2}\right)^{-d/2-1}.
$$

The integral separates into the $i$-coordinate second moment and
$d-1$ zeroth moments. Therefore the exact regression gain is

$$
b_K(v)=\frac{A_a}{s_a^2}\left(1+\frac v{s_a^2}\right)^{-d/2-1}
-\frac{A_r}{s_r^2}\left(1+\frac v{s_r^2}\right)^{-d/2-1},
$$

and, as $v\downarrow0$,

$$
b_K(v)=\kappa+(d+2)\lambda v+O(v^2).
$$

The zero-variance value is defined by continuity. This formula uses a
Gaussian INPUT distribution; it does not assert that the nonlinear
stationary distribution is Gaussian.

Lag independence is unnecessary. For a jointly Gaussian history
$U=(U_1,\ldots,U_{H-1})$, the regression of
$-\eta\sum_j\gamma_j\nabla K(U_j)$ on the whole history has block
coefficients $-\eta\gamma_j b_K(v_j)I_d$. The expected-Jacobian formula
already accounts for the off-diagonal lag covariance. Dropping those
covariances before regression would be a different, unjustified step.

## Comparison with the existing transport calculation

Set $t=\varepsilon^2$, and let $C_{jj}^{(H)}$ be the per-coordinate
unit-noise variance of the linearly predicted lag. A Gaussian surrogate
evaluated at $v_j=tC_{jj}^{(H)}$ replaces the lag force gains by

$$
\eta\gamma_j\kappa\longmapsto
\eta\gamma_j b_K(tC_{jj}^{(H)})
=\eta\gamma_j\kappa
+t\eta\gamma_j\lambda(d+2)C_{jj}^{(H)}+O(t^2).
$$

For a stable linear lag-feedback process, the diffusion coefficient per
unit innovation variance is its squared zero-frequency transfer divided
by two. Thus the frozen-covariance surrogate gives

$$
D^{\rm G}_H(\varepsilon)=
\frac{\varepsilon^2}
{2\left[1+\eta\sum_jj\gamma_j
b_K(\varepsilon^2 C_{jj}^{(H)})\right]^2}.
$$

Expanding the denominator, with the previous definitions of $\mu_H,S_H$,

$$
D^{\rm G}_H(\varepsilon)=
\frac{\varepsilon^2}{2(1+\eta\kappa\mu_H)^2}
-\varepsilon^4\frac{\eta\lambda(d+2)S_H}
{(1+\eta\kappa\mu_H)^3}+O(\varepsilon^6).
$$

This is exactly our $D_2,D_4$. No nonlinear data fit is needed for either
route. If a smooth self-consistent Gaussian branch instead uses
$C_{jj}(t)=C_{jj}(0)+O(t)$, it gives the same first correction, since
$tC_{jj}(t)=tC_{jj}(0)+O(t^2)$. This conditional statement does not
prove existence or uniqueness of that closure branch.

For $H=\infty$, the coefficient comparison remains justified in the
existing strict domain: $C_{jj}\leq j^2\|w_0\|_2^2$, and both
$\sum_j j\gamma_j C_{jj}$ and $\sum_j j\gamma_j C_{jj}^2$ converge.
The first two derivatives of $b_K$ are bounded for $v\geq0$. These
facts justify the expansion of the age sum. They do not replace the
separate summable-remainder proof for the ACTUAL nonlinear process.

For the matched-curvature pair this includes the ratio $-23/13$ and
the opposite signs relative to the common linear reference. Measuring
that mean coefficient would test the full-model prediction against the
uncorrected linear model, but would not distinguish it from this known
approximation at that order.

## Why this is not an exact linear reduction

For the cubic force write

$$
|U|^2U=(d+2)vU+Q_3(U),\qquad
\mathbb E[Q_3(U)U^T]=0.
$$

The nonzero remainder is a third Gaussian-chaos component. Its exact
energy is

$$
\mathbb E|Q_3(U)|^2
=d(d+2)(d+4)v^3-d(d+2)^2v^3
=2d(d+2)v^3.
$$

It is orthogonal to every jointly Gaussian linear observable, including
linear observables at other times. This explains why it drops out of
the first transport cross term. It does not vanish from the force or
from quadratic functions of the response. The existing
[paired-variance calculation](paired_transport_feasibility_2026-10-22.md)
already retains its contribution. Agreement of $D_4$ therefore proves
neither exact Gaussian dynamics nor correctness of a Gaussian-only
sampling-variance estimate. No higher-order transport coefficient is
claimed or automatically commissioned here.

## Deterministic checks and consequence

Thirty-two added cases in
[test_weak_nonlinearity.py](../scripts/test_weak_nonlinearity.py) check:

- the closed gain against an independent radial Gaussian integral at
  variances 0.02 and 0.7, dimensions 1, 3, 7 and both fixed kernels;
- joint regression at positive and negative lag correlations using
  tensor Gauss--Hermite quadrature, without diagonalizing away covariance;
- the derivative of the full projected linear transfer, using a complex
  step, against the existing perturbative matrix response at $H=2,7,21$,
  dimensions 1, 3 and both kernels;
- the nonzero cubic residual energy and its zero linear covariance using
  polynomial-exact Gauss--Hermite quadrature at two variances in dimensions
  1, 2, 3.

These are algebraic/numerical cross-checks of the specialization, not
sampled target trajectories, independent proof review or evidence of
stationary Gaussianity. No production helper or force law was replaced.

**Decision update:** a sign-only or $D_4$-mean-only demonstration cannot
carry an argument for a new mechanism beyond established Gaussian
statistical linearization. The [discussion brief](paper_i_decision_brief_2026-10-23.md)
must explicitly ask whether the controlled validity domain, long-time
interchange and untruncated-memory treatment add enough to justify the
paper. Their own overlap with rigorous approximation theory remains open.
Do not respond by automatically calculating $D_6$, adding a model rule,
or spending billions of updates. The missing aging full text and human
assessment remain explicit gaps; neither blocks this narrower negative
comparison. No inference toward quantum theory or gravity follows.

Verification on 2026-10-24: the 32 added cases pass standalone without
an installed project package. The combined research, frozen-reference,
documentation and claim checks pass 378 tests. Ruff, formatting and the
strict documentation build pass. The existing target-free CI test command
already includes the expanded test file. The preceding `1280c42` commit's
Paper-I and general repository CI jobs have completed successfully; that
does not pre-report the outcome of the next commit's CI.
