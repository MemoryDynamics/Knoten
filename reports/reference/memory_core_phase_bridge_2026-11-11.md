# Kernphase aus Memory und getrennter Feldbenchmark

Stand: 2026-11-14; begonnen am 2026-11-11. Umsetzung der Autorenentscheidung: neue Freiheitsgrade
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

Fortsetzung vom 2026-11-13: Abschnitt 6 leitet die volle normale
Rueckwirkung des bereits vorhandenen aktiven Alignment-Kanals her.
Die Referenzwirkung wird dabei nicht benutzt. Ein implementierter
Ableitungspruefer erfasst auch die beweglichen Orientierungsdeposits;
eine separate Bilanz zeigt, warum Modenintensitaet keine automatisch
erhaltene Ladung ist. Noch kein stabiler Ladungstraeger nachgewiesen.

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

## 6. Dynamischer Anschluss: Normalantwort und Ladung

### Bestehende aktive Regel statt neues Feld

Autorenfreigabe vom 2026-11-13: zuerst den Memory-basierten Ladungstraeger
verfolgen. Hier wird nur der bereits implementierte deterministische
Alignment-Kanal untersucht, kein Maxwell-Feld eingebaut und kein Gain
fuer einen Ziellauf gewaehlt. Im gefuellten, bahnkonsistenten Zustand ist

$$
x_{n+1}=x_n-\eta\sum_{j=0}^{H_s-1}w_j\nabla K(x_n-x_{n-j})
 +\eta_v\sum_{j=0}^{H_v-1}v_jG_v(x_n-x_{n-j})p_{n-j},
$$

$$
p_{n-j}=\frac{x_{n-j}-x_{n-j-1}}{\ell_j},\qquad
\ell_j=|x_{n-j}-x_{n-j-1}|,\qquad
G_v(d)=e^{-|d|^2/(2\sigma_v^2)}.
$$

Die $p_j$ sind im Simulator **Einheitsrichtungen**, im Unterschied zu
den Displacement-Readouts aus Abschnitt 1. Skalare und vektorielle
Gewichte/Horizonte duerfen verschieden sein. Zur Darstellung der letzten
aktiven Richtung ist ein zusaetzlicher Vorgaenger erforderlich; er darf
nicht aus einer kuerzeren skalaren Historie erfunden werden. Eine
gespeicherte Einheitsrichtung allein enthaelt ihre urspruengliche
Schrittlaenge nicht. Der neue Pruefer verlangt deshalb die deklarierte
vollstaendige Positionshistorie als Eingang, nicht nur einen Snapshot
der komprimierten Richtungen.

Die folgende Ableitung gilt bei $\ell_j>0$ fuer alle beitragenden
Vektordeposits. `normalize_orientation(0)` ist zwar implementiert, aber
die Normierung hat dort keine regulaere Ableitung. Solche aktiven
Zustaende werden nicht durch einen kuenstlichen Nenner-Epsilon repariert.
Ausgeschaltete oder exakt nullgewichtete Deposits erzeugen dagegen keine
solche Ableitungsbedingung.

### Vollstaendige Normalvariation

Sei die ungestoerte Historie in einer Ebene und z eine beliebige
Koordinate senkrecht dazu. Fuer den effektiven radialen Skalargradienten
schreibe $\nabla K(d)=a(|d|^2)d$. In der Gauss-Konvention des Repositorys

$$
a(r^2)=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}e^{-r^2/(2\sigma_{\rm rep}^2)}
 +\frac{A_{\rm att}}{\sigma_{\rm att}^2}e^{-r^2/(2\sigma_{\rm att}^2)}.
$$

Bei gefalteten Deposits werden die vorhandenen effektiven Breiten und
Amplituden benutzt, einschliesslich ihrer Abhaengigkeit von der
Umgebungsdimension d. Die erste Variation der Abstandsfaktoren in
Normalrichtung verschwindet. Fuer die Orientierung gilt dagegen
$D(u/|u|)\delta u=(I-pp^T)\delta u/|u|$, also hier
$\delta p_{n-j,z}=(z_{n-j}-z_{n-j-1})/\ell_j$.
Mit $c_j=\eta w_ja(|x_n-x_{n-j}|^2)$ und
$b_j=\eta_vv_jG_v(x_n-x_{n-j})/\ell_j$ folgt exakt

$$
z_{n+1}=z_n-\sum_{j=0}^{H_s-1}c_j(z_n-z_{n-j})
                  +\sum_{j=0}^{H_v-1}b_j(z_{n-j}-z_{n-j-1}).
$$

Der letzte Summand fehlt bei eingefrorenen Orientierungen. Die Funktion
[`planar_alignment_normal_row`](../../src/emergenz_knoten/vector_memory.py)
liefert die erste Zeile dieser Historienabbildung; alle folgenden Zeilen
schieben die Historie weiter. Sie laesst die Simulationsregel unveraendert.
Bei einer allgemeinen planaren Bahn sind die Koeffizienten zeitabhaengig:
Eigenwerte eines einzelnen Schritts sind dann kein Floquet-Nachweis.
Alle d-2 Normalrichtungen haben denselben Block, solange die deklarierte
isotrope Alignment-Regel und planare Grundbahn gelten. Ein positiver
Normalbefund wuerde die ebenen Formmoden noch nicht pruefen.

Eine codeunabhaengige Symmetriekontrolle ist besonders streng: Die
Zeilensumme ist 1, und fuer jede infinitesimale starre Kippung
$z_j=a_1y_{j1}+a_2y_{j2}$ muss dieselbe Zeile genau die entsprechende
Komponente des **nichtlinearen** naechsten Punkts liefern. Die Tests
pruefen dies an den vorhandenen Gradienten-/Vektorprimitive-Funktionen,
nicht an einem behaupteten Zielorbit.

### Bedingter Kreistest, keine neue Kreissuche

Nur fuer einen existierenden gleichfoermigen Kreis
$x_n=R(\cos n\theta,\sin n\theta)$ sind c,b konstant. Mit
$\lambda=e^{i\theta}$, $0<\theta<\pi$, lautet seine Existenzgleichung

$$
\lambda-1=-\sum_jc_j(1-\lambda^{-j})
              +(1-\lambda^{-1})\sum_jb_j\lambda^{-j}.
$$

Die normale charakteristische Funktion ist daher

$$
F(\mu)=\mu-1+\sum_jc_j(1-\mu^{-j})
                    -(1-\mu^{-1})\sum_jb_j\mu^{-j}.
$$

Translation liefert $F(1)=0$. **Erst die erfuellte Existenzgleichung**
liefert auch $F(e^{\pm i\theta})=0$: starre Kippungen der Kreisebene,
keine instabilen Formmoden. Fuer die zwei Kippmoden gibt es hier d-2
Kopien, keine bevorzugte aeussere Ebene. Die schon vorhandene
Polynomdivision durch $(\mu-1)(\mu^2-2\cos\theta\mu+1)$ kann diese
Symmetrien abtrennen, darf einen verbleibenden Rest aber nicht wegwerfen.
An beliebigen Kreis-Startwerten ohne Existenznachweis waere das ein
falscher Stabilitaetsnachweis.

Die leicht pruefbare notwendige Huerde wird

$$
S=F'(1)=1+\sum_j j c_j-\sum_j b_j.
$$

Bei $S<0$ ist F unmittelbar rechts von 1 negativ und fuer grosse
positive $\mu$ positiv. Daher existiert eine wachsende reelle Normalmode
$\mu>1$. Bei $S\ge0$ bleibt Stabilitaet offen: andere reelle oder
komplexe Wurzeln koennen ausserhalb des Einheitskreises liegen.
Ein rigoroser numerischer Instabilitaetsbefund braeuchte eingeschlossene
Koeffizienten und einen bewiesenen Zielorbit. Die neue binary64-Ableitung
liefert kein solches Zertifikat. Positives Alignment verringert S bei
**festgehaltener Geometrie**, veraendert aber zugleich die Existenzgleichung;
daraus folgt keine allgemeine Destabilisierung aller aktiven Orbits.

### Warum selbst eine stabile Phase noch keine Ladung ist

Fuer den abgeleiteten Readout aus Abschnitt 1 setze
$Z'=qe^{i\omega}Z+d$, wobei d genau neue Einspeisung und FIFO-Tail
enthaelt. Der naheliegende Intensitaetskandidat $I=Z^\dagger Z$ erfuellt

$$
I'-I=(q^2-1)I+2\operatorname{Re}[(qe^{i\omega}Z)^\dagger d]+d^\dagger d.
$$

Es gibt also eine explizite Quellen-/Verlustbilanz, kein allgemeines
Erhaltungsgesetz aus dieser Identitaet allein. Eine exakte Gegenprobe
bindet die Aussage an die vorhandene aktive Regel: $H_s=3$, $\eta=0$,
$q=1/2$, $w_0=1$, $H_v=1$, $v_0=1$, $\eta_v=1/2$ und die Historie
$(y_0,y_1,y_2)=(0,-e_1,-e_1)$. Die einzige aktive Einheitsrichtung ist
$e_1$, ihr Kernelwert am aktuellen Punkt 1, also $x^+=e_1/2$.
Bei $\omega=\pi/2$ gilt exakt $Z=e_1$, $Z'=(1+i)e_1/2$ und
$I'-I=-1/2$. Das sind konstruierte rationale Kontrollwerte, kein
Teilchenfit. Das Beispiel widerlegt automatische Erhaltung in der
vorhandenen Modellfamilie, nicht jeden speziellen Parameterbereich
oder die Erhaltung einer anderen Groesse auf einem eingeschraenkten Sektor.

Konstante Intensitaet auf einem speziellen Orbit kann
durch diese Terme bilanziert sein; sie beweist keine Erhaltung unter
Stoerungen oder Kopplung an einen zweiten Traeger. I ist zudem
nichtnegativ und noch keine zustandsabhaengige Plus-/Minus-Ladung.
Die Gleichung ist eine algebraische Identitaet fuer diesen Readout,
kein Ausschluss aller anderen moeglichen Ladungsdefinitionen.

Eine weitere elementare Begrenzung: Ist Q stetig und unter jedem Update
erhalten, und zieht eine einzelne endliche periodische Bahn alle
Zustaende eines Bereichs an, dann ist Q dort konstant. Auf der Bahn
haben alle Punkte wegen Erhaltung denselben Wert; durch Stetigkeit und
Annaeherung gilt dieser auch im ganzen Einzugsgebiet. Dasselbe Argument
gilt fuer eine kompakte Attraktormenge, **wenn Q auf ihr konstant ist**.
Eine stabile Struktur koennte also durchaus einen festen Artenwert
tragen. Eine variable konservierte Ladung folgt aber nicht aus der
relaxierenden Amplitude oder aus der blossen Existenz einer Umlaufphase.
Getrennte Sektoren oder eine Familie mit einer weiteren erhaltenen
Koordinate waeren zusaetzlich nachzuweisen, nicht einzubauen.

Als Methodenabgleich wurden bei
[Guillamon--Huguet, SIADS 8 (2009), DOI 10.1137/080737666](https://doi.org/10.1137/080737666)
im [Autoren-Volltext](https://web.mat.upc.edu/gemma.huguet/papers/GuillamonHuguet09.pdf)
die Abschnitte 2.1--2.3 gelesen: asymptotische Phase, Isochronen und
Phasen-/Amplitudenkoordinaten nahe hyperbolischen Zyklen. Diese Theorie
setzt den geeigneten Zyklus voraus und beschreibt einen klassischen
Zeitparameter. Hier wurde weder ihr numerisches Verfahren reproduziert
noch ihr kontinuierlicher Satz auf unser FIFO als bereits bewiesen
uebertragen. Die obigen diskreten Bilanzen folgen direkt aus der Regel.

### Verifikation und verbleibender Nachweis

Die [28 neuen kleinen Kontrollen](../../tests/test_vector_memory_normal.py)
pruefen alle Historienableitungen fuer d=3,5,7 und drei Depositionsarten,
Translation/Kippung, die Fehlantwort eingefrorener Richtungen, passive
und singulaere Grenzen, den exakt wegfallenden skalaren Selbstterm,
formale stabile/instabile Polynome und die Intensitaetsbilanz an nativen
Updates. Die formalen Polynome sind keine realisierten Memory-Orbits.
Erste Pruefung mit 25 neuen Kontrollen: 54 betroffene Tests bestanden
in 5.90 s. Nach Ergaenzung der Gegenkontrollen: **170 betroffene Tests
bestanden in 2.51 s**, davon 28 in der neuen Datei. Konfigurierte Ruff-
Pruefung, strikter MkDocs-Bau und Whitespacepruefung bestanden;
keine vollstaendige Repository-Testsuite oder unabhaengiger Beweisaudit.

Damit ist der **Pruefoperator**, nicht der Ladungstraeger, weiterentwickelt.
Noch fehlen ein geeigneter nativer Zustand, seine volle Stabilitaet und
eine zu demselben Zustand gehoerende erhaltene Quellen-/Stromgroesse.
Kein neuer Root, Ziellauf, Gain-Scan oder Referenz-Soliton wurde erzeugt.
