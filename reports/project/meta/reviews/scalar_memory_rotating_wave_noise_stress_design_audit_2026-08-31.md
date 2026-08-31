# N0 design audit: numerical noise floor and orbital stability before P5

Date: 2026-08-31.

Decision: **insert one prospective two-scale noise-resolution and orbital-
stability ladder between P4-R-S and P5. Use the Paper-I transition law,
compare Anchor and L3 at common memory time and common diffusion-scaled noise,
and distinguish unresolved binary64 perturbations from dynamically stable
resolved noise. Do not advance a registered noisy target trajectory in this
audit.**

This audit answers a narrower question than P5:

> At what *numerically resolved* stochastic amplitude do the two prepared
> finite-memory rotating waves cease to remain orbitally stable under the
> unchanged Paper-I innovation channel?

It does not identify a physical Planck scale, derive a value of Planck's
constant, establish spontaneous noisy formation, or replace the later
two-loop interaction gate.

## 1. Evidence, inference and hypothesis

- **Evidence:** Anchor and L3 are locally numerically transversely stable at
  `epsilon=0`; P4-R-S transfers the declared discrete port response between
  the two prepared cells with maximum discrepancy `0.00232715 < 0.05`.
- **Inference to be tested:** the stable deterministic skeleton persists over
  a nonzero, numerically resolved innovation interval.
- **Hypothesis:** after scaling noise per memory time, both cells possess a
  common bracket between resolved orbital stability and loss of the
  registered orbit/conditional contraction gates.
- **Not implied by a pass:** generic stochastic formation, a thermodynamic or
  quantum noise law, a physical value of `epsilon`, interaction, spin,
  momentum, inertia or mass.

The audit base is main revision

```text
7f854d88684d02d0b19c687a332a4d1d80e2e8b3
```

with green mainline CI run
[33425970122](https://github.com/MemoryDynamics/Knoten/actions/runs/33425970122).
Relevant immutable Git blobs are:

| dependency | Git blob |
| --- | --- |
| Paper-I long model | `14646211d69a132a6742aea249574f56b67d2b88` |
| Paper-I compact model | `4487172d03e0004977539d9c4b39d2e0a0b20120` |
| native finite-H FIFO map | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| reusable stability machinery | `630beb9952abefea823d91388dcbb2de8f1a2927` |
| formation/phase utilities | `38f16f11a790a64470bab3a34505825cf815e7f0` |
| Anchor stability JSON | `1c9d5746c9553d9cb8031b58258e6d613f1633d9` |
| L3 stability JSON | `18821ed0235e5e915424f61c665be86d569d58cc` |
| P4-R-S raw JSON | `e4eae06ada6860455e49a08691235b9f6e818f51` |
| P4-R-S result review | `4d3297c2bfb0fd191bd73e8e9cad7f7d85a86b87` |

At audit time no N0 protocol, runner, target test, result or figure exists.

## 2. Canonical transition law in Paper-I language

Paper I defines

$$
x_{n+1}=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n),
$$

$$
\rho_{n+1}=(1-\lambda_{\rm m})\rho_n
+\beta G_\sigma(\cdot-x_{n+1}),
$$

with augmented state $z_n=(x_n,\rho_n)$ and centered unit-covariance
innovation $\xi_n$. In the normalized convention

$$
\lambda_{\rm m}=\beta=\alpha,
\qquad q=1-\alpha.
$$

The finite-$H$ rotating-wave implementation is the exact ordered-history
specialization used by this gate. For

$$
Y_n=(x_n,x_{n-1},\ldots,x_{n-H+1})
$$

and native deterministic newest-slot map $F_H$, the noisy step is

$$
\widetilde x_{n+1}=F_H(Y_n)_0,
\qquad
x_{n+1}=\operatorname{fl}(\widetilde x_{n+1}+\varepsilon\xi_n),
$$

$$
Y_{n+1}=(x_{n+1},x_n,\ldots,x_{n-H+2}).
$$

Noise is added after the deterministic force and before the new position is
deposited into memory. This is the same order as the Paper-I equations. No
noise is written independently into old history slots, the center readout or
the P4 source/write actuator.

Equivalently,

$$
z_{n+1}=\mathcal F_H(z_n; q,\eta,M_0,K)
+\varepsilon\,\Sigma_x\xi_n,
$$

where $\Sigma_x$ injects only into the newly written visible coordinate.
This notation separates the deterministic skeleton $\mathcal F_H$ from the
innovation without deleting either from the model.

## 3. Why `epsilon = 10^-20` is not yet a physical statement

Planck's constant is dimensionful, whereas the repository parameter
$\varepsilon$ is a coordinate displacement per update. They cannot be
compared until a physical length, time and action calibration is supplied.
No value of $\hbar$ is used to choose or interpret the grid.

There is a separate numerical problem. For binary64,

$$
u=2^{-52}\simeq2.22\times10^{-16}.
$$

If a coordinate is order one, an intended displacement near $10^{-20}$ can
round to zero. Because orbit coordinates periodically cross zero, a single
global `epsilon < u` rule is insufficient: some components can remain
representable while most are lost. The runner must therefore store, at every
step,

$$
d_n^{\rm eff}
=\operatorname{fl}(\widetilde x_{n+1}+\varepsilon\xi_n)
-\widetilde x_{n+1}
$$

and compare it with the intended increment
$d_n^{\rm int}=\varepsilon\xi_n$.

A cell may be called **numerically deterministic** or **unresolved**, but not
noise-stable, if the intended perturbation is not reliably injected. Exact
mathematical determinism remains only $\varepsilon=0$.

## 4. Two-scale noise coordinate

The Paper-I small-step ansatz uses

$$
D={\varepsilon^2\over2\alpha}.
$$

Copying the same raw $\varepsilon$ into Anchor and L3 would therefore compare
different diffusion exposure per memory time. Freeze instead

$$
\chi={\varepsilon\over R\sqrt{\alpha}},
\qquad
\varepsilon_r=\chi R_r\sqrt{\alpha_r},
$$

where $r\in\{A,L3\}$. Then $D/R^2=\chi^2/2$ is common across scale.
Both raw $\varepsilon_r$ and $\chi$ must be serialized; the primary plot and
decision axis is $\chi$.

The broad grid is fixed before target access:

$$
\chi\in\{0\}\cup\{10^k:k=-22,-21,\ldots,-2\}.
$$

This covers the requested sub-$10^{-20}$ region, the binary64 transition and
the historically destructive larger amplitudes without a confirmatory
parameter search.

## 5. Common noise per memory time

The cells share

$$
H\alpha=12,
\qquad \eta/\alpha=15,
$$

and are run to $\tau=\alpha n=20$. L3 has two updates per Anchor update.
For each fixed master seed, generate 4000 fine independent standard-normal
vectors $\zeta_j$. Use

$$
\xi^{L3}_j=\zeta_j,
\qquad
\xi^A_k={\zeta_{2k-1}+\zeta_{2k}\over\sqrt2}.
$$

Together with $\varepsilon_r=\chi R_r\sqrt{\alpha_r}$, every paired Anchor
increment and the two corresponding L3 increments have the same normalized
variance over $\Delta\tau=0.01$. This is a Brownian-refinement coupling for
comparison, not an assertion that the microscopic process is Brownian.

Freeze three master seeds:

```text
2026083101
2026083102
2026083103
```

The seeds are deterministic stress arms, not three independent physical
experiments. No seed may be dropped after inspection.

## 6. Stronger stability observables than an `x/y` circle

An ambient circle can drift, rotate or deform while still looking plausible.
The primary metric is therefore the frozen quotient distance

$$
D_0(Y,Y_*)
=\min_{a\in\mathbb R^2,\,Q\in SO(2)}
\|Q(Y-a)-Y_*\|_{w},
$$

using the existing finite-memory D0 weights. It removes common translation
and ambient rotation but retains radial and history-shape deformation.

For every candidate, $\chi$ and seed, run two trajectories with the same
noise:

1. the exact prepared circular history;
2. the same history plus the already registered full-history transverse
   perturbation of Euclidean norm $10^{-7}R$.

The common-noise pair distance tests conditional transverse attraction. The
base trajectory supplies:

- maximum and late RMS $D_0(Y_n,Y_*)/\|Y_*\|_{D0}$;
- visible radius error relative to the memory centroid;
- signed adjacent-slot angle error relative to $\theta$ and chirality
  retention;
- center displacement as a translation-mode diagnostic, not a primary fail;
- intended/effective injection RMS ratio and nonzero-injection fraction.

The paired trajectory supplies maximum growth and final/initial quotient
distance. A coordinate plot is retained only as a secondary equal-aspect
linear-axis phase portrait. `x` and `y` take both signs and must not be put on
logarithmic axes. The actual stability plots use logarithmic $\chi$ and
logarithmic nonnegative error metrics.

## 7. Frozen resolution classes

For nonzero $\chi$, define

$$
r_{\rm inj}
=\sqrt{{\sum_n\|d_n^{\rm eff}\|^2
\over\sum_n\|d_n^{\rm int}\|^2}},
\qquad
f_{\rm nz}={1\over N}\#\{n:\|d_n^{\rm eff}\|>0\}.
$$

The cell is:

- `resolved` if $r_{\rm inj}\ge0.5$ and $f_{\rm nz}\ge0.5$;
- `unresolved` if $r_{\rm inj}\le0.1$ or $f_{\rm nz}\le0.1$;
- `partially-resolved` otherwise.

The exact zero cell is `deterministic-control`. A partially resolved cell is
inconclusive and may not anchor a stability boundary.

## 8. Frozen orbital and conditional-stability gates

All fractions below are dimensionless and fixed before target access. A
resolved arm is orbitally stable only if:

1. it completes to $\tau=20$ with finite state;
2. maximum quotient distance is at most `0.10` of the reference D0 norm;
3. late-window RMS quotient distance over $\tau\in[15,20]$ is at most `0.05`;
4. maximum visible relative-radius error is at most `0.05`;
5. late RMS adjacent-slot phase error is at most `0.20 theta` and at least
   `0.99` of sampled increments retain the prepared chirality;
6. the common-noise perturbed/base distance grows by at most factor `10` and
   ends at most `0.10` of its initial value.

The absolute stopping boundary remains `0.25` of the reference D0 norm. It
is a fail, not a censoring rule. The zero-noise base must additionally remain
within absolute quotient distance `1e-10` and the zero-noise paired arm must
retain the historical contraction gate.

For each $\chi$, all three seeds and both candidates must pass for an
`all-cell-stable` classification. Any resolved arm that crosses a primary
gate makes that $\chi$ `stress-fail`. Mixed resolution or a mixture of pass
and fail across seeds/candidates is `inconclusive`.

## 9. Ladder decision and scaling diagnostic

The scan may return:

- `noise-stability-window-bracketed`: at least three consecutive resolved
  nonzero grid cells pass, a higher resolved cell fails, and no stable
  re-entry occurs above the first fail;
- `noise-stable-through-grid`: every resolved cell through `chi=1e-2`
  passes;
- `noise-robustness-fail`: no resolved nonzero cell passes;
- `noise-stress-inconclusive`: partial resolution, nonmonotone re-entry,
  insufficient resolved cells or incomplete execution prevents a bracket.

The largest all-cell stable grid point and the first higher non-pass point
form a bracket only. No critical exponent or interpolated threshold is
estimated.

As a preregistered diagnostic, fit

$$
\log(D_{0,\rm late}^{\rm RMS})
=a+b\log(r_{\rm inj}\varepsilon)
$$

over the first four consecutive resolved stable cells, separately for Anchor
and L3. The linear forced-response expectation is $0.75\le b\le1.25$.
Failure of this diagnostic does not retroactively change individual orbital
gates, but it makes the cross-scale noise interpretation inconclusive.

## 10. Implementation and target firewall

The next allowed actions are:

1. commit this target-free design audit;
2. write and separately freeze a prospective protocol;
3. implement reusable noisy-step, metric and plotting code with synthetic
   reflection, Brownian-refinement, injection-floor and decision falsifiers;
4. prove tests do not execute the registered two-scale scan;
5. perform a separate implementation-readiness review from a clean pushed
   revision;
6. run the registered target exactly once and freeze JSON before review.

Before the readiness review, no new noisy Anchor or L3 trajectory may be
advanced, plotted or summarized. P5-D, P5-C, P5-I and every two-loop target
remain sealed.

## 11. Paper and merge consequence

A reviewed bracket would justify this limited structural statement:

> The Paper-I stochastic transition law contains a deterministic
> finite-memory rotating skeleton whose prepared Anchor and L3 members remain
> conditionally orbitally stable over a registered, numerically resolved
> innovation interval.

It would prepare the transition from deterministic P5-D to common-noise P5-C
and independent-noise P5-I. It would not show that noise forms the loops or
that the stochastic and rotating-wave branches are already one empirical
regime.

