# Paper II - Propagation Speed and Light-Cone Dynamics

Stand: 2026-10-21.

**Nicht als Ergebnisfassung zirkulieren:** `main.tex` ist ein alter
Companion-Draft. Trotz vorsichtigem Abstract enthaelt er noch unbelegte
Aussagen ueber Knoten, fehlende geometrische Inputs und gemessene universelle
Propagation. Der [R0-Audit](../../docs/reference/foundation_feasibility.md)
benennt diese Luecke. Quelle und gegebenenfalls vorhandenes PDF sind noch
nicht an den aktuellen Paper-I-Befund angepasst.

## Rolle

Paper II ist aktuell ein Companion-Draft und Future-Work-Programm. Es sammelt
die These, dass aus Memory-Dynamik und gekoppelten langlebigen
Knoten endliche Antwortzeiten, effektive Signalfronten und spaeter
Lorentz-artige Kinematik entstehen koennen.

Der Draft darf derzeit nicht als Claim-Paper gelesen werden. Seine Rolle ist
Propagation und Kinematik, nicht bereits Gravitationsdynamik. Die aktive
Arbeitsfolge steht allein in den
[Projektprioritaeten](../../docs/status/project_priorities.md).

## Status

Die vorbereitete Struktur ist noch kein physikalischer Nachweis:

- Paper I liefert im getesteten Ast eine klassische lineare Radiusbaseline,
  keinen nachgewiesenen nichtlinearen Materiebaustein.
- B1 muss Zustand, Interventionen und Informationszugriff fuer eine
  gemeinsame operationale Beschreibung klaeren, bevor ein Signaltest
  physikalisch interpretiert wird.
- Die algebraische/operatorische Sprache ist textlich eingearbeitet, die
  numerische Operatorpipeline aber noch offen.
- Keine `d=3`-Selektion, keine harte Signalgeschwindigkeit und keine
  Lorentz-Kinematik als aktuelles Resultat behaupten.
- Die fruehere `D_mem ~=2.94`-Beobachtung im gewaehlten 3D-Embedding ist
  durch ambiente lineare Gaussgeometrie erklaerbar, keine 3D-Emergenz.
- Endliche Antwortschwellen ersetzen keinen Kausalrand. Der direkte
  Gauss-Readout hat bei erlaubter Quellenintervention eine Fernantwort;
  eine effektive Lokalitaet braucht eine eigene Fehler-/Skalenkontrolle.
- Ein gemeinsamer Lichtkegel allein liefert weder die volle Lorentz-
  Invarianz der Dynamik noch Einstein-Gleichungen oder universelle Kopplung.

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
