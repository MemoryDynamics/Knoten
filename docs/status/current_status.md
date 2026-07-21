# Aktueller Stand

Stand: 2026-07-21.

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
| Externe skalare Antwort | Weak-Probe und Frozen-Source sind isotrop vollrangig. Der One-Way-Audit bis `N=103M` zeigt nahezu lineare Zentrumtranslation. | skalarer Fernfeld-Translationskanal | `0/5` Seeds zeigen kontrollgetrennte Formmodifikation; keine Oszillation, Ladung oder neuer Knotentyp |
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

### Offene Hypothesen

- Ein lokaler oder retardierter Mediator koennte einen diskriminierenden
  Transportkanal erzeugen.
- Orientiertes/Vektormemory koennte relationale Observablen tragen, muss sich
  aber gegen Nullkraft- und Randomized-Channel-Kontrollen trennen.
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

Diese Auswahl ist eine Entscheidungsschiene, keine Behauptung, dass andere
Reports geloescht oder ungueltig seien. Fruehe `legacy-sign`-Reports erklaeren
die Historie, tragen aber keine aktuellen Kernelclaims.

## Aktiver Codepfad

- `src/emergenz_knoten/`: kanonischer Paketkern.
- `src/emergenz_knoten/markov/`: reduzierte Operator- und Closure-Werkzeuge.
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

Vor dessen dynamischer Implementierung sind Nullmodell, primaere Observable,
mindestens sechs unabhaengige Formationszustaende, Akzeptanzschwelle und
Stopregel festzulegen. Ein positiver Einzelplot oder ein bester Seed genuegt
nicht.

## Paper-Status

- **Paper 0:** mathematischer Anker oder Supplement; keine robuste
  Knotenexistenz behaupten.
- **Paper I:** Minimalmodell plus linearer co-moving Relaxationsbefund;
  nichtlineare Metastabilitaet und Teilchensprache vermeiden.
- **Paper II:** Propagation und Raumzeitkinematik bleiben gesperrt, bis ein
  lokaler, kontrollgetrennter Transportkanal besteht.
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
