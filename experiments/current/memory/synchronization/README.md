# Synchronization Experiments

Status: planning scaffold.

Initial reusable diagnostics live in `src/emergenz_knoten/synchronization.py`.

This directory is for experiments that test whether memory-driven knots can
synchronize through shared or coupled fields. The goal is not to simulate a
quantum field theory directly. The goal is to define measurable external and
internal observables for one or more knots.

## Core Question

```text
Do two or more metastable knots develop reproducible collective modes that live
in a common low-dimensional external response sector?
```

This replaces the weaker question of whether one trajectory has an occupancy
dimension near three.

## Minimal Objects

A single-knot run should provide:

- `x_center(t)`: coarse external center, for example a rolling mean, dominant
  residence voxel center, memory centroid, or response center induced by an
  external probe field;
- `external_response(t)`: optional coarse field-facing observable, such as the
  displacement of the knot center or shape under a weak applied probe;
- `shape_tensor(t)`: covariance or inertia tensor around the current knot
  center;
- `radius(t)`: scalar size proxy from the shape tensor;
- `mode_coefficients(t)`: low-rank PCA/SVD coefficients of local memory or
  trajectory windows;
- `phase(t)`: optional, only if a robust cyclic mode exists;
- `residence(t)`: residence and escape diagnostics.

A two-knot run should additionally provide:

- cross-correlations between centers, radii, modes, and phases;
- lagged response curves after perturbing one knot;
- response matrix between knot observables;
- effective response rank;
- phase-locking value when phases are defined.

## First Protocol

1. Select a parameter slice that already shows long residence or stable local
   structure. Do not select by `D_occ` alone.
2. Generate or reuse seed ensembles for isolated single-knot candidates.
3. Extract per-run observables with fixed windows and fixed sampling.
4. Cluster runs by observable signatures to estimate basin/knot types.
5. Initialize two candidates from compatible basin types.
6. Run three coupling modes:
   - shared memory field;
   - weak cross-potential between separated memory fields;
   - no coupling control.
7. Measure synchronization diagnostics at multiple lags.
8. Report only effects that separate from the no-coupling control across seeds.

## Acceptance Criteria

A synchronization signal is interesting only if:

- residence remains long enough to define two knot identities;
- cross-correlations exceed no-coupling controls;
- phase-locking or mode-locking is stable across seeds;
- response-rank is lower than the internal state dimension;
- the same response subspace appears under small parameter perturbations.

## Near-Term Implementation Tasks

1. Add a `single_knot_observables.py` extractor for existing long-run outputs.
2. Add tests on synthetic two-oscillator trajectories for phase-lock and
   response-rank metrics.
3. Add a small two-knot pilot runner after the extractor is validated.
4. Produce a report that compares isolated, coupled, and no-coupling controls.

## Guardrails

- Do not call synchronized modes quantum fields.
- Do not call internal labels charge, color, or flavor until they are stable
  labels under interactions.
- Do not require the internal embedding dimension to be three.
- Treat seeds as basin samplers.
