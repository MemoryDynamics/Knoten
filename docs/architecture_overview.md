# Architekturuebersicht

Stand: 2026-06-29.

Das Projekt besteht aktuell aus vier Schichten:

1. Kernbibliothek (`src/emergenz_knoten`)
2. Experiment-Entry-Points (`experiments/`)
3. Daten, Figuren und Reports (`data/`, `figures/`, `reports/`)
4. Dokumentation (`docs/`, ReadTheDocs/MkDocs)

Die additive Non-Markovian/Markov-Embedding-Schicht ist initial unter
`src/emergenz_knoten/markov/` angelegt. Sie arbeitet indexbasiert auf
Update-Zustaenden `z_n` und Sample-Zustaenden `z_i`; eine physikalische
Zeitparametrisierung wird dort nicht vorausgesetzt. Die Detailarchitektur steht
in [Markov-Architektur](markov_architecture.md), die Akzeptanzkriterien in
[Markov-Anforderungen](markov_requirements.md).

## 1. Kernbibliothek

`src/emergenz_knoten/__init__.py`

- Exportiert den oeffentlichen API-Kern.

`src/emergenz_knoten/core.py`

- Definiert `SimulationConfig`.
- Implementiert `simulate_finite_memory`.
- Implementiert optional `simulate_finite_memory_numba`.
- Berechnet den effektiven Speicherhorizont aus `memory_factor / alpha` und
  `max_memory`.

`src/emergenz_knoten/kernels.py`

- Berechnet exponentielle Memory-Gewichte.
- Berechnet Gaussian- und Double-Gaussian-Gradienten.
- Kapselt die Zwei-Skalen-Struktur aus Repulsion und Attraction.

`src/emergenz_knoten/diagnostics.py`

- `covariance_dimension`
- `occupancy_dimension`
- punktwolkenbasierte `spectral_dimension`
- `residence_statistics`
- `bootstrap_mean_ci`

Wichtig: Die aktuelle `spectral_dimension` ist eine Geometrie-Diagnostik auf
einem Punktwolken-Kernel. Sie ist nicht das Spektrum eines dynamischen
Transferoperators.

`src/emergenz_knoten/experiments.py`

- `SimulationRunner`
- `run_simulation`
- `save_simulation_result`
- `load_simulation_result`
- NPZ/JSON-Serialisierung

`src/emergenz_knoten/markov/`

- `features.py`: reduzierte augmentierte Features aus Position und Memory.
- `dataset.py`: Sample-indexed augmented trajectories und Lagged Datasets.
- `transition.py`: Voxel-Labels, Transition Counts und row-stochastic matrices.
- `validation.py`: Autokorrelation, implied timescales und CK-Fehler.
- `metastability.py`: erste slow-mode und spectral-gap helpers.

`src/emergenz_knoten/anchor.py`

- Kompatibilitaets-Fassade fuer fruehere Paper-0-Imports.

## 2. Dynamisches Modell

Sichtbarer Update:

```text
x_{n+1} = x_n + epsilon * noise_n - eta * grad Phi_n(x_n)
```

Memory-Gewichte:

```text
w_k = alpha * (1 - alpha)^k
```

Der sichtbare Prozess `x_n` ist nichtmarkovsch, weil `grad Phi_n` von der
gespeicherten Vergangenheit abhaengt. Der augmentierte Zustand
`z_n = (x_n, history_n, weights_n)` ist dagegen die natuerliche
Markov-Einbettung.

Algebraisch erzeugt diese Einbettung einen Markov-/Koopman-Operator auf
Observablen von `z_n`. Die Iterationen dieses Operators bilden die relevante
Vorwaerts-Halbgruppe. Das ist aktuell eine theoretische Schicht; im Paketkern
existieren noch keine Operator-Schaetzungen.

## 3. Experiment-Entry-Points

`experiments/reference_experiment.py`

- Kleine reproduzierbare Referenzlaeufe.
- Berichtet `D_cov`, `D_occ` und Residence-Statistik.

`experiments/cli.py`

- Listet und startet kategorisierte Skripte.
- Kategorien: `reference`, `dimension_selection`, `propagation_speed`,
  `knot_stability`, `fractal_analysis`, `ou_limit`, `LQG`.

`experiments/fractal_analysis/`

- Aktueller Schwerpunkt fuer den archivierten Dimensionsclaim.
- Enthalten sind Audit- und Reproduktionsskripte.

`experiments/legacy/`

- Historische Skripte und fruehere Referenzpfade.
- Nicht als neue API behandeln.

## 4. Daten- und Ergebnisfluss

Aktueller Flow:

```text
SimulationConfig
  -> simulate_finite_memory / run_simulation
  -> samples, sample_steps, final memory, weights
  -> diagnostics.py
  -> data/processed/*.json|*.npz
  -> reports/*.md
```

Limit:

- Der kanonische Simulation-Output speichert weiterhin keine vollstaendigen
  Memory-Snapshots pro Samplezeitpunkt.
- Die neue Operator-Schicht nutzt deshalb zunaechst reduzierte
  Memory-Summary-Features.
- Voxelbasierte Zustandszuordnung ist ein erster robuster Baseline-Pfad, noch
  keine finale metastability decomposition.

## 5. Non-Markovian/Markov-Schicht

Aktuelle Struktur:

```text
src/emergenz_knoten/markov/
  __init__.py
  features.py
  dataset.py
  transition.py
  validation.py
  metastability.py
```

Minimaler Flow:

```text
samples + memory summaries
  -> augmented features z_i sampled from z_n
  -> lagged pairs (z_i, z_{i+ell})
  -> state assignment
  -> transition counts
  -> transition matrix
  -> Markov/Koopman operator U_ell
  -> implied timescales / CK / spectral gap
  -> metastable memberships
```

Warum additiv:

- Der bestehende Kern bleibt schlank.
- Historische Diagnostik bleibt reproduzierbar.
- Die neue Schicht kann direkt gegen negative Controls getestet und spaeter um PCCA/HMM/PMM erweitert werden.

## 6. Dokumentation

ReadTheDocs/MkDocs-Dateien:

- `.readthedocs.yaml`
- `mkdocs.yml`
- `docs/requirements.txt`
- `docs/index.md`

Kuratierte Statusseiten:

- `docs/current_status.md`
- `docs/non_markovian_basis.md`
- `docs/reproducibility_status.md`

## 7. Architekturprinzipien

- Neue Features zuerst im Paketkern oder in klaren Experiment-Entry-Points.
- Historische Skripte nicht stillschweigend umdeuten.
- Jede Paper-Evidenz braucht Parameter, Seeds, Outputpfad und Diagnostikversion.
- Nichtmarkovsche Sprache nur dort verwenden, wo klar ist, ob `x_n` oder der
  augmentierte Zustand gemeint ist.
- `z_n` fuer augmentierte Zustaende verwenden; `sigma` nur fuer Kernelbreiten
  wie `G_sigma`.
- Geometrische Dimensionen und dynamische Operator-Spektren getrennt halten.
