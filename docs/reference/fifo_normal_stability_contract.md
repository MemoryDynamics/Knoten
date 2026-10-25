# FIFO-Normalstabilitaet: Methodenvertrag

Stand: 2026-10-25. Aufbauend auf der
[Strukturauswahl](fifo_structure_candidate.md), Ausgangsrevision `6a5b76d`.
Analytische Reduktion und synthetischer Prototyp, **kein Zielbefund und
noch kein ausfuehrungsreifes Messprotokoll**. Die Arbeitsreihenfolge steht
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

Lokale Verifikation: 66 Tests in `tests/test_fifo_normal_stability.py`
bestanden; zusammen mit den betroffenen Intervall-, Struktur- und
Dokumentationsregressionen 150 bestanden. Verwendet wurden Python 3.12.14,
mpmath 1.3.0, NumPy 2.3.5, SciPy 1.16.3 und pytest 8.4.2. Die kleinen
Kontrollen ersetzen weder ein unabhaengiges Fachreview noch die fehlende
Rootbox-Anbindung.

## 5. Fehlende Bindung an einen konkreten Kandidaten

Vor einer Zielauswertung fehlen folgende Bestandteile eines begrenzten,
vorab festzulegenden Ausfuehrungsvertrags:

- **Root und Herkunft:** Ein fest ausgewaehlter existenzzertifizierter
  endlicher Kreisroot mit Revision, exakten Parametern und Rootbox. Nicht
  nach Sichtung von Normalbefunden den guenstigsten Kandidaten auswaehlen.
  Das separate unendliche G4-Zertifikat ersetzt diese finite-H-Bindung nicht.
- **Verifizierte Abbildung:** Die Rootbox muss alle exakten $c_j$, den
  Symmetriefaktor und die Quotientenkoeffizienten einschliessen. Der
  Adapter vom vorhandenen Rootzertifikat zum neuen Polynomtest ist noch
  nicht implementiert. In der bestehenden Intervallbalance ist die erste
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

Bis dahin ist nur die Methode vorbereitet. Auch ein spaeterer strikt
bestandener Normaltest waere ein lokaler Strukturbaustein, keine
Herleitung von Teilchen, einer Raumdimension oder der schwachen
Wechselwirkung. Paper-I-Baseline und bisherige FIFO-Claims bleiben bestehen.
