# Zwei FIFO-Fenster als relativer Drehweg-Vergleich

Stand: 2026-11-22. Fortsetzung der
[relativen 4D-Auslese](fifo_4d_relative_phase_2026-11-22.md) und der
[Pfadgegenprobe](fifo_spin_path_memory_2026-11-21.md). Feste Geometrie
und exakte Referenz-Updates, keine native Zieltrajektorie.

**Ergebnis.** Eine rein aus gespeicherten 3D-Rahmen berechnete
relative Pfadauslese erkennt zwei entgegengesetzte Halbdrehungen
trotz gleicher Start- und Endpose. Drei Altersproben pro Arm reichen
und sind unter der Kurzweg-Konvention minimal. Dabei kann ein
einzelner Richtungspfeil auf beiden Wegen die ganze Zeit gleich
bleiben. Der Vergleich braucht keine gemeinsame interne 4D-Basis,
aber vollstaendige Rahmen, eine Altersreihenfolge und korrespondierende
Koerperachsen. Er liest einen relativen Drehweg, keinen privaten
Vorzeichenwechsel bei identischen gesamten Rahmenfolgen.

## 1. Auslese und Zweigwahl

Seien $R_{k,j}\in SO(3)$ die chronologisch geordneten Rahmen des
Arms $k=A,B$. Entferne die jeweilige Ausgangspose:
$P_{k,j}=R_{k,0}^T R_{k,j}$. Ein beliebiger *konstanter*, auch
zwischen den Armen verschiedener Laborbasiswechsel
$R_{k,j}\mapsto G_kR_{k,j}$ kuerzt sich dabei heraus. Die lokalen
Koerperachsen muessen in beiden Armen gleich bezeichnet sein, damit
die so erhaltenen relativen Posen verglichen werden koennen.
Dies ist keine Invarianz unter zeitabhaengigen Bezugssystemen.

Verbinde die $P_{k,j}$ ueber kuerzeste Drehwege mit Winkel unter
$\pi$. Hebe den Weg ab dem Einheitsquaternion stetig an: Unter
den beiden Quaternionen der naechsten Pose waehlt man das mit
positivem euklidischem Skalarprodukt zum bisherigen. Bei einem
Drehabstand von $\pi$ ist diese Wahl mehrdeutig. Das ist die bekannte
Quaternion-Weghebung fuer kurze Drehintervalle, vgl.
[Shoemake (1985)](https://doi.org/10.1145/325165.325242).
Seien $q_A,q_B$ die angehobenen Endpunkte. Bei gleichen Endposen
gilt $q_A=\pm q_B$; das relative Zeichen ist
$s=\operatorname{sgn}(q_A\cdot q_B)$. Bei leicht verschiedenen
Endposen schliesst das Vorzeichen des Skalarprodukts den Weg
noch immer ueber den kuerzesten Endpunktbogen. Auch dieser
Zusammenschluss ist nur bei Winkelabstand unter $\pi$ eindeutig.
So gelesen ist $s$ die Liftklasse der Schleife: Arm A vorwaerts,
kurzer Endpunktbogen, Arm B rueckwaerts.

## 2. Zwei echte Updates, drei Proben

Initialisiere zwei [aktive FIFO-Fenster](../../docs/reference/fifo_4d_spin_projection.md#aktiver-fifo-der-speicher-liefert-den-naechsten-schritt)
mit der gleichen Startpose und gegenlaeufiger Drehachse. Zwei
Anwendungen derselben Referenzregel $F(u_0,u_1,u_2,u_3)=
(-u_3,u_0,u_1,u_2)$ erzeugen als drei juengste Rahmen je

$$
P_A=(I,R_x(\pi/2),R_x(\pi)),\qquad
P_B=(I,R_x(-\pi/2),R_x(-\pi)).
$$

Die letzten Posen sind gleich. Die Lift-Endpunkte sind aber die
beiden entgegengesetzten reinen x-Quaternionen, also $s=-1$.
Der statische Richtungsreadout ist in beiden Armen und bei jedem
Zwischenschritt $+e_x$: Er liegt auf der Drehachse. Das ist ein
konkreter Informationsverlust bei Projektion eines vollen Rahmens
auf nur eine Richtung, nicht bei der Verwendung von 3D an sich.

Die Probe ist minimal bei exakt gleichen relativen Endposen:
Eine Schleife mit negativem Lift muss auf der Einheits-$S^3$
Antipoden verbinden, also dort Bogenlaenge mindestens $\pi$
haben. Auf $SO(3)$ entspricht das einer Winkelweglaenge von mindestens
$2\pi$. Zwei Proben pro Arm liefern insgesamt nur zwei kurze
Boegen der jeweiligen Laenge strikt kleiner als $\pi$ und
koennen daher keinen negativen Lift geben. Vier Vierteldrehungen
erreichen die Schranke. Allgemein gilt bei einer maximalen
Winkellaenge $h<\pi$ pro Intervall und $H$ Proben pro Arm die
notwendige Bedingung $2(H-1)h\geq 2\pi$.

## 3. Fehlertoleranz und Vergessen

Gegenueber einem Vergleich mit gleichen relativen Endposen
werde jede Probe in beiden Armen um hoechstens $\epsilon$ im
$SO(3)$-Winkelabstand gestoert. Ist der groesste ungestoerte
Nachbarabstand $h$, dann bleibt das Zeichen sicher stabil unter

$$
h+2\epsilon<\pi,\qquad 4\epsilon<\pi.
$$

Beweis: Verschiebe die ungestoerten Proben stetig ueber ihre
kurzen Fehlerboegen. Jeder Nachbarabstand bleibt unter
$h+2\epsilon$. Jeder auf seine Startpose normierte Endrahmen
weicht um hoechstens $2\epsilon$ ab; der Abstand beider Enden
ist daher hoechstens $4\epsilon$. Kein Bogen erreicht den Schnitt
bei $\pi$, und das Zeichen kann nicht stetig wechseln. In der
Vierteldrehungskontrolle genuegt also Fehler strikt unter 45 Grad.
Das ist eine geometrische Fehlergrenze, keine Messung von Rauschen
im nativen Modell.

Kurze *Abstaende* der Samples allein beweisen nicht, dass die
tatsaechliche Bewegung dazwischen kurz war. Ein nicht aufgeloester
Vollumlauf ergibt zwei identische Proben. Der genannte Lift
beschreibt per Definition die Kurzweg-Interpolation. Er
beschreibt auch den Lift einer tatsaechlichen Zwischenbewegung,
wenn deren Winkelweglaenge pro Intervall unter $\pi$ bleibt:
Der Lift bleibt dann im offenen Hemisphaerenball um seinen
Startpunkt und muss denselben Zweig treffen.

Ein festes Auslesefenster verliert den Unterschied, wenn der
abweichende Teil beider Pfade aus dem Fenster faellt. Beim
Dreiproben-Vergleich genuegen nach der gemeinsamen Endpose
zwei weitere gleiche Rahmenproben. Das ist keine Aussage,
dass die beiden verborgenen 4D-FIFOs dadurch selbst zusammenfallen.
Ebenso kann der Vergleich eine globale Negation eines Arms
bei unveraenderten Rahmenproben niemals unterscheiden.

## 4. Was die Gravitation zusaetzlich verlangen wuerde

Das Signal ist ein Bit, also ein Phasenvergleich $0$ oder $\pi$.
Bei festgehaltenen Rahmenfolgen aendert dieses Bit sich auch
dann nicht, wenn man die Bahnhoehen zweier Arme veraendert.
Das unterscheidet es vom Gravitationsbenchmark:
Im nichtrelativistischen Vergleich bei vorgegebenen Bahnen
und gleicher Dauer liefert das Newton-Potential $mgz$ den
Aktionsbeitrag zur relativen Phase
$-mg\int(z_A(t)-z_B(t))\,dt/\hbar$. Er ist stetig
veraenderbar und kann bei ganz konstanten Rahmen von null
verschieden sein. Der Bezug ist das
[Neutronenexperiment von Colella, Overhauser und Werner (1975)](https://doi.org/10.1103/PhysRevLett.34.1472),
nicht eine Ableitung seiner gesamten Strahloptik.

Ein nativer Anschluss muss daher zwei getrennte Dinge tragen:
den relativen Orientierungsweg an einer realen Wechselwirkung
und einen stetigen, auf Bahn und Zeit reagierenden Phasenbeitrag
fuer den Gravitationsvergleich. Weder wird das eine durch das
andere ersetzt noch das externe $mgz$ als Memory-Ergebnis
gezaehlt. Kein Transportfeld, keine Born-Regel und keine
Dynamik des Detektors wurden eingefuehrt oder nachgewiesen.

Der [skalare Bahnphasentest](memory_gravity_action_phase_2026-11-22.md)
prueft separat, ob ein vorhandener Memory-Kanal ueberhaupt den
zur Haltezeit proportionalen Hoehenkontrast liefern kann.

Die [Implementierung](../../experiments/current/reference/fifo_relative_frame_lift.py)
nutzt ausschliesslich Rahmenmatrizen. Die
[festen Kontrollen](../../tests/test_fifo_relative_frame_lift.py)
pruefen die beiden Halbwege, Fehlergrenzen, falsche Kurzweg-
Zuordnung bei Unterabtastung und das Vergessen.
