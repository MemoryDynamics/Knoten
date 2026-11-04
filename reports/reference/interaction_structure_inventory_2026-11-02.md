# Energie, Fernfeld und Ladung: Bestandspruefung der Modellvarianten

Stand: 2026-11-02. Anschluss an den
[abgeschlossenen Gauss-Readout-Vergleich](memory_pair_gaussian_readout_2026-11-02.md).
**Code-/Theorieaudit und kleine algebraische Kontrollen; keine neue
Dynamik, kein Ziellauf, keine Parametersuche.** Der Wasserstoff-Benchmark
und die strikte Trennung von Referenztheorie und Emergenz bleiben erhalten.

## Ergebnis

Keine der hier geprueften Varianten liefert bereits **gemeinsam**:
eine aus Memory begruendete Energie-/Arbeitsbilanz, einen passenden
ungeschirmten Ladungskanal und die richtige Ladungsbilanz/-vorzeichenregel.
Dabei fehlen nicht ueberall dieselben Dinge:

- Der native skalare/FIFO-Kern und endliche Gauss-Readouts besitzen
  weder einen asymptotischen Coulomb-Schwanz noch eine geschlossene
  physikalische Gesamtenergie. Die exakte Lesepotentialbilanz ist bekannt.
- Der konstruierte Gradientenmediator besitzt eine gemeinsame Energie,
  aber sein Source-/Readout-Zaehler unterdrueckt den Coulomb-Pol auch
  dann noch, wenn man formal nur die Relaxationsluecke entfernt.
- Andere vorhandene Feld-APIs erlauben einen masselosen statischen
  Antwortkanal. Dieser ist ein gesetzter Grenzfall eines Zusatzmodells,
  keine Herleitung aus den Knoten. Feldantwort allein legt weder die
  Paarenergie noch elektromagnetische Ladung fest.
- Insbesondere ist die Energie eines relaxierenden skalaren Mediators
  nicht automatisch die elektrostatische Energie. Bei positiver
  Poisson-Greenfunktion ziehen gleiche skalare Quellen an. Ein
  Coulomb-Referenzkanal braucht dagegen gleichnamige Abstossung und
  ungleichnamige Anziehung.

Das ist **kein allgemeines No-go fuer Emergenz**, keine Suche ueber alle
moeglichen Knoten und kein Ausschluss kollektiver gaploser Phasen.
Die Reichweitenurteile betreffen die angegebenen linearen homogenen
Antworten bzw. direkt gelesene lokalisierte Quellen bei festen Parametern.
Eine brauchbare Approximation auf einem endlichen Abstandsintervall
waere gesondert zu zeigen. Der langfristige Benchmark verlangt zudem
Spin, Massen, Quantisierung und Spektroskopie; diese folgen auch aus einem
erfolgreichen klassischen Fernfeldtest nicht.

## 1. Gemeinsame Kriterien statt isolierter positiver Befunde

In vorgegebenem dreidimensionalem aeusserem Raum sei die isotrope
statische Paar-Potentialantwort $\chi(k)$. Mit der Fourierkonvention
$\int d^3k/(2\pi)^3$ gilt

$$
\chi(k)\sim C/k^2\quad\Longleftrightarrow\quad
G(r)\sim C/(4\pi r)
$$

fuer den entsprechenden ungeschirmten Monopolanteil, unter den ueblichen
Regularitaets-/Randannahmen. Die Kraft enthaelt eine weitere Ableitung.
Eine Feldantwort darf nicht mit dieser vollstaendigen Paarantwort
verwechselt werden. Mit einem gemeinsamen quadratischen Feldoperator
$D(k)$ und adjungiertem Source-/Readout-Port $B(k)$ ist

$$
\chi(k)=B(k)^*D(k)^{-1}B(k).
$$

Falls $B\sim k^p$ und $D\sim k^{2r}$ mit nichtverschwindenden
Koeffizienten, braucht ein Coulomb-Pol **$r=p+1$**. Ein masseloser
Feldpropagator $1/k^2$ genuegt also bei zwei Gradientenports nicht.
Ein source-neutraler Formfaktor kann den Monopolrest ebenfalls aufheben.
Die Vorzeichen der **Energie** werden durch diese positive
Suszeptibilitaetsformel allein noch nicht festgelegt.

Fuer eine physikalische Deutung muessen daneben bestimmt sein:
der dynamische Quellenzustand, sein leistungskonjugierter Eingriff,
die gemeinsame Energie mit Source-Arbeit und Verlusten sowie eine
additive, lokal bilanzierte Ladung. Eine benannte Richtung, ein
gesetztes Vorzeichen oder eine positive Occupancy-Masse sind keine
Herleitung einer elektrischen Ladung. Die 3D-Fernfeldannahme ist hier
Benchmark-Eingabe, keine Ableitung der inneren oder aeusseren Dimension.

## 2. Was konkret im Repository steht

Die unten verlinkten Quellmodule wurden im Arbeitsstand `848705f`
gelesen. Das ist eine benannte Bestandspruefung, kein behaupteter Audit
jedes historischen Experimentes oder jeder moeglichen Modellphase.

| Bestand | Statische Struktur | Energiebefund und Grenze |
| --- | --- | --- |
| [Skalare Kernel](../../src/emergenz_knoten/kernels.py), [spektrale Darstellung](../../src/emergenz_knoten/spectral_memory_field.py) | Endlich viele feste Gaussbreiten; regulaer bei $k=0$. Nullintegral-Kompensation entfernt den konstanten Term, erzeugt keinen Pol. | Native [FIFO-Lesebilanz](../../docs/reference/memory_pair_energy.md) bleibt offen fuer physikalische Gesamtenergie. Mehr Kernelbreiten reparieren dies nicht automatisch. |
| [Vektormemory](../../src/emergenz_knoten/vector_memory.py), [orientierte Quelle](../../src/emergenz_knoten/oriented_source.py) | Gerichtete Deposits mit Gaussfaktoren, bei lokalisierten Historien weiterhin kurzreichweitig. | `eta_vector=0` ist passiv; die API erlaubt auch Alignment-/2D-Transversal-Feedback. Dieses ist ein Zusatzkanal, weder eine Maxwell-Gleichung noch automatisch ein gemeinsamer Energieport. |
| [Relaxations-Diffusionsmemory](../../src/emergenz_knoten/relaxation_diffusion_memory.py), [Update](../../src/emergenz_knoten/spectral_memory_runtime.py) | $\alpha e^{-\nu k^2}/[1-(1-\alpha)e^{-\nu k^2}]$, multipliziert mit Quellen-/Lesefaktoren. Fuer $\alpha>0$ regulaer bei null. | Diffusion ist schon als Modellerweiterung gekennzeichnet. Normierte Deposition bindet die Quellstaerke an $\alpha$; siehe unten. |
| [Lokale Diffusions-/Telegraphkanaele](../../src/emergenz_knoten/local_mediator.py) | $1/(Dk^2+\mu)$ bzw. $1/(c^2k^2+\omega_0^2)$ statisch. Die API erlaubt $\mu=0$ bzw. $\omega_0=0$. | Vorgegebene 1D-Transportkanaele mit externer Quelle, kein abgeleiteter 3D-Ladungs-/Rueckwirkungsport. Zeitdaempfung allein oeffnet hier keine statische Luecke. |
| [Kontinuitaetsmemory](../../src/emergenz_knoten/continuity_memory.py) | Dichteantwort auf einen Dichteinput ist $\gamma/(\lambda\gamma+c_\rho^2k^2)$, nicht bloss der Kehrwert des Polpolynoms. | Zusatzgesetz fuer Dichte/Fluss. $\gamma\to0$ entfernt auch den statischen Dichtezaehler; $\lambda\to0$ bei normierter nativer Deposition entfernt deren Input. |
| [Aktives skalares Feld](../../src/emergenz_knoten/active_scalar_field.py) | Um $\phi=0$: $P(k)=1+a_2k^2+a_4k^4$, also feste homogene Luecke. Ein endlicher $k$-Instabilitaetsbereich ist kein $k=0$-Coulomb-Pol. | Mit positiver Source-Staerke und positivem Bewegungs-Gain haben Schreiben und Quellenbewegung nicht den gemeinsamen relaxativen Energieport; siehe unten. Nichtlineare strukturierte Phasen sind damit nicht umfassend klassifiziert. |
| [Aktives/inertiales Vektorfeld](../../src/emergenz_knoten/covariant_vector_field.py) | Kanalantwort $1/(a+b_{L/T}k^2+ck^4)$ bei $\omega=0$. $a=0$, $b_{L/T}>0$ ist als Parametergrenze moeglich. | Eigene Feldenergie, Traegheit und Daempfung sind Inputs. Source-to-field ist noch kein scalar-charge-to-charge-Port; ein Gradientenpaar entfernt wiederum den $1/k^2$-Pol. Keine Gauss-Nebenbedingung aus Memory. |
| [Gradientenmediator](../../src/emergenz_knoten/gradient_mediator.py), [gemeinsame Dynamik](../../src/emergenz_knoten/dynamic_gradient_mediator.py) | $g^2k^2/(\lambda\gamma+ak^2+bk^4+ck^6)$. Die zugelassene API fordert $\lambda,\gamma,a,c>0$. | Gemeinsame Source-/Feldenergie und explizite Dissipation vorhanden, aber zusaetzliche Architektur. Kein Coulomb-Pol im zugelassenen Bereich; gleiche Polstellen wie Dichte/Fluss bedeuten nicht gleiche Kopplung. |

Die spektralen und lokalen Implementierungen sind teils periodisch und
eindimensional. Ihre Modenformeln zeigen, welche Operatoren angesetzt
sind, nicht bereits eine gemessene unendliche 3D-Fernantwort. Umgekehrt
darf das Fehlen eines nativen Mechanismus nicht als fehlende Existenz
der separat implementierten Referenz-/Zusatzmodelle dargestellt werden.

## 3. Drei konkrete analytische Hindernisse

### Normiertes Vergessen und masseloser Grenzgang

Fuer eine festgehaltene Quelle und einen Modus setze $h_k=e^{-\nu k^2}$.
Der vorhandene spektrale Update ist exakt

$$
\rho_{n+1,k}=h_k[(1-\alpha)\rho_{n,k}+\alpha M_0G_k].
$$

Sein stationaerer Wert lautet

$$
\rho_{*,k}=\frac{\alpha M_0h_kG_k}{1-(1-\alpha)h_k}.
$$

Bei $k=0$ bleibt die gesamte Memory-Masse $M_0$ erhalten. Fuer jeden
festen $k\ne0$, $\nu>0$ und festen Gain hingegen gilt
$\rho_{*,k}\to0$ bei $\alpha\to0$. Fuer kleine $k$ hat die Antwort
den geschirmten Ausdruck $\alpha M_0/[\alpha+(1-\alpha)\nu k^2]$
in fuehrender Ordnung, samt glatten Quellenfaktoren. Eine wachsende
Laengenskala ist hier nicht dasselbe wie ein endlicher Coulomb-Rest.

Quellstaerke oder Readout-Gain unabhaengig festzuhalten/hochzuskalieren
waere ein anderer deklarierter Grenzgang. Im unendlichen 3D-Raum ist
die stationaere Poisson-Antwort einer dauernd gespeisten positiven
Punktquelle zudem nicht als global endliche positive Memory-Masse
integrierbar. Auf dem periodischen Gitter betrifft dies insbesondere
den Nullmodus. Diese Bilanzen duerfen nicht durch Weglassen von $k=0$
aus der Darstellung als geloest gelten.

### Gradientenport und Ordnung des Nullpunkts

Im Energie-Mediator bewirkt $-g\langle m,\nabla q\rangle$ je einen
Faktor $ik$ und seinen Adjungierten. Selbst der **formale**, in der
aktuellen API nicht zugelassene Grenzfall $\lambda\gamma=0$ ergibt

$$
\chi(k)=\frac{g^2}{a+bk^2+ck^4},\qquad a>0,
$$

also keinen Coulomb-Pol. Erst zusaetzlich $a=0,b>0$ wuerde formal
$\chi\sim g^2/(bk^2)$ liefern; dies ist eine zweite kritische
Parameterbedingung ausserhalb des auditierten positiven Bereichs.
Ein direkter skalarer Port hat einen anderen Zaehler und deshalb eine
andere notwendige Bedingung. Er darf nicht stillschweigend eingesetzt
werden, weil die Pole des Feldes aehnlich aussehen.

### Feldenergie ist nicht automatisch Coulomb-Energie

Fuer einen positiven Operator $L$ und festgelegte reelle skalare
Quellen $J$ betrachte die bereits verwendete Energieform

$$
\mathcal E[m,J]=\tfrac12\langle m,Lm\rangle-\langle J,m\rangle.
$$

Quadratische Ergaenzung liefert

$$
\mathcal E=\tfrac12\|L^{1/2}(m-L^{-1}J)\|^2
-\tfrac12\langle J,L^{-1}J\rangle.
$$

Damit ist die eliminierte Paarenergie
$-\langle J_A,L^{-1}J_B\rangle$. Fuer die positive Poisson-/Yukawa-
Greenfunktion und gleiche skalare Quellen ist das die attraktive
Vorzeichenregel. Nicht jeder positive Operator hat eine punktweise
positive Greenfunktion: die oszillatorische Antwort des alten
Gradientenmediators ist davon zu unterscheiden.

Als **bekannte Referenz**, nicht als neue Memory-Regel, hat die
Minimierung $\tfrac12\int|E|^2$ unter der Gauss-Nebenbedingung
$\nabla\cdot E=\rho_q$ dagegen

$$
E=-\nabla\phi,\quad-\Delta\phi=\rho_q,\qquad
\mathcal E_{\rm Gauss}=+\tfrac12\langle\rho_q,(-\Delta)^{-1}\rho_q\rangle.
$$

Selbstenergien sind separat zu behandeln; fuer zwei getrennte Quellen
ist der Kreuzterm positiv bei gleichem Vorzeichen und negativ bei
entgegengesetztem. Die unterschiedliche Eliminationsstruktur ist
wesentlich. Ein frei relaxierendes skalares Feld einfach umzubenennen
liefert diese elektrische Ladungsregel nicht. Auch eine attraktive
skalare Wirkung ist dadurch noch keine Gravitation: universelle
Kopplung, Stress-Energie und relativistische Dynamik fehlen.

Beim aktiven skalaren Pilot konkret erzwingt
$\dot\phi=-P\phi-u\phi^3+s\delta_X$ fuer den Feld-Gradientenfluss
den Quellterm $-s\phi(X)$ in der Energie. Ein Quellen-Gradientenfluss
mit positiver Mobilitaet waere dann $\dot X=+\mu s\phi'(X)$,
waehrend der Code $\dot X=-\eta\phi'(X)$ benutzt. Bei $s,\eta>0$
sind diese Ports nicht kompatibel mit dieser gemeinsamen Energie und
positiven diagonalen Mobilitaeten. Ein anderer Speicher, aktiver
Antrieb oder andere Vorzeichen waeren gesonderte Modellannahmen,
kein vorhandener Energieabschluss. Dies ist kein allgemeiner
Ausschluss aller Hamilton-/Reservoir-Einbettungen.

## 4. Ladungsobservable und naechster begrenzter Schritt

Der kanonische Memory-Zuwachs ist bei balancierter Gesamtmasse

$$
I(x)=\alpha[M_0G(x-X)-\rho(x)],\qquad \int I=0.
$$

Er besitzt im Allgemeinen einen Dipolmoment, aber als **ganze Quelle**
keine Monopolladung. Teilregionen koennen positive und negative
Anteile besitzen; daraus folgt noch keine robuste Zuordnung zweier
geladener Knotentypen oder eine lokale Transportgleichung mit
physikalisch bestimmtem Strom. Die positive Occupancy $\rho$ und
ihre feste Masse sind wiederum nicht automatisch elektrische Ladung.
Eine Differenz zweier etikettierter Historien kann signiert werden,
doch die Labels und ihre Bilanz waeren dann Inputs, keine Entstehung
von Proton-/Elektronenladung.

**Als naechstes ist der Quellen-/Ladungsbegriff zu schliessen, nicht
ein weiteres attraktives Potential einzustellen.** Konkret ist am
vorhandenen kanonischen Update zu pruefen, welche lokale Bilanz und
welcher Strom aus dem Schreiben/Vergessen tatsaechlich folgen, welche
Freiheiten bleiben und ob ein nichttrivialer additiver signierter
Quellenwert dadurch bestimmt wird. Eine Gauss-Nebenbedingung, ein
Inverse-Laplace-Readout oder ein neues gaploses Feld wird dabei nicht
als bereits emergent vorausgesetzt. Ein benoetigter neuer Mechanismus
ist dem Autor als ausdrueckliche Richtungsentscheidung vorzulegen.

## 5. Verifikation und Literatur

[15 kleine Kontrollen](../../tests/test_interaction_structure_inventory.py)
pruefen den exakten spektralen Fixpunkt, normierte Quellskalierung,
Nullintegral-Kompensation, vorhandene gaplose API-Grenzen,
Dichte-/Gradientenzaehler, abgewiesene kritische Parameter,
Gauss-Vektorreadout, Feldenergie-Quadratergaenzung, die verschiedenen
Kreuzenergievorzeichen und den neutralen Innovationsmonopol. Sie
verwenden keine neuen Zielbahnen. Die asymptotischen Aussagen stammen
aus den oben angegebenen Formeln, nicht aus einem Fit weniger Moden.

Verifikation am 2026-11-02: 327 betroffene Tests bestanden in 21.01 s,
einschliesslich dieser 15 neuen Kontrollen; vollstaendige konfigurierte
Ruff-Pruefung und strikter MkDocs-Build bestanden. Nach der technischen
Unterbrechung am 2026-11-04 unveraendert wieder aufgenommen und gesichert.
Diese Softwarepruefungen liefern keinen allgemeinen physikalischen
Emergenz- oder Vollstaendigkeitsnachweis.

Literaturabgleich: [David Tong, QFT, Kapitel 6](https://davidtong.org/teaching/quantum-field-theory/qfthtml/S6),
Abschnitte 6.1.1, Beginn 6.2 und 6.6.1 wurden gelesen. Dort ist $A_0$
nicht dynamisch, sondern erzwingt die Gauss-Bedingung; der
Coulomb-Grenzfall liefert gleichnamige Abstossung und ungleichnamige
Anziehung. Diese bekannten Referenzstrukturen motivieren den
Vorzeichen-/Porttest; sie sind keine Herleitung aus Memory.
Die alten Cambridge-PDF-/HTML-Adressen lieferten bei dieser Pruefung
502; verwendet wurde die HTML-Fassung auf der Autorenseite.
