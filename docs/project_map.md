# Projektkarte

Stand: 2026-06-14.

## Grobstruktur

```text
src/emergenz_knoten/        # kanonischer Paketkern
experiments/                # reproduzierbare und historische Experiment-Entry-Points
data/raw/                   # unveraenderte Rohdaten und Platzhalter
data/processed/             # kuratierte Auswertungen und JSON/NPY/NPZ-Artefakte
figures/                    # papernahe und draft-Figuren
paper/                      # aktuelle Paper-I- und Paper-II-Quellen
docs/                       # ReadTheDocs/MkDocs, Claim-Register, Projektkarte
reports/                    # datierte Audits und Ergebnisberichte
tests/                      # schnelle Unit-/Smoke-Tests
```

`main` ist die aktuelle Arbeitslinie. Der historische `cleanup`-Branch bleibt
als Referenz bestehen, neue Arbeit soll aber auf `main` laufen.

## Kanonische Schicht

Die aktuelle Paket-API lebt unter `src/emergenz_knoten`:

- `core.py`: finite-memory Update, `SimulationConfig`, NumPy- und
  optionale Numba-Simulation.
- `kernels.py`: exponentielle Gewichte und single/double Gaussian
  Gradienten.
- `diagnostics.py`: geometrische Dimensions- und Residence-Diagnostiken.
- `experiments.py`: `SimulationRunner`, NPZ/JSON-I/O.
- `simulation.py`: Legacy-Kompatibilitaetslayer.

Diese Schicht ist die Basis fuer neue Arbeit. Historische Skripte sollen nur
noch dann direkt erweitert werden, wenn ein reproduzierbarer Vergleich zum
Paketkern vorliegt.

## Historische Skriptfamilien

### Knoten- und Trajektorienmodelle

- `experiments/knot_stability/Knoten.py`
- `experiments/knot_stability/Knoten3D.py`
- `experiments/knot_stability/Knoten3D_prism.py`
- `experiments/knot_stability/knot_chi_scan.py`

Rolle: fruehe memory-driven self-avoiding trajectories, Knotenbildung,
metastabile Spuren und Residence-Intuition.

### Spektral-/Kovarianzdimension und Heatmaps

- `experiments/dimension_selection/DimensionsHeatmap*.py`
- `experiments/dimension_selection/plotD*.py`
- `figures/draft/heatmap_*dimension*.pdf`
- `data/processed/heatmap/`

Rolle: parameterabhaengige Schaetzung von Spektral-/Kovarianzdimension und
Fitqualitaet. Der GPU-Zweig ist langlaufend und muss kontrolliert gestartet
werden.

### Zwei-Skalen-Kernel / Dimension Selection

- `experiments/dimension_selection/2SkalenKernel/`
- Besonders wichtig: `emergent_3D_final.py`, `emergent_3d_scan.py`,
  `SpecCovFrac.py`, `Ueff.py`, `rho.py`

Rolle: Repulsion/Attraction- bzw. Zwei-Skalen-Kernel als moeglicher Mechanismus
fuer stabilere effektive Dimensionen und metastabile Strukturen.

### Fraktale / Occupancy Dimension

- `experiments/fractal_analysis/Fraktale/FD2.py`
- `experiments/fractal_analysis/Fraktale/resultsN.csv`
- `experiments/fractal_analysis/analyze_dimension_claim.py`
- `experiments/fractal_analysis/reproduce_dimension_pilot.py`

Rolle: Quelle des archivierten `D_occ ~ 2.8`-Long-N-Befunds und aktueller
Reproduktionspfad fuer kleine/mittlere `N`.

### Retardierung, Lichtkegel, effektive Signalgeschwindigkeit

- `experiments/propagation_speed/PaperII3D_*.py`
- `figures/draft/diagram*.pdf`
- `figures/draft/front_*`
- `figures/draft/diffusive_*`

Rolle: numerische Grundlage fuer endliche Antwortzeiten, Time-of-flight,
effektive Fronten und operationalen Lichtkegel. Der Claim ist wichtig, aber
aktuell nachrangig gegenueber Paper 0/I-Haertung.

### OU-Limit und analytische Figuren

- `experiments/ou_limit/`
- `figures/draft/fig_OUlimit.pdf`
- `figures/draft/fig_alpha_hbar_eff*.pdf`

Rolle: OU-Grenzfall, Relaxations-/Regime-Diagramme und papernahe
Visualisierungen.

### Legacy

- `experiments/legacy/`
- `experiments/legacy/scripts/highN_regime*.py`

Rolle: fruehere Referenz- und Validierungslaeufe. Nicht loeschen; bei neuer
Nutzung zuerst Parameter, Seed und Outputpfad manifestieren.

## Dokumentation

ReadTheDocs/MkDocs:

- `.readthedocs.yaml`
- `mkdocs.yml`
- `docs/index.md`
- `docs/current_status.md`
- `docs/non_markovian_basis.md`

Kuratierte Projekt-Dokumente:

- `docs/architecture_overview.md`
- `docs/experiment_catalog.md`
- `docs/reproducibility_status.md`
- `docs/hardening_plan.md`
- `docs/paper_claims.md`
- `docs/action_matrix.md`
- `docs/THEORETICAL_CONTEXT.md`

Datierte Reports:

- `reports/dimension_claim_seed_audit_2026-06-13.md`
- `reports/dimension_reproduction_results_2026-06-13.md`
- `reports/fractal_parameter_landscape_reading_2026-06-13.md`
- `reports/fractal_alpha_sweep_pilot_historical_30k_2026-06-13.md`

## Naechste Zielstruktur

Additiv, ohne historische Daten zu zerstoeren:

```text
src/emergenz_knoten/
  markov/
    dataset.py          # augmentierte Features und lagged datasets
    transition.py       # counts, transition matrices, spectra
    validation.py       # ITS, CK, spectral gaps
    metastability.py    # PCCA-/Membership-Schicht
```

Ziel: die bestehende geometrische Diagnostik um eine dynamische
Operator-Schicht erweitern. Dadurch koennen Knoten als metastabile Mengen des
augmentierten Speicherprozesses getestet werden.

## Aufraeumprinzip

1. Historische Skripte erhalten.
2. Neue Experimente ueber Paketkern und klare Entry-Points bauen.
3. Parameter, Seeds, Runtime und Outputpfade manifestieren.
4. Alte Resultate nur dann als Paper-Evidenz nutzen, wenn ihre Herkunft und
   Diagnosevariante dokumentiert ist.
5. Starke physikalische Claims erst nach Negativkontrollen, Seed-Ensembles und
   stabilen Fitfenstern formulieren.
