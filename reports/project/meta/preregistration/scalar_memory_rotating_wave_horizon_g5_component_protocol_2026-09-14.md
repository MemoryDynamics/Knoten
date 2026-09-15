# Prospektives Protokoll: isolierte G5-Direktsimulation

Datum: 2026-09-14.

Status: **outcome-blind eingefroren vor erstem G5-Zugriff**.

Klarstellende Amendierung 2026-09-15, weiterhin vor jedem Zielzugriff: Der
bereits registrierte FIFO-Shift wird indexgenau ausgeschrieben. Parameter,
Schwellen, Stoerungen, Entscheidungen und Stopregeln bleiben unveraendert.
Zusaetzlich wird die bereits verlangte getrennte Freigabe maschinenlesbar als
einmalige Governance-Lease konkretisiert. Auch dies aendert keine
wissenschaftliche Einstellung.

## 1. Frage und Claimgrenze

Der Komponentenlauf fragt ausschliesslich, ob der deterministische
Voll-FIFO-Kreis bei $H=2400$ unter kleinen Stoerungen lokal stabil ist oder
eine reproduzierbare lokale Instabilitaet zeigt. Er simuliert die
Grundgleichung selbst; der harmonische Oszillator ist weder Eingabe noch
Entscheidungsmodell.

Ein Resultat misst nur die lokale Dynamik des festen endlichen Kandidaten.
Es beweist weder die G1--G4-Branchverbindung noch Stabilitaet fuer
$H\to\infty$, spontane Formation, interne Phase, Interaktion, Traegheit oder
Masse. P5-D bleibt geschlossen.

## 2. Grundgleichung und feste Parameter

Mit $q=1-\alpha$ und Alter $j=0,\ldots,H-1$ lautet der deterministische
Positionsschritt

$$
x_{n+1}=x_n-\eta\sum_{j=0}^{H-1}\alpha M_0q^j
\phi(\|x_n-x_{n-j}\|)(x_n-x_{n-j}),
$$

$$
\phi(r)=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
e^{-r^2/(2\sigma_{\rm rep}^2)}
+\frac{A_{\rm att}}{\sigma_{\rm att}^2}
e^{-r^2/(2\sigma_{\rm att}^2)}.
$$

Der Zustandsvektor ist dabei nicht nur der neueste Punkt, sondern die
altersgeordnete Geschichte

$$
Y_n=(h_n^{(0)},h_n^{(1)},\ldots,h_n^{(H-1)})
   =(x_n,x_{n-1},\ldots,x_{n-H+1}).
$$

Nach dem Positionsschritt fuehrt das Skript exakt den FIFO-Shift

$$
h_{n+1}^{(0)}=x_{n+1},\qquad
h_{n+1}^{(j)}=h_n^{(j-1)}\quad(1\leq j\leq H-1)
$$

aus, also

$$
Y_{n+1}=(x_{n+1},x_n,\ldots,x_{n-H+2}).
$$

Im Code sind dies `result[0] = x_new` und
`result[1:] = state[:-1]`. Der bisher aelteste Eintrag
$h_n^{(H-1)}=x_{n-H+1}$ faellt heraus; jeder andere Eintrag wird genau um
eine Altersklasse verschoben. Beim naechsten Kraftlesen traegt
$h_{n+1}^{(j)}$ deshalb das Gewicht $\alpha M_0q^j$. Das ist die endliche,
ungekomprimierte Realisierung des exponentiell vergessenden Gedaechtnisses,
nicht eine vorgegebene Kreisgeometrie. Ein zirkulaerer Puffer waere nur eine
aequivalente Speicheroptimierung dieses Shifts.

Im mitrotierenden Rahmen wird erst nach diesem nativen Shift jede
gespeicherte Koordinate mit $R_{-\theta}$ gedreht. Diese Drehung ist nur ein
Koordinatenwechsel, keine weitere Gedaechtnisdynamik. Es gelten ohne Suche

$$
\alpha=0.01,\quad q=0.99,\quad H=2400,\quad M_0=1,
\quad\eta=0.15,
$$

$$
(A_{\rm rep},\sigma_{\rm rep},A_{\rm att},\sigma_{\rm att})
=(1,1,3.5,3),\qquad \varepsilon=0.
$$

Newton beginnt bei
$(R,\theta)=(0.946517504804225,0.015770381717135)$. Der $H=2400$-Root
wird mit dem registrierten 120-dps-Rootadapter und denselben festen
$10^{-8}$- und $10^{-30}$-Krawczykboxen neu bestimmt. Erst der zertifizierte
Root wird genau einmal nach binary64 gerundet. Es gibt keinen alternativen
Start, Parameterscan oder Root-Retuning.

## 3. Persistierter Grundgleichungs-Preflight

Vor Arnoldi und Trajektorien wird ein eigener Record erzeugt und gehasht. Er
bindet Gleichungskennung, alle Parameter, $q$, Depositionsgewicht
$\alpha M_0$, Root, Historienhash und die direkte Gewichtssumme an

$$
\sum_{j=0}^{H-1}\alpha M_0q^j=M_0(1-q^H).
$$

Fuer $Y_*=(Re^{-ij\theta})_{j=0}^{H-1}$ werden sowohl die native
Kreiskovarianz

$$
T_H(Y_*)=R_\theta Y_*
$$

als auch der mitrotierende Fixpunkt
$R_{-\theta}T_H(Y_*)=Y_*$ direkt ausgewertet. Beide maximalen
Komponentenfehler muessen hoechstens $10^{-14}$ sein. Der volle analytische
Jacobian muss Form $4800\times4800$ und genau 19196 gespeicherte Eintraege
haben; Rotations- und Translationsresiduen muessen hoechstens $10^{-10}$
sein. Jeder Fehler stoppt vor dem Eigensolver.

Historie und sparse Jacobian erhalten kanonische Little-endian-Hashes. Wegen
der trigonometrischen binary64-Konstruktion ist ihre Portabilitaetsgrenze
explizit dieselbe Plattform; die ganzzahligen LCG-Starts bleiben
plattformunabhaengig.

## 4. Lokales Spektrum

Der volle $4800$-dimensionale Jacobian wird mit zwei fest registrierten
Largest-modulus-Arnoldi-Panels ausgewertet: 24 Ritzpaare bei
`ncv=96`, Toleranz `1e-10`, maximal 20000 Iterationen und 36 Ritzpaare bei
`ncv=144`, Toleranz `1e-12`, maximal 40000 Iterationen. Die Starts sind die
bereits eingefrorenen 32-bit-LCG-Vektoren.

Jedes Ritzpaar speichert Eigenwert, Vektor, normalisiertes Residuum und
Symmetrieueberlappungen. Residuen ueber $10^{-8}$, fehlende Vektoren,
falsche Kardinalitaet, nichtendliche Werte, fehlende Symmetriemoden oder ein
Panelabstand ueber $10^{-5}$ sind `inconclusive`. Eine Spektralaussage muss
in beiden Panels von demselben gematchten transversalen Paar getragen
werden.

## 5. Nichtlineare Direktsimulation

Nur nach bestandenem Preflight und vollstaendigen Panels werden vier
Trajektorien mit exakt derselben Grundgleichung aus Abschnitt 2 gerechnet:

1. sichtbare radiale Stoerung des neuesten Punktes;
2. sichtbare tangentiale Stoerung des neuesten Punktes;
3. vollhistorische transversale Stoerung nach Projektion gegen beide
   Translationen und die Rotation;
4. ungestoerte binary64-Kontrolle.

Die Stoerungsamplitude ist $10^{-7}R$. Jeder Arm laeuft maximal 5000
Updates, wird alle 10 Schritte im translations-/rotationsreduzierten
$D_0$-Abstand ausgewertet und stoppt bei Abstand $0.25$ des
Referenznorms. Ein stabiler Befund verlangt ein gematchtes transversales
Spektrum unter $1-10^{-4}$, Abschluss aller drei Stoerungsarme, maximale
transiente Verstaerkung hoechstens 10 und Endabstand hoechstens 0.1 des
Anfangsabstands. Die exakte Kontrolle muss unter $10^{-10}$ bleiben.

Eine lokale Instabilitaet verlangt dasselbe gematchte Paar in beiden Panels
ueber $1+10^{-6}$ und Wachstum mindestens eines Stoerungsarms um Faktor 100.
Alles dazwischen bleibt unentschieden. Die nichtlinearen Arme werden nicht
aus dem Jacobian propagiert.

## 6. Resultat, Audit und Entscheidungen

Der spaetere Komponentenrecord besitzt genau die Ebenen `identity`,
`finite_root`, `preflight`, `arnoldi`, `trajectories`, `classification` und
`publication`. Unbekannte Felder, NumPy-Skalare, nichtendliche Zahlen,
Null-Locher, Hashabweichungen und widerspruechliche Zusammenfassungen sind
unzulaessig. Ergebnis-JSON und Lesereport werden vor einem zuletzt atomar
geschriebenen Hashmanifest erzeugt.

Die zulaessigen Entscheidungen sind:

- `g5-local-direct-stability-pass` nur bei vollstaendiger Spektrum- und
  Kontraktionsevidenz;
- `g5-local-direct-instability-supported` nur bei gematchtem instabilem
  Spektrum plus nichtlinearem Wachstum;
- `g5-inconclusive` bei jedem regulaeren numerischen Zwischenzustand;
- `g5-experiment-invalid` bei Provenienz-, Vertrag-, Hash-, Typ- oder
  Publikationsfehlern.

Ein Standardbibliothek-Auditor rekonstruiert Recordhashes, Kardinalitaeten,
Schwellen, Panelmatch, Trajektoriensummaries und Entscheidung ohne Import des
Runners. Er ist kein zweiter sparse Eigensolver und kann $Jv-\lambda v$
nicht unabhaengig numerisch reproduzieren; diese Trust Base bleibt im
Ergebnis sichtbar.

## 7. Falsifikation, Freigabe und Stopregeln

Vor einem Zielzugriff muessen Tests mindestens mutierte Parameter, falsches
$q$, falsche Gewichtssumme, native Kreisdrift, Fixpunktdrift, falsche
Jacobiandimension/-sparsitaet, Symmetriefehler, mutierte LCG-Starts,
partielle Panels, Nullvektoren, negative/zu grosse Residuen, ungematchte
Instabilitaet, mutierte Stoerungen, fruehe Stops, erfundene Samples und ein
fehlendes Manifest erkennen.

Ein Major-/Critical-Befund, rote exakte CI oder ein schmutziger Arbeitsbaum
stoppt die Ausfuehrung. Nach Zielzugriff sind Parametersuche, Wechsel des
Roots, neue Stoerungsrichtung und Wiederholung ohne Amendierung verboten.

Die Implementierung bleibt zunaechst durch einen getrackten Governance-Record
geschlossen. Eine spaetere Freigabe darf nur diesen Record aendern und muss
einen ausdruecklichen Nutzerentscheid, UUIDv4, Implementierungscommit,
offizielle erfolgreiche CI fuer genau diesen Commit, Readinessreview,
geschuetzte Git-Blobs, Ergebnisvertrag und exakte Python-/NumPy-/SciPy-/
mpmath-Versionen binden. Der Guard prueft sauberen Arbeitsbaum, identischen
Upstream, leere feste Zielpfade und verbraucht vor jeder numerischen Arbeit
atomar genau eine Receipt. Receipt-Hash und Autorisierung werden im
Ergebnisrecord gespeichert und vom Publikationsaudit gegen die Receipt-Datei
rekonstruiert.

Dieses Protokoll autorisiert noch keinen Zielzugriff. Erst ein getrenntes
Readinessreview nach targetfreier Implementierung, unabhaengigem Audit und
gruener exakter CI darf genau einen isolierten G5-Komponentenlauf zur
Nutzerfreigabe vorschlagen.
