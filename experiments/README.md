# Experiments

Stand: 2026-06-14.

Dieses Verzeichnis enthaelt reproduzierbare Entry-Points und historische
Explorationsskripte fuer den Emergenz-Knoten-Kern.

## Aktive Einstiege

```bash
python experiments/cli.py --list
python experiments/cli.py reference --list
python experiments/cli.py reference --script reference_experiment.py
python experiments/reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100
```

## Struktur

- `reference_experiment.py`: kleiner reproduzierbarer Referenzlauf.
- `cli.py`: kategorisierte Steuerung vorhandener Skripte.
- `dimension_selection/`: effektive Dimensionswahl und Kernel-Parameter.
- `fractal_analysis/`: Box-counting, Occupancy-Dimension,
  Dimensionsclaim-Audit und Reproduktionspiloten.
- `propagation_speed/`: Time-of-flight, retarded response, Signalfronten.
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

Die naechste Experimentfamilie sollte die Non-Markovian/Markov-Embedding
Schicht vorbereiten:

- Memory-Summary-Features pro Samplezeitpunkt.
- Lagged datasets.
- Transition Counts und Uebergangsmatrizen.
- Implied timescales, Chapman-Kolmogorov-Checks und spectral gaps.

Fuer den archivierten Dimensionsclaim bleibt
`experiments/fractal_analysis/reproduce_dimension_pilot.py` der aktuelle
Reproduktionspfad.

## Kontext

- `docs/current_status.md`
- `docs/non_markovian_basis.md`
- `docs/experiment_catalog.md`
- `reports/dimension_reproduction_results_2026-06-13.md`
