# Memory-Nullstellen als Ladungskandidat: Existenz und FIFO-Verlust

Stand: 2026-11-14. Analytische Konstruktion und kleine Ein-Schritt-
Kontrollen der vorhandenen Vektormemory. Keine Zieltrajektorie, neue
Simulationsregel, Parametersuche oder elektrische Ladungsidentifikation.

## Ergebnis

**Ein lokaler ganzzahliger Index kann direkt aus dem vorhandenen
Memory-Feld entstehen. Seine Erhaltung folgt daraus aber nicht.**
Eine geschlossene Simplex-Historie besitzt mit nativen positiven
Vergessensgewichten genau eine regulaere Feldnullstelle mit Index +1.
Das gilt auch fuer die im aktiven Simulator verwendeten Einheitsrichtungen.
Es wird weder ein zusaetzliches Materiefeld noch eine feste Feldnorm
eingefuehrt. In 3D genuegen vier Depositionsorte und ihr historischer
Vorgaenger zum Schliessen der Bahn; das sind nicht vier Teilchen.

Die Gegenprobe ist ebenso konkret: Bei einer regulaeren Vierpunkt-
Historie beseitigt ein aktiver Alignment-Schritt mit positivem Gain,
ohne skalaren Drift und Rauschen, **alle** endlichen Feldnullstellen.
Der alte Tail traegt die einzige Richtung ausserhalb eines geeigneten
Halbraums im Richtungsraum. Nach seinem Verlust liegen alle Beitraege
in einer offenen Halbraumklasse; positive Gaussgewichte koennen sich
dann nirgends aufheben. Dies gilt fuer jedes 0 < q < 1, jede endliche
positive Gaussbreite und jeden positiven Alignment-Gain in dieser Klasse.

Der vorhandene skalare Kernel kann dem Verlust entgegenwirken: Eine
explizite Schwelle liefert wieder einen +1-Defekt nach einem Schritt.
Die feste positive Kontrolle verlagert ihn allerdings weit ausserhalb
der Memory-Wolke. Auch ein gleichbleibender Index beweist keine Kernbindung.

Damit liegt ein aus Memory definierter **Defektkandidat**, aber noch
kein dynamisch geschuetzter Ladungstraeger vor. Der Gegenbefund ist
kein allgemeines No-go fuer andere Historien, kollektive Sektoren oder
kontrollierte endliche Lebensdauern. Paper I bleibt unveraendert.

## 1. Zustandsvertrag und Anschluss an Literatur

Verwendet wird ausschliesslich das bestehende Readout
`oriented_history_from_state` / `vector_gaussian_field`. Bei H gerichteten
Depositionen braucht die bahnkonsistente Rekonstruktion H+1 Positionen:

$$
u_j=y_j-y_{j+1},\qquad p_j=u_j/s_j,\qquad
V(z)=\sum_{j=0}^{H-1}w_j p_j G_\sigma(z-y_j),
$$

$$
G_\sigma(r)=e^{-|r|^2/(2\sigma^2)},\qquad
w_j=w_0q^j,\quad w_0=M(1-q)>0,\quad 0<q<1.
$$

Fuer den Displacement-Readout ist s_j=1; fuer den aktiven
Einheitsrichtungs-Kanal ist s_j=|u_j|. In der Konstruktion sind alle
Schritte ungleich null. M ist die native Memory-Massennormierung, keine
Teilchenmasse. Die Richtungen werden nicht unabhaengig von den Orten
gewaehlt. Die Historie ist ein zulaessiger gefuellter Zustand, kein
nachgewiesener Attraktor oder aus leerem Speicher erzeugter Orbit.

Fuer V: R^3 -> R^3 und eine isolierte regulaere Nullstelle z_a lautet
der lokale Brouwer-Index

$$
Q_a=\operatorname{sgn}\det D_zV(z_a)\in\{-1,+1\}.
$$

Auf einer kleinen nullstellenfreien Randkugel ist dies der Grad von
V/|V|: S^2 -> S^2. Nur am Rand wird normiert; V selbst bleibt ein
nicht normiertes, nullstellenfaehiges Memory-Readout. Das ist weder
eine Hopf-Invariante S^3 -> S^2 noch die raeumliche Verknuepfung einer
FIFO-Bahn. Bei mehreren regulaeren Nullstellen in einem begrenzten
Gebiet addieren sich die Indizes, solange der Rand nullstellenfrei ist.

| Quelle und gepruefter Umfang | Verwendbarer Anschluss | Nicht daraus uebernommen |
| --- | --- | --- |
| Mazenko und Wickham, *Ordering kinetics of defect structures*, PRE 57, 2539-2542 (1998); Autorenpreprint von 1997, S. 1-2, Gl. (1)-(10) | Defekte als Feldnullstellen; signierte Dichte aus Deltafunktion und Jacobian; kinematischer Strom bei glatter Zeitentwicklung | TDGL-Energie, gebrochene Symmetrie und statistischer Gaussabschluss sind dort Inputs, keine Memory-Herleitung. |
| Hatcher, *Algebraic Topology* (2002), Abschnitt 2.2, Grad und lokale Gradsumme, Proposition 2.30 | Ganzzahligkeit, Homotopieinvarianz und Addition lokaler Grade | Keine native Randkontrolle, Stabilitaet oder elektromagnetische Wirkung. |

[Mazenko/Wickham: Primaerpreprint](https://arxiv.org/pdf/cond-mat/9704250v1),
[APS-Publikationsnachweis](https://doi.org/10.1103/PhysRevE.57.2539),
[Hatcher: Autorenfassung](https://pi.math.cornell.edu/~hatcher/AT/AT..pdf).
Die folgenden Simplex-/FIFO-Rechnungen sind eigene Ableitungen fuer
das vorhandene Readout, keine reproduzierten Resultate dieser Quellen.

## 2. Exakter Existenzsatz mit positivem Vergessen

Seien y_0,...,y_d affin unabhaengige Punkte in R^d und y_{d+1}=y_0.
Wir verwenden H=d+1 Depositionen, in der Reihenfolge dieses geschlossenen
Polygons. Die d+1 Spalten u_j spannen R^d auf und ihre einzige lineare
Relation ist die Summe null. Daher gilt

$$
V(z_*)=0\quad\Longleftrightarrow\quad
\frac{w_jG_\sigma(z_*-y_j)}{s_j}=c>0
\quad\hbox{fuer alle }j.
$$

Logarithmieren und Subtraktion der Gleichung fuer j=0 ergeben das
nichtsingulaere lineare System

$$
(y_j-y_0)\cdot z_*=
\frac{|y_j|^2-|y_0|^2}{2}
-\sigma^2\log\frac{w_j/s_j}{w_0/s_0},
\qquad j=1,\ldots,d.
$$

Es besitzt genau eine Loesung. Also existiert genau eine endliche
Nullstelle, fuer alle angegebenen positiven Gewichte und Breiten,
ohne Nullstellensuche oder Anpassung an einen Teilchenwert. Sie muss
nicht innerhalb der konvexen Huelle der Depositionsorte liegen.

Am Nullpunkt gilt mit A=sum_j u_j y_j^T:

$$
D_zV(z_*)=\frac{c}{\sigma^2}A,\qquad
\frac{A+A^{\mathsf T}}{2}
=\frac12\sum_{j=0}^{d}u_ju_j^{\mathsf T}>0.
$$

Die zweite Identitaet folgt durch Ausschreiben und Teleskopieren der
geschlossenen Folge. Die strikte Positivitaet folgt aus dem vollen
Rang der Schritte. Die Homotopie von A zu seinem symmetrischen Anteil
haelt diesen positiv definit und ist daher stets nichtsingulaer.
Folglich det A > 0 und **Q=+1**. Der Satz ueber implizite Funktionen
garantiert die Fortsetzung dieses einfachen Nullpunkts unter hinreichend
kleinen Historienstoerungen, auch solchen, die den exakten Ringschluss
aufheben. Das ist lokale strukturelle Robustheit, keine zeitliche Stabilitaet.

Wichtige Grenzen:

- Die gesamte Simplex-Klasse hat Index +1. Umkehren der Historienfolge
  erzeugt hier keine Gegenladung; eine gemeinsame Raumspiegelung von
  Orten und Richtungen ebenfalls nicht. Ein natives Paar mit beiden
  Indexvorzeichen ist damit noch nicht konstruiert.
- In d Dimensionen gilt derselbe Satz mit d+1 Depositionsorten. Es
  zeichnet 3D nicht aus. Ein 3D-Beispiel nur in einen groesseren Raum
  einzubetten erzeugt keine isolierte hoeherdimensionale Nullstelle:
  das Feld hat weiterhin nur drei unabhaengige Komponenten.
- Ein affines Simplex-Polygon ist kein Nachweis eines nichttrivialen
  raeumlichen Knotens, eines Spinwerts oder eines Quarkzustands.
- q=0 und q=1 gehoeren nicht zum Satz. Im nativen Grenzgang q -> 1
  bei festem M verschwindet auch w_0. Eine endliche Richtungsabbildung
  allein sichert keine endliche Feldamplitude oder Stoerungsreserve.

## 3. Nativer Gegenbeweis gegen automatische Defekterhaltung

Waehle in 3D eine regulaere Tetraeder-Eckenfolge mit y_4=y_0,
H=4, p_j=u_j/ell und gemeinsamer Kantenlaenge ell. Dies bezeichnet
vier aufeinanderfolgende Speicherorte einer Bahn, keinen Drei-Quark-
oder Vier-Teilchen-Ansatz. Fuer die drei unabhaengigen Schritte existiert
ein Vektor h mit

$$
h\cdot u_0=h\cdot u_1=h\cdot u_2=1,\qquad h\cdot u_3=-3.
$$

Am aktuellen Ort y_0 ist der Selbst-Gaussfaktor 1, fuer die drei
anderen Orte jeweils g=exp[-ell^2/(2 sigma^2)] in (0,1). Daher

$$
h\cdot V(y_0)=\frac{w_0}{\ell}
\left[1+g(q+q^2-3q^3)\right]
=\frac{w_0}{\ell}\left[(1-g)+g(1-q)(3q^2+2q+1)\right]>0.
$$

Nun genau ein Schritt der vorhandenen Alignment-Regel mit epsilon=0,
eta_scalar=0 und eta_vector>0:

$$
y_+=y_0+\eta_v V(y_0),\qquad
p_+=\frac{y_+-y_0}{|y_+-y_0|}.
$$

Der Schritt ist nicht null und h dot p_+ > 0. Nach dem nativen Push
bleiben die vier Richtungen p_+,p_0,p_1,p_2. Fuer jede davon ist das
Skalarprodukt mit h strikt positiv. Mit positiven Gewichten und
Gaussfaktoren folgt daher

$$
h\cdot V_+(z)>0\quad\hbox{fuer jedes endliche }z.
$$

Vorher gab es genau eine regulaere +1-Nullstelle, danach keine.
Kein dichtes Gitter und keine fehlgeschlagene Nullstellensuche werden
als Abwesenheitsbeweis benutzt: das Halbraumargument gilt global.
Die Skalargain-Nullwahl isoliert einen erlaubten aktiven Modellfall;
sie ist kein passives Weglassen aller Rueckwirkung. Fuer einen
zusaetzlichen Inkrementbeitrag r bleibt der Beweis bestehen, sofern
h dot r > -eta_v h dot V(y_0). Damit besitzt er auch eine offene
Inkrementreserve, ist aber kein Satz fuer beliebig starke skalare
Kopplung oder alle Rauschrealisierungen.

Unter reinem positivem Alignment ist ein solcher gemeinsamer offener
Richtungshalbraum zudem vorwaertsinvariant: Positive gewichtete Summen
der alten Richtungen, ihre Normierung und das Loeschen eines Eintrags
verlassen ihn nicht. Ohne skalaren Drift oder Rauschen koennen dort
spaeter keine Feldnullstellen zurueckkehren. Das schliesst einen
dauerhaft andersartigen, nie in diesen Halbraum eintretenden Sektor
nicht aus.

Es widerspricht keinem topologischen Erhaltungssatz: Die vorhandene
Dynamik fixiert keinen nullstellenfreien Feldrand waehrend des Updates.
Fuer jede feste Kugel um den alten Nullpunkt muss eine stetige Verbindung
der beiden Felder mindestens einmal eine Nullstelle auf dieser Kugel
haben. Aus den beiden diskreten Zustaenden folgt keine eindeutige
physikalische Bahn dieses Randdurchgangs. Insbesondere ist die Summe
der endlichen Indizes ohne Kontrolle am Unendlichen nicht geschuetzt.

## 4. Zwei konkrete Pruefkriterien statt neuer Feldpostulate

### Richtungsbedingung

Da alle Gausskoeffizienten positiv sind, ist eine Nullstelle nur moeglich,
wenn 0 in der konvexen Huelle der gespeicherten Richtungen liegt. Fuer
eine regulaere d-dimensionale Nullstelle muss 0 sogar im Inneren dieser
Huelle in R^d liegen. Beweis: Laege 0 auf deren Rand, gaebe es einen
Stuetzvektor h mit h dot p_j >= 0. Die positive Nullsumme erzwingt
h dot p_j=0 fuer alle j; dann hat auch D V keinen vollen Rang.

Das liefert ein notwendiges diskretes Kriterium **an jedem gefuellten
FIFO-Fenster**. Es ist kein hinreichender Existenz- oder Stabilitaetstest:
die raeumlichen Gaussfaktoren koennen nicht beliebig frei gewaehlt werden.
Insbesondere braucht eine regulaere Nullstelle mindestens d+1 aktive
Depositionen. Drei gespeicherte Richtungen allein liefern in 3D noch
keinen solchen Punktdefekt. Drei zusammengesetzte Knoten mit jeweils
eigener Historie sind eine andere, hier nicht behandelte Situation.

### Vorhandener skalarer Kanal: eine konkrete Gegenkontrolle

Der Verlustsatz rechtfertigt nicht, sofort ein neues Feld einzufuehren.
Fuer dieselbe regulaere Historie laesst sich der vorhandene skalare
Kernel einbeziehen. Sei sein Horizont 4, seien v_j>0 seine Gewichte und
a(ell) der radiale Koeffizient in grad K(r)=a(|r|)r. Fuer Delta-Deposition
im vorhandenen Doppelgauss-Kernel ist

$$
a(\ell)=\frac{A_{\rm att}}{\sigma_{\rm att}^2}
e^{-\ell^2/(2\sigma_{\rm att}^2)}
-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
e^{-\ell^2/(2\sigma_{\rm rep}^2)}.
$$

In der Basis (u_0,u_1,u_2) lauten die Alignment-Koeffizienten

$$
b=\frac{w_0}{\ell}
\bigl(1-gq^3,\ g(q-q^3),\ g(q^2-q^3)\bigr)>0,
\qquad t=(v_1+v_2+v_3,\ v_2+v_3,\ v_3)>0.
$$

Der volle rauschfreie Schritt hat also die Basis-Koeffizienten
d_j=eta_v b_j - eta_s a(ell)t_j. Nach dem Push umfasst die konvexe
Huelle der vier Richtungen genau dann den Ursprung strikt, wenn alle
d_j<0 sind. Denn eine positive Relation zwischen dem neuen Schritt
sum_j d_j u_j und den drei erhaltenen Basisrichtungen existiert genau
unter dieser Bedingung. Fuer positive Gains und a(ell)>0 lautet sie

$$
\eta_s>\max_{j=0,1,2}\frac{\eta_v b_j}{a(\ell)t_j}.
$$

Bei a(ell)<=0 kann dieser skalare Kanal die Bedingung mit eta_s>=0
nicht erfuellen. Das ist eine konkrete lokale Bedingung an die
vorhandene Rueckwirkung, keine willkuerliche neue Ladungskopplung.

In dieser speziellen Vierpunkt-Klasse folgt bei d_j<0 sogar wieder
genau eine regulaere +1-Nullstelle nach dem Schritt. Die neuen Orte
(y_+,y_0,y_1,y_2) sind affin unabhaengig, da d_2 ungleich null ist.
Die neuen unnormierten Schritte haben die positive Nullrelation
r=(1,-d_0,-d_1,-d_2). Mit s_i als neuen Schrittlaengen lautet die
Nullstellenbedingung w_i G_i/s_i=c r_i. Wieder entsteht ein eindeutiges
lineares System durch Logarithmieren der Verhaeltnisse. Fuer den
Jacobian ergibt sich, mit U=(u_0,u_1,u_2),

$$
\det D V_+(z_+)=
\left(\frac{c}{\sigma^2}\right)^3
(\det U)^2 d_0d_1d_2^2>0.
$$

Zur Kontrolle: Nach Translation y_0=0 ist die innere Jacobian-Matrix
dd^T+d_1 e_1 e_0^T+d_2 e_2(e_0+e_1)^T, mit Basisindizes 0,1,2.
Ihr Determinant ist d_0 d_1 d_2^2. Dies ist ein positiver
Ein-Schritt-Existenzbefund, **kein** Mehrschritt-Schutz: Die neue
Geometrie ist im Allgemeinen kein regulaeres Tetraeder, der Defektort
kann weit wandern, und die Schwelle darf nicht unveraendert iteriert
oder als Stabilitaets-/Teilchenfit benutzt werden.

Die fest konstruierte positive Rechenkontrolle macht diese Grenze
besonders sichtbar: Alle neuen Speicherorte liegen innerhalb von
Radius 1 um den Koordinatenursprung, die eindeutige Nullstelle dagegen
ausserhalb von Radius 25. Ihr unskalierter Jacobian-Determinant faellt
unter die binary64-Darstellungsgrenze; sein Vorzeichen wird mit
`slogdet` und der skalierten analytischen Determinante kontrolliert.
Die Feldaufhebung wird relativ zur Summe der Gaussbeitraege geprueft,
nicht mit einer bedeutungslosen absoluten Nulltoleranz. Keine Gains
werden anschliessend nachjustiert. Ein fortbestehender Index ist
offensichtlich noch kein ortsgebundener Kern oder passender Ladungstraeger.

### Exakte Updatebilanz und hinreichender Randschutz

Fuer jedes gefuellte FIFO mit positiver geometrischer Gewichtung gilt
unter dem tatsaechlichen Push, mit dem jeweils tatsaechlichen neuen
Schritt bzw. seiner Einheitsrichtung:

$$
V_+(z)=qV(z)+B(z),\qquad
B(z)=w_0p_+G_\sigma(z-y_+)
-w_0q^Hp_{H-1}G_\sigma(z-y_{H-1}).
$$

Sei D eine begrenzte Kugel mit m=inf_boundaryD |V| > 0. Dann ist

$$
\sup_{z\in\partial D}|B(z)|<qm
$$

hinreichend fuer gleichen Gesamtindex vor und nach diesem Schritt.
Denn W_s=qV+sB, 0 <= s <= 1, bleibt am gesamten Rand nullstellenfrei.
Die Bedingung ist nicht notwendig; ihr Scheitern beweist keinen Verlust.
Sie sichert den Gesamtindex, nicht Anzahl, Position oder Lebensdauer
jedes einzelnen Defekts. Wiederholter Schutz benoetigt die Schranke
bei jedem Schritt, nicht bloss am Anfang.

Es werden euklidische Vektornormen und zugehoerige Operatornormen benutzt.
Fuer eine regulaere Nullstelle mit kleinstem Singulaerwert mindestens
a>0 besitzt die Gaussform eine explizite lokale Reserve. Wegen
norm(D^2 G_sigma) <= 1/sigma^2 gilt mit

$$
L=\frac{\sum_jw_j|p_j|}{\sigma^2},\qquad
0<r<\frac{2a}{L},\qquad
\inf_{|z-z_*|=r}|V(z)|\geq ar-\frac12Lr^2>0.
$$

Dies ist Taylor mit globaler Hessianschranke, keine Randabtastung.
An der Simplex-Nullstelle kann a durch den kleinsten Eigenwert des
positiv definiten symmetrischen Jacobian-Anteils nach unten abgeschaetzt
werden. Fuer eine einzelne Deposition am Ort y ist auf dieser Kugel
G_sigma(z-y) <= exp[-max(|y-z_*|-r,0)^2/(2 sigma^2)]. Damit existiert
auch eine explizite obere Schranke fuer B durch Addition der zwei
Betragsbeitraege. Eine binary64-Auswertung ist noch kein validiertes
Intervallzertifikat. Hier wird kein nativer Mehrschritt-Schutz behauptet.

## 5. Was ein Defektstrom leisten wuerde und was nicht

Bei einer festgelegten glatten Interpolation W(t,z) mit regulaeren
isolierten Nullstellen liefert Differenzieren von W(t,z_a(t))=0

$$
\dot z_a=-(D_zW)^{-1}\partial_tW,\qquad
\rho_{\rm top}=\sum_aQ_a\delta^{(3)}(z-z_a)
=\delta^{(3)}(W)\det D_zW,
$$

$$
J_{\rm top}=\sum_aQ_a\dot z_a\delta^{(3)}(z-z_a),\qquad
\partial_t\rho_{\rm top}+\nabla\cdot J_{\rm top}=0.
$$

Die letzte Identitaet gilt auf regulaeren Defektzweigen; bei generischen
Paarereignissen bleibt der signierte Gesamtindex ohne Randdurchgang
gleich. Die inverse Jacobian-Formel darf am singulaeren Ereignis nicht
verwendet werden. Auch die Delta-Darstellung erfordert dort gesonderte
Behandlung. Fuer das diskrete FIFO ist die Wahl der Interpolation
zunaechst ein Diagnosevertrag, keine hergeleitete Zwischenzeit-Dynamik.

Diese kinematische Bilanz liefert noch keine elektrische Stromquelle,
keine mechanische Energie, keinen Coulomb-Koeffizienten und keine
Quantendynamik. Das rohe V ist am Defekt glatt und dort null; sein
Fluss durch eine schrumpfende Kugel verschwindet, statt einen endlichen
elektrischen Quellwert zu liefern. Das nachtraegliche Definieren eines
Maxwell-Felds mit rho_top als Quelle waere eine neue Kopplung. Auch
die Skalierung einer geometrischen Ganzzahl auf die Elementarladung
ist nicht durch den Index festgelegt.

## 6. Entscheidung und Verifikation

Der Schritt schliesst eine echte Luecke im bisherigen
[Zustandsraumabgleich](topological_state_contract_2026-11-04.md):
Nullstellen sind nicht nur Hindernisse fuer eine globale Normierung,
sondern koennen selbst lokale ganzzahlige Defekte tragen. Anders als
die nicht erhaltene [Modenintensitaet](memory_core_phase_bridge_2026-11-11.md#6-dynamischer-anschluss-normalantwort-und-ladung)
ist dieser Kandidat diskret und gegen hinreichend kleine lokale
Stoerungen geschuetzt. Das ist ein positiver Existenzbefund, kein
elektrischer oder dynamischer Schutzbefund.

Der gleichzeitig bewiesene Ein-Schritt-Verlust verhindert, dass aus
dieser Konstruktion bereits ein Elektronenbenchmark gemacht wird.
Die offene Frage ist eine **unter der vorhandenen Dynamik regenerierte
Richtungsumfassung und ein kontrollierter Randfluss**, nicht die
nachtraegliche Fixierung der Feldnorm. Ein bloss geschlossenes Polygon,
mehr Dimensionen oder positive Modenintensitaet leisten das nicht.
Die skalare Gegenkontrolle zeigt bereits einen vorhandenen Mechanismus,
der den Ein-Schritt-Verlust verhindern kann; seine geschlossene
Mehrschritt-Kontrolle ist noch offen. Keine neue Kopplung wurde gewaehlt.
Die aktive Arbeitsreihenfolge bleibt ausschliesslich in den
[Projektprioritaeten](../../docs/status/project_priorities.md).

Die [kleinen Kontrollen](../../tests/test_memory_defect_charge.py)
verwenden die vorhandenen Feld-, Orientierungs- und Push-Funktionen.
Geprueft werden die exakte Nullstellenformel in 2D/3D/5D, beide
Readout-Konventionen, die Jacobian-Identitaet samt Differenzenquotienten,
Umkehrung/Spiegelung, der aktive Halbraum-Gegenbeweis, die volle
Quellen-/Tailbilanz, Dimensions-Einbettung und die analytische Randreserve.
Zwei fest konstruierte Seiten der abgeleiteten Skalar-Schwelle pruefen
Verlust bzw. erneute +1-Nullstelle, ohne Gain-Suche oder Nachanpassung.
Kein numerischer Parameterscan, keine lange Zeitintegration und kein
Literaturmodell werden damit reproduziert. Testfaelle pruefen
Implementierungsanschluss und Algebra, ersetzen aber nicht die Beweise.
Die Saetze gelten in reeller Arithmetik; Gauss-Unterlauf und sonstige
Gleitkommaeffekte sind damit nicht als Simulationsartefakte ausgeschlossen.

Verifikation am 2026-11-14: **29 neue konstruierte Kontrollen und 130
Tests im betroffenen Panel bestanden**. Das Panel umfasst Defekt-,
Vektormemory-/Normalantwort-, topologische Zustands-, Memory-Strom-,
kollektive Ladungs-, Kernphasen-, Zustands- und Markdown-Mathematiktests.
Ruff, strikter MkDocs-Bau und Whitespacepruefung bestanden. Keine
vollstaendige Repository-Testsuite, kein Intervallzertifikat und keine
unabhaengige Begutachtung der eigenen Beweise.

Quellenstand: gezielte Methodensuche am 2026-11-14, keine systematische
Literaturuebersicht. APS nennt fuer Mazenko/Wickham 1998, der gelesene
arXiv-Preprint stammt von 1997; die Verlagsfassung wurde nicht vollstaendig
gegengelesen. Eine gezielte Korrektursuche ergab keinen einschlaegigen
Treffer, keinen Nachweis genereller Korrekturfreiheit. Die spaetere Arbeit
von Skogvoll et al. (2023) wurde im Suchlauf gefunden, aber nicht als
Volltextbeleg fuer die hier abgeleiteten Memory-Aussagen verwendet.
