# Experiment-Katalog

Stand: 2026-07-01.

Diese Datei ist zugleich Experiment-Katalog, Reproduzierbarkeitsnotiz und
Long-Run-Plan. Sie ersetzt die alten Einzeldateien zu Reproduzierbarkeit,
Hardening und Long-Run-Metastabilitaet.

## Kanonische Entry-Points

| Datei | Thema | Status | Naechste Nutzung |
| --- | --- | --- | --- |
| `experiments/long_run_metastability.py` | Long-N-Metastabilitaetsdiagnostik | aktiv | Knotenscore v0.2 und weitere Ablationen |
| `experiments/anchor_paper_pipeline.py` | Paper-0-Smoke mit Markov-Schicht | aktiv | schneller Sanity-Check |
| `experiments/anchor_sensitivity_analysis.py` | Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet | aktiv | kurze Operator-Pipeline-Checks |
| `experiments/epsilon_step_balance.py` | Rauschen-vs-Drift-Updatebilanz | aktiv | gezielte Epsilon-/Glattheitsdiagnostik |
| `experiments/kernel_shape_probe.py` | 3D-Fuehrungskoordinatenplot fuer Kernelbreiten und Amplituden | aktiv | visuelle Shape-Diagnostik, keine Long-Run-Evidenz |
| `experiments/reference_experiment.py` | kleiner Referenzlauf | aktiv | Smoke-Test |
| `experiments/fractal_analysis/analyze_dimension_claim.py` | Audit des archivierten `D_occ`-Claims | aktiv | Claim-Register |
| `experiments/fractal_analysis/reproduce_dimension_pilot.py` | kleine/mittlere Reproduktion | aktiv | spaetere Dimensionshaertung |
| `experiments/fractal_analysis/plot_d_alpha_n_intensity.py` | d-alpha-N-Heatmaps aus Reproduktions-JSON | aktiv | Seed-/N-Dimensionsberichte |
| `experiments/synchronization/` | Innen/Aussen- und Mehrknoten-Synchronisation | geplant | Single-Knot-Observablen und Response-Rank |
| `experiments/cli.py` | kategorisierte Experimentsteuerung | aktiv | Einstieg in Skriptfamilien |

## Long-Run-Metastabilitaet

Kanonischer Start:

```powershell
python experiments/long_run_metastability.py `
  --steps 10000000 `
  --seeds 1 `
  --conditions baseline `
  --dim 3 `
  --alpha 0.01 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data/processed/long_run_metastability/2026-06-29_initial
```

Abgeschlossener Baseline-Lauf:

| Feld | Wert |
| --- | --- |
| Condition | `baseline` |
| Seed | `1` |
| Updates | `10,000,000` |
| Samples | `9001` |
| Laufzeit | `337.997 s` |
| Steps/s | `29,586` |
| Memory-Horizon | `600` |
| gespeicherte Gewichtsmasse | `0.997595` |
| Bestes Residence-Verhaeltnis | `256 alpha^{-1}` |
| `D_cov` / `D_occ` | `1.699` / `1.792` |

Residence nach Voxelgroesse:

| Voxel | visited | knot_count | max updates | max in `alpha^{-1}` |
| ---: | ---: | ---: | ---: | ---: |
| `0.5` | `674` | `529` | `14,000` | `140` |
| `1.0` | `180` | `168` | `20,400` | `204` |
| `2.0` | `56` | `54` | `25,600` | `256` |

Kontrollreport 2026-07-01:

| Condition | Best residence mean +/- SD in `alpha^{-1}` | Mean centered radius | Lesart |
| --- | ---: | ---: | --- |
| `baseline` | `437.6 +/- 323.1` | `3.880` | kompakt, langlebig, seed-variabel |
| `eta_zero` | `80.0 +/- 12.2` | `57.284` | echte Negativkontrolle |
| `single_scale` | `697.7 +/- 534.6` | `3.734` | Kernel-Ablation, keine Negativkontrolle |

Lesart: Memory-Gradient-Feedback trennt sich deutlich von `eta_zero`; der
zweiskalige Baseline-Kernel ist aber noch nicht als notwendiger Mechanismus
isoliert. Der Report liegt unter `reports/long_run_control_report_2026-07-01.md`.

## Epsilon-Step-Balance

Gezielter Baseline-Run vom 2026-07-01:

| epsilon | median noise | median repulsive step | median net drift | median noise/repulsive | mean turn cosine |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0.03` | `0.04624` | `0.01281` | `0.01231` | `3.615` | `-0.070` |
| `0.015` | `0.02312` | `0.00643` | `0.00618` | `3.598` | `-0.071` |
| `0.01` | `0.01541` | `0.00429` | `0.00412` | `3.594` | `-0.071` |
| `0.005` | `0.00771` | `0.00215` | `0.00206` | `3.593` | `-0.071` |

Lesart: Kleineres `epsilon` skaliert in diesem Slice Noise, Drift und Radius
fast gemeinsam herunter. Es macht die Trajektorie kleiner, aber nicht glatter
oder drift-dominierter. Report: `reports/epsilon_step_balance_2026-07-01.md`.


## Kernel-Shape-Probe

Punktueller 3D-Fuehrungskoordinaten-Run vom 2026-07-02:

| case | sigma_rep | sigma_att | A_rep | A_att | k_eff | mean radius | median step | turn mean | path/chord |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1` | `3` | `1` | `0.35` | `0.1442` | `0.233` | `0.1099` | `-0.342` | `1202.3` |
| `att_zero` | `1` | `3` | `1` | `0` | `0.1500` | `0.225` | `0.1090` | `-0.348` | `1238.7` |
| `rep_zero` | `1` | `3` | `0` | `0.35` | `-0.0058` | `6.620` | `0.1519` | `0.059` | `48.9` |
| `strong_local` | `1` | `3` | `4` | `0.35` | `0.5942` | `0.075` | `0.0707` | `-0.430` | `2746.5` |
| `wide_strong` | `2` | `6` | `16` | `1.4` | `0.5942` | `0.075` | `0.0707` | `-0.430` | `2752.4` |

Lesart: Die schwarze Linie in der Figur ist eine geglaettete Rolling-Mean-
Trajektorie; die farbige Linie ist der roh gesampelte Pfad desselben Cases.
`k_eff = eta(A_rep/sigma_rep^2 - A_att/sigma_att^2)` ist die lokale
restaurierende Skala in der aktuellen Euler-Konvention. Deshalb zerfaellt
`A_att=0` nicht: der `A_rep`-Anteil ist lokal bindend. Die schaerfere
Dispersionskontrolle ist `A_rep=0`, die hier den Radius stark vergroessert.
Report: `reports/kernel_shape_probe_2026-07-01.md`.

## Reproduzierbarkeitsregeln

Jeder Lauf, der als Evidenz genutzt wird, braucht:

- Parameter und Condition;
- Seed-Liste;
- Git-Revision und Arbeitsbaumstatus;
- Burn-in, Sampling und Outputpfad;
- Runtime und Steps/s;
- maschinenlesbares JSON unter `data/processed/`;
- nach Review einen datierten Report unter `reports/`.

Lange Laeufe gehoeren nicht in CI und nicht in die normale Testsuite.

## Markov-/Operator-Status

Initial vorhanden:

- reduzierte Memory-Summary-Features pro Sample;
- Lagged datasets auf Sample-Indizes;
- Transition Counts und Uebergangsmatrizen;
- implied timescales und einfache Chapman-Kolmogorov-Fehler;
- kleine Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet.

Weiter offen:

- vollstaendige Memory-Traces oder reichere Feature-Familien;
- systematischer Bootstrap;
- PCCA-/HMM-/PMM-basierte metastabile Zustandsmodelle;
- Long-Run-Transferoperatoren statt Kurzlauf-Sanity-Checks.

## Effektive Dimension

Archiv:

| embedding dim | N | runs | mean D_occ | Lesart |
| ---: | ---: | ---: | ---: | --- |
| 5 | 60,000,000 | 5 | 2.810559 | staerkster Near-3-Long-N-Befund |
| 3 | 60,000,000 | 10 | 2.372485 | nicht der staerkste Long-N-Punkt |
| 4 | 60,000,000 | 5 | 2.682259 | nahe, aber unter dim 5 |
| 6 | 60,000,000 | 5 | 2.695450 | ein Run gewinnt gegen dim 5 |

Konsequenz: archivierter Long-N-Near-3-Befund mit plausibler
Reproduktionskopplung, kein Nachweis eindeutiger 3D-Selektion.

Seeded d-alpha-N-Scan 2026-06-30:

| Scan | Ergebnis | Lesart |
| --- | --- | --- |
| `d=3..8`, `alpha=0.01/0.02`, `N=30k/100k/300k`, Seeds `1..5` | `D_cov`-Naehe zu 3 wandert von `d=3` ueber `d=5` zu `d=6/7` | kein stabiles `d=3`-Plateau; eher endliche-N-/Fitfenster-/Schaetzerabhaengigkeit |

## Innen/Aussen- und Synchronisationsprogramm

Neuer geplanter Pfad:

| Stufe | Ziel | Messgroessen |
| --- | --- | --- |
| Einzelknoten | stabile externe und interne Observablen extrahieren | center, shape tensor, radius, mode coefficients, residence |
| Basin-Statistik | Seeds als Attraktionskanal-Sampler behandeln | `P(knot type | parameters, seed)` |
| Zwei-Knoten-Pilot | Synchronisation von zwei Knoten testen | cross-correlation, phase-locking, response delay |
| Externer Subraum | gemeinsame makroskopische Wechselwirkungsstruktur messen | response matrix, response rank, subspace stability |

Guardrail: Diese Stufe behauptet keine Quantenfeldtheorie. Sie prueft nur, ob
synchronisierte Knoten kollektive externe Observablen ausbilden.

## Historische Skriptfamilien

| Familie | Dateien | Relevanz | Risiko |
| --- | --- | --- | --- |
| Knotenstabilitaet | `experiments/knot_stability/*.py` | Trajektorien, Knotenvisuals | historische Parameter |
| Dimension Selection | `experiments/dimension_selection/DimensionsHeatmap*.py` | Dimension/Heatmaps | lange Laufzeiten |
| Zwei-Skalen-Kernel | `experiments/dimension_selection/2SkalenKernel/*.py` | Double-Kernel-Regime | unterschiedliche Konventionen |
| Fraktalanalyse | `experiments/fractal_analysis/Fraktale/*.py` | Archivquelle `D_occ ~ 2.8` | alte CSVs ohne Seed-Spalten |
| Propagation Speed | `experiments/propagation_speed/PaperII3D_*.py` | Paper-II-Programm | Threshold-Robustheit offen |
| OU-Limit | `experiments/ou_limit/*.py` | analytische Kontrollfiguren | schematisch |
| Legacy | `experiments/legacy/scripts/highN_regime*.py` | historische High-N-Regime | nur gezielt starten |
