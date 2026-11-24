# Statische Fernwirkung am kritischen FIFO-Mittelfeld

Stand: 2026-11-21. Analytische Referenz, kein neuer Vielknoten-Runner,
kein Ziellauf und keine Aenderung der nativen Einzel-/Paar-Implementierung.

**Ergebnis.** Ein homogenes Dichte-Mittelfeld mit endlichem FIFO und
rein attraktivem Gausskernel besitzt an einer expliziten Schwelle
eine statische $1/r$-Antwort in vorgegebenem 3D. Alle Nichtnullmoden
sind dort im linearen Mittelfeld strikt stabil, aber die langsamste
Mode relaxiert mit einer Rate proportional zu $k^4$, nicht als Welle.
Die Fernwirkung entsteht durch kollektive Rueckkopplung, nicht durch
eine einzelne Gaussquelle oder einen eingesetzten Poisson-Operator.
Kritikalitaet und Dichteabschluss sind Voraussetzungen, keine
aus den Knoten nachgewiesenen dynamischen Eigenschaften.

Die [anschliessende Fluktuationspruefung](critical_fifo_fluctuations_2026-11-21.md)
bestimmt die exakte bedingte Dichteinnovation und einen nichtlinearen
Skalenindikator. Sie kontrolliert nicht den Fortbestand der Fernantwort
im kritischen nichtlinearen Vielteilchen-Grenzfall.
Die [nichtlineare stationaere Schalenbilanz](critical_fifo_stationary_tail_2026-11-21.md)
schliesst inzwischen das hier linear vorhergesagte isotrope 1/r-Profil
im exakten deterministischen Dichteupdate aus. Der lineare Transferpol
bleibt erhalten, aber nicht seine uniforme Uebertragung auf feste Quellen.

Der [Horizontvergleich](collective_fifo_horizon_response_2026-11-22.md)
zeigt zudem: Auch fuer unbeschraenkte Altershorizonte kann keine
nichtnegative Gewichtsverteilung den kollektiven Aufbau gegenueber
H=1 beschleunigen. Die akustische Frequenzschranke bleibt bei
beschraenkter absoluter Gewichtssumme auch fuer signierte Filter erhalten.

## 1. Vergleichsmodell und exakte erste Variation

Der [Paarcode](../../src/emergenz_knoten/reciprocal_nodes.py) liest beide
alten Historien synchron. Eine additive N-Verallgemeinerung ist im
[kollektiven Audit](collective_memory_stability_2026-11-07.md) bereits
als Vergleich, nicht als Produktionsregel definiert. Hier wird eine
homogene, deterministische Dichtebeschreibung dieser Architektur
betrachtet. Konkret wird die zufaellige empirische Vergangenheit
durch ihre Dichten zu den gespeicherten Zeiten ersetzt. Dies ist
ein **deklarierter Mittelfeldabschluss**, kein Beweis eines
Vielteilchen- oder thermodynamischen Grenzwerts bei kritischer Kopplung.

Sei $\rho_n$ die momentane Dichte, $w_a\geq0$ die festen gefuellten
FIFO-Gewichte, $W=\sum_{a=0}^{H-1}w_a>0$. Die externe Testquelle $s_n$
ist in denselben Einheiten wie die gewichtete Dichte. Eine statische
lokalisierte Quelle wird als vorgegebene, festgehaltene Anregung gelesen;
ihre Bildung und Rueckwirkung auf einen eigenen Traeger werden nicht
modelliert. Definiere Potential, Kopftransport und Dichteupdate durch

$$
U_n=K*\Bigl(s_n+\sum_{a=0}^{H-1}w_a\rho_{n-a}\Bigr),\qquad
T_n(x)=x-\eta\nabla U_n(x),\qquad
\rho_{n+1}=G_\varepsilon*(T_n)_\#\rho_n.
$$

Hier ist $G_\varepsilon$ der normierte Gauss der unabhaengigen
additiven Ortsinnovation mit Varianz $\varepsilon^2 I$ pro Update.
Die Faltung nach dem Pushforward entspricht genau der Reihenfolge
des Head-Updates im angegebenen Dichtevergleich. Der Abschluss
kann zunaechst periodisch formuliert werden. Die Fourier-Analyse auf
unendlichem Raum ist die formale homogene Mittelfeldbeschreibung,
nicht der Nachweis ihrer Gueltigkeit an endlichem N.

Um $\rho_n=\rho_0$ konstant, $s_n=0$ und daher $\nabla U_n=0$, ist die
erste Pushforward-Variation $u_n+\eta\rho_0\Delta U_n$.
Mit $u_n(k)=\delta\widehat\rho_n(k)$, $k=|\mathbf k|$, $d_0=\varepsilon^2/2$
und $p(k)=e^{-d_0 k^2}$ folgt fuer jede Mode:

$$
u_{n+1}=p(k)\left[u_n-\eta\rho_0 k^2\widehat K(k)
\left(\widehat s_n+\sum_a w_au_{n-a}\right)\right].
$$

Der Faktor $k^2$ folgt aus Massentransport, nicht aus einem
vermuteten Feldgesetz. Der Nullmodus ist durch die Dichtemasse fixiert;
eine konstante zusaetzliche Potentialkomponente aendert keinen Transport.
Der gesamte FIFO, einschliesslich seiner letzten Ablage, bleibt in der
Gleichung erhalten.

## 2. Kollektive Antwort und Schwelle

Schreibe $P(z)=\sum_a w_a z^{-a}/W$ und $b(k)=\eta\rho_0W\widehat K(k)$.
Elimination der Dichtevariation bei zeitlicher Modenform $z^n$ ergibt
fuer die **gesamte gelesene Potentialantwort** auf die vorgegebene
Quelle (direkter plus induzierter Anteil)

$$
\frac{\widehat U}{\widehat s}
=\widehat K(k)\,\frac{z-p(k)}{z-p(k)+p(k)k^2 b(k)P(z)}.
$$

Fuer statische Antwort auf eine Nichtnullmode gilt $z=1$ und $P(1)=1$.
Das statische Ergebnis haengt nur von der gesamten Lesestaerke W ab,
nicht von ihrer Altersverteilung. Die dynamische Antwort haengt
dagegen vom vollen Filter $P(z)$ ab.

Setze jetzt $\widehat K(k)=-K_0 e^{-a k^2}$ mit $K_0,a>0$, also
ein rein attraktiver effektiver Gausskernel, $d_0>0$ und
$A=\eta\rho_0W K_0\ge0$. Die statische Nennerfunktion ist

$$
\mathcal D(k)=1-p(k)\bigl[1+A k^2e^{-a k^2}\bigr].
$$

Fuer $A\le d_0$ ist die Klammer mal p fuer jedes $k>0$ strikt kleiner
als 1, da $1+d_0 k^2<e^{d_0k^2}$. Die ungetriebene History-Rekursion
hat nichtnegative Kopfkoeffizienten, deren Summe genau dieser Ausdruck
ist. Liegt eine Wurzel $|z|\ge1$ vor, so ergaebe die Kopfgleichung
$|z|\le p(1+A k^2e^{-a k^2})<1$, ein Widerspruch. Damit sind **alle**
Nichtnullmoden des linearen Dichtevergleichs stabil, nicht nur kleine k.
Fuer $A>d_0$ ist fuer hinreichend kleine k die Kopfsumme groesser
als 1; die reelle charakteristische Funktion ist bei $z=1$ negativ
und bei grossem z positiv. Im unendlichen Vergleich existieren dann
wachsende Moden; eine endliche Box muss diese Wellenzahlen erst enthalten.

Unterhalb der Schwelle ist der statische Transfer regulaer bei null,
mit Grenzwert $-K_0d_0/(d_0-A)$. **Exakt bei $A=d_0$** ist

$$
D_4=d_0a+\frac{d_0^2}{2}>0,\qquad
\mathcal D(k)=D_4 k^4+O(k^6),\qquad
\frac{\widehat U}{\widehat s}(k,1)
=-\frac{K_0 d_0}{D_4 k^2}+O(1).
$$

Im unendlichen 3D-Raum und mit Invers-Fouriermass $d^3k/(2\pi)^3$
hat der statische Antwortkernel daher den Schwanz
$-K_0d_0/(4\pi D_4 r)$. Fuer den reinen Gaussfall kann man dazu den
Pol mit einem Faktor $e^{-a k^2}$ abziehen: Der Rest ist glatt am
Ursprung und rasch fallend samt Ableitungen; der abgeschnittene Pol
hat denselben $1/r$-Koeffizienten. Eine glatte lokalisierte Testquelle
mit verschwindendem Gesamtintegral hat diesen Monopolanteil nicht.
Die Aussage ist eine **lineare statische** Fernantwort pro vorgegebener
Quellstaerke. Die induzierte Dichtestoerung hat selbst einen $1/r$-
Schwanz und ist nicht global integrierbar. Ein festes endliches
Massensystem braucht Rand- bzw. Kompensationsbilanz; die stationaere
unendliche Antwort ist nicht der gleichmaessige Grenzwert endlicher Zeiten.

## 3. Der entscheidende Zeit- und Kontrolltest

Bei $k=0$ besitzt die volle H-dimensionale History-Matrix eine einfache
Wurzel $z=1$ und $H-1$ Nullwurzeln. Der Zweig bei 1 ist fuer kleine k
reell und analytisch in $k^2$. Am kritischen Punkt folgt durch Einsetzen
in die charakteristische Gleichung

$$
z(k)=1-D_4 k^4+O(k^6).
$$

Der Beitrag von $P(z)-1$ beginnt hier erst bei Ordnung $k^6$,
weil er mit $k^2$ multipliziert wird. Keine zweite Wurzel naehert sich
1; dieser Kanal liefert bei festem endlichem H **kein** Paar
ballistischer Moden $z=1\pm i c k+O(k^2)$. Die charakteristische
Relaxationszeit skaliert wie $k^{-4}/D_4$ in Updates.

Dies trennt den statischen Grenzwert vom Aufbau: Beginne mit
unperturbierter Historie und schalte eine konstante Testquelle ein.
Am kritischen Punkt ist die Kopfsumme kleiner als 1. Daher gilt nach
n Updates komponentenweise $|u_n|\le n p\eta\rho_0 k^2
|\widehat K\widehat s|$. Fuer jedes feste n hat das Antwortsymbol
somit **keinen** $1/k^2$-Pol. Der Fernschwanz benoetigt den spaeten
Zeitzustand bei jeder Wellenzahl separat. Die Gausskicks und der
direkte Gaussreadout definieren auch keinen harten Signalkegel.

**Entscheidender Gegenvergleich:** H=1 bei gleichem W liefert dieselbe
Schwelle, denselben statischen Pol und denselben fuehrenden $k^4$-Term.
Der Pol ist hier ein kollektiver Kritikalitaetseffekt, kein spezifischer
Nachweis eines nicht-Markovschen Mechanismus. Die erste spezifische
Abweichung laesst sich getrennt vorhersagen. Mit dem gewichteten
mittleren Alter $\bar\ell=\sum_a a w_a/W$ gilt

$$
P(z)=1-\bar\ell(z-1)+O((z-1)^2),\qquad
z_H(k)-z_1(k)=d_0\bar\ell D_4 k^6+O(k^8).
$$

Dazu zieht man die exakte H=1-Gleichung
$z_1=p(1+d_0 k^2e^{-a k^2})$ vom kritischen H-Zweig ab. Der Rest ist
$p d_0 k^2 e^{-a k^2}[P(z_H)-1]$. Fuer positive alte Gewichte ist
der Beitrag positiv: Die schon langsame Langwellenmode relaxiert
etwas langsamer. Das ist der beschraenkte FIFO-Diskriminator, nicht
der statische Pol. $H$ und alle Gewichte bleiben in der Entwicklung fest.

## 4. Einordnung und Verifikation

[Chavanis, arXiv:1306.1225, Abschnitt VI A](https://arxiv.org/abs/1306.1225)
leitet die kontinuierliche Smoluchowski-Dielektrik schon ohne FIFO her
(Volltext, insbesondere Gl. 109-114). Das ist der enge methodische
Vorlaeufer fuer den Rueckkopplungsnenner und fuer den H=1-Vergleich.
Das hier gezeigte Ergebnis ist die diskrete endliche FIFO-Bilanz,
nicht die Neuentdeckung kollektiver Suszeptibilitaet.
[Chavanis, arXiv:0803.0263, Abschnitt 2.1](https://arxiv.org/abs/0803.0263)
diskutiert im Brownian-Vergleich die fehlende gleichmaessige
Mittelfeldkontrolle nahe der Instabilitaetsschwelle. Das ist ein
Warnsignal fuer einen noetigen separaten Fluktuationstest, kein
Uebertrag seines konkreten kritischen Exponenten auf unsere Regel.
Gezielter Primaerquellenabgleich, kein systematischer Review.

Die [festen Kontrollen](../../tests/test_collective_fifo_screening.py)
vergleichen die reduzierte Antwort mit dem Resolventen des vollen FIFO,
pruefen den kritischen Pol, die Zeitrate und den ersten FIFO-Korrekturterm
gegen H=1 und kontrollieren die erste Variation durch direkte
Pushforward-Fourierquadratur. Keine Parametersuche oder Zielauswertung.
Verifikation: 93 Tests im gezielten Panel bestanden, darunter 13 neue
Kontrollen. Ausserdem geprueft wurden kollektive lineare Stabilitaet,
Fernfeldinventar, Paartransfer und Markdown-Formeln. Keine volle Suite.

Die statische Analogie ist **keine Gravitation**: Es fehlen eine
dynamisch begruendete Wahl der Schwelle, der kontrollierte kollektive
Grenzwert, ein universeller Quellen-/Arbeitsport und die relativistische
Tensor-/Propagationsstruktur. Der analytische Vergleich ersetzt weder
die offene 3D-Traegerstabilitaet noch den Quantenanschluss.
