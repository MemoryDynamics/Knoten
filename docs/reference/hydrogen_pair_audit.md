# Direkte Paarkopplung gegen den Wasserstoff-Benchmark

Stand: 2026-10-28. Analytische Bestandspruefung und kleine synthetische
Softwarekontrollen, keine Zielsimulation. Dieser Audit konkretisiert den
[Paper-III-Benchmark](hydrogen_benchmark.md), ohne eine neue Modellregel
oder physikalische Teilchenidentifikation einzufuehren.

**Ergebnis:** Der vorhandene direkte Kanal liefert eine genau definierte
klassische Wechselwirkung. Er liefert nicht bereits Traegheitsmassen,
eine Impuls-/Energiebilanz oder eine geschlossene aeussere 3D-Dynamik.
Fuer lokalisierte Quellen und endlich viele feste Gaussbreiten fehlt ihm
ein asymptotischer Coulomb-Schwanz. Dies begrenzt diesen direkten Readout,
nicht jede moegliche kollektive effektive Theorie des Gesamtmodells.

## Gepruefte Regel und Eingaben

Codebasis: [`reciprocal_nodes.py`](https://github.com/MemoryDynamics/Knoten/blob/88d56c84d9546df4cc5ab8afe79da8c270433cf8/src/emergenz_knoten/reciprocal_nodes.py),
[`_continuation.py`](https://github.com/MemoryDynamics/Knoten/blob/88d56c84d9546df4cc5ab8afe79da8c270433cf8/src/emergenz_knoten/_continuation.py),
[`kernels.py`](https://github.com/MemoryDynamics/Knoten/blob/88d56c84d9546df4cc5ab8afe79da8c270433cf8/src/emergenz_knoten/kernels.py)
und der orientierte Readout in
[`vector_memory.py`](https://github.com/MemoryDynamics/Knoten/blob/88d56c84d9546df4cc5ab8afe79da8c270433cf8/src/emergenz_knoten/vector_memory.py).
Die Schlussfolgerungen werden nicht auf alle archivierten
Mehrsystemvarianten uebertragen.

Fuer $i=A,B$ besteht der Zustand aus aktuellem Punkt $x_i$, altersgeordneter
Historie $y_{ij}$ und festen nichtnegativen Gewichten $w_{ij}$ mit
$W_i=\sum_jw_{ij}>0$. Beide Historien muessen im geprueften Paar-API
dieselbe Laenge $H$ und dieselbe Eingabedimension $d$ haben. Mit
$\chi=\texttt{cross_eta}\geq0$ lautet der synchrone Schritt

$$
x_i^+=x_i+\epsilon_i\xi_i-\eta_iG_i^{\rm self}
-\chi G_{i\leftarrow k},\qquad k\ne i,
$$

$$
G_{i\leftarrow k}=\sum_jw_{kj}\nabla K_{\rm cross}(x_i-y_{kj}),
\qquad K_{\rm cross}(z)=\sum_s a_s e^{-|z|^2/(2\sigma_s^2)}.
$$

Hier sind fuer den Doppelgauss-Kernel $a_1=A_{\rm rep}$ und
$a_2=-A_{\rm att}$; endliche Gauss-Deposition wird in die effektiven
Amplituden/Breiten aufgenommen. Beide Kreuzgradienten lesen den alten
Gesamtzustand. Erst danach werden beide neuen Punkte geschrieben und
die aeltesten Eintraege entfernt. Einweg- und ausgeschalteter Kanal
verwenden dieselben node-spezifischen Rauschfolgen als Gegenkontrollen.

Der gemeinsame Kreuzkernel wird ohne expliziten `cross_readout` aus der
**ersten** Konfiguration gewaehlt. Auch bei explizitem `cross_readout`
stammen Depositionsart und -breite fuer beide Kreuzrichtungen aus der
ersten Konfiguration. Die zweite Konfiguration bestimmt ihren eigenen
Selbstkanal, keinen separaten Kreuz-Depositionskernel. Das ist die
implementierte Konvention, keine nachgewiesene universelle Kopplungsregel.
Eine quellenabhaengige Konvention waere eine zu entscheidende Aenderung.

| Bestandteil | Implementiert / Input | Fuer den physikalischen Benchmark offen |
| --- | --- | --- |
| Zustands- und Ortsraum | $d$, $H$, Historien und euklidische Metrik | Beobachtungsabbildung, interne/aeussere Trennung und kontrollierte Reduktion |
| Quellenstaerke | $W_i$ und Altersgewichte | Erhaltene additive Ladung und ihre Kalibrierung |
| Bewegung | Selbstdrift, Rauschen, ein gemeinsames $\chi$ | Kraft-/Zeitmassstab, unabhaengig bestimmte Traegheit und Massenverhaeltnis |
| Paarwirkung | Direkter Zugriff auf die fremde Vergangenheit | Bilanz des Gesamtsystems einschliesslich moeglicher Feld-/Mediumanteile |
| Geometrische Readouts | Aktuelle Punkte, Memory-Center, Kovarianz, Radiusverhaeltnis | Physikalischer Schwerpunkt, Energie, Spin, magnetisches Moment |
| Quantenzustand | Keine Amplitude oder Messregel in diesem Paar-API | Gemeinsame Wirkungsskala, Statistik und atomare Uebergaenge |

## Bidirektionale Antwort ist noch keine Impulsbilanz

Bezeichne mit $\delta_\times$ den Unterschied eines einzelnen Schritts
gegen den abgeschalteten Kanal bei identischem Anfangszustand und
Rauschen. Fuer $c_x=(x_A+x_B)/2$ und $d_x=x_B-x_A$ gilt exakt

$$
\delta_\times c_x=-\frac\chi2
(G_{A\leftarrow B}+G_{B\leftarrow A}),\qquad
\delta_\times d_x=-\chi
(G_{B\leftarrow A}-G_{A\leftarrow B}).
$$

Im Allgemeinen verschwindet die Summe der Kreuzgradienten nicht:
Ein aktueller Punkt liest eine ausgedehnte vergangene Quelle, nicht
ausschliesslich den anderen aktuellen Punkt. Ungleiche Historienformen
genuegen auch bei gleichem $W_A=W_B$. Der vorhandene symmetrische
Regressionstest belegt die Ausloeschung nur fuer seine spiegelgleichen
Praeparationen, keine Identitaet fuer beliebige Zustaende.

Ein explizites synthetisches Gegenbeispiel verwendet $H=5$, Gewichte
$(0.4,0.15,0.15,0.15,0.15)$ und um den jeweiligen Mittelpunkt die Punkte
$0,\pm r_i e_1,\pm r_i e_2$, mit $x_i$ im Mittelpunkt. Setze
$r_A=0.2$, $r_B=0.8$, Mittelpunktabstand $2e_1$,
$(\sigma_{\rm rep},\sigma_{\rm att})=(1,2)$,
$(A_{\rm rep},A_{\rm att})=(1,3)$ und $\chi=0.02$.
Selbstdrift und Rauschen sind aus. Die unabhaengig summierten
Gaussgradienten stimmen mit dem Paar-Update ueberein; die beiden
Kreuzinkremente summieren sich nicht zu null. Bei $r_A=r_B$ besteht
die Spiegelkontrolle. Das ist ein mathematischer Gegencheck, kein
Praeparations- oder Stabilitaetsnachweis realer Knoten.
Eine weitere Kontrolle verwendet die nativen Gewichte
$w_j=0.2(0.8)^j$: Die positiven Achsenpunkte werden jeweils um den
Faktor $1/0.8$ gestreckt, sodass die Quellen weiterhin zentriert sind.
Auch dort verschwindet die Inkrementsumme nicht. Die symmetrischen
Testgewichte sind also nicht die Ursache des Gegenbeispiels.

Auch die Memory-Center verbergen diesen Effekt nicht. Nach einem
gemeinsamen FIFO-Schritt gilt

$$
\delta_\times\bar y_i=\frac{w_{i0}}{W_i}\delta_\times x_i,
$$

weil die anderen behaltenen Eintraege zwischen den beiden Armen gleich
sind. Weder $c_x$ noch $(\bar y_A+\bar y_B)/2$ ist allerdings schon
ein physikalischer Massenschwerpunkt. **Der Befund beweist keine Verletzung
einer bereits definierten Gesamtimpulserhaltung:** Ein physikalischer
Impuls und eine moegliche Bilanz des Mediums fehlen hier erst noch.
Bidirektionalitaet allein liefert diese Bilanz nicht.

Bei fester Historiengeometrie skaliert $w_{Bj}\mapsto b w_{Bj}$ den
Kreuzdrift von A um $b$, nicht den von B. Das belegt eine Quellenstaerke,
keine gemessene Traegheit von B. Eine geometrische Groessenabhaengigkeit
des Readouts ist ebenso wenig bereits das Proton-Elektron-Massenverhaeltnis.
Die volle Historie kann effektive dynamische Antwort erzeugen; die
Erstordnungsform des Updates schliesst das nicht aus. Der
[separate P5-D-Center-Port](implemented_equations.md) ist ein anderes
Kopplungsgesetz und hat Traegheit ebenfalls nicht nachgewiesen.

## Direkter Gauss-Readout und Coulomb-Grenze

Betrachte eine feste orthogonale Projektion $P$ auf drei aeussere
Koordinaten. Es gelte $X=Px$, $Y_j=Py_j$, $|X|=r>R$ und
$|Y_j|\leq R$. Weitere Koordinaten von $x,y_j$ bleiben beliebig. Fuer
endlich viele feste $0<\sigma_s<\infty$, endliche $a_s$ und feste
Quellenmasse $W=\sum_jw_j$ folgt aus
$|x-y_j|\geq|X-Y_j|\geq r-R$ und $|X-Y_j|\leq r+R$:

$$
\left|P\sum_jw_j\nabla K(x-y_j)\right|
\leq W(r+R)\sum_s\frac{|a_s|}{\sigma_s^2}
\exp\!\left[-\frac{(r-R)^2}{2\sigma_s^2}\right].
$$

Insbesondere geht $r^2|G_{\rm ext}|$ gegen null. Eine feste endliche
Gauss-Deposition ersetzt lediglich
$\sigma_s^2\mapsto\sigma_s^2+s_{\rm dep}^2$ und
$a_s\mapsto a_s(\sigma_s^2/(\sigma_s^2+s_{\rm dep}^2))^{d/2}$;
sie aendert dieses Resultat nicht. Zusaetzliche innere Koordinaten
heben die Schranke fuer diesen euklidischen Projektionsreadout nicht auf.

Zum Vergleich: Eine isolierte statische Ladung hat in 3D ein
$1/r$-Potential und ein $1/r^2$-Feld, siehe
[Tong, Elektrodynamik, Abschnitte 2.1.1 und 2.2.3](https://www.damtp.cam.ac.uk/user/tong/em/em1.pdf).
Eine nichtkompakte Gaussantwort ist somit zwar mathematisch auch in
beliebiger Entfernung vorhanden, aber keine Coulomb-Fernantwort.
Der Vergleich betrifft den **geladenen Einzeltraeger**, nicht ein
neutrales Wasserstoffatom, dessen Monopolterm verschwindet.

Der vorhandene orientierte Readout
$B(x)=\sum_jw_jp_j e^{-|x-y_j|^2/(2\sigma_v^2)}$
erfuellt bei endlicher gewichteter Orientierungsnorm
$C=\sum_jw_j|p_j|$ entsprechend

$$
|PB(x)|\leq C\exp[-(r-R)^2/(2\sigma_v^2)].
$$

Die im Vektor-Simulator geschriebenen Orientierungen sind normiert oder
null. Dieser direkte Vektorkanal liefert deshalb ebenfalls nicht allein
den fehlenden algebraischen Schwanz und ist kein nachgewiesenes
elektromagnetisches Feld.

**Reichweite der Aussage:** Sie gilt fuer den festen direkten Readout
einer lokalisierten Quelle. Sie entscheidet weder ueber eine approximative
Coulomb-Skala auf einem endlichen Intervall noch ueber kollektive
Vermittlung, eine unbegrenzte Skalenverteilung oder eine andere effektive
Metrik. Ein solcher Zwischenbereich ist hier nicht getestet. Die
[archivierte Green-Mediator-Architektur](https://github.com/MemoryDynamics/Knoten/blob/88d56c84d9546df4cc5ab8afe79da8c270433cf8/reports/memory/closure/dynamic_green_kernel_selection_gate_2026-08-11.md)
ist ausdruecklich eine vorgeschlagene Zustandserweiterung, kein aus dem
nativen FIFO abgeleiteter oder hier neu freigegebener Ausweg.

## Innere Dimension: Beobachtung braucht eine Abschlussregel

Fuer eine testweise Koordinatenzerlegung $x=(X,\zeta)$,
$y=(Y,\upsilon)$ wirkt ein Gaussgradient nach aussen als

$$
P\nabla K(x-y)=-\sum_s\frac{a_s}{\sigma_s^2}
e^{-(|X-Y|^2+|\zeta-\upsilon|^2)/(2\sigma_s^2)}(X-Y).
$$

Gleiche aeussere Punkte und Historien liefern daher im Allgemeinen
verschiedene naechste aeussere Updates, wenn ihre verborgenen Abstaende
verschieden sind. Der synthetische 4D-Gegencheck veraendert nur die vierte
Koordinate aelterer Quellenpunkte; aktuelle Punkte, volle Memory-Center
und saemtliche ersten drei Historienkoordinaten bleiben gleich. Der
aeussere Kreuzdrift aendert sich trotzdem.

Damit ist diese reine 3D-Projektion auf dem ganzen zugelassenen
Zustandsraum **nicht autonom abgeschlossen**. Das verbietet weder einen
geeigneten reduzierten Zustandsraum noch statistische Mittelung oder
mitgefuehrte interne Variablen. Auch sagt es nichts gegen nichtgeometrische
innere Freiheitsgrade. Es macht vielmehr die fehlende Verbindung messbar:
Welche Information ueber $\zeta$ braucht dieselbe aeussere Vorhersage?

Ein Literaturwerkzeug hierfuer ist die Mori-Zwanzig-Projektion. Sie zeigt,
wie nichtaufgeloeste Variablen in Memory und einen von ihnen abhaengigen
Rest eingehen; sie liefert nicht automatisch eine billige oder Markovsche
Abschlussregel. Quellenvergleich:
[Gouasmi, Parish und Duraisamy (2017), Abschnitte 1 und 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC5627381/).
Diese Quelle behandelt kontinuierliche reduzierte Dynamik, nicht einen
bereits bewiesenen Abschluss unseres diskreten FIFO-Paars.

## Verifikation und Konsequenz

[`test_hydrogen_pair_contract.py`](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_hydrogen_pair_contract.py)
enthaelt 16 bestandene synthetische Checks: unabhaengige Ein-Schritt-Summe,
asymmetrische und spiegelgleiche Historien, Quellengewicht-Skalierung,
Kreuz-Depositionskonvention, Projektionsgegenbeispiel sowie skalare und
orientierte Fernschranken in 3D/4D/6D. Die Checks verwenden nur konstruierte
H=5-Zustaende, einzelne Updates oder statische Feldauswertungen. Sie
verifizieren Codezuordnung und Gegenbeispiele; die asymptotische Aussage
folgt aus der obigen Schranke, nicht aus endlich vielen Abstandspunkten.
Keine Stabilitaets-, Bindungs-, Spektral- oder Neutronensimulation.
Insgesamt bestehen 84 betroffene Software-/Dokumentationstests sowie
Lint und der strikte Dokumentationsbau; die Produktionsdynamik bleibt
unveraendert.

Die vorhandene direkte Kopplung ist damit **kein fertiges Atommodell**.
Der naechste gemeinsame Engpass ist die effektive Antwortbeschreibung:
beobachtbare Koordinaten, physikalischer Eingriff, Energie-/Impulsbilanz
und ein kontrollierter Memory-Rest. Die Arbeit daran darf nicht durch
Umbenennen von Quellenstaerke in Masse oder durch ungeprueft eingesetzte
Coulomb-/Quantenregeln ersetzt werden. Ein begrenzter analytischer
Reduktionsvergleich bleibt innerhalb der unveraenderten Regel. Die
[anschliessende Paarreduktion](memory_pair_reduction.md) liefert nun
die exakte Center-Gleichung mit FIFO-Rand und nichtlinearem Rest sowie
die bedingte Filtertraegheit und Modengrenze des lokalen kontinuierlichen
Vergleichs. Sie schliesst die Kraft-/Arbeits- und Massenluecke nicht. Ein
zusaetzlicher Mediator oder eine Quantenregel erfordert eine
Richtungsentscheidung. Die einzige Arbeitsreihenfolge steht in den
[Projektprioritaeten](../status/project_priorities.md).
