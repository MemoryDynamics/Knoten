# Paper III - Internal Knot Structure and Synchronization Programme (planned)

This directory is a planning surface for a later companion programme. It is not
a result of Paper 0 and should not be cited as evidence for quantum mechanics,
particle spectra, gauge structure, physical constants, or Standard-Model
phenomenology. It deliberately keeps that route open as a future research
question, but only behind reproducible knot, synchronization, and collective-mode
evidence.

## Reframed Aim

The current working direction is no longer that the minimal process must first
select an ambient dimension `d=3`. The stronger and more useful question is:

```text
Can memory-driven knots be internally high-dimensional while presenting a
low-dimensional, shared external interaction sector?
```

In that framing, a knot is treated as a metastable nonlinear object with:

- internal degrees of freedom carried by its memory field and trajectory
  history;
- external collective observables visible to other knots;
- relaxation modes and possible phase-like coordinates;
- response functions under perturbation or coupling.

A later Standard-Model analogy would require stable internal labels and a common
external sector, not merely a single trajectory with an occupancy dimension near
three.

## Working Hypotheses

These are hypotheses, not claims:

1. **Internal/external split**: a knot may have high-dimensional internal state,
   while external observers interact only with a reduced set of collective
   coordinates.
2. **Common external sector**: interacting knots may synchronize onto a shared
   low-dimensional response subspace. The relevant diagnostic is closer to the
   rank and stability of a response matrix than to the embedding dimension of a
   single run.
3. **Synchronization before particles**: coherent multi-knot behavior should be
   studied like a nonlinear synchronization problem. The laser analogy is useful
   at this level: stochastic microscopic degrees of freedom can produce a stable
   macroscopic order parameter under feedback, gain, and damping.
4. **Internal labels as modes**: charge-, color-, flavor-, or spin-like labels,
   if they ever appear, should first be treated as stable internal mode labels,
   not as assumed fundamental quantum numbers.

## Required Demonstrations

A credible Paper-III path requires the following, in order:

1. **Single-knot mode extraction**
   - center or external coordinate;
   - size/radius and shape tensor;
   - principal internal modes;
   - relaxation spectrum;
   - phase-like or cyclic coordinates, only if measured robustly.

2. **Seed-to-basin statistics**
   - seeds are basin samplers, not nuisance noise;
   - estimate `P(knot type | parameters, seed ensemble)`;
   - separate transient dimension from persistent knot type.

3. **Two-knot synchronization pilot**
   - initialize two separated knot candidates;
   - allow shared or weakly coupled memory fields;
   - measure phase locking, cross-correlation, response delay, residence
     stability, and response-rank.

4. **Shared external subspace test**
   - infer the dimension/rank of observable response modes between knots;
   - require the same external subspace across seeds and small parameter
     perturbations;
   - only then discuss a 3D external sector.

5. **Multi-knot field limit**
   - fields are collective modes of many synchronized knots;
   - particle-like objects are stable localized excitations of those modes;
   - this remains future work until synchronization and response-rank are
     reproducible.

## Non-Claims

This programme does not currently claim:

- emergence of quantum mechanics;
- derivation of `hbar`, `c`, or physical mass;
- Lorentz invariance;
- Standard-Model gauge groups;
- real particles;
- that `d=3` is selected by the current simulations.

## Concrete Next Step

The next implementable unit is not another dimension scan. It is a
synchronization measurement stack:

```text
single-knot observables
    -> mode extraction
    -> two-knot coupling pilot
    -> response matrix
    -> response-rank and phase-lock diagnostics
```

See `experiments/synchronization/README.md` for the first experimental protocol.
