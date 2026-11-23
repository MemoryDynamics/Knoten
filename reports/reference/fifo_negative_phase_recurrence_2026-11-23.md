# Minusdefekt ueber alle vorbereiteten Phasen, aber keine native Wiederkehr

Stand: 2026-11-23. Anschluss an die
[Phasengrenze und die Zehn-Deposit-Zeugen](fifo_defect_phase_threshold_2026-11-23.md).
Vier vorausgesetzte Ortsdimensionen; feste Historien und Kraftsubstitutionen,
keine Zieltrajektorie oder Parameteranpassung.

**Ergebnis.** Eine periodische voll affine Bahn, die durch dieselbe affine
Abbildung in jedem Schritt beschrieben wird, kann unabhaengig von ihrer
Laenge keinen regulaeren Minusdefekt tragen. Fuer die nichtaffinen
Zehn-Phasen-Zeugen bleibt der jeweilige lokale Index dagegen an allen
vorbereiteten Phasen erhalten. Dennoch kann die native Skalar-/Alignment-
Regel genau den Minuszeugen nicht selbst schreiben: Es gibt eine
phasenweise unvertraegliche Kraftgleichung fuer **jede** radiale
Skalarkraft, auch bei getrenntem Vergessen. Eine hinreichende Zahl
von Bahnphasen und ein statischer Minusindex reichen fuer einen
nativen Traeger nicht aus.

## 1. Keine Minusquelle auf einem einzigen affinen Periodenorbit

Sei eine periodische Spur durch dieselbe affine Abbildung in
jeder Phase erzeugt. In der neueste-zuerst Ordnung schreibe
$y_{j+1}=A y_j+b$. Der Schwerpunkt $c$ eines vollen Umlaufs
ist dann fest. Mit $z_j=y_j-c$ gilt $z_{j+1}=A z_j$.
Hat der Umlauf vollen affinen Rang und Periode $P$, dann
ist $A^P=I$: Die $z_j$ spannen den ganzen Raum auf und
werden von $A^P$ fixiert. $A$ hat keinen Eigenwert $1$.
Ein entsprechendes linkes Eigenfunktional waere auf allen
$z_j$ konstant, wegen $\sum_j z_j=0$ also identisch null.
Daraus folgt $\det(I-A)>0$, da nichtreelle Eigenwerte
paarweise konjugiert sind und der einzige moegliche
reelle Eigenwert $-1$ einen Faktor $2$ liefert.

Die Schrittrichtung ist proportional zu $(I-A)z_j$.
Sei $s_j=\|y_j-y_{j+1}\|$ (oder $s_j=1$ fuer den
Verschiebungsreadout). Fuer positives $w_j$ und gleiche
Gaussbreite ist das Feld eines beliebigen endlichen
Fensters deshalb

$$
V(c+x)=\sigma^2e^{-\|x\|^2/(2\sigma^2)}(I-A)\nabla U(x),
\qquad
U(x)=\sum_j \frac{w_j}{s_j}
 e^{-\|z_j\|^2/(2\sigma^2)} e^{x\cdot z_j/\sigma^2}.
$$

$U$ ist konvex. Hat das Fenster vollen linearen Span
der $z_j$, ist die Hesse-Matrix strikt positiv:
Ihre Richtungsform ist eine Summe positiv gewichteter
Quadrate. An jeder Nullstelle ist dann der Index $+1$;
der Ableitungsterm des gemeinsamen Gaussfaktors verschwindet
dort. Sonst kann das Feld wegen Rangmangels keinen
regulaeren Defekt tragen. Enthaelt das Fenster den ganzen
Umlauf, liegt null strikt im Inneren der konvexen Huelle
der $z_j$. Damit ist $U$ koerziv und hat genau ein Minimum,
also gibt es genau eine Nullstelle. Ein kuerzeres
Fenster kann die Nullstelle verlieren, aber keinen
regulaeren Minusindex gewinnen.

Der Beweis schliesst auch nichtorthogonale affine
Darstellungen eines periodischen Orbits ein. Starre
Ein-Schritt-Drehungen beliebiger Perioden sind nur ein
Teilfall. Eine nichtperiodische, aber gebundene starre
Ein-Schritt-Bewegung hat denselben Vorzeichenausschluss:
In der Summe kann dieselbe orthogonale Matrix $A$
ausgeklammert werden. Ein Drift entlang des Fixraums
waere ungebunden; mit Fixrichtungen bildet $I-A$ das
Feld in einen echten Unterraum ab, und ohne Fixrichtungen
ist $\det(I-A)>0$. Diese Aussagen sind unabhaengig von
der nativen Kraftbilanz und dem Skalar-Kernel.

Der Zusammenhang von Schwerpunkt und konvexer
Exponentialsumme ist Standard, vgl.
[Wainwright und Jordan, Prop. 3.1](https://people.eecs.berkeley.edu/~jordan/sail/readings/wainwright-jordan-fnt.pdf).
Die Faktorisierung durch $I-A$ nutzt eigens die
FIFO-Schrittrichtung; sie fuehrt keine thermodynamische
Energie oder stationaere Verteilung ein.

## 2. Vorbereiteter Zehn-Phasen-Zeuge behaelt seinen Index

Verwende die fruehere Geometrie $a_i=v_i$,
$b_i=v_i-6Jv_i$ mit $J=I$ bzw. $J=I-2v_0v_0^T$.
Jedes volle Zehn-Deposit-Fenster derselben Spur
enthaelt alle nahen und fernen Punkte einmal. Eine
Phasenverschiebung rotiert nur ihre Altersgewichte,
nicht die Schrittvektoren der vorgegebenen Spur.
Im Vergleich mit der ungewichteten Nahschale
betraegt die Summe der fehlenden Nahgewichte maximal
$(1+3+5+7+9)(1-q)=1/40$ fuer $q=999/1000$.
Die aeltere Schaetzung fuer eine einzige Startphase
laesst sich damit ohne Aenderung der Kernkugel erweitern.

Im Ball $|z|\le1/8$ liefern die Nahschale, die fehlenden
Nahgewichte und die Fernbeitraege zusammen die
phasengleiche Schranke

$$
\|DF-\kappa J\|<
\frac{15}{32}+\frac{9}{8}\frac1{40}+\frac1{400}
=\frac{799}{1600}<\frac12.
$$

Wie vorher ist $F=V/w_0$ und $\kappa>3/4$. Ferner
$\|F(0)\|<1/40+1/2000$. Der Korrekturschritt
$z\mapsto z-(\kappa J)^{-1}F(z)$ bleibt im Ball und
hat Lipschitz-Konstante kleiner als $2/3$.
Also liegt an jeder vorbereiteten Phase genau ein
regulaerer Defekt mit Index $\det J$ in demselben
Innenball. Dieselben Schranken gelten sogar fuer
die lineare Interpolation der beiden **Felder**
zwischen aufeinanderfolgenden Phasen; in diesem
Auslesevergleich kann der Kern nicht am Rand verloren
gehen. Das ist keine native Zeitinterpolation und
keine Stabilitaet gegen Stoerungen der Bahn.

## 3. Der Minuszeuge besteht die native Kraftbilanz nicht

Fuer den Minuszeugen seien $a_i=v_i$, $b_0=7v_0$ und
$b_i=-5v_i-3v_0$ fuer $1\le i\le4$.
Die Orte sind neueste zuerst in Folge
$a_0,b_0,a_1,b_1,\ldots,a_4,b_4$ geordnet.
Zur Selbstreproduktion muessten die beiden
Spezialphasen $b_0\to a_0$ und $a_0\to b_4$ gelingen.
Projiziere auf $v_0^\perp$, und schreibe $u_i$ fuer
die Projektion von $v_i$ ($1\le i\le4$). Deren einzige
Relation ist $\sum_i u_i=0$.

Verwende die rauschfreie native Alignment-Regel mit
Skalarretention $0<s<1$, Vektorretention $1/2\le q<1$,
Vektorbreite eins und Horizonten aus ganzen
Zehn-Perioden. Die Skalar- und Vektorhorizonte duerfen
verschieden sein. Ganze Wiederholungen eines Umlaufs
multiplizieren nur ihre Phasengewichte mit einem
gemeinsamen positiven Faktor. Die Aussage gilt
fuer **jedes** radiale skalare Gradientenprofil, also
auch fuer die vorhandene doppelte Gaussform.

An beiden Spezialphasen haben alle vier sonstigen
Nahpunkte jeweils denselben Abstand zum Kopf;
ebenso die vier sonstigen Fernpunkte untereinander.
Ihr Altersfaktor ist jeweils proportional zu
$s^{2i}$, waehrend die Projektionen der Orte $u_i$
bzw. $-5u_i$ sind. Damit liegt der skalare Drift
in beiden Phasen in der eindimensionalen Richtung

$$
T_s=\sum_{i=1}^4 s^{2i}u_i.
$$

An $b_0$ hat das Sollinkrement keine Querkomponente.
Setze $t=q^2$, $\ell_0=\sqrt{107/2}$,
$\ell=\sqrt{47/2}$ und $\ell_4=\sqrt{31}$.
Das sind die Laengen der nachfolgenden Schritte
von $b_0$, von $b_1,b_2,b_3$ und von $b_4$ in
der Historienreihenfolge. Alle anderen Nahpunkte
haben zu $b_0$ quadrierten Abstand $107/2$,
alle anderen Fernpunkte Abstand zum Quadrat $100$.
Bis auf einen gemeinsamen positiven Faktor lautet
der native tangentiale Vektorreadout daher
$\sum_i A_i u_i$ mit

$$
\begin{aligned}
K&=e^{-107/4}/q,& B&=e^{-50}/\ell,& B_4&=e^{-50}/\ell_4,\\
A_1&=(K-5B)t-\ell_0^{-1},&
A_2&=(K-5B)t^2-Bt,\\
A_3&=(K-5B)t^3-Bt^2,&
A_4&=(K-5B_4)t^4-Bt^3 .
\end{aligned}
$$

Der aktuelle Schritt am Fernpunkt traegt
$-u_1/\ell_0$. Die sonstigen Nahpunkte tragen
je $u_i$ und die Fernpunkte $(-5u_i-u_{i+1})/\ell$
bzw. $-5u_4/\ell_4$ bei, jeweils mit zugehoerigen
nativen Gewichten. Das ergibt die Koeffizienten
ohne eingefrorene oder frei angesetzte Richtungen.
Es gilt $A_1<0$, denn $Kt<1/8<1/\ell_0$,
und $A_2>0$, denn
$Kt/B=q\ell e^{93/4}>6>5t+1$. Zudem
$A_3=tA_2<A_2$. Die Folge ist damit nicht monoton.
Jede Koeffizientenfolge eines Vielfachen von $T_s$
ist dagegen bis auf Addition einer Konstanten
monoton: $\sum_i u_i=0$ ist ihre einzige Freiheit.
Der Vektorreadout liegt also fuer **kein**
$s\in(0,1)$ in der skalaren Driftrichtung.

Damit kann an $b_0$ nur ein ausgeschalteter
Vektorport $\eta_v=0$ die tangentiale Bedingung
erfuellen. An $a_0$ ist dann jedoch der
tangentiale Anteil des Sollinkrements $-5u_4$, und
$u_4\notin\operatorname{span}(T_s)$:
Die ersten drei Koeffizienten $s^2,s^4,s^6$
sind nicht gleich. Somit gibt es fuer den
vorgegebenen Minuszeugen keinen nativen Umlauf.
Unvollstaendige Umlauffenster, andere Geometrien
und zusaetzliche Wechselwirkungskanaele sind
davon nicht ausgeschlossen.

## 4. Konsequenz und Verifikation

Der Minusdefekt ist robust gegen das Altern
innerhalb der **vorgegebenen** Spur. Das Hindernis
liegt davor, bei der Erzeugung der naechsten
Phase. Mehr Bahnphasen oder ein anderes Vorzeichen
des Skalar-Kernels allein beheben es nicht.
Eine naechste native Konstruktion muss eine
andere, phasenabhaengige Geometrie mit voller
Kraftbilanz liefern, bevor Stabilitaet oder
Kopplung zweier Kerne getestet werden.
Der Fernindex $+1$ der geschlossenen Spur
und damit der Restindex $+2$ ausserhalb
eines Minuskerns bleiben unveraendert.

Die [festen Kontrollen](../../tests/test_fifo_defect_phase_threshold.py)
pruefen alle zehn vorbereiteten Phasen beider
Vorzeichen, einen nichtorthogonalen affinen
Acht-Phasen-Vergleich sowie den nativen
tangentialen Vektor- und Skalarreadout an
beiden Spezialphasen. Die Ausschluesse sind
analytisch, nicht aus einer Stichprobe von
Retentionsfaktoren oder einer simulierten
Zielbahn abgelesen.
