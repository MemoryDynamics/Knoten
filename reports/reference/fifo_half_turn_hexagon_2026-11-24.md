# Treues FIFO-Sechseck mit echter Impulsumkehr im Speicher

Stand: 2026-11-24. Fortsetzung des
[Phasenausgleichs beim Sechseck](fifo_restored_hexagon_2026-11-24.md).
Dieselbe Kopierkarte, derselbe autonome Rotor und dieselben
sechs Schreiborte. Die Kraftprofile werden jedoch neu
gewaehlt. Keine native Zieltrajektorie und kein Scan.

**Ergebnis.** Eine zweite exakte Konstruktion braucht fuer
eine Speichermode *keine* ganze Periode zwischen Writes.
Sie startet und endet bei modaler Koordinate null, kehrt
aber einen nichtverschwindenden Impuls um. Die Historie
ist an jedem Schnitt treu. Mit den anderen beiden internen
Speichermoden auf ganzen Perioden ist diese Konstruktion
fuer jedes positive Speichermassenverhaeltnis quer instabil.
Das Hindernis liegt hier nicht an einer internen freien Drift.

## 1. Welche einzelne Mode netto Impuls uebertragen darf

Setze $\lambda=e^{i\pi/3}$ und
$T=\pi/(3\omega)$. In der Bewegungsebene schreiben wir
$x=X$, $b=-X$ und $y_j=\lambda^{-j-1}X$.
Der Write behaelt Kopf und Traeger am Ort und schreibt
treu, weil $y_2=b$. Fuer
$D=P_x-P_b=2i m\omega X$ behaelt der Write den relativen
Impuls genau dann, wenn $P_{y_2}=-P_b$.
Der relative Flug dreht dann $d=x-b$ und $D$ um $\lambda$.

Wenn nur eine reelle, translationsinvariante Speichermode
netto Impuls uebertraegt, erzwingt die Shift-Gleichung
des vorigen Berichts
$g_0+\lambda g_1+\lambda^2g_2=0$ fuer ihren Registerteil.
Da $\lambda^2=\lambda-1$ und $\lambda$ nicht reell
ist, bleibt nur die Richtung $(1,-1,1)$.
Im Schwerpunkt-Speicher-Teil $(c,y_0,y_1,y_2)$
ist damit der Kovektor

$$
\ell=(-1,1,-1,1)^T .
$$

Seine Koordinate nach dem Write ist null:
$c=0$ und $x(1-\lambda^{-1}+\lambda^{-2})=0$.
Bei nichtverschwindendem Impuls kann die Mode
an denselben Ort mit umgekehrtem Impuls zurueckkehren,
wenn $\Omega_\ell T$ eine ungerade Halbperiodenzahl ist.
Wir setzen $\Omega_\ell=3\omega$. Das ist eine andere
Richtung als der massenorthogonale Zusatz des
vorigen Modells mit dessen beiden alten Kraftprofilen.

Ein konkretes positiv quadratisches Hamiltonian:
Im vollen Ortsvektor $(x,y_0,y_1,y_2,b)$ liegt
$g=(-1/2,1,-1,1,-1/2)^T$.
Mit der inversen Massenmatrix $R$ ergaenzen
$e=(1,0,0,0,-1)^T$,
$a=(0,1,0,-1,0)^T$ und
$v=(1/2,-1/4,-1/2,-1/4,1/2)^T+\tau g$
die massenorthogonale Basis ohne Translation, wobei
$\tau=1/(1+6m/\mu)$.
Die Frequenzen sind $\omega,3\omega,6\omega,12\omega$
fuer $e,g,a,v$. Jeder Potentialterm lautet fuer
seinen Kovektor $l$ und seine Frequenz $\Omega_l$
$\Omega_l^2|l^Tq|^2/(2l^TRl)$. Die Gesamtkopplung
ist konservativ und positiv, aber $g$ verwendet
gemischte Vorzeichen statt konvexer Einzelgewichte.
Die Massennormalisierung ist kein aus Memory
hergeleiteter Mechanismus.

## 2. Impulse, Energie und echter Umlauf

Sei $F$ der modale Impulszuwachs, sodass der
Schwerpunkt-Speicher-Impuls waehrend des Flugs
um $F\ell$ zunimmt. Schreibe $p=P_b$,
$A=P_{y_0}$, $B=P_{y_1}$ und $Q=P_x+P_b$.
Die Rotationsgleichungen fuer diesen Teil sind

$$
\lambda Q=D-F,\quad
\lambda A=p+F,\quad
\lambda B=A-F,\quad
\lambda P_{y_2}=B+F.
$$

Es genuegt zu setzen

$$
\begin{aligned}
F&=\frac{D}{1/2+i\sqrt3\,m/\mu},\\
p&=\frac{(1-\lambda)D-F}{2\lambda},\qquad
Q=D+2p,\\
A&=(p+F)/\lambda,\qquad
B=(A-F)/\lambda,\qquad P_{y_2}=-p.
\end{aligned}
$$

Die letzte Shift-Gleichung und Gesamtimpuls null
folgen aus $\lambda^2-\lambda+1=0$.
Die Vorschrift fuer $F$ kommt aus der Halbperiode:
Der Schwerpunkt-Speicher-Impuls nach dem Write
ist $(D,p,A,B)$; seine Projektion in Richtung $\ell$
wird im Flug verdoppelt abgezogen. Mit
$N=1/(2m)+3/\mu$ fordert dies

$$
F=-\frac2N\left[-\frac{D}{2m}
+\frac{p-A+B}{\mu}\right],\qquad
p-A+B=-(1+\lambda^{-1})F .
$$

Der komplexe Phasenanteil ist entscheidend. Eine
rein reelle Skalierung von $D$ fuer $F$ wuerde
im Allgemeinen die Energiebedingung verfehlen.
Hier hat $D-F$ genau den Betrag von $D$, also
$|Q|=|D|$. Am Write bleiben die kinetischen
Energieterme im Schwerpunkt-Speicher-Teil gleich:
Die Registerimpulsbetraege werden nur permutiert,
und $Q^+=D$. Auch die relativen Impulse behalten
ihre Energie. Die Ortsdaten dieses Teils werden
beim exakten Schreiben gedreht, nicht verzerrt,
und die relative Lage bleibt gleich.

Damit ist die gesamte Schnittarbeit null. Der
Rotor darf mit $\pi_s=M_sL/T$ frei laufen.
Die beiden ganzen Moden kehren komplett zurueck;
die Halbperiodenmode kehrt nur mit umgekehrtem Impuls
zurueck. Zusammen ergibt das genau die verlangte
Drehung des vollen Zustands. Nach sechs Writes
ist auch der Gesamtzustand geschlossen, bei
endlicher Energie und ohne Zeitreset.

## 3. Querinstabilitaet bei jeder positiven Masse

Wie zuvor ist die Rotorzeit gegen eine senkrechte
Stoerung in erster Ordnung unveraendert. Die
Translation kann bei festem Gesamtimpuls entfernt
werden. In Einheiten $m=\omega=1$ seien
$P=ee^T/2$, $U=I-P/2$, $C$ der Orts-Write und
$G=C^{-T}$. Die Halbperiode subtrahiert im Ortsblock
$2Rg g^T/(g^TRg)$ und im Impulsblock die Transponierte.
Mit

$$
A_\tau=U-\frac{2Rg g^T}{g^TRg}
$$

ist die Querableitung nach einer Skalierung der
Impulskoordinaten aehnlich zu
$\begin{psmallmatrix}
A_\tau C&3PG/4\\-PC&A_\tau^T G
\end{psmallmatrix}$.
Der Vektor $Rg/(g^TRg)$ ist affin in $\tau$.
Die $\tau$-Aenderung der ganzen Matrix hat Rang
hoechstens zwei; jedes Koeffizientenpolynom
der Determinante ist daher hoechstens quadratisch
in $\tau$.

Mit $u=\xi+\xi^{-1}$, fuer einen Eigenwert $\xi$,
ergibt sich

$$
\det(\xi I-J)=\xi^5(u-2)(u-1)
\left[u^3-3u^2+B_\tau(u+2)-17/4\right],
\qquad B_\tau=\frac{37-2\tau-8\tau^2}{18}.
$$

Das reduzierte reziproke Polynom ist ein
Standardwerkzeug fuer
[symplektische Spektralstabilitaet](https://www.sciencedirect.com/science/article/pii/037596018790836X).
Die [rationalen Kontrollen](../../tests/test_fifo_half_turn_hexagon.py)
pruefen alle Koeffizienten an drei algebraischen
Interpolationsknoten, nicht an drei simulierten
Massen. Das schliesst den Grad-zwei-Vergleich exakt.
Die Klammer ist bei $u=2$ gleich
$-(1+8\tau)^2/36<0$. Sie ist sogar bei
$u=221/110$ negativ, da $B_\tau\le B_0$ und der
Wert bei $\tau=0$ dort negativ ist. Fuer
$u\to+\infty$ ist die Klammer positiv.
Also gibt es fuer alle $0<\tau<1$ einen
reellen Eigenwert $\xi>11/10$. Im vollen
Sechs-Schritt-Return bleibt dieser Faktor
zur sechsten Potenz. Bei gleichen Massen
zeigt die feste numerische Kontrolle, dass
dieser wachsende Zweig den Kopierfehler trifft.
Die Aussage betrifft Querstoerungen in
mindestens drei Dimensionen, nicht ein
Stabilitaetsurteil allein in der Ebene.

## 4. Einordnung

[Code](../../experiments/current/reference/fifo_carrier_clock_cycle.py)
und [feste Kontrollen](../../tests/test_fifo_half_turn_hexagon.py)
pruefen zwei volle Umlaeufe mit treuer Historie,
den nichtverschwindenden Impulswechsel, das
rationale Polynom und eine Querableitung.

Die alte Voraussetzung ganzer Perioden fuer
alle Moden war nicht grundsaetzlich noetig.
Eine einzelne Impulsumkehr traegt die Bahn
tatsaechlich, stabilisiert sie aber nicht.
Offen ist der andere Fall aus dem Phasenausgleich:
mehrere nichtganzzahlige Moden mit jeweils
nichtverschwindender Ortsprojektion und
kompensierenden Impulsaenderungen.
