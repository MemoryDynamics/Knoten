# Nichtlineare Grenze des statischen Fernprofils

Stand: 2026-11-21. Fortsetzung der [kritischen linearen Fernantwort](collective_fifo_screening_2026-11-21.md)
und der [Fluktuationspruefung](critical_fifo_fluctuations_2026-11-21.md).
Keine neue Modellregel, kein Vielteilchen-Ziellauf und keine Aenderung
am offenen 3D-Stabilitaetsauftrag.

**Resultat.** Im exakt kritischen, deterministischen nichtlinearen
Dichtevergleich auf R3 ist das linear vorhergesagte stationaere
Dichtefernprofil $C/r$ fuer $C\ne0$ unmoeglich. Das gilt fuer beide
Vorzeichen. Der lineare statische Transferpol selbst bleibt korrekt;
er ist keine uniforme Aussage ueber eine feste nichtverschwindende
Quelle bei $r\to\infty$. Ein angenommenes isotropes $1/r^2$-Profil
koennte die fuehrende Bilanz nur mit einem Dichtedefizit erfuellen.
Die Existenz eines solchen Profils wird nicht behauptet.

## 1. Annahmen und exakte schwache Bilanz

Bezeichne mit $G_t(x)=(4\pi t)^{-3/2}\exp(-|x|^2/(4t))$ die
Gaussdichte des Waermeoperators $S_t f=G_t*f$, fuer feste $t>0$.
Die relative Dichte lautet $\rho/\rho_0=1+u$ mit $u$ beschraenkt,
$1+u\ge0$, $\rho_0>0$. Am stationaeren Punkt sind alle FIFO-Alter
gleich; die Gewichtung reduziert sich exakt auf ihre Summe W.
Der attraktive Kernel hat die Fourierform $-K_0e^{-a k^2}$.
Bei der kritischen Gleichheit $\eta\rho_0W K_0=d_0>0$ ist die
Verschiebung

$$
b(x)=d_0\nabla S_a u(x)+b_{\rm ext}(x).
$$

Eine kompakt getragene endliche externe Quelle wird mit demselben
Gausskernel gelesen. Daher ist ihre Verschiebung $b_{\rm ext}$
beschraenkt und faellt schneller als jede Potenz ab. Keine Radialsymmetrie
der Quelle oder der endlichen Dichte wird vorausgesetzt.
Das exakte Update ist Pushforward durch $x\mapsto x+b(x)$ und dann
Faltung mit $G_{d_0}$, nicht eine stationaere PDE fuer u.

Waehle eine nichtnullige, nichtnegative glatte Testfunktion $\phi$
mit kompaktem Traeger in $1<|x|<2$. Sei $\phi_R(x)=\phi(x/R)$,
$\psi_R=S_{d_0}\phi_R$. Schwache Stationaritaet verlangt fuer jede
solche Schale

$$
I_R=\int (1+u(x))[\psi_R(x+b(x))-\phi_R(x)]\,dx=0.
$$

Diese Form gilt ohne Umkehrbarkeit der Transportabbildung und
ohne globale Integrierbarkeit von u. Die gewichteten Integrale
sind endlich. Untersucht werden gleichmaessige Dichteschwaenze
$u(x)=C|x|^{-p}+o(|x|^{-p})$ fuer $p=1$ oder $p=2$,
gleichmaessig in der Richtung. Es werden **keine** Ableitungen
dieser Asymptotik vorausgesetzt.

## 2. Welcher Term in der Schale uebrigbleibt

Auf $R/2<|x|<3R$ gilt $u=O(R^{-p})$ und $b=o(R^{-p})$.
Fuer die zweite Aussage zerlege u in den glatten Vergleich
$C(1+|x|^2)^{-p/2}$ und einen Rest $o(|x|^{-p})$. Der Gradient der
Gaussfaltung des Vergleichs ist $O(R^{-p-1})$; der Rest liefert
wegen des integrierbaren Ableitungskernels $o(R^{-p})$.
Die Beitraege weit ausserhalb der erweiterten Schale sind wegen
Gaussabfall und global beschraenktem b schneller fallend als jede
Potenz von R. Dasselbe gilt fuer die lokalisierte externe Quelle.

Taylorentwicklung **nur der Testfunktion** in b liefert einen
Rest $o(R^{1-2p})$: Die Hesse-Norm ist $O(R^{-2})$, die Schale
hat Volumen $O(R^3)$ und $|b|^2=o(R^{-2p})$. Weiter gilt
$\int(\psi_R-\phi_R)=0$. Nach partieller Integration im linearen
Driftanteil erhaelt man mit Symmetrie der Waermefaltung

$$
I_R=\int u(S_{d_0}-I-d_0\Delta S_{a+d_0})\phi_R
+d_0\int u\,\nabla S_a u\cdot\nabla\psi_R+o(R^{1-2p}).
$$

Im ersten Integral heben sich beide Terme der Ordnung $\Delta$
exakt auf. Der erste verbleibende Operator ist
$-D_4\Delta^2$ mit $D_4=d_0a+d_0^2/2>0$.
Der Rest auf der Schale ist $O(R^{-6})$ in Supremumsnorm, durch
die Waermeentwicklung an der glatten skalierten Testfunktion.
Ausserhalb ist er wieder gaussklein. Damit ist

$$
\int u(S_{d_0}-I-d_0\Delta S_{a+d_0})\phi_R
=-D_4 C R^{-1-p}\int |y|^{-p}\Delta^2\phi(y)\,dy
+o(R^{-1-p}).
$$

Fuer den zweiten Term ist es wichtig, keinen Gradienten des
angenommenen Dichteschwanzes abzuleiten. Stattdessen liefert die
Ungeradheit von $\nabla G_a$ die exakte Symmetrisierung

$$
\int u\,\nabla S_a u\cdot\nabla\psi_R
=\tfrac12\iint u(x)u(x-h)\nabla G_a(h)\cdot
[\nabla\psi_R(x)-\nabla\psi_R(x-h)]\,dh\,dx.
$$

Setze $x=Ry$. Fuer festes h geht die mit $R^2$ multiplizierte
Gradientendifferenz gegen $D^2\phi(y)h$. Auf der erweiterten
Schale sind fuer $|h|\le R/4$ beide skalierten Dichten $R^p u$
gleichmaessig beschraenkt; hier liegt $|x-h|$ stets zwischen
$R/4$ und $13R/4$. Die skalierte Gradientendifferenz ist durch
eine Konstante mal $|h|$ beschraenkt. Groessere h tragen wegen
der Gaussableitung und der endlichen L1-Norm des Testgradienten
nur einen exponentiellen Rest bei. Ausserhalb der erweiterten
Schale bei $|h|\le R/4$ sind beide Testgradienten durch
Gaussabfall lokalisiert. Dominierte Konvergenz und
$\int h_j\partial_i G_a(h)\,dh=-\delta_{ij}$ geben

$$
\int u\,\nabla S_a u\cdot\nabla\psi_R
=-\tfrac12 C^2 R^{1-2p}\int |y|^{-2p}\Delta\phi(y)\,dy
+o(R^{1-2p}).
$$

Diese beiden Formeln testen den **exakten** stationaeren Schritt,
nicht die Stationaritaet einer angenaeherten lokalen Feldgleichung.

## 3. Ausschluss und verbleibender Kandidat

Fuer $p=1$ ist der lineare Beitrag hoechstens $O(R^{-2})$,
waehrend nach partieller Integration auf der Schale gilt

$$
\lim_{R\to\infty} R I_R
=-d_0C^2\int |y|^{-4}\phi(y)\,dy<0\quad(C\ne0).
$$

Dabei wurde $\Delta |y|^{-2}=2|y|^{-4}$ in R3 benutzt.
Das widerspricht $I_R=0$. Eine lokalisierte Quelle kann
den Rest in beliebig weit entfernten Schalen nicht kompensieren.
Auch eine noch so kleine feste Amplitude C aendert sein Vorzeichen
nicht. Der Befund trennt die Ableitung der Antwort bei Quelle null
von einem exakten stationaeren Schwanz bei fester Quelle.

Bei $p=2$ tragen beide Terme auf Ordnung $R^{-3}$ bei. Weil
$\Delta^2 |y|^{-2}=24|y|^{-6}$ und $\Delta |y|^{-4}=12|y|^{-6}$,
verlangt schwache Stationaritaet

$$
\lim_{R\to\infty} R^3 I_R
=-(24D_4 C+6d_0C^2)\int |y|^{-6}\phi(y)\,dy=0.
$$

Also muss fuer ein nichtnulliges isotropes $1/r^2$-Profil
$C=-4D_4/d_0<0$ gelten. Das ist eine notwendige Schalenbilanz,
keine Existenz-, Auswahl- oder Stabilitaetsaussage. Das linear
vorhergesagte gemeinsame $1/r$-Dichte- und Potentialprofil ist
dagegen ausgeschlossen: Bei diesem Dichteansatz wuerde die
Gaussfaltung denselben fuehrenden Potenzschwanz haben.
Nicht erfasst sind nichtisotrope fuehrende Profile, Zeitabhaengigkeit,
endliche Boxen und die stochastische Vielteilchendynamik.
Keine Aussage ueber Gravitation allgemein.

### Das geglaettete Potential

Der Ausschluss laesst sich auf das Potential unter einer zusaetzlichen,
schwaecheren Dichteannahme uebertragen. Angenommen, $u=O(r^{-p})$ und
$S_a u=C/r^p+o(r^{-p})$, uniform in der Richtung. Der lokalisierte
Quellterm hat keinen Potenzschwanz. Fuer eine beliebige Folge
$x_m$ mit $R_m=|x_m|\to\infty$ ist
$v_m(y)=R_m^p u(x_m+y)$ auf $|y|\le R_m/2$ uniform beschraenkt.
Ausserhalb dieser Kugel genuegt $|v_m|\le R_m^p\|u\|_\infty$,
denn feste Gausskerne unterdruecken diesen Teil exponentiell.

Die verschobene geglaettete Dichte $S_a v_m$ konvergiert lokal
gleichmaessig gegen C. Auch ihre Hesse-Norm ist lokal uniform
beschraenkt, durch Faltung mit dem zweiten Ableitungskernel.
Differenzenquotienten mit erst festem, dann gegen null gehendem
Abstand ergeben $R_m^p b(x_m)\to0$. Somit ist $b=o(r^{-p})$.
Die exakte stationaere Dichte besitzt als Faltung des Pushforward
eine glatte Repraesentantin; auf diese beziehen sich Punktwerte.
Vergleicht man ihre Gaussintegrale mit und ohne b, liefert
der Mittelwertsatz fuer den Gausskern $u=S_{d_0}u+o(r^{-p})$:
Fuer $|y-x|\le |x|/2$ ist b gleichmaessig klein, und der Rest
ist wegen der beschraenkten Verschiebung gaussklein.

Jede schwach-* konvergente Teilfolge der auf $|y|\le R_m/2$
trunkierten $v_m$ besitzt daher einen beschraenkten Grenzwert v
mit $S_a v=C$. Die Gaussfaltung ist auf beschraenkten Funktionen
injektiv: Der Fouriermultiplikator ist nirgends null (lokal
in Frequenz darf gegen Testfunktionen durch ihn dividiert werden).
Damit ist v konstant C und $(S_{d_0}v_m)(0)\to C$ fuer jede
Teilfolge. Die stationaere Dichtegleichung liefert
$R_m^p u(x_m)\to C$. Da $x_m$ beliebig war, gilt dieselbe
gleichmaessige Asymptotik fuer u. Insbesondere ist ein isotropes
$1/r$-Potential mit $C\ne0$ auch dann ausgeschlossen, wenn
fuer die Dichte nur $u=O(1/r)$, nicht ihr fuehrender Koeffizient,
vorausgesetzt wird. Ein langsamerer oder nicht abklingender
Dichteanteil ist nicht von diesem Schluss erfasst.

## 4. Quellen und unabhaengige Kontrollen

[Carrillo, Hittmeir, Volzone und Yao, Invent. Math. 218 (2019)](https://arxiv.org/abs/1603.07767),
Definition 2.1 und Satz 2.2 im geprueften Volltext, behandeln
schwache stationaere Zustaende fuer eine kontinuierliche
Aggregation-Diffusions-PDE und endliche Gesamtmasse. Ihre
Radialsymmetrie- und Existenzresultate werden nicht auf den
vorliegenden diskreten Hintergrund mit positiver homogener
Dichte uebertragen. [Chavanis, arXiv:1306.1225, Abschnitt VI A](https://arxiv.org/abs/1306.1225)
ist der bereits gepruefte kontinuierliche Vergleich fuer den
linearen Rueckkopplungsnenner. Die obige Schalenrechnung ist eine
direkte Ableitung der diskreten Pushforward-Regel.

Die [festen Gegenkontrollen](../../tests/test_critical_fifo_stationary_tail.py)
berechnen den vollen radialen Pushforward-Test fuer glatte
synthetische Profile, ohne stationaere Loesung oder Teilchenbahn
zu erzeugen. Unabhaengige radiale Gauss- und Schalenquadraturen
kontrollieren Vorzeichen, die $1/r^2$-Kompensation und ihren
endlichen Rest. Der allgemeine Ausschluss folgt aus der schwachen
Bilanz, nicht aus der numerischen Quadratur.

Verifikation: 103 Tests im gezielten Panel bestanden, davon sechs
neue Schalenkontrollen. Das Panel enthaelt ferner den linearen
Fernfeldvergleich, den Fluktuationsabgleich, die kollektive
Stabilitaet, das Fernfeldinventar und Markdown-Formelkontrollen.
Keine volle Repository-Testsuite.
