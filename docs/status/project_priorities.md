# Projektprioritaeten

Stand: 2026-07-21.

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

## P1: Genau ein neues Transportgate vorregistrieren

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

Pflichtfelder vor Implementierung:

1. Mechanismushypothese und konkurrierendes Nullmodell.
2. Primaere relationale Observable; Zentrumtranslation allein reicht nicht.
3. Mindestens sechs unabhaengige Formations- oder Checkpointzustaende fuer
   inferentielle Aussagen.
4. Gemeinsames Zukunftsrauschen, ungeprobter Pfad und deaktivierter Kanal.
5. Schwellen fuer Source-Eligibility, Shape-Boundedness, Readout und
   Seed-Reproduzierbarkeit.
6. Stopregel, die auch ein negatives Ergebnis beendet.

Reziproke Kopplung bleibt gesperrt, bis ein One-Way-Kanal dieses Gate besteht.

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
