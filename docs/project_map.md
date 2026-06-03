# Projektkarte

Stand: 2026-05-22.

## Grobinventar

Ohne virtuelle Umgebungen und IDE-Dateien liegen aktuell vor:

| Typ | Anzahl | Rolle |
| --- | ---: | --- |
| Python-Skripte | 43 | Simulationen, Scans, Plot-Generatoren |
| PDFs | 27 | Paper-Figuren, Diagramme, Heatmaps |
| PNGs | 7 | Ergebnisplots in Unterordnern |
| NPY/NPZ | 13 | Checkpoints, Progress-Dateien, Ergebnisdaten |
| CSV/TXT | 9 | Fraktal- und Skalierungsresultate |

Git-Zustand beim Audit: Repository existiert, aber es gibt noch keinen Commit;
praktisch alle Projektdateien sind unversioniert.

## Historische Skriptfamilien

### Fruehe Knoten- und Trajektorienmodelle

- `Knoten.py`
- `Knoten3D.py`
- `Knoten3D_prism.py`
- `fig1_knot_trajectory.pdf`, `fig2_knot_scatter.pdf`,
  `fig3_knot_trajectory.pdf`

Rolle: fruehe memory-driven self-avoiding trajectories, Visualisierung von
Knotenbildung und metastabilen Spuren.

### Spektral-/Kovarianzdimension und Heatmaps

- `DimensionsHeatmap.py`
- `DimensionsHeatmapOpt.py`
- `DimensionsHeatmap2Opt.py`
- `DimensionsHeatmap3Opt.py`
- `DimensionsHeatmap4OptGPU.py`
- `plotD.py`, `plotDgpu.py`
- `progress*.npy`, `progress*.npz`
- `heatmap_*dimension*.pdf`, `spectral_dimension_heatmap_optimized.pdf`

Rolle: parameterabhaengige Schaetzung von Spektraldimension,
Kovarianzdimension und Fitqualitaet. Der GPU-Zweig enthaelt sehr lange Laeufe
und Checkpoint-Artefakte.

### Retardierung, Lichtkegel, effektive Signalgeschwindigkeit

- `PaperII3D_4Plots.py`
- `PaperII3D_4Plots2.py`
- `PaperII3D_5Plots1.py`
- `PaperII3D_5Plots2.py`
- `diagram1_retarded_response.pdf`
- `diagram2_time_of_flight.pdf`
- `diagram3_ceff_scaling.pdf`
- `diagram4_light_cone.pdf`
- `front_*`, `diffusive_*`

Rolle: numerische Stuetze fuer endliche Antwortzeiten, Time-of-flight,
effektive Fronten und operationalen Lichtkegel.

### Zwei-Skalen-Kernel / Dimension Selection

- `2SkalenKernel/`
- Besonders wichtig: `emergent_3D_final.py`, `emergent_3d_scan.py`,
  `SpecCovFrac.py`, `3Plots2Traj.py`, `Ueff.py`, `rho.py`
- Ergebnisse: `2SkalenKernel/results*/D_vs_*.png`,
  `2SkalenKernel/checkpoint_emergent3d.npz`

Rolle: Wechsel von Ein-Skalen-Gauss auf Repulsion/Attraction bzw.
Zwei-Skalen-Kernel. Das ist derzeit der wichtigste Zweig fuer die Frage, ob
eine makroskopisch stabile effektive Dimension nahe 3 bevorzugt wird.

### Fraktale / Occupancy Dimension / Finite-Size Scaling

- `Fraktale/FD2.py`
- `Fraktale/Fraktaldimension.py`
- `Fraktale/fit_n_plot.py`
- `Fraktale/results_plot.py`
- `Fraktale/results*.csv`, `Fraktale/scan_results.txt`,
  `Fraktale/N_*.png`

Rolle: Box-counting/Occupancy-Dimension, Skalierungsanalyse ueber `N`,
Embedding-Dimension-Tests und Ergebnisplots.

### Analytische oder schematische Figuren

- `OU-Limit.py`
- `Oszillationen.py`
- `EmergenzGravitation.py`
- `emergenz_2regime.py`
- `fig_alpha*.py`, `fig_Gamma_alpha.py`, `fig_Hlamda_alpha.py`

Rolle: OU-Grenzfall, Relaxations-/Regime-Diagramme, heuristische
Parameterkarten und papernahe Visualisierungen.

## Zielstruktur fuer die naechste Refactor-Runde

Diese Struktur sollte erst nach einem Baseline-Commit der bestehenden Dateien
aktiv durch Verschieben/Refactoring umgesetzt werden:

```text
src/emergenz_knoten/
  core.py              # Speicherupdate, Kernel, Einzelschritt
  kernels.py           # Gaussian, double Gaussian, austauschbare Kernel
  diagnostics.py       # D_cov, D_occ, D_spec, Residence, Relaxation
  experiments.py       # gemeinsame Runner/Seed/Checkpoint-Hilfen

experiments/
  dimension_selection/
  propagation_speed/
  knot_stability/
  ou_limit/

data/
  raw/
  processed/

figures/
  draft/
  paper/

paper/
  paper_i/
  paper_ii/
```

## Aufraeumprinzip

Nicht zuerst Dateien nach Geschmack sortieren, sondern zuerst Bedeutung
konservieren:

1. Historische Skripte versionieren.
2. Pro Skriptfamilie klaeren: Eingaben, Outputs, Laufzeit, relevante Claims.
3. Einen kanonischen Modellkern extrahieren.
4. Alte Skripte nur noch als Reproduktionshistorie behalten oder in
   `experiments/legacy/` verschieben.
