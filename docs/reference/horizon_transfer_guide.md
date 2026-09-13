# Horizonttransfer: vom Ringspeicher zum unendlichen Gedaechtnis

Stand: 2026-09-13.

Diese Seite erklaert den Fixed-alpha-Horizonttest zuerst anschaulich und dann
bis zur implementierten Mathematik. Sie ist ein Lesepfad, keine zweite
Prioritaetenliste. Der verbindliche Arbeitsstand steht unter
[Projektprioritaeten](../status/project_priorities.md).

## 1. Die Frage in einem Satz

Unser Rechner speichert nur die letzten $H$ Positionen. Ein gefundener Kreis
koennte deshalb ein Artefakt des Abschneidens sein. Der Horizonttransfer fragt:
Bleibt derselbe lokale Loesungsast erhalten, wenn $H$ groesser wird, und liegt
auch fuer die unendliche exponentielle Erinnerung noch ein Root in der
kontrollierten Umgebung?

Der FIFO ist dabei nur eine Warteschlange nach Alter. Er schreibt keine
Kreisgeometrie vor. Die Kreisform folgt erst dann, wenn Kraftbalance,
Rootzertifikat und Dynamik gemeinsam bestehen.

## 2. Die Groessen aus dem Modellkern

| Symbol | Einfache Bedeutung | Rolle im Test |
| --- | --- | --- |
| $q=1-\alpha$ | Anteil der Erinnerung, der pro Schritt bleibt | Gewicht eines Eintrags vom Alter $j$: $\alpha M_0q^j$ |
| $H$ | Zahl gespeicherter Schritte | endlicher FIFO-Horizont |
| $B_H$ | normierte geometrische Gedachtnissumme | verbindet endliche Speicherung und Centerfilter |
| $g$ beziehungsweise $\eta$ | Staerke des gelesenen Kraftschritts | multipliziert das Memory-Kraftfeld |
| $(R,\theta)$ | Radius und Drehwinkel pro Schritt | zwei Unbekannte der Kreisbalance |
| $c$ | Memory-Center | mechanische Center-Variable, nicht die interne Kreisphase |
| $\mu$ | effektiver Center-Port-Koeffizient | gehoert nicht zum G4-Rootbeweis |

Fuer einen vorbereiteten Kreis $x_n=R e^{in\theta}$ reduziert sich das volle
Update auf zwei reelle Gleichungen $F_H(R,\theta)=0$: eine radiale und eine
tangentiale Balance. Ein Root ist also ein Wertepaar $(R,\theta)$, bei dem
beide Komponenten gleichzeitig verschwinden.

## 3. Was die Gates G0 bis G6 tun

| Gate | Frage | Was ein Pass bedeutet |
| --- | --- | --- |
| G0 | Stimmen Formeln, Darstellungen und direkter Replay? | technische Grundidentitaeten konsistent |
| G1 | Gibt es an jedem endlichen $H$ einen lokalen Root? | lokale Existenz je Leiterzelle |
| G2 | Gehoeren benachbarte Roots zum selben Ast? | ueberlappende Krawczyk-Homotopieroehren |
| G3 | Schrumpft der Rootdrift bei grossem $H$? | numerische Annaeherung statt Weglaufen |
| G4 | Ueberlebt die Gleichung den unendlichen Tail? | lokaler Root von $F_\infty$ in einer festen Box |
| G5 | Ist der grosse endliche FIFO lokal stabil? | Spektrum und Stoerungstrajektorien stimmen ueberein |
| G6 | Bestehen Speicher- und Nullkontrollen? | FIFO-Indexierung und $\eta=0$ verhalten sich korrekt |

G4 und G5 sind verschieden: G4 fragt, ob eine Gleichgewichtsloesung existiert.
G5 fragt, ob benachbarte Zustaende zu ihr zurueckkehren. Existenz ist noch
keine Stabilitaet.

## 4. G4 Schritt fuer Schritt

Die unendliche Gleichung wird nicht durch eine sehr lange Summe ersetzt,
sondern exakt in einen berechneten Kopf und einen beschraenkten Rest zerlegt:

$$
F_\infty(R,\theta)=F_H(R,\theta)+T_H(R,\theta).
$$

Fuer den Rest werden drei garantierte Obergrenzen benutzt:

$$
\|T_H\|_2\le b_0,
\qquad
\|\partial_R T_H\|_2\le b_R,
\qquad
\|\partial_\theta T_H\|_2\le b_\theta.
$$

Mit $q=1-\alpha$ lauten sie

$$
b_0=2\eta M_0\Phi_0q^H,
\qquad
b_R=4\eta M_0\Phi_1q^H,
$$

$$
b_\theta=\eta M_0(\Phi_0+2R_{\max}\Phi_1)
q^H\left(H+\frac q\alpha\right).
$$

Der Faktor $H+q/\alpha$ entsteht aus der geschlossenen geometrischen
Alterssumme $\alpha\sum_{j=H}^{\infty}j q^j$. Die Bounds werden nicht als
Punktkorrektur geraten, sondern als symmetrische Intervalle zu jeder
Residualkomponente und zur passenden Jacobi-Spalte addiert. Dadurch umfasst
die Rechnung jede Tailfunktion, die diese Schranken erfuellt.

## 5. Was Krawczyk hier beweist

Sei $X$ die kleine Box um den endlichen Root, $c$ ihr Mittelpunkt und $Y$
eine numerische Naeherung an den inversen Punktjacobian. Dann ist

$$
K(X)=c-YF_\infty(c)+(I-YDF_\infty(X))(X-c).
$$

Wenn die outward-rounded Rechnung

$$
K(X)\subset\operatorname{int}(X)
$$

zeigt, liegt in $X$ ein lokaler Root; unter den ueblichen
Krawczyk-Voraussetzungen ist er dort eindeutig. Zwei Rechnungen mit 120 und
160 Dezimalstellen muessen beide strikt einschliessen und ueberlappen.

Das ist kein globaler Einzigkeitsbeweis. Ein Fehlschlag ist wegen der bewusst
groben Tailbounds `inconclusive`, nicht automatisch ein Nichtexistenzbeweis.
Der Beweis bleibt ausserdem konditional auf `mpmath.iv` 1.3.0, solange kein
zweiter Intervallbackend denselben Einschluss reproduziert.

## 6. Was LCG-Arnoldi bedeutet

Arnoldi ist ein Verfahren, das aus dem sehr grossen FIFO-Jacobian nur die
wichtigsten Eigenwerte berechnet. Diese Eigenwerte beantworten spaeter G5:
Wachsen oder schrumpfen kleine Stoerungen?

Das Verfahren braucht einen Startvektor. Eine LCG, ein linearer
Kongruenzgenerator, erzeugt dessen Vorzeichen ausschliesslich durch feste
32-bit-Ganzzahlschritte. Wir verwenden sie nicht als physikalischen Zufall,
sondern als reproduzierbaren technischen Bauplan. Derselbe Seed erzeugt auf
Windows und Linux exakt dieselben Bytes. **LCG-Arnoldi ist daher nur der
portable Stabilitaetsrechner fuer G5 und keine Zutat der G4-Gleichung.**

## 7. Wie Befunde gelesen werden muessen

Ein isolierter G4-Pass stuetzt nur: In der registrierten lokalen Box existiert
unter den Tailbounds ein Root von $F_\infty$. Erst G1 bis G3 verbinden diesen
Root mit der endlichen Anchor-Leiter. Erst G5 fuegt lokale dynamische
Stabilitaet hinzu. G6 kontrolliert die Speicherimplementierung.

Keine Kombination dieser Gates beweist fuer sich physikalische Masse,
internen Spin, generische Knotenbildung oder Knoteninteraktion. Diese Claims
benoetigen eigene Observablen und Falsifikatoren.

