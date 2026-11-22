# Ein Bahnphasentest fuer Eigenmemory und kollektive Fernantwort

Stand: 2026-11-22. Analytischer Vergleich auf vorbereiteten Armen und
im bereits deklarierten linearen Dichteabschluss. Keine neue native
Zieltrajektorie, keine Phasendynamik in die Einzelregel eingebaut.

**Ergebnis.** Ein translationsinvariantes Eigenmemory mit summierbaren
Altersgewichten liefert keinen zur Haltezeit proportionalen kumulierten
Hoehenkontrast. Ein gemeinsames skalares Feld kann ihn liefern. Aber
nach Einschalten der Quelle erreicht der vorhandene kritische
Dichtevergleich einen festen Anteil seiner statischen Langwellenantwort
erst auf der Zeitskala $k^{-4}$. Dasselbe gilt ohne FIFO-Verzoegerung.
Geprueft wurde der Skalarport, nicht die Entstehung einer Quantenauslese.

## 1. Referenz: zwei Armhoehen, gleiche Dauer

Das [relative Drehwegzeichen](fifo_relative_frame_lift_2026-11-22.md)
liefert bei konstanten Rahmen keinen Unterschied. Ein zweiter Test
haelt zwei vorbereitete Arme auf den Hoehen $z$ und $z+d$ fuer die
Dauer $T$, mit festen Abschnitten vor und nach dem Plateau. Verglichen
wird der gravitative **Potentialbeitrag** zur Phase:

$$
\Delta\phi_{\rm ext}=-\frac{mg}{\hbar}\int(z_A(t)-z_B(t))\,dt
=-\frac{mgd}{\hbar}T+\text{Beitrag der festen Abschnitte}.
$$

Ein gemeinsamer, auch zeitabhaengiger Potentialoffset kuerzt sich
bei zeitgleicher Auslese heraus. Entscheidend ist die Steigung,
nicht die Phase modulo $2\pi$ bei einer einzigen Haltezeit.
Der empirische Bezug ist
[Colella, Overhauser und Werner (1975)](https://doi.org/10.1103/PhysRevLett.34.1472).
Die Plateau-Vorschrift rekonstruiert weder ihre Kristalloptik
noch die Gesamtphase einer beliebigen frei fallenden Anordnung.
[Roura (2020)](https://doi.org/10.1103/PhysRevX.10.021014) behandelt
die Kinematik und die weiteren Beitraege beim Eigenzeitvergleich.
Hier sind Bahnen und externe Traegerbedingungen Inputs, ebenso
$m$, $g$ und $\hbar$.

## 2. Eigenmemory ohne extensive Hoehenphase

Sei $x_n$ der vorgegebene Referenzarm. Der zweite Arm sei
$x_n+d s_n e_z$, mit $s_n=1$ fuer $0\le n<N$, sonst null.
Beide Arme haben eine gemeinsame Vor- und Nachgeschichte
und dieselbe Zeitschrittlaenge $\Delta t$. Die eigene Auslese ist

$$
U_n^{\rm self}=\sum_{j\geq0} w_j K(x_n-x_{n-j}).
$$

Betrachtet wird die akkumulierte Differenz $\Delta I_N$ beider
Readouts, multipliziert mit $\Delta t$. Dies setzt eine additive
Auslese voraus, keine daraus hergeleitete Phase. In einem endlichen
FIFO sind innen im Plateau saemtliche eigenen Kopf-Deposit-Abstaende
gleich. Nur die Uebergaenge liefern Kontrast. Diese Aussage gilt fuer
jede gleichzeitig translationsinvariante Auslese des Eigenfensters.

Fuer ein global Lipschitz-stetiges $K$ mit Konstante $L$ und
$\sum_j|w_j|<\infty$ gilt auch bei unendlichem Horizont

$$
|\Delta I_N|\leq 2d\,\Delta t\,L\sum_{j\geq0}|w_j|\min(j,N).
$$

Denn der Abstand der beiden Kernelargumente ist
$d|s_n-s_{n-j}|$ und die Summe ueber alle n ergibt $2d\min(j,N)$.
Die Schranke gilt fuer die gliedweise Differenz; bei beschraenkten
Kernelwerten wie im Gaussfall existieren auch beide einzelnen Readouts.
Bei endlichem erstem Altersmoment ist der kumulierte Betrag
unabhaengig von N beschraenkt. Bereits Summierbarkeit erzwingt
$\Delta I_N/(N\Delta t)\to0$ per dominierter Konvergenz mit
$\min(j,N)/N\leq1$. Endliche, beschraenkte Rampen fester Dauer
aendern das Rechtecksignal nur um eine Folge mit gleichmaessig
beschraenkter absoluter Summe. Durch die Dreiecksungleichung
addiert dies hoechstens einen von N unabhaengigen Beitrag.
Kein konstanter Wirkungsfaktor kann die fehlende Steigung retten.
Eine gemeinsame Quelle oder eine hergeleitete interne Uhr
mit eigener Dynamik sind damit nicht ausgeschlossen.

## 3. Gemeinsamer Kanal: Einschaltprobe am kritischen Pol

Im [kritischen linearen Dichtevergleich](collective_fifo_screening_2026-11-21.md)
ist der Hintergrund vor der Anregung homogen. Schalte bei $n=0$
die gegebene Fouriermode $s\cos(kx_1)$ mit $s\ne0$ ein. Zwei fest
gehaltene Proben haben einen nicht verschwindenden Cosinus-Kontrast.
Eine *gesetzte* additive Phase waere proportional zu
$\Delta t\sum_{n=0}^{N-1}(U_n(x_A)-U_n(x_B))$.
Teile durch dieselbe Auslese bei bereits stationaer vorliegendem Feld.
Der Ortspaar-Kontrast, die Quellstaerke und ein gemeinsamer
Phasenkoeffizient kuerzen sich im Quotienten.

Schreibe $p=e^{-d_0 k^2}$, $c=p d_0k^2e^{-a k^2}$, $\omega_j=w_j/W$.
Bei festem H ist $M$ die Historienmatrix mit Kopfzeile
$p e_0^T+c\omega^T$ und den FIFO-Shiftzeilen darunter.
Normiert auf $s/W$ ist der Antrieb $c e_0$. Der stationaere Zustand
ist $Y_\infty=c\boldsymbol1/(1-p-c)$. Fuer die Nullvorgeschichte
liefert $Y_n=(I-M^n)Y_\infty$ und
$U_n=\widehat K s(1+\omega^T Y_n)$ exakt

$$
\mathcal R_N(k)
=\frac{1}{N}\sum_{n=0}^{N-1}\frac{U_n}{U_\infty}
=1-\frac{c}{1-p}\frac{1}{N}\sum_{n=0}^{N-1}\omega^T M^n\boldsymbol1.
$$

Der langsame Eigenwert ist $z=1-D_4 k^4+O(k^6)$ mit
$D_4=d_0a+d_0^2/2$; der zugehoerige rechte Eigenvektor ist
$v_j=z^{-j}$. Aus $z^{H-1}v\leq\boldsymbol1\leq v$ und
$M\geq0$ folgt $z^{n+H-1}v\leq M^n\boldsymbol1\leq z^n v$.
Daher ist $\omega^T M^n\boldsymbol1=z^n(1+O(k^4))$ gleichmaessig
in n. Da $c/(1-p)\to1$, liefert die geometrische Summe im Grenzwert
$k\to0$, $N D_4 k^4\to\tau$ den Ausdruck

$$
\mathcal R_N(k)\longrightarrow 1-\frac{1-e^{-\tau}}{\tau}.
$$

Die stetigen Endwerte sind null bei $\tau=0$ und eins bei
$\tau=\infty$. Bei einer Relaxationszeit erreicht die akkumulierte
Auslese $e^{-1}\approx0.368$, nicht den Momentananteil $1-e^{-1}$.
Doppelte Wellenlaenge kostet asymptotisch sechzehnmal so viele
Updates fuer denselben Anteil. Der Grenzwert gilt bei erst
linearisiertem Quellport, nicht bei fest grosser Quelle.
Er gilt bereits fuer $H=1$, also auch ohne FIFO-Verzoegerung.

## 4. Was fuer einen gemeinsamen Physiktest fehlt

Der Eigenkanal besteht den Plateau-Steigungstest nicht. Der
gemeinsame lineare Kanal kann im stationaeren Referenzzustand
einen kumulierenden Skalar liefern. Die Einschaltprobe widerlegt
keinen bereits statisch vorbereiteten Vergleich, trennt diesen
Kanal aber von einer prompten Langwellenantwort. Die
[nichtlineare Schalenbilanz](critical_fifo_stationary_tail_2026-11-21.md)
schliesst einen unbesehenen Uebertrag des linearen stationaeren
Fernprofils auf feste Quellen aus.

Ein gemeinsamer Kandidat muesste dasselbe schwache Feld an
Beschleunigung und Wirkung koppeln. Ist fuer Traegerart $i$
der Kraftport $-b_i\nabla U$ und der entsprechende Phasenbeitrag
$-a_i\int U\,dt$, dann muessen bei gemeinsamen Feldeinheiten
$b_i/m_i$ artunabhaengig sein und $a_i/b_i=1/\hbar$ gelten.
Die Massen waeren unabhaengig aus mechanischer Traegheit zu
bestimmen, nicht aus dem Phasefit oder einem History-Filter.
Der native erste Drift ist kein solcher Kraftport. Eine passende
Steigung fuer einen Armvergleich weist weder Universalitaet noch
kohaerente Rekombination, Gravitation oder Quantisierung nach.

Der [Wirkungstest am nativen Lesepotential](memory_single_path_action_2026-11-22.md)
zeigt jetzt, warum die unveraenderte retardierte Leseregel kein
solcher Einbahn-Wirkungsgradient ist. Die positive bedingte
Pfaddichte liefert auch in Fourier-Schreibweise keine relative Phase.

Feste Kontrollen: [Eigenkanal](../../tests/test_memory_action_phase.py)
und [kollektiver Einschaltvergleich](../../tests/test_collective_fifo_screening.py).
Letzterer benutzt kleine Matrixpotenzen und zum Abgleich 21
direkte lineare Referenzschritte; kein Vielknotenlauf.
