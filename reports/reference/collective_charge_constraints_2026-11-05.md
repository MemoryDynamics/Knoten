# Kollektive Ladung: lokale Nebenbedingungen statt Knotenzahl

Stand: 2026-11-05. Gezielter Literatur-/Bestandsabgleich und bedingte
Algebra, **keine neue Modelldynamik oder Zielsimulation**.

## Ergebnis fuer die Richtungsentscheidung

Ein Hopf-Sektor ist keine notwendige Voraussetzung jeder moeglichen
Ladungsentstehung. Eine andere bekannte Route identifiziert Ladungen
als lokale Defekte einer kollektiven Flussbedingung. Entscheidend ist
dann nicht die Wahl einer isolierten Knotenform, sondern die Herkunft
dieser Bedingung, der Zustandsstatistik und der Wechselwirkung.

Fuer den naheliegenden Anschluss an die FIFO-Alterskette gibt es hier
einen konkreten Gegenbefund: **Geometrischer Ringschluss macht einen
altersgewichteten Linienfluss nicht divergenzfrei.** Die Gewichtsdifferenzen
erzeugen innere Quellenbeitraege. Bereits die Ersetzung der vorhandenen
gerichteten Punktdepositionen durch exakte Linienintegrale waere eine
zusaetzliche Readout-Definition, keine Identitaet des bestehenden Felds.

Das ist weder ein Ausschluss anderer kollektiver Phasen noch ein Beleg
fuer elektrische Ladung. Die bisherigen Invariantensaetze verbieten
nicht lokale Gegenladungen bei konstantem Gesamtwert. Ebenso betrifft
der fehlende Coulomb-Schwanz einzelner lokalisierter Gaussreadouts nicht
automatisch kollektive Langwellenantworten. Eine neue physikalische
Regel wird durch diesen Vergleich nicht ausgewaehlt.

## Was die drei Primaerarbeiten tatsaechlich liefern

**Klassische Zustandsstatistik.** Huse, Krauth, Moessner und Sondhi,
*Coulomb and Liquid Dimer Models in Three Dimensions*, PRL 91, 167004
(2003), behandeln harte Dimere auf vorgegebenen Gittern. Auf dem
bipartiten kubischen Gitter wird aus der lokalen Belegungsbedingung
ein divergenzfreier Linkfluss; Monomere verletzen die Bedingung mit
entgegengesetzten Vorzeichen auf den beiden Untergittern. Die Arbeit
postuliert eine quadratische grobgekoernte statistische Gewichtung und
stuetzt ihre dipolaren Korrelationsvorhersagen numerisch. Die
Monomerwirkung ist entropisch. Nichtbipartite Vergleichsgitter liefern
andere Phasen: lokale Regeln allein garantieren keine Coulomb-Phase.
Dies ist keine Ableitung von Quantenmechanik.
[Primaervolltext, v3](https://arxiv.org/pdf/cond-mat/0305318v3),
[Publikationsnachweis](https://doi.org/10.1103/PhysRevLett.91.167004).

**Energetische magnetische Wirkung.** Castelnovo, Moessner und Sondhi,
*Magnetic Monopoles in Spin Ice*, Nature 451, 42-45 (2008), identifizieren
Defekte der Eisregel als magnetische Quasiteilchen. Die energetische
Coulomb-Wirkung nutzt bereits vorausgesetzte dipolare Wechselwirkungen.
Die Arbeit unterscheidet sie ausdruecklich von einem entropischen,
mit Temperatur verschwindenden Beitrag. Die Defekte sind Quellen des
H-Felds im Material, nicht fundamental eingefuehrte magnetische Monopole
oder Elektronen/Protonen. Die Eisregel allein reproduziert diesen
energetischen Anschluss nicht.
[Primaervolltext, v2](https://arxiv.org/pdf/0710.5515v2),
[Publikationsnachweis](https://doi.org/10.1038/nature06433).

**Quantenmechanischer Eichanschluss.** Hermele, Fisher und Balents,
*Pyrochlore Photons: The U(1) Spin Liquid in a S=1/2 Three-Dimensional
Frustrated Magnet*, PRB 69, 064404 (2004), beginnen mit Quantenspins auf
einem vorgegebenen Gitter. Stoerungstheorie liefert einen effektiven
Ringtausch im energiearmen Unterraum; die behandelte U(1)-Phase besitzt
eine Maxwell-artige Langwellenbeschreibung. Im Rotoranschluss werden
konjugierte Quantenoperatoren verwendet. Diese Quantenstruktur stammt
nicht aus klassischem Rauschen. Die lokale Erhaltung des projizierten
Hamiltonoperators darf nicht als exakte lokale Erhaltung des gesamten
mikroskopischen Hamiltonoperators bei endlicher Querkopplung gelesen werden.
[Primaervolltext, v3](https://arxiv.org/pdf/cond-mat/0305401v3),
[Publikationsnachweis](https://doi.org/10.1103/PhysRevB.69.064404).

Die Schlussfolgerung fuer unser Projekt ist bedingt: Eine statische
Flussbedingung oder ein attraktiver Paarbeitrag reicht nicht fuer
propagierende Quantenfelder. Auch eine entropische freie Energie ist
nicht ohne Nachweis einer passenden Verteilung und Temperatur eine
mechanische Energie der nichtgleichgewichtigen Memory-Dynamik.

## Referenzalgebra: wo eine inverse Laplace-Wirkung herkommt

Die folgende Rechnung legt ihre Annahmen offen; sie ist kein neuer
Memory-Simulator und keine Neuheitsbehauptung. Sei $D$ die ausgehende
Inzidenzmatrix eines endlichen zusammenhaengenden Graphen: jede Kante
hat +1 an ihrem Anfang und -1 an ihrem Ende. Alle Kantenenden liegen
im Graphen; es gibt keine aeusseren Randreservoire. Fuer Linkfluesse $f$
definieren wir formal

$$
q=Df,\qquad \boldsymbol{1}^{\mathsf T}q=0.
$$

Eine Aenderung einer einzelnen Kante erzeugt zwei entgegengesetzte
lokale Aenderungen; ein Zyklenfluss $c$ mit $Dc=0$ laesst alle $q$ unveraendert.
Ganzzahligkeit folgt nur aus einem entsprechend diskreten Flussalphabet,
nicht aus dieser Identitaet. Die Gesamtneutralitaet ist hier eine
geometrische Randidentitaet, noch kein Schutz einzelner Defekte.

Nehmen wir zusaetzlich eine positive quadratische Energie oder freie
Energie und kontinuierliche Linkfluesse an:

$$
\mathcal F(f)=\frac{\kappa}{2} f^{\mathsf T}f,\qquad
Df=q,\qquad \kappa>0.
$$

Mit $L=DD^{\mathsf T}$ und der Moore-Penrose-Inversen $L^+$ gilt fuer neutrale $q$

$$
f_* = D^{\mathsf T} L^+q,\qquad
\mathcal F_{\min}(q)=\frac{\kappa}{2}q^{\mathsf T}L^+q.
$$

Beweis: $LL^+q=q$ auf dem zu Konstanten orthogonalen Unterraum. Jeder
andere zulaessige Fluss ist $f_*+c$ mit $Dc=0$. Weil $f_*^{\mathsf T}c=0$, ist sein
Mehrbetrag genau kappa mal die quadrierte Norm von c, geteilt durch 2.
Bei nichtneutralem $q$ existiert auf diesem Graphen kein zulaessiger
Fluss; ein blindes Pseudoinversen-Rezept entfernt dessen Mittelwert
und loest damit eine andere Aufgabe. Bei diskreten oder beschraenkten
Links ist die kontinuierliche Minimierung nicht automatisch die exakte
mikroskopische Aufgabe. Eine statistische Verwendung benoetigt ebenfalls
einen eigenen Anschluss an die Verteilung der zugelassenen Zustaende.

Die positive Quellquadratik entsteht aus der **Nebenbedingung**. Sie
ist nicht die negative Quellquadratik beim freien Relaxieren eines
linear an eine Quelle gekoppelten skalaren Felds, siehe
[Energie-/Fernfeld-Audit](interaction_structure_inventory_2026-11-02.md).
Die bereits bekannte Kontinuitaetsidentitaet
$\Delta\rho+\nabla\cdot J=0$ liefert diese Nebenbedingung und Energie nicht.

Ebensowenig legt die Graphrechnung 3D fest. Auf einem $N$-Zyklus fuer
$q=\delta_0-\delta_d$ ist

$$
q^{\mathsf T}L^+q=\frac{d(N-d)}{N},\qquad 1\le d\le N/2.
$$

Dies folgt auch aus zwei parallelen Wegen mit Laengen $d$ und $N-d$.
Es ist eine andere Abstandsgesetzlichkeit als die 3D-Coulomb-Wirkung.
Erst wenn $L$ im angegebenen Kontinuums-/Randgrenzfall zu $-\Delta$ in drei
Dimensionen wird, ist die passende unendliche Greenfunktion
$1/(4\pi r)$. Bei zwei lokalisierten Quellen ist dann nach getrennter
Behandlung der Selbstbeitraege der Kreuzterm proportional zu $q_1q_2/r$.
Der positive Gesamtausdruck allein legt auf beliebigen endlichen
Graphen weder diese Abstandsform noch jedes Vorzeichen seiner
einzelnen Matrixelemente fest. Hier wird keine 3D-Grenze hergeleitet.

## Konkreter Bestandsabgleich: der FIFO-Altersfluss

Die vorhandene Funktion
[`oriented_history_from_state`](../../src/emergenz_knoten/vector_memory.py)
verwendet bei newest-first-Historie $y_0,\ldots,y_{H-1}$ die Verschiebungen
$y_j-y_{j+1}$ und die Gewichte $w_j$. Das resultierende gerichtete Gaussfeld
besteht aus Punktdepositionen am neueren Ende. Es ist **kein** exaktes
Linienintegral entlang der Zwischenstrecke.

Um sogar die guenstigere Linieninterpretation zu pruefen, definieren wir
nur als analytischen Vergleich, fuer $H\geq2$ und normiertes glattes $G$,

$$
F(z)=\sum_{j=0}^{H-2} w_j (y_j-y_{j+1})
\int_0^1 G\bigl(z-y_{j+1}-s(y_j-y_{j+1})\bigr)\,ds.
$$

Direkte Ableitung des Integranden und Teleskopieren liefern exakt

$$
\nabla\cdot F(z)=-w_0G(z-y_0)
+\sum_{j=1}^{H-2}(w_{j-1}-w_j)G(z-y_j)
+w_{H-2}G(z-y_{H-1}).
$$

Bei gleichen Gewichten bleiben nur die Endpunkte. Bei nativen
geometrischen Gewichten $w_j=M_0\alpha(1-\alpha)^j$, $0<\alpha<1$,
$M_0>0$, gilt dagegen $w_{j-1}-w_j=\alpha w_{j-1}>0$. Auch auf einem
geometrischen Ring $y_{H-1}=y_0$ bleibt am gemeinsamen Ende der
Koeffizient $w_{H-2}-w_0$; die inneren Beitraege verschwinden nicht.
Die Koeffizientensumme ist trotzdem null. Fuer verschiedene innere
Stuetzpunkte eines einfachen Rings sind damit lokale Defekte an allen
Stuetzpunkten moeglich, nicht lediglich zwei frei verschiebbare Enddefekte.
Spezielle Ueberlagerungen oder degenerierte Geometrien werden nicht
ausgeschlossen. Bei einem einfachen Ring und Gaussglattung kann die
Summe mit diesen nichtverschwindenden Koeffizienten nicht identisch null
sein: Die Gauss-Fouriertransformierte ist nirgends null, und die
Diracmassen an verschiedenen Orten sind linear unabhaengig. Diese
konstruierte Historie ist kein beobachteter nativer Attraktor.

Gleiche Gewichte sind hier eine synthetische Positivkontrolle, nicht
der unveraenderte native Fall $\alpha=0$: bei festem $H$ und $M_0$ verschwindet
in diesem Grenzgang zugleich die native Masse. Die notwendigen
Skalierungsunterscheidungen stehen im
[Grenzfallbericht](fading_memory_limits_2026-11-04.md). Der Gegenbefund
schliesst einen erst noch nachzuweisenden kontrollierten Grenzfall nicht aus.

Die [anschliessende Umlauf-/Kollektivpruefung](loop_flux_limits_2026-11-05.md)
bestimmt nun einen solchen bedingten Readout-Grenzfall fuer vorgegebene
periodische Historien. Sie leitet keine native Bahn her und zeigt
getrennt, weshalb unabhaengige lokalisierte Umlaeufe die langwellige
Amplitude der klassischen Coulomb-Referenz dennoch verfehlen.

Schliesslich besitzt selbst das native **Punkt**-Vektorfeld einer
gleichgewichteten geschlossenen Polygonhistorie im Allgemeinen eine
nichtverschwindende Divergenz. Der direkte Test vergleicht dessen
analytische Ableitung mit Differenzenquotienten und dem divergenzfreien
Linienfluss. Damit wird die Ersatzinterpretation nicht stillschweigend
als bestehende Implementierung ausgegeben. Keine der beiden
Divergenzen ist damit bereits als elektrische Ladung identifiziert.

## Fehlender Anschluss, nicht bloss neue Benennung

| Erforderliche Eigenschaft dieser Route | Stand im geprueften Bestand |
| --- | --- |
| Lokale Flussvariable und Defektdefinition aus demselben Zustand | Gerichtete Readouts vorhanden; die einfache altersgewichtete Bahn liefert die obigen Quellenreste. Kein identifizierter kollektiver Gaussabschluss. |
| Erhaltung oder kontrolliert seltener Bruch der lokalen Bedingung | Massenerhaltung ist belegt, elektrische Quellenbilanz nicht. Endliche Lebensdauern brauchen Fehler-/Zeitgrenzen; globale Neutralitaet allein reicht nicht. |
| Deconfinerte Defekte statt wachsender Verbindungskosten | Keine entsprechende native gemeinsame Energie oder stationaere freie Energie nachgewiesen. |
| Langreichweitige Paarantwort mit passendem Vorzeichen und Amplitude | Bedingte Graphrechnung vorhanden; keine aus Memory abgeleitete Graph-/Kontinuumsgrenze oder Steifigkeit. |
| Quantenzustaende und ihre Dynamik | Im Referenzzweig Inputs, im Emergenzzweig offen. Statische Korrelationen sind keine Quantenphotonen. |
| Elektron/Proton und Gravitation | Weder Identifikation mit bekannten Materieladungen noch Massen/Spin/Statistik oder universelle gravitative Kopplung gewonnen. |

Der entscheidende Anschluss ist daher eine aus dem nativen Zustand
definierte lokale Bedingung **mit ihrer Updatebilanz und ihrer
statistischen oder energetischen Begruendung**. Eine nachtraegliche
Inzidenzmatrix, das Entfernen der Altersgewichte oder das Einsetzen
einer inversen Laplace-Wirkung genuegen nicht. Falls die benoetigte
Bedingung nur durch neue Regeln existiert, waere dies eine explizit zu
entscheidende Erweiterung. Die Autorenentscheidung bleibt offen;
die Arbeitsreihenfolge steht nur in den
[Projektprioritaeten](../../docs/status/project_priorities.md).

## Verifikation und Quellenumfang

Die [konstruierten Tests](../../tests/test_collective_charge_constraints.py)
pruefen lokale Gegenquellen, Zyklen, fehlende automatische
Ganzzahligkeit, Orientierungskonvention, neutrale Loesbarkeit,
Minimierung gegen ein unabhaengiges KKT-System und die Zyklusformel.
Die FIFO-Gegenkontrollen verwenden die vorhandenen nativen Gewichte,
Historienzuordnung und Fourier-Linienintegrale. Es werden keine
Zielbahnen, Eigenmoden von Knoten oder physikalischen Parameter gesucht.
Ein Testpass ersetzt weder den Beweis noch die fehlende native Ableitung.

Verifikation am 2026-11-05: **79 betroffene Tests bestanden in 2.31 s**,
darunter 13 neue konstruierte Kontrollen. Ruff, strikter MkDocs-Bau und
Whitespacepruefung bestehen. Dies ist keine vollstaendige Repository-
Testsuite. Keine Zielsimulation, neue Produktionsfunktion oder
unabhaengige Reproduktion der Literaturmodelle wurde ausgefuehrt.

Quellenpruefung am 2026-11-05: Huse et al. v3 vom 14.11.2003, Modell,
Gl. (1)-(5), Monomerpassage und Vergleich der Gittersysteme; Hermele et
al. v3 vom 25.11.2003, Abschnitt II A, Rotor-/Eichabbildung Gl. (13)-(18),
Kontinuumswirkung Gl. (44), Abstract; Castelnovo et al. v2 vom
31.10.2007, Modell und Defekt-/Wechselwirkungspassagen auf S. 1-3.
Keine eigene Reproduktion der dortigen Vielteilchennumerik. APS-
Publikationsdaten wurden direkt geprueft; die Nature-Seite war beim
aktuellen Abruf gesperrt, Journal/DOI sind in arXiv bestaetigt.
Eine gezielte DOI-Suche nach Korrekturen ergab keinen einschlaegigen
Treffer, ist aber kein vollstaendiger Korrektheits-/Retraktionsaudit.
PDF-Satzdaten werden nicht mit Publikations- oder Versionsdaten verwechselt.
Dies ist kein systematischer oder vollstaendiger aktueller Literaturreview.
