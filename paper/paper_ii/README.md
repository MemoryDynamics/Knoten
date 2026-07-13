# Paper II - Propagation Speed and Light-Cone Dynamics

Stand: 2026-07-13.

## Rolle

Paper II ist aktuell ein Companion-Draft und Future-Work-Programm. Es sammelt
die These, dass aus irreversibler Speicherdynamik und gekoppelten metastabilen
Knoten endliche Antwortzeiten, effektive Signalfronten und spaeter
Lorentz-artige Kinematik entstehen koennen.

Der Draft darf derzeit nicht als Claim-Paper gelesen werden. Die aktuelle
Paper-0/Paper-I-Linie bleibt konservativ: erst Markov-Einbettung,
co-moving scalar-knot Evidenz und Kontrolltrennung; danach erst Propagation,
`c_eff` und Lorentz-artige Kinematik.

## Status

Die Struktur ist vorbereitet, aber die empirische Haertung steht hinter der
aktuellen Paper-0/Paper-I-Arbeit:

- Zuerst Non-Markovian Basis und Markov-Einbettung klaeren.
- Dann Paper I als Minimalmodell haerten.
- Danach Propagation, `c_eff` und Lorentz-Kinematik mit klaren
  Negativkontrollen und robusten Onset-Kriterien weiterziehen.
- Die algebraische/operatorische Sprache ist textlich eingearbeitet, die
  numerische Operatorpipeline aber noch offen.
- Keine `d=3`-Selektion, keine harte Signalgeschwindigkeit und keine
  Lorentz-Kinematik als aktuelles Resultat behaupten.
- Aktueller Input aus Paper I: lokale `D_mem ~=2.94`-Memory-Shape im
  gewaehlten 3D-Embedding. Paper II muss erst klaeren, ob daraus unter
  Ambient-Dimension, Mehrknoten-Wechselwirkung und externer Grobkoernung eine
  robuste externe/macroskopische 3D-Beschreibung wird.

## Dateien

- `main.tex`: LaTeX-Hauptdatei.
- `references2.bib`: Bibliographie.
- `main.pdf`: kompilierte Paper-II-Fassung, falls gebaut.

## Verwandte Experimente und Figuren

- `experiments/propagation_speed/`
- `figures/draft/propagation/diagrams/diagram1_retarded_response.pdf`
- `figures/draft/propagation/diagrams/diagram2_time_of_flight.pdf`
- `figures/draft/propagation/diagrams/diagram3_ceff_scaling.pdf`
- `figures/draft/propagation/diagrams/diagram4_light_cone.pdf`
- `figures/draft/propagation/front/front_*`
- `figures/draft/propagation/diffusive/diffusive_*`

## Haertungsbedarf

- Kick/no-kick-Ensembles mit gleicher Seed-Struktur.
- Vorab definierte Response-Observable.
- Onset-Detection robust gegen Threshold, Glaettung und Fenster.
- `t_onset(L)`-Fits mit Fehlerbalken.
- Tests gegen Speicher-Randomisierung und diffusive Nullmodelle.
- Pruefung, ob verschiedene Knoten denselben effektiven `c_eff` messen.
