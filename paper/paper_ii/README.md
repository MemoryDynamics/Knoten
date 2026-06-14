# Paper II - Propagation Speed and Light-Cone Dynamics

Stand: 2026-06-14.

## Rolle

Paper II sammelt die These, dass aus irreversibler Speicherdynamik und
gekoppelten metastabilen Knoten endliche Antwortzeiten, effektive
Signalfronten und spaeter Lorentz-artige Kinematik entstehen koennen.

## Status

Die Struktur ist vorbereitet, aber die empirische Haertung steht hinter der
aktuellen Paper-0/Paper-I-Arbeit:

- Zuerst Non-Markovian Basis und Markov-Einbettung klaeren.
- Dann Paper I als Minimalmodell haerten.
- Danach Propagation, `c_eff` und Lorentz-Kinematik mit klaren
  Negativkontrollen und robusten Onset-Kriterien weiterziehen.

## Dateien

- `main.tex`: LaTeX-Hauptdatei.
- `references2.bib`: Bibliographie.

## Verwandte Experimente und Figuren

- `experiments/propagation_speed/`
- `figures/draft/diagram1_retarded_response.pdf`
- `figures/draft/diagram2_time_of_flight.pdf`
- `figures/draft/diagram3_ceff_scaling.pdf`
- `figures/draft/diagram4_light_cone.pdf`
- `figures/draft/front_*`
- `figures/draft/diffusive_*`

## Haertungsbedarf

- Kick/no-kick-Ensembles mit gleicher Seed-Struktur.
- Vorab definierte Response-Observable.
- Onset-Detection robust gegen Threshold, Glaettung und Fenster.
- `t_onset(L)`-Fits mit Fehlerbalken.
- Tests gegen Speicher-Randomisierung und diffusive Nullmodelle.
- Pruefung, ob verschiedene Knoten denselben effektiven `c_eff` messen.
