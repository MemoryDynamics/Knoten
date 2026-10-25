# FIFO-Schleife als orientierte Struktur

Stand: 2026-10-25. Analytische Strukturauswahl auf Basis von `fc5a1cb`;
keine neue Modellregel, kein Ziel- oder Stabilitaetslauf und kein
unabhaengiges Fachreview. Arbeitsfolge:
[Projektprioritaeten](../status/project_priorities.md).

## 1. Der konkrete Kandidat

**Arbeitskandidat ist eine altersgeordnete rotierende Memory-Schleife mit
einem aus ihren Punkten abgeleiteten Orientierungsrahmen.** Das ist noch
kein topologisch geschuetzter Knoten, Hopfion, Spin oder Teilchen. Es ist
eine Struktur des vorhandenen Zustands, ohne ein neues Feld einzusetzen.

Die [Kreisreduktion](rotating_wave_foundation.md) liefert vorbereitete
relative Gleichgewichte im skalaren, rauschfreien K0-H-Modell. Sechs lokale
Existenzzertifikate und separate lokale 2D-Stabilitaetsbefunde liegen vor.
Der spaetere [G5-Komponentenpass](https://github.com/MemoryDynamics/Knoten/blob/fc5a1cb87ead4a5575f938918478636fc5d741e5/reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.md)
betrifft exakt $H=2400$. Er belegt weder Stabilitaet gegen zusaetzliche
3D-Auslenkungen noch Formation, Interaktion oder den vollen Horizonttransfer.
G4 liefert separat einen lokalen unendlichen Root, keine solche Stabilitaet.

Die Kreisgeschichte ist nach Alter geordnet:

$$
Y_j=R(\cos j\theta,-\sin j\theta,0),\qquad
j=0,\ldots,H-1,\quad R>0,\quad0<\theta<\pi.
$$

Die dritte Koordinate ist hier eine **gewaehlte Einbettung**, keine
hergeleitete Dimension. Fuer denselben radialen Delta-Depositionskernel
bleibt jede vorbereitete Ebene rauschfrei invariant. Deshalb uebertraegt
sich die Kreisloesung algebraisch nach 3D; ihre transversale Stabilitaet
uebertraegt sich nicht automatisch. Das FIFO-Ende wird dabei weiterhin
verworfen, nicht geometrisch mit dem Anfang verbunden.

## 2. Ein Rahmen aus vorhandenen Freiheitsgraden

Fuer $H\geq3$ setze $u=Y_1-Y_0$, $v=Y_2-Y_0$ und

$$
e_1=\frac{u}{|u|},\qquad
v_\perp=v-(v\cdot e_1)e_1,\qquad
e_2=\frac{v_\perp}{|v_\perp|},\qquad e_3=e_1\times e_2.
$$

Auf dem Bereich $u\ne0$, $u\times v\ne0$ ist
$Q(Y)=(e_1,e_2,e_3)\in SO(3)$ ein eindeutiges Readout. Die Reihenfolge
kommt von den Alterslabels, nicht von einem nachtraeglich gewaehlten
Drehsinn. Unter $Y_j\mapsto a OY_j+b$ mit $a>0$, $O\in SO(3)$ gilt
$Q\mapsto OQ$. Translation und positive Skalierung aendern den Rahmen
nicht. Bei fast kollinearen Punkten wird die Auswertung schlecht
konditioniert; ein Frame ist dort nicht durch numerisches Normalisieren
zu erzwingen. Die Normen von $u$ und $v_\perp$ sind mitzuberichten.

In 2D ist die Kreisphase eine $SO(2)$-Gruppenbahn. Im Formquotienten bleibt
ein Punkt, wie [R0](foundation_feasibility.md) festhaelt. Das bedeutet
**keine interne Phase**, nicht physikalische Bedeutungslosigkeit einer
Orientierung relativ zu anderen Objekten. Raeumliche Symmetrie ist hier
nicht automatisch eine Eichredundanz. Ein Rotor waere aber erst mit
abgeleiteter Dynamik und mechanischer Interpretation mehr als ein Readout.

Die beiden ebenen Drehsinne sind in 3D keine intrinsisch verschiedenen
Haendigkeitsklassen:

$$
Y_j(-\theta)=O_x(\pi)Y_j(\theta),\qquad
O_x(\pi)=\operatorname{diag}(1,-1,-1)\in SO(3).
$$

Sie werden durch eine eigentliche Raumrotation verbunden, ohne Spiegelung
des 3D-Raums. Ein Unterschied relativ zu einer festgehaltenen externen
Achse bleibt moeglich. Daraus folgt keine intrinsische Chiralitaet und erst
recht keine Identifikation mit der schwachen Wechselwirkung.

## 3. Echte, aber bedingte Topologie

Die starre Orientierungsfamilie einer solchen altersmarkierten Geschichte
ist $SO(3)$: Zwei nichtparallele Differenzvektoren haben keinen
nichttrivialen gemeinsamen Stabilisator unter eigentlichen Rotationen.
Die ungeordnete, unmarkierte geometrische Kreislinie waere ein anderes
Objekt mit anderem Stabilisator.

Staerker gilt fuer den ganzen Bereich $\mathcal U$ mit nichtkollinearen
ersten drei Punkten die Gram-Schmidt-Parametrisierung

$$
\mathcal U\simeq
\mathbb R^3\times SO(3)\times(0,\infty)^2\times\mathbb R
\times\mathbb R^{3(H-3)}.
$$

Die Faktoren sind $Y_0,Q,a,c,b$ und die uebrigen Punkte, mit
$u=a e_1$, $v=b e_1+c e_2$, $a,c>0$. Somit ist $\mathcal U$
zusammenhaengend und $\pi_1(\mathcal U)=\mathbb Z_2$.
**Die zwei Klassen betreffen geschlossene Wege von Konfigurationen,
nicht zwei Knotentypen oder zwei getrennte Zustandssektoren.**

Eine $2\pi$-Rotation ist in diesem Bereich nicht kontrahierbar; ihr Lift
auf die Einheitsquaternionen endet am negativen Startquaternion. Die
tatsaechlichen Punkte und der Rahmen sind nach $2\pi$ aber bereits wieder
identisch. Ein Vorzeichenwechsel einer physikalischen Wellenfunktion ist
damit nicht hergeleitet. Das Auftreten von $SO(3)$ und seiner Doppel-
ueberlagerung allein beweist weder Spin $1/2$ noch eine interne $SU(2)$-
Eichwechselwirkung.

**Dimensionsgrenze:** Bei frei zugaenglichem $d\geq4$ ist der natuerliche
Zweirahmenraum $V_2(\mathbb R^d)$, nicht $SO(3)$. Die Projektion auf den
ersten Einheitsvektor hat Faser $S^{d-2}$ und Basis $S^{d-1}$. Beide sind
dann einfach zusammenhaengend; die Homotopiesequenz ergibt
$\pi_1(V_2(\mathbb R^d))=0$. Die 3D-Wegklasse ist also nicht dimensions-
unabhaengig. Fuer eine direkte 4D-Gegenkontrolle setze

$$
h_\beta(t)=(\cos\beta\cos t,\cos\beta\sin t,\sin\beta,0),\qquad
e_1=h_\beta(t),\quad e_2=(-h_2,h_1,h_4,-h_3).
$$

Dabei sind $h_i$ die vier Komponenten von $h_\beta(t)$. Fuer
$\beta\in[0,\pi/2]$ bleiben $e_1,e_2$ orthonormal. Bei $\beta=0$ ist dies
die volle Kreisrotation in der ersten Ebene, bei $\beta=\pi/2$ ein konstanter
Rahmen. Jeder Zwischenweg ist geschlossen. Somit kann die Schleife in
4D sogar ohne Formkollaps kontrahiert werden. Eine dynamische Bindung an
einen gemeinsamen 3D-Sektor waere eine zusaetzliche zu pruefende Aussage.

Im **vollen** nativen FIFO-Konfigurationsraum sind kollineare und
kollabierte Geschichten erlaubt. Bei festem $H$ und festen Altersgewichten
ist dieser Raum $\mathbb R^{3H}$, also kontrahierbar. Fuer die oben um den
Ursprung zentrierte Kreisgeschichte ist ein expliziter Weg zur Aufloesung
der Rotationsschleife

$$
F(s,t)=sY+(1-s)O_z(t)Y,\qquad
0\leq s\leq1,\quad0\leq t\leq2\pi.
$$

Fuer jedes $s$ bleiben die Endpunkte $F(s,0)=F(s,2\pi)=Y$ fest; bei
$s=1$ ist der Weg konstant. Bei $(s,t)=(1/2,\pi)$ kollabiert die ganze
Geschichte auf null und der Rahmen ist undefiniert. Der Gausskernel bleibt
dort regulaer; eine vollstaendig kollabierte Geschichte ist sogar ein
rauschfreier Fixpunkt. Dies ist eine zulaessige Konfigurationsdeformation,
**keine simulierte Zerfallsbahn** und kein Nachweis einer kleinen Barriere.
Ein dynamisch langlebiger Bereich ohne solche Entartungen bleibt moeglich,
muss aber begruendet werden. Exakter topologischer Schutz folgt nicht aus
dem nachtraeglichen Ausschluss dieser Zustaende.

Ein einzelner Rahmen ist ausserdem kein raeumliches Ordnungsparameterfeld
$n(\mathbf x):S^3\to S^2$ mit Randbedingung. Damit liegt bisher keine
Hopf-Ladung vor; eine Normalenrichtung an einer Schleife ersetzt dieses
Feld nicht.

## 4. Die noch fehlende 3D-Stabilitaetsfrage

Fuer den radialen Drift $\nabla K(d)=\phi(|d|)d$ zerfaellt die
Linearisierung an einer ebenen Geschichte in den bekannten ebenen Block
und einen normalen Block. Schreibe $w_j=\alpha M_0(1-\alpha)^j$,
$r_j=|Y_0-Y_j|$, $c_j=\eta w_j\phi(r_j)$ fuer $j\geq1$. Fuer kleine
normale Auslenkungen $z_j$ ist der neue Normalwert

$$
z'_0=\left(1-\sum_{j=1}^{H-1}c_j\right)z_0
+\sum_{j=1}^{H-1}c_j z_j,\qquad
z'_j=z_{j-1}\quad(j\geq1).
$$

Dies definiert eine reelle $H\times H$-Companionmatrix $B_\perp$.
Die Rueckrotation um die Kreisnormale wirkt auf diese Koordinate als
Identitaet. Die Normalkraftableitung braucht hier keinen radialen
$\phi'$-Term, da die ungestoerten Chords keine Normalkomponente besitzen.

**Symmetriekontrolle:** $B_\perp\mathbf1=\mathbf1$ ist die normale
Translation. Mit $v_j=e^{-ij\theta}$ gilt auch ausserhalb eines Roots

$$
B_\perp v-e^{i\theta}v=-(F_R+iF_T)(1,0,\ldots,0)^T.
$$

An einem exakten Kreisroot folgen deshalb die neutralen Multiplikatoren
$1,e^{i\theta},e^{-i\theta}$. Das Paar beschreibt die beiden Neigungen
der Kreisebene im mitrotierenden Bezugssystem, keine instabilen internen
Moden. **Die uebrigen Normalmoden sind durch den bisherigen 2D-G5-Pass
nicht bewertet.** In hoeheren Dimensionen entstehen weitere Kopien des
Normalblocks; diese Rechnung selektiert keine Raumdimension.

Eine spaetere lokale Rauschanalyse waere zuerst eine diskrete lineare
Fluktuationsrekursion auf den stabilen Formmoden. Die Orientierung hat
Symmetriemoden und darf nicht ungeprueft als rueckstellender OU-Modus
behandelt werden. Ein kontinuierlicher OU-Grenzwert und eine
Quanteninterpretation waeren jeweils weitere, getrennte Schritte.

## 5. Strukturauswahl und entscheidbare Grenze

| Kandidat | Was vorhanden ist | Entscheidung dieses Audits |
| --- | --- | --- |
| Raumphase der ebenen Schleife | $S^1$ aus Raumrotation | Kein neuer interner Freiheitsgrad. |
| Altersmarkierte Schleife mit Rahmen | Abgeleitetes $SO(3)$-Readout in gewaehltem 3D; bedingte Wegtopologie | Geeigneter begrenzter Arbeitskandidat, kein schon geschuetzter Knotentyp. |
| Hopfion, verknuepfte Feldroehren oder intrinsische Knotenchiralitaet | Benoetigtes Feld bzw. geeignete Kurvenstruktur fehlt im geprueften Kreisast | Nicht aus der FIFO-Adresse oder dem Rahmen ableiten. |

Das naechste fachliche Gate fuer diesen Kandidaten ist in den
[Projektprioritaeten](../status/project_priorities.md) verankert: normaler
Stabilitaetsblock und saubere Trennung von Gruppen- und Formmoden, vor
Lebensdauer-, Teilchen- oder Kopplungsinterpretation. Ein neuer messender
Lauf braucht einen vorab begrenzten Vertrag und Ausfuehrungsfreigabe.
Keine neue Parametersuche, G5-Wiederholung oder P5-Freigabe folgt aus
dieser analytischen Strukturauswahl.

## 6. Literaturvergleich ohne Modellimport

Geprueft am 2026-10-25. Quellenbefunde, keine eigene Reproduktion:

| Primaerquelle und gelesener Umfang | Verwendbare Aussage | Fehlende Uebertragung |
| --- | --- | --- |
| [Krzyzanowska--Nowel, 1507.04892v2](https://arxiv.org/pdf/1507.04892v2), Einleitung und Definitionen in Abschnitt 2 | Der Raum unabhaengiger geordneter Rahmen und seine Homotopie sind bekannte mathematische Strukturen, insbesondere die $\mathbb Z_2$-Gruppe fuer zwei Rahmenvektoren in 3D. | Keine physikalischen Zustaende oder Quantenstatistik aus dem Rahmenbegriff; die 4D-Gegenkontrolle oben ist eine eigene elementare Rechnung. |
| [Krusch--Speight, hep-th/0503067v2](https://arxiv.org/pdf/hep-th/0503067v2), Einleitung und Abschnitte 2--3 | Hopf-Solitonen verwenden ein $S^2$-wertiges Feld samt Randbedingung; die Konfigurationsraumtopologie ist fuer fermionische Quantisierung relevant. | Die Quantisierung und das Feld sind nicht aus unserer skalaren Memory hergeleitet. |
| [Eto--Hamada--Nitta, 2407.11731v2](https://arxiv.org/pdf/2407.11731v2), Einleitung, Modell und Knot-Soliton-Abschnitt bis zur Stabilisierungserklaerung | Verknuepfte Defekte zweier komplexer Skalarfelder koennen in dem vorgeschlagenen Modell durch die Kopplung an ein Eichfeld stabilisiert werden. | Konkrete zusaetzliche Felder und Kopplungen, kein allgemeiner QFT-Satz ueber beliebige Knoten; keine Ableitung der schwachen Wechselwirkung aus FIFO-Robustheit. |
| [Jaeykkae--Speight, PRD 84, 125035](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.84.125035), Verlagsabstract | In der dort untersuchten Ginzburg-Landau-Fortsetzung verschwinden Knotensolitonen beim Wiederherstellen der zuvor weggelassenen Superstromkopplung. | Gegenbeispiel gegen pauschale Stabilisierung durch weitere Felder; kein Volltextaudit und kein No-go fuer andere Feldmodelle. |

Die Hypothese einer spaeteren Stabilisierung durch andere Strukturen bleibt
offen. Ob eine Kopplung zur schwachen Wechselwirkung gehoert, verlangt
deren konkrete Symmetrie-, Ladungs- und chirale Kopplungsstruktur; weder
ein langer Zerfall noch ein $\mathbb Z_2$-Weglabel identifiziert sie.

## 7. Verifikation und Grenzen

Die [synthetischen Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_fifo_structure.py)
pruefen Rahmenkovarianz, Rotation zwischen Drehsinnen, Entartung,
Konfigurationskontraktion, Quaternion-Lift, kollapsfreie 4D-Kontraktion,
ebene Einbettung und den
Normalblock gegen den vorhandenen Produktionskernel und die unabhaengige
Kreisbalance. Die Geometrien sind kleine, fest gewaehlte Nicht-Root-
Kontrollen. Keine archivierte Zielzelle wird neu ausgewertet, kein
Spektrum oder Attraktorbecken gemessen. Die Topologieaussagen folgen aus
der expliziten Parametrisierung, nicht aus einer Punktwolken-Persistenz.

Lokaler Lauf: `pytest tests/test_fifo_structure.py -q`, 26 bestanden mit
NumPy 2.3.5, SciPy 1.16.3 und pytest 8.4.2. Diese endlichen Checks ersetzen
die allgemeinen Ableitungen und ein unabhaengiges Review nicht.

Offen bleiben Stabilitaet in den zusaetzlichen Richtungen, Kondition und
Lebensdauer des Rahmens unter Rauschen, nichtkreisfoermige Strukturtypen,
Formation und physikalische Mehrsystemdynamik. Paper-I-Baseline und alle
bisherigen FIFO-/P5-Claimgrenzen bleiben unveraendert.
