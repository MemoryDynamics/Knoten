# Experiment-Katalog

Stand: 2026-06-29.

## Kanonische Entry-Points

| Datei | Thema | Status | Naechste Nutzung |
| --- | --- | --- | --- |
| `experiments/reference_experiment.py` | kleiner Referenzlauf mit `D_cov`, `D_occ`, Residence | aktiv | Smoke-Test und Basis fuer neue Trace-Erweiterung |
| `experiments/cli.py` | kategorisierte Experimentsteuerung | aktiv | Einstiegspunkt fuer vorhandene Skriptfamilien |
| `experiments/fractal_analysis/analyze_dimension_claim.py` | Audit des archivierten `D_occ`-Claims | aktiv | Claim-Register und Paper-Formulierung |
| `experiments/fractal_analysis/reproduce_dimension_pilot.py` | seed-kontrollierte Reproduktion kleiner/mittlerer `N` | aktiv | Naechste Numba-Millionenlaeufe |
| `experiments/anchor_paper_pipeline.py` | Paper-0-Smoke mit augmentierten Features und Transferoperator-Schaetzung | aktiv | schneller Operator-Pipeline-Check |
| `experiments/anchor_sensitivity_analysis.py` | Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet fuer die Markov-Schicht | aktiv | kleine Evidenztabelle und P0.2-Validierung |
| `experiments/long_run_metastability.py` | Long-N-Metastabilitaetsdiagnostik (`n >= 10^7`) | aktiv | Hintergrundlauf fuer Paper-I-Evidenz |

## Historische und thematische Skriptfamilien

| Familie | Dateien | Relevanz | Risiko |
| --- | --- | --- | --- |
| Knotenstabilitaet | `experiments/knot_stability/*.py` | Trajektorien, Knotenvisuals, Residence-Ideen | meist historische Parameter, teils lange Laeufe |
| Dimension Selection | `experiments/dimension_selection/DimensionsHeatmap*.py` | Heatmaps, Kovarianz-/Spektraldimension | lange Laufzeiten, GPU/Numba-Zweige |
| Zwei-Skalen-Kernel | `experiments/dimension_selection/2SkalenKernel/*.py` | Double-Kernel-Regime, Dimension/Attraktor-Hypothesen | sehr hohe `N`, Checkpoints, unterschiedliche Konventionen |
| Fraktalanalyse | `experiments/fractal_analysis/Fraktale/*.py` | Archivquelle des `D_occ ~ 2.8`-Befunds | alte CSVs ohne explizite Seed-Spalten |
| Propagation Speed | `experiments/propagation_speed/PaperII3D_*.py` | Time-of-flight, Response, `c_eff` | Threshold-/Glattungsrobustheit offen |
| OU-Limit | `experiments/ou_limit/*.py` | analytische Kontroll- und Regimefiguren | eher schematisch als beweisend |
| Legacy-Validierung | `experiments/legacy/scripts/highN_regime*.py` | reproduzierbare Varianten historischer High-N-Regime | nur mit kleinen Parametern als Pilot starten |

## Wichtigste Ergebnisartefakte

### Long-Run-Metastabilitaet

- `experiments/long_run_metastability.py`
- `data/processed/long_run_metastability/*/summary.json` nach Abschluss eines Laufs
- [Long-Run Metastability Plan](long_run_metastability_plan.md)

### Paper-0-Markov-Schicht

- `data/processed/anchor_paper/sensitivity_summary.json`
- `reports/anchor_sensitivity_2026-06-29.md`

### Effektive Dimension

- `experiments/fractal_analysis/Fraktale/resultsN.csv`
- `data/processed/fractal_analysis/dimension_claim_summary.json`
- `data/processed/fractal_analysis/dimension_reproduction_pilot.json`
- `data/processed/fractal_analysis/dimension_reproduction_archive_scaling_check.json`
- `data/processed/fractal_analysis/fractal_alpha_sweep_pilot_historical_30k.json`
- `reports/dimension_claim_seed_audit_2026-06-13.md`
- `reports/dimension_reproduction_results_2026-06-13.md`
- `reports/fractal_parameter_landscape_reading_2026-06-13.md`

### High-N- und Alpha-Regime

- `data/processed/highN_regime/*.json`
- `data/processed/sweep_alpha/*.json`
- `data/processed/alpha/*.json`
- `reports/fractal_alpha_sweep_pilot_historical_30k_2026-06-13.md`

### Endliche Propagation

- `figures/draft/diagram1_retarded_response.pdf`
- `figures/draft/diagram2_time_of_flight.pdf`
- `figures/draft/diagram3_ceff_scaling.pdf`
- `figures/draft/diagram4_light_cone.pdf`
- `figures/draft/front_*`
- `figures/draft/diffusive_*`

### Paper-I-Figuren

- `paper/paper_i/fig1_knot_trajectory.pdf`
- `paper/paper_i/fig2_knot_scatter.pdf`
- `paper/paper_i/fig3_knot_trajectory.pdf`
- `paper/paper_i/fig_alpha.pdf`
- `paper/paper_i/fig_Gamma_alpha.pdf`

## Aktueller Dimensionsstand

Archiv:

| embedding dim | N | runs | mean D_occ | Lesart |
| ---: | ---: | ---: | ---: | --- |
| 5 | 60,000,000 | 5 | 2.810559 | staerkster Near-3-Long-N-Befund |
| 3 | 60,000,000 | 10 | 2.372485 | nicht der staerkste Long-N-Punkt |
| 4 | 60,000,000 | 5 | 2.682259 | nahe, aber unter dim 5 |
| 6 | 60,000,000 | 5 | 2.695450 | ein Run gewinnt gegen dim 5 |

Neue Reproduktion:

- `50k` und `100k`: neuer Pfad trifft die Archivskala sehr gut.
- `300k`: gleiche Groessenordnung, aber noch nicht long-N.
- `<= 60k` mit Kontrollen: kein Near-3-Claim sichtbar.

Konsequenz:

> Der aktuelle Claim ist ein archivierter Long-N-Near-3-Befund mit plausibler
> Reproduktionskopplung, nicht der Nachweis eindeutiger 3D-Selektion.

## Kontrollstrategie

Prioritaet fuer neue Laeufe:

1. Long-Run-Metastabilitaet im kanonischen Paper-I-Modell mit `n >= 10^7`.
2. Baseline gegen `eta_zero` und `single_scale` trennen.
3. Mehrere Seeds erst nach erster Laufzeit- und Skalenmessung.
4. Archivierten Dimensionspfad separat mit expliziten Seeds im Millionenbereich haerten.
5. Fitfenster-, Burn-in- und Sampling-Sensitivitaet.

## Non-Markovian / Markov-Embedding Status

Initial vorhanden:

- reduzierte Memory-Summary-Features pro Sample;
- Lagged datasets auf Sample-Indizes;
- Transition Counts und Uebergangsmatrizen;
- implied timescales und einfache Chapman-Kolmogorov-Fehler;
- kleine Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet.

Weiter offen:

- vollstaendige Memory-Traces oder reichere Feature-Familien;
- systematische Bootstrap-Auswertung;
- PCCA-/HMM-basierte metastabile Zustandsmodelle;
- Long-Run-Transferoperatoren statt nur Kurzlauf-Sanity-Checks.
