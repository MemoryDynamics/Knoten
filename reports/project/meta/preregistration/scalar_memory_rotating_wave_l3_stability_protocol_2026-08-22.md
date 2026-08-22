# Prospective P1 non-Anchor stability gate: L3 rotating wave

Date: 2026-08-22.

Status: **frozen before any L3 Jacobian spectrum or L3 perturbation
continuation is evaluated.** The first commit containing this file is the
protocol freeze. Implementation may follow in a later commit, but no threshold,
cell, panel, start vector, perturbation or decision rule may change after an L3
spectral output has been opened.

## 1. Question and claim boundary

The gate asks one question:

> Does local numerical transverse source stability survive at one
> existence-certified non-Anchor scale of the unchanged native K0-H rotating
> relative equilibrium?

A pass supports only local numerical stability evidence at L3 in the declared
spectral and nonlinear panels. Together with the Anchor result it would give
two tested scales, not stability of L0--L5, a complete spectral enclosure,
formation, noise robustness, an internal phase, mechanics, interactions or
mass.

The downstream Loop--Center compatibility gate remains closed until this run
and its critical review both pass.

## 2. Cell selection before spectral inspection

The selection base is clean main revision

```text
e10da5cad0ad85868b8c33ace9e3dd8c5baae9a6
```

At that revision the repository contains no L3 stability, eigenvalue,
multiplier or spectrum artifact. The only L3 numerical values found by the
selection audit are balance roots and continuum-scaling replays.

The frozen selection rule is:

1. test the refinement direction below the Anchor, so L0 and L1 are excluded;
2. exclude L2 because it is the Anchor parameter cell already tested;
3. among the certified finer cells L3, L4 and L5, select the smallest full-FIFO
   state dimension before any spectral calculation.

This selects **L3**. It is the first finer cell, halves the step size and doubles
the horizon relative to the Anchor while preserving

\[
H\alpha=12,
\qquad
\eta/\alpha=15.
\]

L4 and L5 would increase computational cost without improving the first
binary discrimination: Anchor-only stability versus stability at one finer
scale. No stability proxy, short continuation or exploratory Ritz value was
used in this choice.

## 3. Frozen candidate and provenance

The full model tuple is

\[
d=2,quad \varepsilon=0,quad M_0=1,quad
\alpha=0.005,quad H=2400,quad \eta=0.075,
\]

\[
\sigma_{\rm rep}=1,quad \sigma_{\rm att}=3,quad
A_{\rm rep}=1,quad A_{\rm att}=3.5,
\]

with delta deposition and no noise. The candidate identifier is

```text
k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1
```

The 120-dps certified L3 center is frozen as

\[
R_3=
0.944805811705743656419366118422595657454474452804188781825799206245348464567689511866917417017911971955244464,
\]

\[
\theta_3=
0.00790666146243552374938496703030974246197803459527409259815696583141708245813094145986593003659167675765833059.
\]

The execution must verify these Git blobs before constructing the state:

| dependency | frozen Git blob |
| --- | --- |
| refinement-ladder JSON | `66e8681c2b2e9aa7309a48acba15bb8dc33143f5` |
| foundation-audit JSON | `622c06c3d9c2ad24819e39daf5c9bd86f90c515a` |
| Anchor-stability JSON | `1c9d5746c9553d9cb8031b58258e6d613f1633d9` |
| full-FIFO stability module | `9defb5a6876371202e1ba57cea030c997b9c6edd` |
| rotating-wave balance module | `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d` |

The runner must also confirm that both registered interval panels certify L3
and that the independent foundation replay contains the same L3 cell. Any
provenance mismatch blocks execution rather than becoming a scientific fail.

## 4. Co-rotating map and mandatory controls

For

\[
Y_n=(x_n,x_{n-1},\ldots,x_{n-H+1})\in\mathbb R^{4800},
\]

use the existing analytic co-rotating map and sparse Jacobian

\[
\mathcal G_{\theta_3}(Y)=\mathcal R(-\theta_3)\mathcal F(Y).
\]

No finite-difference Jacobian may be used for the L3 spectrum. Before an
Arnoldi panel is accepted, all of the following must pass:

1. the double-precision circular history is fixed by \(\mathcal G_{\theta_3}\)
   to maximum component error at most \(10^{-14}\);
2. the Jacobian has shape \(4800\times4800\) and exactly 19196 stored entries;
3. the existing unrelated \(H=17\) centered finite-difference test passes at
   relative tolerance \(2\,10^{-9}\);
4. the unrelated production-kernel/FIFO-shift reconciliation passes at
   absolute and relative tolerance \(2\,10^{-15}\);
5. the analytic rotation tangent has relative residual at most \(10^{-10}\),
   and both common-translation tangents at most \(10^{-10}\);
6. the D0 quotient test removes a common translation and proper rotation to
   absolute error below \(4\,10^{-15}\).

Unit-test failure, provenance failure, a dirty execution tree or a failed
full-map control yields `execution-blocked`; it is not evidence for or against
stability.

## 5. Frozen spectral panels

Both panels request largest-modulus Ritz pairs from the analytic sparse
Jacobian. They deliberately use different deterministic start vectors. They
remain two configurations of the same SciPy/ARPACK backend and therefore are
not an independent spectral proof.

| panel | eigenpairs | Arnoldi subspace | tolerance | max iterations | start |
| --- | ---: | ---: | ---: | ---: | --- |
| primary | 32 | 128 | \(10^{-10}\) | 40000 | S1 |
| convergence | 48 | 192 | \(10^{-12}\) | 80000 | S2 |

For zero-based state index \(k\),

\[
S1_k=\sin(\sqrt2(k+1))+\cos(\sqrt3(k+1/2)),
\]

\[
S2_k=\sin(\sqrt5(k+1/4))-\cos(\sqrt7(k+3/4)),
\]

followed by Euclidean normalization.

Every returned pair must have normalized residual at most \(10^{-8}\). The
known symmetry subspace is fixed before the spectrum:

- global rotation with multiplier 1;
- two common translations with multipliers \(e^{\pm i\theta_3}\).

An eigenvector receives a symmetry label only at normalized overlap at least
0.99 with the corresponding analytic subspace. Both panels must recover all
three symmetry multipliers within \(10^{-7}\).

The leading transverse value from the primary panel must have a partner in the
convergence panel within \(10^{-5}\) in the complex plane and \(10^{-6}\) in
modulus. ARPACK nonconvergence, missing symmetry modes, residual failure or
panel disagreement is `source-stability-inconclusive`. No alternative start,
shift-invert target, extra iteration budget or third panel may be opened for
the registered decision.

## 6. Frozen nonlinear perturbation panel

The normalized continuation horizon is inherited from the Anchor:

\[
\alpha N=50.
\]

Thus L3 runs exactly 10000 co-rotating updates and samples every 20 updates,
again every 0.1 memory time. The horizon covers about 12.59 rotations. The
perturbation scale is

\[
\delta=10^{-7}R_3.
\]

Seven continuations are frozen:

1. exact unperturbed history;
2. visible radial displacement \(+\delta e_x\) of the current point only;
3. visible radial displacement \(-\delta e_x\);
4. visible tangential displacement \(+\delta e_y\) of the current point only;
5. visible tangential displacement \(-\delta e_y\);
6. \(+\delta\) times the deterministic full-history direction
   \(\sin(0.37k)+\cos(0.11k)\), projected away from all three analytic
   symmetry tangents and normalized;
7. the negative of that full-history direction.

Distance is the unchanged D0 metric after optimal common translation and
proper rotation. A nonzero arm stops if the distance becomes nonfinite or
exceeds 0.25 times the reference D0 norm. No noise is used.

## 7. Frozen decision rule

Define `spectral-controls` as all provenance, full-map, panel, symmetry,
residual and agreement checks passing.

The decision is **`unstable-source-fail`** only if:

1. `spectral-controls` passes;
2. both panels contain the matched transverse multiplier with
   \(|\lambda|>1+10^{-6}\); and
3. at least one registered nonzero perturbation reaches amplification at
   least 100 in D0 distance before or at stopping.

The decision is **`numerically-stable-source-pass`** only if:

1. `spectral-controls` passes;
2. every returned transverse multiplier in both panels satisfies
   \(|\lambda|<1-10^{-4}\);
3. every registered nonzero perturbation completes without stopping, never
   exceeds 10 times its initial D0 distance and ends at or below 0.1 times its
   initial distance; and
4. the exact control remains below absolute D0 distance \(10^{-10}\).

Every other completed outcome is **`source-stability-inconclusive`**. In
particular, the interval between transient amplification 10 and 100 is
deliberately inconclusive. A fail does not invalidate the certified L3 balance
root; it invalidates the downstream stability premise.

## 8. Registered diagnostics that do not decide the gate

For each leading matched transverse multiplier report

\[
\gamma_3=-\frac{\log|\lambda_3|}{\alpha}
\]

and compare it with the existing Anchor value. Also report conjugacy,
translation/rotation overlaps, the complete returned Ritz tables, maximum
transient amplification, mirrored-sign differences and the exact-control
floor. These diagnostics may motivate a later protocol but cannot rescue or
downgrade the frozen P1 decision.

## 9. Execution, artifacts and computational stops

The planned executable is

```text
experiments/current/dynamics/rotation/scalar_memory_rotating_wave_l3_stability_gate.py
```

It must start from a clean committed revision containing this unchanged
protocol. The implementation commit is allowed to add code and tests but not
to alter the frozen scientific choices above. The runner must write

```text
reports/dynamics/rotation/scalar_memory_rotating_wave_l3_stability_2026-08-22.json
reports/dynamics/rotation/scalar_memory_rotating_wave_l3_stability_2026-08-22.md
```

and record execution revision, protocol freeze revision, dependency blobs,
SciPy/NumPy/Python versions, ARPACK exceptions and all returned values.

The two registered ARPACK `maxiter` values and the nonlinear stopping radius
are the only scientific computational stops. An external interruption,
machine shutdown or unrelated resource failure is `execution-incomplete` and
may be rerun only from the same clean revision with identical inputs. It may
not change the result semantics.

## 10. Mandatory critical review

Before status or Paper claims change, a separate review must audit:

1. prospective selection and absence of prior L3 spectra;
2. protocol and dependency hashes;
3. implementation agreement with the production kernel and the Anchor path;
4. symmetry classification, ARPACK convergence, residuals and panel matching;
5. non-normal transient growth and mirrored perturbations;
6. the gap between returned largest-modulus Ritz pairs and a complete spectral
   enclosure;
7. exact distinction between a prepared relative equilibrium, formation,
   internal topology, mechanics and mass.

Only an upheld `numerically-stable-source-pass` may open P2. No outcome opens
formation, noise, topology, mechanics or interactions directly.
