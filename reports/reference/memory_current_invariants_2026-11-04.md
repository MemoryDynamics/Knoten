# FIFO-Strombilanz und Grenze exakter Zustandsinvarianten

Stand: 2026-11-04. Analytischer Anschluss an die
[Energie-/Fernfeld-Bestandspruefung](interaction_structure_inventory_2026-11-02.md).
Keine neue Zielsimulation, Parametersuche oder Modellregel. Paper I bleibt
unveraendert; dieser Befund betrifft den Memory-Anschluss an Paper III.

Die [anschliessende Grenzfallpruefung](fading_memory_limits_2026-11-04.md)
behandelt separat stetige Invarianten untrunkierter Memory und gibt ein
unstetiges Gegenbeispiel. Die endliche Aussage dieses Berichts wird
dadurch nicht auf alle unendlichen messbaren Zustandsfunktionen erweitert.

## Befund und Bedeutung

Das gefuellte endliche FIFO erhaelt seine gesamte Memory-Masse exakt.
Schreiben, Altern und Entfernen des aeltesten Eintrags lassen sich als
lokale Kontinuitaetsidentitaet darstellen. Der zugehoerige Strom ist
jedoch nicht eindeutig und durch die Updategleichung nicht als
physikalischer Transport ausgewaehlt. Weder elektrische Ladung noch
Maxwell-Dynamik, eine Kraft oder eine Energie folgen daraus.

Eine zweite, staerkere Aussage gilt unter klar begrenzten Annahmen:
Bei festem endlichem H, uneingeschraenkten Ortskoordinaten, endlichem
Drift und unabhaengigem nichtentartetem Gaussrauschen kann keine
nichtkonstante messbare Funktion des aktuellen FIFO-Zustands fuer
alle Anfangszustaende fast sicher exakt erhalten sein. Der unten
ausgeschriebene Beweis benutzt die positive Dichte nach H Schritten,
nicht eine numerische Suche oder angenommene Ergodizitaet.

Das ist **kein allgemeiner Ausschluss emergenter Ladung**. Ein fester
Gesamtladungssektor, lokale entgegengesetzte Ladungen bei festem Gesamtwert,
effektive endliche Lebensdauern oder Grenzfaelle sind dadurch nicht
ausgeschlossen. Insbesondere ist ein endliches Simulationsgedaechtnis
nicht ohne Weiteres das vollstaendige physikalische System.

## 1. Exakter Update einschliesslich FIFO-Rand

Es seien H Eintraege $y_j$ in neueste-zuerst-Reihenfolge und feste
Gewichte $w_j\geq0$ gegeben. Die Depositionsform G sei normiert;
Delta-Deposits sind distributionell eingeschlossen. Mit

$$
\rho(z)=\sum_{j=0}^{H-1}w_jG(z-y_j),\qquad
\rho^+(z)=w_0G(z-x^+)+\sum_{j=1}^{H-1}w_jG(z-y_{j-1})
$$

und $w_H=0$, $a_j=w_j-w_{j+1}$ folgt unmittelbar

$$
\Delta\rho(z)=\sum_{j=0}^{H-1}a_j
 [G(z-x^+)-G(z-y_j)],\qquad
\sum_j a_j=w_0,\qquad \int\Delta\rho(z)\,dz=0.
$$

Bei monoton fallenden Gewichten sind alle $a_j$ nichtnegativ. Bei
anderen festen Gewichten bleibt die Identitaet richtig, aber einzelne
Umverteilungskoeffizienten koennen negativ sein. Der alte aktuelle Punkt
x ist kein zusaetzlicher Deposit; insbesondere darf eine Praeparation
$x\ne y_0$ nicht doppelt gezaehlt werden.

Fuer die kanonischen $w_j=M_0\alpha q^j$, $q=1-\alpha$, gilt

$$
\rho^+=q\rho+M_0\alpha G(z-x^+)
              -M_0\alpha q^H G(z-y_{H-1}),\qquad
W_H=M_0(1-q^H).
$$

Der letzte Term ist wesentlich. Ohne ihn erschiene faelschlich ein
Monopol $\alpha(M_0-W_H)=M_0\alpha q^H$. Tatsaechlich ist die volle
Bilanz exakt neutral. Die Entnahmekoeffizienten sind
$a_j=\alpha w_j$ fuer $j<H-1$, aber $a_{H-1}=w_{H-1}$.

Vor dem Fuellen ist die Lage anders: Bei n vorhandenen Eintraegen,
$n<H$, waechst die Masse beim Schreiben um $M_0\alpha q^n$.
Die Aussage fester Gesamtmasse gilt fuer das **gefuellte** FIFO.
Fuer normierte unendliche geometrische Memory ist bei Masse $M_0$
die Bilanz $\Delta\rho=\alpha[M_0G(z-x^+)-\rho]$ ohne FIFO-Rand
gueltig; der Grenzuebergang von Zustandsinvarianten ist damit noch
nicht untersucht.

## 2. Lokaler Strom: Konstruktion und Nicht-Eindeutigkeit

Waehle fuer jeden alten Deposit die gerade Verbindung nach $x^+$ und
setze $d_j=x^+-y_j$. Dann ist ein Strom pro Update

$$
J(z)=\sum_j a_j d_j\int_0^1G(z-y_j-sd_j)\,ds.
$$

Wegen $\partial_sG(z-y_j-sd_j)=-d_j\cdot\nabla G(z-y_j-sd_j)$ gilt

$$
\nabla\cdot J=\sum_j a_j[G(z-y_j)-G(z-x^+)]=-\Delta\rho.
$$

Das ist eine lokale Bilanzidentitaet, aber kein lokales Bewegungsgesetz:
Die Konstruktion verbindet im selben diskreten Update beliebig entfernte
Punkte. Sie definiert keinen endlichen Signalkegel. Fuer ein Zeitintervall
$\Delta t$ waere der zeitgemittelte Strom $J/\Delta t$.
Bei existierenden ersten Momenten gilt zudem
$\int J\,dz=\sum_j a_jd_j=\int z\Delta\rho(z)\,dz$.

Jede andere stueckweise glatte Route mit denselben Endpunkten liefert
dieselbe Divergenz. In mindestens zwei Dimensionen koennen die Stroeme
verschiedene, nichtverschwindende divergenzfreie Anteile besitzen.
Ein geschlossener Umlauf aendert die Dichte ueberhaupt nicht. Die
Dichtefolge allein identifiziert diese Umlaeufe somit nicht. In einer
Dimension mit verschwindenden Randstroemen ist diese Freiheit kleiner.

Mit Fourierkonvention $\widehat f(k)=\int e^{-ik\cdot z}f(z)\,dz$
lautet die Bedingung $ik\cdot\widehat J=-\widehat{\Delta\rho}$.
Fuer $k\ne0$ ist die rein longitudinale Wahl

$$
\widehat J_L(k)=\frac{ik}{|k|^2}\widehat{\Delta\rho}(k)
$$

eine moegliche Rekonstruktion, nicht ein hergeleitetes Kraftgesetz.
Der hier auftretende inverse Laplace-Operator kommt aus der Wahl des
Stroms. Er belegt weder eine Coulomb-Energie noch ein elektromagnetisches
Vorzeichen. Randbedingungen, Integrabilitaet und der Nullmodus sind
gesondert festzulegen; ein allgemeines Minimum-Energie-Prinzip wird
nicht vorausgesetzt.

Die zu pruefende additive Depositgroesse
$Q_f=\sum_jw_j f(y_j)$ hat die Aenderung

$$
\Delta Q_f=w_0f(x^+)-\sum_j a_j f(y_j).
$$

Bei $w_0>0$ und geforderter Gleichheit fuer **alle** neuen Orte muss
f konstant sein. Uebrig bleibt ein Vielfaches der festen Memory-Masse,
keine zustandsabhaengige Plus-/Minus-Knotenklassifikation. Dies betrifft
diesen linearen Ansatz; der folgende Satz erfasst auch nichtlineare
messbare Zustandsfunktionen unter Rauschannahmen.

## 3. Satz fuer nichtentartetes Rauschen und endliches H

**Annahmen.** Nach dem Schreiben ist der konsistente Zustand
$Z=(y_0,\ldots,y_{H-1})\in\mathbb R^{dH}$ mit aktuellem Punkt $x=y_0$.
Alle Parameter bleiben fest. Die Aktualisierung ist

$$
x^+=b(Z)+\varepsilon\xi,\qquad
Z^+=(x^+,y_0,\ldots,y_{H-2}),\qquad
\xi\sim N(0,I_d),\quad\varepsilon>0.
$$

Die Innovationen sind unabhaengig ueber Zeit, b ist messbar und bei
jedem endlichen Zustand endlich. Es gibt keine ausgeschlossenen
Konfigurationen oder zusaetzlichen erhaltenen Labels. Die kanonische
Gausskernel-Dynamik erfuellt die Driftannahme in exakter reeller
Arithmetik. Ideales Gaussrauschen ist hier eine mathematische Annahme,
kein Zertifikat fuer einen endlichen Pseudozufallszahlengenerator.

**Behauptung.** Ist $Q:\mathbb R^{dH}\to\mathbb R$ messbar und gilt
$Q(Z^+)=Q(Z)$ fast sicher fuer **jeden** Anfangszustand Z, dann ist Q
konstant.

**Beweis.** Fuer beliebige H aufeinanderfolgende Schreiborte
$u_1,\ldots,u_H$ ist die gemeinsame bedingte Dichte

$$
p_Z(u_1,\ldots,u_H)=
\prod_{r=1}^H (2\pi\varepsilon^2)^{-d/2}
\exp\left[-\frac{|u_r-b(Z_{r-1})|^2}{2\varepsilon^2}\right]>0.
$$

$Z_{r-1}$ wird aus dem Startzustand und den bereits festgelegten Orten
gebildet. Keine Unabhaengigkeit der Schreiborte wird behauptet; es
werden die bedingten Dichten multipliziert. Nach H Updates ist der
vollstaendige Zustand $(u_H,\ldots,u_1)$. Die Permutation der Koordinaten
aendert das Lebesgue-Mass nicht. Deshalb ist $P^H(Z,\cdot)$ fuer jeden
Start Z zum Lebesgue-Mass auf $\mathbb R^{dH}$ aequivalent.

Exakte Erhaltung in jedem Schritt impliziert
$P^H(Z,\{Q=Q(Z)\})=1$. Also hat die Niveaumenge $\{Q=Q(Z)\}$ ein
Lebesgue-Nullkomplement. Gaebe es zwei Startzustaende mit verschiedenen
Q-Werten, muessten zwei disjunkte Niveaumengen beide ein Nullkomplement
haben. Das ist unmoeglich. Damit ist Q konstant.

Der Beweis benutzt **gegenseitige absolute Stetigkeit**, nicht nur Erreichbarkeit
offener Mengen. Ein einzelner vorgeschriebener Zielpunkt hat weiterhin
Wahrscheinlichkeit null. Die positive Dichte ist keine untere Schranke
fuer praktische Uebergangswahrscheinlichkeiten oder Uebergangszeiten.

Bei zwei synchron gekoppelten FIFOs derselben Laenge und unabhaengigem
vollrangigem Rauschen fuer beide Punkte gilt dasselbe Produktargument
in Dimension $2dH$, sofern die gemeinsame Drift endlich bleibt.
Ein gemeinsames Rauschen niedrigen Ranges ist damit nicht abgedeckt.

### Geltungsgrenzen

- Kein Beweis fuer Existenz einer stationaeren Verteilung, Rekurrenz,
  schnelle Mischung oder Verlust langlebiger metastabiler Formen.
- Nicht nur $E[Q(Z^+)\mid Z]=Q(Z)$, sondern fast sichere Erhaltung ist
  vorausgesetzt. Martingale sind damit nicht ausgeschlossen.
- Keine Aussage fuer $\varepsilon=0$, unendliches Gedaechtnis,
  thermodynamische Grenzwerte, eingeschraenkte Zustandsraeume,
  singulaere Barrieren oder entartetes Rauschen. Ob dort die gesuchten
  physikalischen Eigenschaften entstehen, bleibt jeweils zu beweisen.
- Feste externe Labels, andere Parameterwerte oder weitere Felder sind
  nicht Funktionen des hier definierten Zustands. Sie duerfen nicht als
  widerlegte oder bereits abgeleitete Sektoren ausgegeben werden.
- Eine konstante Gesamtladung in einem festen Sektor ist mit dem Satz
  vereinbar. Lokale entgegengesetzte Anregungen und Ladungsaustausch
  sind dadurch nicht ausgeschlossen. Auch effektive endliche
  Erhaltung kann relevant sein, ist aber keine exakte Teilchenladung.

Die physikalische Konsequenz ist eng: Unterschiedliche **exakt erhaltene**
Knotenlabels koennen nicht allein nichtkonstante Readouts desselben
uneingeschraenkten endlichen verrauschten FIFO-Zustands sein.
Eine neue Symmetrie-, Topologie- oder Rauschstruktur wuerde den Vertrag
aendern und braucht eine explizite Begruendung, nicht nur ein Label.

## 4. Unabhaengige Kontrollen und Evidenzstatus

Die neue [Diagnostik](../../src/emergenz_knoten/memory_current.py) veraendert
keinen Simulator. Sie berechnet die exakten Fourierformeln fuer Delta-
oder normierte Gaussdeposition. Geradensegmente werden mit dem analytischen
Sinc-Faktor integriert; kleine Inkremente mit `expm1` ausgewertet.
Andere Depositionsformen sind im Hilfsmodul nicht implementiert.

Die [19 konstruierten Tests](../../tests/test_memory_current.py) pruefen
den echten `update_history`-Schritt, geometrische Tailkoeffizienten,
Fuellen versus volle Historie, Nullmodus, erstes Moment, Fourierdivergenz,
Translation, signierte Entnahmekoeffizienten und verschiedene Routen.
Eine unabhaengige adaptive Segmentquadratur kontrolliert den vollen Strom,
nicht nur seine Divergenz. Zwei H=3-Konstruktionen schreiben dieselbe
vorgegebene Zielhistorie aus verschiedenen Starts durch explizit berechnete
Innovationen. Sie ziehen keine Zufallszahlen und sind kein Stabilitaetslauf.
Der analytische Satz folgt aus dem Beweis, nicht aus diesen Beispielen.

Verifikation am 2026-11-04: **346 betroffene Tests bestanden in 11.24 s**,
einschliesslich dieser 19 neuen Kontrollen. Die konfigurierte Ruff-Pruefung,
der strikte MkDocs-Bau und die Whitespacepruefung bestehen. Dies ist keine
vollstaendige Repository-Testsuite und kein physikalischer oder formaler
Beweisassistenten-Pass. Alle freigabepflichtigen Zielpanels bleiben geschlossen.

## 5. Quellenregister und offene Entscheidung

| Quelle | Gepruefter Umfang | Verwendung und Grenze |
| --- | --- | --- |
| [Kanonischer Code](../../src/emergenz_knoten/core.py), `finite_memory_step`, `update_history`; [Gewichte](../../src/emergenz_knoten/kernels.py) | Update, Rauschen und FIFO-Reihenfolge direkt gelesen | Definition des hier untersuchten Modells; Beweis in idealer Arithmetik, keine Simulation daraus als Theorem ausgegeben. |
| [Esirkepov, arXiv:physics/9901047v1 (1999)](https://arxiv.org/pdf/physics/9901047) | Abstract, Einleitung und Abschnitte 2 bis Anfang 3, inklusive Bedingungen 1-3 der Dichtezerlegung | Bekannter Kontext ladungserhaltender PIC-Stroeme. Maxwell, Lorentzkraft und Teilchenladungen sind dort Inputs. Die Eindeutigkeit innerhalb einer bestimmten linearen Gitterzerlegung hebt die hier gezeigte Freiheit kontinuierlicher Routen nicht auf. Kein Volltextreview der spaeteren publizierten Fassung. |
| [Hairer, Ergodic Properties of Markov Processes, Fassung 29.07.2018](https://hairer.org/notes/Markov.pdf) | Definition 2.25/Beispiel 2.26, Definition 5.10 und Korollar 5.11 mit Beweis | Begriffe fuer Uebergangskerne und invariante Mengen. Die Aussagen in Abschnitt 5 setzen eine invariante Wahrscheinlichkeit voraus; diese wird fuer unser Modell nicht daraus uebernommen. Unser endlicher Dichtebeweis ist oben eigenstaendig angegeben. Kein vollstaendiger Literaturreview zur Nichtlinearitaet oder Metastabilitaet. |

Methodik: direkte Algebra am implementierten Update, Gegenkonstruktionen
zur Stromeindeutigkeit und endlicher bedingter Dichtebeweis, ergaenzt durch
gezielte Primaerquellenlekture. Keine Neuheitsbehauptung fuer diese
elementaren Resultate und keine umfassende No-go-Literaturrecherche.

Die neue Entscheidungsgrundlage lautet: Sollen kontrollierte Grenzfaelle
des vorhandenen Modells zuerst auf einen echten Erhaltungsmechanismus
untersucht werden, oder soll eine explizite Erweiterung mit solcher
Struktur als getrennte Hypothese vorbereitet werden? Weder Variante ist
damit ausgewaehlt oder erfolgreich. Ein blosses Aendern von Rauschstaerke,
Kernel oder H ohne benannten Mechanismus waere keine Antwort. Ein
physikalischer Ladungsnachweis muesste ausserdem den konservierten Wert
mit Quellenkopplung, Paarvorzeichen und Arbeits-/Energiebilanz verbinden.
Die verbindliche Arbeitsreihenfolge steht nur in den
[Projektprioritaeten](../../docs/status/project_priorities.md).
