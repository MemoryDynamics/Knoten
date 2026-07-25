# Response to the Manus Review of Paper 0 and Paper I

Date: 2026-07-26.

## Scope

This note records how the supplied review was checked against the
current repository evidence and how the manuscripts were changed. The review
was useful on positioning and redundancy, but its literature statements were
not accepted without verification.

## Literature verification

### Benaim, Ledoux, and Raimond (2002)

The published model uses the normalized cumulative occupation measure

```text
mu_t = (1/t) integral_0^t delta_(X_s) ds.
```

It is directly relevant to self-interaction and augmented occupation-state
methods, but its time weighting is not exponential. The existing bibliography
also omitted Michel Ledoux from the author list; both Paper 0 and Paper I now
correct this.

- DOI: <https://doi.org/10.1007/s004400100161>

### Benaim and Raimond (2005)

For symmetric interactions on a compact Riemannian manifold, this paper proves
almost-sure convergence of the occupation measure toward the critical set of a
nonlinear free-energy functional and generic convergence toward a local
minimum. This is the relevant benchmark for the hard convergence results that
the present papers do not prove.

- DOI: <https://doi.org/10.1214/009117905000000251>

### Herrmann and Roynette (2003)

The review described this work as using exponential memory. That description
is incorrect. Its drift contains the unweighted full-history integral

```text
integral_0^t Phi(Z_t - Z_s) ds.
```

The paper proves convergence or boundedness for particular one-dimensional
self-attracting interactions. It remains relevant as a strong localization
comparison, but is now cited explicitly as a non-exponential full-history
model.

- DOI: <https://doi.org/10.1007/s00208-002-0370-0>

### Milisic, Meunier, and Roux (2026)

This recent preprint and the associated CIRM presentation are the closest
verified temporal-memory comparison. They introduce aging weights for linear
self-interaction, analyze general convolution kernels, and include a
particular exponential-memory case with an explicit solution. The full SSRN
PDF was protected by an automated access challenge in this review environment;
the abstract, CIRM presentation description, and bibliography were available
and mutually consistent. The manuscript therefore cites the preprint only for
this limited, directly supported description.

- SSRN DOI: <https://doi.org/10.2139/ssrn.6659876>
- CIRM record: <https://doi.org/10.24350/CIRM.V.20483303>

### Kuramoto and mean-field models

No Kuramoto citation was added. Delayed or adaptive Kuramoto models are an
adjacent collective-dynamics literature, but they do not directly support the
single-trajectory deposited-memory model or its current scalar result. Adding
them here would broaden the bibliography without sharpening the novelty
boundary. A mean-field comparison becomes relevant only after a genuine
multi-generator limit is formulated.

## Review disposition

| Review point | Disposition |
| --- | --- |
| Novelty was underpositioned | Addressed by an explicit comparison with cumulative, full-history, aging-kernel, and Markov-embedding literature. The papers no longer present exponential memory or state augmentation alone as novel. |
| Paper 0 sat between paper and supplement | Addressed by calling it a technical companion note, shortening it, removing the unused skew-product section and removing the redundant pipeline narrative. |
| Baseline regularity was vague | Addressed by separate assumptions for the discrete process, continuum scaling, and Hessian linearization. |
| Paper I needed a null hypothesis | Addressed centrally. The exact memory-centroid recursion yields a linear relative mode and an explicit stationary-radius prediction. |
| Numerical evidence was too thin for a nonlinear knot claim | Accepted. Nine active long-run slices agree with the linear prediction to 0.76% median and 1.15% maximum relative error. The nonlinear claim is withdrawn. |
| D_mem near three could mislead | Addressed by removing it as a headline result and stating that it is expected ambient isotropic shape behavior. |
| Knot terminology was suggestive | Addressed by using `localized memory cloud` for the established scalar state and reserving `dynamical knot` for a future nonlinear metastable result beyond controls. |
| Paper dates were stale | Updated to 2026-07-26. |
| Paper 0 and Paper I were redundant | Reduced. Paper 0 carries structural proofs and mathematical caveats; Paper I carries the exact linear null model and numerical test. |

## Revised scientific claim

### Evidence

- The augmented state is Markov and the visible projection is generally not.
- The memory fibre contracts along a fixed visible path.
- The normalized memory centroid obeys an exact affine recursion.
- The locally linear scalar relative mode predicts the measured active
  long-run radii across nine slices with at most 1.15% relative error.
- Matched one- and two-scale kernels collapse on local restoring curvature.

### Inference

The current scalar compact branch is best described as a co-moving linear
relaxation cloud. The earlier two-scale interpretation is not identified in the
sampled Taylor regime.

### Not established

- a nonlinear metastable knot;
- a finite-amplitude phase transition;
- dimension selection;
- a physical mass or particle interpretation;
- spacetime, relativistic, quantum, or Standard-Model structure.

## Remaining publication gap

The revision converts an ambiguous localization story into a controlled
baseline result. Publication strength now depends on whether that result is
sufficient for the chosen venue. A stronger nonlinear paper would still need a
scale-aware almost-invariant set, a reproducible bifurcation, or another
observable that falsifies the linear center-relative null model under matched
controls.
