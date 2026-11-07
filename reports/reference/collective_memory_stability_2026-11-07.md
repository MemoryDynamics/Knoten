# Kollektive Stabilisierung: gemeinsame Mode und phasenversetzte Historien

Stand: 2026-11-07. Analytischer Anschluss an die Autorenhypothese eines
gemeinsam stabilisierten Knotens bzw. eines Dreier-FIFO. **Keine neue
Zielsimulation, Parametersuche, Modellfreigabe oder Quantenherleitung.**
Bestandsbasis: `e82b71c782b4b9494a636461369c5bec0061b4fe`.

## Ergebnis und Bedeutung

Eine kollektive Stabilisierung ist eine sinnvolle, aber noch unbelegte
Hypothese. Die Instabilitaet eines einzelnen Kandidaten beweist weder
die Notwendigkeit anderer Knoten noch die Existenz eines quantisierten
Feldes. Der fruehere lineare Quantenabschluss und die mechanische
FIFO-Stabilitaet sind verschiedene Fragen.

Hier wird eine konkrete Unterscheidung hergeleitet:

- Identische deckungsgleiche Historien mit gleicher gesamter Lesestaerke
  behalten ihre Einzelgleichung **einschliesslich der gemeinsamen
  instabilen Mode**. Blosses Vervielfachen stabilisiert diesen Kandidaten
  nicht, auch nicht bei drei Komponenten.
- Zusaetzliche unnormierte Kreuzkopplung aendert schon die gemeinsame
  Einzelgleichung. Ein Erfolg waere gegen eine Einzelreferenz bei dieser
  effektiven Staerke zu vergleichen, nicht nur gegen den alten Gain.
- Phasenversetzte Historien aendern auch bei gleicher Gesamtstaerke die
  gemeinsame Rueckwirkung. Fuer einen regelmaessig versetzten Kreisansatz
  liegen unten eine exakte Existenzgleichung und ein hinreichender
  Normal-Instabilitaetstest vor. **Noch kein solcher Orbit nachgewiesen.**

Das sind Kriterien fuer die Auswahl eines Mechanismus, keine neuen
Teilchenbefunde. Selbst eine bestandene mechanische Pruefung waere noch
kein Spin-, Ladungs-, Quantenfeld- oder Wasserstoffnachweis. Drei
History-Labels sind insbesondere keine hergeleiteten Farbfreiheitsgrade.

## 1. Was im Code steht und was nur bedingt verallgemeinert wird

Gelesen wurden die vollstaendige
[Paarimplementierung](../../src/emergenz_knoten/reciprocal_nodes.py), ihre
[Gradientenprimitive](../../src/emergenz_knoten/_continuation.py), die
[lokalen Paarmoden](../../src/emergenz_knoten/reciprocal_modes.py) und die
[Paarreduktion](../../docs/reference/memory_pair_reduction.md).
Die Paar-API entwickelt zwei eigene FIFO-Historien synchron; beide
Kreuzgradienten lesen den Zustand vor dem Update. Sie integriert kein
zusaetzliches autonomes quantisiertes Feld. Die gelesene API hat genau
zwei Komponenten; ein allgemeiner N-Runner wird hier nicht eingefuehrt.

Fuer gleiche effektive Kernel, Gewichte und Horizonte lautet die
rauschfreie Paarregel in einer **deklarierten algebraischen
N-Verallgemeinerung**:

$$
x_{i,n+1}=x_{i,n}-\sum_{j=0}^{N-1} G_{ij}\sum_{a=0}^{H-1}w_a
\nabla K(x_{i,n}-y_{j,a,n}),\qquad
y_{i,0,n+1}=x_{i,n+1},\quad y_{i,a+1,n+1}=y_{i,a,n}.
$$

Es gilt $i,j=0,\ldots,N-1$; die Schieberegel endet bei $a=H-2$.
Wir beschraenken uns auf bahnkonsistente Zustaende $y_{i,0,n}=x_{i,n}$.
Die gefalteten Gaussbreiten/-amplituden gehoeren zum effektiven $K$.
Im identischen Paar ist $G_{ii}=\eta$, $G_{ij}=\chi$ fuer $i\ne j$.
Die Produktions-API verlangt anfangs nichtverschwindenden Centerabstand;
die deckungsgleiche Konfiguration unten ist die glatte mathematische
Fortsetzung ihrer Gleichungen, kein behaupteter API-Ziellauf.
Verschiedene Kernel oder Gewichte brauchen den entsprechend erweiterten
Operator; sie werden nicht durch diese identische Variante abgedeckt.

Die Kopplung ist **nicht** bloss $-\kappa(x_i-x_j)$: Selbst bei
deckungsgleichen Historien ist deren alternder Gradient im Allgemeinen
nicht null. Unabhaengiges Rauschen zerstoert exakte Synchronie; alle
Stabilitaetsaussagen hier betreffen zunaechst den deterministischen Kern.

## 2. Vollstaendige Rueckwirkung statt eingefrorenem Hintergrund

Mit $B_{ij,a,n}=w_a\nabla^2K(x_{i,n}-y_{j,a,n})$ lautet die exakte
erste Variation:

$$
\delta x_{i,n+1}=\delta x_{i,n}
-\sum_{j,a}G_{ij} B_{ij,a,n}
 (\delta x_{i,n}-\delta y_{j,a,n}),
$$

zuzueglich des linearisierten FIFO-Schiebens. Der Term mit
$\delta y$ ist die Rueckwirkung der beweglichen Quellen. Alle Historien
und Punkte gemeinsam um einen konstanten Vektor zu verschieben wird
exakt weitergetragen: die Differenzen verschwinden. Nur den empfangenden
Punkt bei festgehaltenem Quellenfeld zu variieren prueft dagegen einen
anderen Operator und kann keine Stabilitaet des geschlossenen Systems
belegen. Eine aktive zusaetzliche Feldvariable muesste ebenfalls mit
variiert werden. Dass reziprok gelesen wird, schliesst ausserdem nicht
automatisch die [physikalische Gesamtenergie](../../docs/reference/memory_pair_energy.md).

## 3. Exakter Satz fuer deckungsgleiche Historien

Sei $\sum_jG_{ij}=s$ unabhaengig von $i$. Auf der synchronen Teilmenge
$y_{j,a,n}=y_{a,n}$ ist die Bewegung exakt die Einzelregel mit Gain $s$.
Dies gilt fuer beliebige glatte Kernel und endliche Historien, nicht
nur fuer die lokale quadratische Naeherung. Fuer den synchronen
Ein-Schritt-Jacobian $J_s(n)$ und die Einbettung $Ev=(v,\ldots,v)$ gilt

$$
J_N(n)E=EJ_s(n).
$$

Durch Multiplikation gilt dieselbe Identitaet fuer beliebig viele
linearisierte Schritte. Existiert die synchron fortgesetzte Einzelbahn,
bleibt deshalb jede ihrer wachsenden gemeinsamen Formstoerungen im
Gesamtsystem erhalten. Bei periodischen bzw. relativ periodischen
Bahnen gilt das auch fuer den passend mitrotierten Floquet-Operator.
Eine Stabilisierung der Differenzen zwischen den Komponenten beseitigt
diese Instabilitaet nicht. Das ist keine Aussage gegen andere, etwa
nichtsynchrone kollektive Attraktoren.

Fuer eine Knotenmode $Gv=\gamma v$ und $\delta y_{i,a}=v_i u_a$ ergibt
sich dagegen der History-Block

$$
u_0'=\left[I-s\sum_a B_a\right]u_0
       +\gamma\sum_a B_a u_a,\qquad u_{a+1}'=u_a.
$$

Die gemeinsame Mode hat $\gamma=s$. Fuer symmetrisches $G$ liefern die
Eigenvektoren alle Knotenmoden; bei defekten nichtsymmetrischen Matrizen
sind Jordan-Kopplungen gesondert zu pruefen. Fuer den gemeinsamen
Instabilitaetsbeleg reicht die Einbettung ohne Diagonalisierbarkeit.

Beim vollstaendigen Graphen mit festen Selbst-/Kreuzstaerken ist
$s=\eta+(N-1)\chi$. Bei festgehaltenem Gesamtbudget $s$ und Selbstanteil
$p$ waere dagegen $G_{ii}=sp$, $G_{ij}=s(1-p)/(N-1)$ fuer $N>1$.
Beide Konventionen sind explizit zu unterscheiden. Hier wird **keine**
davon als neue physikalische Regel gewaehlt.

Der archivierte H=1200-Kreis hat
[eine wachsende Normalmode](../dynamics/rotation/fifo_archived_normal_slope_2026-10-26/report.md).
Identische Kopien mit derselben Zeilensumme, denselben Parametern und
derselben Bahn erben diese Instabilitaet. Bei zusaetzlichem Gain gilt
dieser konkrete Archivtransfer nicht, weil bereits die Bahnexistenz und
das Spektrum neu zu bestimmen waeren. Keine Neuauswertung des Archivs.

## 4. Nichtdeckungsgleicher Kandidat: phasenversetzter Kreis

Als analytischen Ansatz, nicht als gefundene Struktur, setze fuer $r>0$
im vorgegebenen aeusseren 3D-Raum

$$
x_{i,n}=r(\cos(n\theta+\phi_i),\sin(n\theta+\phi_i),0),\qquad
\phi_i=2\pi i/N.
$$

Das ist ein gemeinsam rotierendes Polygon mit eigenen zeitversetzten
Historien, nicht bereits N raeumlich getrennte Knoten oder ein Proton.
Sei $G$ zirkulant (zum Beispiel gleiche Selbst-/Kreuzkopplung) und
$\nabla K(z)=k(|z|^2)z$. Definiere

$$
\psi_{ij,a}=a\theta+\phi_i-\phi_j,\quad
d_{ij,a}^2=2r^2(1-\cos\psi_{ij,a}),\quad
C_a(i,j)=G_{ij}w_a k(d_{ij,a}^2),\quad b_a=\sum_j C_a(i,j).
$$

Die $b_a$ sind unabhaengig von $i$ und die $C_a$ zirkulant. Der Ansatz
ist nur dann eine Bahn der angegebenen Regel, wenn Real- und Imaginaerteil
der folgenden Gleichung erfuellt sind:

$$
e^{i\theta}-1=-\sum_{j,a} C_a(i,j)(1-e^{-i\psi_{ij,a}}).
$$

Hier wird kein $r,\theta$ gesucht oder eingesetzt, um diese Gleichung
zu erfuellen. Ein bereits existierender Einzelkreis erfuellt sie nach
Phasenaufteilung im Allgemeinen nicht mehr.

Weil alle Differenzen in der Ebene liegen, ist die normale Hessian-
Komponente genau $k(d^2)$. Normale Stoerungen $z_{i,n}$ erfuellen daher

$$
z_{n+1}=\left(1-\sum_a b_a\right)z_n
         +\sum_a C_a z_{n-a}.
$$

Die diskrete Fourierzerlegung ueber die Knotenlabels zerlegt diesen
vollen Normalblock. Ihre Eigenwerte sind
$\lambda_{m,a}=\sum_j C_a(0,j)e^{2\pi imj/N}$; die zugehoerigen
History-Polynome sind

$$
P_m(\mu)=\mu^H-\left(1-\sum_a b_a+\lambda_{m,0}\right)\mu^{H-1}
-\sum_{a=1}^{H-1}\lambda_{m,a}\mu^{H-1-a}.
$$

Fuer die gemeinsame Knotenmode $m=0$ gilt $\lambda_{0,a}=b_a$.
Der Altersnullterm hebt sich exakt auf. Deshalb ergibt sich derselbe
hinreichende Test wie beim Einzelkreis, jetzt mit kollektiven Gewichten:

$$
S_N=1+\sum_{a=1}^{H-1}a b_a<0
\quad\Longrightarrow\quad\text{reeller Normalmultiplikator }\mu>1.
$$

Beweis: $P_0(\mu)/\mu^{H-1}=\mu-1+\sum_{a\geq1}b_a(1-\mu^{-a})$
verschwindet bei eins, hat dort negative Ableitung und geht fuer
$\mu\to+\infty$ gegen $+\infty$. Bei einer tatsaechlichen Bahn ist
dies eine wachsende Mode, keine neutrale Translation oder Rotation.
**$S_N\geq0$ beweist keine Stabilitaet.** Andere reelle oder komplexe
Normalmoden und der gesamte ebene Block bleiben zu kontrollieren.
Die Formel fuer vorbereitete Punkte allein beweist keine Bahnexistenz.

Im Gegensatz zu deckungsgleichen Kopien enthalten die $b_a$ jetzt andere
Abstaende und Kernelkruemmungen. Das ist ein konkreter Mechanismus,
an dem die kollektive Hypothese scheitern oder weiterkommen kann.
Es gibt in dieser Herleitung keine allgemeine Bevorzugung von $N=3$.

## 5. Literaturabgleich und Grenzen des Gegenarguments

[Pecora und Carroll, PRL 80, 2109 (1998)](https://doi.org/10.1103/PhysRevLett.80.2109)
behandeln Master-Stabilitaetsfunktionen gekoppelter synchroner Systeme.
Hier wurde nur das Verlagsabstract gelesen; beide versuchten offiziellen
PDF-Zugaenge lieferten 401. Die FIFO-Identitaeten oben sind deshalb
explizit hergeleitet, nicht als aus ungelesenen Gleichungen uebernommen
ausgegeben. Es wird keine Neuheit der allgemeinen Modenzerlegung behauptet.

[Ramana Reddy, Sen und Johnston, arXiv:chao-dyn/9805029v1](https://arxiv.org/pdf/chao-dyn/9805029v1),
zu PRL 80, 5109 (1998): Gelesen wurden der vierseitige Preprint,
insbesondere Gleichungen (1)-(4), (8)-(10) und die Diskussion der
Abbildungen. Verzoegerte Kopplung kann in diesem klassischen Modell den
instabilen gemeinsamen Ruhezustand identischer Oszillatoren stabilisieren;
die Autoren behandeln auch N=2,3,4 und den Gross-N-Grenzfall. Das ist
Amplitude death, nicht die Stabilisierung eines nichttrivialen Knotens.
Auf der synchronen Bahn bleibt ein Term $K[Z(t-\tau)-Z(t)]$ erhalten:
Die gemeinsame Dynamik aendert sich, sodass der Satz aus Abschnitt 3
bei festgehaltener Einzelregel nicht widersprochen wird. Diese
Stuart-Landau-Gleichungen sind Referenzannahmen, keine Memory-Herleitung.
Der Preprint wurde am 28.05.1998 eingereicht; das PDF-interne Datum
18.09.2018 ist nicht als neue Einreichung behandelt worden.

Die Literatur stuetzt somit die **Moeglichkeit klassischer kollektiver
Stabilisierung**, nicht ihre Notwendigkeit und nicht QFT-Emergenz.
Kein Review aller kollektiven Mechanismen oder Neuheitsnachweis.

## 6. Verifikation und Entscheidungsgrundlage

Die [30 konstruierten Kontrollen](../../tests/test_collective_memory_stability.py)
pruefen die unveraenderte gemeinsame Regel fuer N=1,2,3,4, ihren vollen
History-Jacobian, additive Gain-Veraenderung, relative Graphmoden,
Rueckwirkung und Translation, die native Paarimplementierung fuer einen
einzigen konstruierten Schritt, die komplexe Existenzgleichung gegen
den direkten Bewegungsupdate sowie die Polygon-Normalbloecke gegen
den unabhaengig assemblierten vollen Hessian-Operator. Zentrale Differenzen
pruefen auch nichtsynchrone Zustaende. Zwei kleine Polynome kontrollieren
die einseitige Aussagekraft des Steigungskriteriums. Keine H=1200-
Rechnung, neue Zielbahn oder Parametersuche. Tests belegen diese
Identitaeten, nicht die Existenz oder Stabilitaet eines kollektiven Knotens.

Verifikation am 2026-11-07: 77 betroffene Tests einschliesslich dieser
30 Kontrollen bestanden in 6.13 s. Vollstaendige konfigurierte Ruff-
Pruefung und strikter MkDocs-Build bestanden. Diese Softwarechecks sind
kein empirischer Nachweis einer neuen physikalischen Struktur.

Die kanonische [Prioritaetenliste](../../docs/status/project_priorities.md)
enthaelt den naechsten Entscheidungspunkt: Kopplungs-/Normierungsvertrag
und Kandidat explizit bestimmen, bevor ein N-Vergleich freigegeben wird.
Ein belastbarer Vergleich braucht sowohl gleiche Mikrokopplung als auch
eine Kontrolle der dadurch veraenderten Gesamtstaerke, volle gemeinsame
und relative Stoerungen, sowie Ausschluss von Kollaps in einen trivialen
Ruhezustand. Quantisierung und Teilchenidentifikation bleiben separate
Nachweispflichten; keine feste aeussere Falle als Emergenz ausgeben.
