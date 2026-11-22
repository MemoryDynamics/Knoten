# Warum das native Lesepotential noch keine gemeinsame Wirkung ist

Stand: 2026-11-22. Analytischer Anschluss an den
[Bahnphasentest](memory_gravity_action_phase_2026-11-22.md).
Feste Pfadvariationen und Quadratur, keine neue Modellregel und
keine neue Zieltrajektorie.

**Ergebnis.** Auf einer einzelnen Ortsbahn ist der verzoegerte
native Drift nicht der Gradient einer Wirkung. Er reagiert auf
Veraenderungen frueherer Orte, waehrend die umgekehrte Ableitung
null ist. Das Variieren der Summe der Lesepotentiale liefert
zusaetzlich einen Term aus spaeteren Zeiten und aendert die
Dynamik. Der exakte stochastische Pfad besitzt zwar eine
Antwortdarstellung mit einem Faktor i, aber sein integriertes
Gewicht bleibt eine positive klassische Wahrscheinlichkeit.

## 1. Der Zwei-Zeiten-Test

Beim [bedingten Lesepotential](../../docs/reference/memory_pair_energy.md)
bleibt der ganze Speicher beim Differenzieren des Kopfes fest.
Hier variieren wir dagegen einzelne Orte einer *konsistenten*
Bahn, einschliesslich ihrer spaeteren Rolle als gespeicherte
Orte. Betrachte ein endliches Zeitfenster mit frei variierbaren
inneren Zeiten und festgehaltener Vorgeschichte. Der skalare
Eigenmemory-Beitrag am Ort $x_n$ ist

$$
b_n[x]=-\eta\sum_{j=1}^{H-1} w_j\nabla K(x_n-x_{n-j}).
$$

Der Altersnullterm ist bei radialem glattem $K$ kraftlos.
Liegen $n-j$ und $n$ beide im freien Teil, ist

$$
D_{x_{n-j}}b_n=+\eta w_j D^2K(x_n-x_{n-j}),\qquad
D_{x_n}b_{n-j}=0.
$$

Die erste Ableitung ist im aktiven Kanal nicht identisch null:
Es genuegen $\eta w_j\ne0$ und nichtverschwindende Kruemmung
des effektiven Kernels an einem erreichbaren Pfadargument.
Hier meint erreichbar nur eine frei waehlbare Pfadvariation,
keine autonom ausgebildete Trajektorie. Fuer einen $C^2$-Skalar
$S[x]$ muessten die Ableitungen von $b_n=-\partial_{x_n}S$
transponierte gemischte Hessianbloecke sein. Der vorliegende
Drift ist daher off shell kein solcher Wirkungsgradient.
Eine konstante nichtverschwindende Umrechnung von Drift in
Kraft oder die Addition einer echten lokalen Bewegungswirkung
hebt diese Asymmetrie nicht auf. Sind alle verzoegerten
Ableitungen identisch null, greift der Test nicht.

Geprueft wird der **additive native Kraftkandidat in diesen
Koordinaten**. Das ist kein Satz gegen alle aequivalenten
Bewegungsgleichungen, andere Variablen, einen konservativen
Skalengrenzwert oder eine Wirkung mit dynamischem Medium.
Ein fest vorgegebenes aeusseres Feld ist auch kein verzoegerter
Selbstterm und faellt nicht unter den Ausschluss.

## 2. Was die Summe der Lesepotentiale wirklich variiert

Fuer Paare innerhalb des Fensters bilde
$V[x]=\eta\sum_n\sum_{j\geq1} w_j K(x_n-x_{n-j})$.
Randterme aus festgehaltener Vorgeschichte koennen als
ausserer Beitrag mitgefuehrt werden. Fuer gerades $K$ ergibt
sich im Inneren

$$
-\partial_{x_n}V
=b_n[x]-\eta\sum_{j:\,n+j\ \text{im Fenster}}
w_j\nabla K(x_n-x_{n+j}).
$$

Die zweite Summe kommt daher, dass der Punkt $x_n$ in den
spaeteren Potentialen selbst eine Quelle ist. Das ist der
diskrete nichtlineare Gegenfall zum zeitlich symmetrisierten
Oszillatorkern bei [Galley (2013), Gl. (2)-(4)](https://link.aps.org/accepted/10.1103/PhysRevLett.110.174301).
Den zusaetzlichen Term wegzulassen ist keine Aenderung der
Notation, sondern eine Aenderung der Variationsregel.

Auch ein durch stationaere Variation eliminiertes Feld
beseitigt das Problem nicht automatisch. Ist $S[x,y]$
glatt und liefert $S_y=0$ einen glatten Zweig $y_*(x)$,
dann bleibt $S[x,y_*(x)]$ ein Skalar mit symmetrischer
Hesse-Matrix. Ein retardiert aus Anfangsdaten geloester
Mediumkanal muss nicht diesem Zweig eines gemeinsamen
Randwertproblems entsprechen. Seine volle Dynamik oder eine
passende Zwei-Pfad-Beschreibung bleibt gesondert zu begruenden.

## 3. Was schon exakt als Antwortfunktion existiert

Sei $\epsilon>0$ die Standardabweichung der unabhaengigen
Gauss-Kopfinnovationen, und sei
$r_n=x_{n+1}-x_n-b_n[x]$ der zu einer vorgegebenen Bahn passende
Innovationswert. Bei fester Anfangshistorie ist die Abbildung
der Folge neuer Orte auf $(r_n)_n$ block-dreieckig mit
Einheitsbloecken auf der Diagonale: $b_n$ haengt nicht von
$x_{n+1}$ ab. Die inverse Rekursion ist eindeutig. Die
bedingte Pfaddichte ist damit exakt

$$
\begin{aligned}
p[x\mid\text{Historie}]
&=\prod_n\frac{\exp(-\|r_n\|^2/(2\epsilon^2))}
                  {(2\pi\epsilon^2)^{d/2}}\\
&=\int\prod_n\frac{d^d\lambda_n}{(2\pi)^d}
\exp\left[\sum_n\left(i\lambda_n\cdot r_n
-\frac{\epsilon^2}{2}\|\lambda_n\|^2\right)\right].
\end{aligned}
$$

$\lambda_n$ ist eine integrierte Fourier-Hilfsvariable, kein
Knotenzustand. Die lineare Form $\sum_n\lambda_n\cdot r_n$
liefert beim Variieren nach dieser zweiten Variablen die
kausale Residualgleichung ohne Term aus spaeteren Zeiten in der
Memory-Kraft. Nach Integration steht aber wieder eine
reelle, positive Dichte. Die reelle Kostenfunktion
$\sum_n\|r_n\|^2/(2\epsilon^2)$ ist weder eine mechanische
Wirkung noch ein Phasenwinkel. Die Antwortdarstellung
ist eine endliche explizite Version der klassischen
Antwortfeldmethode, vgl.
[Martin, Siggia und Rose (1973)](https://doi.org/10.1103/PhysRevA.8.423).

## 4. Positivkontrolle und Folgerung

Bei **gegebenem** konservativem Potential $V(x,t)$ erzeugt
derselbe Term $-\int V\,dt$ die mechanische Kraft
$-\nabla V$ und in der quantenmechanischen Referenz den
Wirkungsphasenbeitrag. [Feynman und Vernon (1963),
Gl. (3.1)-(3.2)](https://doi.org/10.1016/0003-4916(63)90068-X)
zeigen fuer diesen Fall den Einflussfaktor zwischen zwei
unabhaengigen Historien. Das ist strukturell etwas anderes als
die Fourier-Integration einer einzigen klassischen Pfaddichte.
Insbesondere liefert die Pfaddichte keine Phasendifferenz bei
kohaerenter Rekombination.

Der gemeinsame Kraft-/Phasentest kann folglich nicht mit der
unveraenderten retardierten Leseregel und dem blossen Etikett
Wirkung bestanden werden. Fuer eine positive Route ist ein
gemeinsam hergeleiteter Medien- oder Kollektivabschluss
zu pruefen, der den konservativen Kraftanteil von der
retardierten Antwort trennt und die relative Phase selbst
traegt. Ein mathematisches Verdoppeln der Koordinaten oder
ein externer bekannter Potentialterm ist noch keine Herleitung
dieses Abschlusses aus Memory.

Die [festen Kontrollen](../../tests/test_memory_path_action.py)
pruefen am vorhandenen Gauss-Kernel die gemischten Zeitableitungen,
den Zusatzterm, den Einheits-Jacobian und die positive Fourier-
Ruecktransformation an vorgegebenen Pfaden.
