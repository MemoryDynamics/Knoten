# Aktueller Stand

Stand: 2026-07-28.

Diese Seite ist die kurze wissenschaftliche Frontdoor. Details, Laufprotokolle
und historische Zwischenlesarten stehen in den datierten Reports und in
`docs/archive/status/current_status_through_2026-07-21.md`.

## Sieben-Punkte-Ueberblick

| Bereich | Evidenz | Belastbare Lesart | Grenze |
| --- | --- | --- | --- |
| Modellkern | Der sichtbare Prozess ist im Allgemeinen nichtmarkovsch; Position plus vollstaendiger Memory-Zustand bilden die Markov-Einbettung. | strukturelles Resultat des definierten Modells | keine Aussage ueber reale Raumzeit |
| Skalarer kompakter Ast | Gematchter Ein- und Zweiskalenkernel kollabieren auf der Achse `A_eff=A_att-9`; Long-Run-Radien folgen dem linearen Finite-Memory-Modus bis maximal `1.16%` relativ. | kontrollierte co-moving Relaxationswolke | kein isolierter nichtlinearer Knoten und kein Phasenuebergang |
| Nichtlinearitaetsgate | Bei `R_linear/L=0.3` liegt der Radius seed-stabil etwa `6.2%` ueber linear, ohne Shape-Umschlag. | kleine glatte Kernelkorrektur | vorregistrierte Composite-Entscheidung bleibt `inconclusive`; Residence-Metriken sind skalenempfindlich |
| Dimension | `D_mem` folgt im linearen isotropen Regime der Ambient-Geometrie; Heat-Trace- und Shape-Dimension trennen sich. | Diagnostik der gespeicherten Wolke | keine eindeutige externe `d=3`-Selektion |
| Spektrales Memory-Feld | Fourier-`rho` reproduziert das exponentielle Memory; Relaxations-Diffusion glaettet kontrolliert. | kompakte Reprasentation bzw. explizite Modellerweiterung | Eigenvektor-/Segmentgate isoliert keinen stabilen physikalischen Modus |
| Externe Antwort | Der persistente Vektorkanal besteht das feste-Kopplungs-/Distanzgate in 6/6 Paaren; beide lokalen Mediatoren bestehen ihre Response-/Shape-Gates, aber das dynamische Common-Source-Gate trennt sie nur in 4/6 Paaren robust. | kontrollierter relationaler Kanal und zwei lauffaehige lokale Markov-Erweiterungen | negatives Modellselektionsgate; Transportgesetze, Persistenz und Source-Readout sind Inputs, Reziprozitaet fehlt |
| Paper-Programm | Paper 0 traegt als mathematischer Anker; Paper I kann den linearen Relaxationsbefund berichten. | eng begrenzter Minimalmodell-Claim | Propagation, Lorentz-, Quanten- und Standardmodellbruecken bleiben Future Work |

## Evidenz, Inferenz und Hypothese

### Strukturell gestuetzt

- Die exponentielle Memory-Dynamik ist im augmentierten Zustand markovsch.
- Die Memory-Faser kontrahiert unter den dokumentierten Normannahmen pfadweise.
- `state.py` und `checkpoints.py` repraesentieren den implementierten
  finite-memory Zustand vollstaendig und checksum-validiert.
- Die spektrale `rho`-Darstellung ist fuer die getestete periodische
  1D-Reprasentation numerisch mit der direkten Historie reconciliiert.

### Numerisch gestuetzt

- Der aktuelle kleine-Radius-Ast ist kompakter als `eta=0`, wird aber fast
  vollstaendig durch den linearen Memory-Center-Relativmodus erklaert.
- Die dynamische Relaxations-Diffusion veraendert Radius und Kraft glatt und
  aufloesungsstabil; sie liefert eine reduzierte Vorhersagebeschreibung.
- Der skalare Cross-Kernel erzeugt reproduzierbare Zentrumtranslation bei
  sehr kleiner Shape-Aenderung.
- Der konstruierte persistente Vektorkanal trennt sich zuerst in 6/6 Seeds und
  danach bei globalem `eta_v` in 6/6 unabhaengigen Paaren von Random-Sign- und
  Ein-Schritt-Kontrollen, bei kleinen Shape-Stoerungen.
- Die autonomen orientierten Sources bestehen in 6/6 Faellen das vorregistrierte
  Spektral-Identifizierbarkeitsgate fuer beide lokalen Mediatorregeln. Der
  Transferkontrast ist jedoch fuer persistenten und Ein-Schritt-Input nahezu
  gleich; dies stuetzt keine spezifische Vektorpersistenz.
- Unter identischer autonomer Source bestehen beide Mediatorregeln in 6/6
  Paaren Messbarkeit, Oddness, Shape-Huelle und Distanzabfall. Die verlangte
  robuste Diffusion-/Telegraph-Trennung besteht nur in 4/6 Paaren; der
  dynamische Modellselektionsversuch ist damit negativ.


### Nicht gestuetzt oder widerlegt

- Ein spezifisch zweiskaliger nichtlinearer Knotenmechanismus ist nicht
  isoliert.
- Komplexe AR-Moden sind nicht von `eta=0` getrennt und nicht segmentstabil;
  sie sind keine Oszillations- oder Photonenevidenz.
- `D_mem` nahe drei im 3D-Embedding ist keine Dimensionsselektion.
- Der positive skalare Memory-Kanal besitzt keine interne Ladungs- oder
  Neutralitaetsstruktur.
- Direkte Fernkopplung und diffusive Felder liefern keine harte endliche
  Signalgeschwindigkeit.
- Der aktuelle komponentenweise Vektormediator kann keine eindeutige
  Ambient-Dimension drei selektieren: Seine Ambient-Transfermatrix ist
  proportional zu `I_d` und erhaelt ohne weiteren Mechanismus den Rang einer
  vollrangigen Source.

### Offene Hypothesen

- Ein spaeteres physikalisches Mediatorgesetz braucht ein unabhaengiges
  Targetkriterium oder eine weitere falsifizierbare Mechanismusannahme. Ein
  weiterer Fit derselben Kopplungen an dieselben Zielantworten waere nicht
  identifizierend.
- Felder selektieren nicht automatisch drei Dimensionen. Eine spaetere
  Dimensionshypothese braucht dieselbe eingefrorene Regel ueber mehrere
  Ambient-Dimensionen und einen kontrollgetrennten effektiven Response- oder
  Modenrang; eine 3D-Feldsimulation waere nur eine 3D-Annahme.
- Reziproke Mehrknotendynamik ist erst sinnvoll, wenn ein One-Way-Kanal
  Identitaet und Form unter Transport besteht.

## Kanonische Evidenzschiene

Der kuratierte Einstieg in die mehr als 100 Markdown-Reports liegt in
`reports/README.md`. Fuer den aktuellen Entscheidungsstand sind besonders
wichtig:

1. `reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md`
2. `reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md`
3. `reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md`
4. `reports/memory/low_mode_identity_audit_2026-07-20.md`
5. `reports/response/one_way_interaction_age_N3M_2026-07-21.md`
6. `reports/response/scalar_cross_readout_resolution_2026-07-21.md`
7. `reports/response/oriented_history_current_audit_2026-07-21.md`
8. `reports/response/oriented_vector_one_way_gate_2026-07-25.md`
9. `reports/response/oriented_vector_fixed_pair_distance_gate_2026-07-26.md`
10. `reports/response/local_oriented_mediator_gate_2026-07-28.md`
11. `reports/response/oriented_source_mediator_identifiability_2026-07-28.md`
12. `reports/response/dynamic_common_source_mediator_gate_2026-07-28.md`

Diese Auswahl ist eine Entscheidungsschiene, keine Behauptung, dass andere
Reports geloescht oder ungueltig seien. Fruehe `legacy-sign`-Reports erklaeren
die Historie, tragen aber keine aktuellen Kernelclaims.

## Aktiver Codepfad

- `src/emergenz_knoten/`: kanonischer Paketkern.
- `src/emergenz_knoten/markov/`: reduzierte Operator- und Closure-Werkzeuge.
- `src/emergenz_knoten/oriented_source.py`: passiver orientierter Zusatzstate
  mit gepaarten One-Way-Kontrollen.
- `src/emergenz_knoten/oriented_diagnostics.py`: gemeinsame Response-, Shape-
  und Distanzmetriken fuer den konstruierten orientierten Kanal.
- `src/emergenz_knoten/local_mediator.py`: lokale 1D
  Relaxations-Diffusions- und Telegraph-Zustaende.
- `src/emergenz_knoten/mediator_identifiability.py`: segmentierte
  Source-Spektren und sourcegewichteter komplexer Transferkontrast.
- `src/emergenz_knoten/external_field_response.py`: gepaarte zeitabhaengige
  Aktiv-/Flip-/Kanal-aus-Targetfortsetzung.
- `experiments/current/`: reproduzierbare aktive Entry-Points.
- `experiments/archive/`: historische oder nichtkanonische Skripte.
- `data/processed/`: standardmaessig ignorierte Bulk-Outputs; nur reviewed
  Snapshots werden explizit getrackt.
- `reports/`: datierte Evidenz mit maschinenlesbaren JSON-Paaren, soweit
  sinnvoll.
- `figures/draft/`: Reportabbildungen, nicht automatisch Paper-Evidenz.

## Aktuelle Entscheidung

Der skalare Fernkanal ist als Negativ-/Baseline-Modell ausreichend gehaertet.
Weitere Amplituden-, kleinere-Epsilon- oder reine Alters-Scans sind ohne neue
diskriminierende Hypothese nicht priorisiert.

Das statische Cross-Readout-Gate scheitert in `d=3/10` am vorregistrierten
1%-Formsignal. Auch die anschliessende kostenlose Umdeutung der geordneten
skalaren Historie besteht weder als polarer Strom noch als antisymmetrische
Zirkulation die konditionale 99%-Random-Sign-Null. Damit wird als genau ein
neuer Mechanismus ein **eigenstaendig evolvierender orientierter Zustand mit
relationalem Readout** geoeffnet. Ein lokaler/retardierter skalarer Mediator
bleibt fuer eine spaetere Lokalitaets- oder Laufzeitfrage zurueckgestellt.

Das vorregistrierte orientierte One-Way-Gate besteht in 6/6 Formationsseeds.
Die relevante Trennung ist persistent/random-q95 `5.76..11.64` gegen
Ein-Schritt/random-q95 `1.40..2.04`, nicht die per Formel normalisierte rohe
Auslenkung. Dies stuetzt den konstruierten Zusatzkanal, nicht seine Emergenz.

Das feste-Kopplung-Gate besteht ebenfalls in 6/6 zyklisch verschiedenen
Source/Target-Paaren. Random-Sign-Trennung `3.16..11.70`, Persistenzgewinn
`2.25..8.64` und Fern/Nah `9.36e-4..2.80e-3`; alle Flip- und Shape-Gates
bestehen. Dies haertet den konstruierten Kanal gegen stateweises Retuning. Der
Gauss-Readout erzwingt jedoch bereits raeumliche Abschwaechung und ist
instantan; daraus folgt weder emergente Lokalitaet noch Propagation.

Der lokale Mediator-Holdout besteht als Architekturtest fuer beide eingesetzten
Regeln. Relaxations-Diffusion erreicht maximal `9.09%` Lag-Vorhersagefehler und
`0.31%` Aufloesungsdrift, Telegraph `7.88%` bzw. `4.91%`; beide bestehen
`5/5` Holdout-Paare bei Shape-Stoerungen unter `3.72e-4`. Das Ergebnis ist
**mechanism underdetermined**, weil die jeweilige Skalierung in der
Feldgleichung steckt. Es ist keine Propagationsgesetz-Entdeckung.

Vor dem dynamischen One-Way-Lauf wurde deshalb ein Identifizierbarkeitsaudit
gesetzt:
Traegt die autonome orientierte Source kontrollgetrennte Spektralleistung in
Baendern, in denen sich diffusive und Telegraph-Transferfunktion in Betrag
oder Phase ausreichend unterscheiden? Ohne solchen Inputkontrast kann ein
weiterer Lauf die Mechanismen nicht entscheiden. Reziprozitaet und ein
`d=3`-Claim bleiben gesperrt.

Das Audit besteht mit 6/6 Sources. Minimaler sourcegewichteter komplexer
Transferkontrast `1.064`, unterscheidbarer Output-Leistungsanteil mindestens
`0.9969` und Segmentdrift maximal `0.1568`. Persistenter/Ein-Schritt-Kontrast
liegt aber nur bei `0.951..1.008` (Median `0.991`). Das zeigt, dass die autonome
Quelle die bewusst verschiedenen Regeln unterscheiden kann, nicht dass
Persistenz noetig oder eines der Gesetze physikalisch ist. Dieser Pass oeffnete
genau den inzwischen abgeschlossenen dynamischen Common-Source-Holdout mit
festen Kopplungen und beiden Inputarmen.

Das dynamische Common-Source-Gate ist abgeschlossen und negativ. Beide
Mediatorregeln bestehen fuer alle 6/6 Paare Response-, Oddness-, Shape- und
Distanzgates. Die relative Trace-Trennung besteht jedoch nur in 4/6 Paaren
ueber alle drei Distanzen statt der geforderten 5/6. Im Nahfeld bestehen 4/6,
bei `5` und `10 R_pair` jeweils 6/6 Paare. Ohne unabhaengige Zieltrajektorie
waehlt dieser Befund weder ein Transportgesetz noch Persistenz; Kopplungs-
Retuning ist durch die Stopregel ausgeschlossen.

Die Dimensionsfrage ist damit nicht zeitgleich geloest. Der aktuelle
komponentenweise Kanal ist `O(d)`-aequivariant und uebertraegt jede Ambient-
Komponente mit demselben skalaren Filter. Er besitzt keinen Mechanismus, der
bei `d>3` gerade drei Richtungen aktiv laesst. Ein cross-`d`-Test wird erst
sinnvoll, nachdem eine solche rangreduzierende Dynamik explizit formuliert und
vor dem Lauf falsifizierbar gemacht wurde.

## Paper-Status

- **Paper 0:** mathematischer Anker oder Supplement; keine robuste
  Knotenexistenz behaupten.
- **Paper I:** Minimalmodell plus linearer co-moving Relaxationsbefund;
  nichtlineare Metastabilitaet und Teilchensprache vermeiden.
- **Paper II:** Zwei lokale Transportarchitekturen sind konstruiert, aber das
  dynamische Modellselektionsgate ist negativ. Propagationsgesetz,
  Raumzeitkinematik und `d=3` bleiben gesperrt, bis unabhaengige Evidenz bzw.
  ein echter Dimensionsreduktionsmechanismus vorliegt.
- **Paper III:** offene spekulative Tuer ohne Claim-Status.

## Reproduzierbarkeitsregeln

Jeder neue Evidenzlauf braucht vor dem Start:

- eine falsifizierbare Hypothese und passende Negativkontrolle;
- feste Seeds, Lauflaenge, Burn-in, Sampling und primaere Metrik;
- Git-Revision und sauberen Arbeitsbaum;
- maschinenlesbare Summary und datierten Review-Report;
- eine explizite Entscheidung `pass`, `fail`, `inconclusive` oder
  `pipeline-only`.

Lange Laeufe gehoeren nicht in CI. CI prueft Code, kleine deterministische
Kontrollen und die Dokumentationsoberflaeche.
