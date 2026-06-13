# Theoretical Context — Emergenz Knoten (concise)

This document extracts the core theoretical claims from the ChatGPT-derived
notes in `docs/ChatGPT Chatverläufe/` and links them to the concrete
experimental entry points in `experiments/`.

## Core claims (short)

- Minimal dynamical model: a discrete order parameter n and a state
  σ_n = (x_n, ρ_n) with stochastic updates (trajectory + memory) and
  irreversible memory updates.

- Emergence of time: Arrow-of-Time arises from memory relaxation; an
  emergent proper time scale τ_p ∼ 1/α; time as an integration parameter,
  not identical to the discrete index n.

- Emergence of space & kinematics: spatial structure and an effective
  light-speed c emerge from trajectory statistics and maximal drift.
  Local Lorentz behaviour and macroscopic GR-like coupling are
  conceptually compatible.

- Knot dynamics & phases: clear knot typology (free, transient, attractor,
  metastable, destructor); phase transitions controlled by
  Λ = η/(α ε); mean free path is an order parameter; mass emerges as
  an attractor relaxation scale.

- Microscopic → quantum: linearization near attractors yields complex
  structures; Schrödinger / Dirac normal forms emerge with
  ℏ_eff ∼ ε^2/α; spinor structure appears from frame redundancies.

- Parameter elimination: ε, η, α become replaceable by emergent
  physical quantities (ℏ, c, m, τ_p) in the effective description.

## Practical mapping to repository experiments

- `experiments/reference_experiment.py`
  - Purpose: small, reproducible reference runs; computes
    `D_cov`, `D_occ`, `residence_statistics` (connects to claims about
    effective dimension and knot diagnostics).

- `experiments/dimension_selection/` (Heatmaps, 2SkalenKernel)
  - Purpose: map `D_spec` / spectral dimension across parameter space
    (connects to Emergence of Space & kinematics, two-scale kernels).

- `experiments/fractal_analysis/` (Fraktale)
  - Purpose: occupancy dimension, box-counting, finite-size scaling
    (connects to knot occupancy and fractal-like spatial structure).

- `experiments/propagation_speed/` (Paper II scripts)
  - Purpose: time-of-flight, retarded response, operational light-cone
    (direct test of emergent c and propagation scaling).

- `experiments/knot_stability/`
  - Purpose: trajectory-based knot tests, scans for metastable
    attractors and lifetime statistics (connects to Knot dynamics).

- `experiments/cli.py` and `experiments/reference_experiment.py`
  - Use these as canonical entry points for reproducible runs and
    linking with the theoretical claims above.

## Where the Chat notes live

See `docs/ChatGPT Chatverläufe/` for the raw conversational notes used to
compile this summary. Most relevant files included:

- `ErsterEmergenzChat.md` — high-level program, Paper I/II/III split
- `Nebenrechnungen.md` — linearization, effective dimension derivations
- `Skriptreview.md` — script-level corrections and plotting guidance
- OU and mathematical drafts: `OU-Limit.md`, `Mathematische Formulierung der Existenz.md` (if present)

## Recommended next steps (short)

1. Finalize Sections 2 (Minimal Model) and 3 (Memory & Arrow-of-Time)
   formally — these are the mathematical backbone for Paper I.
2. Use `experiments/reference_experiment.py` as a reproducible smoke test
   and then run targeted scans in `dimension_selection/` and
   `propagation_speed/` to gather the diagnostics required for Paper I.
3. Consolidate plotting scripts following `Skriptreview.md` to ensure
   figures are reviewer-proof (use the corrected OU/ℏ_eff-based plots).

---

If you want, I can now:

- Insert short context links into each `experiments/*/README.md` referencing
  the relevant paragraphs above, and
- Produce a short `docs/THEORETICAL_CONTEXT_BRIEF.md` for the paper
  introduction.

Tell me which of these you prefer next.