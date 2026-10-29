# Memory-Paar: Lesepotential und FIFO-Bilanz

Stand: 2026-10-29. Analytische Anschlusspruefung der
[Paarreduktion](memory_pair_reduction.md), ohne neue Modellregel oder
Zielsimulation. Geprueft wird die unveraenderte synchrone Paardynamik in
[`reciprocal_nodes.py`](https://github.com/MemoryDynamics/Knoten/blob/151c479d00434dcaba9794fbfe6ee21f62af11a4/src/emergenz_knoten/reciprocal_nodes.py).

**Ergebnis:** Ein bedingtes Lesepotential erzeugt den nativen Drift exakt.
Seine Aenderung zerfaellt in einen Bewegungs- und einen FIFO-Anteil.
Der FIFO-Anteil hat kein allgemeines Vorzeichen und kann das Potential
sogar bei einem stillstehenden Punkt erhoehen. Das Lesepotential ist
deshalb keine allgemeine erhaltene oder monoton fallende Gesamtenergie.
Eine physikalische Energie einschliesslich Memory/Medium ist damit weder
hergeleitet noch ausgeschlossen. Insbesondere ist diese Bilanz noch kein
Energie-, Massen- oder Bindungsnachweis fuer den Wasserstoff-Benchmark.

## 1. Was den nativen Drift erzeugt

Fuer Empfaenger $i$ und Quelle $j$ in $\{A,B\}$ seien $Y_j$ die alten
Historien und $y_{j\ell}$ deren Punkte, vom juengsten zum aeltesten.
Mit gefuelltem FIFO der Laenge $H$ gelten

$$
w_{j\ell}=M_{0j}\alpha_jq_j^\ell,\qquad q_j=1-\alpha_j,
\qquad 0<\alpha_j\leq1,\quad M_{0j}>0.
$$

Die effektiven Kernel enthalten bereits die jeweilige Deposition.
Die Selbstkernel stammen aus der eigenen Konfiguration; der gemeinsame
Kreuzkernel und seine Depositionskonvention folgen der im
[Paar-Audit](hydrogen_pair_audit.md) dokumentierten Implementierung.
Definiere

$$
S_{ij}(x;Y_j)=\sum_{\ell=0}^{H-1}w_{j\ell}K_{ij}(x-y_{j\ell}),\qquad
V_i(x;Y)=\sum_j a_{ij}S_{ij}(x;Y_j),
$$

mit $a_{ii}=\eta_i$ und $a_{ij}=\chi$ fuer $i\ne j$. Der native Schritt ist

$$
b_i=-\nabla_x V_i(x_i;Y),\qquad
x_i^+=x_i+b_i+\epsilon_i\xi_i.
$$

Bei dieser Ableitung bleiben **beide alten Historien fest**, auch ihr
juengster Eintrag. Erst nach Berechnung beider neuen Positionen wird
geschoben und geschrieben. $y_{i0}=x_i$ darf daher nicht vor der Ableitung
als mitbewegte Variable eingesetzt werden. Es ist eine bedingte
Potentialableitung, keine Ableitung auf der gesamten konsistenten
Historienmannigfaltigkeit.

Fuer frei deklarierte konstante $\mu_i>0$ laesst sich schreiben

$$
E_{\rm read}(X;Y)=\sum_i\frac{V_i(x_i;Y)}{\mu_i},\qquad
F_i^{\rm decl}=-\frac{\nabla V_i}{\mu_i},\qquad b_i=\mu_iF_i^{\rm decl}.
$$

Dies ist eine mathematische Normierung, noch keine Auswahl einer
physikalischen Mobilitaet. Die beiden Kreuzleseterme sind keine bereits
symmetrische Zweikoerperenergie, die hier nur doppelt gezaehlt wuerde:
Die Quellen sind gespeicherte Historien, nicht die mitbewegten zweiten
Punktkoordinaten.

## 2. Exakte diskrete Bilanz

Schreibe $E=E_{\rm read}$. Ohne Taylorentwicklung oder kleines Rauschen gilt

$$
\begin{aligned}
E(X^+;Y^+)-E(X;Y)
&=\Delta_{\rm read}E+\Delta_{\rm FIFO}E,\\
\Delta_{\rm read}E&=E(X^+;Y)-E(X;Y),\\
\Delta_{\rm FIFO}E&=E(X^+;Y^+)-E(X^+;Y).
\end{aligned}
$$

Der erste Teil besitzt bei festem $Y$ die exakte Linienintegralform

$$
W_{\rm read}^{\rm decl}
=\sum_i\int_0^1 F_i^{\rm decl}(x_i+\theta\Delta x_i;Y)
\cdot\Delta x_i\,d\theta=-\Delta_{\rm read}E.
$$

Das ist konservative Linienarbeit des deklarierten Feldes; der lineare
Interpolationsweg ist kein hergeleiteter physikalischer Zwischenverlauf.
Das Produkt $F_{i,n}^{\rm decl}\cdot\Delta x_i$ ist bei einem endlichen
Schritt im Allgemeinen **nicht** gleich diesem Integral. Auch die
Linienarbeit ist ohne physikalische Zuordnung noch keine zugefuehrte
Arbeit oder dissipierte Waerme.

Fuer den zweiten Teil setze $o_j=y_{j,H-1}$. Die Indexverschiebung
$Y_j^+=(x_j^+,y_{j0},\ldots,y_{j,H-2})$ ergibt bei festem $x_i^+$

$$
S_{ij}(x_i^+;Y_j^+)=q_jS_{ij}(x_i^+;Y_j)
+w_{j0}K_{ij}(x_i^+-x_j^+)
-w_{j0}q_j^H K_{ij}(x_i^+-o_j).
$$

Damit ist die fehlende Potentialaenderung explizit:

$$
\boxed{\Delta_{\rm FIFO}E=\sum_{ij}\frac{a_{ij}}{\mu_i}
\left[-\alpha_jS_{ij}(x_i^+;Y_j)
+w_{j0}K_{ij}(x_i^+-x_j^+)
-w_{j0}q_j^H K_{ij}(x_i^+-o_j)\right].}
$$

Die drei Terme kommen aus Alterung, Neuschreiben und Ausscheiden.
Das Ausscheiden entfernt das **bereits gealterte** alte Endgewicht
$q_jw_{j,H-1}=w_{j0}q_j^H$. Die Formel gilt auch bei $H=1$ oder
$\alpha_j=1$; dann heben sich die entsprechenden Altterme auf.
Ueber mehrere Schritte teleskopiert die Summe beider Anteile exakt zur
gesamten Potentialaenderung. Die Bilanz bleibt bei additiven Innovationen
gueltig, ohne sie dadurch als thermisches Rauschen zu identifizieren.

## 3. Gegenbeispiel ohne Bewegung oder Rauschen

Schon ein erlaubter Selbstkanal, also $\chi=0$, genuegt gegen eine
allgemeine Lyapunovdeutung dieses Lesepotentials. Waehle Punktdeposition,
$H=2$, $\alpha=1/2$, $M_0=1$, $\eta=0.01$, $\epsilon=0$, $\mu=1$ und

$$
K(r)=e^{-r^2/2}-2e^{-r^2/8},\qquad
x=y_0=0,\quad y_1=L e_1,\quad L=\sqrt{8\log2/3}.
$$

Es gelten $K'(0)=K'(L)=0$. Der Punkt bleibt deshalb exakt stehen,
$x^+=x$, und $\Delta_{\rm read}E=0$. Der FIFO wird jedoch von
$(0,Le_1)$ auf $(0,0)$ umgeschrieben. Aus
$K(0)=-1$ und $K(L)=-3\,2^{-4/3}$ folgt pro Knoten

$$
\Delta E=\Delta_{\rm FIFO}E
=\frac{\eta}{4}\left(3\,2^{-4/3}-1\right)>0.
$$

Das ist kein Zeitschrittfehler eines bewegten Punktes und kein
Rauscheffekt. Es ist ein konstruierter erlaubter Zustand, kein Nachweis
eines Attraktors oder seiner Entstehung. Die Softwarekontrolle setzt
ihn in zwei entkoppelte, verschobene Knoten des nativen Paarsimulators
ein. Eine separate Kontrolle mit rein attraktivem Gausskernel liefert
einen negativen FIFO-Anteil. Der Anteil ist also im Modellbereich nicht
vorzeichenbestimmt. Fuer eine bestimmte eingeschraenkte Parameter-/
Zustandsklasse kann eine weitere Lyapunovaussage trotzdem moeglich sein.

## 4. Welche physikalische Auswahl fehlt

Eine gemeinsame Skalierung
$E\mapsto sE$, $F^{\rm decl}\mapsto sF^{\rm decl}$,
$\mu_i\mapsto\mu_i/s$ mit $s>0$ laesst den nativen Drift unveraendert.
Diese Einheiten-/Identifizierbarkeitsfreiheit ist allein kein Hindernis
fuer Physik; auch physikalische Modelle brauchen Kalibrierung.
Entscheidend fehlt hier die unabhaengige Zuordnung: Welcher Eingriff
leistet Arbeit an welcher Koordinate, und was traegt den Gegenanteil
beim Schreiben, Altern und Ausscheiden? Den berechneten FIFO-Rest
nachtraeglich als Reservoirarbeit zu benennen liefert keinen solchen
Mechanismus. Eine beliebige rein historieabhaengige Ergaenzung $C(Y)$
wuerde ebenfalls den Lesedrift unveraendert lassen, aber die Bilanz
aendern. Auch sie muesste physikalisch bestimmt werden.

Eine engere strukturelle Grenze betrifft bereits den kontinuierlichen
Vierzustandsvergleich der Paarreduktion. Fuer
$z=(x_A,c_A,x_B,c_B)$ sei $\dot z=Qz$. Eine reine Gradientendynamik
$\dot z=-M\nabla U$ mit konstantem positivem **diagonalem** $M$ wuerde
eine symmetrische Matrix $-M^{-1}Q$ verlangen. Bei $b_A>0$ gilt aber
$Q_{x_A,c_B}=b_A$ und $Q_{c_B,x_A}=0$. Keine positive diagonale Skalierung
kann diese fehlende Rueckkante ersetzen. Das widerlegt nur diese
Gradientenrealisierung in den genannten Koordinaten. Eine Energie mit
nichtdiagonaler Kopplung, reversibler Dynamik, zusaetzlichen Zustaenden
oder einem Medium ist damit nicht ausgeschlossen. Insbesondere besteht
kein Widerspruch zur bedingten kinetischen Filterenergie in den
$(c,\dot c)$-Koordinaten der vorherigen Notiz.

Die bereits implementierten Source-/Write-/Age-Bilanzen fuer den
[zusaetzlich deklarierten Center-Aktuator](scalar_memory_center_filter.md#8-center-konjugierte-aktuatorarchitektur)
bleiben getrennt. Sie zeigen, wie eine spezifizierte Kopplung bilanziert
werden kann; sie waehlen nicht die native Mikromechanik aus. Der bekannte
fehlgeschlagene P4-Gesamttest wird durch die vorliegende Algebra nicht
revidiert.

## 5. Literatur und Evidenzgrenze

[Seifert (2012), Abschnitte 2.3.1 und 4.6.1](https://arxiv.org/pdf/1205.4176),
trennt im thermischen Langevinmodell die Arbeit durch Potentialaenderung
bei festem Ort von der Bewegung im Potential. Fuer athermische Systeme
unterscheidet er mathematische Fluktuationsrelationen von einer durch
zusaetzliche physikalische Annahmen gerechtfertigten Waerme-/Arbeitsdeutung.
Diese Unterscheidung passt zur hiesigen offenen Zuordnung. Die Quelle
beweist weder unsere FIFO-Identitaet noch ein thermodynamisches No-go.
Ihr thermischer Kraft-/Rauschbezug und ihre Umkehrdynamik werden hier
nicht vorausgesetzt. Es wird kein Fluktuationstheorem fuer unseren
vollen Historienprozess beansprucht. Geprueft wurden diese Abschnitte,
nicht die gesamte Uebersichtsarbeit.

[Acht synthetische Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_memory_pair_energy.py)
pruefen die Bilanz gegen den unveraenderten nativen Simulator: H=5-Paare
mit ungleichen Quellengewichten, Relaxationen und Selbstkerneln in 3D
mit Punktdeposition und 4D mit Gaussdeposition, jeweils sieben Updates.
Geprueft werden Driftzuordnung, alle vier FIFO-Kanalidentitaeten,
Linienarbeit und Teleskopsumme. Dazu kommen die beiden H=2-Kontrollen,
ein endlicher Arbeitsquadratur-Gegencheck, zwei Normierungskontrollen
und eine feste Matrixkontrolle der fehlenden Rueckkante. Die allgemeinen
Aussagen folgen aus der Algebra, nicht aus einer endlichen Stichprobe.
Keine Zielrechnung, Parametersuche oder neue FIFO-/P5-/AL1-Freigabe.

Verifikation am 2026-10-29: **119 betroffene Tests bestanden in 9.62 s**,
einschliesslich dieser acht neuen Checks, bisheriger Paar-/Kerneltests,
AL1-Archivkontrollen und Dokumentationstests. Lint und strikter MkDocs-Bau
bestehen. Keine vollstaendige Repository-Testsuite; Produktionsdynamik,
Paper-I-Manuskript und archivierte Zielbefunde bleiben unveraendert.

Der Befund widerlegt die allgemeine Identifikation
"Kernelpotential gleich gesamte physikalische Energie". Er schliesst
nicht die Suche nach einer begruendeten effektiven Mechanik.
Die aktive Arbeitsreihenfolge bleibt allein in den
[Projektprioritaeten](../status/project_priorities.md).
