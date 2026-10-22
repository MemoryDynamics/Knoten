# Paper I: PRE reassessment and local nonlinear prediction

Date: 2026-10-19. Internal research assessment, not an external referee report.
The canonical work order is in the
[project priorities](../../../docs/status/project_priorities.md).

## Decision

The 2026-10-09 manuscript is a technically closed, reproducible baseline,
not yet a persuasive PRE submission. The
[journal criteria](https://journals.aps.org/pre/about) require a substantive,
significant addition to knowledge. Correct RMS definitions, a linear
variance calculation and agreement deep in a Taylor regime do not by
themselves establish that addition. This is an editorial assessment, not
an acceptance prediction.

The candidate physical question is narrower than a new localization
mechanism: **when does equality of local kernel curvature cease to predict
the same relative cloud and transport, and can that failure be predicted
without fitting the nonlinear data?** The candidate has not passed a
complete novelty review or a prospective numerical test.

## Source and claim ledger

Initial sources checked on 2026-10-19; the additions below are dated
2026-10-21. A source-reported theorem is not an
independent reproduction. Absence of a result from this ledger is not
proof that it is absent from the literature.

| Source and inspected material | Verified overlap / source-reported result | Scope and consequence for this paper |
| --- | --- | --- |
| [Grima, PRL 95, 128103 (2005), author manuscript v2](https://arxiv.org/pdf/q-bio/0505004), Eqs. (1)--(3), (8), Fig. 1 | Deposited, diffusing and decaying chemical field coupled back to a noisy trajectory; approximate renormalized diffusion with inverse-square coupling dependence. | The derivation has explicit scale assumptions. Its field model is not our fixed spatial kernel. Nevertheless, reduced diffusion without self-localization is already an established physical story, not our new mechanism. |
| [Milisic, Meunier and Roux, SSRN 6659876](https://doi.org/10.2139/ssrn.6659876), abstract; [CIRM author talk description](https://www.carmin.tv/en/video/self-interacting-diffusions-with-aging) | Linear attraction/repulsion to history with aging; long-time regimes depending on the memory kernel and an explicit exponential-memory case. | Closest linear competitor. The full 22-page manuscript was not retrieved; exact coefficient and discretization equivalence remain unresolved. Abstract-level evidence is sufficient to reject a broad novelty claim, not to declare theorem-by-theorem equivalence. |
| [Du, Ren, Suciu and Wang, arXiv:2311.11428v3](https://arxiv.org/html/2311.11428v3), Eq. (4), Assumption 1 and Example 1; [journal record](https://doi.org/10.1016/j.matpur.2025.103782) | The same continuous-time architecture of a trajectory and exponentially weighted occupation measure is explicit; contractivity and stationary measures are proved under stated drift conditions. | Their uniform large-distance restoring assumption does not follow from our bounded Gaussian interaction alone. Do not import their absolute ergodicity theorem into our unpinned translation-invariant model. The architecture and Markov augmentation are not new here. |
| [Sarkar, PRE 112, 054111 (2025)](https://journals.aps.org/pre/pdf/10.1103/t7nk-4p57), Secs. II B--C, Eqs. (1)--(3) | A noisy particle writes a fading Gaussian scalar imprint and responds to its gradient; the paper reports structured motion. | Particularly close topical precedent, absent from the frozen bibliography. Its equations include both a convolutional field source and intrinsic velocity memory. These extra temporal filters cannot be silently removed to declare identical models. Its coherence/energy interpretations are source-reported, not adopted or reproduced here. |
| [Kopp and Klapp, arXiv:2210.03182v3](https://arxiv.org/pdf/2210.03182), Secs. II--III, Eqs. (1)--(5) | Overdamped Brownian motion with a nonlinear finite-range Gaussian force depending on a delayed position; linearization is explicitly separated from nonlinear behavior. | A single discrete delay and repulsive feedback differ from our distributed, net-attractive history. Nonlinear Gaussian memory feedback and comparing its linear/nonlinear transport are nevertheless not new categories. |
| [Newman and Grima, PRE 70, 051916 (2004), author-uploaded full text](https://www.researchgate.net/publication/8128610_Many-body_theory_of_chemotactic_cell-cell_interactions), abstract, Sec. II and Sec. V inspected 2026-10-21 | Langevin chemotaxis with a diffusing, decaying field; explicit coupling-perturbation corrections to diffusion, including a second-order calculation in one dimension. | Perturbatively corrected memory-mediated diffusion is not a new category either. Their expansion parameter is chemotactic coupling, not our noise amplitude. The age-dependent heat kernel is not our fixed-width Gaussian mixture; no coefficient identity follows without a model and limit mapping. |

On 2026-10-21 the Kopp--Klapp comparison was extended to Sec. IV,
Eqs. (19)--(22): their analytical transport estimate expands in small
delay and uses the Hessian at zero. This is a different asymptotic limit
from fixed-memory weak noise, but does not establish novelty of our
coefficient. Newman--Grima's Sec. V likewise prevents presenting a generic
"first nonlinear transport correction" as a new mechanism. Its author-
uploaded primary text was accessible; the publisher PDF returned HTTP 401.
The aging-paper delivery URL again returned HTTP 403. Its full-text
comparison remains missing, not silently treated as a completed review.

Own inference: the linear transport story is a useful baseline and a
required control, but is not a sufficient replacement novelty claim. The
remaining candidate is a controlled, kernel-sensitive nonlinear correction
with a clearly bounded domain of validity. That candidate also needs a
focused comparison with nonlinear autochemotaxis and stochastic perturbation
literature before any assertion of priority.

Search boundary: exact aging-paper title and authors; exponentially weighted
self-interacting diffusion; self-attraction, finite memory and transport;
nonlinear/quartic history interactions. The author talk independently confirms
the aging topic, but does not close the missing full-text comparison. No
simulations are justified merely by this incomplete search.

The added Gaussian-feedback search exposed Sarkar's paper, which the
2026-10-09 bibliography had missed. Its model-level comparison must be
included in the next introduction. It is not a reason to copy its broad
coherence claims, to lower the evidence standard, or to regard PRE publication
of a neighboring model as proof that this baseline is publishable.

## What remains established

The frozen dataset and PDFs are unchanged. The 85 terminal radius traces
support consistency with an observable-matched linear reference at the
archived conditions. They do not contain the coordinate histories needed
to establish a long-lag displacement curve. Their 10,001-point terminal
blocks must not be treated as 30M or 300M independent observations.

The repository already contains untruncated linear center/visible MSD
references in `src/emergenz_knoten/force_work_port.py`. The new research
calculation uses finite-history lag coordinates to calculate perturbative
coefficients and provides an independent linear covariance cross-check;
it does not replace those established helpers or the production simulator.

## Formal first nonlinear correction

This section is an original derivation in this working note, **not a claim
of literature priority**. Its general use is conditional on a smooth local
weak-noise moment expansion. The updates below distinguish the now-proved
restricted domains from the remaining stationary and transport-limit gaps.

Update 2026-10-21: the [finite-memory stationarity note](finite_memory_stationarity_2026-10-21.md)
now supplies existence, uniqueness and finite polynomial moments for fixed
finite $H$ and positive noise under the full bounded force. Its
minorization is not uniform in $H$ or vanishing noise. An explicit
coexistence example also shows why local linear stability alone does not
select the stationary weak-noise branch.

A subsequent [global-contraction note](weak_noise_validity_2026-10-21.md)
justifies the quadratic-moment expansion below under the stronger
condition $|\eta|G_2q/\alpha<1$, where $G_2$ bounds the full kernel Hessian.
Its argument also covers untruncated exponential memory. All active
archived Paper-I cells lie outside this sufficient domain. The transport
extension to that note now supplies a summable innovation-coupling bound
for the Taylor remainder, justifying the infinite-lag covariance sum and
an explicit untruncated transport coefficient in the same strict domain.
The later positive-averaging extension of the finite-memory note gives a
second sufficient domain for stationary quadratic moments: nonnegative
radial feedback with $\eta(A_a/s_a^2)(q-q^H)<1$. It includes all archived
model coefficients at fixed $H=600$, but its enormous constants do not
validate their finite noise or terminal blocks. It does not extend the
transport theorem or control $H\to\infty$. Outside these stated domains
the corresponding expansions remain conditional. None of these validity
arguments by itself establishes publication novelty.

For the manuscript kernel, direct Taylor expansion gives

$$
\nabla K(u)=\kappa u+\lambda |u|^2u+O(|u|^5),\qquad
\kappa=\frac{A_a}{s_a^2}-\frac{A_r}{s_r^2},\qquad
\lambda=\frac{A_r}{2s_r^4}-\frac{A_a}{2s_a^4}.
$$

Define $L_{j,n}=x_n-x_{n-j}$ for $j=1,\ldots,H-1$ and
$w_j=\alpha q^j/(1-q^H)$, including $j=0$. The local force increment is

$$
x_{n+1}-x_n=-g\sum_j w_j L_{j,n}
-\beta\sum_j w_j |L_{j,n}|^2 L_{j,n}+\varepsilon\xi_n+O(L^5),
\quad g=\eta M_H\kappa,\quad\beta=\eta M_H\lambda.
$$

Here $L_{0,n}=0$. Let $b$ be the all-ones vector of length $H-1$ and $S$
the matrix with ones immediately below its diagonal. In scaled coordinates
$U=L/\varepsilon$, the linear transition is $A=S-gb(w_1,\ldots,w_{H-1})$.
For $0\leq g<1$, its relative state is stable. The per-coordinate unit-noise
covariance solves the ordinary discrete Lyapunov equation

$$
C=ACA^T+bb^T.
$$

At the Gaussian reference, Wick contraction yields

$$
\mathbb E[U_i^a|U_j|^2U_j^a]=(d+2)C_{ij}C_{jj}.
$$

Thus the first-order covariance forcing is identical to that of a linear
drift perturbation

$$
A_1=-(d+2)b(w_1C_{11},\ldots,w_{H-1}C_{H-1,H-1}).
$$

Writing $t=\beta\varepsilon^2$, the conditional expansion is
$\operatorname{Cov}(L^a)=\varepsilon^2(C+tC_1+O(\varepsilon^4))$ at fixed
model coefficients, with

$$
C_1=AC_1A^T+A_1CA^T+ACA_1^T.
$$

This determines the leading correction without fitting the measured
nonlinear radius. With $v=(w_1,\ldots,w_{H-1})^T$,

$$
R_r^2=d\varepsilon^2 v^T(C+tC_1)v+O(\varepsilon^6),
$$

$$
R_Q^2=d\varepsilon^2\left[
\sum_{j=1}^{H-1}w_j(C+tC_1)_{jj}-v^T(C+tC_1)v
\right]+O(\varepsilon^6).
$$

The same first-chaos contraction applies to first-order two-time moments.
The corresponding formal per-coordinate transport expansion is

$$
\frac{D}{\varepsilon^2}=\frac{1}{2(1+g\bar j)^2}
-t\frac{(d+2)\sum_{j=1}^{H-1}j w_j C_{jj}}{(1+g\bar j)^3}
+O(\varepsilon^4),\qquad \bar j=\sum_j j w_j.
$$

The second term is a prediction to test, not measured nonlinear transport.
The separate contraction note now justifies the all-lag covariance
interchange only in its strict domain; local linear stability is still
insufficient. The cubic polynomial must
not be simulated as though it were a globally stable replacement for the
bounded Gaussian force: an explicit cubic update can diverge at large
amplitudes regardless of its local expansion.

### A discriminating kernel pair already available

For $s_r=1$, $s_a=3$, the historically compared pairs $(A_r,A_a)=(0,26)$
and $(1,35)$ have identical $\kappa=26/9$, but respectively
$\lambda=-13/81$ and $\lambda=23/81$. Their first force corrections have
opposite signs. At fixed $g$, $\alpha$, $H$, dimension and noise, the
linear covariance is identical, while the formal leading nonlinear
corrections are proportional to these different coefficients. For an
observable whose response coefficient is nonzero, this is substantially
more discriminating than simply observing a 6.24% endpoint shift in one
kernel. A radius-correction sign must be calculated, not inferred solely
from the sign of $\lambda$; discrete update effects matter.

For transport, the newly justified coefficient is more specific: with
$\eta>0$ inside both contraction domains, the weighted age-covariance sum
and the response denominator are positive. The two $\varepsilon^4$
corrections are respectively positive and negative relative to the common
linear reference, with ratio $-23/13$. This does not assert opposite
radius corrections, superdiffusion or an effect above the Brownian control.
No finite-noise test of this asymptotic sign/ratio has been performed.

The legacy three-scale statistic is a normalized median width,
not the RMS used above. The 6.24% value must not be used to calibrate
$C_1$, select a preferred noise range, or claim a test of these formulas.

### Error-domain diagnostic, not a stationary error bound

For each Gaussian, $|e^{-z}-1+z|\leq z^2/2$ for $z\geq0$. Consequently
the pointwise gradient remainder is bounded by

$$
|\nabla K(u)-\kappa u-\lambda |u|^2u|
\leq \left(\frac{|A_r|}{8s_r^6}+\frac{|A_a|}{8s_a^6}\right)|u|^5.
$$

This bound is checked against the production kernel at synthetic distances.
At the Gaussian reference,
$\mathbb E|L_j|^5=\varepsilon^5 C_{jj}^{5/2}
2^{5/2}\Gamma((d+5)/2)/\Gamma(d/2)$, so the retained weighted fifth
moments give an explicit force-remainder diagnostic. The relevant
separations are **all age-resolved pairs**, not merely $x_n-c_n$. A small
current-point radius alone does not bound an old deposit's displacement.
Neither the pointwise bound nor its Gaussian expectation is a bound on the
stationary covariance error of the nonlinear process. The separate
contraction and finite-$H$ positive-averaging arguments supply that transfer
in their respective moment domains; neither currently provides a usable
error tolerance for the archived active cells.

## Checks and evidence boundary

`scripts/weak_nonlinearity.py` implements the lag covariance, Lyapunov
derivative, linear MSD and zero-frequency transport response. Synthetic
tests compare the radius with the independent FIFO impulse calculation;
check Brownian controls, the mean-age diffusion expression and Green--Kubo
slope; compare the derivative with perturbed Lyapunov equations and an
analytic $H=2$ cubic moment balance; check correlated cross-lag Gaussian
contractions by exact quadrature; and compare both cubic kernel coefficients
and the remainder bound directly with the existing production gradient.
These tests audit algebra and implementation. They are not nonlinear
trajectory data, a replication, or proof of the conditional expansion.

Local verification on 2026-10-19: 21 synthetic research tests, eight frozen
baseline tests and two Markdown-math checks pass (31 total). Ruff and the
strict documentation build pass. The dedicated CI research job installs
the separately pinned SciPy dependency; the baseline dependency set and
archived figures remain unchanged.

No new production trajectories were generated and no historical gate was
renamed. Parameter values, outcome access and acceptance thresholds for a
prospective panel have not been frozen in this note. It is not itself an
execution authorization or a preregistered experiment.

## Conditions before new target data

Update 2026-10-22: the [external-review audit](external_review_audit_2026-10-22.md)
reproduces the proposed cell's untruncated coefficients but rejects its
current readiness claim. At the proposed $L=100$, raw block-MSD has a
37.17% linear bias relative to long-time transport, and the leading kernel
contrast is only 35.33% of its long-time value. Corrected independent
Gaussian sizing gives about $2.32\sigma$, not $13.5\sigma$; paired precision
is not yet calculated. The Gaussian force-remainder diagnostic remains
distinct from a transport error bound. No proposed target budget has been
authorized. This is a correctable design problem, not evidence that no
informative paired test exists.

The subsequent [paired feasibility calculation](paired_transport_feasibility_2026-10-22.md)
repairs the leading lag bias using an established two-length estimator and
calculates the model-specific long-block paired variance. The third chaos
contributes to this variance even though it drops out of the first mean
correction. Neither the statistical method nor this reference calculation
is sufficient publication novelty. A further
[finite-sample bound](finite_block_transport_bound_2026-10-22.md) now
controls sampling of the leading coefficient at finite block length;
finite-noise estimator/transport accuracy and practical initialization
still need to be controlled.

The defensible candidate core is now concrete: **an explicit weak-noise
diffusion correction for the full nonlinear, exponentially weighted
history law, controlled by a global sufficient condition, with a
matched-curvature kernel contrast.** The contraction and Gaussian-chaos
methods are standard; the model-specific coefficient and its discriminating
comparison are the candidate contribution. It would be misleading to
substitute generic memory, Markov augmentation or diffusion renormalization
as the novelty claim. The fixed-noise coupling expansion of Newman--Grima
and the small-delay expansion of Kopp--Klapp use different limits; difference
of limits alone is not proof of sufficient scientific significance.

The untruncated transport formula now avoids making the separate FIFO
orbit theory a prerequisite for Paper I. Its sufficient domain still
excludes the active frozen baseline. The additional fixed-$H$ moment
result covers those model coefficients asymptotically, but provides no
usable finite-noise error tolerance or route to the fundamental physics
program. An independent mathematical
review and the unresolved full-text comparison remain necessary before
treating this research note as a publication-ready theorem package.

The remaining full-text/novelty comparison and an explicit error-domain
assessment must precede a bounded prospective protocol. That protocol must
declare the kernel pair, noise levels from the theoretical small parameter,
memory times and gains, paired innovations, independent seeds, burn-in,
stored coordinates and lags, and a fixed stopping budget. It must include
linear and no-feedback controls and kernel/null cases that can falsify the
correction, rather than search only for visible nonlinear departures.

Report per-seed squared-displacement curves and matched RMS quantities;
use independent seeds as the replication unit. Overlapping lag windows are
correlated. Any block procedure needs a correlation-based, predeclared
block rule. Precision thresholds and equivalence margins must be fixed
from theory and scientific relevance, not chosen after seeing outcomes.
Insufficient precision or unobserved long-lag diffusion must return
inconclusive, not trigger an unlimited run extension. A common nonlinear
force implementation must be shared with, or independently checked against,
the existing production kernel.

If the correction is already known, not controlled, or not resolved within
the fixed budget, retain the baseline as an anchor/technical note and ask
the author about a different manuscript scope. Do not combine FIFO orbit
claims into this paper simply to increase apparent significance.
