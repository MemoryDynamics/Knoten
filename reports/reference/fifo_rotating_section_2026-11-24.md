# Welche Schreibgeometrien der synchronisierte FIFO traegt

Stand: 2026-11-24. Fortsetzung des
[beweglichen FIFO-Speichers](fifo_mobile_memory_cycle_2026-11-24.md).
Keine native Zieltrajektorie und keine Suche ueber Massen
oder Winkel.

**Ergebnis.** Beim selben reversiblen Write, dem Zentrum aus
den zwei juengsten Eintraegen und konstanter Flugzeit
$T=\pi/\omega$ gibt es in den folgenden Klassen keine
periodische Folge von mehr als zwei Kopfpositionen am
Schreibschnitt: jede ungerade Laenge ab drei bei jedem
ganzzahligen Frequenzverhaeltnis $r=\Omega/\omega>1$,
sowie $H=3$ bei gleichen Massen und in einer offenen
Umgebung davon. Auch eine starre Rotation um einen
Winkel ungleich $0$ oder $\pi$ pro Write ist ausgeschlossen.
Das ist ein Existenz-Ausschluss in den genannten
Klassen, unabhaengig von der bisherigen Stabilitaetsrechnung.
Ueber Pfade zwischen den Schnitten oder wechselnde
Flugzeiten sagt er nichts.

## 1. Was eine rotierende Schreibfolge erfordern wuerde

Der Orts- und Impulsteil eines Vorwaerts-Writes ist
$(C,C^{-T})$, gefolgt vom exakten Hamilton-Flug.
Bei festem $T$ ist der gesamte Register-Return eine
reelle lineare Matrix $J$ je Raumkoordinate. Hier geht
es um den **exakten** Return auf Bahnen mit dieser
Flugzeit, nicht nur um eine Linearisierung der Zweiperiode.
Andere Bahnen koennen ueber Arbeit am Schnitt einen
anderen Rotorimpuls und damit andere Flugzeiten haben.

Eine starre Drehung zwischen zwei Schnitten waere eine
relative periodische Bahn im Sinn von
[Wulff, Lamb und Melbourne](https://doi.org/10.1017/S0143385701001298).
Zwei Koordinaten der Rotationsebene lassen sich als
Real- und Imaginaerteil eines Registervektors auffassen.
Sie verlangen einen Eigenwert $e^{i\theta}$ von $J$,
wenn sich die Register von Write zu Write um $\theta$
drehen. Allgemeiner koennen exakt periodische Ortsfolgen
nur durch Wurzeln der Einheit im Spektrum getragen
werden. Das folgt auch fuer die Kopfprojektion allein
aus der von $J$ vorgegebenen linearen Rekursion. Wenn
die einzigen Einheitskreis-Nullstellen $\pm1$ sind,
koennen periodische Folgen nur konstant oder alternierend
sein. Jordan-Anteile koennen keine weiteren periodischen
Punkte erzeugen.

Der exakte Kopierfehler $b-y_{H-1}=0$ waere dabei eine
zusaetzliche Bedingung. Hier fehlt in den genannten
Faellen bereits die erforderliche Mode, selbst bevor
man die Kopierbedingung stellt. Eine reine Rotation
erhaelt ausserdem die interne Energie. Bei autonomer
positiver Rotorbewegung kann sie daher nicht gleichzeitig
den Betrag des Rotorimpulses von Schritt zu Schritt
aendern.

## 2. Ganzzahlige Frequenzen: Ausschluss auf dem Einheitskreis

Fuer ganzzahliges $r$ hat $J$ die Diagonalbloecke
$B,B^{-T}$ aus dem beweglichen Referenzmodell. Es
genuegt daher, Einheitskreis-Nullstellen von $B$
zu bestimmen.

**Gerades $r$.** Aus dem Orts-Polynom folgt fuer
$|\lambda|=1$

$$
1=|\lambda^{H+2}|=|\lambda^2-\lambda-1|
=|-1+2i\sin\theta|,\qquad \lambda=e^{i\theta}.
$$

Dies ist nur bei $\sin\theta=0$ moeglich.

**Ungerades $r\ge3$.** Nach Abspalten von $\lambda+1$,
mit $\alpha=1/r^2$, hat das Polynom die Form
$\lambda^{H-1}A(\lambda)+D(\lambda)$, wobei
$A=\lambda^2-2\alpha\lambda-\alpha$ und
$D=-2(1-\alpha)\lambda^2+\alpha\lambda+1$.
Auf dem Einheitskreis muss $|A|=|D|$ gelten.
Mit $c=\cos\theta$ ergibt sich

$$
|D|^2-|A|^2
=(1-c)\bigl[(8-12\alpha)c+8-14\alpha\bigr].
$$

Ausser $c=1$ bliebe nur
$2c=-2+1/(2r^2-3)$. Dies verlangt fuer
$\lambda$ die primitive ganzzahlige Gleichung

$$
(2r^2-3)\lambda^2+(4r^2-7)\lambda+2r^2-3=0 .
$$

Sie ist ueber den Rationalen irreduzibel, weil
$-1<c<1$ und beide Wurzeln nicht reell sind.
Nach dem Gauss-Lemma muesste ihr Leitkoeffizient
$2r^2-3$ den Leitkoeffizienten $r^2$ des mit
$r^2$ multiplizierten Orts-Polynoms teilen.
Das ist fuer $r\ge3$ unmoeglich. Auch hier sind
also $\pm1$ die einzigen Einheitskreis-Nullstellen.
Der Ausschluss gilt insbesondere fuer Dreieck,
Viereck und beliebig viele Schreibpunkte, ohne
einen Winkel zu probieren.

## 3. Gleiche Massen: rationale Fehlerschranke

Fuer $H=3$, $\mu=m$, ist $r=\sqrt2$; der Orts-
und Impulsblock faktorisiert nicht mehr. Die volle
$10\times10$-Matrix $J$ ist jedoch symplektisch.
Ein Eigenvektor zu $+1$ ist die gemeinsame
Translation, einer zu $-1$ die kollineare
Alternation mit Impulsen null. Aus der reziproken
Form des charakteristischen Polynoms folgt daher
mit $u=\lambda+\lambda^{-1}$

$$
\det(\lambda I-J)
=(\lambda^2-1)^2\lambda^3 f(u),\qquad
f(u)=u^3+a u^2+b u+c_0 .
$$

Eine weitere Einheitskreis-Nullstelle braeuchte
$u\in[-2,2]$. Mit $m=\omega=1$ werden $\pi$,
$\cos(\sqrt2\,\pi)$ und $\sin(\sqrt2\,\pi)/\sqrt2$
durch rationale Zentren mit Fehler kleiner $10^{-6}$
eingeschlossen. Machins Formel, alternierende
Arctangensreihen und Taylorreste der trigonometrischen
Funktionen genuegen. Aus den Flugprojektoren und
der Schreibmatrix folgt fuer die rationale
Matrix $J_0$ der induzierte Normfehler
$\|J-J_0\|_\infty<11\cdot10^{-6}$ und
$\max(\|J\|_\infty,\|J_0\|_\infty)<16$.
Die Differenz der Spuren der ersten drei Potenzen
folgt per Teleskopsumme; die Newton-Identitaeten
geben daraus $a>1.3$, $0<b<0.3$, $c_0>5$.
Somit ist $f$ auf $[-2,0]$ groesser als
$-2.8-0.6+5>0$, und auf $[0,2]$ ebenfalls positiv.

Die [rationalen Kontrollen](../../tests/test_fifo_rotating_section.py)
setzen diese Schranken mit exakten Bruechen um und
gleichen die Matrix mit dem implementierten
Referenzflug ab. Der Ausschluss kommt nicht aus
gerundeten Eigenwerten nahe $\pm1$. Da die beiden
exakten Symmetrie-Eigenvektoren erhalten bleiben
und das Restpolynom strikt positiv auf einem
kompakten Intervall ist, gilt der Ausschluss auch
fuer Massenverhaeltnisse in einer offenen Umgebung
von $\mu/m=1$ bei $H=3$. Die Breite dieser Umgebung
wird hier nicht bestimmt.

## 4. Weiterer Diskriminator

Es gibt keinen Stabilitaetstest fuer ein synchron
rotierendes Vieleck, solange es in der gewaehlten
Dynamik gar nicht existiert. Nicht ausgeschlossen
sind andere konstante Flugzeiten sowie mehrschrittige
Bahnen mit internem Energieaustausch am Rotor.
Letztere muessen bei Schreibarbeit $\Delta E_n$
die Timing-Bilanz

$$
\Delta E_n=\frac{M_sL^2}{2}
\left(T_{n-1}^{-2}-T_n^{-2}\right)
$$

erfuellen; die Flugzeiten duerfen nicht unabhaengig
gesetzt werden. Eine nichtkollineare Kopierfolge mit
dieser Bilanz waere ein echter Vergleich zur
vorbereiteten kollinearen Zweiperiode.
