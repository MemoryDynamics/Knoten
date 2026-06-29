# Paper 0 - Mathematical Anchor Paper

Working title:

**Self-Interacting Dynamics with Exponential Memory: Markovian Embedding, Contractive Memory Fibres, and Metastability**

## Role

Paper 0 is the conservative mathematical anchor for the project and can be
used as supplementary mathematical material for Paper I. It defines the
discrete self-interacting stochastic process with exponential forgetting,
proves the direct structural statements, and frames knots as metastable
objects diagnosed through residence times, memory weight, autocorrelation,
local relaxation, and transfer-operator modes. It is not meant to carry a
standalone numerical claim that robust knots exist across parameter ranges.

The paper now states the more general memory update
`rho_{n+1}=(1-lambda_m) rho_n + beta G_sigma`. The previously used
`alpha` form is the normalized convention `lambda_m=beta=alpha`, which
preserves unit memory mass for normalized kernels and unit-mass initial data.
The current figures and simulation pipeline use this normalized convention.

It deliberately does not claim derivations of spacetime, Lorentz kinematics,
quantum dynamics, Standard-Model structure, physical masses, or constants.
Those topics are treated only as future-work directions.

Concrete companion locations:

- Paper II, propagation and spacetime-kinematics programme:
  <https://github.com/MemoryDynamics/Knoten/tree/main/paper/paper_ii>
- Paper III, planned quantum and Standard-Model programme roadmap:
  <https://github.com/MemoryDynamics/Knoten/tree/main/paper/paper_iii>

## Files

- `main.tex`: LaTeX source.
- `references.bib`: bibliography for the mathematical anchor.
- `generate_figures.py`: reproducible figures used by the paper.
- `fig_memory_weights.pdf`: exponential memory weights.
- `fig_transfer_spectrum.pdf`: small reproducible transfer-diagnostic example.

## Build

From this directory:

```powershell
python generate_figures.py
latexmk -xelatex main.tex
```

If `latexmk` is unavailable, run `xelatex`, `bibtex`, `xelatex`, `xelatex`.

## Companion Pipeline

The repository-level script

```powershell
python experiments/anchor_paper_pipeline.py
```

runs a small parameter sweep, records reduced augmented-state features, and
writes residence, autocorrelation, and transfer-operator diagnostics to
`results/anchor_paper/pipeline_summary.json`. This is a pipeline sanity check, not the Long-Run metastability campaign for Paper I.
