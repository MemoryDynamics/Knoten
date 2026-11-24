# Ein FIFO-Zyklus mit beweglichen Speichereintraegen

Stand: 2026-11-24. Fortsetzung der
[Kraft aus dem FIFO-Zentrum](fifo_memory_center_cycle_2026-11-24.md).
Klassischer Vergleich mit demselben autonomen Rotor und
idealer Schreibflaeche. Keine native Zieltrajektorie.

**Ergebnis.** Endliche Speichermassen aendern die Querantwort,
lassen aber den vorbereiteten Zwei-Write-Zyklus exakt bestehen.
Mit den beiden juengsten Eintraegen als Zentrum ist diese
Bahn fuer jedes ganzzahlige Verhaeltnis der beiden Frequenzen
instabil, fuer jede ungerade FIFO-Laenge ab drei.
Beim nichtganzzahligen Vergleich mit gleichen Massen
zeigt auch die volle numerisch ausgewertete Querableitung
einen wachsenden Kopierfehler. Fuer andere nichtganzzahlige
Verhaeltnisse ist Stabilitaet nicht entschieden.

## 1. Bewegliche Register bei derselben exakten Bahn

Kopf und Traeger haben Masse $m$, jedes der $H$ Register
erhaelt Masse $\mu>0$. Zwischen zwei Writes hat das System
mit $M=\sum_j w_j y_j$ die Energie

$$
E_{\rm int}=
\frac{|P_x|^2+|P_b|^2}{2m}
+\sum_j \frac{|P_{y_j}|^2}{2\mu}
+\frac{m\omega^2}{2}(|x-M|^2+|b-M|^2).
$$

Die Register nehmen nicht nur den Gegenimpuls auf, sondern
bewegen sich damit vor dem naechsten Write. Der Gesamtimpuls
und der Drehimpuls bleiben erhalten. Die Schreibkarte ist
weiterhin kanonisch und verwendet bei endlichen Registermassen
auch deren kinetische Energie in der Sprungbilanz.
Die Hamiltonschen Normalmoden einer sichtbaren Koordinate
mit beweglichen Hilfsfreiheitsgraden sind aus anderen
Modellen bekannt, etwa aus dem
[Rubin-Modell bei Das et al.](https://doi.org/10.1103/PhysRevE.102.062130).
Hier gibt es aber einen endlichen FIFO-Schreibschnitt,
keine Waermebad- oder Kontinuumsannahme.

Fuer ungerades $H$ und paritaetsbalancierte Gewichte gilt
wieder $x=A$, $b=-A$, $y_j=(-1)^{j+1}A$ am Schreiben,
bei $M=0$ und allen Impulsen null. Der Write selbst kostet
auf der Grundbahn nichts. Im anschliessenden Flug
bleiben $x=-b$ und $M=0$, sodass die Registerkraft null
ist. Der freie Rotor mit $T=\pi/\omega$ trifft den
naechsten Umkehrpunkt. Nach zwei Writes ist der ganze
Zustand wieder erreicht, fuer jedes $\mu>0$.
Diese Bahn ist weiterhin vorbereitet, nicht selbstselektiert.

Der Relativabstand $d=x-b$ erfuellt $\ddot d=-\omega^2 d$.
Der Versatz $s=(x+b)/2-M$ erfuellt

$$
\ddot s=-\Omega^2 s,\qquad
\Omega^2=\omega^2\left(1+\frac{2m}{\mu}\sum_j w_j^2\right).
$$

Die beiden Richtungen sind in der Massenmetrik orthogonal.
Die uebrigen Moden driften frei. Der Code setzt damit den
exakten linearen Flug um; ein Zeitintegrator ist nicht
erforderlich. Fuer die folgenden Vergleiche gilt
$w_0=w_1=1/2$, alle anderen null, also
$r=\Omega/\omega=\sqrt{1+m/\mu}$.

## 2. Was jeder ganzzahlige Frequenzabgleich uebrig laesst

Setze $r\in\{2,3,\ldots\}$. Quer zur Grundbahn
bleibt die Rotorflugzeit in erster Ordnung unveraendert,
weil der Schnitt-Energiesprung keinen linearen Querterm
enthaelt. Bei $T=\pi/\omega$ verschwinden die Sinusterme
beider Oszillatoren. Nullmoden koennen einen oberen
rechten Driftblock beitragen, nicht aber einen
Impulszuwachs aus einem reinen Ortsfehler.
Damit ist die volle Querableitung blockdreieckig mit
Diagonalbloecken $B$ und $B^{-T}$, wobei $B$ die
Positionsableitung von Write plus Flug ist.

**Gerades $r$.** Der gekoppelte Versatz $s$ kehrt ganz
zurueck, $d$ wechselt das Vorzeichen. Im Ortsblock werden
also Kopf und Traeger nach dem Write getauscht; die
Registerorte werden im Ortsblock nicht bewegt.
Dies ergibt exakt das
[Polynom des reinen Traegerflugs](fifo_carrier_clock_cycle_2026-11-24.md)
$\lambda^{H+2}+\lambda^2-\lambda-1$.
Der reziproke Querimpulsmodus des Kopfs waechst wie dort
um mehr als $4/3$ pro Write. Endliche Registermasse
entfernt ihn in diesem Fall nicht.

**Ungerades $r$.** Nun spiegeln beide Normalmoden.
Sei $t=y_{H-1}$ und $\alpha=1/r^2$. Nach dem Write
ist der doppelte Versatz $2s'=2t-b-y_0$.
Die massengewichtete Reflexion des Versatzes verteilt
diesen Fehler auf beide Koerper und beide gelesenen
Register. Der volle Ortsblock ist

$$
\begin{aligned}
x_{\rm neu}&=t-\alpha(2t-b-y_0),&
b_{\rm neu}&=x-\alpha(2t-b-y_0),\\
(y_0)_{\rm neu}&=x+b-t+(1-\alpha)(2t-b-y_0),&
(y_1)_{\rm neu}&=y_0+(1-\alpha)(2t-b-y_0),\\
(y_j)_{\rm neu}&=y_{j-1}\quad(j\ge2).
\end{aligned}
$$

Die $\alpha$-Abhaengigkeit ist eine Rang-eins-Aenderung,
also ist das charakteristische Polynom affin in $\alpha$.
Bei $\alpha=0$ liefern die unabhaengigen Zeilen fuer
$x,b$ und den Shift $\lambda x=t$, $\lambda b=x$,
$\lambda y_1=2t-b$ und $y_1=\lambda^{H-2}t$.
Das ergibt $\lambda^{H+1}-2\lambda^2+1$.
Die verbleibende $y_0$-Zeile liefert den Faktor $\lambda+1$.
Bei $\alpha=1$ ergibt sich das Polynom des zuletzt
untersuchten unbeweglichen Zentrums. Zusammen:

$$
p_\alpha(\lambda)=(\lambda+1)\left[
\lambda^{H+1}-2\alpha\lambda^H-\alpha\lambda^{H-1}
-2(1-\alpha)\lambda^2+\alpha\lambda+1\right].
$$

Die Koeffizienten an $\lambda^{H+1}$ und $\lambda$ sind
$1-2\alpha$ und $1+\alpha$. Sie sind fuer jedes endliche
ungerade $r$ verschieden. Bei einem reellen monischen Polynom
mit konstantem Term eins wuerden ausschliesslich Nullstellen
auf dem Einheitskreis Reziprozitaet erfordern.
Da das Betragsprodukt eins ist,
liegt mindestens eine Wurzel ausserhalb des Einheitskreises.
Fuer $H=3$ ist die Ableitung der Klammer bei $\lambda=1$
gleich $-3\alpha<0$; damit gibt es hier sogar eine reelle
Wurzel groesser als eins.

Dieser Modus ist am Schreibfehler $e=b-t$ sichtbar.
Waere $e=0$, ergaebe die Differenz der Koerperzeilen
$(\lambda+1)(x-t)=0$. Fuer $|\lambda|>1$ folgt also
$x=b=t$. Die Traeger- und erste Registerzeile verlangen dann
$\alpha y_0=(\lambda-1+\alpha)t$ und
$(\lambda+1-\alpha)y_0=(2-\alpha)t$.
Das erzwingt $\lambda^2=1$, oder bei $t=0$ einen
verschwindenden Eigenvektor. Ein echter wachsender
Ortsmodus kann den Kopierfehler somit nicht umgehen.
Beide Halbschritte haben denselben Querblock, sodass
die volle Zweiperiode das Quadrat behaelt.

## 3. Nichtganzzahlige Gegenprobe und Ausblick

Der feste Vergleich $H=3$, $\mu=m$ hat $r=\sqrt{2}$.
Hier koppeln Ort und Impuls auch im unteren linken
Block. Eine numerische Auswertung der exakten
linearen Flugmatrix nach dem Write (keine Trajektorie)
liefert fuer $\det(\lambda I-J)$ bei $\lambda=-2$
ungefaehr $+191.72$, bei $\lambda=-3/2$ ungefaehr
$-4.21$. Der reelle wachsende Zweig dazwischen hat
einen nichtverschwindenden Quer-Kopierfehler.
Eine zweite Auswertung durch Querableitung des vollen
Rotor-Returns bestaetigt die Matrix. Das ist ein einziger
vorab festgelegter Massenvergleich, keine Aussage ueber
alle nichtganzzahligen $r$.

Damit kann weder die starre noch die in Phase
zurueckkehrende bewegliche Speicherstruktur den
vorbereiteten kollinearen Zyklus stabilisieren.
Die verbleibende Frage ist nicht nur eine andere Masse:
Liegt die Instabilitaet an dieser Zweiplatz-Geometrie
oder am verwendeten reversiblen Kopierschnitt selbst?
Eine nichtkollineare periodische Schreibgeometrie mit
demselben Schnitt waere ein struktureller Vergleich.

[Referenzcode](../../experiments/current/reference/fifo_carrier_clock_cycle.py)
und [feste Kontrollen](../../tests/test_fifo_mobile_memory_cycle.py)
pruefen zwei Writes, Energiesprung, Beweglichkeit,
Energie und Impulse, inverse Entwicklung und beide
Querpolynome sowie die volle nichtganzzahlige Ableitung.

Der [Ausschluss rotierender Schreibgeometrien](fifo_rotating_section_2026-11-24.md)
prueft den konstant getakteten Referenzflug selbst auf
neutrale Rotationsmoden, noch vor einer Stabilitaetsanalyse.
