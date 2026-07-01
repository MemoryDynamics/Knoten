# Aktueller Stand

Stand: 2026-07-01.

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

Der erste Baseline-Seed-Satz ist abgeschlossen; die passenden Kontroll-Seed-
Saetze fuer `eta_zero` und `single_scale` liegen inzwischen ebenfalls lokal
vor und muessen als naechstes zusammengefuehrt werden.

Der initiale Baseline-Lauf:

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
diesem Lauf. Der naechste Paper-I-Engpass ist nicht ein weiterer einzelner
Long-Run, sondern die gemeinsame Statistik der Baseline-, `eta_zero`- und
`single_scale`-Seed-Ensembles.

## Dimensionsbefund

Belastbar aus dem Archiv:

- Quelle: `experiments/fractal_analysis/Fraktale/resultsN.csv`.
- Staerkster Long-N-Gruppenbefund: `embedding dim = 5`, `N = 60,000,000`,
  fuenf Runs, `mean D_occ = 2.810559`, population std etwa `0.029533`.

Belastbar aus den neuen kontrollierten Reproduktionslaeufen vom 2026-07-01:

- Die allgemeine Memory-Variante ist technisch umgesetzt:
  `rho_{n+1}=(1-lambda_m)rho_n+beta G_sigma`, mit altem Spezialfall
  `beta=lambda_m=alpha`.
- Kernel-Skalen-, Memory-Zeit- und Memory-Masse-Scans sind abgeschlossen und
  reportgebunden committed.
- Der einzelne High-N-Referenzlauf `d=5`, `N=100,000,000`, `alpha=0.01`,
  `beta/alpha=1`, `sigma_att=0.15`, Seed `1`, liefert `D_occ=2.013`,
  `D_cov=1.337`, `D_spec=1.210`.
- Bei `N=1,000,000`, Seeds `1..5`, zeigt keine getestete Achse ein stabiles
  Plateau nahe `D=3`. Die groessten `D_occ`-Mittelwerte liegen unter `1.6`.
- Niedrigeres `beta/alpha` kann in dieser Pipeline `D_occ` erhoehen, erzeugt
  aber keine robuste Dreidimensionalitaet.

Lesart: Der archivierte Near-3-Befund bleibt als historischer/high-N-Befund
interessant, ist aber nicht durch die aktuelle kontrollierte Reproduktions-
pipeline bestaetigt. Fuer Paper I/II darf daraus kein `d=3`-Selektionsclaim
abgeleitet werden. Der naechste wissenschaftliche Schritt ist Reconciliation:
Parameterdefinitionen, Schaetzfenster, Sampling, historische Skripte und
Negativkontrollen gegeneinander pruefen.

## Naechste technische Schritte

1. Baseline, `eta_zero` und `single_scale` seedweise zusammenfuehren.
2. Kontrollstatistik als Report committen und Paper-I-Evidenzstatus bewerten.
3. Dimension-Reproduction nicht weiter blind verlaengern, sondern zuerst den
   Archivbefund gegen aktuelle Parameterdefinitionen, Schaetzfenster und
   Sampling rekonstruieren.
4. Danach Voxel-/Lag-/Sampling-Sensitivitaet entscheiden.
5. Erst danach eine Paper-I-Evidenztabelle formulieren.
6. Transferoperatorfeatures fuer Long-Run-Daten erweitern, wenn die
   Residence-Kontrollen tragen.
