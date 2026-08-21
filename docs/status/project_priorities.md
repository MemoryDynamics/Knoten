# Projektprioritaeten

Stand: 2026-08-21.

Diese Seite ist die aktive Arbeitsliste. Sie enthaelt hoechstens fuenf
parallele Gates. Das fruehere Arbeitsprotokoll mit abgeschlossenen Einzelschritten
liegt unter
`docs/archive/status/project_priorities_through_2026-07-20.md`.

## Leitentscheidung

Der aktuelle skalare Ast ist eine gut kontrollierte lineare Baseline, aber kein
isolierter nichtlinearer Knotenmechanismus. Neue Rechenzeit ist nur gerechtfertigt,
wenn ein Test zwischen konkurrierenden Mechanismen unterscheiden oder eine
bestehende Interpretation falsifizieren kann.

Der getrennte native Rotating-wave-Ast hat diese Schwelle inzwischen fuer
**vorbereitete raeumliche Schleifen** erreicht: fuenf finite-H-Roots sind lokal
existenzzertifiziert, der Fixed-gain-Kontinuumsast ist unabhaengig reproduziert
und der Anchor ist lokal numerisch stabil. Das macht ihn nicht zu einem
internen S1, materiellen Knoten oder Masseobjekt.

## Massgebliche aktive Reihenfolge

Diese Liste ist fuer den Schleifenast autoritativ. Die laengeren P0--P3.8-
Abschnitte darunter dokumentieren parallele beziehungsweise historische
Programmaeste und heben diese sequentiellen Abhaengigkeiten nicht auf.

1. **Foundation und CI -- abgeschlossen.** Der historische main-CI-Fehler war
   ein Ruff-F401-Fehler durch neun fehlende `__all__`-Eintraege, nicht ein
   Rotationsfehler. Die Root-API besitzt nun einen allgemeinen
   Regressionscheck. Der Foundation-Audit besteht nach dokumentierter
   Decimal-Pipeline-Reconciliation alle A--E-Gates; der initiale Fail bleibt
   sichtbar.
2. **L5-Existenz und Skalierung -- als Naechstes.** Vor dem Lauf genau die
   Zelle
   \((\alpha,H,\eta)=(0.00125,9600,0.01875)\) mit unveraendertem
   \(H\alpha=12\), \(\eta/\alpha=15\) und unveraendertem Kernel einfrieren.
   Primaer sind lokaler Krawczyk-Einschluss, Astkorridor, exakte
   Dezimalskalierung und eine vorab definierte First-order-Diskrimination.
   Kein Amplituden-Retuning und kein gleichzeitiges Stabilitaetsclaim.
3. **Nicht-Anchor-Stabilitaet -- nur nach L5-Existenzpass.** Genau eine
   zertifizierte Nicht-Anchor-Zelle und zwei feste Arnoldi-Panels plus
   registrierte Stoerungen vorab waehlen. Ein negativer oder unvollstaendiger
   Spektralbefund stoppt Formation und Rauschen. Ein Pass bleibt lokal
   numerisch, solange keine vollstaendige Spektraleinschliessung vorliegt.
4. **Formation und Basin -- nur nach Nicht-Anchor-Stabilitaet.** Feste
   nichtkreisfoermige Historienfamilien, chirality-symmetrische Seeds und eine
   vorbereitete-Bahn-Positivkontrolle vorregistrieren. Erst Basin-Evidenz
   autorisiert unabhaengige Rauschzellen. Der \(A_{\rm att}=7\)-Holdout bleibt
   bis dahin versiegelt.
5. **Interne Topologie und Mechanik getrennt halten.** Persistent Homology der
   ambienten Kreisbahn ist kein interner S1-Test. Ein Topologieast darf erst
   eine quotientierte Observable oeffnen. Center-Aktuator, Arbeit und Masse
   bleiben ein separater Architekturast mit mikroskopischer Reziprozitaet und
   Ledger; ein Schleifenpass kann ihn nicht ersetzen.

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
- exakte ganzzahlige Kernelamplituden aus geometrischer Numerologie;
- Relaxationsrate als physikalische Masse.

Fertig, wenn `paper/paper_i`, `docs/status/paper_claims.md` und die
kanonischen Reports dieselbe Claim-Grenze verwenden.

Long-Run-Zulassungsprotokoll: Der retrospektive `d=10`, `A_att=35`-Audit
besteht fuer 5/5 Seeds. Vier Alterscheckpoints `N={1M,3M,10M,30M}` liegen bei
Radiusbereich, Radius-CV, Trend pro Dekade und rotationsinvariantem
Shape-Spektrum innerhalb der fixierten Grenzen; ein unangetasteter
`N=300M`-Holdout bestaetigt alle Seeds. Das macht `N=30M` zum ersten mit den
vorhandenen Daten pruefbaren Kandidaten, nicht zur nachgewiesenen
Formationszeit.

Fuer neue Formationslaeufe gilt verbindlich:

1. resumierbare Zustaende auf `N0*{1,3,10,30,100,...}` speichern;
2. vier Checkpoints ueber mindestens eine Dekade vor einer Kandidatur;
3. Radiusbereich `<=10%`, Radius-CV `<=15%`, Radiustrend pro Dekade `<=5%`
   und normalisierte Shape-Spektrum-TV `<=10%`;
4. ein mindestens dreimal spaeterer Holdout;
5. in jedem Checkpoint vier lokale Radius-/Shape-Fenster plus ein Holdout.

Legacy-Traces besitzen lokal nur Radius, keinen zeitaufgeloesten Shape-Tensor.
Ihr 5/5-Pass bleibt daher `retrospective provisional`; automatisches Stoppen
wird erst mit neu erzeugten Shape-Fenstern zulaessig.

`D_occ` und das automatische `D_win` sind kumulative, cadence- und
estimatorabhaengige Messungen und duerfen nicht in dieses intrinsische
Radius-/Shape-Gate gemischt werden. Das separate Messkonvergenzgate verlangt
vier vergleichbare Checkpoints, mindestens eine N-Dekade, festen Sampler und
Estimator sowie einen mindestens dreimal spaeteren Holdout. Der vorhandene
Sechs-Endpunkt-Satz ist nicht auswertbar: Trainingsbereich und Trend verfehlen
die 10%/5%-Grenzen, fruehe `D_win`-Fits sind ungueltig und bei `N=300M`
wechseln Cadence und Codeversion. Ein neuer Long Run muss deshalb dieselbe
Revision und feste Online-/Samplingdefinition durchgehend verwenden.

Die investierte Long-Run-Evidenz bleibt erhalten: `N=30M/300M`-Slices,
Parameter-Heatmaps und einzelne `D_occ`-nahe-drei-Punkte sind dokumentierte
Beobachtungen und Kandidatenkarten. Das neue Messkonvergenzgate verwirft diese
Daten nicht; es begrenzt nur die zulaessige Aussage. Heatmap-Punkte aus
wechselnden Revisionen, Cadences oder Fitfenstern duerfen weder als
N-unabhaengiges Plateau noch als Dimensionsselektion zusammengezogen werden.
Der naechste teure Lauf ist erst nach einer eingefrorenen
Online-Observable-/Checkpoint-Spezifikation zulaessig.

## P1: Orientierter Kanal und lokales Feldgesetz

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
ohne Retuning auf die uebrigen Paare/Distanzen angewendet. Implementiert werden
zwei getrennte lokale Markov-Erweiterungen auf der Source-Target-Achse:

```text
d_t a = D d_xx a - mu a + s
d_tt a + 2 gamma d_t a + omega_0^2 a = c^2 d_xx a + s.
```

Beide erhalten dieselbe am Kalibrationspaar fixierte Korrelationslaenge und
nominale Relaxationszeit. Die Source pulst eine Memory-Zeit; Target-Aktiv,
globaler Flip und Kanal-aus teilen Zukunftsrauschen. Primaer sind ein
Kalibrations-/Linearitaetscheck, Aufloesungsstabilitaet, monotone Lags,
Out-of-sample-Vorhersage und Shape-Huelle. Vier von fuenf vollstaendigen
Holdout-Paaren muessen ohne Retuning bestehen.

Wichtige Korrektur: Fuer Relaxations-Diffusion gilt `t_peak ~ r^2` nur im
schwach gedaempften Nahbereich. Aus
`G(r,t) ~ t^-1/2 exp[-r^2/(4Dt)-mu t]` folgt fuer einen kurzen Puls

```text
t_peak ~= [sqrt(1 + 4 mu r^2/D) - 1]/(4 mu) + T_pulse/2,
```

mit linearem Fernbereichs-Crossover. Der Telegraph-Arm wird dagegen am
Finite-Front-Onset `t_onset ~= r/c` geprueft. Das Experiment kann nur
Architekturkompatibilitaet vergleichen, nicht die physikalische Regel
entdecken, weil beide Transportgesetze Modellinputs sind. Auch ein Pass oeffnet
zunaechst nur eine dynamische One-Way-Source-Diskrimination, nicht sofort
Reziprozitaet.

Die 1D-Achse ist eine ressourcensparende relationale Kanalnaeherung und keine
Dimensionsselektion. Ein Feld kann in jedem vorgegebenen `d` existieren. Ein
spaeterer `d=3`-Test muss eine unveraenderte Mediatorregel und dieselben
absoluten dimensionslosen Parameter ueber mehrere Ambient-Dimensionen halten
und einen reproduzierbaren externen Response-/Modenrang nahe drei samt
Unterdrueckung weiterer Richtungen zeigen.

Ergebnis auf sauberem Commit `64c2826`: Beide konstruierten Regeln bestehen
ihre eigenen Architektur- und Holdout-Gates. Relaxations-Diffusion erreicht
`1.12%` medianen und `9.09%` maximalen Lag-Vorhersagefehler bei `0.31%`
maximaler Primaer/Fine-Aufloesungsdrift; Telegraph `5.55%`, `7.88%` und
`4.91%`. Jeweils `5/5` vollstaendige Holdout-Paare bestehen. Die finalen
Targetantworten liegen ueber alle Faelle bei `8.37e-4..8.96e-3 R_target`;
Shape- und Radiusstoerungen bleiben unter `3.72e-4` bzw. `1.31e-4`.

Entscheidung: **architecture pass, mechanism underdetermined**. Die Skalierung
ist in der jeweiligen Feldgleichung eingesetzt; der Lauf entdeckt keine der
beiden Regeln. Reziprozitaet und ein `d=3`-Claim bleiben gesperrt.

Naechster diskriminierender Schritt ohne Parametersweep:

1. Die sechs geerbten Source-Zustaende laufen nach 20 Memory-Zeiten Burn-in
   autonom ueber zwei nicht ueberlappende Segmente zu je 8192 Updates. Ein
   komponentensummiertes Hann-Periodogramm liefert die Nicht-DC-Leistung.
2. Statt eines frei gewaehlten Wellenvektors werden die exakten diskreten
   Impulsantworten beider bereits fixierten Mediatorgitter an allen 18
   geerbten Pair-Distanzen Fourier-transformiert. Pro Gesetz und Distanz wird
   nur der endliche DC-Gain auf eins normiert; keine Kopplung wird neu
   kalibriert.
3. Primaerer Source-Kanal ist die persistente Carrier-Orientierung. Die
   normierte Ein-Schritt-Richtung wird nur als diagnostischer Vergleich
   berichtet und ist kein Nullgate fuer die bereits eingefuehrte Persistenz.
4. Vorab gelten pro Pair und an allen drei Distanzen: komplexer
   Einzel-Frequenz-Kontrast `>=0.25`, sourcegewichteter Gesamtkontrast
   `>=0.25`, unterscheidbarer Output-Leistungsanteil `>=0.20`, uebertragener
   Leistungsanteil `>=0.01` und relative Segmentdrift des Kontrasts `<=0.25`.
   Source-Carrier-RMS muss `>=1e-3`, Radiusdrift `<=0.5` und normierte
   Shape-Spektrumdrift `<=0.25` sein.
5. Gesamtpass nur bei mindestens 5/6 Sources. Nur dann darf derselbe
   autonome Source-Trace ohne Retuning durch beide Mediatoren in ein
   dynamisches Holdout-Vorhersagegate eingehen.

Fail bedeutet: Die aktuellen Source-Daten koennen die Mediatorfamilien nicht
identifizieren; dann kein weiterer Lauf nur zur Erzeugung erwartbarer Kurven.
Ein Pass zeigt lediglich prinzipielle Input-Identifizierbarkeit. Er waehlt
weder ein physikalisches Feldgesetz noch den persistenten Kanal und selektiert
keine drei Dimensionen.

Ergebnis auf sauberem Commit `3619401`: **6/6 Sources bestehen**. Der kleinste
sourcegewichtete komplexe Kontrast ist `1.064`, der kleinste unterscheidbare
Output-Leistungsanteil `0.9969`, der kleinste uebertragene Leistungsanteil
`0.0322` und die groesste Zwei-Segment-Drift `0.1568`. Source-Radius und
Shape-Spektrum bleiben innerhalb der vorab gesetzten Huelle.

Die wichtige Negativabgrenzung: Persistenter/Ein-Schritt-Transferkontrast liegt
nur bei `0.951..1.008`, Median `0.991`. Die persistente Orientierung verlagert
Leistung in tiefe Frequenzen, ist fuer die reine Unterscheidbarkeit der beiden
bewusst verschiedenen Regeln aber nicht spezifisch erforderlich. Entscheidung:
**source eligible, mechanism and memory specificity underdetermined**.

Naechster Schritt ist genau ein dynamisches Common-Source-Holdout mit den
bereits kalibrierten Kopplungen. Vorregistrierte Regel:

1. dieselben sechs Paare und `2.5, 5, 10 R_pair`; 20 Memory-Zeiten gemeinsames
   Einschwingen von autonomer Source, Mediator und Target, danach 50
   Memory-Zeiten Auswertung bei Sampling alle 10 Updates;
2. Gitter, Mediatorparameter, Laengeneinheit und pulse-kalibrierte Kopplungen
   bleiben unveraendert. Die Vektorkomponenten treiben unabhaengige Kanaele
   desselben relationalen 1D-Mediators;
3. persistenter Carrier ist primaer. Ein-Schritt-Richtung, channel-off und
   globaler Flip laufen mit identischem Target-Zukunftsrauschen; der
   Ein-Schritt-Arm wird nicht nachtraeglich amplitude-gematcht und ist kein
   primaeres Gate;
4. pro Modell und Distanz muss die persistente Target-RMS-Antwort in
   `[1e-4, 0.1] R_target` liegen. Die Obergrenze haelt die feste Paarachse in
   ihrer linearen Geometriehuelle. Pfadweiser gerader Flip-Rest `<=0.1`,
   Flip-RMS-Verhaeltnis `0.9..1.1`, Target-Radius- und Shape-Aenderung je
   `<=0.1`; Source-Radius `<=0.5` und Shape-Spektrumdrift `<=0.25`;
5. pro Modell darf die RMS-Antwort mit 25% Toleranz nicht mit Distanz wachsen,
   Fern/Nah muss `<=0.5` sein. Der persistente Response-Trace beider Modelle
   muss an jeder Distanz relativ mindestens `0.25` getrennt sein;
6. Modell- und Separation-Pass jeweils erst bei mindestens 5/6 Paaren. Ein
   Fail stoppt oder reformuliert die lokale Erweiterung ohne Retuning.

Der Lauf darf nur Architekturunterschiede oder einen Shape-/Response-Fail
feststellen. Ohne unabhaengige beobachtete Target-Daten kann auch ein
Ein-Modell-Pass kein physikalisches Mediatorgesetz auswaehlen; Reziprozitaet
bleibt gesperrt.

Ergebnis auf sauberem Commit `b5b754e`: **dynamisches Diskriminationsgate
negativ**. Beide Regeln bestehen in 6/6 Paaren Response-Fenster, pfadweise
Oddness, Source-/Target-Shape und Distanzabschwachung. Relaxations-Diffusion
liefert `0.0043..0.0552 R_target`, Telegraph `0.0032..0.0454 R_target`; die
maximale Target-Shape-Aenderung bleibt `0.0015`. Die vorregistrierte
Modelltrennung besteht jedoch nur in 4/6 statt 5/6 Paaren, weil zwei Quellen
im Nahfeld unter `Delta_DT=0.25` bleiben. Bei `5` und `10 R_pair` bestehen
jeweils 6/6 Paare. Der Zweig wird nicht durch Kopplungsretuning gerettet.

Die persistente Source hat nur `0.0279..0.0311` RMS gegenueber der normierten
Ein-Schritt-Richtung `1`, erzeugt nach den stark filternden Mediatoren aber
eine aehnlich grosse Targetantwort. Das stuetzt eine spektrale Tiefpasslesart,
nicht die physikalische Auswahl eines Feldgesetzes oder die Notwendigkeit des
persistenten Kanals.

Die analytische Response-Rang-Null ist abgeschlossen und im Paket getestet.
Jede Ambient-Komponente laeuft unabhaengig durch denselben skalaren Transfer,
also `T=H I_d`; im festen `d=10`-Audit bleiben Eingangs- und Ausgangsrang zehn
und es entsteht keine Luecke nach Komponente drei. Ein cross-`d`-Lauf bleibt
gesperrt, solange kein expliziter komponentenuebergreifender Ordnungsparameter
oder anderer falsifizierbarer Unterdrueckungsmechanismus existiert.

Der lokale Feldoperator-Audit ersetzt zugleich einen freien radialen Kernel
durch die eingeschraenkte Antwortfamilie
`H(k)=(s0+s2 k^2)/(c0+c2 k^2+c4 k^4)`. Die positive `k^2/k^4`-Familie ist
die analytische Gauss-Null. Genau ein neuer Mechanismus darf als naechstes
dynamisch geoeffnet werden: `a2<0` in `P(u)=1+a2 u^2+u^4`, also ein
endliches-Wellenzahl-Minimum mit UV-Stabilisierung. Vor einem Lauf werden eine
feste dimensionslose Koeffizientenwahl, `v=0` als ausdrueckliche
Vorzeichensymmetrie sowie positive-`a2`-, cubic-off-, source-off- und eta-zero-
Kontrollen registriert. Primaere Observablen sind Feldpeak und Peakbreite,
Ast-/Gap-Persistenz, Source-Field-Closure und Shape-Bounds. Ein Pass waere
klassische Musterbildung, noch keine Quantisierung oder QFT-Evidenz.

Abgeschlossenes Gate: Die fuer lineare homogene Faltung exakte
Reparametrisierung wurde in drei Seeds und je 10,000 Updates bei identischem
Rauschen geprueft. Fuer
`rho'=q rho+beta G_x, phi=K*rho` und
`phi'=q phi+beta(K*G)_x` mit Dirac-Identitaetsreadout betragen die maximalen
Pfad-, relativen Feld- und Gradientenfehler `7.11e-15`, `2.25e-15` und
`1.43e-14`. Ein raeumlich konstantes `K=1` ist die getrennte kraftfreie Null.
Der Pass aendert nur die Zustandsbedeutung von Occupancy-Memory zu signiertem
Potentialmemory; er ist keine neue Physik.

Abgeschlossenes Gate: Das aktive skalare Delta-Quellfeld wurde ohne breiten
Depositkernel in drei Seeds gegen die registrierten Gaussian-null-,
stable-finite-k-, cubic-off-, source-off- und eta-zero-Arme gerechnet.
`dt=0.05` gegen `0.025` und `N_x=256` gegen `512` stimmen in den niedrigen
Moden bis `6.12e-7` bzw. `7.50e-11` relativ ueberein; der stationaere
Gleichungsrest ist `4.38e-5`. Der aktive Arm saettigt bei `k=1`, cubic-off
trifft den Amplitudenstopp und source-off bleibt exakt null. Damit besteht das
Gate fuer klassische Finite-Wellenzahl-Musterbildung.

Stopregel: `eta=0` bildet nahezu dasselbe Feld. Die Feldordnung ist daher
nicht feedback-spezifisch und noch kein multidimensionaler oder metastabiler
Knoten. Der explorative Wechsel des Source-Field-Phasenlags von etwa null auf
pi mit anschliessendem Pinning ist ein Folgehinweis, kein registrierter Pass.
Es folgt kein freier `a2/u/s`-Sweep und die Vektor-/Chiralitaetsenergie
wird nicht allein durch diesen Pass geoeffnet. Ein spaeterer Feldtest braucht
zuerst eine unabhaengige Source-/Target-Regel oder eine vorregistrierte
Observable, die Trajektorie-Feld-Rueckkopplung von der eta-zero-Musterbildung
trennt. Diese Stopregel bleibt bestehen; der anschliessende P2-Nullaudit ist
inzwischen abgeschlossen.

## P2: Scheinmoden analytisch einordnen

**Abgeschlossen, negatives Modengate.** Fuer rohe ungerichtete Fouriermoden
schliesst der `eta=0`-Prozess unter Gauss-Inkrementen exakt in einem reellen
Viererblock. Seine Eigenwerte sind der sichtbare Phasenmultiplikator
`exp(-epsilon^2 k^2/2)` und der Memory-Multiplikator
`(1-lambda)exp(-nu k^2)`, jeweils doppelt. Keine Sampling-Cadence kann daraus
durch Potenzieren eine komplexe Eigenmode erzeugen.

Der N=1M-Audit verwendet dieselben fuenf Seeds, `sample_every=20`, dieselben
Lags und dieselbe Diffusionsskala wie der archivierte Closure-Lauf:

- analytischer Rohoperator: keine komplexen Eigenwerte;
- gepoolte Rohfits: `0/15` komplex;
- vollstaendige seedweise Rohfits: `0/75` komplex;
- kurze Segmentfits: `27/375` kleine Leckpaare bei maximal
  `7.25e-4` Frequenz pro Memory-Zeit und hoher Konditionszahl;
- ausgerichtete aktive und `eta=0`-Subraeume ueberlappen weiterhin `>0.9999`
  und bestehen weder Kontrolltrennung noch Segmentidentitaet.

Damit greift die vorregistrierte Fail-Regel. Die vorhandenen komplexen
Nebenmoden werden als Darstellungs-/Fitmoden klassifiziert, nicht als
physikalische Oszillation, Photon-, Spin- oder Phasenmodus. Der Nullaudit
veraendert die geometrische Long-Run-Evidenz nicht.

Ein spaeterer positiver Modentest muss keine permanente globale Sinusmode
fordern. Fuer ueberwiegend chaotische gekoppelte Dynamik bleibt ModeScore v0.2
ereignisbasiert: vorab segmentierte Bursts, Duty-Cycle, Dauer/Survival,
Within-event Frequenz/Q und Phasenkontinuitaet sowie Kontroll-/Surrogatabstand.
Er wird erst auf einen neuen, kontrollgetrennten Mechanismus angewandt.

## P3: Interaktionsbefunde ueber unabhaengige Zustaende haerten

**Aktualisiert am 2026-08-04:** Der reziproke Zwei-Knoten-Zweig ist jetzt
analytisch vorregistriert. Fuer die synchrone lokale Skalarreduktion existiert
ein stabiles komplexes Cross-Gain-Fenster nur bei
`g < lambda/(1+lambda)`, mit `c > g` innerhalb des Fensters. Die kompakte
Baseline besitzt `g=0.4333` bei `lambda=0.01` und liegt damit weit ausserhalb
der Schwelle `0.009901`. `g+c>1` erzeugt einen negativen Determinanten und
somit reelle Eigenwerte mit entgegengesetztem Vorzeichen, nicht automatisch
Instabilitaet und keinen harmonischen Modus.

Prioritaetsfolge:

1. **P3.0 abgeschlossen:** Common-/Relative-Mode-Herleitung, exakter
   Vier-Zustands-Matrixabgleich und Regimekarte.
2. **P3.1 abgeschlossen, negatives Modengate:** Zwei Kopien des sauberen
   `d=3`, `N=100M`-Checkpoints laufen fuer fuenf gemeinsame
   Zukunftsrauschpfade je 500 Memory-Zeiten als Channel-off, One-way und
   synchron reziprok. Bei festem `c=0.02` sind alle 60 post-transienten
   Segmentfits reell; `0/5` Seeds bestehen in jedem Arm das komplexe
   Segment-/Phasengate. Kanal-aus ist bitgenau, Response und Shape-Huelle
   bestehen im reziproken Arm 5/5.
3. **Belastbare P3.1-Lesart:** Direkte synchrone skalare Reziprozitaet bindet
   bzw. relaxiert die Zentren in diesem Ast. Nach 500 Memory-Zeiten liegt der
   reziproke Abstand bei `0.31..0.88 R`, waehrend Channel-off auf
   `2.78..9.21 R` diffundiert. Das ist keine Oszillation, kein Orbit und noch
   keine basin-uebergreifende Aussage, weil alle fuenf Fortsetzungen aus
   einem Formationscheckpoint stammen.
4. **P3.2 abgeschlossen, negatives Modengate:** Der auf Einheits-DC-Gain
   normierte Telegraph-Filter verwendet unveraendert `lambda=0.01`, `c=0.02`,
   `L=5R`, Relaxation `10` Memory-Zeiten, Rasterweite `0.25R` und festen
   Readout bei `2.5R`. Kanal-aus, der bitidentische direkte P3.1-Arm und
   retardiert einseitig sind Common-Noise-Kontrollen.
5. **Belastbare P3.2-Lesart:** Mediator, Response und Shape-Huelle bestehen
   jeweils 5/5. Trotzdem sind alle 80 rohen Segmentfits reell und 0/5 Seeds
   bestehen in jedem Arm das komplexe Gate. Der retardiert reziproke
   Endabstand `0.58..1.21R` ist groesser als direkt `0.31..0.88R`:
   Verzoegerung schwaecht oder verschiebt die Bindung, erzeugt im registrierten
   `(x_-,m_-)`-AR(1)-Readout aber keine Rotation.
6. **Review-Hardening abgeschlossen:** Der isotrope Modenfit vermischte
   koordinatenspezifische Gleichlagen. Der korrigierte Fixed-Effects-Fit
   rekonstruiert ein synthetisches komplexes Gegenbeispiel bis `1e-12`.
   Saubere unveraenderte Nachlaeufe bleiben dennoch bei `0/60` (P3.1) und
   `0/80` (P3.2) nichtreellen Fits. Das staerkt den registrierten
   AR(1)-Messnullbefund, nicht einen Nullsatz fuer das augmentierte System.
7. **P3.2a abgeschlossen, sichtbare Closure statt augmentiertem Modenclaim:**
   Die gemeinsame Holdout-Leiter bei `0.5` Memory-Zeiten rekonstruiert einen
   synthetischen Hidden-Oszillator und trennt ambienten Rotationsfit. Der
   sichtbare `(x_-,m_-)`-Delayzustand besteht 9/9 Closure- und
   Identifizierbarkeitsgates (`kappa=46.8..81.0`) ohne ein einziges
   tiefenstabiles Segmentmatching.
8. **P3.2b abgeschlossen, kein Rausch-Unmasking:** Bei festen
   Einzelknoten-Marginalen senkt `rho={0,0.9,0.99}` den gemessenen relativen
   RMS-Schritt von etwa `0.579R` auf `0.183R` und `0.0579R`. Die reziproke
   Bindung wird staerker (mittlerer Endabstand `0.946R -> 0.299R -> 0.0946R`),
   die Closure-Kurven bleiben jedoch nahezu gleich und kein
   kontrollgetrennter Modus erscheint.
9. **P3.2-Langhorizont abgeschlossen, negativer Closure-Trend:** Bei
   identischen Train-/Testzielen verschlechtern sich alle 45 gepaarten
   Designzellen aus drei unabhaengigen Seeds, drei skalierten
   Rauschkorrelationen und fuenf verschachtelten Raengen von 1000 auf 12500 Updates; medianes
   `Delta RMSE/Persistenz=+0.1203`. Sichtbarer Stable-/Entropy-Rank waechst
   `1.67/6.62 -> 5.87/49.4` ohne Plateau. Feld/Impuls kehrt den Trend nicht
   um. Bei Rang 16/32 liegt reziprok minus Einweg terminal nur in
   `-0.00366..+0.00244`. Das stuetzt Informationsverduennung bei wachsender
   stochastischer Historie, keine laengere physikalische Persistenz.
10. **Pol-Identity-Stoptest abgeschlossen, negativ:** Seeds 1/2 tragen einen
    rang-/tiefenstabilen Kandidaten nahe `omega=0.103`, doch derselbe Pol trifft
    im Einwegarm noch `6..8/12` Zellen; Seed 3 erreicht reziprok nur `9/12`.
    Vier korrelationsuebergreifende Kandidaten, null kontrollgetrennte
    Ueberlebende. P3.2 ist geschlossen. Ein spaeter auf Nutzerwunsch
    ausgefuehrter 500k-Akkumulationskontrolllauf aendert diese Entscheidung
    nicht: Die grossen Pfaddifferenzen treten im Einwegarm nahezu gleich auf.
11. **P3.2c abgeschlossen, source-lokaler Modus null:** Die exakte
    finite-grid Telegraphregel ist mit emitterlokalem `d=x-m` stabil und
    besitzt einen Pol bei `omega=0.08294` pro Memory-Time. Sein normiertes
    Knot-Residuum ist aber nur `3.54e-5`, der Generatorabstand zum naechsten
    Einwegpol nur `0.00622`; der lokale Schrittstrom koppelt nochmals etwa
    hundertfach schwaecher. Alle drei strukturerhaltenden Modenreduktionen
    stimmen zu. Kein 500k-Lauf und keine Gain-Suche dieses Mechanismus.
12. **P3.2d abgeschlossen, Shape-Multipol null:** Die alten Traces enthielten
    keinen vollstaendigen zeitabhaengigen Shape-Tensor; deshalb wurde eine
    minimale autonome Reproduktion vom reifen Checkpoint vorregistriert. Alle
    fuenf Baseline-Pfade bleiben shape-begrenzt. `Q` zeigt starke Leistung nahe
    dem unteren Bandrand, aber keine Segmentidentitaet (`0/5` Kandidaten); im
    `eta=0`-Arm ist derselbe Niederfrequenzcharakter staerker (`2/5`).
    `Delta Q/Delta tau` liefert `0/5` Baseline-Kandidaten. Keine
    Tensor-Mediatorregel wird autorisiert.
13. **Vektormemory formal gehaertet; passives Source-Gate negativ:** Der
    Zustand z=(x,rho,p,m), seine vollstaendige finite-memory Darstellung,
    Symmetrien, Nullgrenzen, Tailfehler und Produkt-Identifizierbarkeit sind
    dokumentiert und getestet. Polarisation trennt sich in 6/6 Seeds von der
    Random-Sign-Null (Faktor 3.42..4.49), behaelt aber keine robuste Achse;
    das Gesamtgate besteht 0/6. Der Zirkulations-Bivektor liegt in 6/6 Seeds
    unter der q99-Null (Faktor 0.54..0.76) und besteht ebenfalls 0/6.
    Kein Lambda-/Kappa-Sweep dieses passiven Zustands. Die O(d)-kovariante
    Analyse ist abgeschlossen: parity-even Ein-Feld-Gradientenfluss hat ein
    reelles Spektrum; eine endliche Raumskala entsteht nur fuer
    b_hat_L oder b_hat_T < -2. Das passive Mikro-Update besitzt exakt nur den
    homogenen Faktor 1-lambda_v und keine solchen Gradientenkoeffizienten.
    Die source-konditionierte L/T-Fourier-Closure bestaetigt diese exakte Null
    in 6/6 Seeds: q- und Raumkoeffizientenfehler bleiben unter 6.6e-15 bzw.
    1.9e-15. Laengere passive Runs koennen daher keine aktiven
    Feldkoeffizienten selektieren. Als naechstes ist hoechstens eine
    source-unaufgeloeste Grobkoernung ueber mehrere Blockskalen zulaessig;
    deren Koeffizienten gelten nur bei Seed-, Skalen- und Holdout-Stabilitaet
    als emergent-effektiv. Andernfalls muss ein aktives Feldgesetz als neues
    Postulat deklariert werden. Ladung und Flavor bleiben undefiniert; kein
    Photon- oder Spinclaim.
14. **500k-Akkumulationskontrolle abgeschlossen, negativ:** Zwei
    Zukunftsrauschpfade ueber 5000 Memory-Zeiten bleiben im reziproken Arm
    shape-gueltig. Die kontrollsubtrahierte Pfaddifferenz waechst stark, aber
    nahezu identisch im Einwegarm (`19.14R` vs. `19.03R` und `10.51R` vs.
    `10.31R`). Das ist sensitive Pfaddivergenz nach persistenter Stoerung,
    keine kontrollgetrennte reziproke Akkumulation.
15. **Kein Lambda-Sweep im bestehenden Checkpoint:** Die Gewichte im
    `FiniteMemoryState` kodieren Lambda bereits. Bei aktuellem `g=0.4323` und
    `c=0.02` kann zudem kein Lambda den direkten Modus komplex machen, da
    `c>g` notwendig ist. Eine spaetere Lambda-Kampagne braucht neue kompatible
    Formationszustaende, festen Tailfehler und vorab definierte Invarianten.
16. **P3.3 gesperrt bis Mode-Pass:** ambient-dimensionsuebergreifender Rangtest.
    Eine komplexe Rotation waere noch keine raeumliche `d=3`-Selektion.
17. **P3.4 Adjungierte Reziprozitaet: Eligibility-Pass, Metrik offen:** Fuer die
    diskrete Closure `x'=x-sqrt(g) B^dagger h`, `h'=q h+sqrt(g) B x'`
    ist ein Singulaermodus
    exakt komplex, wenn
    `(1-sqrt(q))^2 < g sigma_B^2 < (1+sqrt(q))^2`. Die bereits implementierte
    normierte Richtungsdeposition besitzt lokal
    `B=kappa(I-u u^T)/|Delta x|`: eine longitudinale Nullrichtung und `d-1`
    entartete transversale Richtungen. In den sechs reifen `d=3`-Snapshots
    variiert die mediane Schrittweite nur um Faktor `1.045`; unter euklidischem
    Metrik-Kandidaten und der geerbten festen Kopplung liegen mindestens
    `99.83%` der Schritte im komplexen Fenster. Das ist nur kinematische
    Eligibility. Der adjungierte Rueckkanal ist neu, die Kopplung stammt aus
    einem anderen Einweg-Gate, und eine Reskalierung des Memory-Metriks
    verschiebt denselben Modus aus dem Fenster. Weder Oszillation noch
    Traegheit wurden simuliert oder beobachtet.

    **Drei-Metrik-Gate abgeschlossen, negativ (0/6):** Der korrigierte,
    vor Ergebnisannahme festgelegte Segmenttest trennt numerische Messbarkeit
    von physikalischer Closure. Finite-Differenz-Linearitaet (maximal
    `2.18e-9`) sowie Predictive-Cadence-Skala (`0.0261..0.0748`) und -Form
    (`2.16e-6..5.68e-6`) bestehen in allen Paaren. Am finalen Horizont ist
    die Kovarianzmetrik in 12/12 Segmenten instabil, die Vorhersagemetrik in
    11/12 ueberdaempft und einmal gemischt, die isotrope RKHS-Metrik in 12/12
    komplex. Die Klassifikationen stimmen in keinem Paar ueberein; mehrere
    Kovarianzskalen und Segmentformen sind noch horizontabhaengig. Der
    Supportueberlapp von praktisch eins ist wegen des konstruktiven
    transversalen Rangs nicht eigenstaendige Evidenz. Damit ist der
    euklidische Eligibility-Pass normalisierungsabhaengig. Kein nichtlinearer
    reziproker Pilot und kein Gain-/Lambda-Retuning.

18. **P3.5 abgeschlossen, negativ: balancierte Vollmemory-Feature-Closure.** Auf den
    sechs bestehenden reifen Zustaenden wird ohne neuen Formation-Long-Run
    matrixfrei geprueft, ob das deponierte orientierte Feld einen kleinen
    Unterraum besitzt, der zugleich durch die Trajektorie angeregt
    (Controllability) und im fixierten unabhaengigen Probe-Readout beobachtet
    wird (Observability). Primaer sind Hankel-Singulaerwerte, ein vorab
    festgelegtes Spektralgap, Principal-Angle-Stabilitaet ueber Seeds,
    Segmente, Horizonte und Cadences sowie echte Holdout-Vorhersage. Ein Pass
    autorisiert nur einen reduzierten Carrier-plus-Feld-Zustand und dessen
    Metriktest. Ohne stabilen Unterraum wird der adjungiert-reziproke
    Vektorast geschlossen; ein quadratisches Feldgesetz bleibt dann eine
    explizite konstitutive Annahme.

    **Vorregistriert und ausgefuehrt am 2026-08-10:** Der Test verwendet die sechs reifen
    `d=3`-Zustaende, zwei Segmente, Horizonte 5/10 Memory-Zeiten und Cadences
    1/5/10. Feste Gates sind Rang hoechstens 8, Hankel-Gap mindestens 3,
    Energieanteil mindestens 90%, Principal-Cosinus mindestens 0.90 und
    Far-Probe-Holdoutfehler hoechstens 15%. Flat-Readout und altersvertauschte
    Raumfaktoren trennen generische Delay-Kompression von knotenspezifischer
    Raum-Alters-Struktur. Ein Pass autorisiert nur einen reduzierten
    Carrier-plus-Feld-Metriktest; eine Parametersuche nach maximaler
    Schwingung bleibt bis zu dessen unabhaengiger Zeitbereichsvalidierung
    gesperrt. Das Ergebnis ist `0/6`: Zwar waehlen alle 72
    Actual-Geometry-Auswertungen stabil Rang 1 bei etwa `96.6..97.8%`
    Energieanteil und internem Principal-Cosinus ueber `0.999`, aber derselbe
    Modus stimmt mit Flat- und Age-Shuffle-Kontrolle zu ueber `0.9999`
    ueberein. Der unabhaengige Fernreadoutfehler liegt bei `0.501..0.862`.
    Damit wurde ein generischer exponentieller Delay-/Readoutmodus gefunden,
    keine knotenspezifische raeumlich uebertragbare Mode.

19. **P3.6 abgeschlossen, struktureller Pass: reversibler Feldmechanismus statt
    Parametersuche.** Das passive orientierte Memory besitzt weder einen
    identifizierten Rueckkanal noch eine geometriespezifische reduzierte Mode.
    Weitere Long Runs oder Gain-/Lambda-Sweeps koennen diese fehlende Struktur
    nicht erzeugen. Falls der Paper-III-Ast fortgesetzt wird, ist zuerst eine
    minimale O(d)-kovariante, phasentragende Dynamik mit explizit reversiblem
    beziehungsweise antisymmetrischem Anteil zu formulieren. Vor jeder
    Simulation sind Dispersionsrelation, Stabilitaetsfenster, dimensionslose
    Gruppen, passive Nullkontrolle und ein unabhaengiger Zeitbereichs-Holdout
    festzulegen. Die neue Gleichung waere ein Postulat, bis ihre Koeffizienten
    aus einer tieferen Dynamik oder Daten identifiziert sind.

    **Ergebnis vom 2026-08-11:** Der fruehere reaktive `2 x 2`-Platzhalter ist
    nun mit der raeumlichen Vektorfeldenergie ueber ein konjugiertes
    Impulsfeld verbunden. Fuer jeden L/T-Modus gilt exakt
    `I s^2 + gamma s + D_q(k) = 0`. Alle sechs registrierten Identitaeten
    bestehen; der groesste Kovarianzfehler ist `1.18e-13`. Stabile gedaempfte
    Schwingung erfordert `D_q(k)>0`, `gamma>0` und
    `4 I D_q(k)>gamma^2`. Die Negativkontrolle bestaetigt, dass negative
    Kruemmung trotz positiver Daempfung einen positiven Eigenwert behaelt.
    Der Pass ist konstruktiv-strukturell: Er zeigt mathematische
    Moeglichkeit, keine emergente oder beobachtete Knotenschwingung. Der
    Operator bleibt O(d)-kovariant und selektiert kein `d=3`.

20. **P3.7 als naechstes: Identifizierbarkeits-/No-go-Gate vor jeder
    Parameterermittlung.** Der P3.6-Oszillator erweitert den Zustand um ein
    unabhaengiges konjugiertes Feld; er ist nicht aus `z=(x,rho)` abgeleitet
    und nicht in den Knotensimulator eingebaut. Deshalb wird zuerst eine feste
    Projektion `Y=Psi(x,rho)` ausschliesslich aus kanonischen Variablen
    vorregistriert. Eine zweite Ordnung darf nur weiterverfolgt werden, wenn
    sie auf Holdout-Daten eine erste-Ordnung-Kontrolle uebertrifft, ihre Pole
    ueber Seeds, Segmente, Cadences und Grobkoernung identisch bleiben und eine
    unabhaengige Response vorhersagen. Die bisherigen passiven Closure-Befunde
    liefern noch keinen solchen konjugierten Zustand. Ein Fit auf maximale
    Schwingung, ein Gain-Sweep und ein gekoppelter Feldpilot bleiben gesperrt.
    Selbst bei einem Pass identifiziert ein komplexes Polpaar zunaechst nur
    `gamma/I=2 Gamma` und `D/I=Gamma^2+omega^2`; die absolute Skala benoetigt
    eine unabhaengig normierte Response oder Energie.

    **P3.7a jetzt: Same-law-Jacobian-Audit des kanonischen Zwei-Knoten-Astes.**
    Fuer gespeicherte reife Zustaende werden ohne Trajektorienfit die
    dimensionslosen Matrizen `G=eta Hess(Phi_self)` und
    `C(R)=eta_cross Hess(Phi_cross)` bestimmt. `Y_-=(x_-,xbar_rho_-)` ist die
    feste kanonische Projektion und `A_-(G,C,lambda)` ihr abgeleiteter
    `2d x 2d`-Operator, kein neuer Parameter. Primaer ist die gemeinsame
    Self-/Cross-Regel `eta_cross=eta` ueber vorab festgelegte Distanzen und
    Eigenrichtungen. Falls `C<=G` und kein stabil komplexer Vollmatrixmodus
    auftritt, ist ein gemeinsames Gain-Retuning als Loesung ausgeschlossen.
    Erst ein unabhaengig vorhergesagter komplexer Bereich autorisiert einen
    `N=500k`-Low-g-Pilot mit mindestens fuenf Formationsseeds.

    **P3.7a Jacobian-Ergebnis: lokale Common-Scale-Eligibility, Pilot noch
    gesperrt.** Beim Checkpoint-Gain `eta=0.15` bleiben alle Moden reell. Eine
    gemeinsame Skalierung von Self und Cross ergibt jedoch bei
    `R=sigma_rep` ein ueber `d=3`, `d=10` und alle 13 Richtungsfaelle
    geschnittenes Intervall `eta=0.0009965..0.0026549`; der feste geometrische
    Mittelpunkt `eta=0.0016266` besteht im Vollmatrixoperator 13/13. Die
    Intervalle bei `2.5 R_mem` und `10 R_mem` sind wegen `c/g-1` von nur
    `1e-7..1e-6` numerisch fragil. Das Ergebnis reduziert `g,c` auf einen
    gemeinsamen Gain, zeigt aber weder Gain-Selbstauswahl noch eine
    nichtlineare Schwingung.

    **P3.7b jetzt: affines Kraftbilanz-Gate.** Die lokale Dynamik lautet
    allgemein `delta Y_next=A_- delta Y+b_*+noise`. Vor einem Pilot muss daher
    fuer dieselbe Geometrie der affine Relativdrift `b_*` verschwinden. Ein
    stabil-komplexer Jacobian an einem Punkt mit endlicher Anziehung ist kein
    Normalmodus. Erst wenn Jacobian- und Kraftbilanz-Gate gleichzeitig
    bestehen, ist der `N=500k`-Pilot freigegeben.

    **P3.7b abgeschlossen, negativ:** Kein zuvor komplex-eligibler Abstand
    besteht die Kraftbilanz (`0/13` je Abstand). Bereits bei `2.5 R_mem`
    betraegt die eingefrorene Relativdrift pro Memory-Zeit etwa `1.25 R_mem`,
    bei `R=sigma_rep` `1300..2355 R_mem`. Im kompakten Punktgrenzfall ist dies
    strukturell: Selbstkonfinierung verlangt
    `A_att/L_att^2>A_rep/L_rep^2`, ein positiver Kraftnullpunkt desselben
    Zweigauss-Kernels die umgekehrte Ungleichung. Ein gemeinsames Eta-,
    Lambda- oder Amplituden-Retuning kann diesen Konflikt nicht loesen. Der
    angekuendigte `N=500k`-Pilot ist gesperrt.

21. **P3.8 jetzt als Mechanismusentscheidung: gemeinsame Source-/Readout-
    Energie mit expliziter Kraftbilanz.** Genau eine
    Kopplungsenergie `H_int[x,m] = - integral J[x] dot m dx` muss dann sowohl
    Feldquelle als auch reziproke Trajektorienkraft liefern. Getrennt
    eingestellte Deposit-/Readout-Gains sind nicht zulaessig. Diskrete
    Energiebilanz, Source-off-, Reversible-off- und First-order-Kontrollen
    werden vor einem einzigen modellkonditionalen Pilot vorregistriert. Der
    neue Mechanismus muss zusaetzlich entweder Self- und Cross-Geometrie
    begruendet trennen oder eine signierte/orientierte interne Source liefern;
    andernfalls reproduziert er das P3.7b-No-go. Zuerst werden Gleichungen,
    Symmetrien, affine Gleichgewichte und identifizierbare dimensionslose
    Gruppen abgeleitet. Noch kein Simulations- oder Parametersweep.

    **P3.8a analytischer Kandidat, strukturell bestanden:** Statt
    eines frei orientierten Knotenchannels wird das skalare Memory um einen
    lokal bilanzierten Strom `j` erweitert. Fuer den longitudinalen Modus gilt
    `(s+lambda_m)(s+gamma_j)+c_j^2 k^2=0`; komplexe Pole entstehen genau bei
    `2 c_j k > |lambda_m-gamma_j|`. Die vorhandene Memory-Innovation hat bei
    stationaerer Masse exakt Monopol null, ihr Dipol ist
    `lambda_m M0 (x-xbar_rho)`, und Blockinnovationen teleskopieren. Damit ist
    die Source aus dem kanonischen Update abgeleitet und nicht als Ladungslabel
    gesetzt. Der Strom sowie `gamma_j,c_j` bleiben jedoch neue Modellinhalte.
    Das Gate loest weder die negative affine Kraftbilanz noch einen
    transversalen Spinmodus und selektiert kein `d=3`. Der bestehende skalare
    Datensatz waehlt diesen Kandidaten nicht aus.

    **P3.8b nach Review: separater Gradientenmediator, analytisch bestanden.**
    Der `k^2`-Zaehler folgt nicht aus dem P3.8a-Dichte-Strom-Memory. Er verlangt
    einen eigenstaendigen longitudinalen Zustand `(m,p)` und die gemeinsame
    Energie `H_int=-g integral m dot grad(q) dx`; `q` ist die skalare Quelle,
    `m` weder `rho` noch `j`. Fuer den lokalen
    konstitutiven Operator `D(k)=a+b k^2+c k^4` und einen gemeinsamen
    gradientenfoermigen Write/Readout folgt
    `K_eff(k,w)=g^2 k^2 / [(-iw+lambda_m)(-iw+gamma_p)+k^2 D(k)]`.
    Damit ist `K_eff(0,w)=0` exakt und die Quelle-/Readoutamplitude tritt nur
    als `g^2` auf. Nach Naturalskalierung bleiben
    `delta=b/sqrt(a c)`, `mu=lambda_m gamma_p sqrt(c)/a^(3/2)` und das
    vertauschungsinvariante `r_gamma=max(lambda_m,gamma_p)/min(...)>=1`. Die
    Antwort waehlt ihre Wellenzahl ueber
    `2 y_*^3+delta y_*^2-mu=0`, `y_*=u_*^2`, ohne Zielwellenzahl oder
    Amplitudensweep. Ein fester, nicht gefitteter Existenzpunkt
    `(delta,mu,r_gamma)=(-1.9,0.3,1)` besitzt positive konstitutive Energie,
    einen stabilen komplexen selektierten Modus und wechselnde
    Realraumschalen. Die exakte Residueninversion ist gegen unendliche
    Fourierquadratur verifiziert; das erste getrennte lineare Paarminimum liegt
    bei `r/ell=6.99092` hinter einer Barriere bei `3.91920`. Dies ist ein
    linearer Punktquellenbefund, keine Knotensimulation und keine
    Parameterherleitung.

    **P3.8c quasistatische Diskrimination abgeschlossen, konditionaler Pass.**
    Zwei starre vollstaendige `d=3`, Seed-1, `N=100M`-Memory-Wolken wurden ohne
    Dynamik, Gain-Fit oder Sweep getestet. Bei `R=5 ell` sagen statischer
    kompensierter Arm und Gradientenmediator robuste entgegengesetzte
    Kraftvorzeichen voraus. Die Vollmemory-Wolke reproduziert Barriere und
    stabiles Minimum des Gradientenarms mit quadratischer Punktgrenz-
    konvergenz. Wegen `R_mem/ell=2.12e-4`, einem Seed und gesetztem
    `ell=sigma_rep=1` ist dies Mechanismus-Diskriminierbarkeit, keine Auswahl
    und kein dynamisch stabiler Knoten.
    Die primaere Paarenergie ist eine neue reziproke Memory-Memory-
    Cross-Geometrie; eine separat energiesymmetrisierte kanonische
    Sichtpunkt-Memory-Kontrolle behaelt nur wegen der kompakten Punktgrenze
    dieselben Vorzeichen. Diese Architekturwahl bleibt im dynamischen Gate
    explizit offen.

22. **P3.8d abgeschlossen: konditionaler dynamischer Existenzpass.** Eine
    zeitdiskrete `(m,p,R)`-Fortschreibung aus einer gemeinsamen Energie
    besteht Source-work-, Daempfungs-, Cross-off- und Zeitschrittgates. Der
    erster-Ordnung-Arm besitzt dieselbe statische Suszeptibilitaet, aber keinen
    reversiblen Overshoot. Beide Zeitordnungen erreichen bei `R0=5,8` dasselbe
    getrennte Basin nahe `6.99 ell`; die reversible Separationskurve ist nur
    schwach verschieden. Fruehe Krafttransienten sind UV-Cutoff- und
    Initialisierungs-sensitiv; bei statisch aequilibriertem Feld verschwindet
    das Ringing.
    Der Mediator, seine Koeffizienten und `nu=1` sind gesetzt; der Test ist
    punktfoermig, kollinear und entwickelt weder Knotenform noch `rho`.

23. **P3.8e technisch reconciliert: Null nicht verworfen.** Das historische
    Ergebnis ist `superseded-methodologically-inconclusive`: freie und
    "gedaempfte" AR(2) waren fuer die berichteten stabilen komplexen Pole
    dieselbe Parametrisierung, und die alte Panel-Hankel-Matrix konnte durch
    unterschiedliche Residuen kuenstlich Rang erzeugen. Der korrigierte Lauf
    aus Revision `e4f56b8` trennt active und `eta=0`, lernt Pole nur aus den
    Memory-Readouts, haelt die sichtbare Relativkoordinate zurueck, verwendet
    gemeinsame Zielzeiten und baut die Hankel-Spalten nur aus Zeitshifts.

    Alle Interventionskontrollen bestehen weiterhin: Uniformfehler
    `2.95e-13`, vollstaendige spaete `eta=0`-Extinktion, diagonale und volle
    Cross-`k`-Linearitaet `0.001/0.001`, maximale Radiusstoerung `0.006`.
    Trotzdem besteht kein Kanal das korrigierte zweite-Ordnungs-Gate. Alle
    gepoolten aktiven AR(2)-Pole sind reell; AR(2) verbessert weder Memory-
    noch sichtbares Holdout, und die echte ungedaempfte Nebenhypothese ist
    deutlich schlechter. Die korrigierten Hankel-Spektren haben zwar
    `0.875..0.988` Energie in den ersten zwei Singulaerwerten, aber
    `s3/s2=0.557..0.695` und damit keine isolierte Rang-2-Struktur.

    Die Negativaussage bleibt begrenzt: Das Memory-Holdout enthaelt nur
    `0.2%..0.8%` der skalenbalancierten Energie. Zudem sind die fuenf
    Eingangsprofile stark kollinear (medianer Gram-Konditionswert `15867`,
    maximale Off-Diagonale `0.9964`). Der Altersvergleich besteht nur relativ
    zur bereits grossen Seed-Streuung. Der belastbare Status lautet daher
    `null-not-rejected-memory-holdout-limited`, nicht skalares No-go.

    Die Intervention ist eine gueltige massen- und zentrumserhaltende
    Stoerung des vollstaendigen Memory-Zustands. Sie wurde jedoch nicht durch
    den kanonischen Trajektorie-zu-Deposition-Port geschrieben. P3.8e misst
    damit primaer Read-/Zustandssuszeptibilitaet und schliesst weder einen
    universellen skalaren No-go-Satz noch ein adjungiertes Write-/Read-Paar.
    P3.8d bleibt eine konstruierte Erweiterung; seine Parameter werden nicht
    auf dieses negative Ergebnis hin nachjustiert.

24. **P3.8f als letzter skalarer Closure-Test: kanonischer Write-Port.** Vor
    einer orientierten oder gemeinsamen Felderweiterung wird genau ein
    weiterer diskriminierender Test zugelassen:

    1. ein gepaarter schwacher sichtbarer `+delta/-delta`-Dipolpuls mit
       verschwindender direkter Nettotranslation schreibt ausschliesslich
       ueber die vorhandene Trajektorie-zu-`rho`-Deposition;
    2. dieselben festen `kR_mem`-Readouts und ein unabhaengiger sichtbarer
       Kraft-/Relativkoordinaten-Readout werden ohne Zielpol verwendet;
    3. `eta=0`, zwei Staerken, fuenf Seeds und common random numbers bleiben
       Pflicht. Es gibt pro Achse genau einen bekannten Trajektorieninput;
       Memory-Zentrum und `kR_mem`-Moden sind Outputs, keine frei waehlbaren
       Eingangsprofile;
    4. nur nach einem informativen Write-/Read-Gate werden erste, zweite und
       achte Ordnung auf vorab fixierten blockierten Signalfenstern verglichen.
       Keine Kernel-, Gain-, Noise- oder P3.8d-Parametersuche.

    **Ergebnis P3.8f-a:** Der benachbarte `(+delta,-delta)`-Puls besteht alle
    G0-Kontrollen in 5/5 reifen N=3M-Zustaenden. Nach Entfernung der globalen
    Translationsnullmode bleibt das Memory-Signal in 3/3 Holdouts messbar, die
    relative Positions-/Selbstkraftantwort aber nur fuer etwa
    `0.12 tau_mem` oberhalb von `1e-3` ihres Peak-RMS; ihre
    Holdout-Verhaeltnisse liegen bei rund `8e-8`. G1 ist
    daher `0/5 inconclusive`, G2 und G3 sind `blocked`. Die fruehere
    Auswertung mit absoluter Position war durch eine bleibende Translation
    kontaminiert und wurde vor Ergebnis-Commit korrigiert.

    **Naechster diskriminierender Schritt:** kein G2-Fit und kein Parameter-
    Sweep. Zulaessig ist genau eine vorregistrierte Port-Reparatur, bei der
    der ebenfalls zero-net Rueckkick nach einer bereits intrinsisch gegebenen
    Memory-Zeit erfolgt. Der bisherige Nachbarpuls bleibt Negativkontrolle.
    Besteht auch dieser dimensionslose Write-Test G1 nicht, wird die kanonische
    skalare Route zu `(m,p)` geschlossen. Ein orientiertes/current Memory oder
    ein gemeinsames Mehrquellenfeld ist dann offen als neue Modellannahme zu
    deklarieren.

    **Ausfuehrungsreihenfolge aktualisiert:** Das fruehere Composite-Gate ist
    jetzt in `G0` experimentelle Gueltigkeit, `G1` Identifizierbarkeit, `G2`
    zweiter Zustand und `G3` komplexe Phase getrennt. `G1`-Mangel ergibt
    `inconclusive`; nachgelagerte Gates sind dann `blocked`. Die vorhandenen
    alten direkten P3.8e-Profile besitzen robusten gemeinsamen Rang 4. Dieser
    Rang gehoert nicht zum kanonischen P3.8f-Eingang und wird dort nicht
    invertiert. G2 verlangt keine komplexen Pole. Erst G3 tut dies.

    P3.8f ist lokal seedweise shardbar implementiert. Das kuratierte
    versionierte Fuenf-State-Bundle, hashgepruefte NPZ/JSON-Shards und ein
    Aggregate-Manifest liegen vor; ein GitHub-Worker ist fuer den kurzen Lauf
    weiterhin nicht erforderlich. Die wissenschaftlichen Gates bleiben
    sequentiell; nur Seed-Simulationen duerfen parallel laufen. Protokoll:
    `reports/project/meta/preregistration/p38f_split_gate_execution_protocol_2026-08-14.md`.

25. **Claim-getrennter S1-/Masse-Falsifikationsast; Center bis A, S1 nur
    Methodenkontrollen.** Ein
    moeglicher Parametersatz fuer knoteninterne Oszillation und externe
    Wechselwirkung wird nicht in P3.8f hineingedeutet. Vor jedem neuen
    S1-Ziellauf muss `P0-S` das vollstaendige Parametertupel, Architekturlevel,
    Code-/State-Hashes, alle betrachteten Discovery-Daten und eine Regel fuer
    neue konfirmatorische Seeds einfrieren. Im Repository liegt derzeit kein
    eindeutiger neuer S1-Satz vor.

    Der Topologieast definiert zuerst das behauptete Objekt: deterministischer
    Orbit, stochastischer Dichte-Ridge, Delay-Rekonstruktion oder kollektiver
    Zwei-Knoten-Orbit. Eine Winkeltransformation, Hilbert-Phase oder
    candidate-getunter Delay ist vor einem persistenten `H1`-Pass verboten.
    Danach folgen out-of-sample Kreiskoordinate, autonome force-off-Dynamik und
    erst zuletzt externe Phasenkopplung. Ein periodischer externer Drive darf
    sein eigenes `S1` nicht als knoteninterne Topologie einschleusen.

    Parallel dazu bleiben die Referee-Gates A--F logisch getrennt: physischer
    Port, unabhaengige `tau/mu/M0`-Skalierung, Zwei-Knoten-Komposition und
    Gesamtimpuls, ungesehene Kraftprofile sowie Symmetrie-/Open-System-Audit.
    Ein `S1`-Pass erzeugt keine Masse; ein Masse-Fail widerlegt keine robuste
    interne Phase. Charter:
    `reports/project/decisions/s1_phase_mass_falsification_program_2026-08-16.md`.

    Der zweite Referee-Pass korrigiert den diskreten Periodenorbit-/`S1`-
    Fehlschluss, den Raw-cloud-Shuffle-Nulltest, Pseudoreplikation und die
    offene Impulsbilanz. Gestartet ist nur ein dependency-gepinnter
    synthetischer Method-Training-Split. Sein endlicher 12-Zyklus traegt trotz
    nichtkreisfoermiger Invariantmengentopologie eine lange `H1`-Klasse und
    demonstriert damit die notwendige Trennung von Geometrie und Dynamik. Der
    Validation-Split bleibt ungeoeffnet; P0-S blockiert weiterhin S1-Zielruns.

    Der inzwischen ausgefuehrte repositoryweite S1-P0-Audit bestaetigt diese
    Blockade formal: kein eindeutiger neuer S1-Kandidaten-/Discovery-Datensatz,
    27 akkumulierte Manifestdefekte und `target_data_opened=false`. Ein
    getesteter Validator prueft Vollparameter, State-/Artefakthashes,
    Discovery-Selektion und Confirmatory-Seals. D0/D1 wurden folgerichtig
    nicht geoeffnet; dies ist kein negatives Topologieergebnis.

    Der danach getrennt untersuchte native d=2-Rotating-wave-Kandidat ist
    inzwischen deutlich staerker als eine visuelle Kreisbahn: Der Anchor und
    vier gematchte finite-H-Zellen besitzen lokale Krawczyk-Rootzertifikate.
    Eine prospektive Fixed-gain-Reconciliation zeigt First-order-Annaeherung
    an den nativen Kontinuumsroot bei exakt eta/alpha=15. Dieser Erfolg
    repariert den frueheren Kontinuums-Targetfehler, aber nicht P0-S: D0
    identifiziert die Bahn als ambiente SO(2)-Gruppenbahn, die nach Quotient
    zum Punkt kollabiert. Sie ist daher kein neuer knoteninterner S1-Kandidat
    und oeffnet weder Topologie- noch Massegates.

    Der davon getrennte K0-Memory-Center besteht P0-M mit null Defekten. Alle
    frueheren Centerdaten und Seeds 1--20 sind Discovery, neue Seeds 21--25
    und eine Transferzelle bleiben versiegelt; der Pass oeffnet nur A und
    versiegelt D0--D5 explizit. Gate A identifiziert den implementierten
    Inputempfaenger als `x`, aber nicht den physischen Port: ein x-konjugierter
    Port hat den Rest `f dr`, waehrend ein effektives `U_ext(c,Q)` zur selben
    additiven x-Gleichung transformiert. Ohne reziproken mikroskopischen
    Aktuator und finite-H-Grenzledger bleibt der mathematische passive
    Center-Port gueltig, waehrend Center-Arbeit und die nachgelagerten
    Massegates B/C/E/F1 gestoppt sind.

    Der prospektiv eingefrorene A2-Folgetest schliesst inzwischen die engere
    finite-H-Frage fuer einen **neu deklarierten effektiven Wrapper**: alle
    fuenf Tail-Zellen bestehen eine globale Small-Gain-/Positive-Real-Schranke
    mit mindestens 89-facher registrierter Sicherheitsmarge; der dichte
    Frequenzgrid bleibt nichtentscheidend. Das repariert weder die fehlende
    mikroskopische Portauswahl noch macht es den History-Centroid materiell.
    Daher ist ausschliesslich ein B-star-Systemidentifikationstest von
    `m_filter=tau/mu` geoeffnet; physisches B/C/E/F1 und S1-D0--D5 bleiben
    versiegelt.

    Dieser B-star-Ast ist nun prospektiv ausgefuehrt und besteht. Beide
    Estimanden liefern tau-Exponent 1, mu-Exponent -1 und M0-Exponent 0; die
    gemeinsame Holdout-Ecke ergibt 3.99997 gegen die Vorhersage 4. Zugleich
    aendert M0 die diskrete Daempfung deutlich, die Intervention ist also
    nicht wirkungslos. Die fast perfekte lokale Ableitung bestaetigt die
    implementierte Filterarchitektur, nicht materielle Masse. Weitere
    B-star-Zellen koennen den fehlenden mikroskopischen Port nicht
    identifizieren; dafuer waere eine neue Aktuatorarchitektur mit frischem
    P0/A-Vertrag erforderlich.

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

- ungeregistrierte oder frei retunete reziproke Mehrknotenkopplung;
- weitere reine Skalar-Amplituden- oder Epsilon-Sweeps;
- dynamische LoG-Vergleichslaeufe, solange der beobachtete Ast nur
  `R_mem/L << 1` und damit dieselbe lineare Kruemmung abtastet;
- eindeutige externe `d=3`-Selektion;
- harte endliche Signalgeschwindigkeit aus direkter Fernkopplung;
- Lorentz-, Quanten- und Standardmodellableitungen;
- physikalische Massen- oder Ladungsidentifikation.

## Abgeschlossene Evidenzbloecke

1. **Kernel und Skalarast:** Signkorrektur, matched Ablation, lineare
   Reconciliation, feste-`g`-Skalenpruefung und analytischer LoG-/Taylor-Audit
   als zero-mean Nullfamilie ohne Amplitudenselektion; lokaler
   Feldoperator-Audit mit Gaussian-`k^4`-Match und Finite-k-Stabilitaetsgrenze.
2. **Dimension:** Ambient-Sweeps, D_spec-Sensitivitaet und Rohsnapshot-Retest;
   kein robuster externer 3D-Claim.
3. **Memory-Feld:** spektrale Reprasentation, Relaxations-Diffusion,
   Realraum-/Aufloesungskontrollen, negativer Mode-Identity-Audit und exakte
   `eta=0`-Rohmoden-Nullreferenz bei archivierter N=1M-Kadenz.
4. **Externe Antwort:** Weak Probe, Frozen Source, signierter Architekturtest
   sowie One-Way-Source- und Interaction-Age-Gates.
5. **Repository-Hardening:** Paketkern, Checkpoints, Tests, CI und kuratierte
   Doku-Frontdoor.

Die zugehoerigen Entscheidungstragenden Reports sind in `reports/README.md`
indexiert; die vollstaendige Chronologie bleibt im Doku-Archiv und in Git.
