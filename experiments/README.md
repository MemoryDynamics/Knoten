# Experiments

Stand: 2026-08-10.

Dieses Verzeichnis enthaelt reproduzierbare Entry-Points und historische
Explorationsskripte fuer den Emergenz-Knoten-Kern.

## Aktive Einstiege

```bash
python experiments/cli.py --list
python experiments/cli.py memory --list
python experiments/current/reference/reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100
python experiments/current/anchors/anchor_paper_pipeline.py
python experiments/current/dynamics/long_runs/long_run_metastability.py --help
python experiments/current/markov/knot_score_report.py
python experiments/current/memory/synchronization/calibration/weak_probe_response.py
python experiments/current/memory/synchronization/one_way/oriented_vector_one_way_gate.py --help
```

## Struktur

- `current/anchors/` und `current/reference/`: kurze Baselines und
  reproduzierbare Referenzlaeufe.
- `current/dimensions/`: Claim-, Snapshot-, Sensitivitaets- und N-Audits.
- `current/dynamics/{centering,epsilon,long_runs,scaling}/`: co-moving
  Diagnostik, Rauschbilanz, Langlauf- und Skalierungsreconciliation.
- `current/kernels/{families,controls,field}/`: Kernelklasse, fest
  vorgegebene Kontrollen und separate Feldkandidaten.
- `current/markov/` und `current/knot_stability/`: Zustandsreduktion,
  Scorecards und geometrische Stabilitaetsproben.
- `current/memory/{closure,representations}/`: Modenclosure und alternative
  Memory-Darstellungen.
- `current/memory/synchronization/{calibration,one_way,mediation,reciprocity}/`:
  das gestufte externe Response-Programm.
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

Der separat relaxierende passive Vektormemory-Kanal besteht sein
vorregistriertes Sechs-Seed-One-Way-Gate. Die relevante Trennung ist der
`3.50..8.05`-fache Gewinn gegen einen Ein-Schritt-Kanal; Orientierung,
Persistenz und instantanes Readout sind dennoch konstruiert. Vor einem lokalen
oder retardierten Mediator folgt deshalb eine feste-Kopplung-Replikation mit
verschiedenen Source/Target-Seeds, 64 Random-Sign-Kontrollen und Distanzleiter.

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
