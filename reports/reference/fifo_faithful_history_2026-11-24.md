# Exaktes Schreiben ist nicht dasselbe wie treue FIFO-Historie

Stand: 2026-11-24. Fortsetzung des
[Tests mit veraenderlicher Rotorzeit](fifo_timing_cycle_2026-11-24.md).
Dasselbe bewegliche Memory-Center-Hamiltonian und dieselbe
reversible Kopierkarte, fuer jedes $H\ge2$, beliebige nichtnegative
normierte Gewichte, positive Massen und positive Flugzeiten.
Keine native Zieltrajektorie und kein Parameterscan.

**Ergebnis.** Sollen die beweglichen Register an jedem
Schreibschnitt die wirklichen frueheren Kopfpositionen
enthalten, kann jede absolut periodische Bahn hoechstens
zwei verschiedene Kopfpositionen schreiben. Dasselbe gilt
ab einem Anfangsstueck fuer dauerhaft beschraenkte
Vorwaertsbahnen mit endlicher Gesamtenergie. Insbesondere
ist ein Dreieck aus drei echten historischen Proben auch
mit wechselnden Rotorzeiten ausgeschlossen. Erlaubt man,
dass die Eintraege zwischen den Schnitten ihre Werte
veraendern, entfaellt die zentrale Voraussetzung.

## 1. Zwei getrennte Speicherbedingungen

Die Schreibkarte speichert am Schnitt genau dann den Kopf
$x_n$, wenn $b_n=y_{H-1,n}$. Das allein sagt nichts ueber
die spaetere Lage des neuen Registers. Fuer ein treues
Orts-FIFO gilt vor jedem Schnitt zusaetzlich

$$
y_{j,n}=x_{n-1-j}.
$$

Nach einem korrekten Write ist also $Y_n^+=Y_{n+1}$:
Jeder Registerort muss nach dem Flug wieder am Ort
unmittelbar nach dem Shift sein, auch wenn er sich
waehrenddessen bewegt. Logische Umkehrbarkeit und
das explizite Erhalten einer Historie sind auch bei
[Bennett](https://www.cs.princeton.edu/courses/archive/fall04/cos576/papers/bennett73.html)
verschiedene Anforderungen an eine Konstruktion.
Hier wird keine thermodynamische Folgerung aus
seiner Berechnungskonstruktion uebernommen.

Das Zentrum $M=\sum_j w_j y_j$ koppelt alle Speicherimpulse
durch dieselbe Kraft: $\dot P_Y=w f(t)$ je Raumkomponente.
Mit $\Pi_w$ als orthogonalem Projektor auf den Gewichtsvektor
$w$ ist $(I-\Pi_w)P_Y$ im Flug konstant.
Da alle Register dieselbe Masse $\mu$ haben, gilt fuer
einen beliebigen Flug mit Drift $\Delta Y_n=Y_{n+1}-Y_n^+$

$$
(I-\Pi_w)P_{Y,n}^+
=(I-\Pi_w)P_{Y,n+1}
=\frac{\mu}{T_n}(I-\Pi_w)\Delta Y_n .
$$

Bei treuer Historie ist $\Delta Y_n=0$. An beiden
Flugenden muessen daher die Speicherimpulse im
Gewichtsprofil liegen. Am Schnitt schreiben wir
$P_{Y,n}=w a_n$ und $P_{Y,n}^+=w b_n^{\rm imp}$,
wobei $a_n,b_n^{\rm imp}$ Raumvektoren sind.
Die kanonische Impulskarte verlangt

$$
w_j b_n^{\rm imp}=w_{j-1}a_n\quad (1\le j<H),
\qquad P_{b,n}=w_0 b_n^{\rm imp}.
$$

Ist das Paar der abgeschnittenen Gewichtsvektoren
$(w_0,\ldots,w_{H-2})$, $(w_1,\ldots,w_{H-1})$
linear unabhaengig, folgt $a_n=b_n^{\rm imp}=0$.
Dies umfasst das bisher verwendete Zentrum aus den
beiden juengsten Eintraegen bei $H\ge3$.

## 2. Warum auch die besonderen Gewichte nicht ausweichen

Zunaechst ist der Gesamtimpuls $P_{\rm tot}$ null.
Er ist erhalten, und das massengewichtete Ortsmoment
waechst im Flug um $T_n P_{\rm tot}$. Beim exakten
Schreiben aendert es sich um
$\mu(x_n-x_{n-H})$, da Kopf und Traeger ihre
Positionen am Schnitt behalten. Ueber einen periodischen
Umlauf summiert sich dieser Zusatz zu null. Daher
erzwingt absolute Rueckkehr $P_{\rm tot}=0$.
Bei einer beschraenkten Vorwaertsbahn bleiben auch
die Teilsummen des Schreibzusatzes beschraenkt.
Mit endlicher Gesamtenergie und nichtnegativer
interner Energie hat der freie Rotor eine obere
Impulsschranke, also $\sum_n T_n=\infty$.
Auch dann folgt $P_{\rm tot}=0$.

Da die Speicherorte an beiden Flugenden gleich sind,
bleibt damit der Mittelpunkt $c=(x+b)/2$ von Schnitt
zu Schnitt konstant. Aus $b_n=x_{n-H}$ folgt
$x_{n+H}=2c-x_n$ und $x_{n+2H}=x_n$.
Schon dies schliesst bei allen Gewichten nichtstationaere
Kopfpositionen auf jeder ungeraden Periode aus.
Der folgende Schritt schliesst auch nichtkollineare
gerade Perioden aus.

Sei $D=P_x-P_b$ der relative Impuls. Die Impulskarte
und $P_{\rm tot}=0$ liefern am Schnitt

$$
D^-=-a_n-2 w_0b_n^{\rm imp},
\qquad
D^+=-(1+w_{H-1})a_n-3 w_0b_n^{\rm imp}.
$$

Der relative Ortsabstand $d=x-b$ ist beim exakten
Write unveraendert. Im Flug ist
$E_d=|D|^2/(4m)+m\omega^2|d|^2/4$ fuer sich erhalten,
weil $d$ ein entkoppelter Oszillator ist.

Sind die beiden abgeschnittenen Gewichtsvektoren
linear abhaengig, gibt es wegen $w_j\ge0$ nur drei
Faelle:

- Bei durchgehend geometrischen Gewichten
  $w_j=w_0\rho^j$ mit $\rho>0$ ist
  $b_n^{\rm imp}=a_n/\rho$. In $D^+$ ist der
  positive Faktor von $-a_n$ strikt groesser
  als in $D^-$.
- Ist nur das juengste Gewicht eins, gilt $a_n=0$;
  die relativen Impulse sind $-2 b_n^{\rm imp}$
  und $-3 b_n^{\rm imp}$.
- Ist nur das aelteste Gewicht eins, gilt $b_n^{\rm imp}=0$;
  die relativen Impulse sind $-a_n$ und $-2a_n$.

In jedem Fall steigt $E_d$ am Write strikt, sofern
die verbleibenden Impulse nicht null sind. Das kann
sich auf einer periodischen Bahn nicht zu null
summieren. Fuer den beschraenkten Fall: Der
monotone Anstieg ist durch die Gesamtenergie
beschraenkt, daher gehen die verbleibenden Impulse
gegen null. Die Folge $|d_n|^2$ ist bereits periodisch.
Aus Konvergenz von $E_d$ folgt deshalb, dass
$|d_n|^2$ konstant ist. Dann wuerde jeder von null
verschiedene relative Impuls bei jedem Write um
denselben Faktor groesser als eins wachsen.
Beschraenktheit erzwingt erneut den Nullfall.

Somit sind in allen Faellen die Speicher-,
Traeger- und Kopfimpulse an den Schnitten null.
Bei festem $c$ und einem freien relativen
Oszillator mit Umkehrpunkten an beiden Flugenden
bleibt die geordnete Position $(x,b)$ beim
naechsten Schnitt entweder gleich oder wird
vertauscht. Es gibt hoechstens zwei geschriebene
Kopforte. Zwischen den Schnitten koennen sich
die Eintraege bewegen; die Aussage betrifft
die treue Historie an den Schnitten.

## 3. Messbarer Unterschied zum Modell mit Drift

Fuer einen nicht treuen Flug heisse
$E_n=(\mu/T_n)(I-\Pi_w)\Delta Y_n$ der
Impulsanteil ausserhalb des Kraftprofils.
Bei linear unabhaengigen abgeschnittenen
Gewichtsvektoren sei
$L=[w_{0:H-1},-w_{1:H}]$ deren Zweispaltenmatrix.
Der Shift gibt

$$
L\begin{pmatrix}a_n\\b_n^{\rm imp}\end{pmatrix}
=(E_n)_{1:H}-(E_{n-1})_{0:H-1}.
$$

Damit ist die Norm der beiden gestapelten
Kraftprofil-Anteile durch
$(\|E_n\|+\|E_{n-1}\|)/\sigma_{\min}(L)$
beschraenkt. Der Traegerimpuls wird am Schnitt
entsprechend zu $P_{b,n}=w_0 b_n^{\rm imp}+(E_n)_0$.
Ein korrekt kopierender Kandidat mit variablen
Zeiten muss daher zusaetzlich auf die Drift seiner
Eintraege geprueft werden. Die Schreibgenauigkeit
allein weist kein treues FIFO nach.

[Referenzcode](../../experiments/current/reference/fifo_timing_cycle.py)
liefert zusaetzliche lineare Zeilen fuer den Vergleich
mit den frueheren Kopfwerten. Die
[algebraischen Kontrollen](../../tests/test_fifo_faithful_history.py)
pruefen die Driftprojektion und die relative Sprungarbeit
in den drei Ausnahmefaellen. Die
[Timing-Kontrollen](../../tests/test_fifo_timing_cycle.py)
pruefen die historischen Zeilen an der bekannten
Zweiperiode und an einer nicht geschlossenen Folge.
Kein Ausschluss fuer ein driftendes Gedaechtnis
oder fuer mehrere unabhaengige Kraftprofile:
Gerade die Impulskopplung durch nur ein Profil
ist die angreifbare Modellannahme.

Das [exakte Sechseck mit zwei Kraftprofilen](fifo_two_center_hexagon_2026-11-24.md)
ueberwindet die Ein-Profil-Barriere konstruktiv, bleibt aber
gegen Stoerungen senkrecht zur Schreibebene instabil.
