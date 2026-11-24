# Native Defektfortsetzung und die Grenze kleiner Zeitschritte

Stand: 2026-11-16. Analytischer Anschluss im Memory-/Paper-III-Zweig.
Keine neue Modellregel, Zielbahn, Parametersuche oder Aenderung an Paper I.

## Ergebnis und offene Huerde

Ein einzelner regulaerer Defekt kann nach einem **tatsaechlichen** FIFO-
Update durch ein endliches Kontraktionskriterium lokalisiert und sein
Index gesichert werden. Dies staerkt den bisherigen reinen Gesamtgrad-
Randschutz um Eindeutigkeit und eine Ortsfehlerschranke relativ zur
Memory-Wolke. Noch ist keine vorwaertsinvariante Klasse nativer Historien
gefunden, die dieses Kriterium bei jedem Schritt erfuellt.

Zwei vermeintliche Abkuerzungen sind getrennt auszuschliessen:

- Bei festem Depositionsgewicht ist die Einheitsrichtungs-Deposition
  am verschwindenden Bewegungsschritt unstetig. Kleine Gains garantieren
  deshalb keinen kleinen Eingriff in das Feld.
- Bei der unten **explizit definierten diffusiven Zeitverfeinerung**
  verschwindet die neu erzeugte Einheitsrichtungs-Memory im Mittelquadrat
  an jedem festen Ort. Die Aussage gilt auch mit adaptivem, gleichmaessig
  beschraenktem Drift. Eine vorgegebene Anfangshistorie muss separat
  abklingen oder ausgespuelt sein. Das ist kein allgemeines Defekt-No-go.

Die bisherigen [statischen Vorzeichenzeugen](nonminimal_memory_defects_2026-11-15.md)
bleiben gueltig; der [Ausschluss ihrer festen Achtfolge](nonminimal_kernel_obstruction_2026-11-16.md)
wird hier weder aufgeweicht noch durch einen neuen Fit umgangen.

## 1. Quellen-/Tail-Bilanz mit moeglicher Kompensation

Gefuellter Speicher, Dimension d, 0<q<1, Masse M>0, Breite ell>0:

$$
V(z)=\sum_{j=0}^{H-1}w_0q^jp_jG_\ell(z-y_j),\quad
w_0=(1-q)M,\quad |p_j|\leq1,\quad
G_\ell(r)=e^{-|r|^2/(2\ell^2)}.
$$

Mit dem nativen neuen Ort und seiner wirklichen Schritt-Richtung gilt
die bereits hergeleitete Identitaet

$$
V_+=qV+B,\qquad
B=w_0[p_+G_\ell(z-y_+)-q^Hp_tG_\ell(z-y_t)],
\quad (y_t,p_t)=(y_{H-1},p_{H-1}).
$$

Die globalen Gauss-Schranken sind L1=1/(ell sqrt(e)) fuer den Gradienten
und L2=1/ell^2 fuer die Hesse-Operatornorm. Schreibe
d_y=|y_+-y_t| und e_p=|p_+-q^Hp_t|. Durch Addition/Subtraktion von
q^H p_t G_ell(z-y_+) folgt

$$
\|B\|_\infty\leq w_0[e_p+q^H|p_t|L_1d_y],\qquad
\|DB\|_\infty\leq w_0[e_pL_1+q^H|p_t|L_2d_y].
$$

Diese hinreichenden Schranken behalten eine moegliche Kompensation
zwischen neuem Eintrag und entferntem Tail. Sie sind nicht notwendig.
Auch bei gleichen Orten und Richtungen bleibt bei q^H<1 ein Rest.
Eine angenommene periodische Kompensation muss die volle Bewegungsregel
erfuellen; eine geometrisch vorgegebene Folge reicht nicht.

## 2. Ein regulaerer Defekt nach dem wirklichen Update

Sei V(z_*)=0, J=DV(z_*), sigma_min(J)>=a>0. Waehle vor der
Nullstellenbestimmung einen Verschiebungspraediktor u, setze
z_c=z_*+u und A=qJ. Auf der abgeschlossenen Kugel mit Zentrum z_c
und Radius r>0 seien die folgenden Grenzen gesichert:

$$
|V_+(z_c)|\leq R,\quad \|DV_+(z_c)-A\|\leq E,\quad
\sup_{B_r(z_c)}\|D^2V_+\|\leq L_+.
$$

Dabei ist L_+=sum_j w_j|p_{+,j}|/ell^2 stets eine gueltige Wahl. Ein expliziter
Anschluss an Abschnitt 1 lautet E<=q L_old |u|+||DB||_infty, mit
L_old=sum_j w_j|p_j|/ell^2. Beim Residuum R koennen die tatsaechlichen
Vektorsummen benutzt werden; getrennte Betragsaddition ist oft zu grob.

**Hinreichender Satz.** Definiere

$$
\kappa=\frac{E+L_+r}{qa},\qquad b=\frac{R}{qa}.
\qquad \kappa<1,\quad b+\kappa r<r.
$$

Dann hat V_+ in dieser Kugel genau eine Nullstelle z_+. Sie ist
regulaer, hat denselben lokalen Index wie z_* und erfuellt

$$
|z_+-z_c|\leq\frac{b}{1-\kappa}<r.
$$

Beweis: T(z)=z-A^{-1}V_+(z) besitzt in der Kugel die Lipschitzkonstante
hoechstens kappa und |T(z_c)-z_c|<=b. Die strikte zweite Ungleichung
bildet die abgeschlossene Kugel in ihr Inneres ab. Banachs Satz liefert
Existenz, Eindeutigkeit und die Ortsgrenze. Fuer jedes z in der Kugel
ist ||A^{-1}(DV_+(z)-A)||<=kappa<1. Die geradlinige Jacobian-Homotopie
zu A bleibt invertierbar; det(A)=q^d det(J) erhaelt das Vorzeichen.
Der Satz braucht keine erfundene Zwischenzeit-Dynamik. Er behauptet
keine eindeutige physikalische Defektbahn zwischen diskreten Zustaenden.

### Kernbezug ohne nachtraeglich verschobenes Beobachtungsfenster

Der geometrische gewichtete Memory-Schwerpunkt ist
c=sum_j w_j y_j/W mit W=M(1-q^H). Fuer den gefuellten Speicher gilt exakt

$$
c_+=qc+\frac{w_0}{W}(y_+-q^Hy_t).
$$

Waehle u=c_+-c. Dann ist z_+-c_+=(z_*-c)+(z_+-z_c). Insbesondere
genuegt |z_*-c|+b/(1-kappa)<=R_core fuer die deklarierte Kernradiusgrenze
nach diesem Schritt. c ist **kein** hergeleiteter physikalischer
Massenschwerpunkt. Auch seine Bindung an den aktiven Ort ist separat
zu pruefen. Ein mit der gesuchten Nullstelle nachgefuehrtes Fenster
waere kein solcher unabhaengiger Kernbezug.

Die Ein-Schritt-Fehler koennen sich aufsummieren. Fuer dauerhafte Bindung
fehlen ein invarianter Historienbereich mit uniformen Reserven oder ein
nachgewiesener rueckstellender Mechanismus. Ein negativer Ortsjacobian
des eingefrorenen Feldes ist keine Stabilitaet des vollen FIFO-Zustands.
Ein fehlgeschlagenes hinreichendes Kriterium ist umgekehrt kein
Instabilitaetsbeweis.

## 3. Warum kleine Gains den diskreten Schritt nicht regularisieren

Fixiere eine gefuellte Historie und einen rauschfreien nativen Drift
f ungleich null. Multipliziere beide Bewegungs-Gains mit delta>0,
ohne Vergessen, M oder ell zu veraendern. Dann
y_+(delta)=x+delta f und p_+(delta)=f/|f|. Bei delta=0 setzt die
Implementierung `normalize_orientation(0)` dagegen auf null. In exakter
Arithmetik folgt

$$
\lim_{\delta\downarrow0}[V_{\delta,+}(z)-V_{0,+}(z)]
=w_0\frac{f}{|f|}G_\ell(z-x)\ne0
$$

an jedem endlichen z. Beide Updates entfernen denselben Tail.
Dies ist eine Unstetigkeit der vorhandenen Normierung, nicht eines
neu postulierten Feldes. Der fruehere positive Alignment-Verlustsatz
fuer H=4 gilt sogar bei beliebig kleinem positivem Gain.

Die [fruehere Grenzfallanalyse](fading_memory_limits_2026-11-04.md)
klaert bereits: q gegen 1 bei festem H laesst die rohe Speichermasse
verschwinden. Nach Division durch w0 bleibt dagegen im Allgemeinen ein
endlicher Quellen-/Tail-Austausch. Die Indexgeometrie wird durch blosses
Verkleinern der positiven Gesamtamplitude nicht langsamer.

## 4. Diffusive Zeitverfeinerung: ein eigener, bedingter Satz

Dies ist eine untersuchte Skalierung, **keine Entscheidung**, dass der
native diskrete Schritt nur ein numerisches Zeitgitter ist. Vorausgesetzt:

$$
x_k=x_{k-1}+h b_{k-1}+\sigma_B\sqrt h\,\xi_k,\quad
|b_{k-1}|\leq B,\quad \sigma_B>0,
\qquad q_h=e^{-\gamma h},\quad \gamma>0.
$$

Die xi_k sind unabhaengige N(0,I_d)-Innovationen. Der Drift ist
F_{k-1}-messbar und gleichmaessig in h beschraenkt. M, ell, gamma,
sigma_B und B bleiben fest. Gespeichert wird p_k=(x_k-x_{k-1})/
|x_k-x_{k-1}|, nicht das unnormierte Inkrement. Zum Zeitpunkt n>=H
besteht der gesamte Speicher aus so erzeugten Schritten:

$$
V_h(z)=\sum_{j=0}^{H-1}M(1-q_h)q_h^j X_{n-j}(z),\quad
X_k(z)=p_kG_\ell(z-x_k).
$$

H darf von h abhaengen. Es wird weder eine unabhaengige Historie noch
Stationaritaet vorausgesetzt. Das Abfrage-z ist zunaechst deterministisch.

### Bedingter Mittelwert: Richtung und Depositionsort sind korreliert

Fuer m(a)=E[(xi+a)/|xi+a|] gilt m(0)=0 und |m(a)|<=|a|. Beweis:
Differentiation der verschobenen Gaussdichte statt der singulaeren
Normierungsfunktion ergibt fuer jeden Richtungsvektor v
|Dm(a)v|<=E|v dot xi|<=|v|. Integration entlang a liefert die Grenze.
Damit |E[p_k|F_{k-1}]|<=B sqrt(h)/sigma_B.

Zerlege X_k in p_k G_ell(z-x_{k-1}) und den Ortsverschiebungsrest.
Aus |G|<=1, der Lipschitzgrenze L1 und E|xi|<=sqrt(d) folgt

$$
|\mu_k(z)|:=|E[X_k(z)\mid\mathcal F_{k-1}]|
\leq a_h:=\frac{B\sqrt h}{\sigma_B}
+L_1(\sigma_B\sqrt{dh}+Bh).
$$

Schon bei b=0 ist mu_k(z) im Allgemeinen **nicht null**. Der neue Ort
enthaelt dieselbe Innovation wie die Richtung. Diese Korrelation darf
nicht durch eine scheinbare isotrope Mittelung entfernt werden.

### Martingalabschaetzung ohne Unabhaengigkeit der Speicherbeitraege

D_k=X_k-mu_k sind Martingaldifferenzen. E|D_k|^2<=1, und verschiedene
D_k sind im L2-Skalarprodukt orthogonal. Die Gewichte sind deterministisch.
Minkowski und die geometrische Reihe ergeben

$$
\|V_h(z)\|_{L^2}
\leq M\left[
\frac{B\sqrt h}{\sigma_B}
+L_1(\sigma_B\sqrt{dh}+Bh)
+\sqrt{\frac{1-q_h}{1+q_h}}
\right]=O(\sqrt h).
$$

Dies gilt gleichmaessig in H und n>=H. Fuer DV_h in Frobeniusnorm gilt
derselbe Beweis mit |X_k|<=L1 und Lipschitzgrenze L2 fuer grad G:

$$
\|DV_h(z)\|_{L^2(F)}\leq M\left[
L_1\frac{B\sqrt h}{\sigma_B}
+L_2(\sigma_B\sqrt{dh}+Bh)
+L_1\sqrt{\frac{1-q_h}{1+q_h}}
\right].
$$

Der nativen Alignment-Regel entspricht hier eta_scalar=h kappa_s,
eta_vector=h kappa_v und epsilon=sigma_B sqrt(h). Bei festen endlichen
Kopplungen, Massen und positiven Kernelbreiten ist ihr Drift durch die
globalen Gaussgradient- und Vektoramplitudengrenzen beschraenkt. Das
waehlt keine solchen Parameter fuer einen neuen Lauf.

### Anfangshistorie und bewegte Abfrage nicht unterschlagen

Vor dem Ausspuelen kann ein beliebiger anfaenglicher Vektorspeicher
einen Zusatz von Betrag bis M q_h^n tragen. Bei nh=t bleibt das bis
M exp(-gamma t), also im Allgemeinen **nicht null** bei h gegen null.
Der Satz gilt fuer den erzeugten Anteil; fuer den ganzen Speicher erst
nach Ausspuelen oder gesonderter Kontrolle dieses Anfangsterms.

Aus punktweisem L2-Verschwinden allein folgt kein Satz an einem
adaptiven Ort wie x_n. Hier gibt es jedoch einen Zusatz: Die Felder
haben deterministische globale Lipschitzkonstanten <=M L1, ihre
Jacobians <=M L2. Auf jedem festen Kompaktum K liefert ein endliches
delta-Netz

$$
\sup_K|V_h|\leq\max_{z_i\text{ im Netz}}|V_h(z_i)|+ML_1\delta.
$$

Erst h gegen null bei festem Netz, dann delta gegen null zeigt uniformes
Verschwinden in Wahrscheinlichkeit auf K; analog fuer DV_h. An einer
**straffen** Familie von Abfrageorten folgt somit ebenfalls Verschwinden
in Wahrscheinlichkeit, ohne Unabhaengigkeit vom Feld. Beschraenkter
Drift und straffe Anfangsorte liefern diese Straffheit an beschraenkten
physikalischen Zeiten. Keine Aussage uniform ueber beliebig lange Zeiten.

### Was das bedeutet und was nicht

Bei dieser Skalierung bleibt nach vollstaendigem Ausspuelen oder bei
separat verschwindendem Anfangsterm kein endlicher Alignment-Beitrag mit
fester physikalischer Kopplung an straffen Orten uebrig. Es ist damit
kein automatisch nichttrivialer glatter
Ladungstraeger-Grenzfall. Das beweist **nicht**, dass endliche-h-Felder
keine Nullstellen oder Indizes besitzen: Multiplikation mit einer
positiven kleinen Zahl bewahrt Indizes, waehrend ihre absolute
Jacobian-Reserve schrumpft. Auch die Verhaeltnisse im lokalen Satz
aus Abschnitt 2 koennen nicht allein daraus beurteilt werden.

Nicht erfasst: feste mikroskopische Schritte, rauschfreie Bahnen,
anders skalierendes/korreliertes Rauschen, divergierende Kopplungen,
schrumpfende Kernelbreiten oder eine normierte Fluktuationsgrenze.
Das Ersetzen der Deposition oder eine Gegenreskalierung von M/Gain
waeren neue, gesondert zu begruendende Entscheidungen, kein Ergebnis.

## 5. Enger Literaturabgleich

Primaerquelle: V. Skogvoll, J. Ronning, M. Salvalaglio, L. Angheluta,
*A unified field theory of topological defects and non-linear local
excitations*, npj Computational Materials **9**, 122 (2023),
[DOI](https://doi.org/10.1038/s41524-023-01077-6),
[arXiv v2, 29.06.2023](https://arxiv.org/html/2302.03035v2).
Verlagsdatum 13.07.2023. Geprueft am 16.11.2026; enge Titelsuche nach
Korrektur/Erratum lieferte keinen Treffer, keine umfassende Negativgarantie.

| Gelesen | Aussage der Quelle | Grenze des Transfers |
|---|---|---|
| Abschnitte I.1, II.1, Gl. 4-9 | Nichtsingulaere Defektdichte aus einem Ordnungsparameter; Gleichheit mit topologischer Ladung unter passenden Randamplituden | Native Gauss-Memory hat keinen daraus folgenden festen Amplitudenrand. |
| Gl. 10-15 | Geschwindigkeit aus Feldableitungen auf regulaeren Bereichen; kinematische Stromfreiheit und Zusatzbedingungen bei Linien | Der aktuelle FIFO-Push und seine Stabilitaet werden dadurch nicht bestimmt. |
| Beginn II.2, Gl. 16 | BEC-Anwendung mit festgelegter Gross-Pitaevskii-Dynamik | Keine Herleitung dieser Dynamik aus Memory. |

Die Arbeit unterstuetzt die Trennung zwischen Defektkinematik und
modellabhaengiger Erzeugung/Stabilitaet. Ihr Titel bezeichnet keine
Vereinheitlichung von Quantenmechanik und Gravitation. Kein Import von
Wirkung, Vakuumzwang oder Feldgleichung. Supplement und Simulationen
wurden nicht reproduziert. Die Saetze in Abschnitten 2-4 sind hier
hergeleitete Aussagen, keine Resultate dieser Literaturquelle.

## 6. Verifikation und Konsequenz

27 feste Softwarekontrollen in `tests/test_memory_defect_transport.py`:
native Quellen-/Tail-Identitaet samt kompensationssensitiven Schranken,
Memory-Schwerpunkt, Klein-Gain-Unstetigkeit, synthetische lokale
Kontraktionsfaelle und Gegenfaelle, exakte Filtermomente, Anfangstail
sowie eindimensionale Gaussintegrale mit korreliertem Depositionsort.
Kein Nullstellensucher, stochastischer Ziellauf oder Parameteroptimierer.
Numerische Kontrollen ersetzen weder die obigen analytischen Beweise
noch einen unabhaengigen mathematischen Review.

Verifikation: 27 neue Kontrollen und 250 Tests im betroffenen Panel
bestanden, ebenso Ruff fuer den konfigurierten Code-/Testbereich und
strikter MkDocs-Bau. Keine vollstaendige Repository-Testsuite. Das Panel
umfasst Defekttransport, die vier vorherigen Defekt-/Rekurrenzberichte,
den Zwei-Gauss-Ausschluss, Vektormemory samt Normalantwort, topologischen
Zustandsvertrag, Memory-Strom, kollektive Ladungsbedingungen,
Kernphasenanschluss, Zustand und Markdown-Mathematik.

Die konkrete offene Aufgabe ist jetzt die **Selbstregeneration der
Reserven**: richtungsumfassende Historien, regulaerer Defekt, Kernbindung
und volle History-Stabilitaet muessen gemeinsam erhalten werden.
Ein einmaliges Kontraktionszertifikat oder kleinere Schrittweite allein
schliesst das nicht. Elektrische Quellenwirkung und Ladungsnormierung
bleiben danach eigenstaendige Nachweise.
Rauschfreie Invarianz und kontrollierte endliche Lebensdauer bei Rauschen
sind dabei verschiedene Ziele; die frueheren Volltraeger-No-gos fuer
exakte globale Invarianten werden hier nicht aufgehoben.
