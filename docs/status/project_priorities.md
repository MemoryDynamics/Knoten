# Projektprioritaeten

Stand: 2026-07-26.

Diese Seite ist die aktive Arbeitsliste. Sie enthaelt hoechstens fuenf
parallele Gates. Das fruehere Arbeitsprotokoll mit abgeschlossenen Einzelschritten
liegt unter
`docs/archive/status/project_priorities_through_2026-07-20.md`.

## Leitentscheidung

Der aktuelle skalare Ast ist eine gut kontrollierte lineare Baseline, aber kein
isolierter nichtlinearer Knotenmechanismus. Neue Rechenzeit ist nur gerechtfertigt,
wenn ein Test zwischen konkurrierenden Mechanismen unterscheiden oder eine
bestehende Interpretation falsifizieren kann.

## P0: Paper-I-Claim-Synchronisation

Ziel: Text, Figuren und README auf dieselbe enge Lesart bringen.

Akzeptiert:

- nichtmarkovsche sichtbare Dynamik und augmentierte Markov-Einbettung;
- kompakte co-moving lineare Relaxationswolke gegen `eta=0`;
- reduzierte lineare Vorhersagebeschreibung fuer getestete Memory-Features.

Zu entfernen oder klar als historische Hypothese zu markieren:

- isolierte nichtlineare Metastabilitaet;
- `D_mem ~=3` als Dimensionsselektion;
- Spin-, Photon-, Ladungs-, Neutralitaets- oder Teilchensprache;
- Relaxationsrate als physikalische Masse.

Fertig, wenn `paper/paper_i`, `docs/status/paper_claims.md` und die
kanonischen Reports dieselbe Claim-Grenze verwenden.

## P1: Orientierten Kanal mit fester Kopplung replizieren

Entscheidung: Das vorgeschaltete Cross-Readout-Gate scheitert in `d=3` und
`d=10`. Selbst bei `sigma_rep/R_mem=2.5` und 1.25 kombinierten Memory-Radien
bleibt die Orientierungs-Driftspanne mit `1.96e-3` bzw. `4.32e-4` unter 1%; die
kalibrierte orientierungsabhaengige Verschiebung betraegt nur `5.98e-5` bzw.
`1.52e-5 R_mem` pro Memory-Zeit. Das ist ein pathweises negatives Gate aus je
einem Checkpoint, kein allgemeiner Unmoeglichkeitssatz fuer skalare Felder.

Als genau ein neuer Mechanismus wird daher **orientiertes Vektor-/Strommemory**
geoeffnet. Weitere direkte skalare Readout-Verengung ist beendet. Ein lokaler
oder retardierter skalarer Mediator bleibt fuer eine spaetere, getrennte
Lokalitaets- oder Laufzeitfrage zurueckgestellt; der vorliegende Test bewertet
nur seinen moeglichen skalaren Formpayload.

Der vorgeschaltete History-Current-Audit scheitert ebenfalls in beiden
Einbettungen. Bei `sigma/R_mem=2.5` liegen polarer Strom in `d=3/10` nur bei
`0.474/0.168` und antisymmetrische Zirkulation bei `0.626/0.743` ihrer
jeweiligen konditionalen 99%-Random-Sign-Schwelle. Die Richtungen sind zur
groeberen Skala stabil, aber die Koharenzamplituden sind nicht von der Null
getrennt. Das ist erneut pathweise Evidenz aus je einem Checkpoint: Die
vorhandene geordnete Historie kann unter diesen Observablen nicht einfach als
kohaerente orientierte Quelle umbenannt werden.

Als genau ein neuer Mechanismus ist damit ein **eigenstaendig evolvierender
orientierter Zustand** ausgewaehlt und vorregistriert. Der passive Zusatzkanal
mittelt die normierte Source-Schrittrichtung linear mit
`kappa=lambda_v=alpha=0.01`; er wirkt nur einseitig auf ein skalares
Target, waehrend die skalare Source autonom bleibt. Persistenz wird damit
explizit hinzugefuegt und nicht als emergent beansprucht. Ein lokaler/
retardierter Skalarmediator wird nicht parallel geoeffnet.

Festes Gate vor dem kanonischen Lauf:

1. Sechs unabhaengige `d=3`, `N=3M`-Formationen, je 20 Vektormemory-Zeiten.
2. Gleiche Source-/Target-Zukunftsrauschpfade fuer aktiven Kanal, globalen
   Vorzeichenflip, exakten Kanal-aus-Pfad und 16 depositweise Random-Sign-Nullen.
3. Ein `lambda_v=kappa=1`-Arm prueft, ob persistentes Memory die konditionale
   Nulltrennung gegenueber einem Ein-Schritt-Kanal um mindestens Faktor 1.25
   verbessert.
4. Pro Seed gelten vorab: `active/random-q95 >= 2`, `active/R_mem >= 1e-3`,
   Flip-Kosinus `<= -0.9`, Tangentialanteil `>= 0.5`, Target-Radius und
   Shape-Tensor jeweils `<= 0.1` relative Aenderung sowie Source-Radius
   `<= 0.5` und Source-Shapespektrum `<= 0.25` Drift.
5. Gesamtpass nur bei mindestens 5/6 Seeds. Fail beendet oder reformuliert
   genau diesen orientierten Zustand; keine seedweise Nachkalibrierung.

Ergebnis: Das Gate besteht in 6/6 Seeds. Persistent/random-q95 liegt bei
`5.76..11.64`, der Ein-Schritt-Arm bei `1.40..2.04`; der Persistenzgewinn
betraegt `3.50..8.05`. Flip, Tangentialanteil und alle Shape-Bounds bestehen.
Die aktive Verschiebung bleibt mit `0.0040..0.0076 R_mem` klein. Damit traegt
der eingefuehrte Zustand einen kontrollgetrennten relationalen Kanal, aber
Persistenz und instantanes direktes Vektorreadout sind weiterhin Modellinputs.

Naechstes diskriminierendes Gate, ohne neuen Parametersweep:

1. Ein globales `eta_v=5.079e-6`, abgeleitet als Median der sechs
   vorab normalisierten Kopplungen, wird fuer alle Folgefaelle festgehalten.
2. Source und Target stammen aus verschiedenen Formationsseeds in einer festen
   zyklischen Paarung statt aus demselben geklonten Zustand.
3. Mit `R_pair=(R_source+R_target)/2`, `sigma_v=2.5 R_source` und der
   Distanzleiter `2.5, 5, 10 R_pair` werden feste Nahantwort, raeumliche
   Abschwaechung und ein praktischer Fernnullarm geprueft.
4. 64 Random-Sign-Pfade, channel-off, globaler Flip und Ein-Schritt-Memory
   verwenden weiter gemeinsames Zukunftsrauschen.
5. Der Nahpass verwendet die bisherigen Gates `active/random-q95 >= 2`,
   `active/R_target >= 1e-3`, Persistenzgewinn `>= 1.25`, Flip-Kosinus
   `<= -0.9` mit Magnitudenverhaeltnis `0.5..2` sowie dieselben Source-/
   Target-Shape-Bounds. Der Tangentialanteil wird nur berichtet: Bei
   unabhaengiger Formation ist die Source-Orientierung nicht an die
   willkuerliche Paarachse gebunden.
6. Distanzpass: Antwort nicht zunehmend mit 10% numerischer Toleranz und
   `response(10 R_pair)/response(2.5 R_pair) <= 0.1`. Gesamtpass nur bei
   mindestens 5/6 zyklischen Paaren. Nur dann wird ein lokaler/retardierter
   orientierter Feldzustand geoeffnet.

Ergebnis: Das feste-Kopplungs-Gate besteht in 6/6 zyklisch unabhaengigen
Paaren. Nahantwort `0.00177..0.00777 R_target`, Random-Sign-Trennung
`3.16..11.70`, Persistenzgewinn `2.25..8.64` und Fern/Nah-Verhaeltnis
`9.36e-4..2.80e-3`; Flip und alle Shape-Bounds bestehen. Ein Paar besitzt nur
`0.341` Tangentialanteil und bestaetigt damit, dass die willkuerliche Paarachse
kein universelles Transversalitaetsgate sein darf.

Das ist eine Generalisierungs- und Pipeline-Evidenz fuer den konstruierten
instantanen Gauss-Readout. Die beobachtete Abschwaechung ist durch dessen
Kernelregel erwartet und keine emergente Lokalitaets-, Propagations- oder
QFT-Evidenz. Reziproke Kopplung bleibt gesperrt.

Naechstes Gate: ein gemeinsames lokales Mediatorgesetz wird auf genau einem
Kalibrationspaar im Nahfeld an die bestehende Antwortskala angepasst und dann
ohne Retuning auf die uebrigen Paare/Distanzen angewendet. Ein kontrollierter
Source-Puls vergleicht zwei vorab getrennte Hypothesen: Relaxations-Diffusion
mit Lag-Skalierung `t ~ r^2` gegen einen gedaempften Wave-/Telegraph-Zustand mit
`t ~ r`. Primaer sind Kontrollabstand, monotoner Onset-/Peak-Lag, Out-of-sample
Skalengesetz und Shape-Huelle. Erst ein reproduzierbarer Holdout-Pass oeffnet
eine reziproke Mehrknotenprobe; auch er waere noch kein Photon-, Spin-,
Ladungs-, Teilchen- oder QFT-Claim.

## P2: Scheinmoden analytisch einordnen

Die komplexen AR-Nebenmoden ueberlappen fuer aktiv und `eta=0` praktisch
vollstaendig und driften zwischen Zeitsegmenten. Die Arbeitsannahme ist daher
ein lineares Sampling-/Projektionsphaenomen, nicht ein physikalischer Modus.

Naechster diskriminierender Test:

- lineares Zustandsraummodell oder analytische Nullreferenz fuer dieselbe
  Sampling-Cadence ableiten;
- Eigenvektor-, Rate- und Segment-Matching gegen diese Referenz pruefen;
- keine weitere Parametersuche, bevor die Nullherkunft verstanden ist.

Pass: aktive Moden trennen sich seed- und segmentstabil von der Nullreferenz.
Fail: dieselbe Modenfamilie entsteht im linearen oder `eta=0`-Modell.

Ein spaeterer positiver Modentest muss keine permanente globale Sinusmode
fordern. Fuer ueberwiegend chaotische gekoppelte Dynamik ist ModeScore v0.2
ereignisbasiert: vorab segmentierte Bursts, Duty-Cycle, Dauer/Survival,
Within-event Frequenz/Q und Phasenkontinuitaet sowie Kontroll-/Surrogatabstand.
Diese Modenmetriken bleiben strikt getrennt vom KnotScore, der die statistisch
gebundene Identitaet und Shape-Huelle bewertet.

## P3: Interaktionsbefunde ueber unabhaengige Zustaende haerten

Der signierte skalare Kanal besteht Architekturtests, verwendet aber extern
vergebene Labels und bislang zu wenige unabhaengige Zustaende. Der positive
skalare Fernkanal zeigt Translation ohne kontrollgetrennte Formdynamik.

Nur falls der Mechanismus weiterverwendet wird:

- mindestens sechs, bevorzugt zehn unabhaengige Formationszustaende;
- feste Distanzleiter ohne seedweises Retuning;
- Source-Eligibility vor Stoerung;
- getrennte Center-, Radius- und Shape-Entscheidungen;
- `pass`, `fail` oder `inconclusive` pro primaerem Gate.

Eine verlaengerte Laufzeit desselben negativen Fernkanals hat derzeit niedrigere
Prioritaet als ein mechanistisch anderer Test.

## P4: Kuration und Infrastruktur

Bei jedem wissenschaftlichen Commit:

- Ruff, Tests und MkDocs strict ausfuehren;
- nur reviewed Summaries, Reports und Figuren tracken;
- `reports/README.md` aktualisieren, wenn sich die kanonische Evidenzschiene
  aendert;
- keine Buildprodukte, Caches oder Scratch-Kopien committen;
- alte Zwischenlesarten als `legacy-sign`, `superseded`, `pipeline-only` oder
  `negative` kennzeichnen statt sie still zu loeschen.

## Stopregeln

Ein Arbeitszweig wird beendet oder neu formuliert, wenn eines gilt:

- der Effekt ist in der passenden Negativkontrolle gleich gross;
- das Ergebnis haengt von einem einzelnen Seed, Voxel oder Fitfenster ab;
- eine laengere Laufzeit vergroessert nur einen bereits linearen Trend;
- die primaere Observable ist nicht vor dem Lauf festgelegt;
- der Mechanismus erfordert nachtraegliches seedweises Retuning;
- ein einfacheres Modell erklaert dieselben KPIs innerhalb der Messgenauigkeit.

## Bewusst zurueckgestellt

- reziproke Mehrknotenkopplung;
- weitere reine Skalar-Amplituden- oder Epsilon-Sweeps;
- eindeutige externe `d=3`-Selektion;
- harte endliche Signalgeschwindigkeit aus direkter Fernkopplung;
- Lorentz-, Quanten- und Standardmodellableitungen;
- physikalische Massen- oder Ladungsidentifikation.

## Abgeschlossene Evidenzbloecke

1. **Kernel und Skalarast:** Signkorrektur, matched Ablation, lineare
   Reconciliation und feste-`g`-Skalenpruefung.
2. **Dimension:** Ambient-Sweeps, D_spec-Sensitivitaet und Rohsnapshot-Retest;
   kein robuster externer 3D-Claim.
3. **Memory-Feld:** spektrale Reprasentation, Relaxations-Diffusion,
   Realraum-/Aufloesungskontrollen und negativer Mode-Identity-Audit.
4. **Externe Antwort:** Weak Probe, Frozen Source, signierter Architekturtest
   sowie One-Way-Source- und Interaction-Age-Gates.
5. **Repository-Hardening:** Paketkern, Checkpoints, Tests, CI und kuratierte
   Doku-Frontdoor.

Die zugehoerigen Entscheidungstragenden Reports sind in `reports/README.md`
indexiert; die vollstaendige Chronologie bleibt im Doku-Archiv und in Git.
