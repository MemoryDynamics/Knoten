# Experiments

Stand: 2026-07-09.

Dieses Verzeichnis enthaelt reproduzierbare Entry-Points und historische
Explorationsskripte fuer den Emergenz-Knoten-Kern.

## Aktive Einstiege

```bash
python experiments/cli.py --list
python experiments/cli.py reference --list
python experiments/cli.py reference --script current/reference/reference_experiment.py
python experiments/current/reference/reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100
python experiments/current/anchors/anchor_paper_pipeline.py
python experiments/current/anchors/anchor_sensitivity_analysis.py
python experiments/current/dynamics/epsilon_step_balance.py
python experiments/current/dynamics/epsilon_floor_visual_probe.py
python experiments/current/kernels/kernel_shape_probe.py
python experiments/current/dynamics/long_run_metastability.py --help
python experiments/current/markov/knot_score_report.py
```

## Struktur

- `reference_experiment.py`: kleiner reproduzierbarer Referenzlauf.
- `anchor_paper_pipeline.py`: Paper-0-Smoke mit augmentierten Features und Transferoperator-Schaetzung.
- `anchor_sensitivity_analysis.py`: kleine Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet fuer die Markov-Schicht.
- `epsilon_step_balance.py`: gezielte Update-Bilanz zwischen Rauschen, repulsivem Beitrag und Netto-Drift.
- `epsilon_floor_visual_probe.py`: flexible 3D-Visualisierung der Epsilon-Floor-Faelle.`r`n- `epsilon_dynamic_center_sweep.py`: kurzer Epsilon-Sweep auf dynamischem Center, KnotScore v0.5 und Spin-Proxy gegen `eta_zero`.
- `kernel_shape_probe.py`: gezielte Kernelbreiten-/Amplituden- und Seed-Probe mit skaliertem 3D-Fuehrungskoordinatenplot.
- `long_run_metastability.py`: seedfaehige Long-Run-Piloten mit
  `baseline`, `eta_zero`, `single_scale`, `zero_mean_two_scale` und
  `matched_deposition_renormalized`.
- `knot_score_report.py`: Scorecard-Auswertung vorhandener Long-Run-JSONs mit v0.3-v0.5-Knotenscore.
- `cli.py`: kategorisierte Steuerung vorhandener Skripte.
- `dimension_selection/`: effektive Dimensionswahl und Kernel-Parameter.
- `fractal_analysis/`: Box-counting, Occupancy-Dimension,
  Dimensionsclaim-Audit und Reproduktionspiloten.
- `propagation_speed/`: Time-of-flight, retarded response, Signalfronten.
- `synchronization/`: geplanter Pfad fuer Single-Knot-Observablen,
  Mehrknoten-Synchronisation und Response-Rank.
- `knot_stability/`: Knoten- und Trajektorienlaeufe.
- `ou_limit/`: OU-Kontrollen und analytische Grenzfaelle.
- `LQG/`: orbitartige Explorationslaeufe und Kruemmungsstatistiken.
- `legacy/`: alte Skripte und temporaere Tests.

## Workflow fuer neue Experimente

1. Wenn moeglich den Paketkern `src/emergenz_knoten` nutzen.
2. Parameter, Seeds, Git-Revision und Runtime dokumentieren.
3. Outputs unter `data/processed/<thema>/` speichern.
4. Diagnostikversion und Fitfenster im JSON oder Report festhalten.
5. Negativkontrollen frueh planen, aber zuerst dort laufen lassen, wo ein
   Baseline-Signal sichtbar ist.

## Aktueller Schwerpunkt

Die Non-Markovian/Markov-Embedding-Schicht ist initial vorhanden. Der aktuelle
Experimentfokus ist ihre Haertung:

- Seed-Sensitivitaet.
- Lag-Sensitivitaet in Sample-Indizes und Update-Schritten.
- Voxel-/Feature-Sensitivitaet.
- Negativkontrollen wie `eta_zero` und shuffelte Memory-Features.
- Spaeter PCCA/HMM/PMM-Fallbacks, falls reduzierte Features nicht ausreichend markovsch sind.
- Epsilon-Step-Balance: `epsilon=0` friert den Nullstart ein; positive Werte skalieren die lokale Bewegung, machen sie aber in der getesteten Baseline nicht glatter.`r`n- Epsilon-Dynamic-Center-Sweep 2026-07-12: fuer `A_att=35`, `N=100k`, Seeds `1..3` traegt ein kurzes v0.5-Score-Plateau von etwa `epsilon=1.65e-6` bis `0.741`; ab `epsilon=2.72` kollabiert der aktive Lauf auf `eta_zero`-aehnliche Metriken.
- Kernel-Shape-Probe: Paketkernel-Paritaet, `A_att=0`/`A_rep=0`-Ablation, Seedvergleich und Shared-/Flexible-Scale-3D-Fuehrungskoordinatenplots.
- Der Kernelgradient wurde korrigiert; fruehere Knotenscore-/Force-Piloten
  sind `legacy-sign`-Auditmaterial.
- Der korrigierte q=3-Retest und die Amplitudenhierarchie sind gelaufen:
  `A_att=0.35` dispergiert, kompakte Kandidaten liegen im Kurzpilot bei
  `A_att=9..35`.
- Erster AR-Modentest auf den korrigierten Kandidaten: langsame Moden bleiben reell. Der Grenzscan lokalisiert `A_att ~= 7.9`; fuer oszillatorische/Photon-Tracks ist Vektor-/Phasenmemory wahrscheinlicher als weiteres Skalieren des skalaren Modells.

Fuer den archivierten Dimensionsclaim bleibt
`experiments/fractal_analysis/reproduce_dimension_pilot.py` der aktuelle
Reproduktionspfad.

## Kontext

- `docs/status/current_status.md`
- `docs/status/project_priorities.md`
- `docs/reference/THEORETICAL_CONTEXT.md`
- `docs/reference/repository_map.md`
- `docs/reference/experiment_catalog.md`
- `docs/status/paper_claims.md`
