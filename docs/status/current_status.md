# Aktueller Stand

Stand: 2026-08-04.

Diese Seite ist die kurze wissenschaftliche Frontdoor. Details, Laufprotokolle
und historische Zwischenlesarten stehen in den datierten Reports und in
`docs/archive/status/current_status_through_2026-07-21.md`.

## Sieben-Punkte-Ueberblick

| Bereich | Evidenz | Belastbare Lesart | Grenze |
| --- | --- | --- | --- |
| Modellkern | Der sichtbare Prozess ist im Allgemeinen nichtmarkovsch; Position plus vollstaendiger Memory-Zustand bilden die Markov-Einbettung. | strukturelles Resultat des definierten Modells | keine Aussage ueber reale Raumzeit |
| Skalarer kompakter Ast | Gematchter Ein- und Zweiskalenkernel kollabieren auf der Achse `A_eff=A_att-9`; Long-Run-Radien folgen dem linearen Finite-Memory-Modus bis maximal `1.16%` relativ. Ein retrospektives Checkpoint-/Holdout-Gate besteht fuer 5/5 Seeds von `N=1M..30M` gegen `N=300M`. | kontrollierte co-moving Relaxationswolke mit methodisch bestaetigter spaeter Endstationaritaet | kein isolierter nichtlinearer Knoten, kein Phasenuebergang und keine identifizierte Formationszeit |
| Nichtlinearitaetsgate | Bei `R_linear/L=0.3` liegt der Radius seed-stabil etwa `6.2%` ueber linear, ohne Shape-Umschlag. | kleine glatte Kernelkorrektur | vorregistrierte Composite-Entscheidung bleibt `inconclusive`; Residence-Metriken sind skalenempfindlich |
| Dimension | `D_mem` folgt im linearen isotropen Regime der Ambient-Geometrie; Heat-Trace- und Shape-Dimension trennen sich. | Diagnostik der gespeicherten Wolke | keine eindeutige externe `d=3`-Selektion |
| Feld- und Memory-Operatoren | Fourier-`rho` reproduziert das exponentielle Memory. `phi=K*rho` ist linear exakt. Der aktive Delta-Quellfeld-Pilot bildet kontrolliert einen beschraenkten Peak bei `k=1`. Der exakte `eta=0`-Rohmodenblock und alle vollstaendigen N=1M-Fits bleiben reell. | kompakte Reprasentation, klassische Finite-k-Musterbildung und analytisch klassifizierte AR-Nullmoden | `a2<0` und kubische Saettigung sind Modellannahmen; Feldmuster und komplexe ausgerichtete AR-Paare sind nicht feedback-spezifisch |
| Externe Antwort | Der persistente Vektorkanal besteht das feste-Kopplungs-/Distanzgate in 6/6 Paaren. Direkte und Telegraph-retardierte skalare Reziprozitaet sind aktiv und formschonend, aber alle 60 direkten und 80 P3.2-Segmentfits bleiben reell. | kontrollierter relationaler Kanal plus direkte/verzoegerte Bindung und Relaxation | ein Formationsbecken; der Telegraph-Eingang bleibt zielabhaengig; kein komplexer Modus, lokales Feldgesetz, Spin-, Ladungs- oder Teilchenclaim |
| Paper-Programm | Paper 0 traegt als mathematischer Anker; Paper I kann den linearen Relaxationsbefund berichten. | eng begrenzter Minimalmodell-Claim | Propagation, Lorentz-, Quanten- und Standardmodellbruecken bleiben Future Work |

## Evidenz, Inferenz und Hypothese

### Strukturell gestuetzt

- Die exponentielle Memory-Dynamik ist im augmentierten Zustand markovsch.
- Die Memory-Faser kontrahiert unter den dokumentierten Normannahmen pfadweise.
- `state.py` und `checkpoints.py` repraesentieren den implementierten
  finite-memory Zustand vollstaendig und checksum-validiert.
- Die spektrale `rho`-Darstellung ist fuer die getestete periodische
  1D-Reprasentation numerisch mit der direkten Historie reconciliiert.
- Die lineare Write-/Read-Reparametrisierung `phi=K*rho` ist analytisch exakt
  und im Drei-Seed-Audit fuer Pfad, Feld und Gradient bis `1.5e-14`
  bestaetigt. Dirac-Faltung ist der Identitaetsreadout; ein konstantes `K=1`
  erzeugt exakt keinen Gradienten.
- Ein auf die bestehende lokale Kruemmung gematchter LoG-Kernel ist analytisch
  abklingend und exakt zero mean. Das ist eine verfuegbare Nullfamilie, keine
  Evidenz fuer Neutralitaet oder eine bestimmte Amplitude.
- Die eingeschraenkte lokale skalare Feldentwicklung
  `tau d_t phi=-(c0-c2 Delta+c4 Delta^2)phi+(s0-s2 Delta)rho+...`
  besitzt den stationaeren Transfer
  `H(k)=(s0+s2 k^2)/(c0+c2 k^2+c4 k^4)`. Sie matcht den normierten
  Gausskernel bis `k^4`; `s0=0` erzwingt exakt `H(0)=0`.

### Numerisch gestuetzt

- Der aktuelle kleine-Radius-Ast ist kompakter als `eta=0`, wird aber fast
  vollstaendig durch den linearen Memory-Center-Relativmodus erklaert.
- Fuer `d=10`, `A_att=35` bestehen 5/5 Seeds ein retrospektives Altersgate
  ueber `N={1M,3M,10M,30M}` und den separaten `N=300M`-Holdout sowie lokale
  Radius-Endfenster. Der Befund bestaetigt spaete Endstationaritaet innerhalb
  der Messgrenzen, nicht deren erste Entstehungszeit; zeitaufgeloeste
  Shape-Fenster fehlen in den Legacy-Traces.
- Die dichtere Dimensionsreproduktion ueber sechs N-Endpunkte zeigt fuer drei
  gematchte Seeds `D_mem=8.857..9.268` im vorgegebenen `d=10`. `D_cov`
  schwankt; der spaete `D_occ`/`D_win`-Rueckgang ist mit zehnfach groberem
  Sampling konfundiert. Daraus folgt weder ein Plateaugesetz noch 3D-Selektion.
- Das aktive skalare Delta-Quellfeld besteht den vorregistrierten
  Mechanismus-Piloten in drei Seeds: `dt=0.05` gegen `0.025` und `N_x=256`
  gegen `512` stimmen in niedrigen Moden bis `6.12e-7` bzw. `7.50e-11`
  relativ ueberein. Der aktive Arm saettigt bei `k=1`, cubic-off erreicht den
  Sicherheitsstopp und source-off bleibt exakt null. `eta=0` bildet nahezu
  dasselbe Feld, daher ist nur klassische Musterbildung gestuetzt. Explorativ
  verschiebt das aktive Readout die Source-Field-Phase von etwa null auf pi
  und die Quelle um etwa eine halbe Wellenlaenge, bevor sie spaet pinnt.
- Die dynamische Relaxations-Diffusion veraendert Radius und Kraft glatt und
  aufloesungsstabil; sie liefert eine reduzierte Vorhersagebeschreibung.
- Der exakte `eta=0`-Rohmodenblock besitzt nur reelle Multiplikatoren. Bei
  derselben N=1M-Kadenz bleiben gepoolte (`0/15`) und vollstaendige seedweise
  (`0/75`) Rohfits reell; `27/375` kurze Segmentfits zeigen nur kleine
  konditionierungsbedingte Leckpaare bis `7.25e-4` Frequenz pro Memory-Zeit.
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
- Der feste P3.2-Telegraph-Filter besteht Mediator-, Response- und Shape-Gates
  in 5/5 Common-Noise-Fortsetzungen. Alle 80 rohen Segmentfits in Kanal-aus,
  direkt reziprok, retardiert einseitig und retardiert reziprok bleiben exakt
  reell. Der retardierte Endabstand `0.58..1.21R` gegen direkt `0.31..0.88R`
  stuetzt verzoegerte oder geschwaechte Bindung, keine beobachtbare Rotation.
  Da der Eingang weiterhin ein zielabhaengiger Cross-Gradient ist, ist dies
  noch keine rein quelllokale Feldtheorie.


### Nicht gestuetzt oder widerlegt

- Ein spezifisch zweiskaliger nichtlinearer Knotenmechanismus ist nicht
  isoliert.
- Die vorhandenen Scans selektieren keinen exakten Amplitudenwert. Insbesondere
  folgt `A_eff=26` aus der aktuellen Parametrisierung; `27=3^3` und der daraus
  hypothetisch gebildete Rohwert `36` sind nicht dynamisch hergeleitet.
- Komplexe ausgerichtete AR-Moden sind nicht von `eta=0` getrennt und nicht
  segmentstabil. Die exakte rohe Memory-Null ist reell; damit sind die
  bestehenden Paare Darstellungs-/Fitmoden und keine Oszillations- oder
  Photonenevidenz.
- `D_mem` nahe drei im 3D-Embedding ist keine Dimensionsselektion.
- Der positive skalare Memory-Kanal besitzt keine interne Ladungs- oder
  Neutralitaetsstruktur.
- Direkte Fernkopplung und diffusive Felder liefern keine harte endliche
  Signalgeschwindigkeit.
- Der aktuelle komponentenweise Vektormediator kann keine eindeutige
  Ambient-Dimension drei selektieren: Seine Ambient-Transfermatrix ist
  proportional zu `I_d` und erhaelt ohne weiteren Mechanismus den Rang einer
  vollrangigen Source.
- Der vorhandene Random Walk bestimmt weder einen negativen `k^2`-Term noch
  quadratische/kubische Feldnichtlinearitaeten. Eine endliche-Wellenzahl-
  Instabilitaet, diskrete Aeste oder Quantisierung sind daher nicht aus den
  bisherigen Annahmen abgeleitet.

### Offene Hypothesen

- Ein spaeteres physikalisches Mediatorgesetz braucht ein unabhaengiges
  Targetkriterium oder eine weitere falsifizierbare Mechanismusannahme. Ein
  weiterer Fit derselben Kopplungen an dieselben Zielantworten waere nicht
  identifizierend.
- Felder selektieren nicht automatisch drei Dimensionen. Eine spaetere
  Dimensionshypothese braucht dieselbe eingefrorene Regel ueber mehrere
  Ambient-Dimensionen und einen kontrollgetrennten effektiven Response- oder
  Modenrang; eine 3D-Feldsimulation waere nur eine 3D-Annahme.
- Weitere reziproke Vollsimulationen sind erst sinnvoll, wenn eine quelllokale
  Emissions-/Readout-Regel analytisch definiert und ihr sichtbarer Modus vorab
  von den eingesetzten internen Mediatorpolen getrennt ist.
- Der angenommene negative dimensionslose `k^2`-Koeffizient in
  `P(u)=1+a2 u^2+u^4` erzeugt mit kubischer Saettigung numerisch robuste
  endliche Wellenzahlen. Weil derselbe Ast fuer `eta=0` entsteht, braucht ein
  naechster Feldtest eine vorab definierte feedback-spezifische Observable
  oder unabhaengige Source-/Target-Dynamik; weitere Koeffizientensuche waere
  nicht identifizierend.

## Kanonische Evidenzschiene

Der kuratierte Einstieg in die mehr als 100 Markdown-Reports liegt in
`reports/README.md`. Fuer den aktuellen Entscheidungsstand sind besonders
wichtig:

1. `reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md`
2. `reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md`
3. `reports/long_runs/stability/checkpoint_stability_gate_d10_A35_2026-07-30.md`
4. `reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md`
5. `reports/memory/low_mode_identity_audit_2026-07-20.md`
6. `reports/memory/eta_zero_raw_mode_null_audit_2026-07-31.md`
7. `reports/response/one_way_interaction_age_N3M_2026-07-21.md`
8. `reports/response/scalar_cross_readout_resolution_2026-07-21.md`
9. `reports/response/oriented_history_current_audit_2026-07-21.md`
10. `reports/response/oriented_vector_one_way_gate_2026-07-25.md`
11. `reports/response/oriented_vector_fixed_pair_distance_gate_2026-07-26.md`
12. `reports/response/local_oriented_mediator_gate_2026-07-28.md`
13. `reports/response/oriented_source_mediator_identifiability_2026-07-28.md`
14. `reports/response/dynamic_common_source_mediator_gate_2026-07-28.md`
15. `reports/kernels/field/local_field_operator_audit_2026-07-29.md`
16. `reports/kernels/field/write_read_reparameterization_audit_2026-07-30.md`
17. `reports/kernels/field/active_scalar_delta_field_pilot_2026-07-31.md`
18. `reports/response/reciprocal_full_knot_gate_2026-08-04.md`
19. `reports/response/retarded_reciprocal_full_knot_gate_2026-08-04.md`

Diese Auswahl ist eine Entscheidungsschiene, keine Behauptung, dass andere
Reports geloescht oder ungueltig seien. Fruehe `legacy-sign`-Reports erklaeren
die Historie, tragen aber keine aktuellen Kernelclaims.

## Aktiver Codepfad

- `src/emergenz_knoten/`: kanonischer Paketkern.
- `src/emergenz_knoten/markov/`: reduzierte Operator- und Closure-Werkzeuge.
- `src/emergenz_knoten/stability.py`: Checkpoint-, Holdout- und lokale
  Stationaritaetsgates fuer lange Formationslaeufe.
- `src/emergenz_knoten/measurement_stability.py`: separates
  Messkonvergenzgate fuer cadence- und estimatorabhaengige
  Occupancy-Dimensionen.
- `src/emergenz_knoten/active_scalar_field.py`: reelles periodisches
  ETD1-Delta-Quellfeld mit kubischer 1/2-Dealiasing-Regel.
- `src/emergenz_knoten/oriented_source.py`: passiver orientierter Zusatzstate
  mit gepaarten One-Way-Kontrollen.
- `src/emergenz_knoten/oriented_diagnostics.py`: gemeinsame Response-, Shape-
  und Distanzmetriken fuer den konstruierten orientierten Kanal.
- `src/emergenz_knoten/local_mediator.py`: lokale 1D
  Relaxations-Diffusions- und Telegraph-Zustaende.
- `src/emergenz_knoten/mediator_identifiability.py`: segmentierte
  Source-Spektren und sourcegewichteter komplexer Transferkontrast.
- `src/emergenz_knoten/retarded_reciprocal.py`: direkte und statisch normierte
  Telegraph-retardierte Vollknotenarme mit festen Common-Noise-Kontrollen.
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

Der analytische lokale Feldoperator-Audit schliesst diese Rang-Null nun als
getestete Paketfunktion ab. Zugleich trennt er die bisherige Gauss-/LoG-
Nullfamilie von einem moeglichen neuen Mechanismus: Erst `a2<0` in
`1+a2 u^2+u^4` erzeugt ein bevorzugtes endliches Wellenzahlband. Der
kritische Wert `a2=-2`, eine positive nichtlineare Saettigung und eine
komponentenuebergreifende Ordnung sind jedoch zusaetzliche Annahmen. Deshalb
folgt weder Quantisierung noch `d=3` aus diesem Audit.

Der anschliessende aktive Delta-Quellfeld-Pilot besteht das numerische und
klassische Finite-k-Mechanismusgate. Die kubisch gesaettigte Instabilitaet ist
beschraenkt, waehrend cubic-off divergiert und source-off exakt null bleibt.
Da `eta=0` dieselbe Feldordnung traegt, ist dies noch kein gekoppelter Knoten.
Die beobachtete feedback-spezifische Phasenrelokation ist explorativ und kein
Oszillations- oder Metastabilitaetsgate. Die analytische Nullreferenz fuer die
AR-Scheinmoden ist nun abgeschlossen:
Der rohe `eta=0`-Operator ist reell, volle N=1M-Fits bleiben reell und die
ausgerichteten komplexen Paare sind nicht kontrollgetrennt. Der Feldzweig wird
daher nicht mit einem freien Koeffizientensweep erweitert. P3.1 und P3.2 sind
nun abgeschlossen: Direkte und Telegraph-retardierte skalare Reziprozitaet
sind aktiv, formschonend und bindend, liefern in den registrierten
`(x_-,m_-)`-Fits aber ausschliesslich reelle Moden. P3.3 bleibt gesperrt.
P3.2a/b ist nun abgeschlossen. Der sichtbare `(x_-,m_-)`-Delayzustand
besteht bei allen neun Seed-/Rauschkorrelationspaaren das Holdout-Closure- und
Identifizierbarkeitsgate mit `kappa=46.8..81.0`, aber ohne ein einziges
tiefenstabiles Segmentmatching. Feld- und Impulsreadouts liefern nur
`-1.94%..+0.20%` zusaetzlichen Holdout-Gewinn und machen die augmentierte
Delaymatrix mit `kappa=1.55e16..1.93e16` spektral nicht identifizierbar.
Ihre 33/36 scheinbar passenden komplexen Segmente sind deshalb kein Modenpass.

Die Variation `rho={0,0.9,0.99}` haelt die Einzelknoten-Rauschleistung bei
etwa `0.818R` und senkt den relativen RMS-Schritt wie vorhergesagt auf etwa
`0.579R`, `0.183R` und `0.0579R`. Der mittlere retardiert reziproke
Endabstand sinkt entsprechend von `0.946R` auf `0.299R` und `0.0946R`;
die Closure-Kurven bleiben nahezu unveraendert. Das ist staerkere Bindung bei
kleinerer relativer Diffusion, kein Rausch-Unmasking einer Oszillation.

Der beobachtete leichte Anstieg von RMSE/Persistenz ueber die kurze Delayleiter
ist noch kein physikalischer Persistenztrend: tiefere OLS-Fits verlieren dort
Trainingsziele und gewinnen Regressoren. Der nun vorregistrierte
Langhorizont-Audit haelt deshalb alle Trainings- und Testzielzeiten konstant,
verwendet feste Hankelraenge `{2,4,8,16,32}` und erweitert bei unveraenderter
50-Update-Cadence auf 1000..12500 Updates Historie. Drei Seeds und
`rho={0,0.9,0.99}` werden reziprok gegen den Einweg-Mediator verglichen; weder
Gain noch Lambda, Epsilon oder Kernel werden veraendert.

Dieser Schritt entscheidet nur ueber rank-robusten zusaetzlichen
Vorhersagenutzen und numerischen Rang. Gespeicherte reduzierte DMD-Pole sind
noch kein Modenbefund; dafuer bleibt anschliessend Identitaet ueber Rang,
Delaytiefe, Zeitsegmente und Kontrolle erforderlich. Erst danach kommt P3.2c
mit einer quelllokalen Emissions-/Readout-Regel. Keines dieser Gates wertet das
negative registrierte P3.2-AR(1)-Primaergate rueckwirkend um. Die
Long-Run-Geometrieschiene bleibt mit eingefrorener Messmethodik erhalten.

## Paper-Status

- **Paper 0:** mathematischer Anker oder Supplement; keine robuste
  Knotenexistenz behaupten.
- **Paper I:** Minimalmodell plus linearer co-moving Relaxationsbefund;
  nichtlineare Metastabilitaet und Teilchensprache vermeiden.
- **Paper II:** Zwei lokale Transportarchitekturen sind konstruiert; sowohl das
  dynamische Modellselektionsgate als auch das feste reziproke Telegraph-
  Modengate sind negativ. Propagationsgesetz, Raumzeitkinematik und `d=3`
  bleiben gesperrt, bis unabhaengige Evidenz, eine quelllokale Feldregel und
  ein echter Dimensionsreduktionsmechanismus vorliegen.
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
