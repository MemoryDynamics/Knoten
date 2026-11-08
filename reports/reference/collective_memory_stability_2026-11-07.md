# Kollektive Stabilisierung: gemeinsame Mode und phasenversetzte Historien

Stand: 2026-11-08, begonnen am 2026-11-07. Analytischer Anschluss an die Autorenhypothese eines
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
Die anschliessende Paar-Spezialisierung in Abschnitt 7 trennt nun alle
normalen und ebenen Stoerungen, gibt ein hinreichendes Stabilitaetskriterium
fuer **nur einen** Block und eine notwendige geometrische Bedingung an.
Abschnitt 8 ordnet die naheliegende Troepfchen-Referenz ein. Auch damit
liegt noch kein stabiler nativer Paarorbit vor.
**Gegenpruefung vom 2026-11-08:** Abschnitt 9 zeigt, dass die einfache
Positivitaetsvoraussetzung des Abklingkriteriums beim dokumentierten
Ankerkernel in einem ganzen Bereich um die archivierte Geometrie
unerreichbar ist, fuer jedes nichtnegative Selbst-/Kreuz-Gain-Verhaeltnis.
Das schliesst diesen Nachweisweg dort aus, nicht stabile Paarorbits.

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

Die ersten [30 konstruierten Kontrollen](../../tests/test_collective_memory_stability.py)
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

Verifikation der ersten Stufe am 2026-11-07: 77 betroffene Tests einschliesslich dieser
30 Kontrollen bestanden in 6.13 s. Vollstaendige konfigurierte Ruff-
Pruefung und strikter MkDocs-Build bestanden. Diese Softwarechecks sind
kein empirischer Nachweis einer neuen physikalischen Struktur.

Die anschliessende Paar-Spezialisierung ergaenzt 15 Kontrollen, insgesamt
45 in derselben Testdatei: Summen-/Differenzbloecke, Existenz-/Neigungs-
Residuum, vollstaendig mitrotierender ebener Operator samt Symmetrien,
bedingtes gemeinsames Abklingen und dessen Randfall, repulsiver
Existenz-Ausschluss sowie ein vorgeschriebenes Zweialter-Gegenbeispiel.
105 betroffene Tests bestanden in 2.71 s; konfigurierte Ruff-Pruefung
und strikter MkDocs-Build bestanden ebenfalls. Ein erster Testlauf
traf bei der trigonometrischen Darstellung des exakten Vierteldrehungs-
Beispiels auf 4.44e-16 Rundungsrest. Die Kontrolle prueft nun die beiden
Koeffizientenidentitaeten exakt und erlaubt fuer die trigonometrische
Auswertung acht Maschinen-Epsilon; kein physikalisches Kriterium wurde
nachtraeglich gelockert. Kein Zielorbit wurde berechnet.

Die kanonische [Prioritaetenliste](../../docs/status/project_priorities.md)
enthaelt den naechsten Entscheidungspunkt: Kopplungs-/Normierungsvertrag
und Kandidat explizit bestimmen, bevor ein N-Vergleich freigegeben wird.
Ein belastbarer Vergleich braucht sowohl gleiche Mikrokopplung als auch
eine Kontrolle der dadurch veraenderten Gesamtstaerke, volle gemeinsame
und relative Stoerungen, sowie Ausschluss von Kollaps in einen trivialen
Ruhezustand. Quantisierung und Teilchenidentifikation bleiben separate
Nachweispflichten; keine feste aeussere Falle als Emergenz ausgeben.

## 7. Antipodales Paar: konkreter Mechanismus und vollstaendige Moden

Analytische Fortsetzung am selben Tag, ohne Entscheidung ueber neue
Kopplungsregeln oder einen festen Kreuz-Gain. Grundlage ist die bereits
implementierte identische Paarregel mit Selbststaerke $\eta\geq0$ und
Kreuzstaerke $\chi\geq0$, beide weiter symbolisch. Der Winkel $\pi$
bezeichnet den **Ortsphasenversatz** der zwei Historien, nicht einen
Spinwinkel oder die Schwingungsphase eines zusaetzlichen Feldes.

Sei $x_{B,n}=-x_{A,n}$, $r>0$, $0<\theta<\pi$. Schreibe mit Altersindex
$\ell=0,\ldots,H-1$ und $\nabla K(z)=k(|z|^2)z$:

$$
d_{s,\ell}^2=2r^2(1-\cos\ell\theta),\qquad
d_{c,\ell}^2=2r^2(1+\cos\ell\theta),
$$

$$
a_\ell=\eta w_\ell k(d_{s,\ell}^2),\qquad
b_\ell=\chi w_\ell k(d_{c,\ell}^2),\qquad
c_\ell=a_\ell+b_\ell,\quad d_\ell=a_\ell-b_\ell.
$$

Hier bezeichnet $b_\ell$ nur den Kreuzanteil, nicht die Zeilensumme aus
Abschnitt 4. Die exakten Existenzresiduen sind

$$
F_R=\cos\theta-1+\sum_\ell[a_\ell(1-\cos\ell\theta)
                                  +b_\ell(1+\cos\ell\theta)],
$$

$$
F_T=\sin\theta+\sum_\ell d_\ell\sin\ell\theta.
$$

Nur $F_R=F_T=0$ beschreibt den Kreisorbit. Ein normal stabiler Operator
an einer beliebigen vorbereiteten Geometrie ist kein Ersatz dafuer.

### Gemeinsame und relative Normalmode

Fuer $z_+=(z_A+z_B)/2$ und $z_-=(z_A-z_B)/2$ gilt exakt

$$
z_{+,n+1}=(1-\sum_\ell c_\ell)z_{+,n}
                  +\sum_\ell c_\ell z_{+,n-\ell},
$$

$$
z_{-,n+1}=(1-\sum_\ell c_\ell)z_{-,n}
                  +\sum_\ell d_\ell z_{-,n-\ell}.
$$

Das ist die konkrete stabilisierende Moeglichkeit: Ein positiver
Kreuzanteil erhoeht bei **festgehaltener Geometrie**
$S_+=1+\sum_{\ell\geq1}\ell c_\ell$, wirkt aber im relativen
Quellenfeedback mit dem anderen Vorzeichen. Positive $b_\ell$ fuer alle
Alter sind nicht vorausgesetzt; mit langen Historien koennen auch
Kreuzpunkte nahe am empfangenden Punkt liegen. Eine echte Bahn aendert
bei veraendertem $\chi$ im Allgemeinen auch $r$ und $\theta$. Daher ist
die Steigungsverbesserung bei festem $r,\theta$ **kein** Stabilitaetsbeleg.

Ein positiver bedingter Satz geht weiter als der negative Steigungstest:

$$
c_\ell\geq0\ (\ell\geq1),\qquad
C=\sum_{\ell\geq1}c_\ell<1
\quad\Longrightarrow\quad
\text{alle gemeinsamen Normalmoden ausser Translation klingen asymptotisch ab.}
$$

Fuer einen nichtverschwindenden Multiplikator gilt
$\mu=1-C+\sum_{\ell\geq1}c_\ell\mu^{-\ell}$.
Bei $|\mu|\geq1$ erzwingt die Dreiecksungleichung $|\mu|\leq1$.
Im Gleichheitsfall fixiert der strikt positive Term $1-C$ die Phase auf
$\mu=1$; diese Nullstelle ist wegen $S_+>0$ einfach. Nullmultiplikatoren
sind kontrahierend. Das beweist den Satz auch bei verschwindenden
Einzelgewichten. Bei $C=1$ koennen weitere ungedaempfte Moden auftreten.
Die Bedingungen sind hinreichend, nicht notwendig; ihre Erfuellung an
einem tatsaechlichen nativen Paarorbit wurde hier nicht gezeigt.
Die spaetere Kompatibilitaetspruefung in Abschnitt 9 schliesst ihre
Erfuellbarkeit im dort benannten Ankerbereich sogar aus.

Die beiden Neigungen der Kreisebene liegen beim antipodalen Paar im
**relativen** Normalblock. Mit $v_\ell=e^{-i\ell\theta}$ und dessen
History-Matrix $T_-$ gilt sogar abseits eines Roots

$$
T_-v-e^{i\theta}v=-(F_R+iF_T)e_0.
$$

Erst bei exakter Kreisbalance sind also $e^{\pm i\theta}$ echte neutrale
Neigungsmoden. Die gemeinsame normale Translation hat stets $\mu=1$.
Weitere relative Formmoden sind gesondert zu kontrollieren, nicht als
Neigungen zu entfernen.

### Ebener Block und mitrotierende Historie

Setze im gemeinsamen mitrotierenden Koordinatensystem
$A_\ell=\eta w_\ell\nabla^2K(x_A-y_{A,\ell})|_{xy}$,
$B_\ell=\chi w_\ell\nabla^2K(x_A-y_{B,\ell})|_{xy}$ und
$R_-=R(-\theta)$. Wegen der geraden radialen Hessian sind die beiden
Diagonalknotenbloecke identisch und ebenso die beiden Kreuzbloecke.
Fuer die gemeinsamen/relativen ebenen Variationen lautet der volle
mitrotierende History-Operator

$$
u_0'=R_-\left([I-\sum_\ell(A_\ell+B_\ell)]u_0
                  +\sum_\ell(A_\ell\pm B_\ell)u_\ell\right),\qquad
u_{\ell+1}'=R_-u_\ell.
$$

Auch **alle verschobenen Historienpunkte** muessen mitrotieren. Nur den
aktuellen Punkt zu drehen und den Tail mit Identitaetsbloecken zu
schieben erzeugt einen anderen Operator. Die Tests vergleichen beide
ebenen Bloecke mit dem vollstaendigen, gemeinsam rotierten Paar-Jacobian.
Bei einem exakten Orbit liegen die ebenen Translationsmoden im
gemeinsamen Block bei $e^{\pm i\theta}$, die Rotation innerhalb der
Ebene im relativen Block bei eins. Diese Symmetrien sind keine Daempfung.
Ein Spektralnachweis muss zudem die Semisimplizitaet der neutralen
Moden bzw. moegliche Jordan-Verstaerkung und die verbleibenden Moden
beachten; ein paar Stichprobenwinkel reichen nicht.

### Zwei notwendige Gegenpruefungen

Erstens verlangt die radiale Existenzgleichung

$$
\sum_\ell[a_\ell(1-\cos\ell\theta)+b_\ell(1+\cos\ell\theta)]
=1-\cos\theta>0.
$$

Liegen alle beteiligten Abstaende im rein repulsiven Bereich $k\leq0$,
ist das unmoeglich. Fuer den Zweigausskernel mit breiterer attraktiver
Komponente, positiven Amplituden und $k(0)<0$ gibt es genau einen
positiven Kraftnullpunkt

$$
d_*^2=\frac{2\log(A_{rep}\sigma_{att}^2/(A_{att}\sigma_{rep}^2))}
                 {\sigma_{rep}^{-2}-\sigma_{att}^{-2}}.
$$

Da jede Chordlaenge hoechstens $2r$ ist, ist $r>d_*/2$ notwendig.
Dies verwendet die bereits vorhandene Funktion
[`double_gaussian_force_crossing_radius`](../../src/emergenz_knoten/rotating_wave.py),
keine neue Kernelwahl. Es ist eine geometrische Bedingung in
Modelllaengeneinheiten, kein Teilchenradius- oder Massengesetz.

Zweitens ist selbst eine exakt passende relative Rotation nicht genug:
Bei **nur zwei Altersplaetzen und einer Vierteldrehung pro Schritt**
($H=2,\theta=\pi/2$) erzwingt $F_T=0$ die Beziehung $a_1-b_1=-1$.
Die Selbst-/Kreuzchords sind dann gleich lang; bei gleichem Kernel,
$\eta,\chi>0$ und positiven Gewichten gilt

$$
|c_1|=\frac{\eta+\chi}{|\eta-\chi|}>1.
$$

Fuer $\eta=\chi$ ist bereits die Tangentialbalance unmoeglich.
Sonst hat der gemeinsame Normalblock neben eins den Multiplikator
$-c_1$ und ist instabil. Das ist **nur** dieser Zweialter-Vierteldrehungs-
Ausschluss, kein No-go fuer andere Winkel, laengere Memory oder das
H=1200-Paar. Die algebraische Gegenkontrolle setzt Koeffizienten vor;
sie behauptet nicht deren Realisierung durch einen gefundenen Gaussorbit.

## 8. Nahe Referenz: Paare mit gemeinsamem Wellengedaechtnis

Gezielte Primaerquellensuche am 2026-11-07 nach orbitierenden
Walking-Droplet-Paaren, keine systematische Literaturuebersicht.

**Oza, Siefert, Harris, Molacek und Bush (2017),**
[Orbiting pairs of walking droplets: Dynamics and stability](https://thales.mit.edu/bush/wp-content/uploads/2017/12/Oza-OrbitsPRF2017.pdf),
PR Fluids 2, 053601, DOI 10.1103/PhysRevFluids.2.053601.
Gelesen: Abstract, Modellgleichungen (1)-(10) und Diskussionsauszuege aus
III A-C und IV; kein vollstaendiger Audit des Anhangs oder der
Messdaten. Die Arbeit untersucht experimentell und theoretisch antipodal
orbitierende Paare. Das Modell summiert beide alternden Wellenspuren,
enthaelt jedoch vorgegebene Traegheit, Reibung, raeumlich gedaempfte
Besselwellen und einen angetriebenen Fluessigkeitsuntergrund. Eine
semiempirisch angepasste Abhaengigkeit der Auftreffphase von der lokalen
Wellenhoehe verbessert die Orbitalstabilitaet und den Messvergleich;
sie folgt nicht aus dem reduzierten horizontalen Modell selbst.
Die gemeinsame/relative Modentrennung ist dort bereits vorhanden.
**Einordnung:** hilfreicher klassischer Mechanismusvergleich, kein
Beleg fuer unsere freie 3D-Normalstabilitaet oder QFT. Die Auftreffphase
ist von unserem geometrischen $\pi$-Versatz zu unterscheiden. Eine
fehlende horizontale Falle bedeutet nicht fehlende aeussere Energiezufuhr.
Der alternative `math.mit.edu/sites/bush`-PDF-Link lieferte 404; gelesen
wurde die verlinkte Autorenfassung auf `thales.mit.edu`.

**Valani und Slim (2018),**
[Pilot-wave dynamics of two identical, in-phase bouncing droplets](https://arxiv.org/pdf/1806.10264v1),
arXiv v1 vom 27.06.2018; veroeffentlicht in Chaos 28, 096114,
DOI 10.1063/1.5032128 laut
[institutionellem Publikationseintrag](https://research.monash.edu/en/publications/pilot-wave-dynamics-of-two-identical-in-phase-bouncing-droplets/).
Gelesen: Einleitung, Modellgleichungen in II, Beginn IV und IX einschliesslich der
Experimentgrenzen; kein Volltext-/Numerikaudit aller Regime.
Die Gleichungen (1)-(2) koppeln zwei vorgegebene massive Punkte an die
Summe exponentiell alternder Besselspuren. Das liefert einen direkten
Vergleich fuer Selbst-/Kreuzmemory, aber weder unser endliches FIFO noch
einen Nachweis emergenter Masse. Die Autoren unterscheiden vorhergesagte
Paarregime von experimentell zugaenglichen Parametern und weisen auf
moegliche Aenderungen durch die vernachlaessigte variable Auftreffphase
hin. Das untersuchte Ortsproblem ist horizontal, nicht freie 3D-Bewegung.

Diese Vergleiche begruenden weder eine neue Impulsvariable noch einen
feldabhaengigen Gain in unserem Modell. Beides waeren zu entscheidende
Erweiterungen. Kollektive Bindung ist ein bekannter klassischer Effekt;
unser Ziel verlangt zusaetzlich einen eigenstaendigen Nachweis von
Quantendynamik, Ladung, Spin und dem Gravitationsanschluss.

## 9. Gegenpruefung: Positivitaetskriterium im Ankerbereich ausgeschlossen

Ergaenzung vom 2026-11-08 auf Grundlage von `ceb9d6a`. Keine neue
Zielrechnung oder Modellwahl. Geprueft wird die **Anwendbarkeit** des
hinreichenden Kriteriums, nicht erneut dessen mathematische Gueltigkeit.

### Zwei positive Altersgewichte genuegen zum Ausschluss

Fuer denselben effektiven Zweigausskernel auf beiden Ports schreibe

$$
k(u)=-P e^{-u/(2\sigma_r^2)}+Q e^{-u/(2\sigma_a^2)},\qquad
P=A_r/\sigma_r^2,\quad Q=A_a/\sigma_a^2,\quad P>2Q>0.
$$

Es gilt global fuer $u\geq0$

$$
k(0)+k(u)\leq-P+2Q,\qquad
|k'(u)|\leq L:=P/(2\sigma_r^2)+Q/(2\sigma_a^2).
$$

Definiere den gemeinsamen Koeffizienten ohne sein positives Altersgewicht:

$$
f(\varphi)=\eta k(2r^2(1-\cos\varphi))
             +\chi k(2r^2(1+\cos\varphi)),\qquad
c_\ell=w_\ell f(\ell\theta).
$$

Es seien $\eta,\chi\geq0$, $\eta+\chi>0$, $r>0$, $0<\theta<\pi$ und
$m=\lceil\pi/\theta\rceil\leq H-1$. Die Altersplaetze 1 und $m$ seien
mit strikt positiven Gewichten besetzt, wie bei geometrischer Memory
mit $0<\alpha<1$. Mit $\delta=m\theta-\pi\in[0,\theta)$ folgt aus
$2(1-\cos t)\leq t^2$ und der Lipschitzschranke fuer $k$:

$$
f(\theta)+f(m\theta)
\leq(\eta+\chi)[-(P-2Q)+Lr^2(\theta^2+\delta^2)]
\leq(\eta+\chi)[-(P-2Q)+2Lr^2\theta^2].
$$

Die Ausgangssumme ist $f(0)+f(\pi)=(\eta+\chi)[k(0)+k(4r^2)]$;
beide Argumentverschiebungen aendern die quadrierten Chordlaengen um
hoechstens $r^2\theta^2$ bzw. $r^2\delta^2$. Damit ist bewiesen:

$$
r\theta<\sqrt{\frac{P-2Q}{2L}},\quad
H-1\geq\lceil\pi/\theta\rceil
\quad\Longrightarrow\quad
c_1<0\ \text{oder}\ c_m<0.
$$

Mindestens eine Positivitaetsvoraussetzung des gemeinsamen Abklingsatzes
scheitert also. Wichtig: Wir verwenden **nicht** den Altersnullterm,
der aus diesem Normalblock herausfaellt. Der Befund ist unabhaengig
vom positiven Gain-Verhaeltnis und von der Groesse der beiden positiven
Altersgewichte. Eine Vorzeichenpruefung nur bei einer Querphase oder
kurzer sichtbarer Teilhistorie kann ihn uebersehen.

### Anwendung auf die dokumentierten Parameter, ohne neue Koeffizienten

Die gelesene
[Ankerspezifikation](../dynamics/rotation/scalar_memory_rotating_wave_initial_state_spec_2026-08-20.json)
setzt $\sigma_r=1$, $\sigma_a=3$, $A_r=1$, $A_a=7/2$ und Delta-Deposition.
Es sind daher exakt

$$
P=1,\quad Q=7/18,\quad P-2Q=2/9,\quad L=169/324,\qquad
\sqrt{(P-2Q)/(2L)}=6/13.
$$

Die in der Spezifikation gespeicherten Dezimalzahlen erfuellen
$0<r<1$, $1/100<\theta<1/50$ und $H\geq400$.
Dieser **ganze offene Geometriebereich** erfuellt die Schranken:
$r\theta<1/50<6/13$ und
$m\leq\lceil100\pi\rceil\leq315<H$.
Die Lesepruefung verwendet exakte Brueche aus den JSON-Dezimalzahlen,
nicht neu erzeugte H=1200-Koeffizienten, Root-Suche oder Trajektorien.
Sie zertifiziert keinen neuen Paarorbit aus dem alten Einzelkreis.

Die Aussage gilt fuer identische Ports und positive gemeinsame
Altersgewichte. Andere Kernel, verschiedene Gewichte, negative Gains,
zu kurze Historien oder Geometrien ausserhalb der Schranke sind damit
nicht beurteilt. Innerhalb des Bereichs hilft dem **Positivitaetskriterium**
weder eine additive Gain-Erhoehung noch eine Umverteilung bei fester
Gesamtstaerke. Aendert eine echte Bahn dabei Radius oder Winkel so weit,
dass sie den Bereich verlaesst, greift dieser Ausschluss nicht mehr.

### Warum das kein Instabilitaetsbeweis ist

Die Koeffizienten $c_1=-1/5$, $c_2=1/5$ liefern beispielsweise

$$
p(\mu)=(\mu-1)(\mu^2+1/5).
$$

Trotz negativem $c_1$ liegen alle Moden ausser der einfachen Translation
streng innerhalb des Einheitskreises. Dieses vorgeschriebene Polynom
ist eine algebraische Gegenkontrolle, kein nachgewiesener Gaussorbit.
Deshalb bleibt die volle Pruefung signierter gemeinsamer und relativer
Normalbloecke sowie der ebenen Bloecke erforderlich.

Die neun ergaenzten Kontrollen pruefen die rationalen Konstanten, sechs
vorab festgelegte kleine Zweiphasenbeispiele, die reine Parameter-
Zuordnung des Archivs und dieses Gegenbeispiel. Die frueheren
Konstruktionstests verwendeten bewusst auch andere Kernelparameter;
ihre bestandenen Identitaeten waren kein Nachweis fuer die Ankergeometrie.
Es wurde keine Suche nach einem guenstigen Gain oder Radius ausgefuehrt.

Verifikation der Gegenpruefung am 2026-11-08: 114 betroffene Tests
bestanden in 5.81 s, darunter alle 54 Kontrollen dieser Testdatei.
Vollstaendige konfigurierte Ruff-Pruefung und strikter MkDocs-Build
bestanden ebenfalls. Der analytische Ausschluss gilt fuer den oben
angegebenen ganzen Bereich; die sechs Punktkontrollen ersetzen seinen
Beweis nicht. Keine neue Literaturbehauptung oder Zielrechnung.
