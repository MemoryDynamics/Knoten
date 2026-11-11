# Kernphase aus Memory und getrennter Feldbenchmark

Stand: 2026-11-11. Umsetzung der Autorenentscheidung: neue Freiheitsgrade
im Emergenzzweig erst herleiten, den phaenomenologischen Feld-/Kernvergleich
trotzdem ausarbeiten. Keine neue native Regel, keine Zielsimulation.
Die Arbeitsreihenfolge steht nur in den
[Projektprioritaeten](../../docs/status/project_priorities.md).

## Ergebnis und Reichweite

Ein komplexer Modenreadout laesst sich **ohne neue Zustandsvariable** aus
den vorhandenen Vektordeposits ableiten. Seine exakte Updategleichung
behaelt jedoch Einspeisung und FIFO-Tail. Eine einzelne Phase ist deshalb
noch kein autonomer, erhaltener Kernfreiheitsgrad. Hoehere Dimension
schafft mehr moegliche Strukturen, aber auch Ausweichrichtungen: Eine
projizierte Phasenwicklung kann sich ohne Nullstelle des Gesamtreadouts
aufloesen. Ein expliziter Pfad belegt das fuer die unten definierte Klasse.

Der getrennte Referenzzweig bekommt eine vollstaendig benannte klassische
Witten-Wirkung: ein wirbelbildendes Feld plus ein elektrisch geladenes,
im Vakuum nicht kondensiertes Kernfeld. Sie schliesst Strom und Energie
auf Modellebene, beweist aber weder einen stabilen Einheitsladungssoliton
noch ein Elektron. Sie ersetzt nicht die bisherige Mischkopplung durch
eine behauptete Memory-Ableitung; sie ist eine **andere, explizite
Referenzarchitektur** ohne Axionterm oder nachtraeglichen Bilanzrest.

## 1. Ein wirklich aus Historie abgeleiteter Kandidat

`oriented_history_from_state(mode="displacement")` in
[`vector_memory.py`](../../src/emergenz_knoten/vector_memory.py) bildet
aus neuesten-zuerst-Positionen die Deposits $u_j=y_j-y_{j+1}$.
Bei H gespeicherten Positionen gibt es hier $L=H-1$ solche Deposits.
Mit $w_j=w_0q^j$, $0<q<1$, definiere als Diagnose

$$
Z_n(\omega)=w_0\sum_{j=0}^{L-1}q^j e^{ij\omega}u_{n-j}
\ \in\mathbb C^d.
$$

Die reellen und imaginaeren Teile sind zwei reelle gewichtete
Memory-Momente. Die komplexe Schreibweise setzt keine Quantenamplitude
voraus. Eine Wahl von $\omega$ ist hier eine Analysefrequenz, noch keine
dynamisch ausgewaehlte Eigenfrequenz oder Massenskala. Die Konstruktion
gilt fuer beliebige endliche innere Dimension d, nicht nur fuer 3D.
Im vorhandenen Code haben Positionen und Orientierungen dieselbe
Dimension. Ein hiervon unabhaengiger hoeherdimensionaler innerer Faserraum
oder seine Beobachtungsabbildung auf einen aeusseren 3D-Raum ist damit
noch nicht implementiert oder hergeleitet.

Verschieben der Summe ergibt exakt

$$
Z_{n+1}=qe^{i\omega}Z_n+w_0u_{n+1}
       -w_0q^Le^{iL\omega}u_{n-L+1}.
$$

Ohne neue Einspeisung und Tail waere dies eine gedaempfte Rotation.
Im wirklichen endlichen Speicher darf aber keiner dieser Terme ohne
Fehlerkontrolle gestrichen werden. Fuer $|u_j|\le U$ ist der Tailbetrag
hoechstens $w_0q^LU$; die frische Einspeisung wird durch groesseres L
nicht kleiner. Der neue Deposit folgt seinerseits der nativen Dynamik.

Eine exakte Gegenprobe zeigt den fehlenden Abschluss sogar bei gleichem
vorgegebenem neuen Deposit: $L=3$, $q=1/2$, $\omega=\pi/2$, $w_0=1$.
Die Aenderung $(\delta u_0,\delta u_1,\delta u_2)=(h/4,0,h)$ laesst
Z unveraendert. Nach demselben neuen Deposit unterscheiden sich die
Readouts aber um $ih/8$. Z und die Einspeisung allein bestimmen den
naechsten Zustand also nicht. Das ist eine Aussage ueber den Filter,
kein behauptetes Paar nativer Loesungsbahnen mit gleichem Drift.

Ein begrenzter positiver Anschluss bleibt: Fuer eine fest deklarierte
reelle Projektion a sei $z=a^TZ$ und $z'=qe^{i\omega}z+b$. Wenn
$|b|<q|z|$, gilt geometrisch

$$
\left|\arg\left(\frac{z'}{qe^{i\omega}z}\right)\right|
\le\arcsin\frac{|b|}{q|z|}.
$$

Damit kann eine Phase auf einem nachgewiesenen nichtverschwindenden
Bereich kontrolliert werden. Erforderlich sind eine Amplitudenuntergrenze
und die kombinierte Einspeisungs-/Tailkontrolle. Dies ist kein Beweis
ihres Vorliegens, keiner beliebig langen Phasentreue und kein neues
exaktes Ladungsgesetz.

## 2. Mehr Komponenten schuetzen eine Phase nicht automatisch

Fuer $L\ge2$ und $\sin\omega\ne0$ ist der obige Readout auf dem
uneingeschraenkten **Displacement-Historienraum** surjektiv. Zu jedem
$Z=A+iB$ waehle

$$
u_1=\frac{B}{w_0q\sin\omega},\qquad
u_0=\frac{A-\cot\omega B}{w_0},\qquad u_{j\ge2}=0.
$$

Diese Deposits lassen sich durch rekursives Aufsummieren in echte
endliche Positionshistorien heben. Das sind zulaessige Zustaende, keine
behaupteten Attraktoren. Der Satz gilt nicht unveraendert fuer separat
laengenbeschraenkte oder einzeln normierte Deposits.

Fuer $d\ge2$ betrachte nun die geschlossene Familie

$$
Z(s,\vartheta)=(\cos s\,e^{i\vartheta},\sin s,0,\ldots),
\quad 0\le s\le\pi/2,\quad \vartheta\in S^1.
$$

Ihre Norm ist immer 1. Bei s=0 windet die erste komplexe Komponente
einmal; bei $s=\pi/2$ ist die ganze Schleife ein konstanter Vektor.
Die Phase der ersten Komponente wird undefiniert, der volle Readout
bleibt regulaer. Die obige Hebung realisiert den gesamten Pfad in
Positionshistorien. Es ist **kein Nullstellenzwang im Gesamtvektor**
noetig, um dieses projizierte Label zu verlieren. Dies ist ein expliziter
Homotopiepfad, nicht eine native zeitliche Zerfallsloesung und kein
Nachweis einer kleinen Barriere. $\vartheta$ ist hier ein Parameter
einer Zustandsfamilie, nicht bereits eine raeumliche Kernkoordinate.

Das verstaerkt den bestehenden
[Zustandsraumabgleich](topological_state_contract_2026-11-04.md), ersetzt
ihn aber nicht durch ein allgemeines No-go fuer Vektormemory. Ein aus
Memory dynamisch isolierter komplexer eindimensionaler Modenraum, ein
geordneter kollektiver Hintergrund oder hoeherdimensionale Texturen
koennten andere Bedingungen liefern. Nachzuweisen waeren dann insbesondere
die zulaessige Zustandsklasse, normale Rueckstellantwort, Amplitudengrenze
und Phasen-/Stromtransport. Eine Projektionswahl oder ein nachtraeglicher
Zwang auf eine Ebene ist keine solche Herleitung. Ein einzelnes zeitliches
Phasensignal ist zudem noch kein Feld entlang eines geschlossenen Kerns.

## 3. Phaenomenologischer Vergleich mit explizitem Ladungstraeger

Als analytischer Referenzvertrag, nicht als neue Memory-Regel, verwenden
wir die bosonische U(1)-mal-U(1)-Architektur von Witten. In vorgegebenem
3+1-dimensionalem Minkowski-Raum, Signatur $(+---)$ und $\hbar=c=1$:

$$
\mathcal L=-\tfrac14F_X^{\mu\nu}F_{X\mu\nu}
-\tfrac14F_A^{\mu\nu}F_{A\mu\nu}
 +|D_X\phi|^2+|D_A\psi|^2-V,
$$

$$
D_X=\partial+ig_X X,\quad D_A=\partial+ieA,\qquad
V=\frac{\lambda_1}{4}(|\phi|^2-v_1^2)^2
 +\frac{\lambda_2}{4}(|\psi|^2-v_2^2)^2
 +\beta|\phi|^2|\psi|^2-\frac{\lambda_2v_2^4}{4}.
$$

Alle genannten Kopplungen und $v_1,v_2$ seien positiv. Der Zielrand ist
$|\phi|\to v_1$, $\psi\to0$, mit endlicher Gesamtenergie. Der
X-Kanal ist dort massiv, der A-Kanal masselos. Die Quelle unter A ist
die **zusaetzlich vorgegebene** Spezies $\psi$, nicht ein leerer
Maxwell-Kanal neben einem neutralen Knoten.

Eine eigene elementare Potentialkontrolle liefert einen hinreichenden,
nicht notwendigen Vakuumbereich:

$$
4\beta^2>\lambda_1\lambda_2,\qquad
\lambda_1v_1^4>\lambda_2v_2^4,\qquad
m_\psi^2=\beta v_1^2-\lambda_2v_2^2/2>0.
$$

In den Variablen $x=|\phi|^2,y=|\psi|^2\ge0$ hat die Hesse-Matrix
die Diagonale $(\lambda_1/2,\lambda_2/2)$ und Nebendiagonale $\beta$.
Die erste Ungleichung macht einen inneren stationaeren Punkt zum Sattel.
Minima liegen somit auf den Achsen; deren minimale Energien sind 0
und $(\lambda_1v_1^4-\lambda_2v_2^4)/4$. Die zweite Ungleichung
waehlt den richtigen globalen Rand. Die dritte zeigt explizit die lokale
Massenluecke und folgt hier bereits aus den ersten beiden. Nur die
lokale Massenbedingung ohne globalen Vakuumvergleich reicht nicht.
Aus unserer kinetischen Normierung folgen $m_X^2=2g_X^2v_1^2$ und
$m_A^2=0$. Eine andere Feldnormierung verlangt entsprechende Faktoren.

Die Maxwell-Quelle und ihre On-shell-Bilanz sind

$$
j_A^\mu=-2e\,\mathrm{Im}(\psi^*D_A^\mu\psi),\qquad
\partial_\mu F_A^{\mu\nu}=j_A^\nu,\qquad
\partial_\mu j_A^\mu=0.
$$

Die letzte Gleichung folgt aus der $\psi$-Gleichung, da
$\partial V/\partial|\psi|^2$ reell ist. Anders als beim nackten
Axion-Bulkstrom ist kein undefinierter Kern-Bilanzrest einzusetzen.
Mit verschwindendem Materiestromfluss am aeusseren Rand wird $Q_e=\int j_A^0$
erhalten; die Energie folgt aus derselben Wirkung und umfasst beide
Felder und beide Materiespezies. Das sind Referenzgesetze, nicht
Memory-Energien. Bei offenen Raendern muessen die Ausfluesse mitbilanziert werden.

Explizit ist die Energie das Raumintegral von

$$
\mathcal E=\tfrac12(E_X^2+B_X^2+E_A^2+B_A^2)
+|D_{X0}\phi|^2+|\mathbf D_X\phi|^2
+|D_{A0}\psi|^2+|\mathbf D_A\psi|^2+V.
$$

Die Gauss-Bedingungen sind Nebenbedingungen, kein frei zu minimierender
negativer elektrostatischer Energieterm. Elektrischer Fernfluss und
Materiestromfluss am Rand sind dabei verschiedene Groessen.

### Kernbildung ist ein Spektralproblem

Das negative lokale $\psi$-Massenquadrat bei $\phi=0$ allein beweist
noch kein Kernkondensat. Um einen geraden neutralen X-Wirbel mit Profil
$|\phi|=f(r)$ und $\psi=0$ ist der lineare transversale Operator

$$
\mathcal H_\perp=-\Delta_\perp+\beta f(r)^2-\lambda_2v_2^2/2.
$$

Eine negative Eigenzahl bedeutet hier Instabilitaet des unbesetzten
Kerns gegen Kondensation, nicht Stabilitaet einer geladenen Schleife.
Bei $\psi=h(r)e^{i(kz-\omega t)}$ ist die lineare Eigenzahl
$\omega^2-k^2$. Der A-Strom ist quadratisch in $\psi$, weshalb A
in dieser linearen Onset-Pruefung verschwindet, nicht im spaeteren
endlichen geladenen Zustand.

Als reine Methoden-Gegenkontrolle, **kein Wirbelprofil**, setze
$f=0$ fuer $r<a$ und $f=v_1$ sonst. Fuer den Gauss-Testzustand
$h_R=\exp[-r^2/(2R^2)]$ ist der Rayleigh-Quotient exakt

$$
\mathcal R(R)=R^{-2}+\beta v_1^2e^{-a^2/R^2}-\lambda_2v_2^2/2.
$$

Ein negativer Wert ist ein hinreichender Onset-Test fuer diesen
deklarierten Operator; ein positiver Wert ist **kein Ausschluss** einer
negativen Eigenmode. Die Gradientenstrafe $R^{-2}$ darf nicht durch
Ablesen des lokalen Potentials ersetzt werden. Das echte f und die
spaetere Rueckwirkung sind gemeinsam aus der Wirkung zu bestimmen.

## 4. Was der Benchmark messen darf und nicht verspricht

| Groesse | Vertrag |
| --- | --- |
| Freiheitsgrade, aeussere 3D-Geometrie, relativistische Wirkung | Explizite Referenzinputs. Kein Herkunftsnachweis aus Memory. |
| Elektromagnetische Kopplung | Bei einem spaeteren Realweltvergleich $e^2=4\pi\alpha_{\rm em}$ als Input, nicht frei zur Stabilisierung verkleinern. |
| Ladung | $Q_e=e\mathcal Q$, mit klassisch stetigem Noetherwert $\mathcal Q$. Einheitsladung verlangt $\mathcal Q=\pm1$ als Vorbereitung/Input, nicht allein eine ganzzahlige geometrische Wicklung. |
| Masse | Eine Energieeinheit koennte an $m_e$ kalibriert werden. Das ist keine Massenvorhersage; gleiche Einheiten fuer alle weiteren Groessen. |
| Kernparameter | $\lambda_1,\lambda_2,\beta,g_X,v_2/v_1$ bleiben Modellparameter; reale Elektronenmasse und Ladung bestimmen sie nicht. Kein freier Scan oder Nachfit. |
| Stabilitaet und Fernfeld | Volle Materie-/Feldvariationen, Gauss-Nebenbedingungen, asymptotischer elektrischer Fluss und Rand-/Gitterfehler. Eine axialsymmetrische Relaxation oder neutraler Grenzfall allein reicht nicht. |
| Spin, Statistik, Momente | Nicht in die Definition hineinfitten. Klassische Rotation eines bosonischen Kondensats liefert weder Spin 1/2 noch Fermi-Statistik. Quantisierung bleibt getrennt offen. |

Insbesondere skaliert eine gemeinsame Energie-/Laengeneinheit
$(E,R)\mapsto(\Lambda E,R/\Lambda)$ nicht den dimensionslosen
Noetherwert $\mathcal Q$. Eine makroskopisch geladene Literaturloesung
wird durch einen Massenfit nicht zu einem einfach geladenen Elektron.
Auch das Produkt ER bleibt bei dieser Einheitenwahl unveraendert.
Keine Werte fuer die noch freien Kernparameter oder einen neuen Lauf
werden hier ausgewaehlt. Der Vergleich liefert ein geschlossenes
Referenzproblem und dessen Ausschlusskriterien, kein geloestes Teilchen.

## 5. Gezielter Literaturabgleich und Verifikation

- [Witten, Superconducting strings (1985)](https://doi.org/10.1016/0550-3213(85)90022-7):
  Originalarchitektur mit bosonischen oder fermionischen Kerntraegern.
  Hier nur Verlagsmetadaten/Abstract ueber die Princeton-Autorenseite
  geprueft; keine Behauptung, den ganzen Originalartikel gelesen zu haben.
- [Garaud--Radu--Volkov, PRL 111, 171602 (2013)](https://doi.org/10.1103/PhysRevLett.111.171602),
  [Volltext v2](https://arxiv.org/html/1303.3044v2): Modell, stationaere
  Ladung/Fernfeld und Abschnitt zur Dynamik gelesen. Stationaere Loesungen
  enthalten beide Eichfelder; die nichtlinearen Stabilitaetslaeufe wurden
  im globalen Grenzfall ausgefuehrt. Ein Uebergang zu kleiner Kopplung
  wird argumentiert, nicht als voller elektromagnetischer Lauf gezeigt.
  Diese Arbeit begruendet die Referenzwahl, nicht einen Elektronenbefund.
- [Battye--Cotterill--Pearson, JHEP 04 (2022) 005](https://doi.org/10.1007/JHEP04(2022)005),
  [Volltext v1](https://arxiv.org/pdf/2112.08066): Einleitung, Wirkung
  und Beginn von Abschnitt 2 bis Gl. (2.7) gelesen. Ihr Wirbel-U(1) ist
  lokal, das Kern-U(1) im untersuchten Modell global: neutraler
  Stromgrenzfall, keine voll rueckwirkende elektromagnetische Kernquelle.
  Der Titel allein beantwortet daher unseren Ladungs-/Stabilitaetstest nicht.

Keine Neuheitsbehauptung, kein systematischer Review und keine eigene
Reproduktion dieser Solitonen. Die algebraischen Memory-, Vakuum- und
Rayleigh-Aussagen oben sind eigene Nachrechnungen mit deklarierten
Annahmen, keine Uebertragung ihrer numerischen Stabilitaetsbefunde.

Die [kleinen Kontrollen](../../tests/test_memory_core_phase_bridge.py)
pruefen native Historienauslese gegen die Summen-/Randformel, deren
Nichtabschluss, die stetige Historienhebung, Phasenfehlerkontrolle,
Potentialbedingungen und unabhaengige Rayleigh-Quadratur.
Sie ersetzen keine Bahnen, Eigenwertloesung oder Solitonstabilitaet.
Verifikation am 2026-11-11: 19 neue Kontrollen; zuerst 89 Tests bestanden
in 11.08 s, abschliessend **103 Tests bestanden in 3.62 s**, einschliesslich
der direkt verwendeten Historien-/Vektormemory-Funktionen. Konfigurierte
Ruff-Pruefung, strikter MkDocs-Bau und Whitespacepruefung bestanden.
Keine vollstaendige Repository-Testsuite und kein neuer Produktionssolver.
