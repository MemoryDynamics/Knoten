# Experiments

Stand: 2026-07-21.

Dieses Verzeichnis enthaelt reproduzierbare Entry-Points und historische
Explorationsskripte fuer den Emergenz-Knoten-Kern.

## Aktive Einstiege

```bash
python experiments/cli.py --list
python experiments/cli.py memory --list
python experiments/current/reference/reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100
python experiments/current/anchors/anchor_paper_pipeline.py
python experiments/current/dynamics/long_run_metastability.py --help
python experiments/current/markov/knot_score_report.py
python experiments/current/memory/synchronization/weak_probe_response.py
```

## Struktur

- `current/anchors/`: Paper-0-Smokes und kurze Markov-Sensitivitaet.
- `current/dynamics/`: Long Runs, Center-Traces, Dimension und Kernelkontrollen.
- `current/markov/`: KnotScore, AR-Moden und Feature-Closure.
- `current/memory/`: Vektormemory und das gestufte externe Response-Programm.
- `current/memory/synchronization/weak_probe_response.py`: gepaarte uniforme
  `+delta/-delta`-Kalibrierung mit Nullpfad und `eta_zero`.
- `current/kernels/`: gezielte Kernel-Shape- und Amplitudenproben.
- `fractal_analysis/`: Occupancy-Dimension, historische Reproduktion und
  Dimensionsclaim-Audits.
- `propagation_speed/`: Ballistik-, Time-of-flight- und spaetere
  Ausbreitungsprotokolle.
- `archive/`: historische oder nichtkanonische Skripte.

## Workflow

1. Den Paketkern unter `src/emergenz_knoten` verwenden oder zuerst erweitern.
2. Parameter, Seeds, Git-Revision, Kontrollen und Auswertefenster dokumentieren.
3. Bulk-Outputs unter `data/processed/<thema>/` speichern.
4. Nur kuratierte Reports, Zusammenfassungen und Figuren committen.
5. Ein Haupteffekt pro Experiment; Probestarken vor breiten Parameterachsen
   auf Linearitaet und Nichtdestruktivitaet pruefen.
6. Deskriptive Dimension oder Singularwertenergie nicht mit statistischer
   Reproduzierbarkeit gleichsetzen.

## Aktueller Schwerpunkt

Der skalare `A_att=35`, `epsilon=1e-4`-Zustand ist inzwischen als lineare
co-moving Relaxationsbaseline eingeordnet. Weak Probe, Frozen Source,
signierter Architekturtest und One-Way-Interaction-Age-Audit sind ausgefuehrt.
Der Fernkanal akkumuliert Zentrumtranslation, isoliert aber keine
kontrollgetrennte Formmodifikation oder Oszillation.

Neue Experimente muessen deshalb vorab zwischen zwei Mechanismen entscheiden:

- lokaler bzw. retardierter Mediator mit explizitem Feldzustand; oder
- orientiertes Vektormemory mit relationalem Readout.

Reine Laufzeitverlaengerung, kleinere Epsilon-Werte oder neue Amplitudensweeps
des alten Skalarpfads sind ohne falsifizierbare Zusatzhypothese nicht aktiv.
Der aktuelle Entscheidungsstand und die kanonischen Reports stehen in
`docs/status/project_priorities.md` und `reports/README.md`.

## Kontext

- `docs/status/current_status.md`
- `docs/status/project_priorities.md`
- `docs/reference/THEORETICAL_CONTEXT.md`
- `docs/reference/repository_map.md`
- `docs/reference/experiment_catalog.md`
- `docs/status/paper_claims.md`
