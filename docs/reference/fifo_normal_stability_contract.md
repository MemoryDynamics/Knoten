# FIFO-Normalstabilitaet: Methodenvertrag

Stand: 2026-10-26. Aufbauend auf der
[Strukturauswahl](fifo_structure_candidate.md), Ausgangsrevision `6a5b76d`.
Analytische Reduktion, synthetische Kontrollen und der in Abschnitt 5
dokumentierte unentschiedene Zielversuch. **Keine neue Zielausfuehrungsfreigabe.** Die Arbeitsreihenfolge steht
in den [Projektprioritaeten](../status/project_priorities.md).

## 1. Welche Aussage geprueft werden soll

Der Kandidat ist die altersgeordnete, vorbereitete rotierende FIFO-Schleife
des unveraenderten rauschfreien K0-H-Modells. Gefragt ist ausschliesslich:
Klingen ihre kleinen Formstoerungen senkrecht zur Kreisebene linear ab,
nachdem normale Translation und die beiden Ebenenneigungen getrennt sind?

Der bisherige 2D-G5-Pass beantwortet das nicht. Ein positiver Normaltest
waere auch allein kein vollstaendiger 3D-Stabilitaetsbeweis: Der ebene
Formblock muss am selben exakten Kreisroot kontrolliert sein. Formation,
Rauschlebensdauer, topologischer Schutz, Quantisierung und physikalische
Kopplung bleiben weitere Fragen. Es wird keine neue Modellregel eingefuehrt.

## 2. Exakter Symmetriequotient

Mit den in der Strukturanalyse definierten $c_j$ hat der Normalblock
$B_\perp$ die erste Zeile $b_0=1-\sum_{j=1}^{H-1}c_j$, $b_j=c_j$
und Einsen auf der unteren Nebendiagonale. Sein charakteristisches Polynom
ist

$$
p_H(z)=z^H-b_0z^{H-1}-b_1z^{H-2}-\cdots-b_{H-1}.
$$

Am **exakten** Kreisroot mit $H\geq3$, $R>0$, $0<\theta<\pi$ bilden
$\mathbf1$, $(\cos j\theta)_j$ und $(\sin j\theta)_j$ einen
dreidimensionalen invarianten Symmetrieraum. Seine Multiplikatoren sind
$1,e^{i\theta},e^{-i\theta}$, also

$$
p_H(z)=g_\theta(z)q_{H-3}(z),\qquad
g_\theta(z)=(z-1)(z^2-2\cos\theta\,z+1).
$$

Die kubische Koeffizientenfolge lautet
$[1,-(1+2\cos\theta),1+2\cos\theta,-1]$.
Fuer eine orthogonale Basis $U$, deren erste drei Spalten diesen Raum
aufspannen, gilt

$$
U^T B_\perp U=\begin{pmatrix}T&C\\0&A\end{pmatrix},\qquad
\det(zI-T)=g_\theta(z),\quad\det(zI-A)=q_{H-3}(z).
$$

Der Formquotient $A$ ist strikt linear asymptotisch stabil genau dann,
wenn **alle** Nullstellen von $q_{H-3}$ strikt im Einheitskreis liegen.
Das entfernt genau drei bekannte Symmetriemoden, nicht alle Eigenwerte
in einer numerischen Umgebung von eins. Zusaetzliche neutrale Moden,
auch bei denselben Eigenwerten oder in Jordan-Ketten, bleiben im Quotienten.
Die orthogonale Restebene muss selbst nicht invariant sein; der obere
rechte Block $C$ darf ungleich null sein.

An einer nur angenaeherten Kreisloesung muss die Division einen Rest
liefern duerfen. Ein kleiner Rest oder ein Intervallrest, der null enthaelt,
ist **kein Existenzbeweis** fuer einen Root und legitimiert nicht das
Weglassen von Moden. Die exakte Faktorenidentitaet folgt aus der
Kreisbalance, nicht aus einer Toleranzentscheidung.

## 3. Bekannter Vollspektrumtest statt Wurzelauswahl

Verwendet wird die klassische reelle Schur-Cohn-Rekursion, kein neuer
Stabilitaetssatz. Fuer ein monisches Polynom
$q_m(z)=z^m+a_1z^{m-1}+\cdots+a_m$ setze $\kappa_m=a_m$. Solange
$|\kappa_m|<1$, lautet die normierte Reduktion

$$
q_{m-1}(z)=
\frac{q_m(z)-\kappa_m z^m q_m(1/z)}{z(1-\kappa_m^2)}.
$$

Strikte Schur-Stabilitaet ist aequivalent zu $|\kappa_m|<1$ in allen
Reduktionsschritten. Das konstante monische Polynom hat keine Nullstellen.
Notwendig ist bereits $|a_m|<1$ als Produkt der Wurzelbetraege; die
Rekursion liefert die vollstaendige Pruefung. Negative Reflexions-
koeffizienten sind erlaubt. Gepruefte Primaerquelle: V. Olshevsky,
[A Superfast Algorithm for Determining the Discrete-time Stability for Matrix Polynomials](https://www2.math.uconn.edu/~olshevsky/papers/schurcohn_s.pdf),
Abschnitt 0.1.2, PDF-Seite 2, am 2026-10-25. Verwendet wird nur dessen
klassischer skalarer Ausgangstest, nicht der spaetere schnelle
Matrixalgorithmus.

Der Prototyp wertet die Koeffizienten als nach aussen gerundete Intervalle
mit `mpmath.iv` aus. Die Entscheidung betrifft die **vorgegebene reelle
monische Koeffizientenbox**:

| Ausgabe | Hinreichend gepruefte Bedingung | Aussage |
| --- | --- | --- |
| `strictly-schur` | In jedem Schritt liegt die obere Schranke fuer $|\kappa_m|$ unter eins. | Alle Polynome der Eingangsbox sind strikt Schur-stabil, unter der verwendeten Arithmetik-Vertrauensbasis. |
| `not-strictly-schur` | Nach strikt bestandenen Schritten liegt die untere Schranke fuer $|\kappa_m|$ mindestens bei eins. | Kein Polynom der Box ist strikt Schur-stabil. Keine automatische Unterscheidung zwischen neutralen und wachsenden Moden. |
| `inconclusive` | Das Intervall erlaubt keine dieser Entscheidungen. | Keine Stabilitaets- oder Instabilitaetsaussage. |

Ungueltige Eingaben werden abgewiesen, nicht als physikalischer Fail
klassifiziert. Insbesondere bedeutet $|\kappa_m|=1$ nicht automatisch
nur Randwurzeln: $z^2-\tfrac52z+1$ hat die Wurzeln $2$ und $1/2$.
Eine positive Wachstumsaussage braucht einen eigenen Aussenwurzelbeleg.

## 4. Was der Prototyp nachweist

[Implementierung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/src/emergenz_knoten/fifo_normal_stability.py)
und [synthetische Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_fifo_normal_stability.py)
enthalten keine archivierten Zielparameter, keinen Ziel-Dateilader und
keine Produktionsfreigabe. Geprueft werden:

- Exakte rationale Division durch den Symmetriefaktor; jeder Rest bleibt
  erhalten. Intervallquotienten und -reste umschliessen rationale Kontrollen.
- Uebereinstimmung mit einer unnormierten rationalen Schur-Rekursion bei
  50 und 90 Dezimalstellen, inklusive binarer Endpunkt-Einschliessungen.
- Unabhaengige orthogonale Matrixreduktion kleiner synthetischer
  Companionmatrizen und Vergleich des vollstaendigen Restspektrums.
- Erhalt einer zusaetzlichen Mode bei eins sowie knapp darunter und
  darueber; Intervall-Unentschiedenheit und Eingabevalidierung.
- Ein strikt stabiler, nichtnormaler Block mit voruebergehender
  Verstaerkung: Fuer $A=\left(\begin{smallmatrix}1&-1/4\\1&0\end{smallmatrix}\right)$
  liegen beide Eigenwerte bei $1/2$, aber $\|A\|_2>1.4$.

Strikte Spektralstabilitaet bedeutet deshalb nicht monotone
Ein-Schritt-Kontraktion. Eine spaetere quantitative Rausch- oder
Nichtlinearitaetskontrolle braucht auch transiente Verstaerkung und
Stoerungsamplituden. Der Test allein liefert weder Basin noch Lebensdauer.

Die einfache Rekursion kostet quadratisch viele Arithmetikoperationen in
$H-3$. Intervallabhaengigkeiten und kleine Nenner bei $|\kappa_m|\approx1$
koennen die Einschliessung aufweiten. Weder Laufzeit noch Entscheidbarkeit
an den langen FIFO-Horizonten sind mit diesen kleinen Tests belegt.
Zwei Praezisionen sind kein zweiter unabhaengiger Intervallbackend.
Die gespeicherten binaeren Endpunkte sind fuer Einschliessungen massgeblich;
Dezimaldarstellungen dienen der Lesbarkeit.

### Rootbox-Anbindung

`certify_normal_fifo_box` ergaenzt jetzt die zuvor fehlende Kette. Fuer
exakte dezimale Parameter und eine vorgegebene Box wird zuerst das
vorhandene finite-H-Krawczyk-Verfahren erneut ausgewertet. Ohne dessen
bestandene Bedingungen folgt `root-not-certified`, ohne Schur-Auswertung.
Die Anbindung akzeptiert kein externes Pass-Flag.

Die binaeren Endpunkte der gesamten zertifizierten Rootbox gehen direkt
in die Intervallrechnung fuer $c_j$, $p_H$, $\cos\theta$ und den
Polynomquotienten ein. Weder Mittelpunkt noch angezeigte Dezimalgrenzen
werden zurueckgelesen. Die Division und die Schur-Rekursion arbeiten ohne
dezimalen Zwischenexport. Bei einem mit der Faktorenidentitaet
unvereinbaren Rest folgt `inconsistent-symmetry-factor`, kein physikalischer
Instabilitaetsclaim. Parameter, Root-Eingaben, Zertifikat und alle
Polynomintervalle werden zusammen ausgegeben. Der Adapter bindet noch
keinen bestimmten archivierten Kandidaten und ist kein Zielrunner.

Zwei **konstruierte Methodenkontrollen**, keine ausgewaehlten
Forschungskandidaten, pruefen diese ganze Kette. Fuer $H=4$, $R=1$,
$\theta=\pi/2$, $q=1-\alpha$, $\eta=M_0=1$ erzwingt die Kreisbalance

$$
c_1=-\frac{1}{1-q^2},\quad c_2=\frac{1}{1-q^2},\quad
c_3=-\frac{q^2}{1-q^2},\qquad
q_{H-3}(z)=z-\frac{q^2}{1-q^2}.
$$

Mit $\sigma_{\rm rep}=1$, $\sigma_{\rm att}=2$ lassen sich die beiden
Gaussamplituden aus den erforderlichen Kraftfaktoren bei den Chordlaengen
$\sqrt2$ und $2$ durch ein lineares Zweiersystem bestimmen. Der Test
waehlt vorab $q=1/2$ und $q=3/4$: Die Normalformmode ist dann $1/3$
beziehungsweise $9/7$. Die Amplituden werden auf 110 Dezimalstellen
geschrieben; anschliessend zertifiziert der Adapter den nahen Root des
**so definierten Dezimalmodells** bei 60 und 90 Stellen. Dies setzt keinen
exakt rationalen Winkel oder unveraenderten Root nach Rundung voraus.
Die Stabilitaetsaussagen folgen aus der Intervallkette, nicht allein aus
der idealisierten Kontrollformel. Ueber den ebenen Formblock dieser
Testmodelle wird nichts behauptet.

Die [23 Adaptertests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_fifo_normal_adapter.py)
pruefen zudem eine unabhaengige Chordformel, den normalen Differenzenquotienten
des Produktionskernels, Nicht-Roots, absichtlich inkonsistente Faktoren,
beschadigte Anzeigedezimalen, Eingaben und Praezisionswiederherstellung.
Die 66 bisherigen Polynomtests bleiben gruen. Zusammen mit den betroffenen
Intervall-, Struktur- und Dokumentationsregressionen: **173 bestanden**.
Verwendet wurden Python 3.12.14, mpmath 1.3.0, NumPy 2.3.5, SciPy 1.16.3
und pytest 8.4.2. Diese Kontrollen sind weder ein unabhaengiges Fachreview
noch eine neue Auswertung archivierter FIFO-Zellen.

## 5. Begrenzte Zielauswertung und Ergebnis

Eine begrenzte Zielauswertung erfordert folgende Bestandteile eines
vorab festzulegenden Ausfuehrungsvertrags:

- **Root und Herkunft:** Ein fest ausgewaehlter existenzzertifizierter
  endlicher Kreisroot mit Revision, exakten Parametern und Rootbox. Nicht
  nach Sichtung von Normalbefunden den guenstigsten Kandidaten auswaehlen.
  Das separate unendliche G4-Zertifikat ersetzt diese finite-H-Bindung nicht.
- **Verifizierte Abbildung:** Der jetzt implementierte Adapter muss mit
  dem festgelegten Zielinput und seiner Herkunft verbunden werden; seine
  Kontrollfaelle sind kein Zielpass. In der bestehenden Intervallbalance ist die erste
  Komponente $-F_R$, die zweite $F_T$; diese Vorzeichenkonvention bleibt
  explizit zu pruefen.
- **Symmetrie und Rest:** Der exakte Kreisroot begruendet die Division;
  der numerische Rest wird separat berichtet. Null im Restintervall ist
  lediglich eine Konsistenzbedingung, kein Ersatz fuer den Rootbeweis.
- **Budget und Abbruch:** Praezisionsstufen, Laufzeitbudget, feste Eingaben
  und Ergebnisformat vorab begrenzen. Bei unzureichender Einschliessung
  `inconclusive`, keine automatische Parametersuche oder unbegrenzte
  Praezisionserhoehung.
- **Autorisierung:** Erst nach Adapterpruefung und Freigabe einen solchen
  Zieltest ausfuehren. Alte G5- und P5-Freigaben werden nicht wiederverwendet.

Der [vorgeschlagene Ankertest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/project/meta/preregistration/fifo_normal_stability_anchor_proposal_2026-10-25.md)
legt den urspruenglichen H=1200-Anker, die Quellenrevision, zwei
Praezisionsstufen und Abbruchgrenzen vor jeder Zielauswertung fest.
Der begrenzte Runner ist inzwischen mit 34 Ablauf- und Fehlerkontrollen
implementiert, darunter ein echter Prozessabbruch und ein kleiner
Nicht-Root-Worker. Zusammen mit den vorherigen Regressionen bestehen 207
Tests. Der Runner liest den gepinnten Git-Input, verlangt eine saubere
benannte Ausfuehrungsrevision und ueberschreibt keine bestehende Auswertung.
Sein Ausfuehrungsflag ersetzt keine menschliche Zustimmung. Die konkrete
Autorenfreigabe liegt inzwischen vor und verlangt auch schraege Stoerungen.
Der entsprechend ergaenzte Vertrag legt zehn feste Winkel-/Vorzeichenarme
fuer 2000 Updates im bestehenden ersten Panelbudget fest. Das sind
float64-Formdiagnosen in einem endlichen Fenster, kein Ersatz fuer den
linearen Normaltest oder ein allgemeiner 3D-Pass.

Der [einmalige Versuch](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/analysis.md)
ist inzwischen abgeschlossen. Beide Rootpruefungen bestehen; beide
Normaltests bleiben durch Aufweitung der Intervall-Polynomdivision schon
beim ersten Schur-Vergleich unentschieden. Die vorab festgelegten
schraegen/normalen Stoerungen wachsen stark im endlichen Fenster, die
getestete planare Stoerung klingt ab. Dies ersetzt das fehlende
asymptotische Zertifikat nicht. Keine automatische Wiederholung.

Auch ein spaeterer strikt
bestandener Normaltest waere ein lokaler Strukturbaustein, keine
Herleitung von Teilchen, einer Raumdimension oder der schwachen
Wechselwirkung. Paper-I-Baseline und bisherige FIFO-Claims bleiben bestehen.

## 6. Ein gezielter hinreichender Instabilitaetsbeleg

Nach dem endlichen Wachstumsbefund ist zunaechst eine echte wachsende
Normalmode von transienter Verstaerkung zu unterscheiden. Dafuer kann
eine elementare Vorzeichenpruefung ausreichen, ohne den gesamten
Formquotienten auszurechnen. Die folgende eigene Herleitung ist eine
Anwendung des Zwischenwertsatzes, kein beanspruchter neuer allgemeiner
Stabilitaetssatz. Sie wurde noch nicht am Anker ausgewertet.

Fuer den Normalblock aus Abschnitt 2 und reelles $x>0$ sei

$$
f(x)=\frac{p_H(x)}{x^{H-1}}
=x-1+\sum_{j=1}^{H-1}c_j(1-x^{-j}).
$$

Die Translationssymmetrie liefert exakt $f(1)=0$, nicht nur numerisch.
Weiter gilt

$$
S=f'(1)=p_H'(1)=1+\sum_{j=1}^{H-1}j c_j.
$$

**Hinreichendes Kriterium:** Falls $S<0$, hat $B_\perp$ mindestens
einen reellen Multiplikator $\lambda>1$.

**Beweis:** Aus $f(1)=0$ und $f'(1)<0$ folgt $f(x)<0$ fuer $x>1$
hinreichend nahe an eins. Fuer $x\to\infty$ gilt $f(x)\to\infty$.
Der Zwischenwertsatz liefert eine Nullstelle oberhalb eins. Explizit
genuegt als obere Vergleichsstelle $u=1+\sum_j|c_j|>1$, denn

$$
f(u)\geq u-1-\sum_j|c_j|(1-u^{-j})
=\sum_j|c_j|u^{-j}>0.
$$

Damit liegt mindestens eine reelle Nullstelle in $(1,u)$. Der zugehoerige
Companion-Eigenvektor hat Komponenten $v_j=\lambda^{-j}$. Am exakten
Kreisroot kann diese Mode nicht im bekannten Symmetrieraum liegen,
dessen Multiplikatoren nur $1,e^{\pm i\theta}$ sind. Es handelt sich
also um eine linear wachsende Formmode. Weder die genaue Wachstumsrate
noch Eindeutigkeit oder ein spaeterer nichtlinearer Attraktor sind damit
bewiesen.

**Gegenrichtung ungueltig:** $S\geq0$ schliesst Instabilitaet nicht aus.
Negative oder komplexe Aussenwurzeln sowie eine gerade Zahl positiver
Aussenwurzeln koennen dem Kriterium entgehen. Synthetische Gegenbeispiele
mit diesen drei Faellen verhindern eine falsche Stabilitaetsklassifikation.
Am Kreisroot gilt zudem exakt
$S=2(1-\cos\theta)q_{H-3}(1)$, was unabhaengig gegen die direkte
Polynomableitung kontrolliert wird.

Fuer einen Intervallbeleg muss die **obere** Grenze von
$1+\sum_j j[c_j]$ strikt negativ sein. Ein negativer Mittelpunkt
genuegt nicht. Die Koeffizienten muessen weiterhin den exakten
existenzzertifizierten Kreisroot einschliessen. Die neue arithmetische
Hilfsfunktion `normal_translation_slope` berechnet nur diese Summe;
sie ist kein eigenstaendiger physikalischer Zertifikatsrunner.
Der Vorteil ist eine lineare Summe ohne die wiederholte
Symmetrie-Polynomdivision. Ein nicht-negatives oder null einschliessendes
Ergebnis bleibt fuer die Instabilitaetsfrage unentschieden.

### Literatur und Abgrenzung

Geprueft am 2026-10-26:

- [Trefethen et al., Hydrodynamic Stability Without Eigenvalues, Science 261 (1993), 578-584](https://people.maths.ox.ac.uk/trefethen/publication/PDF/1993_57.pdf),
  Abstract und Einleitung, Druckseite 578: starke transiente Verstaerkung
  kann trotz abklingender Eigenmoden auftreten. Das begruendet die Trennung
  von Kurvenwachstum und Spektralbeleg; es ist kein Ergebnis ueber FIFO.
- [Rump, Verified Error Bounds for All Eigenvalues and Eigenvectors of a Matrix](https://www.tuhh.de/ti3/paper/rump/Ru22a.pdf),
  Autorenmanuskript, Abstract, Einleitung und Satz 2.1, PDF-Seiten 1-3:
  verifizierte Eigenpaar- bzw. Invariantenraum-Einschliessungen sind eine
  bekannte allgemeinere Route. Sie werden hier nicht implementiert oder
  reproduziert. Ein gescheiterter Einschluss ist kein Stabilitaetsbefund.

Die Vorzeichenroute soll zunaechst an synthetischen Faellen geprueft
werden; diese Pruefung ist inzwischen erfolgt: 20 neue exakte bzw.
Intervallkontrollen bestehen, insgesamt 270 betroffene Regressionstests.
Ein Ankertest waere ein eigener begrenzter Beleg anhand der schon
gespeicherten Koeffizientenintervalle, ohne neue Trajektorien oder
Parametersuche. Die bisherigen Versuchsfreigaben werden dafuer nicht
wiederverwendet.

Die gespeicherten binaeren Endpunkte lassen sich als exakte rationale
Zahlen lesen. Da nur ganzzahlige Gewichte und Summen vorkommen, kann
dieser spaetere Archivtest ohne weitere Rundung erfolgen. Das wuerde
die Vertrauensbasis der urspruenglichen Root- und Koeffizientenintervalle
nicht ersetzen, aber neue Summationsrundung vermeiden. Die Hilfe und
synthetischen Tests enthalten keinen solchen Ankeraufruf.
