# FIFO-Strukturen: starre Bewegung und ihre Grenzen

Stand: 2026-10-27. Analytische Anschlussarbeit nach dem
[Instabilitaetsbeleg am H=1200-Kreis](https://github.com/MemoryDynamics/Knoten/blob/ad9873832335da5d9f6b2e136dd416382f88bef6/reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26/report.md).
Keine neue Modellregel, Zielauswertung, Rootsuche oder Trajektoriensimulation.
Die Arbeitsreihenfolge bleibt in den [Projektprioritaeten](../status/project_priorities.md).

**Geltungsbereich:** Die Klassifikation Punkt/Gerade/Kreis/Helix betrifft
nur starre relative Gleichgewichte einer einzelnen Bahn in **3D**. Sie
schliesst weder kugel- oder torusartige Memory-Verteilungen noch
nichtstarre Dynamik oder hoehere Raumdimensionen aus. Die normale
Kreisinstabilitaet beweist weder eine stabile Helix noch ein allgemeines
Scheitern raeumlich ausgedehnter Strukturen.

## Bahn, Memory-Form und Raumdimension trennen

Der erzeugende Punkt $x_n$ ist nicht das ganze raeumliche Objekt. Der
Zustand enthaelt seine Altersverteilung
$\rho_n=\sum_j w_j\delta_{y_j}$; das gelesene Feld ist
$\Phi_n=K*\rho_n$. Eine Bahnklassifikation ist deshalb keine
vollstaendige Klassifikation der Memory- oder Feldformen.

| Gemeinte Struktur | Innerhalb der unveraenderten Modellarchitektur denkbar | Was noch zu zeigen waere |
| --- | --- | --- |
| Kugelschale oder kugelfoermige Wolke in 3D | Eine nichtstarre Bahn bzw. rauschende Dynamik kann Richtungen abtasten; eine geglaettete Memory-Verteilung kann raeumlich ausgedehnt sein. | Ein einzelner Zustand statt nur Kugelsymmetrie nach Ensemble-/Zeitmittelung; dynamische Entstehung, Lokalisation und Robustheit. |
| Donut in 3D | Toroidale Dichtegeometrie ist nicht dasselbe wie eine helikale Punktbahn. Schon ein hinreichend dicht besetzter Kreis kann bei geeigneter positiver Glaettung und Schwelle eine torusartige Roehre darstellen. Eine Bahn auf einer Torusoberflaeche kann zwei Winkel besitzen. | Vorab definierte Aufloesung und Dichteschwelle, Selbstkonsistenz sowie Erhalt der Form statt eines Darstellungseffekts. |
| Mehrdimensionale Rotation oder Propagation | Der Kernel und die FIFO-Regel sind nicht auf 3D festgelegt. In hoeherer Dimension gibt es mehrere unabhaengige Rotationsebenen. | Die hoeherdimensionale Selbstkonsistenz und Stabilitaet sowie die Verbindung zur beobachteten Physik; Eingabedimension ist keine emergierte Dimension. |

Bei endlichem $H$ ist die rohe Memory eine atomare Verteilung. Eine
glatte Oberflaeche oder ein Volumen braucht daher eine ausdrueckliche
Diagnosekonvention, etwa positive Glaettung $G_s*\rho_n$ mit festem $s$;
sie darf nicht mit dem eventuell signierten Potential $K*\rho_n$
gleichgesetzt werden. Glaettung nur zur Diagnose ist keine neue Dynamik.
Kugelschale $S^2$, Kugelvolumen, Torusoberflaeche $T^2$ und ausgefuellter
Torus sind unterschiedliche Objekte. Eine kugelfoermige Mittelverteilung
allein beweist keine kugelfoermige, langlebige Einzelstruktur.

## 1. Welche Struktur die native Regel erhalten kann

Fuer den rauschfreien skalaren Zustand $Y=(y_0,\ldots,y_{H-1})$ gilt

$$
y'_0=\left(1-\sum_{j=1}^{H-1}c_j(Y)\right)y_0
       +\sum_{j=1}^{H-1}c_j(Y)y_j,\qquad
y'_j=y_{j-1}\quad(j\geq1),
$$

mit $c_j(Y)=\eta w_j\varphi(|y_0-y_j|^2/2)$ und
$w_j=\alpha M_0(1-\alpha)^j$. Hier bezeichnet $\varphi(\chi)$ den
Double-Gaussian-Gradientenfaktor als Funktion der halben Abstandsquadrate,
wie in der [Kreisreduktion](rotating_wave_foundation.md).

**Fixpunkte:** Aus $Y'=Y$ folgt bereits durch die Verschiebungszeilen
$y_0=\cdots=y_{H-1}$. Umgekehrt ist jede solche kollabierte Historie ein
Fixpunkt, weil alle Kraftdifferenzen verschwinden. Ein raeumlich ausgedehnter,
deterministisch ruhender FIFO-Fixpunkt existiert damit nicht. Eine stationaere
Wahrscheinlichkeitsverteilung unter Rauschen ist eine andere Aussage.

**Affiner Raum:** Die Koeffizienten der ersten Zeile summieren sich exakt
zu eins. Deshalb gilt $\operatorname{aff}(Y')\subseteq\operatorname{aff}(Y)$,
auch bei negativen $c_j$. Dies ist keine Konvexhuellen- oder
Kontraktionsaussage. Eine exakt ebene rauschfreie Historie bleibt eben;
eine normale Instabilitaet benoetigt eine normale Anfangsstoerung, Rauschen
oder numerischen Fehler als Anregung. Daraus folgt keine Selektion von 3D
aus einem hoeherdimensionalen Raum.

## 2. Vollstaendige Geometrie der starren relativen Gleichgewichte in 3D

Ein starres relatives Gleichgewicht bedeutet hier exakt
$\mathcal F(Y)=gY$ mit einer festen eigentlichen Isometrie
$g(x)=Qx+t$, $Q\in SO(3)$, angewendet auf jede Altersklasse.
Die native Abbildung $\mathcal F$ ist euklidisch aequivariant. Daher
gilt $\mathcal F^n(Y)=g^nY$. Aus den Verschiebungszeilen folgt zudem
$y_j=g^{-j}y_0$: Die Historienpunkte sind nicht frei waehlbare Punkte
eines starren Koerpers, sondern Abschnitte genau einer Bahn.

Fuer $Q=I$ ist diese Bahn eine Gerade oder ein ruhender Punkt.
Fuer $Q\ne I$ besitzt $Q$ eine Achse $a$. Schreibe $t=v a+t_\perp$.
Auf der Ebene senkrecht zu $a$ ist $I-Q$ invertierbar; ein Achsenpunkt
$b$ mit $(I-Q)b=t_\perp$ entfernt den transversalen Translationsanteil.
In geeigneten Koordinaten bleibt

$$
x_n=b+R\cos(n\theta)e_1+R\sin(n\theta)e_2+(z_0+nv)a.
$$

Das umfasst Kreis ($v=0$), Helix ($Rv\ne0$) und degenerierte Faelle.
Es ist eine elementare diskrete Schraubenzerlegung, kein neuer
allgemeiner Geometriesatz. Sie behauptet noch nicht, dass eine dieser
Bahnen die Kraftgleichung erfuellt oder stabil ist.

Bei $v\ne0$ ist die vollstaendige Bahn axial unbeschraenkt und nicht
geschlossen, obwohl die letzten $H$ Punkte relativ zum aktuellen Punkt
beschraenkt sein koennen. Bei $v=0$ liegt die Bahn in einer Ebene.
Damit erzeugt diese Klasse in 3D keinen eingebetteten nichttrivialen
geschlossenen Bahnknoten. Eine kuenstliche Verbindung vom aeltesten zum
juengsten Speicherpunkt waere eine zusaetzliche Konvention, keine
native Bindung. Die Aussage betrifft diese Bahn-/Historienklasse, nicht
alle denkbaren Topologien von Feldern oder zeitabhaengigen Attraktoren.

**Geometrische Haendigkeit ist moeglich, aber nicht geschuetzt.** Anders
als beim Kreis kann eine nichtdegenerierte altersmarkierte Helix nicht
durch eine eigentliche Rotation mit ihrem Spiegelbild identifiziert
werden. Fuer die unten verwendete Historienkonvention und $H\geq4$ gilt
fuer das orientierte Volumen der ersten vier Punkte

$$
\det(y_1-y_0,y_2-y_0,y_3-y_0)
=4R^2v\sin\theta(1-\cos\theta)^2.
$$

Der Ausdruck bleibt unter Translation und eigentlicher Rotation gleich,
wechselt aber unter Spiegelung das Vorzeichen. Fuer $R>0$, $v\ne0$ und
$0<\theta<\pi$ ist er ungleich null. Er kann kontinuierlich ueber $v=0$
verschwinden: geometrische Haendigkeit ist damit weder eine geschuetzte
topologische Ladung noch Quantenchiralitaet. Dies ist eine Eigenschaft
des Ansatzes, noch kein existierender oder stabiler neuer Knotentyp.

## 3. Exakte Schraubenbalancen ohne zusaetzliches Feld

Fuer $R>0$, $0<\theta<\pi$ und axialen Vorschub $v$ pro Update setze

$$
y_j=(R\cos j\theta,-R\sin j\theta,-jv),\qquad
\chi_j=R^2(1-\cos j\theta)+\frac{j^2v^2}{2},\qquad
c_j(R,\theta,v)=\eta w_j\varphi(\chi_j).
$$

Der naechste Bahnpunkt soll $(R\cos\theta,R\sin\theta,v)$ sein.
Direktes Einsetzen ergibt genau die drei Bedingungen

$$
F_R=\cos\theta-1+\sum_j c_j(1-\cos j\theta)=0,
$$

$$
F_T=\sin\theta+\sum_j c_j\sin j\theta=0,
$$

$$
v Z(R,\theta,v)=0,\qquad Z(R,\theta,v)=1+\sum_j j c_j(R,\theta,v).
$$

**Nicht durch $v$ dividieren, wenn $v=0$.** Am Kreis ist die dritte
Gleichung automatisch erfuellt. Fuer eine echte Helix $v\ne0$ muss
hingegen $Z=0$ zusammen mit beiden planaren Gleichungen gelten.
Die ersten beiden Residuen und $Z$ sind gerade in $v$, die undividierte
axiale Gleichung ist ungerade. Spiegelpartner sind keine unabhaengigen
Existenzergebnisse.

Selbst wenn $Z=0$ loesbar ist, kann $F_R\ne0$ bleiben. Eine synthetische
H=2-Kontrolle konstruiert genau diesen Fall mit dem nativen Kernel:
$c_1=-1$ liefert $Z=F_T=0$, aber $F_R=2(\cos\theta-1)\ne0$.
Axiale Selbstkonsistenz allein ist daher kein Helixnachweis.

## 4. Was der bereits belegte negative Wert S ausschliesst

Am Kreis gilt exakt $Z(R,\theta,0)=S=p'_H(1)$. Fuer festes endliches
$H$ ist $Z$ stetig. Liegt am Kreis $S\ne0$, so existiert eine Umgebung
von $(R,\theta,0)$, in der $Z\ne0$ bleibt. In dieser Umgebung gibt es
keine selbstkonsistente Schraubenloesung mit $v\ne0$, auch wenn Radius
und Drehwinkel mitveraendert werden.

**Folgerung fuer den geprueften Anker:** Sein zertifiziertes $S<0$
schliesst eine beliebig nahe Helixfortsetzung bei unveraenderten
Parametern aus. Die Groesse dieser Umgebung ist nicht berechnet.
Ein ferner Helixast, ein nichtstarrer Attraktor oder ein spaeterer
nichtlinearer Uebergang werden dadurch nicht ausgeschlossen.

Eine stetig am Kreis ansetzende Helixverzweigung bei Parametervariation
benoetigt mindestens $S=0$. Das reicht fuer Existenz oder Stabilitaet
nicht aus. Die direkte lineare Bedeutung laesst sich ohne Eigenwertsuche
sehen: Fuer $a_j=-j$, $e_0=(1,0,\ldots,0)^T$ und den bekannten Normalblock
gilt

$$
(B_\perp-I)a=\mathbf1-S e_0,\qquad
(B_\perp-I)\mathbf1=0.
$$

Bei $S=0$ entsteht damit eine Jordan-Kette bei eins. Fuer $S\ne0$ ist
die Vorschubhistorie $a$ dagegen weder eine stationaere Driftmode noch
automatisch der instabile Eigenvektor. Negative $S$ beweist die zuvor
hergeleitete wachsende Mode, aber keine vorgegebene nichtlineare Endform.

## 5. Geradliniger Vergleich statt vorschnellem Teilchenclaim

Fuer $R=0$ entfallen die planaren Gleichungen. Ein vorbereiteter
Translator $x_n=nv a$ mit $v\ne0$ verlangt

$$
D(v)=1+\eta\sum_{j=1}^{H-1}j w_j\varphi(j^2v^2/2)=0.
$$

Falls $D(0)<0$, folgt aus Stetigkeit und $D(v)\to1$ fuer $v\to\infty$
mindestens eine positive Loesung; wegen Spiegelinvarianz auch ihr
negativer Partner. Das ist nur ein hinreichender Existenzsatz, kein
Stabilitaets- oder Formationssatz. Die Bedingung wurde hier an keinem
Zielparametersatz ausgewertet. Insbesondere ist $D(0)$ am kollabierten
Zustand nicht dasselbe wie $S$ am Kreis.

Als exakt konstruierbare Kontrolle ergibt H=2 mit rein repulsivem
Gausskernel und $\kappa=\eta w_1 A_{\rm rep}/\sigma_{\rm rep}^2>1$
den Vorschub $|v|=\sigma_{\rm rep}\sqrt{2\log\kappa}$.
Das ist ein spezieller synthetischer Grenzfall, keine Veraenderung oder
Rettung des registrierten Ankers. Gedaechtnisgetriebene Translation ist
als klassischer Mechanismus bereits eng mit bekannter Literatur verwandt.

## 6. Hoehere Dimensionen: bereits starre Bewegung ist reichhaltiger

Fuer $Q\in SO(d)$ kann eine orthonormale Basis bis zu
$\lfloor d/2\rfloor$ unabhaengige zweidimensionale Rotationsbloecke
und einen Fixraum trennen. Nach Entfernen des transversalen
Translationsanteils hat eine starre Bahn allgemein die Form

$$
x_n=b+\sum_{k=1}^{r}R_k
\bigl(\cos(n\theta_k)e_{2k-1}+\sin(n\theta_k)e_{2k}\bigr)
+n v,\qquad Qv=v.
$$

Bereits in 4D erlaubt dies

$$
x_n=(R_1\cos n\theta_1,R_1\sin n\theta_1,
     R_2\cos n\theta_2,R_2\sin n\theta_2).
$$

Diese Bahn liegt auf $S^1(R_1)\times S^1(R_2)$ in $\mathbb R^4$.
Das ist ein Torusansatz trotz fester Raumrotation, also ein direktes
Gegenbeispiel gegen eine dimensionsunabhaengige Punkt/Gerade/Kreis/Helix-
Behauptung. Eine endliche Punktfolge beweist keine gleichmaessige
Torusbelegung. In 3D kann ein geometrischer Donut dagegen schon durch
zwei nichtstarr kombinierte Winkel beschrieben werden; dafuer ist keine
physische vierte Raumdimension notwendig.

Die native Selbstkonsistenz wird nicht durch die Kinematik erledigt.
Fuer mehrere belegte Rotationsebenen ersetzt

$$
\chi_j=\sum_k R_k^2(1-\cos j\theta_k)+\frac{j^2|v|^2}{2}
$$

die Ein-Ebenen-Distanz. Jede Ebene mit $R_k>0$ braucht eigene radiale
und tangentiale Balancen aus Abschnitt 3 mit $\theta_k$; alle verwenden
dieselben $c_j=\eta w_j\varphi(\chi_j)$. Hinzu kommt bei $v\ne0$
die axiale Gleichung $Z=0$. Die Ebenen sind daher dynamisch gekoppelt,
auch wenn die kinematischen Rotationsbloecke unabhaengig sind.
Ein synthetischer 4D-Gegencheck bestaetigt diese Residuen gegen den
Produktionskernel; keine Loesung des Zielmodells wird damit behauptet.

Mehrdimensionale Propagation ist ausserdem von der Umgebungsdimension
zu trennen: Eine raeumliche Stoerung oder eine Struktur kann sich schon
in 3D in wechselnden Richtungen ausbreiten. Eine solche Antwort ist mit
der konstanten Vorschubgeschwindigkeit eines starren Ansatzes nicht
vollstaendig erfasst. Ein physikalisches Ausbreitungs- oder Lokalitaetsgesetz
muss eigens hergeleitet werden.

## 7. Gepruefte Literatur und offene Trennung

Quellenpruefung 2026-10-26/27; nur der jeweils genannte Umfang wurde fuer
diese Anschlussfrage gelesen. Keine unabhaengige Reproduktion:

| Primaerquelle / Umfang | Verwendbare Einordnung | Nicht uebertragbar |
| --- | --- | --- |
| [Kopp--Klapp, PRE 107, 024611; arXiv:2210.03182v3](https://arxiv.org/pdf/2210.03182v3), Abschnitt II sowie III.B bis zur Geschwindigkeitsformel Gl. (7)--(8), PDF-Seiten 2--5 | Repulsives Gauss-Feedback mit einem festen Zeitverzug kann gleichfoermige Translation erzeugen; eine Geschwindigkeits-Selbstkonsistenzgleichung ist bereits bekannt. | Kontinuierliche Einzelverzoegerung statt diskreter Altersverteilung; keine FIFO-Helix oder Normalstabilitaet unseres Kreises. |
| [Galloway--Justh--Krishnaprasad, Cyclic pursuit in three dimensions, CDC 2010](https://user.eng.umd.edu/~krishna/images/galloway_justh_psk_published_cdc_2010.pdf), Abschnitt V, Druckseite 7145, PDF-Seite 5 | Gerade, Kreis und Helix erscheinen als bekannte Klassen starrer relativer Gleichgewichte unter Raumbewegungen. | Mehrteilchen-Verfolgungsmodell mit eigenen Steuerregeln, kein FIFO-Existenzsatz. Unsere Verschiebungsbindung und diskrete Rechnung sind separat hergeleitet. |
| [Lisicki--Reigh--Lauga, Autophoretic motion in three dimensions](https://arxiv.org/pdf/1803.01589), Abstract, PDF-Seite 1 | Helikale Bewegung ist in klassischen Modellen durch Translation und Rotation bekannt. | Oberflaechenaktivitaet, Mobilitaet und phoretische Stroemung sind zusaetzliche Physik, nicht aus der skalaren Memory abgeleitet. |
| [Sergei Treil, Linear Algebra Done Wrong, Abschnitt 6.5, Satz 6.5.1](https://www.math.brown.edu/streil/papers/LADW/HTML_2026_08-31/Ch6.html), indexierter Volltextauszug mit Satz und Beweis; direkter Seitenabruf scheiterte am Timeout | Eigentliche orthogonale Abbildungen zerfallen in ebene Rotationsbloecke und einen Fixraum; die Ein-Achsen-Intuition aus 3D gilt nicht allgemein. | Lineare Algebra, kein Existenz- oder Stabilitaetssatz fuer das Memory-Modell. |

Ein geeigneter interagierender Baustein muesste mindestens selbstkonsistent,
relativ lokalisiert und auf einer begruendeten Zeitskala robust sein.
Strikte Stabilitaet und kontrollierte Metastabilitaet sind dabei verschiedene
Claims; eine endliche Lebensdauer waere nicht automatisch ein Ausschluss.
Erst mit dieser Abgrenzung sind kollektive Freiheitsgrade und Kopplungen
sinnvoll zu bewerten. Ein Bahnknoten braeuchte zusaetzlich eine sauber
definierte geschlossene Struktur und eine dynamische Erhaltung ihrer
Topologie. Weder die Schraubenkinematik noch das Wort Helix liefert dies.

Die analytischen Aussagen werden durch 28 kleine synthetische Kontrollen
gegen den Produktionskernel und exakte rationale Companion-Identitaeten
geprueft. Sie ersetzen kein allgemeines Fachreview. Kein Zielroot, kein
Ankerspektrum und keine Ankertrajektorie wird neu ausgewertet. Ein
unabhaengiger Existenz- und Stabilitaetsbeleg fuer einen geeigneten
3D-Baustein fehlt weiterhin; Quantisierung, Gravitation und das
Standardmodell bleiben getrennte offene Anforderungen.
