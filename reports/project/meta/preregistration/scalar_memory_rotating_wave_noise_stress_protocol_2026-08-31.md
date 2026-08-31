# N0 protocol: resolved-noise orbital stability before P5

Date: 2026-08-31  
Status: **prospectively frozen after the separately committed design audit;
no registered N0 trajectory existed when this file was written**  
Design-freeze commit: `6b17f9562baed07f842e1cb9f3a565652371f5d4`

Pre-target clarification (2026-09-01): before runner completion or any target
execution, the D0 denominator was restored to the design-audit reference norm
and the radius and edge-phase references were made explicit. The originally
committed text remains visible in Git history; no threshold or target datum
was inspected.

## 1. Registered question and claim boundary

At what *numerically resolved* innovation amplitude do the prepared Anchor
and L3 rotating waves cease to satisfy the frozen finite-time orbital
stability gates? The test may return a grid bracket, stability through the
grid, a robustness fail, or an inconclusive result.

It cannot determine a physical value of Planck's constant, a continuum noise
law, stationary stochastic formation, interaction, spin, momentum, inertia,
mass or universality. An intended perturbation that rounds away in binary64
is unresolved, not evidence of robustness.

## 2. Frozen model law and noise placement

The shared Paper-I transition language is

$$
x_{n+1}=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n).
$$

For the native finite-history specialization, first evaluate the unchanged
deterministic FIFO step and call its newest position
$\widetilde x_{n+1}$. Then and only then set

$$
x_{n+1}=\operatorname{fl}(\widetilde x_{n+1}+\varepsilon\xi_n).
$$

The older slots are exactly the native FIFO shift. No noise is written into
an old slot, force, memory weight, centre, phase, radius or fitted parameter.
The random vectors are independent standard normal vectors in two
coordinates. The `epsilon=0` arm must be bitwise identical to the native
deterministic step.

For every step serialize the aggregate intended and effective increments

$$
d_n^{\rm int}=\varepsilon\xi_n,\qquad
d_n^{\rm eff}=\operatorname{fl}(\widetilde x_{n+1}+d_n^{\rm int})
               -\widetilde x_{n+1}.
$$

## 3. Frozen candidates

```text
Anchor
candidate_id = k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1
R = 0.946517504804223960990626662735384935160072399313332184824852189820406142783597632634323623097735558253263801
theta = 0.0157703817171349919012689641413413231316321140980062507765923663663284306507309780740587352166842324150748019
alpha = 0.01
H = 1200
eta = 0.15
steps = 2000

L3
candidate_id = k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1
R = 0.944805811705743656419366118422595657454474452804188781825799206245348464567689511866917417017911971955244464
theta = 0.00790666146243552374938496703030974246197803459527409259815696583141708245813094145986593003659167675765833059
alpha = 0.005
H = 2400
eta = 0.075
steps = 4000
```

Both use `d=2`, `M0=1`, repulsive width/amplitude `(1,1)` and attractive
width/amplitude `(3,3.5)`. Both satisfy `H alpha=12` and `eta/alpha=15`.
Exact decimals and parsed binary64 values are serialized. No root, parameter
or initial history may be refitted.

## 4. Registered dimensionless ladder

The primary amplitude coordinate is

$$
\chi={\varepsilon\over R\sqrt\alpha},\qquad
\varepsilon_r=\chi R_r\sqrt{\alpha_r},\qquad
{D\over R^2}={\chi^2\over2}.
$$

The exact ordered grid is

```text
0,
1e-22, 1e-21, 1e-20, 1e-19, 1e-18, 1e-17, 1e-16,
1e-15, 1e-14, 1e-13, 1e-12, 1e-11, 1e-10, 1e-9,
1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2
```

The zero arm is a separate deterministic control and is never placed on a
logarithmic axis. Results must serialize `chi`, raw `epsilon`, and
`D_over_R_squared`.

## 5. Frozen common path, seeds and execution order

Master seeds, in order, are

```text
2026083101, 2026083102, 2026083103
```

For each seed, NumPy's `Generator(PCG64(seed)).standard_normal((4000,2))`
generates the fine L3 path $\zeta_j$. The Anchor path is constructed without
new random draws:

$$
\xi_k^A={\zeta_{2k}+\zeta_{2k+1}\over\sqrt2},
\qquad k=0,\ldots,1999.
$$

This is a Brownian-refinement coupling over common memory time, not an
independent replication. Each candidate runs to $\tau=\alpha n=20$.

Serialization and execution order is candidate (`Anchor`, `L3`), increasing
grid order, seed order, then arm (`base`, `transverse-pair`). The runner must
execute all cells even after the first failure; a non-finite state or a
quotient distance above `0.25 R` stops only that arm and records its step.
No seed or grid point may be dropped after inspection.

## 6. Frozen initial conditions and samples

The base history is the existing positive-chirality prepared target history.
The paired history adds the existing deterministic stability gate's
full-history transverse perturbation, projected off translation and rotational
neutral directions and normalized to Euclidean norm `1e-7 R`. Base and pair
receive bitwise identical noise at every step.

Metrics are sampled at the exact memory times

```text
0, 0.05, 0.10, ..., 20.00
```

giving 401 intended samples per complete arm. A sample is taken after the
update reaching that time, except the stored initial sample at zero.

## 7. Frozen metrology

For a history $Y$, compute the existing normalized finite-memory weighted
centre and compare with the matching positive-chirality target by the existing
translation- and SO(2)-quotiented distance $D_0$. In agreement with the
design audit, its primary denominator is the target's frozen D0 norm
$\lVert Y_*\rVert_{D0}$; `D0/R` is serialized only as secondary metrology.
The visible-radius reference is the centre-reduced newest-slot radius of
$Y_*$, not the uncentred parameter $R$. The signed adjacent-slot phase is the
translation-invariant edge phase

$$
\arg\left[(Y_0-Y_1)\overline{(Y_1-Y_2)}\right].
$$

At every sample record:

1. base $D_0/\lVert Y_*\rVert_{D0}$ and secondary $D_0/R$;
2. visible newest-slot radius relative error against the corresponding
   centre-reduced target radius;
3. wrapped adjacent-slot phase-increment error relative to positive `theta`;
4. chirality sign retention;
5. common-noise pair $D_0/R$ and ratio to its initial value;
6. finite-state and stop flags.

For each nonzero arm define across all updated coordinates

$$
r_{\rm inj}=
{\operatorname{RMS}(d^{\rm eff})\over
 \operatorname{RMS}(d^{\rm int})},\qquad
f_{\rm nz}={\#\{d^{\rm eff}_{n,j}\ne0\}\over2N}.
$$

Classification precedence is:

- `unresolved` if `r_inj <= 0.1` or `f_nz <= 0.1`;
- `resolved` if `r_inj >= 0.5` and `f_nz >= 0.5`;
- `partially-resolved` otherwise.

The zero arm is `deterministic-control`. No dynamic pass/fail interpretation
is assigned to a partially resolved cell.

## 8. Frozen arm gates

The zero control passes only if its base history remains within
`max D0/R <= 1e-10`, it is bitwise native at every update, and its historical
paired contraction gates pass.

A resolved nonzero arm is stable only if all conditions hold:

| metric | threshold |
|---|---:|
| completes through `tau=20` | required |
| maximum base `D0/reference_D0_norm` | `<= 0.10` |
| late (`15 <= tau <= 20`) RMS base `D0/reference_D0_norm` | `<= 0.05` |
| maximum visible radius relative error | `<= 0.05` |
| late RMS wrapped phase error | `<= 0.20 theta` |
| sampled positive-chirality fraction | `>= 0.99` |
| maximum pair-distance / initial pair-distance | `<= 10` |
| final pair-distance / initial pair-distance | `<= 0.1` |
| stop threshold | never reaches `0.25 R` |

Non-finiteness, missing samples or malformed registration precede all dynamic
labels and make the run inconclusive. Any threshold equality passes.

## 9. Frozen grid and study decisions

For a nonzero `chi`:

- `all-cell-stable`: all three seeds for both candidates are resolved and
  pass every arm gate;
- `stress-fail`: at least one resolved arm crosses a primary gate;
- `inconclusive`: otherwise, including mixed or partial resolution.

Study labels, applied in order, are:

1. `n0-inconclusive` for provenance, construction, completeness,
   non-finiteness or zero-control failure;
2. `n0-noise-robustness-fail` if no resolved nonzero grid cell is
   `all-cell-stable`;
3. `n0-noise-stability-window-bracketed` if at least three consecutive
   resolved cells pass, a higher resolved cell fails, and no higher stable
   re-entry occurs;
4. `n0-noise-stable-through-grid` if every resolved cell through `1e-2`
   passes;
5. otherwise `n0-inconclusive`.

Unresolved and partially resolved low-amplitude cells locate the numerical
resolution transition; by themselves they do not invalidate a later run of
resolved cells. They contribute neither passes nor failures to the required
three-cell stable sequence. A mixed cell above resolution is retained as
`inconclusive` and prevents a bracket that would have to cross it.

A bracket reports only the last stable registered grid value and the first
higher failing registered grid value. It must not interpolate a critical
amplitude.

As a secondary scaling check, regress

$$
\log(\operatorname{RMS}_{15\le\tau\le20}D_0/\lVert Y_*\rVert_{D0})
=a+b\log(\operatorname{RMS}d^{\rm eff}/R)
$$

over the first four consecutive resolved stable cells, separately for each
candidate after pooling the three seed RMS values geometrically. The frozen
compatibility interval is `0.75 <= b <= 1.25`. Failure changes the
cross-scale interpretation to inconclusive but does not relabel an individual
orbital gate.

## 10. Frozen figures

One registered multi-panel PNG contains:

1. log-log `chi` versus late RMS `D0/reference_D0_norm`, with resolution
   class and gate threshold;
2. log-log `chi` versus `r_inj` and `f_nz` (the latter may use a logarithmic
   ordinate only after zero values are shown separately);
3. log-log `chi` versus maximum radius error and late phase RMS;
4. representative last-stable and first-failing `x-y` trajectories for both
   candidates, with **linear equal-aspect axes**.

The zero control is annotated outside log axes. Floors used only for display
must be recorded and must never enter decisions.

## 11. Implementation firewall and outputs

Before target execution, synthetic tests must establish:

- exact zero-noise equivalence and newest-slot-only injection;
- effective-increment accounting, including a sub-ULP unresolved example;
- translation, rotation and reflection covariance with transformed noise;
- exact Brownian-refinement construction and deterministic RNG ordering;
- resolution boundary equality and decision precedence;
- quotient-distance invariance and transverse-pair construction;
- tests do not run the registered candidate grid;
- output path restriction, overwrite refusal and atomic complete writes.

The registered default outputs are exclusively

```text
reports/dynamics/rotation/scalar_memory_rotating_wave_noise_stress_2026-08-31.json
reports/dynamics/rotation/scalar_memory_rotating_wave_noise_stress_2026-08-31.md
reports/dynamics/rotation/scalar_memory_rotating_wave_noise_stress_2026-08-31.png
```

The runner must require a clean, pushed execution revision containing the
design freeze, this protocol, implementation and a separately committed,
CI-green readiness review. It refuses existing final or temporary outputs.
All three complete artifacts are written via temporary siblings and renamed
only after the full decision is available. A failed run leaves no registered
artifact.

The first registered execution occurs once. Its artifacts are committed and
pushed without code changes, followed by an independent recomputation and a
separately committed result review before priorities or Paper I claims change.

## 12. Falsification charter

N0 is falsified or rendered inconclusive if any of the following occurs:

1. sub-ULP disappearance is counted as stochastic stability;
2. raw `epsilon` rather than common `chi` is used for cross-scale comparison;
3. the two candidates do not share the registered refined Brownian path;
4. noise enters old history slots or changes the deterministic force law;
5. registration, samples or failing arms are omitted;
6. an `x-y` logarithmic plot hides sign or geometry;
7. thresholds, seeds, grid or candidates change after target inspection;
8. a finite grid bracket is reported as an exact transition;
9. a pass is described as physical quantum calibration, stationary formation,
   interaction, inertia or mass.
