# Experiments

Dieses Verzeichnis enthält die sauber strukturierten Reproduktions- und
Explorationszugänge für den Emergenz-Knoten-Kern.

## Struktur

- `dimension_selection/` — Experimente zur effektiven Dimensionswahl und zum
  Einfluss verschiedener Kernel-Parameter.
- `propagation_speed/` — Messungen zur Ausbreitungsgeschwindigkeit, Time-of-
  Flight und Signalfronten.
- `knot_stability/` — historische Knoten- und Trajektorienläufe mit Fokus auf
  metastabile Strukturen.
- `ou_limit/` — OU-Kontrollläufe und analytische Grenzfälle.
- `fractal_analysis/` — Box-counting und Occupancy-Dimensionen.
- `LQG/` — orbitartige Explorationslaeufe und Kruemmungsstatistiken.
- `legacy/` — Alte Scripts und uneingepasste Explorationsläufe. Diese bleiben
  als Referenz erhalten, aber neue Reproduktion sollte aus den anderen
  Unterverzeichnissen erfolgen.

## Workflow

1. Installiere das Paket im Entwicklungsmodus:

```bash
python -m pip install -e .
```

2. Der erste reproduzierbare Einstiegspunkt ist `experiments/reference_experiment.py`.
3. Für kategorisierte Experimente kannst du `experiments/cli.py` verwenden.

```bash
python experiments/cli.py --list
python experiments/cli.py dimension_selection --list
python experiments/cli.py dimension_selection --script DimensionsHeatmap.py
```

4. Wähle ein Experimentverzeichnis und prüfe vorhandene Skripte.
5. Erzeuge eine neue, reproduzierbare Version eines Laufs mit klaren
   Eingabedaten und Ausgabeformaten.
6. Speichere Resultate in `data/raw/` oder `data/processed/` und beschreibe
   Parameter in einer separaten Metadatei, wenn möglich.

## Ziel

- Historische Explorationsskripte werden nicht gelöscht, sondern als `legacy`
  archiviert.
- Neue Experiment-Entry-Points sollen den Paketkern `emergenz_knoten`
  nutzen, statt auf rohe Skripte mit hartkodierten Pfaden.
- Die Dokumentation soll klar machen, welche Ordner für welchen Zweck da
  sind.

## Theoretical Context

Für die Einordnung der Experimente siehe [docs/THEORETICAL_CONTEXT.md](../docs/THEORETICAL_CONTEXT.md)
— dort sind die zentralen theoretischen Aussagen (Zeit, Raum, Knoten, ℏ_eff)
kompakt zusammengefasst und mit den passenden Experiment-Entry-Points
verlinkt.
