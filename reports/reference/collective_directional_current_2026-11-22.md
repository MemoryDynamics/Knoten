# Ein kritischer Richtungsstrom liefert Wellen, aber nicht den statischen Pol

Stand: 2026-11-22. Analytischer, deklarierter gemeinsamer
Dichte-/Richtungsabschluss. Die Ein-Schritt-Regel und das Schreiben
der normierten Schrittvektoren stammen aus dem Repository, die
gemeinsame deterministische Dichte ist eine Vergleichsannahme.
Keine neue native Zieltrajektorie und keine Parametersuche.

**Ergebnis.** Im isotropen Zustand ist der mittlere Richtungsstrom
normalerweise relaxierend. Bei exakt kritischer Alignment-Staerke
liefert er neben der Dichte eine zweite langsame Variable. Daraus
entstehen lineare Wellenzweige; ein fester Zweialter-Vergleich
liefert gedaempfte Wellen bei langen Wellenlaengen. Aber am selben
skalaren Quell-/Leseport verschwindet dabei der statische
$1/k^2$-Pol. Erzwingt man dort stattdessen wieder einen statischen
Pol, geht die lineare Wellengeschwindigkeit auf null.

## 1. Uebernommene Regel und gesetzter Abschluss

Die [native Alignment-Regel](../../src/emergenz_knoten/vector_memory.py)
addiert zum skalaren und zufaelligen Schritt ein gelesenes
Vektorfeld. Geschrieben wird die normierte **realisierte**
Verschiebung am **neuen Ort**. Wir betrachten genau diesen
Schreibzeitpunkt, nicht die separat implementierte passive
Orientierungsfaser. Der Abschluss ersetzt die empirischen
Deposits durch ihre gemeinsamen ortsabhaengigen Dichten.
Eine Propagation-of-Chaos-Aussage oder universelle lokale
Stromerhaltung wird nicht vorausgesetzt.

Seien $\epsilon Z$ isotrope 3D-Gaussinnovationen, $Z\sim N(0,I)$,
$\epsilon>0$, und $d$ die mittlere Schrittverschiebung.
In relativen Dichte-Einheiten lauten die Aktualisierungen
fuer die Ortsdichte und die am neuen Ort geschriebene
Richtungsdichte als Erwartungswerte des Transports $x\mapsto
x+d(x)+\epsilon Z$. Die zweite Auslese traegt dabei die
Markierung $(d+\epsilon Z)/|d+\epsilon Z|$.

Bei homogener Dichte $\rho_0$ sei $g_0$ der gesamte
Vektor-Lesefaktor: Gain mal $\rho_0$, mal Gewichtssumme
und Integral des Gausskernels. Fuer einen konstanten
kleinen Drift ist die Richtungs-Suszeptibilitaet

$$
\left.D_d\mathbb E\frac{d+\epsilon Z}{|d+\epsilon Z|}
\right|_{d=0}=\chi I,\qquad
\chi=\frac{\mathbb E|Z|}{3\epsilon}
    =\frac{2\sqrt{2/\pi}}{3\epsilon}.
$$

Das folgt durch Ableiten der verschobenen Gaussdichte,
die Ableitung liefert $Z/\epsilon$, und durch Isotropie.
An der homogenen Nullmode hat das Richtungsfenster daher
die charakteristische Gleichung $z=g_0\chi P_v(z)$, mit
$P_v(z)=\sum_j \omega_j z^{-j}$, $\omega_j\ge0$,
$\sum_j\omega_j=1$, und endlichem Fenster. Fuer
$0\le g_0\chi<1$ liegen alle Richtungswurzeln strikt
innerhalb des Einheitskreises. Bei $g_0\chi=1$ ist
$z=1$ eine einfache Wurzel pro Komponente (Ableitung
$1+\bar j_v$). Ist $\omega_0>0$, kann keine weitere
Richtungswurzel auf dem Einheitskreis liegen: Gleichheit
in der Dreiecksungleichung verlangt gleichphasige Terme
und insbesondere Phase null relativ zu $z$ fuer den
Term $j=0$. Bei $g_0\chi>1$ existiert eine reelle
Wurzel groesser als eins. Das ist eine gerichtete
Ordnungsinstabilitaet, keine mechanische Impulserhaltung.

## 2. Langwellenblock und der endliche Wellenzweig

Sei k die Wellenzahl in Richtung $e_1$. Bezeichne mit u
die normierte Ortsdichtevariation und mit m die
longitudinale Richtungsdichte. Setze

$$
p=e^{-\epsilon^2k^2/2},\quad
B(k)=\mathbb E[\hat Z_1\sin(k\epsilon Z_1)],\quad
T(k)=\epsilon^{-1}\mathbb E[\hat Z_1 Z_1\cos(k\epsilon Z_1)].
$$

Hier ist $\hat Z=Z/|Z|$. Der Faktor $B(k)$ stammt aus dem
Schreiben **nach** der Bewegung; ohne diese Korrelation
von Ort und Richtung waere die Wellengleichung eine andere.
Fuer eine zeitliche Mode $z^n$ und longitudinalen Drift d
liefert die erste Variation exakt

$$
zu=p(u-ikd),\qquad zm=-iB(k)u+T(k)d,\qquad
d=g(k)P_v(z)m-ik b_s(k)P_s(z)u.
$$

$g(k)=g_0 e^{-\sigma_v^2 k^2/2}$ ist der Vektorport,
$b_s(k)$ der gesamte skalare Lesefaktor inklusive
Kernelvorzeichen; $b_s=b_s(0)$ und $P_s(1)=1$.
Die beiden Gauss-Erwartungen sind analytisch mit
$T(k)=\chi+O(k^2)$ und $B(k)=\epsilon^2\chi k+O(k^3)$.

Bei $g_0\chi=1$ setzt man $z=1+k\lambda$ in den
Determinanten des 2-mal-2-Blocks ein. Nach Division
durch $k^2$ ist die fuehrende Gleichung

$$
(1+\bar j_v)\lambda^2+\epsilon^2+b_s=0.
$$

Bei $\epsilon^2+b_s>0$ hat sie zwei einfache
Nullstellen $\lambda=\pm i v$ mit
$v^2=(\epsilon^2+b_s)/(1+\bar j_v)$. Die analytische
Fortsetzung liefert $z_\pm=1\pm i v k+O(k^2)$.
Beide Zweige haben einen nichtverschwindenden Orts-
und Richtungsanteil. Bei $\epsilon^2+b_s<0$ ist
ein Zweig bereits in Ordnung k instabil. Bei
$\epsilon^2+b_s=0$ bleibt kein von null verschiedener
linearer Wellenspeed.

**Kontrolle der Daempfung.** Fuer einen skalaren Sofortleser
und zwei Vektoralter $(2/3,1/3)$ waehle den alten skalaren
kritischen Wert $b_s=-\epsilon^2/2$. Dann ist
$v^2=3\epsilon^2/8$. Aus den radialen und winkeligen
Gaussmomenten folgt
$T(k)/\chi=1-(6/5)\epsilon^2k^2+O(k^4)$.
Definiere $D_v=\sigma_v^2/2+(6/5)\epsilon^2$.
Mit $\zeta=\log z$ liefert der Determinant bis
Gesamtgrad drei

$$
\tfrac43\zeta^2+\tfrac{\epsilon^2}{2}k^2
+\zeta^3+(D_v-\epsilon^2/6)\zeta k^2.
$$

Daher gilt $\operatorname{Re}\log z_\pm=
\tfrac38(13\epsilon^2/24-D_v)k^2+o(k^2)<0$
fuer ausreichend kleine Nichtnull-k. Das beweist
Daempfung der beiden langen longitudinalen Zweige in
diesem Fall, nicht Stabilitaet aller k oder des
nichtlinearen Vielteilchensystems.

## 3. Derselbe skalare Quellport verliert den statischen Pol

Fuege die Testquelle s zu genau dem bisherigen skalaren
Lesekanal hinzu, also statisch
$d=g(k)m-ik b_s(k)(u+s)$. Weder die Quelle noch eine
Extrakopplung wird dem Richtungsdeposit hinzugefuegt.
Bei $z=1$ und $L=p^{-1}-1$ folgen aus den beiden
oberen Gleichungen $d=iLu/k$ und $m=i(TL/k-B)u$.
Daher ist die exakte statische Gleichung

$$
\left[(1-gT)\frac{L}{k^2}+\frac{gB}{k}+b_s(k)\right]u
=-b_s(k)s.
$$

Ist $g_0=0$, geht der Nenner gegen
$\epsilon^2/2+b_s$; bei $b_s=-\epsilon^2/2$ ergibt
sich der alte [kritische Skalarpol](collective_fifo_screening_2026-11-21.md).
Ist hingegen $g_0\chi=1$, geht der Nenner gegen
**denselben Koeffizienten $\epsilon^2+b_s$**, der
die quadrierte Wellengeschwindigkeit bestimmt.
Fuer $v\ne0$ bleibt die reine skalare Auslese
$\widehat K_s(k)(s+u)$ daher im Langwellenlimit
beschraenkt. Ein statischer $1/k^2$-Pol an diesem
Port verlangt mindestens $b_s=-\epsilon^2$,
also $v=0$. Ob dort der naechste Term wirklich den
Pol liefert, haengt von den Kernelbreiten ab; ein
fester Kontrollfall erhaelt ihn zurueck, aber ohne
nichtverschwindende Ausbreitungsgeschwindigkeit.

## 4. Befund und Grenze

Die [skalare Horizontschranke](collective_fifo_horizon_response_2026-11-22.md)
gilt nicht mehr fuer das kritische Vektorsystem: Die
zusaetzliche langsame Richtungsvariable ist tatsaechlich
nachweisbar und koppelt an die Dichte. Das reicht aber
an demselben Quellport nicht fuer den
[Kraft-/Phasen-Benchmark](retarded_scalar_interferometer_2026-11-22.md).
Die neutralisierte Richtung ist feinabgestimmt und
nicht automatisch ein konservierter Impuls. Andere
Quelloperatoren oder nichtlineare Abschluesse sind
hier nicht ausgeschlossen. Ein eingesetzter anderer
Quellport waere aber keine Herleitung.

Die [Stromrekonstruktion](collective_accumulated_current_2026-11-22.md)
identifiziert inzwischen einen Wellen-/Poisson-Transfer im
akkumulierten Transport. Am gegenwaertigen Kraftport ist
der statische Gradient dieser Auslese jedoch um $O(k^2)$
unterdrueckt. Die neue Auslese ist keine native Kraft.

Die enge Analogie sind polare Ordnungsuebergaenge und
gekoppelte Dichte-/Richtungsgleichungen bei aktiver Materie:
[Vicsek et al. (1995)](https://doi.org/10.1103/PhysRevLett.75.1226)
und [Bertin, Droz und Gregoire (2006)](https://arxiv.org/abs/cond-mat/0601038).
Hier wird weder deren Uebergang neu beansprucht noch
ihre Mikrodynamik mit dem FIFO gleichgesetzt. Der neue
Vergleich nutzt den konkreten Gauss-Schritt, die
Schreibreihenfolge und den selben skalaren Quellport.
[Feste Kontrollen](../../tests/test_collective_directional_current.py)
pruefen Gaussmomente, die Nullmode, die Daempfung und den
Tausch zwischen statischem Pol und Wellengeschwindigkeit.
