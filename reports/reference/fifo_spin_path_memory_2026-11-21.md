# 720 Grad: Pfadvorzeichen und gespeicherter FIFO-Zustand

Stand: 2026-11-21. Kinematische Gegenprobe fuer
[die 4D-Spinreferenz](../../docs/reference/fifo_4d_spin_projection.md)
und [den nativen aktiven Zustand](four_cycle_active_form_2026-11-21.md).
Vorgeschriebene, alterskonsistente Kontrollfolgen, keine native
Zieltrajektorie, Parameterwahl oder neue Dynamik.

**Ergebnis.** Drei Kontrollfolgen mit null, einer und zwei
aeusseren Umdrehungen ergeben am Ende **denselben** vollen
FIFO-Zustand. Ihre aufgezeichneten Orientierungswege haben
trotzdem die Quaternion-Endzeichen $+,-,+$. Der Unterschied
ueberlebt also weder als Momentanreadout noch als dauerhafte
Eigenschaft eines festen FIFO-Fensters. Es ist ein
Pfadmerkmal. Auch in einem idealisierten unendlichen
exponentiell verblassenden Speicher kann ein *stetiges
diskretes* Label den Unterschied nicht dauerhaft bewahren.

## 1. Drei Folgen, echte FIFO-Ueberlappung

Sei $a_n=(r\cos(n\pi/2),r\sin(n\pi/2),(-1)^n h)^T$
die Referenz mit $r,h>0$ und allen Alterslabels. Setze
fuer $m=0,1,2$ und eine ganze Schrittzahl $N\geq32$

$$
\alpha_n^{(m)}=2\pi m\min(1,\max(0,n/N)),\qquad
x_n^{(m)}=R_z(\alpha_n^{(m)})a_n.
$$

Nur der jeweils neue Kopf wird so vorgeschrieben. Das
Fenster ist stets $Y_n^{(m)}=(x_n^{(m)},\ldots,x_{n-4}^{(m)})$;
es entsteht durch wirkliches Verschieben, nicht durch getrennte
Rotation aller gleichzeitig gespeicherten Eintraege.
Alle neuen Schritte haben Hoehendifferenz $2h$ im Betrag
und damit definierte Einheitsrichtungen. Fuer jedes
$n\leq0$ und $n\geq N$ stimmen die Kopfpositionen aller drei
Folgen exakt ueberein. Folglich gilt

$$
Y_{N+4}^{(0)}=Y_{N+4}^{(1)}=Y_{N+4}^{(2)}.
$$

Dies gilt einschliesslich des Vorgaengers der aeltesten
Richtung, also auch fuer alle aktiven Orts-/Richtungsdeposits.
Bei gleichen Kernelparametern ist jedes skalare oder
vektorielle Readout dasselbe. Gleiche weitere Inputs
und gleiche Rauschinkremente koppeln die Zukunft identisch.
Falls man diese Pfade als deterministisches Experiment
realisiert, ist der jeweils erforderliche additive Kopfinput
die Differenz zwischen Zielkopf und nativem Vorschlag. Die
Folgen werden hier lediglich analytisch vorgeschrieben;
es wird weder ein solcher Inputverlauf berechnet noch
eine autonome Erreichbarkeit behauptet.

## 2. Der Orientierungsweg verliert seinen Lift nicht

Aus den drei juengsten Orten bilde einen eigentlichen
Rahmen $F(Y)$. Die erste Achse zeigt von $y_2$ nach
$y_0$; die zweite zeigt in Richtung $y_1-(y_0+y_2)/2$
nach Abzug ihres Anteils entlang der ersten Achse. Die
dritte ist das Kreuzprodukt. Dies ist eine Variante des
[altersmarkierten Rahmenreadouts](../../docs/reference/fifo_structure_candidate.md).
Der phasenbereinigte relative Rahmen

$$
Q_n=F(Y_n)F(a_n,a_{n-1},a_{n-2})^T
$$

vergleicht mit derselben nativen Viererphase. Anders
wuerde die innere Umlaufphase mit dem aeusseren Drehweg
vermischt. Wir verbinden die Q-Samples entlang der
kuerzesten SO(3)-Wege; das ist eine deklarierte geometrische
Interpolation, keine Behauptung ueber Zwischenzeitphysik.

### Eindeutiger Lift ohne Fast-Kollinearitaet

Lasse m in der Notation weg und setze
$d_j=\alpha_n-\alpha_{n-j}$. Mit
$\delta=2\pi m/N\leq\pi/8$ gilt
$0\leq d_2\leq2\delta$ und
$|d_1-d_2/2|\leq\delta/2$. Interpoliere inner-
halb jedes Rahmens zwischen der starr bei $\alpha_n$
platzierten Referenz und dem echten Fenster: Benutze
fuer Ort $j$ den Winkel $\alpha_n-\tau d_j$,
$0\leq\tau\leq1$. Die Homotopie ist eine der
**Rahmenwege**, nicht eine zusaetzliche FIFO-Trajektorie.

Fuer jeden solchen Rahmen hat $y_0-y_2$ Laenge
$2r\cos(\tau d_2/2)>0$ und Azimut
$\beta=n\pi/2+\alpha_n-\tau d_2/2$.
Mit $e_\beta^\perp=(-\sin\beta,\cos\beta,0)^T$
ist der projizierte zweite Richtungspfeil

$$
-r A e_\beta^\perp -2(-1)^n h e_z,qquad
A=\cos(\tau(d_1-d_2/2))+\sin(\tau d_2/2).
$$

Das folgt durch Projektion des mittleren Punkts und
des Mittelpunkts der beiden anderen auf $e_\beta^\perp$.
Die Hoehenkomponente bleibt von null verschieden und
$1/2<A<2$. Der Rahmen ist fuer alle n und $\tau$
regulaer. Relativ zu $R_z(\alpha_n)$ unterscheiden
sich der Azimut um hoechstens $\delta$ und der
Kippwinkel um hoechstens $|\log A|/2$:
Fuer $k=2h/r$ hat $\arctan(k e^{-x})$ Ableitungsbetrag
hoechstens $1/2$. Der SO(3)-Winkelabstand zur
starren Referenz ist somit kleiner als
$\delta+(\log 2)/2$. Folglich bleibt der Abstand
zweier benachbarter Samples fuer die ganze Homotopie
unter $3\delta+\log 2<\pi$. Kein Schritt gelangt
an die Mehrdeutigkeit der kuerzesten Rotation.

Bei $n=0$ und $n=N+4$ ist $Q_n=I$ fuer alle $\tau$.
Die interpolierten Wege sind daher geschlossene
Schleifen am gleichen Basispunkt. Bei $\tau=0$
ist der Weg genau $m$-mal die z-Drehung.
Die Homotopie behaelt die Klasse bei $\tau=1$.
Der eindeutige Lift ab dem positiven Einheitsquaternion
endet folglich bei $(-1)^m$, obwohl Rahmen **und** voller
FIFO-Zustand am Ende identisch sind. Der bekannte
Halbwinkel ist hier eine Auswertung des ganzen
Rahmenwegs, kein neuer Zustand des Kopfupdates.

| Aeussere Drehung | Endrahmen | End-FIFO | Endzeichen des Pfadlifts |
| --- | --- | --- | --- |
| 0 Grad | Identitaet | gemeinsame Endhistorie | + |
| 360 Grad | Identitaet | gemeinsame Endhistorie | - |
| 720 Grad | Identitaet | gemeinsame Endhistorie | + |

## 3. Laengeres Fenster und exponentielles Gedaechtnis

Bei einem beliebigen festen Horizont H derselben
Orts-/Richtungsarchitektur reicht eine gemeinsame
Endfolge von H weiteren Updates, damit auch der
Vorgaenger der aeltesten aktiven Richtung uebereinstimmt.
Ein laengeres Fenster kann die Drehspur laenger
enthalten, aber nicht das unveraenderliche Vorzeichen
dieses Weges durch eine beliebig lange gemeinsame
Endfolge tragen.

Eine ideale unendliche Fortsetzung mit exponentiell
verblassenden Eintraegen ist davon zu unterscheiden.
Fuer einen festen Laengenmassstab $\ell>0$ und
$0<\vartheta<1$ verwende die normierte Abstandssumme

$$
d_\vartheta(X,X')=(1-\vartheta)\sum_{j\geq0}\vartheta^j
\left(\frac{|y_j-y_j'|}{\ell}+|p_j-p_j'|\right).
$$

Die Folgen bleiben beschraenkt und die Summe ist endlich.
Die gemeinsam neu eingefuegten Deposits ab $n>N$ sind
exakt gleich; alles Vorherige altert gemeinsam. Darum
gilt nach k Warteupdates sogar exakt

$$
d_\vartheta(X_{N+k}^{(m)},X_{N+k}^{(0)})
=\vartheta^k d_\vartheta(X_N^{(m)},X_N^{(0)}).
$$

Der unendliche Ausgangsspeicher ohne aeussere Drehung ist
in jeder der vier Phasen ein fester Zustand. Entlang jeder
dieser Phasenfolgen konvergieren also auch die beiden
gedrehten Historien im gewichteten Mass zu demselben
Ausgangszustand. Ein dort stetiges Readout mit diskretem
Wertebereich $\{+1,-1\}$ muss fuer hinreichend grosses
k mit der Basisfolge uebereinstimmen. Ein unstetiger
Decoder, der beliebig schwach gewordene alte Eintraege
ausliest, wird damit nicht ausgeschlossen; eine mit
dieser Topologie robuste Vorzeichenerhaltung schon.
Es wird kein nativer unendlicher Bewegungsverlauf
simuliert oder vorausgesetzt.

Die [stochastische Folgeanalyse](fading_memory_future_mixing_2026-11-21.md)
ersetzt die hier vorgeschriebene gemeinsame Endfolge durch eine
Kopplung der nativen bedingten Inkrementgesetze bei positivem Rauschen.
Sie kontrolliert die statistische Zukunft, nicht das formale Tail.

## 4. Konsequenz fuer einen Spinbenchmark

Der aktuelle Zustand kann den Unterschied **dieser**
zwei Pfadklassen nach Zusammenfallen der Historien
nicht anzeigen. Auch eine kontinuierliche Wahl eines
Liftquaternions auf dem ganzen starren Orientierungsorbit
ist unmoeglich: Die geschlossene 2-Pi-Folge muesste
zugleich bei ihrem Anfangsquaternion und nach Weghebung
bei dessen Negativ enden. Das ist die bekannte
Doppelueberlagerung, nicht ein neuer Spinsatz.

Ein Kandidat mit echter 720-Grad-Antwort muesste zeigen,
wo die relative Phase weiterhin dynamisch unterscheidbar
bleibt, etwa in nicht zusammenfallenden internen Zustaenden
oder in einer hergeleiteten Transportregel auf einer
Ueberlagerung und einem relativen Ausleseprotokoll.
Eine nachtraeglich multiplizierte Folge von Quaternionen
genuegt nicht. Die Gegenprobe schliesst weder andere
native Pfade aus, die eine dauerhafte Deformation
zuruecklassen, noch zusaetzliche interne Dynamik oder
eine spaetere Quantisierung.

[Shoemake, SIGGRAPH 1985](https://doi.org/10.1145/325334.325242)
beschreibt Quaternion-Interpolation von Raumrotationen.
[Krusch und Speight](https://arxiv.org/abs/hep-th/0503067)
verwenden Schleifen im Faddeev-Hopf-Konfigurationsraum
fuer explizit eingefuehrte Finkelstein-Rubinstein-
Quantisierungsbedingungen. Hier kommt der neue
Unterschied aus der FIFO-konsistenten gemeinsamen
Endfolge, nicht aus einer Quantisierung der Rahmen.

Die [zehn festen Kontrollen](../../tests/test_fifo_spin_path_memory.py)
pruefen die kurzen Rahmenintervalle, die Liftzeichen,
die exakte Endgleichheit samt Richtungsdeposits und die
geometrische Abschwaechung des alten Pfadunterschieds.
84 Tests im betroffenen Panel bestehen. Keine Zielsimulation,
kein Spin- oder Teilchennachweis.
