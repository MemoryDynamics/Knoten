# Eine laengere Altersliste ersetzt keinen Wellenkanal

Stand: 2026-11-22. Analytische Pruefung des bestehenden
[linearen kollektiven Dichteabschlusses](collective_fifo_screening_2026-11-21.md)
gegen die [retardierte Skalarfeld-Referenz](retarded_scalar_interferometer_2026-11-22.md).
Feste Matrix- und Fourierkontrollen, kein neuer Vielknotenlauf und
keine Aenderung der nativen Orts- oder Richtungsregel.

**Ergebnis.** Bei gleicher Gesamtlesestaerke baut kein
nichtnegatives Altersprofil den kollektiven Anteil schneller auf
als die Referenz ohne Verzoegerung. Die Schranke gilt auch fuer
mit der Wellenlaenge anwachsende oder unendliche Speicher.
Im Frequenzband einer Langwelle verschwindet der relative
kollektive Beitrag zum direkten Readout selbst bei einem
vorzeichenbehafteten Altersfilter mit gleichmaessig beschraenkter
absoluter Gewichtssumme. Der vorhandene lineare statische
$1/r$-Pol reicht daher auch bei einem Horizontgrenzwert nicht aus.

## 1. Gleiche Kopplung, beliebige Altersverteilung

Fuer eine feste raeumliche Wellenzahl $k>0$ benutze dieselbe
lineare Rekursion wie im Dichteabschluss, mit einer auf
Quelleneinheiten normierten Dichte $y_n$:

$$
y_{n+1}=p y_n+c\left(s_n+\sum_{j\geq0}\omega_j y_{n-j}\right),
\qquad U_n=\widehat K(k)
\left(s_n+\sum_{j\geq0}\omega_j y_{n-j}\right).
$$

Hier sind $p=e^{-d_0k^2}$, $c=p A k^2 e^{-ak^2}$,
$d_0,a>0$ und $0<A\le d_0$; $A$ ist die kollektive
Lesestaerke des attraktiven Gausskanals einschliesslich
des gesamten Gewichts. $s_n$ ist die vorgegebene Quelle,
kein dynamischer Knoten. Die Dichtevorgeschichte bis $n=0$
ist ungestoert. Fuer diesen Abschnitt gilt
$\omega_j\ge0$, $\sum_j\omega_j=1$. Die Gewichte
duerfen von k abhaengen und eine unendliche Anzahl von
Altersklassen belegen. Weder ein erstes Altersmoment
noch eine exponentielle Abfallrate wird vorausgesetzt.

Setze $s_* = \sup_n |s_n|$, $z_*=p+c<1$ und

$$
v_n=s_*\frac{c}{1-z_*}(1-z_*^n)\quad(n\geq0),
\qquad v_n=0\quad(n<0).
$$

Dies ist die Antwort bei $\omega_0=1$ und konstanter
Quelle $s_*$. Sie ist monoton nicht fallend. Per
Induktion gilt

$$
|y_n|\leq v_n,\qquad
\left|\frac{U_n}{\widehat K(k)}-s_n\right|\leq v_n .
$$

Denn die Summe der Betraege alter Werte ist durch
$\sum_j\omega_j v_{n-j}\le v_n$ beschraenkt; damit
ist der naechste Wert hoechstens $(p+c)v_n+c s_* = v_{n+1}$.
Die Aussage gilt fuer komplexe Fourieramplituden und
erfasst neben einer Einschaltquelle auch beliebige
beschraenkte Zeitpulse.

## 2. Zeit bis zu einem festen Anteil des statischen Feldes

Bei $s_n=1$ und konstanten Historien ist der statische
Wert $U_\infty=\widehat K(k)(1-p)/(1-z_*)$ fuer alle
normierten Altersprofile gleich. Er wird auch bei
unendlich vielen Altersklassen aus der Nullvorgeschichte
erreicht: Die erzwungene Folge ist monoton (Induktion
auf ihren Inkrementen), beschraenkt, und dominierte
Konvergenz im Altersmittel setzt ihren Grenzwert auf
$c/(1-z_*)$.

Fuer jeden n folgt aus der Schranke

$$
0<\frac{U_n}{U_\infty}
\leq 1-\frac{c}{1-p}z_*^n .
$$

Bei kritischer Lesestaerke $A=d_0$ ist
$1-z_*=D_4 k^4+O(k^6)$ mit $D_4=d_0a+d_0^2/2$ und
$c/(1-p)\to1$. Fuer einen festen Anteil $0<q<1$ braucht
daher **jedes** nichtnegative Altersprofil mindestens

$$
\frac{-\log(1-q)+o(1)}{D_4 k^4}
$$

Schritte. Die Referenz ohne Verzoegerung erreicht diese
Schranke asymptotisch. Dasselbe Schrankenargument
erfasst den phasenrelevanten Zeitmittelwert: Er kann
den Wert der Referenz ohne Verzoegerung nicht uebertreffen.
Bei Beobachtungsdauer $n\le C/k$ liefert schon
$v_n\le s_*cn$ nur $O(k)$ induzierten Anteil zum
direkten Readout. Eine groessere Alterstiefe kann den
Aufbau weiter bremsen: Bei $\omega_L=1$ bleibt der
gelesene kollektive Anteil bis einschliesslich Schritt
L exakt null. Waechst L schneller als $k^{-4}$, ist
die Quartik keine obere Zeitschranke mehr.

## 3. Keine versteckte Verstaerkung im akustischen Frequenzband

Die frequenzaufgeloeste Antwort bei $z=e^{i\theta}$ lautet
mit $P(z)=\sum_j\omega_j z^{-j}$

$$
\frac{\chi(k,z)}{\widehat K(k)}
=\frac{z-p}{z-p-cP(z)}.
$$

Jetzt duerfen die Gewichte auch reell und vorzeichenbehaftet
sein. Wenn ihre absolute Summe durch V beschraenkt ist,
gilt $|P(e^{i\theta})|\le V$. Das gilt unabhaengig
vom Horizont und von Oszillationen in den Altersphasen.
Fuer $m k\le |\theta|\le M k$ mit festen $0<m<M$
gilt bei kleinem k:

$$
\left|\frac{\chi}{\widehat K}-1\right|
\le \frac{cV}{|\sin\theta|-cV}=O(k).
$$

Denn $p$ ist reell, $|z-p|\ge|\sin\theta|$ und
$c=O(k^2)$. Der feste Gausskernel ist bei null
beschraenkt und ungleich null. Die gesamte Antwort
bleibt daher $O(1)$ und ihr Verhaeltnis zur kritischen
statischen Antwort geht wie $O(k^2)$ gegen null.
Fuer signierte Filter ist dies eine Randfrequenzschranke
des Symbols, keine allgemeine Stabilitaetsaussage.
Sie schliesst versteckte interne Eigenwerte mit
verschwindendem Einfluss auf den gemessenen Port nicht aus.

Ein echter Wellenkanal mit demselben statischen $1/k^2$-Pol
liefert dagegen bei einer Einschaltquelle und auf skalierten
Zeiten $t=\tau/k$ die Antwort
$(1-\cos(v\tau))/(v^2 k^2)$ pro Quellstaerke,
fuer die deklarierte Gleichung $\ddot U+v^2k^2U=s$.
Das unterscheidet den Aufbau schon abseits der Resonanz;
es ist kein Vergleich ueber eine einzelne schnellste Wurzel.
Soll ein signierter Altersfilter bei unveraendertem
$O(k^2)$-Port den $O(k)$-Term $z-p$ kompensieren,
muss seine absolute Gewichtssumme mindestens von Ordnung
$1/k$ sein. Das ist nur notwendig, nicht hinreichend;
hergeleitet oder physikalisch zugelassen ist ein solcher
singulaerer Filter hier nicht.

## 4. Konsequenz fuer die native Suche

Mehr positive Rueckschau ersetzt in diesem Dichtekanal
keinen eigenstaendigen dynamischen Strom. Das ist keine
Aussage gegen alle Memory-Modelle. Der naechste
diskriminierende Test fuer Vektormemory ist, ob im
Langwellenlimit **ein unabhaengiger langsamer Strom**
neben der Dichte existiert und an denselben Kraftport
koppelt. Eine gespeicherte Richtung oder ein einzelner
rotierender Knoten ist noch kein Nachweis dafuer.
Der Unterschied zwischen geschwindigkeitsaufgeloestem
Kramers- und reinem Smoluchowski-Kanal hat bekannte
Vorlaeufer; siehe [Chavanis (2013)](https://arxiv.org/abs/1306.1225).
[Goldstein (1951)](https://doi.org/10.1093/qjmam/4.2.129)
liefert eine getrennte klassische Positivreferenz fuer
Richtungspersistenz und Telegraphendynamik, nicht fuer
die hier untersuchte reine Altersgewichtung.

Der [Richtungsabschluss](collective_directional_current_2026-11-22.md)
liefert jetzt den gesuchten zweiten linearen Strommodus bei exakt
kritischer Ausrichtung. Er zeigt aber auch, dass am selben skalaren
Quellport der statische Pol mit nichtverschwindender Wellengeschwindigkeit
verschwindet.

Die [festen Kontrollen](../../tests/test_collective_fifo_screening.py)
pruefen die Zeitbereichsschranke, einen langen reinen Lag
und normierte sowie signierte Filter im akustischen Band.
Der lineare Dichteabschluss, 3D und die attraktive
Lesekonvention bleiben Voraussetzungen.
