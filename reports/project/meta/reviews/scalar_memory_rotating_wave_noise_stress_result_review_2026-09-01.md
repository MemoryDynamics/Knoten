# N0 result review: resolved-noise orbital stability before P5

Date: 2026-09-01  
Verdict: **`n0-noise-stability-window-bracketed-reviewed-pass`**  
Claim class: finite-time numerical robustness of two prepared rotating waves  
Next gate: P5 design and prospective protocol may open; P5 target execution
remains closed.

## 1. Immutable evidence reviewed

| artifact | identifier |
|---|---|
| execution revision | `1ea46d86588d0a2e60021439fae4d6a5ef04406e` |
| raw-result commit | `ea42cfd16f3e7b4aa728a0e0fc452c4b4b87b17d` |
| JSON blob | `0bcf489068fc0c7004f0c65b973f7be49dfe1621` |
| Markdown blob | `5d0951d68fd1f35ee4dd28d52e1a1c6cffa438ab` |
| PNG blob | `f9621b07e906e9ee7a983b45ece2b030d7ebae77` |
| independent recompute commit | `255c6916ed1168a72e3020260fe72cb409062457` |
| independent JSON blob | `030d26b308a22cd1e1dbd91e1f32f13fc04204a7` |
| auditor CI | [GitHub run 33467976497](https://github.com/MemoryDynamics/Knoten/actions/runs/33467976497), success |

The registered runner executed once from its clean pushed readiness revision.
It produced 132 candidate/grid/seed rows in the frozen order and completed in
211.43 seconds. The raw result was committed before auditor code or review
text was added.

## 2. Primary registered result

The exact grid classification is:

| common amplitude `chi` | registered classification |
|---:|---|
| `1e-22` through `1e-16` | inconclusive: binary64 innovation unresolved |
| `1e-15` through `1e-4` | all cells stable |
| `1e-3`, `1e-2` | stress fail |

Thus the registered decade bracket is

$$
10^{-4}\le \chi_{\rm stable}<\chi_{\rm fail}=10^{-3},
\qquad
\chi={\varepsilon\over R\sqrt\alpha}.
$$

It is not an interpolated critical point. In the Paper-I diffusion coordinate,
the two bracketing grid values are

$$
{D\over R^2}={\chi^2\over2}=5\times10^{-9}
\quad\hbox{and}\quad
5\times10^{-7}.
$$

The corresponding raw binary64 amplitudes are:

| candidate | last stable epsilon | first failing epsilon |
|---|---:|---:|
| Anchor | `9.465175048e-6` | `9.465175048e-5` |
| L3 | `6.681796113e-6` | `6.681796113e-5` |

The exact zero control is bitwise native and passes. All three seeds and both
candidates contribute at every resolved stable and failing cell; no seed was
dropped.

## 3. What actually fails

At `chi=1e-3`, neither gross geometry nor transverse contraction is close to
its gate:

- maximum `D0/reference_D0_norm` is only about `1.47e-3..1.74e-3`, far below
  `0.10`;
- late RMS D0 is about `7.70e-4..1.09e-3`, far below `0.05`;
- maximum centre-reduced radius error is about `1.47e-3..1.80e-3`, far below
  `0.05`;
- final common-noise pair ratios remain about `1.86e-4..3.56e-4`, far below
  `0.1`.

The registered fail is instead driven by the local edge-phase and chirality
gates:

| candidate | late phase RMS / theta at `chi=1e-3` | chirality fraction |
|---|---:|---:|
| Anchor, three seeds | `0.528..0.647` | `0.955..0.970` |
| L3, three seeds | `1.514..1.728` | `0.733..0.761` |

Both cross the frozen `0.20` phase and `0.99` chirality limits. The last stable
cell `chi=1e-4` is closer: L3 phase RMS/theta is `0.151..0.173`. The bracket is
therefore a **phase-coherence robustness bracket**, not a claim that a visible
circle disintegrates between the two decades. The nearly coincident x-y panels
are consistent with, and less discriminating than, the registered phase gate.

## 4. Numerical resolution transition

The requested region below `1e-20` is exactly deterministic in this binary64
implementation: no intended increment survives. Resolution begins gradually
above it. At `chi=1e-16`, RMS effective/intended ratios reach about `0.39..0.48`
but only `4.8%..7.0%` of components are nonzero, so the prospective rule still
classifies every arm as unresolved. At `chi=1e-15`, both criteria cross their
registered `0.5` limits for all arms.

Therefore:

- **evidence:** this implementation is numerically indistinguishable from its
  deterministic skeleton through the lower registered region;
- **inference:** the first fully resolved decade is `chi=1e-15` for these
  coordinates, histories and binary64 operations;
- **not supported:** mathematical determinism for nonzero epsilon, a physical
  noise floor, or a value derived from Planck's constant.

## 5. Scaling check

The prospective first-four-resolved-cell fits give

| candidate | registered slope | frozen interval |
|---|---:|---:|
| Anchor | `0.936260` | `0.75..1.25` |
| L3 | `0.870355` | `0.75..1.25` |

Both pass. An explicitly exploratory one-decade shift of the same four-cell
window gives `0.998363` and `0.992540`. This sensitivity supports an
approximately linear response once clear of the representation transition,
but it is post-hoc and cannot strengthen the registered claim. Four decades
from two prepared candidates do not establish a universal stochastic scaling
law.

## 6. Independent recomputation and integrity

The separate auditor recomputes, without importing the runner's decision
helpers:

- exact 132-row registration and order;
- every resolution label;
- every dynamic gate;
- all 21 grid labels;
- the final bracket decision;
- both registered slopes.

There are zero resolution or gate mismatches. The PNG signature is valid.

The Markdown digest equals the canonical LF Git-blob SHA256
`487023fe0a7bf197a400f4c8a5ef086a6ddf6d59c679ca2395a2913ee38079bc`.
On the Windows review checkout, Git's CRLF working-tree transformation gives a
different local byte SHA; on Linux CI the checked-out bytes equal the embedded
digest. This is not repository corruption. Future writers should nevertheless
hash the final bytes or label the digest explicitly as canonical-LF to prevent
platform confusion.

## 7. Referee restrictions

The pass does not establish:

1. stationary noisy formation or an invariant stochastic measure;
2. robustness beyond common memory time `tau=20`;
3. independent physical replication from three deterministic seeds;
4. a continuum limit from two prepared finite-H cells;
5. state-dependent, colored, anisotropic or multiplicative noise robustness;
6. a physical calibration of epsilon, action or Planck's constant;
7. interaction, charge, spin, momentum, inertia or mass;
8. visible destruction of the circle at the first failing decade.

The common Brownian-refinement path is a controlled scale-transfer device, not
independent evidence. The phase threshold is operational and preregistered;
its physical meaning remains to be derived.

## 8. Gate consequence

The N0 gate passes in its narrow registered sense. It supplies a resolved
finite-time noise window and a higher resolved phase-coherence failure for
both prepared cells. This is sufficient to return the project to the P5
**design/protocol** path with a justified deterministic-first decomposition:

1. P5-D: deterministic mutual-response design and controls;
2. only after a reviewed P5-D result, P5-C: common-noise cancellation;
3. only after that, P5-I: independent-noise robustness.

No P5 implementation or target trajectory is authorized by this review alone.
The N0 branch may enter main after status surfaces, full tests and final CI are
green.
