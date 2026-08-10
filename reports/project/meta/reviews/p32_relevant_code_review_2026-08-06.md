# P3.2 relevant code and artifact review

Date: 2026-08-06.

## Scope

Reviewed implementation and result lineage:

- `src/emergenz_knoten/retarded_reciprocal.py`;
- `src/emergenz_knoten/local_mediator.py`;
- `src/emergenz_knoten/reciprocal_diagnostics.py`;
- `experiments/current/memory/synchronization/reciprocity/retarded_reciprocal_full_knot_gate.py`;
- `experiments/current/memory/synchronization/reciprocity/measurement_closure_relative_noise_gate.py`;
- `src/emergenz_knoten/hankel_pole_identity.py` and its report/CLI layer;
- `src/emergenz_knoten/source_local_linear.py` and
  `source_local_modal.py`;
- corresponding tests, reports, JSON summaries, and figures.

## Findings

### No dynamics-changing defect found

- The gradient sign matches the corrected repulsive/attractive convention.
- Self coupling is applied once. The `coupling` argument of `path_gradient`
  currently acts only as a zero shortcut; the caller applies `eta`. This name
  is confusing but does not double-apply the coupling.
- The direct arm is bitwise locked to the P3.1 implementation.
- Zero cross coupling makes all four arms bitwise identical.
- The one-way source remains on its channel-off path.
- Each Telegraph direction has an independent local field state. Its finite
  difference update, finite delay, DC normalization, and stability guards are
  covered by tests.
- Relative-noise correlation preserves both node marginals and changes only
  the relative half-noise by the registered square-root law.
- Frequency and damping are divided by `alpha * sample_every`; sparse output
  therefore remains in memory-time units.

### Corrected verification gap

The canonical P3.2 run stored every update. A 500,000-update continuation at
that cadence would allocate several large observable tensors unnecessarily.
The code already accepted sparse `sample_steps`, but no end-to-end regression
proved that this was exact subsampling of the same hidden update path.

`tests/test_retarded_sampling_regression.py` now requires bitwise equality of
dense and every-fifth sampled positions, memory centres, shape tensors, and
mediator readouts. It also requires fitted frequency and damping to remain
unchanged after exact subsampling. This permits `sample_every=10` for the
registered long control without changing the dynamics.

## Artifact curation decision

No reviewed scientific artifact is obsolete enough to delete:

- `reciprocal_local_mode_gate` is the analytic regime-map precursor;
- `reciprocal_full_knot_gate` tests direct nonlinear coupling;
- `retarded_reciprocal_full_knot_gate` tests the fixed delayed channel;
- measurement closure and long-horizon Hankel reports test predictive state
  representations, not the same primary gate;
- the pole-identity audit closes the stored DMD candidate;
- the source-local linear gate removes a known locality limitation and answers
  a distinct architecture question.

Deleting any of these would break the evidence chain. They remain curated,
dated results rather than active competing implementations. No unreferenced
duplicate P3.2 Python script or result was found.

## Remaining limitations

- The P3.2 mediator source is target-specific; only transport is local.
- All continuation seeds branch from one formation checkpoint and are not
  independent basins.
- A fixed relational axis and inserted Telegraph law do not establish a
  physical field, finite continuum signal speed, spin, charge, or dimension.
- A two-seed 500k run can reject a simple accumulation hypothesis but cannot
  support population-level claims.

