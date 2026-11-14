# Feldstabilisierung: Kernbindung und elektrische Fernladung

Stand: 2026-11-10. Gezielter Literatur-/Algebraabgleich fuer den
[datengebundenen Wasserstoff-Benchmark](../../docs/reference/hydrogen_benchmark.md).
Keine neue Zielsimulation, kein Feldmodell in die native Memory eingebaut.
Die Bedeutung von N als moeglichem Massentraeger bleibt offen.

## Entscheidungsergebnis

**Ein stabilisierendes Feld und ein elektrischer Ladungskanal sind zwei
getrennt nachzuweisende Funktionen, nicht zwingend zwei verschiedene Felder.**
Die konkrete unten gepruefte Higgs-Stabilisierung darf aber nicht zugleich
als ungeschirmter elektromagnetischer Kanal eingesetzt werden. Das ist
eine strukturelle Auswahlbedingung vor jedem Massen-/Radiusfit.

Zusaetzlich muss das Feld bei einer Stabilitaetspruefung mitvariieren.
Eine Struktur in ihrem eingefrorenen Selbstfeld kann stabil erscheinen,
obwohl das gemeinsame System eine energiesenkende Richtung hat.
Diese beiden Tests konkretisieren den naechsten Modellvertrag; sie
ersetzen weder dessen Auswahl noch den Nachweis eines Teilchens.

Fortsetzung am selben Tag: Abschnitt 6 prueft eine konkrete nichtminimale
Mischkopplung. Sie umgeht das reine Kondensatstrom-Korollar, braucht aber
einen Kernstrom. Im angegebenen geschlossenen Vergleich bestimmt die
Verknuepfung allein nicht die Gesamtladung. Ein zusaetzlicher Kernzustand
schliesst die lokale Strombilanz, noch nicht die Dynamik oder Stabilitaet.

## 1. Zwei gezielte Literaturkontrollen

| Primaerquelle | Befund und Grenze |
| --- | --- |
| Eto, Hamada, Nitta, [Tying Knots in Particle Physics, PRL 135, 091603 (2025)](https://doi.org/10.1103/s3vd-brsn), veroeffentlicht 29.08.2025 | Zwei komplexe Skalarfelder und eine axionartige Eichkopplung stabilisieren verknuepfte Wirbel numerisch. Das stabilisierende elektrische Feld ist abgeschirmt. Gezeigte Verknuepfungszahlen sind 4 und 5; kleinere sind nicht allgemein ausgeschlossen. Endliche Kopplungen geben eine Barriere, kein absolutes Kreuzungsverbot. Quantentunneln bleibt moeglich. Das sind keine Elektronen- oder Protonmodelle. |
| Jaeykkae, Speight, [Supercurrent coupling destabilizes knot solitons, PRD 84, 125035 (2011)](https://doi.org/10.1103/PhysRevD.84.125035), [Volltext v2](https://arxiv.org/html/1106.5679v2) | Die Fortsetzung bekannter Hopf-Solitonen mit voller Superstromkopplung schrumpft im untersuchten Modell. Analytisch kann die Feldantwort den gegen Schrumpfen schuetzenden Term aufheben. Fehlende globale Minimierer schliessen nicht alle lokalen Minima aus. Die Autoren pruefen auch, ob scheinbare Minima Gitterartefakte sind. Kein allgemeines No-go fuer gekoppelte Felder. |

Gelesen: PRL S. 1--3, insbesondere Modell und Knot-Soliton-Abschnitt;
zusaetzlich [arXiv v2](https://arxiv.org/pdf/2407.11731v2), Anhang A,
Gauss-Nebenbedingung und numerisches Verfahren. Der separate PRL-Supplement-
Abruf war nicht zugaenglich; dessen Gleichheit mit dem alten Anhang ist
nicht verifiziert. Beim zweiten Artikel wurden Abschnitte 1--3 gelesen,
nicht der Code reproduziert. Kein systematischer Review, kein eigener
Kontinuums- oder Lebensdauernachweis. Der fruehere
[Abstractvergleich](../../docs/reference/fifo_structure_candidate.md#6-literaturvergleich-ohne-modellimport)
ist damit fuer diese Fragestellung vertieft, nicht als neue Simulation gezahlt.

## 2. Warum ein eingefrorenes Selbstfeld taeuschen kann

Eigene elementare Nachrechnung fuer eine **deklarierte Energieklasse**,
nicht fuer den nichtvariationalen FIFO-Kreis. Um einen stationaeren
Zustand seien u die Kern- und v die freien Feldvariationen. Nach Entfernung
von Symmetrie-/Eichnullrichtungen habe die quadratische Energie die Form

$$
E^{(2)}=\tfrac12u^T K u-u^T Bv+\tfrac12v^T L v,
\qquad L>0.
$$

Bei festgehaltenem v=0 sieht man nur K. Die korrekte lokale statische
Elimination ergibt durch quadratische Ergaenzung

$$
E^{(2)}=\tfrac12(v-L^{-1}B^Tu)^T L(v-L^{-1}B^Tu)
+\tfrac12u^T(K-BL^{-1}B^T)u.
$$

Damit ist $K_{\rm eff}=K-BL^{-1}B^T\preceq K$. Die volle Hesse-Matrix
ist genau dann positiv definit, wenn $K_{\rm eff}>0$. Beispielsweise
geben K=L=1 und B=2 bei eingefrorenem Feld positive Kruemmung 1,
aber nach Relaxation -3. Fuer $0<|B|<1$ bleibt dieses Beispiel positiv:
Feldkopplung ist also nicht grundsaetzlich destabilisierend.

K ist bereits die Kruemmung **des gekoppelten Modells** am betrachteten
Zustand, nicht die des isolierten Knotens. Der Vergleich beweist deshalb
nicht, dass ein Feld einen zuvor instabilen Knoten nie stabilisieren kann.
Bei Nebenbedingungen ist nur im zulaessigen Tangentialraum zu variieren.
Insbesondere ist das elektrostatische Potential A0 kein frei zu
minimierender physikalischer Modus; zuerst ist die Gauss-Bedingung zu loesen.
Fuer dissipative FIFO-Orbits bleiben stattdessen die vollstaendigen
Historien-/Feldvariationen und Floquet-Multiplikatoren erforderlich.

## 3. Kernladung ist nicht automatisch Fernladung

Als analytische Referenz in vorgegebenem aeusserem $\mathbb R^3$ sei

$$
(-\Delta+m_A^2)A_0=s,\qquad E=-\nabla A_0,
$$

mit homogener positiver Feldmasse $m_A$, lokalisierter Quelle und
abklingendem Rand. Fuer eine Punktquelle der Staerke Q gilt ausserhalb
des Ursprungs

$$
A_0(r)=\frac{Qe^{-m_A r}}{4\pi r},\qquad
\oint_{S_r}E\cdot dS=Q(1+m_A r)e^{-m_A r}.
$$

Bei $m_A>0$ verschwindet dieser Fluss fuer $r\to\infty$, obwohl
$\int s=Q\ne0$. Die lokale Bilanz lautet
$\nabla\cdot E=s-m_A^2 A_0$: Quelle und Abschirmungsantwort muessen
gemeinsam betrachtet werden. Eine Verknuepfungs- oder Kernquellzahl ist
somit nicht allein eine ungeschirmte elektrische Monopolladung.
Bei $m_A=0$ bleibt dagegen der Fluss Q. Auf einem begrenzten Messbereich
koennen sehr kleine Massen Coulomb-aehnlich wirken; dann ist die
Reichweiten-/Fehlerschranke anzugeben, nicht exakte Masselosigkeit zu behaupten.

Die positive Gauss-Feldenergie ist nach Elimination
$\tfrac12\langle s,(-\Delta+m_A^2)^{-1}s\rangle$.
Sie ist nicht die negative eliminierte Energie eines frei relaxierenden
skalaren Mediators aus der
[Bestandspruefung](interaction_structure_inventory_2026-11-02.md).
Die Punktquelle hier prueft nur das Fernfeld; ihre Selbstenergie ist
singulaer und definiert keinen endlichen Teilchenkern.

## 4. Ein konkreter Auswahltest fuer mehrere Kanaele

Referenzannahmen: endlich viele abelsche Eichkanaele mit kanonisch
positiver kinetischer Normierung, homogener Vakuumgrenze, linearer
statischer Antwort und lokalisierten direkten Quellen. Kein allgemeiner
Satz ueber stark gekoppelte Phasen. Fuer Kondensate
$\langle\phi_s\rangle=v_s/\sqrt2$ und
$c_s=(g_1q_{s1},\ldots,g_pq_{sp})^T$ liefert die Expansion von
$\sum_s|D\phi_s|^2$ um das Vakuum

$$
\mathsf M^2=\sum_s v_s^2c_sc_s^T,\qquad
\ker\mathsf M^2=\{n:c_s^Tn=0\ \text{fuer alle }s\text{ mit }v_s\ne0\}.
$$

Dies folgt direkt aus
$n^T\mathsf M^2n=\sum_s v_s^2(c_s^Tn)^2$.
Bei kinetischer Mischung muss vor diesem Test die positive kinetische
Form kanonisiert und die Quellen mittransformiert werden. Ein regulaerer
Basiswechsel kann aus einer vollrangigen Massenmatrix keinen Nullraum machen.

Sei $P_0$ der orthogonale Projektor auf diesen Nullraum, $P_a$ die
Projektoren auf die positiven Eigenwerte $m_a^2$. Fuer Punktquellen mit
Kopplungsvektoren $j_A,j_B$ ist die Kreuzenergie im linearen Vergleich

$$
V_{AB}(r)=\frac{1}{4\pi r}j_A^T
\left[P_0+\sum_{a:m_a>0}e^{-m_a r}P_a\right]j_B.
$$

**Entscheidend ist $P_0j$, nicht nur $\ker\mathsf M^2\ne0$.** Bei genau
einem masselosen Kanal mit Einheitsvektor n lautet dessen effektive
Ladung $q_{\rm eff}=n^Tj$. Der Vorzeichenvergleich ist dann
$V_{AB}\sim q_Aq_B/(4\pi r)$; bei mehreren masselosen Kanaelen bleiben
Ladungsvektoren. Fuer ausgedehnte Kerne sind die j durch die aus der
vollstaendigen Loesung bestimmten Monopolkoeffizienten zu ersetzen;
sie duerfen nicht allein aus einem Flavorlabel behauptet werden.

Eine schaerfere Quellenbedingung folgt ohne Parametersuche: Sind die
einzigen Quellen die minimal gekoppelten Stroeme genau der im Vakuum
kondensierten Spezies, gilt punktweise

$$
j^\mu(x)=\sum_{s:v_s\ne0}c_s I_s^\mu(x)
\quad\Longrightarrow\quad P_0j^\mu(x)=0.
$$

Die skalaren Stromkoeffizienten $I_s^\mu$ duerfen dabei beliebige
Profile haben. Auch ein lokales Verschwinden eines solchen Kondensats
im Kern aendert nicht seinen Ladungsvektor oder den asymptotischen
Nullraum. Ein ungebrochener Kanal allein reicht fuer diese Quellenklasse
also nicht. Eine weitere, im Vakuum nicht kondensierte geladene Spezies
oder eine anderweitig begruendete topologische/mischende Quelle koennte
die Voraussetzung aendern; ihre Existenz und Ladung sind zusaetzlich
nachzuweisen. Nichtminimale Kopplungen sind von diesem Korollar nicht erfasst.

Ein exakt pruefbares Zweikanalbeispiel, **kein ausgewaehltes Modell**:
$v=1$, $c=(1,1)^T$ geben

$$
\mathsf M^2=\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
P_0=\tfrac12\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
$$

Die Quelle $j=(1,1)^T$ bleibt trotz masselosem Kanal vollstaendig
abgeschirmt. Fuer $j=(1,0)^T$ ist $j^TP_0j=1/2$; die Gegenquelle -j
hat den negativen Kreuzkoeffizienten. Ein zweites unabhaengiges Kondensat
mit $c_2=(1,-1)^T$, $v_2=1$ ergibt $\mathsf M^2=2I$: auch der letzte
masselose Kanal verschwindet. Die Quelle $(1,0)^T$ ist insbesondere
nicht aus dem einzigen minimalen Kondensatstrom $(1,1)^T I^\mu$
hergeleitet. Die Kondensatrichtungen beschraenken also
die Architektur, bevor ihre Staerken numerisch angepasst werden.

## 5. Konsequenz fuer den ersten Feldbenchmark

Die Kernbindung darf zunaechst phaenomenologisch sein, aber ihre Energie,
Rueckwirkung und Freiheitsgrade sind vollstaendig zu deklarieren. Ein
eigener ungeschirmter Kanal ist nur dann nutzbar, wenn derselbe Kern
eine begruendete Quelle dafuer besitzt. Einen leeren Maxwell-Kanal
neben einen neutralen stabilen Knoten zu stellen wuerde den Test nicht bestehen.

Soll die konkrete gebrochene-U(1)-Route als Kernmechanismus verwendet
werden, braucht der Wasserstoffvergleich zusaetzlich einen geeigneten
ungeschirmten Kanal oder eine ungebrochene Linearkombination. Innerhalb
dieser abelschen Referenzklasse sind zwei Eichkanaele mit Rang eins ein
kleinstes algebraisches Beispiel, aber noch kein stabiler Soliton.
Alternativ koennte ein neutraler Bindungsmechanismus mit einem einzigen
ungebrochenen U(1)-Kanal kombiniert werden. **Zwei Eichfelder sind daher
keine universelle Notwendigkeit.** Keine dieser Erweiterungen ist hier gewaehlt.

Die aktuelle Arbeitsentscheidung bleibt in den
[Projektprioritaeten](../../docs/status/project_priorities.md): zuerst
einen gemeinsamen Kern-/Quellenvertrag ausarbeiten, erst danach einen
begrenzten Solverlauf entscheiden. Echte emergente Ladung, Spin/Statistik,
Quantendynamik und Gravitation bleiben offen. Bekannte Eichgleichungen
oder vorgegebene Quellladungen gehoeren bis zu einer Herleitung in den
getrennten Referenzzweig; sie sind kein Beweis fuer QFT aus FIFO.

## 6. Konkreter Anschluss: Mischkopplung mit Kernstrom

### Quelle im ungeschirmten Kanal

Als **Pruefhypothese**, nicht native Regel, seien X ein Higgs-Kanal und A
ein ungebrochener Maxwell-Kanal. Ausserhalb der Defektkerne betrachte

$$
S_{\rm mix}=\kappa\int\theta F_A\wedge F_X,\qquad
F_A=dA,\quad F_X=dX,\quad p=d\theta.
$$

Das Differential d bezeichnet hier Raumzeit, $\wedge$ das aeussere
Produkt. Die Normierung ist durch diesen Term festgelegt. Variation
nach A liefert bei kanonischem Maxwell-Term
$d{*F_A}=J_{\rm bulk}=\kappa p\wedge F_X$, ausserhalb der Kerne und
ohne weitere Quellen. Statisch ist die Dichte
$\kappa\nabla\theta\cdot B_X$. Sie koppelt an A, obwohl die
kondensierten Felder unter A neutral sein koennen. Das ist ein konkreter
nichtminimaler Ausweg aus Abschnitt 4, kein Nachweis einer Gesamtladung.

Fuer global glattes, einwertiges $\theta$, $\nabla\cdot B_X=0$ und
verschwindenden Randterm ist bereits
$\int\nabla\theta\cdot B_X=\int\nabla\cdot(\theta B_X)=0$.
Ein nichttrivialer Wicklungsfall verlangt einen anderen Zustandsraum.

### Erhaltung verlangt einen Kernbeitrag

Fuer eine geschlossene String-Weltflaeche $\Sigma$ mit Wicklung w gilt
im idealisierten Defektgrenzfall $dp=2\pi w\delta_\Sigma$. Die
Zweiform $\delta_\Sigma$ ist die orientierte Poincare-Duale der
Weltflaeche. Ohne magnetische Monopole ist $dF_X=0$, also

$$
dJ_{\rm bulk}=2\pi\kappa w\delta_\Sigma\wedge F_X.
$$

Dieser Ausdruck ist bei allgemeinen zulaessigen Feldstoerungen nicht null.
Eine reine statische Magnetfeldprobe kann ihn uebersehen. Maxwell verlangt
hingegen $dJ_{\rm total}=d^2{*F_A}=0$.
Mit $c=2\pi\kappa w$ lautet eine lokale kinematische Vervollstaendigung

$$
J_{\rm core}=\xi\wedge\delta_\Sigma,\qquad
d_\Sigma\xi=-cF_X|_\Sigma,\qquad
\xi=-cX|_\Sigma+d_\Sigma\sigma.
$$

Dann ist $d(J_{\rm bulk}+J_{\rm core})=0$. Unter
$X\mapsto X+d\lambda$, $\sigma\mapsto\sigma+c\lambda|_\Sigma$
bleibt $\xi$ invariant. Auf nichttrivialen Weltflaechen sind diese
Ausdruecke patchweise zu verstehen; globale Vertraeglichkeit ist eine
weitere Bedingung. Ein nachtraeglicher beliebiger Bilanzrest ersetzt
keine physikalische Kerndynamik.

Diese bekannte Struktur ist in
[Heidenreich--Reece--Rudelius, JHEP 11 (2021) 004, Anhang B](https://arxiv.org/pdf/2108.11383v2)
fuer mehrere Eichfelder ausgearbeitet. Gelesen wurden B.1--B.2,
einschliesslich der zusaetzlichen Dualitaetsbedingung ihres Beispiels.
Wir uebernehmen **nicht** die dortigen Weak-Gravity-/String-Vermutungen
als Beweise fuer unser Ziel und waehlen noch keine Weltflaechenwirkung.

### Gegenkontrolle ohne singulaere Ableitungen

Lokal an einer geraden Weltflaeche in t,z ersetze den Winkelgradienten
durch die glatte Einform, $a>0$,

$$
p_a=w\frac{-y\,dx+x\,dy}{r^2+a^2},\quad
dp_a=\frac{2wa^2}{(r^2+a^2)^2}dx\wedge dy,\quad r^2=x^2+y^2.
$$

Das ist ein konstruierter Regulator, keine hergeleitete Kernloesung.
Fuer $F_X=\mathcal E\,dt\wedge dz$ ergibt sich
$dJ_{\rm bulk}=2\kappa w\mathcal E a^2/(r^2+a^2)^2$
mal das orientierte Raumzeitvolumen. Sein transversales Integral ist
$2\pi\kappa w\mathcal E$, fuer jede positive Kernbreite a. Glaetten
allein entfernt den fehlenden Strom nicht. Mit $X=\mathcal E t\,dz$
hebt der lokale Term $-\kappa\,dp_a\wedge X$ dessen Divergenz auf.
Dies prueft eine Bilanz, keine Loesung der gekoppelten Feldgleichungen.

Der physikalische Kernregulator und seine Stroeme werden im konkreten
Fermionmodell von [Harvey--Ruchayskiy, JHEP 06 (2001) 044](https://arxiv.org/pdf/hep-th/0007037)
behandelt; gelesen wurden Abschnitte 2.1--2.2 bis zur Stromformel (20).
Dort sind Fermionen Inputs. Das ist keine Entstehung von Fermionen aus FIFO.

### Verknuepfung und Gesamtladung sind verschieden

Auf einem Zeitschnitt sei C der geschlossene Kern, X global regulaer,
ohne Monopole, und der Randterm von $p\wedge X$ bei unendlich null.
Aus $d(p\wedge X)=dp\wedge X-p\wedge F_X$ folgt

$$
Q_{\rm bulk}=c\oint_C X,\qquad
Q_{\rm core}=-c\oint_C X+\oint_C d_\Sigma\sigma,
\qquad Q_{\rm total}=\oint_C d_\Sigma\sigma.
$$

Im duennen Flussschlauchvergleich ist $\oint_C X=\Phi_X\,\mathrm{Lk}$:
Die Verknuepfung liefert einen **Teilbeitrag**, der sich in dieser Bilanz
aufhebt. Bei global einwertigem reellem $\sigma$ ist die Gesamtladung null.
Ein konsistenter kompakter Kernzustand mit Periode P koennte dagegen
$Q_{\rm total}=P n$ tragen. Periode, erlaubte Sektoren und grosse
Eichtransformationen muessen zur Gesamtwirkung passen; sie sind nicht
aus Memory oder der geometrischen Verknuepfung bestimmt. Hier betrachtet
werden regulaere Eichtransformationen, die in den umgebenden Raum
fortsetzbar sind, keine unbegruendete Gleichsetzung von Sektoren.
Die ganze Zahl n ist eine Wicklungszahl, nicht die angefragte Schrittzahl N.
Eine Dynamik koennte Kernzustand und Verknuepfung korrelieren; die obige
Bilanz allein leitet eine solche Beziehung weder her noch schliesst sie aus.

Der Einkanalvergleich in
[Agrawal et al., JHEP 01 (2022) 103, Abschnitte 2 und 3.1](https://doi.org/10.1007/JHEP01(2022)103)
trennt ebenfalls Feld-, Kern- und Gesamtladung; diese Abschnitte wurden
im Verlagsvolltext gelesen. Keine Uebernahme seiner astrophysikalischen
Groessen oder Reproduktion seiner Dynamik. Die obige Zweikanalbilanz
folgt aus den expliziten Annahmen, nicht aus einem ungeprueften Transfer
der gesamten Einkanaltheorie.

**Konsequenz:** Den nackten Bulk-Term nicht als fertigen geladenen
Solitonsimulator verwenden. Ein Kernzustand samt Strom und Energie ist
ein konkreter benoetigter Baustein. Die A-Strombilanz ist kinematisch
geschlossen; X-/Phasendynamik, globale Wirkung, Quellenenergie,
Stabilitaet und der Memory-Anschluss bleiben offen. Ein kompakter
Kernzustand ist weder automatisch FIFO-Altersphase noch Spin 1/2.

## 7. Verifikation

[Kleine algebraische Kontrollen](../../tests/test_field_stabilization_channels.py)
pruefen quadratische Ergaenzung, eingefrorene/freie Feldkruemmung,
Gauss-Abschirmung, die Gram-Massenmatrix, exakte Projektorbeispiele,
Quellenprojektion, Basiswechsel und den vollrangigen Gegenfall.
Die Fortsetzung ergaenzt 15 Kontrollen zu Regulator, Strombilanz,
Eichtransformation und Teil-/Gesamtladung, insgesamt 37 in dieser Datei.
Verifiziert am 2026-11-10: **70 betroffene Tests bestanden**
in insgesamt 4.81 s; konfigurierte Ruff-Pruefung und strikter MkDocs-Bau
bestanden. Keine vollstaendige Repository-Testsuite. Die Testdatei enthaelt
nur konstruierte Algebra, keinen neuen Produktionssolver.
Keine Zieltrajektorien, neue Parameterwahl oder Solitonreproduktion.
Die allgemeinen Aussagen folgen aus den angegebenen Herleitungen;
endliche numerische Proben ersetzen weder Beweise noch einen
Stabilitaetsnachweis fuer das nichtlineare Feld-/FIFO-System.

Autorenentscheidung vom 2026-11-11: Freiheitsgrade im Emergenzzweig erst
aus Memory herleiten und daneben einen getrennten phaenomenologischen
Feld-/Kernbenchmark ausarbeiten. Der [konkrete Anschluss](memory_core_phase_bridge_2026-11-11.md)
prueft einen aus Historien gebildeten Phasenreadout und definiert eine
Witten-Referenz mit explizitem Ladungstraeger. Er importiert keinen dieser
Feldfreiheitsgrade in FIFO und ist kein neuer Simulationslauf.
