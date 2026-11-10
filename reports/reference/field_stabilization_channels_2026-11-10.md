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

## 6. Verifikation

[Kleine algebraische Kontrollen](../../tests/test_field_stabilization_channels.py)
pruefen quadratische Ergaenzung, eingefrorene/freie Feldkruemmung,
Gauss-Abschirmung, die Gram-Massenmatrix, exakte Projektorbeispiele,
Quellenprojektion, Basiswechsel und den vollrangigen Gegenfall.
Verifiziert am 2026-11-10: **22 neue, 55 betroffene Tests bestanden**
in insgesamt 8.10 s; konfigurierte Ruff-Pruefung und strikter MkDocs-Bau
bestanden. Keine vollstaendige Repository-Testsuite. Die Testdatei enthaelt
nur konstruierte Algebra, keinen neuen Produktionssolver.
Keine Zieltrajektorien, neue Parameterwahl oder Solitonreproduktion.
Die allgemeinen Aussagen folgen aus den angegebenen Herleitungen;
endliche numerische Proben ersetzen weder Beweise noch einen
Stabilitaetsnachweis fuer das nichtlineare Feld-/FIFO-System.
