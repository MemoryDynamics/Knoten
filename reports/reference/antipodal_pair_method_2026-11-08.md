# Antipodaler FIFO-Paarorbit: Existenz vor Stabilitaet

Stand: 2026-11-08. Methodenimplementierung und kleine konstruierte Tests.
**Kein neuer H1200-Lauf, keine Anker-Koeffizientenrechnung, keine
Parametersuche, keine Modellentscheidung.**

## Ergebnis

Der neue [Auswerter](../../src/emergenz_knoten/antipodal_pair_interval.py)
setzt die antipodalen Gleichungen aus Abschnitt 7 des
[kollektiven Audits](collective_memory_stability_2026-11-07.md) um.
Er trennt eine Newton-Naeherung, ein lokales Existenzzertifikat und
einen hinreichenden Instabilitaetstest. Keine seiner Ausgaben behauptet
Stabilitaet. Ein kleiner, absichtlich instabiler nativer Testorbit
besteht den Existenznachweis und scheitert anschliessend am Normaltest.
Das ist Methodenvalidierung, kein neuer Teilchenkandidat.

Der bestehende Einzelsolver und sein Parameterschema bleiben unveraendert.
`AntipodalPairParameters` komponiert dessen positive Selbstparameter mit
einem expliziten nichtnegativen `cross_eta`; keine Normierung wird
automatisch vorgenommen. Beide Knoten lesen synchron denselben Kernel
mit identischen endlichen Gewichten, ohne Rauschen. Der Auswerter
erwartet effektive Double-Gauss-Parameter, keine zusaetzliche Faltung.

## Gleichungen und Schnittstellen

Der Ansatz ist $x_{B,n}=-x_{A,n}$ mit Radius $r>0$ und Winkel
$0<\theta<\pi$. Beide Historien gehoeren zur gemeinsamen Kreisbahn;
es handelt sich nicht um zwei getrennte Knotenzentren.
Mit $w_l=\alpha M_0(1-\alpha)^l$, $l=0,\ldots,H-1$, und

$$
k(u)=-\frac{A_r}{\sigma_r^2}e^{-u/(2\sigma_r^2)}
     +\frac{A_a}{\sigma_a^2}e^{-u/(2\sigma_a^2)},
$$

gelten $a_l=\eta w_l k(2r^2(1-\cos l\theta))$ und
$b_l=\chi w_l k(2r^2(1+\cos l\theta))$.
Der Code benutzt die Vorzeichenkonvention des Einzelsolvers:

$$
F_0=1-\cos\theta-\sum_l[a_l(1-\cos l\theta)+b_l(1+\cos l\theta)],
\qquad
F_1=\sin\theta+\sum_l(a_l-b_l)\sin l\theta.
$$

Die Kreuzwirkung bei Alter null ist enthalten. Anders als die eigene
Alter-null-Verschiebung verschwindet sie im antipodalen Paar nicht.
Alle Ableitungen nach $r,\theta$ sind analytisch; die Selbstterme werden
aus dem bestehenden Intervallmodul wiederverwendet.

- `point_pair_balance_and_jacobian`: Punktwerte von $F$, Jacobian und
  $S_+=1+\sum_{l=1}^{H-1}l(a_l+b_l)$. Kein Zertifikat.
- `refine_antipodal_pair_root`: feste Zahl Newton-Schritte an den zwei
  Orbitunbekannten; alle Modellparameter bleiben fest. Kein Neustart,
  keine Daempfung, Fortsetzung oder automatische Parametersuche.
  Singularitaet, nichtendliche Auswertung oder Verlassen des physischen
  Bereichs brechen ab. Auch ein vollstaendig verbrauchtes Schrittbudget
  behauptet weder Konvergenz noch Existenz.
- `certify_antipodal_pair_box`: genau eine vorgegebene Box mit
  Intervallauswertung und Krawczyk-Bild. Strikte innere Inklusion,
  physischer Bereich, Nullenthaltung der Balance und nichtsingulaere
  Intervall-Jacobimatrix/Preconditioner sind explizite Gates.
  Es gibt keine automatische Box- oder Praezisionsanpassung.

Alle Ergebnisse enthalten Parameter und Dezimalpraezision; Newton
archiviert Iterierte/Korrekturen, der Boxauswerter auch angeforderte
Mitte/Halbbreiten und tatsaechliche binaere Intervallendpunkte.
Nur die binaeren Endpunkte steuern Zertifikatsentscheidungen.
Dezimalanzeigen sind keine Ersatz-Rundungszertifikate.
Die globale mpmath-Intervallpraezision wird auch bei Fehlern restauriert;
gleichzeitige Aufrufe in verschiedenen Threads sind nicht vorgesehen.

## Bedeutung des Zertifikats

Krawczyk liefert bei bestandenen Gates einen eindeutigen Nullpunkt
$(r,\theta)$ **innerhalb der ausgewiesenen Box**, bei festen Parametern
und festgehaltener Ansatzgeometrie. Er beweist weder globale Eindeutigkeit
noch einen Anziehungsbereich. Translation, Wahl der Ebene und
Orientierungsphase werden dadurch nicht als physikalische Freiheitsgrade
beseitigt. Numerische Intervallbibliothek und korrekte Gleichungsableitung
bleiben Voraussetzungen, kein formaler Proof-Assistant-Nachweis.

Der verwendete Einschlusssatz ist Standard; geprueft wurden Abschnitt
13.1, Saetze 13.1--13.3 und Algorithmus 13.4 in S. M. Rump,
*Verification methods: rigorous results using floating-point arithmetic*,
Acta Numerica 19 (2010), 287--449,
[Autorenfassung](https://www.tuhh.de/ti3/rump/intlab/ActaNumerica2010.pdf).
Keine Behauptung einer vollstaendigen Lektuere der 163-seitigen Arbeit
oder einer neuen Intervallmethode.

Die Ausgabe unterscheidet genau:

| Klassifikation | Aussage |
| --- | --- |
| `orbit_inconclusive` | Existenz in dieser Box nicht zertifiziert; kein Nichtexistenzbeweis. |
| `certified_orbit_common_normal_unstable` | Orbit zertifiziert und das gesamte Steigungsintervall strikt negativ; eine reelle gemeinsame Normalmode hat Multiplikator groesser eins. |
| `certified_orbit_stability_unresolved` | Orbit zertifiziert; dieser hinreichende Instabilitaetstest entscheidet nicht. |

Der zweite Fall nutzt den bereits hergeleiteten Satz $S_+<0$.
Ein negatives Intervall ohne zertifizierten Orbit erhaelt dagegen
**keine** Instabilitaetsklassifikation. Weder $S_+\geq0$ noch eine
kleine Punktrestnorm beweisen Stabilitaet. Die uebrigen normalen und
ebenen gemeinsamen/relativen Bloecke samt Symmetrie- und Jordanpruefung
bleiben bei offenem Ausgang erforderlich.

## Konstruierter nativer Testorbit

Das Methodenbeispiel ist vorab algebraisch festgelegt:
$H=2$, $r=1$, $\theta=\pi/2$, $\alpha=1/2$, $M_0=1$,
$\sigma_r=1$, $\sigma_a=3$, $A_r=1$, $A_a=3$.
Es verwendet **nicht** die H1200-Ankerparameter.
Schreibe $u=k(2)<0$, $v=k(4)>0$; hier ist $u/4+v/2>0$.
Dann setzen wir ohne Suche

$$
\chi=\frac{1}{u/4+v/2}>0,
\qquad \eta=\chi-\frac4u>0.
$$

Damit gilt analytisch $a_1-b_1=-1$ und $a_1+b_1+2b_0=1$,
also $F_0=F_1=0$. Gleichzeitig ist

$$
S_+=1+a_1+b_1=\frac{\chi u}{2}<0.
$$

Die Tests berechnen diese konstruierten Gains bei 100 Dezimalstellen
und uebergeben 90-stellige Dezimalstrings. Fuer **diese gerundeten
Parameter** erfolgen sechs Newton-Schritte ab $(1.001,1.57)$ bei
80 Stellen und eine einzige Boxpruefung mit Halbbreiten $10^{-25}$.
Zertifiziert wird der nahe Nullpunkt der uebergebenen Dezimalparameter,
nicht die exakte Identitaet seines Winkels mit $\pi/2$.
Die gemeinsame normale Instabilitaet wird mit derselben Box belegt.
Dieses Beispiel demonstriert gerade, weshalb Existenz allein nicht reicht.

Die [Methodentests](../../tests/test_antipodal_pair_interval.py) pruefen
zusaetzlich native Gradienten-/Hessianwerte bei kleinen festen Horizonten,
Finite-Differenzen des Jacobians, Reduktion auf den Einzelfall bei
$\chi=0$, Kreuzwirkung bei Alter null, Intervallenthaltung, Eingabefehler,
Abbruch ohne Wiederholung und Praezisionsrestauration. Affine und singulaere
Mockfunktionen testen ausschliesslich Ausgabegates, nicht die Physik.

Verifikation am 2026-11-08: 37 neue Methodentests; zusammen mit den
betroffenen bestehenden Intervall-, Kollektiv-, Paar-, Archiv- und
Markdown-Pruefungen **166 Tests bestanden in 3.11 s**. Ruff fuer
`src`, `tests`, `experiments/current` und `experiments/cli.py` sowie
`mkdocs build --strict` bestehen. Dies ist keine vollstaendige
Repository-Testsuite und keine unabhaengige physikalische Replikation.

## Ausfuehrungsgrenze

Dies ist eine reine Methodenbibliothek, **kein freigegebener Ziellauf**.
Sie enthaelt keinen Prozess-Watchdog oder Lease-Verbrauch. Vor einer
Zielausfuehrung sind weiterhin die Autorenentscheidung zur Kopplung,
ein festes Parameter-/Seed-/Box-/Iterationspanel und ein separat gepruefter
Einmal-Runner mit harter Zeitgrenze, einem CPU-Thread, sauberem
Code-Commit und ohne automatische Wiederholung erforderlich.
Alte AL1-/FIFO-Freigaben werden nicht wiederverwendet.

Ein erhoehter additiver Gesamt-Gain darf spaeter nicht ohne passende
Einzelreferenz als kollektiver Stabilisierungseffekt ausgegeben werden.
Die aktive Reihenfolge bleibt ausschliesslich in den
[Projektprioritaeten](../../docs/status/project_priorities.md).
Paper I bleibt unveraendert. Mechanische Stabilisierung, halbzahliger
Spin, Quarkstruktur und QFT-Emergenz sind getrennte Nachweispflichten.
