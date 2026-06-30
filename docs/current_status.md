# Aktueller Stand

Stand: 2026-06-30.

## Repository

- Arbeitsbranch: `main`.
- Remote: `https://github.com/MemoryDynamics/Knoten`.
- Der kanonische Paketkern liegt unter `src/emergenz_knoten`.
- Die aktive Doku-Oberflaeche ist auf sieben Dokumente reduziert; historische
  Chat- und Paper-Artefakte bleiben Rohmaterial.

## Codekern

- `core.py`: `SimulationConfig`, finite-memory Simulation, Numba-Variante,
  Memory-Horizon `min(max_memory, memory_factor / alpha)`.
- `kernels.py`: exponentielle Memory-Gewichte und Gaussian-Kernelgradienten.
- `diagnostics.py`: `D_cov`, `D_occ`, geometrische `spectral_dimension`,
  Residence-Statistiken und Bootstrap-CI.
- `experiments.py`: Runner und NPZ/JSON-Serialisierung.
- `markov/`: additive Markov-/Transferoperator-Schicht mit reduzierten
  augmentierten Features, Lagged Datasets, Transition Counts,
  row-stochastic operators, implied timescales, CK-Fehlern und slow-mode
  Helfern.
- `anchor.py`: Kompatibilitaets-Fassade fuer fruehere Paper-0-Imports.

Der sichtbare Prozess `x_n` ist wegen des Speichers im Allgemeinen
nichtmarkovsch. Der augmentierte Zustand `z_n=(x_n,rho_n)` bzw. eine konkrete
Memory-Reprasentation ist die Markov-Einbettung.

## Paper-Status

- Paper 0: mathematischer Anker bzw. moegliches Supplement. Es formuliert die
  allgemeine Memory-Form `(1-lambda_m)rho_n + beta G_sigma`, die
  Markov-Einbettung und die kontraktive Memory-Faser. Es behauptet keine
  robuste Knotenexistenz.
- Paper I: Minimalmodell mit synchronisierter Memory- und Markov-Sprache. Die
  starke Knoten-Evidenz muss aus Long-Runs und Kontrollen kommen.
- Paper II: Propagation, `c_eff` und Raumzeit-Kinematik bleiben Folgeprogramm.
- Paper III: Quanten-/Standardmodellprogramm bleibt geparkt.

## Long-Run-Status

Der erste echte Baseline-Lauf ist abgeschlossen:

| Feld | Wert |
| --- | --- |
| Condition | `baseline` |
| Seed | `1` |
| Updates | `10,000,000` |
| Dimension | `3` |
| `alpha` | `0.01` |
| Burn-in | `1,000,000` |
| Sample-Abstand | `1000` Updates |
| Samples | `9001` |
| Laufzeit | `337.997 s` |
| Git-Revision | `c36816e` |
| Bestes Residence-Verhaeltnis | `256 alpha^{-1}` |
| `D_cov` / `D_occ` | `1.699` / `1.792` |

Lesart: Das ist ein starkes Baseline-Signal fuer langlebige Residence in genau
diesem Lauf. Es ist noch kein robuster Paper-I-Befund, weil `eta_zero`,
`single_scale`, weitere Seeds und Sensitivitaeten fehlen.

## Dimensionsbefund

Belastbar aus dem Archiv:

- Quelle: `experiments/fractal_analysis/Fraktale/resultsN.csv`.
- Staerkster Long-N-Gruppenbefund: `embedding dim = 5`, `N = 60,000,000`,
  fuenf Runs, `mean D_occ = 2.810559`, population std etwa `0.029533`.

Belastbar aus neuen Kurzlaeufen:

- `50k` und `100k` koppeln plausibel an den Archivpfad an.
- Bei `N <= 60k` ist kein Near-3-`D_occ` sichtbar.
- Die Kontrollen trennen den Claim noch nicht stark genug.

## Naechste technische Schritte

1. `eta_zero` und `single_scale` fuer denselben Long-Run-Satz laufen lassen.
2. Baseline gegen Kontrollen auswerten und als Report committen.
3. Danach mehrere Seeds oder Voxel-/Lag-Sensitivitaet entscheiden.
4. Erst danach eine Paper-I-Evidenztabelle formulieren.
5. Transferoperatorfeatures fuer Long-Run-Daten erweitern, wenn die
   Residence-Kontrollen tragen.
