# Ein nativ regenerierter 4D-Defekt und seine Instabilitaet

Stand: 2026-11-23. Anschluss an den
[Vier-Deposit-Fuenfzyklus](native_fifo_four_volume_rotation_2026-11-23.md)
und den [Simplex-Nullstellensatz](memory_defect_charge_2026-11-14.md).
Vier vorausgesetzte Ortsdimensionen, keine neue Zustandsvariable,
Zieltrajektorie oder Parametersuche.

**Ergebnis.** Mit einem fuenften Richtungsdeposit existiert eine
exakte Familie nativer, vollrangiger Fuenfzyklen mit positivem
Alignment und rein attraktivem skalarem Gauss-Kernel. Der regulaere
$+1$-Defekt wird im nativen Vektorreadout in jedem Schritt wieder
erzeugt. In einem analytisch bestimmten Teilbereich liegt er strikt
innerhalb der Memory-Wolke. Trotzdem ist die **gesamte hier
konstruierte Familie** linear instabil. Die Konstruktion ersetzt
weder einen Stabilitaetsnachweis anderer Zweige noch die Suche
nach einer dynamisch geschuetzten Gegenladung.

## 1. Warum der fuenfte Beitrag die Kraftbilanz aendert

Verwende $H_v=5$ und $H_s=4$. Der rauschfreie native Schritt
liest die fuenf aus sechs aufeinanderfolgenden Positionen
gebildeten Einheitsrichtungen. Bei einem geschlossenen
Fuenfzyklus $y_5=y_0$ gilt $\sum_{j=0}^4 d_j=0$ mit
$d_j=y_j-y_{j+1}$. Wie im vorigen Bericht sei $R$ die
Doppeldrehung um $2\pi/5$ und $4\pi/5$ und $y_j=R^{-j}y_0$.
Alle Schrittlaengen sind $L$. Das Polynom
$1+z+z^2+z^3+z^4$ erzwingt im Vollrang, dass die effektiven
Koeffizienten der ersten vier Richtungen alle $-1$ betragen:
Dann ist der neue Schritt genau $d_4=R d_0$.

Die Vektorbeitraege seien
$b_j=\eta_v w_jG_1(y_0-y_j)/L$ und die skalaren
Gradientkoeffizienten $\gamma_1,\gamma_2,\gamma_3$ positiv
fuer Anziehung. Nach Eliminieren von $d_4$ lautet die native
Kopfbedingung

$$
b_j-b_4-\sum_{k=j+1}^{3}\gamma_k=-1\quad (0\leq j\leq3),
$$

also $b_4-b_3=1$ und $\gamma_j=b_{j-1}-b_j$ fuer $1\le j\le3$.
Anders als beim Vierplatzfall kann das Kriterium mit **positivem**
Alignment erfuellt werden: Das aelteste Deposit liegt wieder
naeher am Kopf als das vorletzte, so dass sein staerkerer
Gauss-Faktor den zusaetzlichen Altersverlust ueberwiegt.

Fixiere beide Breiten und Memory-Massen auf eins, Delta-Deposition
und Vektorretention $q=1/2$. Sei $t>2$ ein reeller Parameter,

$$
M=2t^2-2t+1,\quad a=\log M,\quad d=\log t,\qquad
D_1=D_4=2a,\quad D_2=D_3=2(a+d).
$$

$D_j$ ist der quadrierte Abstand von $y_0$ zu $y_j$.
Die Gauss-Faktoren sind $g_1=1/M$, $g_2=1/(tM)$.
Die beiden Radienquadrate entlang der Drehungen um
$2\pi/5$ bzw. $4\pi/5$ sind

$$
P_1=\frac{2a+d}{5}+\frac{d}{\sqrt5},\qquad
P_2=\frac{2a+d}{5}-\frac{d}{\sqrt5}.
$$

Da $M>t^2$, gilt $a>2d$ und beide sind strikt positiv.
Die beiden verschiedenen Drehfrequenzen geben den
vier unabhaengigen Schritten vollen Rang. Mit
$\eta_v=2L B$, $B=16tM/(t-2)$, ist

$$
(b_0,b_1,b_2,b_3,b_4)=
\frac{(16tM,\,8t,\,4,\,2,\,t)}{t-2}.
$$

Nimm den rein attraktiven nativen Teilfall $K=-G_1$,
Skalarretention $s=1/(4t-2)$ und
$\eta_s=b_3/[(1-s)s^3g_2]$. Dann gilt
$\gamma_j=\eta_s(1-s)s^jG_1(y_0-y_j)=b_{j-1}-b_j$
fuer $1\le j\le3$. Zudem ist $b_4-b_3=1$.
Die native Kraftbedingung ist somit exakt erfuellt;
$R$ ist keine Rotationsvorgabe im Update. Das ist eine
inverse Existenzkonstruktion, keine Parameterprognose.

## 2. Der Defekt bleibt auf der exakten Bahn innerhalb der Wolke

Die fuenf Orte bilden einen affinen Simplex und der
Ringschluss ist durch die native Kopfgleichung gesichert.
Der [allgemeine Satz](memory_defect_charge_2026-11-14.md#2-exakter-existenzsatz-mit-positivem-vergessen)
liefert an jeder Phase die eindeutige regulaere Nullstelle
mit Index $+1$. Spiegelung erzeugt kein Minus. Da der
Ortsursprung der Mittelwert der fuenf Orte ist und ihre Normen
gleich sind, lautet die Nullstellenbedingung

$$
y_j\cdot z_*=(j-2)\log 2,\qquad j=0,\ldots,4.
$$

Die Gram-Matrix $G_{ij}=y_i\cdot y_j$ verschwindet in der
konstanten Richtung. Auf den beiden reellen Fourier-Ebenen
hat sie die Eigenwerte $5P_1/2$ und $5P_2/2$.
Fuer die baryzentrischen Gewichte muss
$G\lambda=(\log 2)(-2,-1,0,1,2)^T$ und $\sum\lambda_j=1$
gelten. Die Projektionen des Vektors $(-2,-1,0,1,2)$
auf die zwei Fourier-Ebenen sind
$(-1,-\varphi,0,\varphi,1)$ und
$(-1,\varphi^{-1},0,-\varphi^{-1},1)$, mit
$\varphi=(1+\sqrt5)/2$. Wegen $P_1>P_2$ und
$\varphi-\varphi^{-1}=1$ ist der erste Eintrag der
kleinste. Damit

$$
\lambda_{\min}=\frac15-\frac{2\log2}{5}
                  \left(\frac1{P_1}+\frac1{P_2}\right)
>\frac15-\frac{\log2}{d}.
$$

Die letzte Schranke benutzt $P_{1,2}>d(1\pm1/\sqrt5)$.
Fuer **alle $t\ge32$** ist daher $\lambda_{\min}>0$.
Die Nullstelle liegt strikt innen und dreht mit der
Historie. Dies ist geometrische Innenlage, keine
Bindungsenergie und keine Aussage ueber Einzugsbereiche.
Ein Gegenfall innerhalb derselben Existenzfamilie ist
$t=3$, wo die Nullstelle ausserhalb der Huelle liegt.

Auch ein grosser geometrischer Abstand zum Rand ist
kein Beleg fuer eine starke Feldantwort: Der gemeinsame
Wert $w_jG_1(z_*-y_j)$ ist
$\exp[-(\|z_*\|^2+P_1+P_2)/2]/8$.
Es gilt $P_1+P_2=2\log t+O(1)$. Aus der inversen
Gram-Matrix auf den Fourier-Ebenen folgt zudem
$\|z_*\|^2=O(1/\log t)$. Die Ableitung jedes Summanden
multipliziert den gemeinsamen Wert nur mit einer
Einheitsrichtung und dem Abstand zum Kern, von der
Groessenordnung $\sqrt{\log t}$. Damit ist die Norm des
Feld-Jacobians am Defekt $O(\sqrt{\log t}/t)$ fuer
$t\to\infty$.

## 3. Ausschluss dynamischer Stabilitaet fuer die ganze Familie

Die volle konsistente Historie hat sechs Orte bzw. 24 reelle
Koordinaten. Im mitdrehenden Rahmen tragen nur die juengsten
Kopfableitungen zur Spur bei; alle Shiftzeilen liegen ausserhalb
der Diagonalbloecke. Mit $r_j=y_0-y_j$ und $p_0=d_0/L$ ist
der Kopfsensitivitaetsblock

$$
J_0=b_4 I+\sum_{j=1}^3\gamma_j r_jr_j^T
-B p_0p_0^T-\sum_{j=1}^4 b_jd_jr_j^T .
$$

Die Normierungsableitung der juengsten Richtung ist enthalten.
Die Identitaetsbeitraege addieren sich zu
$1-\sum_j\gamma_j+B=1+b_3=b_4$.
Schreibe $U=d-a$ und $V=-d$ fuer $d_0\cdot d_1$ bzw.
$d_0\cdot d_2$. Aus der Zyklusgeometrie gilt
$r_1\cdot R^{-1}r_1=U$, $r_{2,3}\cdot R^{-1}r_{2,3}=-V$,
und die vier Werte $r_j\cdot R^{-1}d_j$ sind der Reihe nach
$V,2V,U+2V,-U$. Mit $\operatorname{tr}R=-1$ ergibt sich
fuer die Spur der vollen mitdrehenden Ableitung

$$
T=-b_4+K U-C V,\qquad
K=B-b_1+1-\frac{B}{2a},\qquad C=2b_1+2b_2+b_3.
$$

Fuer jedes $t>2$ gilt $a>\log5>3/2$,
$d>\log2>2/3$, $U<-d$, $K/B>17/30$ und
$C/B=1/M+5/(8tM)<21/80$.
Die Logarithmusschranken folgen aus den ersten Termen
der Reihe fuer $2\operatorname{artanh}((x-1)/(x+1))$.
Aus $B=16Mt/(t-2)$ folgt $B>160$: fuer $2<t<4$
ist $t/(t-2)>2$ und $M>5$, fuer $t\ge4$ ist $M\ge25$.
Also ist $K-C>3B/10$ und damit $T<-32<-24$.
Mindestens ein Multiplikator hat Betrag groesser $4/3$.
Wegen Aequivarianz und $R^5=I$ ist seine fuenfte
Potenz ein wachsender voller Periodenmultiplikator, keine
starre Symmetrierichtung. Der analytische Ausschluss gilt
fuer alle $t>2$ in **dieser** Familie, nicht fuer andere
Retentionsfamilien, unterschiedliche Breiten oder nichtstarre
mehrphasige Wiederkehr.

## 4. Konsequenz und Nachweisumfang

Die native Regel hat einen innerhalb der eigenen Wolke
mitbewegten, regulaeren Defekt hervorgebracht, ohne eine
eingesetzte Erhaltungsbedingung. Bewiesen ist die Wiederkehr
eines vorbereiteten Orbits, keine Entstehung aus beliebigen
Saaten. Das nachgewiesene Wachstum schliesst den ganzen
untersuchten Zweig als robusten Traeger aus; die Indexzahl
$+1$ liefert noch keinen zweiten Ladungstyp. Ein weiterer
Parameterpunkt desselben Zweigs aendert beides nicht.
Andere Retentionen oder Breiten koennen fuer die
Stabilitaetsfrage relevant sein, nicht aber fuer das
Indexvorzeichen eines geschlossenen Simplex. Fuer ein
Paar beider Indexvorzeichen ist daher eine andere
Memory-Geometrie noetig. Ein Ladungsanspruch braucht
zusaetzlich eine Quellenbilanz.

[Bacot et al., PRL 122, 104303 (2019)](https://arxiv.org/abs/1812.08825v2)
zeigen stabile freie Zustaende mit kohaerenter Wellenerinnerung
in einem anderen System. Die hiesige Instabilitaet ist kein
Argument gegen Stabilisierung durch Memory allgemein und
die Wellendynamik jener Arbeit ersetzt keinen FIFO-Formtest.

Die [festen Kontrollen](../../tests/test_native_fifo_four_volume_rotation.py)
vergleichen exakte Kraftkoeffizienten, alle fuenf vorgeschriebenen
Kopfwerte, die innere Nullstelle samt regulaerem Jacobian und
die Spur der vorhandenen Kopfableitung mit den Formeln.
Die Familienresultate folgen aus der Algebra, nicht
aus Stichproben oder einer Zielsimulation.
