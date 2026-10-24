# R0: Machbarkeit der physikalischen Verbindungen

Stand: 2026-10-21. Interner, begrenzter Annahmenaudit gegen Repository-Stand
`5090860`; kein unabhaengiges Fachgutachten und keine neue Zielsimulation.
Arbeitsfolge: [Projektprioritaeten](../status/project_priorities.md).
Gesamtziel: [Forschungsroadmap](../status/research_roadmap.md).
Modellbasis: [Paper-I-Gleichungen](https://github.com/MemoryDynamics/Knoten/blob/5090860/paper/paper_i/manuscript/content.tex),
[lineare Referenz](https://github.com/MemoryDynamics/Knoten/blob/5090860/paper/paper_i/manuscript/appendix.tex),
[native FIFO-Regel](implemented_equations.md) und
[Rotation samt Claim-Grenzen](rotating_wave_foundation.md).

## 1. Ergebnis

Der aktuelle Ansatz liefert gepruefte klassische Memory-Dynamik, aber noch
keine gemeinsame effektive Grundlage fuer Gravitation und Standardmodell.
Drei Verbindungen sind unterschiedlich einzustufen:

- **Freiheitsgrade:** Die Kreisphase des vorbereiteten Single-Loop-Asts ist
  eine Raumrotation, keine zusaetzliche interne Phase. Das schliesst weder
  andere Formmoden noch relative Orientierungen mehrerer Objekte aus.
- **Lokalitaet:** Der direkte Gauss-Readout hat keine strikte raeumliche
  Reichweite. Eine lokale Aenderung seiner Quelle kann die naechste
  Zielantwort auch in grosser Entfernung aendern. Gedaechtnis allein liefert
  deshalb keinen harten Signalkegel. Eine emergente, kontrolliert lokale
  Langwellenbeschreibung ist damit weder bewiesen noch allgemein widerlegt.
- **Quantenfaehigkeit:** Eine Bell-lokale klassische Messbeschreibung mit
  unabhaengiger Messwahl bleibt auch mit Gedaechtnis CHSH-beschraenkt.
  Dem Minimalmodell fehlt bisher ueberhaupt eine abgeleitete Beschreibung
  zweier Messstationen. Daher liegt weder ein Quantennachweis noch ein
  pauschaler Unmoeglichkeitsbeweis fuer alle Modellvarianten vor.

**Aus R0 abgeleiteter Anschluss:** B1, einen gemeinsamen operationalen
Zustands-/Interventionsvertrag, pruefen. Die
[Bestandsanalyse liegt inzwischen vor](operational_contract.md); die
physikalische Mehrsystem-/Messregel bleibt unbestimmt. Ohne deren Klaerung
keine Quanten-, Lichtkegel- oder Teilchensuche durch Parameteroptimierung.
Paper I bleibt parallel ein begrenzter klassischer Anker; seine
Publikationsfrage ist davon getrennt.

## 2. Annahmen und Resultate

| Bereich | Input | Belegt / hergeleitet | Fehlender Schritt / entscheidender Gegenbefund |
| --- | --- | --- | --- |
| Raum und Zeit | $x_n\in\mathbb R^d$, euklidische Norm, Updateordnung, isotropes Gaussrauschen, vorgegebener Kernel | definierter stochastischer Prozess; augmentierter Zustand ist Markov | Eine externe Geometrie braucht ein operationales Readout und Skalentrennung. Wiederfinden der Eingabedimension ist keine Emergenz. |
| Skalarer Ast | lokaler linearer Drift mit vorgegebenem Gain, gewaehlte Radiusobservablen | Radiusbaseline; analytische lineare Transportformel, keine Transportvalidierung durch Radiusdaten | Kein isolierter nichtlinearer Materiebaustein. Ein Radiusfit allein kann keine fehlende interne Mode nachweisen. |
| FIFO-Rotation | rauschfreier 2D-Ast, vorbereitete Historie, separat gepruefte Parameter | lokale Existenz und numerische Stabilitaet im dokumentierten Umfang; raeumliche Gruppenbahn | Interne Phase muss eine geeignete Symmetriereduktion ueberleben. Single-Loop-Raumphase tut dies nicht; andere Moden bleiben offen. |
| Propagation | im Minimalmodell gespeicherte Spur ohne eigenes raeumliches Transportgesetz; direkte Faltung | algebraischer Fernantwortkanal bei erlaubter Quellenintervention | Eine Antwortschwelle ist kein Kausalrand. Fuer effektive Lokalitaet fehlen Skalierung, Fehlerkontrolle und zugelassene Quellen-/Detektoroperationen. |
| Quantenmechanik | klassische positive Wahrscheinlichkeiten; kein abgeleiteter Praeparations-/Messvertrag | bedingte CHSH-Schranke fuer lokal faktorisierende Messmodelle, unabhaengig von der Groesse des Memory-Zustands | Lokale, messwahlunabhaengige B1-Realisierung koennte keinen quantenmechanischen Bell-Test tragen. Nichtlokalitaet oder andere Annahmen muessen explizit geprueft werden. |
| Gravitation / Standardmodell | bislang Programmziele; Mediatoren, Vorzeichenlabels und Ports in Erweiterungen gesetzt | keine abgeleitete dynamische Raumzeit oder Quantenfeldtheorie | Universelle geometrische Kopplung und Einstein-Grenzfall bzw. Eichstruktur, chirale Fermionen, Statistik und konsistente Wechselwirkungen fehlen. Namen und Analogien ersetzen keine Dynamik. |

Die native Single-Trajectory-Regel legt kein eindeutiges Mehrknotengesetz
fest. Mehrere unabhaengige Kopien bleiben ohne weitere Regel unabhaengig.
Gemeinsame Memory-Felder, Cross-Kernel und reziproke Ports sind jeweils
explizite Erweiterungen, selbst wenn sie dieselbe Kernelform verwenden.
Dass ein solcher Zusatz mathematisch funktioniert, leitet ihn nicht her.

## 3. Analytische Gegenpruefungen

### A. Raumrotation und interne Phase

Fuer die vorbereitete Kreisgeschichte gilt
$Y_n=\mathcal R_{n\theta}Y_*$, einschliesslich aller FIFO-Altersklassen.
Jede unter gemeinsamer Raumrotation invariante Observable hat deshalb auf
dieser idealen Bahn einen konstanten Wert. Die ganze Bahn bildet im
$SO(2)$-Quotienten einen Punkt. Das ist eine Aussage ueber den exakten
Kreisansatz, nicht ueber beliebige nichtkreisfoermige Loesungen.

**Gegenkontrolle:** Fuer zwei Objekte ist nur die gemeinsame Raumrotation
zu entfernen. Ihre relative Orientierung kann erhalten bleiben. Beide
Objekte getrennt zu quotientieren wuerde diese Information kuenstlich
loeschen. Umgekehrt ist relative Raumorientierung noch kein interner
Eichfreiheitsgrad oder quantenmechanischer Spin.

Im untrunkierten linearen Zweizustandsmodell sind die Multiplikatoren
$1$ und $(1-\alpha)(1-g)$. Diese Aussage darf nicht auf den vollen FIFO
uebertragen werden: bereits bei $H=3$, $\alpha=0.2$, $g=0.8$ besitzt die
lineare Historienmap ein gedaempftes komplexes Paar. Komplexe Eigenwerte
sind daher weder ausgeschlossen noch fuer sich Quantenevidenz.

### B. Vorbereitete Unterraeume

Fuer einen radialen Kernel laesst sich der rauschfreie Schritt schreiben als

$$
x_{n+1}=\left(1-\eta\sum_j w_j\phi_j\right)x_n
        +\eta\sum_j w_j\phi_j x_{n-j},
\qquad \nabla K(u)=\phi(|u|)u.
$$

Die Koeffizienten summieren sich zu eins, muessen aber nicht positiv sein.
Somit bleibt die neue Position in der affinen Huelle der vorhandenen
Historie. Eine vorbereitete Ebene ist invariant; das ist keine spontane
Auswahl von zwei oder drei Dimensionen.

Bei $\varepsilon>0$ und unabhaengigen nichtentarteten Gaussinnovationen
besitzt dagegen jeder neue Punkt bedingt auf die Vergangenheit eine volle
$d$-dimensionale Dichte. Nach $H$ frischen Updates haben die $H$
Historienpunkte deshalb fast sicher affinen Rang $\min(d,H-1)$: Jeder
weitere Punkt liegt mit Wahrscheinlichkeit null in der echten affinen
Untermenge der vorherigen Punkte. Das betrifft exakten geometrischen Rang,
nicht effektive Dimension, Antwort-Rang oder eine rauscharm naeherungsweise
niedrigdimensionale Beschreibung. Letztere benoetigt eine eigene Skala.

### C. Ein-Schritt-Antwort statt Schwellenlichtkegel

Betrachte den direkten Readout einer Punktquelle der Masse $m$ bei $y$ an
einem Ziel $x$. Eine Verschiebung $y\mapsto y+s v$ erhaelt die Quellenmasse.
Bei gleichem Zielzustand und gleicher Innovation gilt

$$
\left.\frac{\partial x_{n+1}}{\partial s}\right|_{s=0}
=\eta m\nabla^2K(x-y)v.
$$

Dies gilt, wenn die veraenderte Quelle schon beim betrachteten Force-Read
zugaenglich ist. Eine andere Write-/Read-Reihenfolge kann eine feste
Updateverzoegerung hinzufuegen, aber keine distanzabhaengige Laufzeit.
Fuer eine attraktive Einzelgaussfunktion $K(u)=-A\exp(-|u|^2/(2\sigma^2))$
und $v\perp(x-y)$ ist der Antwortfaktor
$\eta m A\exp(-L^2/(2\sigma^2))/\sigma^2$, strikt positiv fuer jedes endliche
$L=|x-y|$, sofern $\eta,m,A>0$. Bei nichttrivialen Zweiskalen-Gausskernen
aendern isolierte Ausloeschungen nichts an der nichtkompakten Reichweite.

Das ist kein Beweis fuer praktisch nutzbare ueberlichtschnelle Signale:
Interventionszugang, Detektor, physikalische Zeit und messbare Genauigkeit
sind noch zu definieren. Eine Schwelle oder numerischer Underflow kann
kleine Antworten verbergen, aber keinen exakten Kausalrand herleiten.
Auch die unbeschraenkten Gaussinnovationen verhindern eine harte maximale
Schrittweite; dieser separate Befund allein ist kein Signalisierungsbeweis.

### D. Gedaechtnis und Quantenkorrelationen

Fuer Einstellungen $a,b\in\{0,1\}$, Ergebnisse $A,B\in\{-1,1\}$ und einen
vollstaendigen klassischen Zustand $\lambda$ vor der aktuellen Messwahl,
einschliesslich Memory und gemeinsamer Vergangenheit, seien

$$
p(A,B\mid a,b,\lambda)=p(A\mid a,\lambda)p(B\mid b,\lambda),
\qquad p(\lambda\mid a,b)=p(\lambda).
$$

Mit den bedingten Mittelwerten $A_a,B_b\in[-1,1]$ folgt punktweise

$$
|A_0(B_0+B_1)+A_1(B_0-B_1)|
\leq |B_0+B_1|+|B_0-B_1|\leq2.
$$

Integration liefert $|S|\leq2$. Bei adaptiver Memory-Dynamik kann man auf
die ganze Vergangenheit konditionieren. Werden die aktuellen Einstellungen
jeweils frisch, unabhaengig und gleichverteilt gewaehlt, ist die bedingte
Gewinnwahrscheinlichkeit im CHSH-Spiel weiterhin hoechstens $3/4$.
Zwischen Versuchen ist weder Stationaritaet noch Unabhaengigkeit noetig.
Endliche Daten koennen die Erwartungsschranke zufaellig ueberschreiten;
eine Signifikanzpruefung benoetigt geeignete sequenzielle Statistik, keine
unbegruendete IID-Fehlerrechnung. Versuche duerfen nicht nach Einstellungen
oder Ergebnissen aussortiert werden.

**Gegenkontrolle:** Nicht-Signalisieren und Bell-Verletzung reichen auch
zusammen nicht zur Identifikation von Quantenmechanik. Die binaere
PR-Box mit gleichverteilten Randwahrscheinlichkeiten und
$A_{\rm bit}\mathbin{\oplus}B_{\rm bit}=ab$ hat $S=4$, oberhalb der
quantenmechanischen CHSH-Grenze $2\sqrt2$. Die beigefuegten Tests stellen
lokale Strategien, eine bekannte Quantenkorrelation und diese nichtquanten-
mechanische Box gegenueber; keine davon ist aus unserem Modell gewonnen.

## 4. Quellen und Gegenargumente

Geprueft am 2026-10-21. Die eigenen kurzen Ableitungen oben beanspruchen
keine Literaturprioritaet. Externe Aussagen werden nicht als unabhaengig
reproduzierte Physik ausgegeben.

| Quelle / gepruefter Umfang | Relevanz | Grenze der Uebertragung |
| --- | --- | --- |
| [CHSH (1969), Verlagsabstract](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.23.880); [Gill, arXiv v2, Abschnitte 2--4](https://arxiv.org/pdf/quant-ph/0301059v2) | Bedingte lokale Schranken; Gills explizite Memory-/Randomisierungsanalyse | Kein Ausschluss eines Modells, das die genannten Voraussetzungen nicht erfuellt. Eigenen Zwei-Stationen-Vertrag zuerst angeben. |
| [Rohrlich und Popescu (1995), Abschnitt 2](https://arxiv.org/pdf/quant-ph/9508009) | Nicht-Signalisieren erlaubt staerkere als Quantenkorrelationen | Weder Nichtlokalitaet noch ein hoher CHSH-Wert allein etabliert Quantenmechanik. |
| [Nelson (1966), Verlagsabstract](https://journals.aps.org/pr/abstract/10.1103/PhysRev.150.1079) | Stochastischer Ansatz mit expliziter Diffusionskonstante $\hbar/(2m)$ und weiterer mechanischer Struktur | Kein Satz, dass beliebiges Gaussrauschen quantisiert. Die angegebene Kalibrierung ist Voraussetzung, keine Herleitung von $\hbar$ in unserem Modell. Kein Volltextabgleich durchgefuehrt. |
| [Wallstrom (1994), Verlagsabstract](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.49.1613) | Warnt vor Gleichsetzung von Madelung-Gleichungen und voller Schroedinger-Theorie ohne zusaetzliche Quantisierungsbedingung | Pruefpunkt fuer einen spaeteren stochastischen Ansatz, kein universeller Ausschluss heutiger Erweiterungen; kein Volltextabgleich durchgefuehrt. |
| [Levin und Wen, arXiv v2, Abschnitte I--III und Hilbertraumdefinition](https://arxiv.org/pdf/cond-mat/0404617v2) | Konstruktiver Gegenbeleg gegen die Behauptung, emergente Eichbosonen und Fermionen seien grundsaetzlich unmoeglich | Quantum-Spins, Hilbertraum und Hamiltonian sind bereits Inputs. Keine Herleitung dieser Strukturen aus unserer klassischen skalaren Historie; kein Nachweis des gesamten chiralen Standardmodells. |

Eine vollstaendige Literaturklassifikation von Quantengravitation und
emergenter Quantenmechanik ist nicht Gegenstand dieses endlichen Audits.
Keine gefundene Quelle begruendet, dass gerade unsere Mikrodynamik das
Fernziel erreicht. Ebenso begruendet eine fehlende Quelle kein No-go.

## 5. B1 und Alternativen

**Aus R0 ausgewaehlter Brueckenschritt B1:** Fuer einen konkret
benannten bestehenden Modellzweig den operationalen Vertrag festhalten:
vollstaendiger Zustand, Praeparation, zulaessige Interventionen, Readouts
zweier Teilsysteme, Informationszugriff beim Update und zeitliche Zuordnung.
Aus genau dieser Regel den ersten Antwortoperator und die bedingte
Wahrscheinlichkeitsstruktur herleiten. Nichts davon durch einen passenden
Mediator oder ein gewuenschtes Korrelationsgesetz ersetzen.

**Abnahmekriterium:** Entweder sind diese Operationen aus vorhandenen Regeln
eindeutig bestimmt und erlauben ein falsifizierbares gemeinsames Experiment,
oder die fehlende Modellregel wird als konkreter Blocker ausgewiesen.
Ein lokal faktorisierender Vertrag bleibt fuer den Quantenpfad negativ;
ein direkter Fernzugriff muss auf beobachtbares Signalisieren geprueft werden.
Ein positives B1-Ergebnis waere nur eine definierte Pruefbasis, kein Go fuer
Quantenmechanik, Gravitation oder Standardmodell.

**Fortschreibung:** Die [B1-Bestandsanalyse](operational_contract.md) ordnet
die vorhandenen Regeln zu und leitet fuer die Frozen-Source-Erweiterung
Antwort und bedingte Verteilung ab. Der gemeinsame physikalische
Mehrsystem-/Messvertrag bleibt als konkreter Blocker offen.

**Aktuelle Luecke:** Der native Einzelprozess definiert keine zwei
unabhaengig einstellbaren Messstationen. Die bisherigen Mehrknotenports
sind konstruierte Erweiterungen. Welche davon physikalisch gemeint ist,
folgt nicht aus Paper I. Die vorhandenen Definitionen duerfen analytisch
verglichen werden; neue Regeln oder Ziellaeufe bleiben eine
Richtungsentscheidung. Insbesondere bleibt P5-D geschlossen.

**Alternativen:** Den klassischen Ansatz als eigenstaendiges Modell
weiterentwickeln, ohne einen fundamentalen Anspruch zu behaupten; oder
eine begruendete neue mikroskopische Struktur formulieren und deren
zusaetzliche Annahmen offen tragen. Diese zweite Option wird hier nicht
automatisch gewaehlt. Die B1-Bestandsanalyse benennt die fehlenden Regeln;
ob diese hergeleitet oder als Erweiterung gesetzt werden sollen, bleibt
eine explizite Richtungsentscheidung.

## 6. Verifikation und offene redaktionelle Luecke

[Zwoelf synthetische Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_foundation_feasibility.py)
pruefen mit unveraenderten Repository-Helfern Rotation/Shape-Kontrolle,
relative Orientierung, analytische versus differenzierte Gaussantwort,
Affine-Huelle/Rauschkontrolle, reelle Zweizustands- versus komplexe
FIFO-Moden sowie lokale und nichtlokale Korrelationstabellen.
Sie verwenden keine Produktionscheckpoints, Rootsuche oder Gate-Ziellaeufe.
Lokaler Lauf: `pytest tests/test_foundation_feasibility.py -q`, 12 bestanden
mit NumPy 2.3.5, SciPy 1.16.3 und pytest 8.4.2.
Die numerischen Checks ersetzen die allgemeinen Argumente oben nicht.
Die fast-sichere Rangaussage wird analytisch begruendet, nicht aus einem
kleinen Zufallsensemble geschaetzt.

Der alte Paper-II-Text enthaelt trotz vorsichtigem Abstract noch nicht
belegte Aussagen ueber metastabile Knoten, fehlende geometrische Inputs und
bereits gemessene universelle Propagation. Er ist damit keine verlaessliche
Zusammenfassung des jetzigen Paper I und darf bis zur sachlichen
Ueberarbeitung nicht als Ergebnisfassung zirkulieren. Dieser Audit aendert
keine Manuskript-PDFs und gibt den alten Text nicht frei.
