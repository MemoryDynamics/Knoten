# Geschlossene FIFO-Schreibfolgen mit veraenderlicher Rotorzeit

Stand: 2026-11-24. Fortsetzung des
[Ausschlusses bei konstanter Halbperiode](fifo_rotating_section_2026-11-24.md).
Dasselbe bewegliche Hamilton-Register und dieselbe reversible
Schreibkarte. Keine native Zieltrajektorie, kein Parameterscan.

**Ergebnis.** Eine nichtkollineare, absolut periodische
Kopierfolge mit variablem autonomem Takt muss zwei getrennte
Tests bestehen: einen linearen Rueckkehr- und Kopiertest
sowie einen quadratischen Energieabschluss. Fuer jedes
feste ungerade $H\ge3$ und jede feste Periodenzahl
gibt es bei hinreichend kurzen positiven Flugzeiten
keine nichtstationaere absolut periodische Registerbahn.
Auch bei allgemeinen Flugzeiten ist eine solche Bahn nur
auf einer Ausnahmemenge moeglich. Das ist kein
allgemeiner Existenz-Ausschluss: Die autonome Dynamik
koennte gerade eine Ausnahmekombination auswaehlen.

## 1. Rueckkehr, exakte Kopie und Geometrie

Fixiere $H$, die Massen und das bewegliche
Memory-Center-Hamiltonian. Pro Raumkomponente
steht der Vektor $z$ fuer alle $H+2$ Orte
gefolgt von allen $H+2$ Impulsen. Sei
$D=C\oplus C^{-T}$ der kanonische Write,
$F(T)$ der exakte lineare Flug und
$J(T)=F(T)D$. Fuer $p$ vorgeschlagene
positive Flugzeiten $T_0,\ldots,T_{p-1}$ setze

$$
W_0=I,\qquad W_{n+1}=J(T_n)W_n.
$$

Absolute Rueckkehr erfordert $(W_p-I)z=0$.
Mit der Zeile $e$ fuer $b-y_{H-1}$ lautet der
exakte Kopiertest $eW_n z=0$ fuer alle $n<p$.
Sei $\mathcal K$ der gemeinsame Kern dieser Zeilen
und der Rueckkehr. Die Kopie erfolgt jeweils am
Schreibschnitt; bewegliche Register koennen sich danach
weiter verschieben. Es wird keine Gleichheit mit einer
unbeweglichen Liste vergangener Positionen behauptet.

Fuer $d$ Raumdimensionen sei $Z$ die Matrix der $d$
Komponenten und $G=ZZ^T$ ihre Gram-Matrix. Die Zeilen
von $L_x$ seien $h^T(W_n-I)$, wobei $h^T$ die
Kopfposition liest. Dann ist die Gram-Matrix der
Schreibpunktdifferenzen $L_x G L_x^T$. Eine
nichtkollineare Geometrie verlangt Rang mindestens
zwei dieser Matrix, nicht von $G$ allein. Der
Translationsvektor $\tau$ mit allen Orten gleich
und allen Impulsen null gehoert stets zu
$\mathcal K$ und wird von $L_x$ vernichtet.
Daher muss $\dim\mathcal K\ge3$ gelten: zwei
geometrisch unabhaengige Komponenten zusaetzlich
zur gemeinsamen Translation. Dies ist notwendig,
nicht allein hinreichend.

## 2. Der Rotor muss den Zeitplan selbst erzeugen

Sei $z^TKz$ die interne Energie pro Raumkomponente
in einem Registerchart. Der $n$-te Write und Flug
aendern sie um

$$
\Delta E_n
=\operatorname{tr}\!\left[
(W_{n+1}^T K W_{n+1}-W_n^T K W_n)G
\right].
$$

Da der Flug die interne Energie erhaelt, ist dies
die Arbeit am Write. Die Rotorenergie nach dem
$n$-ten Write ist $R_n=M_sL^2/(2T_n^2)$.
Autonomie verlangt $\Delta E_n=R_{n-1}-R_n$
mit zyklischen Indizes. Eine uebereinstimmende
Summe ueber den Zyklus reicht nicht; jeder Schritt
muss einzeln stimmen.

Fuer feste Zeiten sind diese Gleichungen linear in
$G$. Das Anheben quadratischer Daten auf eine
Gram-Matrix hat einen methodischen Bezug zu
[Candes, Strohmer und Voroninski](https://arxiv.org/abs/1109.4499);
hier wird kein Resultat zur Phasenrekonstruktion
uebernommen. Die Bedingungen

$$
G\succeq0,\quad \operatorname{rang}G\le d,\quad
\operatorname{im}G\subseteq\mathcal K,\quad
\operatorname{rang}(L_xG L_x^T)\ge2
$$

samt der Energiebilanz sind fuer die hier definierte
nichtkollineare Folge notwendig und hinreichend.
Denn aus $G$ rekonstruiert eine reelle Faktorisierung
ein $Z$. Die positive Rotorloesung ist
$\pi_{n+1}=M_s L/T_n$; mit der Arbeit aus $Z$
ist sie exakt das transmittierte Ergebnis der
autonomen Schreibkarte. Jeder Flug hat die gewuenschte
Dauer ohne externen Reset. Die Aussage setzt absolute
Rueckkehr, nur Vorwaerts-Writes und $T_n>0$ voraus.
Sie enthaelt weder relative Rueckkehr mit Drift oder
Drehung noch einen Stabilitaetsnachweis.

## 3. Kurze Zeiten und der generische Rang

Am analytischen Grenzpunkt $T_n=0$ ist $W_p=D^p$.
Der Ortsblock $C$ hat das charakteristische Polynom

$$
(\lambda-1)(\lambda^{H+1}+\lambda-1).
$$

Der Kopf bleibt am Write unveraendert. Auf dem
verbleibenden Block ergeben $\lambda b=y_{H-1}$,
$\lambda y_0=b-y_{H-1}$ und der Shift genau
den zweiten Faktor. Dessen Einheitskreis-Nullstelle
muesste wegen $|\lambda^{H+1}|=|1-\lambda|=1$
gleich $e^{\pm i\pi/3}$ sein. Da dann
$1-\lambda=\lambda^{-1}$ gilt, waere
$\lambda^{H+2}=1$ noetig. Bei ungeradem $H$
ist das unmoeglich. Die einzige Einheitskreis-
Nullstelle von $C$ ist folglich die einfache $+1$.

Damit hat $D^p-I$ fuer jedes $p$ genau zwei
Nullrichtungen: $\tau$ und den reinen Kopfimpuls
$\nu$, weil der kanonische Write diesen bei
allen anderen Impulsen null unveraendert laesst.
Auch $h^T(D^p-I)=0$. Eine kurze Flugzeit
loest die zweite Nullrichtung auf. Aus der
kinematischen Gleichung $\dot x=P_x/m$ folgt

$$
h^T(W_p-I)\nu
=\frac{\sum_n T_n}{m}+O(\|\mathbf T\|^2).
$$

Der erste Term ist fuer jede positive Zeitfolge
gleichgerichtet. Zur Rangsicherung waehle einen
bei $\mathbf T=0$ invertierbaren Block von
$D^p-I$ auf einem Komplement von $\tau,\nu$.
Ergaenze seine Zeilen um $h^T$ und seine Spalten
um $\nu$. Die neuen Nebendiagonalbloecke sind
jeweils $O(\|\mathbf T\|)$; der Schur-Komplement-
Term veraendert die obige erste Ordnung nur
quadratisch. Weil $\sum_n T_n\ge\|\mathbf T\|_\infty$
fuer positive Zeiten, ist die erweiterte
Untermatrix fuer alle hinreichend kurzen Zeiten
invertierbar. Die Schranke haengt von der festen
Periodenzahl und den Modellparametern ab.
Somit ist die einzige periodische Moeglichkeit
die reine Translation, also alle Register am
selben Ort und alle Impulse null. Dann kostet
kein Write Energie und der Rotor laesst
keine ungleichen Zeiten zu.

Dieselbe erweiterte Determinante ist reell
analytisch in den Zeiten und nicht identisch null.
Ihre Nullmenge hat Lebesgue-Mass null
([Mityagin](https://arxiv.org/abs/1512.07276)).
Auf jedem Strahl $T_n=t\,r_n$ mit festen $r_n>0$
ist sie ebenfalls nicht identisch null, da sie
nahe $t=0$ nicht verschwindet. Ihre positiven
Nullstellen sind dort isoliert. Ein echter
nichtkollinearer Kandidat muss auf dieser
Ausnahmemenge sogar mindestens zwei nichttriviale
Nullrichtungen neben der Translation liefern,
die Kopierzeilen erfuellen und schliesslich
die Rotorbilanz mit einer zulaessigen Gram-Matrix
bestehen. Mass null ist ausdruecklich **kein**
Beweis, dass endogen ausgewaehlte Zeiten diese
Bedingungen nicht erfuellen.

## 4. Kontrollen und Verwendung

[Referenzcode](../../experiments/current/reference/fifo_timing_cycle.py)
baut die linearen Zeilen und Energieformen auf;
er waehlt keine Zeiten und startet keine Suche.
[Feste Kontrollen](../../tests/test_fifo_timing_cycle.py)
gleichen sie mit drei tatsaechlich unterschiedlichen
aufeinanderfolgenden Flugzeiten einer Referenzfolge
ab. Diese Folge ist kein geschlossener Kandidat.
Ein zweiter Check rekonstruiert die bekannte
kollineare Zweiperiode und trennt den Rang von $G$
vom Rang der Kopfgeometrie. Kurze unterschiedliche
Fluege und die lineare Kopfimpuls-Ableitung werden
fuer feste Horizonte gegengeprueft. Der allgemeine
Rangausschluss folgt aus der Algebra, nicht aus
den ausgewaehlten Zeiten.

Der [Treue-Test fuer die gesamte Historie](fifo_faithful_history_2026-11-24.md)
unterscheidet exakte Kopie am Schnitt von exakter Aufbewahrung.
Mit treuen historischen Proben sind mehr als zwei Schreiborte
im beweglichen Ein-Zentrum-Modell auch bei beliebigem Takt
ausgeschlossen. Der Test fuer driftende Eintraege bleibt offen.
