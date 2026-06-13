# data/raw

Dieser Ordner enthält unveränderte Rohdaten und Ausgangsresultate von
Simulationen. Die strukturierte Ablage in Unterordnern macht es leichter,
Originaldaten von verarbeiteten Ausgaben zu trennen.

## Kategorien

- `alpha/`: Rohdaten von Alpha-Scans und Plateau-Analysen
- `highN_regime/`: Rohdaten aus High-N-Regime-Läufen
- `sweep_alpha/`: Rohdaten von Alpha-Sweep-Experimenten
- `reference/`: Ursprüngliche Referenzläufe und Pilotdaten
- `heatmap/`: Rohdaten für Heatmap-Generierung
- `progress/`: Checkpoints und Fortschrittsdaten

## Verwendung

Neue Simulationen sollen ihre unverarbeiteten Ergebnisse zuerst hier
ablegen. Danach können sie in `data/processed/` weiter bearbeitet werden.
