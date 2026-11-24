# FIFO-Sechseck mit zwei kompensierenden Speicherphasen

Stand: 2026-11-24. Fortsetzung des
[Sechsecks mit einer Impulsumkehr](fifo_half_turn_hexagon_2026-11-24.md).
Dieselbe autonome Uhr und reversible Kopierkarte, andere konservative
Kraefte. Keine native Zieltrajektorie und kein Parameterscan.

**Ergebnis.** Auch zwei Speichermoden mit nichtverschwindenden
Ortskoordinaten koennen ihre Impulse so umkehren, dass alle
sechs Writes die Historie treu erhalten. Beide Phasen liegen
zwischen ganzen und halben Perioden. Fuer die explizite
Konstruktion mit $\mu/m=16/9$ bleibt jedoch eine
Querinstabilitaet bestehen: Intervallarithmetik belegt einen
reellen Einzelmultiplikator zwischen $-1.2$ und $-1.1$.
Das ist ein konkreter Zweiphasen-Vergleich, kein allgemeiner
Ausschluss kompensierender Moden.

## 1. Erst Impulse und Geometrie, dann Frequenzen

Sei $\lambda=e^{i\pi/3}$ und wie bisher
$T=\pi/(3\omega)$, $x=X$, $b=-X$,
$y_j=\lambda^{-j-1}X$ am Schnitt. Bei
$D=P_x-P_b=2i m\omega X$ erhaelt der Write den
relativen Impuls, falls $P_{y_2}=-P_b$. Der
relative Flug dreht dann $d=x-b$ und $D$ um $\lambda$.

Im Schwerpunkt-Speicher-Teil $z=(c,y_0,y_1,y_2)$
sind die Ortsdaten an beiden Enden eines Flugs
identisch. Die harmonischen Eigenmoden koennen daher
entweder ihren Impuls behalten (ganze Periode) oder
umkehren. Bezeichne mit $\mathsf U$ den vollen
Schwerpunkt-Speicher-Impuls direkt nach dem Write
und mit $\mathsf V$ den Impuls am Flugende.
Schreibe $p=P_b$, $A=P_{y_0}$, $B=P_{y_1}$
und $Q=P_x+P_b$. Fuer die gewuenschte Rotation gilt

$$
\mathsf U=(D,p,A,B)^T,\qquad
\mathsf V=\lambda(Q,A,B,-p)^T,\qquad Q=D+2p .
$$

Sind zwei Richtungen reflektiert und eine bleibt
erhalten, muss $\mathsf U+\mathsf V=\sigma n$
fuer eine reelle, translationsinvariante Richtung
$n=(n_c,a,b_1,d_1)^T$ gelten. Sei
$K=a-\lambda b_1+\lambda^2d_1$. Aus der Kopierkarte
folgen direkt

$$
\sigma=\frac{(1+\lambda)D}{n_c-\lambda K},\qquad
p=\frac{\sigma K}{2},\qquad
A=\frac{-p+\sigma a}{\lambda},\qquad
B=\frac{-A+\sigma b_1}{\lambda}.
$$

Damit die Reflexion in der Massenmetrik
kinetische Energie erhaelt, muss
$n^TR_z(\mathsf U-\sigma n/2)=0$ gelten.
Mit $r=m/\mu$, $s=a+b_1+d_1=-n_c$ und
$R_z=\operatorname{diag}(1/(2m),1/\mu,1/\mu,1/\mu)$
reduzieren sich Real- und Imaginaerteil auf

$$
s(a-d_1)=0,\qquad
b_1s+2r(ab_1-ad_1+b_1d_1)=0 .
$$

Dies grenzt moegliche erhaltene Richtungen ohne
Frequenzsuche ein. Wir setzen $a=d_1=1$ und
$b_1=1/4$, woraus $r=9/16$ und
$n=(-9/4,1,1/4,1)^T$ folgen. Die alternative
Richtung mit $s=0$ und
$a^2+ab_1-b_1^2=0$ wurde hier nicht auf
Stabilitaet untersucht.

## 2. Zwei Frequenzwurzeln ohne Orbit-Suche

Im Rest der Rechnung sind $m=\omega=1$.
Die $R_z$-orthogonale Ergaenzung von $n$ und der
Translation hat die Kovektoren
$g_a=(0,1,0,-1)^T$,
$g_s=(2/3,1,-8/3,1)^T$
mit Massen-Normen zum Quadrat $9/8$ und $385/72$.
Normiere beide auf eins. Die modalen Ortswerte
von $z^+=(0,X,\lambda^{-1}X,\lambda^{-2}X)^T$
und die modalen Startimpulse aus $\mathsf U$
sind durch die reelle symmetrische Matrix

$$
K_{\rm ret}=\frac1{224}
\begin{pmatrix}
15\sqrt3&5\sqrt{1155}\\
5\sqrt{1155}&-77\sqrt3
\end{pmatrix}
$$

verbunden. Konkret liefert die Matrix aus den zwei
Ortskoordinaten die zwei Impulskoordinaten im
normierten Basisraum $(g_a,g_s)$. Die Umlaeufe
beider Raumkomponenten benutzen dieselbe Matrix.
Diagonalisiere sie mit Eigenwerten
$\eta_\pm=(-31\sqrt3\pm\sqrt{35223})/224$.
Fuer jede dieser Richtungen mit modalem
Startimpuls $\eta q$ ist genau

$$
\Omega\tan(\Omega T/2)=\eta
$$

noetig, um an denselben Ort mit umgekehrtem Impuls
zurueckzukehren. Waehle die eindeutige positive
Wurzel auf $(0,3)$ fuer $\eta_+>0$ und auf
$(3,6)$ fuer $\eta_-<0$. Auf dem ersten Zweig ist
die linke Seite strikt steigend von null nach
$+\infty$, auf dem zweiten von $-\infty$ nach
null. Die Frequenzen liegen bei etwa $1.01612$
und $5.63942$. Die Mode $n$ hat Frequenz sechs,
also genau eine ganze Periode. Alle internen
Kopplungen sind positive quadratische Potentiale
der entstehenden massenorthogonalen Moden.

Der vorgegebene Flug dreht damit den gesamten
Zustand um $\lambda$. Da die interne Energie im
Flug und unter dieser Drehung erhalten ist, ist die
Schnittarbeit null. Der freie Rotor laeuft mit
$\pi_s=M_sL/T$ weiter und erzeugt genau den
geprueften Flug. Der Write erfasst in jedem Schritt
den tatsaechlichen Kopf; die beweglichen Eintraege
nehmen an der naechsten Schnittflaeche wieder
ihre echten historischen Werte an. Nach sechs
Schritten sind auch Impulse und Uhr geschlossen.
Die beiden Zahlenwurzeln bestimmen einzelne
Normalfrequenzen, nicht einen Treffer aus
Trajektorien oder einem Parameterbereich.

## 3. Querinstabilitaet durch ein Intervallvorzeichen

Die Rotorzeit ist gegen eine senkrechte Stoerung
in erster Ordnung unveraendert. Die Querableitung
$J$ besteht daher aus dem linearen Flug und der
kanonischen Schreibkarte. Die reine Translation
kann aus dem Flugdrift entfernt werden, da der
Gesamtimpuls erhalten ist und nur diese
Translationsrichtung speist. Sie hat keinen
Einfluss auf die Eigenwerte.

Die [Intervallkontrolle](../../tests/test_fifo_compensated_hexagon.py)
schliesst die beiden eindeutigen Frequenzwurzeln
durch Vorzeichen an rationalen Endpunkten ein.
Aus den Spektralprojektoren von $K_{\rm ret}$
und der Frequenzgleichung folgen die Flugbloecke
ohne kritische Winkelauswertung:

$$
\cos(\Omega T)-1=\frac{-2\eta^2}{\Omega^2+\eta^2},
\quad
\frac{\sin(\Omega T)}{\Omega}=\frac{2\eta}{\Omega^2+\eta^2},
\quad
-\Omega\sin(\Omega T)=\frac{-2\eta\Omega^2}{\Omega^2+\eta^2}.
$$

Fuer den symplektischen Rueckkehrblock, wie in der
[Spektralstabilitaet von Howard und MacKay](https://wrap.warwick.ac.uk/id/eprint/25081/),
liefern die nach aussen gerundeten Intervalle

$$
\det(-1.2 I-J)>0,\qquad
\det(-1.1 I-J)<0 .
$$

Dazwischen liegt ein reeller wachsender Multiplikator.
Die Ableitung des tatsaechlichen autonomen Returns
bestaetigt numerisch die reine Flug-und-Write-Matrix.
Der feste Eigenvektortest zeigt einen nichtverschwindenden
Anteil im Kopierfehler $b-y_2$. Die volle Sechs-Schritt-Bahn
ist folglich in mindestens drei Dimensionen
linear instabil. Fuer Stoerungen allein in der Ebene
wird hier kein Stabilitaetsurteil behauptet.

## 4. Reichweite

[Referenzcode](../../experiments/current/reference/fifo_compensated_hexagon.py)
und [Kontrollen](../../tests/test_fifo_compensated_hexagon.py)
pruefen einen Umlauf ohne Reset, beide nichttrivialen
Impulsumkehrungen, die Intervallvorzeichen und die
volle Querableitung.

Dass zwei angeregte Phasen ihre Impulse ausgleichen
koennen, ist jetzt konstruktiv belegt. Nicht belegt
sind robuste Bindung und eine Auswahl dieser
Kopplung aus der nativen Knoten-Dynamik. Die
algebraisch andere erhaltene Richtung und andere
Frequenzzweige bleiben offen; der hier ausgeschlossene
Fall darf nicht auf alle Kompensationen verallgemeinert werden.
