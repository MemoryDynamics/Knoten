# B1: Zustand, Eingriffe und Readouts

Stand: 2026-10-21. Analytische Bestandsaufnahme gegen `0ef0bf2`, keine neue
Modellregel und kein Produktionslauf. Anschluss an den
[R0-Audit](foundation_feasibility.md) und die
[Forschungsroadmap](../status/research_roadmap.md).

## Ergebnis und Geltungsbereich

Fuer die vorhandene Frozen-Source-Erweiterung lassen sich Zustand,
Quellenvariation, Readout, Ein-Schritt-Antwort und bedingte Verteilung
explizit angeben. Das schliesst die analytische B1-Bestandsaufgabe ab.
Ein gemeinsamer **physikalischer** Zwei-Stationen-Vertrag fuer II/III fehlt
weiterhin: Die Einzelprozessregel legt weder ein Mehrsystemgesetz noch
unabhaengige Messwahlen, Aktuatoren und Detektoren fest. Die vorhandenen
Kopplungen sind deklarierte Erweiterungen, keine Herleitung dieser Regeln.

| Bestehender Zweig | Zustand und Praeparation | Eingriff und Readout | Informationszugriff / Grenze |
| --- | --- | --- | --- |
| Paper-I-Einzelprozess | Position und vollstaendige Memory; Parameter und Anfangszustand gesetzt | Position, Memory-Zentrum und Formobservablen | Liest eigene gesamte Spur; keine zwei separat einstellbaren Messstationen. |
| Frozen Source | Bewegliches Ziel mit geordneter Historie, festgehaltene Quellenhistorie, Gewichte und Pulszaehler | Initiale Verschiebung nur der Quelle; Zielposition, Memory-Zentrum und Form | Direkter Zugriff auf alle Quellenpunkte beim Force-Read; Quelle hat weder autonome Antwort noch Rueckwirkung. |
| Direkt reziprokes Paar | Zwei vorbereitete Historien, getrennte Innovationsarrays, gemeinsamer Updatezaehler | Channel-off-, One-way- und Reciprocal-Arm; Positionen und Formen beider Objekte | Kreuzgradienten aus beiden vollstaendigen Zustaenden vor dem Update. Keine distanzabhaengige Laufzeit und keine spezifizierten Messsettings. |

Quellbasis: [Paper-I-Regel](https://github.com/MemoryDynamics/Knoten/blob/0ef0bf2/paper/paper_i/manuscript/content.tex),
[FiniteMemoryState](https://github.com/MemoryDynamics/Knoten/blob/0ef0bf2/src/emergenz_knoten/state.py),
[Frozen Source](https://github.com/MemoryDynamics/Knoten/blob/0ef0bf2/src/emergenz_knoten/frozen_source.py)
und [direktes Paar](https://github.com/MemoryDynamics/Knoten/blob/0ef0bf2/src/emergenz_knoten/reciprocal_nodes.py).
Das direkte Paar ist nicht der konstruierte P5-D-Center-Port. Dessen
geschlossene Ausfuehrung bleibt unberuehrt.

## Expliziter Frozen-Source-Vertrag

Das Ziel hat Position $x_n$, geordnete Memory-Zentren
$Y_n=(y_{n,0},\ldots,y_{n,H-1})$ und feste Altersgewichte $w_j^T$.
Die vorbereitete Quelle besteht aus Zentren $s_j$ und Gewichten $w_j^S$.
Ihre Verschiebung $u$ wird vor dem Puls gewaehlt und bleibt waehrend des
Laufs fest; die API implementiert keinen autonom bewegten Quellenaktuator.
Parameter, Quellengeometrie und Pulszaehler gehoeren zum augmentierten
Zustand. Die analytische Gegenueberstellung haelt den anfaenglichen
Zielzustand und alle Parameter fest.

`FiniteMemoryState` akzeptiert allgemeine nichtnegative Gewichte positiver
Gesamtmasse. Exponentielle Altersgewichte und die Konsistenz mit der
Paper-I-Praeparation muessen vom Aufrufer sichergestellt werden; die
Fortsetzungs-API erzwingt sie nicht. Die folgenden Formeln gelten fuer die
bereitgestellten festen Gewichte, ohne sie neu zu normalisieren.

Mit $b_n=1$ fuer $0\leq n<N_{\rm pulse}$, sonst $b_n=0$, lautet der
deterministische Anteil des naechsten Positionsschritts

$$
f_u(Z_n)=x_n
-\eta_T\sum_j w_j^T\nabla K_T^{\rm eff}(x_n-y_{n,j})
-b_n\eta_\times\sum_j w_j^S\nabla K_\times^{\rm eff}(x_n-s_j-u).
$$

Die effektiven Kernel enthalten die jeweils deklarierte
Depositionsfaltung. **Zuerst** werden beide Gradienten aus dem alten Zustand
gelesen, **danach** folgen Position und FIFO-Write:

$$
x_{n+1}=f_u(Z_n)+\varepsilon_T\xi_n,
\qquad
Y_{n+1}=(x_{n+1},y_{n,0},\ldots,y_{n,H-2}).
$$

Die Quelle wird nicht fortgeschrieben. Die ausgegebenen Memory-Zentren und
Formtensoren werden nach dem Write aus den gespeicherten Zentren berechnet;
sie sind keine separat evolvierenden Freiheitsgrade.

**Bedingte Wahrscheinlichkeiten:** Unter der expliziten Modellannahme
$\xi_n\sim\mathcal N(0,I_d)$, unabhaengig von bisherigem Zustand und
Quellenwahl, gilt bei $\varepsilon_T>0$

$$
x_{n+1}\mid Z_n,u\sim
\mathcal N\bigl(f_u(Z_n),\varepsilon_T^2I_d\bigr).
$$

Bei $\varepsilon_T=0$ ist dies eine Punktmasse; der restliche
Zustandsuebergang ist in beiden Faellen durch den FIFO-Write bestimmt.
Die API selbst prueft nur Form und Endlichkeit des gelieferten Noise-Arrays,
nicht dessen Verteilung oder Unabhaengigkeit. Bei vorgegebenem Array ist die
Fortsetzung deterministisch. Diese Unterscheidung gehoert zum Vertrag.

## Antwort und unterscheidbare Verteilungen

Fuer eine Quellenverschiebung $u=s v$ bei festem Ausgangszustand und gleicher
Innovation in den Vergleichsarmen ergibt sich

$$
J_1v=\left.\frac{\partial x_1}{\partial s}\right|_{s=0}
=\eta_\times\sum_j w_j^S\nabla^2K_\times^{\rm eff}(x_0-s_j)v.
$$

Das Vorzeichen ist positiv: Die Ableitung nach der Quellenposition und das
Minuszeichen des Drifts heben sich auf. Die Selbstkraft bleibt beim ersten
Schritt gleich. Fuer das normierte Memory-Zentrum ist die Antwort nach dem
Write genau $w_0^T/(\sum_j w_j^T)$ mal $J_1v$.

Ein nichtverschwindendes $J_1v$ impliziert fuer hinreichend kleine
Quellenvariationen unterschiedliche bedingte Mittelwerte. Bei gleichem
Gaussrauschen sind damit auch die Positionsverteilungen verschieden.
Eine Projektion entlang ihrer Mittelwertdifferenz mit einer Schwelle
zwischen beiden Mitteln unterscheidet ihre Wahrscheinlichkeiten. Das ist
eine mathematische Auswertung des vorhandenen Positionsreadouts, keine
abgeleitete Theorie physikalischer Messgeraete.

Der direkte Kanal ist daher **unter diesen zugelassenen Quellen- und
Positionsoperationen** kein nichtsignalisierender Kanal. Daraus folgt keine
physikalisch nutzbare Ueberlichtkommunikation: Die initiale Quellenvariation
ist noch kein dynamischer lokaler Aktuator, und Raumzeitzuordnung, Aufloesung
und raumartige Trennung sind nicht definiert. Der nichtkompakte Kernel
allein liefert weiterhin keinen harten Kausalrand; effektive Lokalitaet
verlangt eine separate, fehlerkontrollierte Skalenanalyse.

Zwei wichtige Kontrollen verhindern eine falsche Interpretation:

- `paired_frozen_source_response` haelt das Ziel anfangs gleich und
  verschiebt nur die Quelle. Dagegen platziert `initial_center_separation`
  im reziproken Paar **beide** Objekte symmetrisch um ihren gemeinsamen
  Mittelpunkt. Ein Scan dieses Parameters ist keine reine Fernintervention
  an einem sonst identischen Ziel.
- Gemeinsame Zufallszahlen in den Vergleichsarmen entfernen die additive
  Innovation aus der Ein-Schritt-Differenz. Nach weiteren Schritten kann
  die Antwort ueber die nichtlinearen Bahnen vom Noise abhaengen. Die
  numerische Kopplung der Arme ist Varianzreduktion, kein Nachweis von
  Verschraenkung oder vier gleichzeitig messbaren Bell-Ergebnissen.

## Was das fuer den Quantenpfad bedeutet

Unter der expliziten Annahme unabhaengiger Innovationen, auch unabhaengig
vom alten Zustand und den Eingriffen, liefern zwei direkt gekoppelte
Objekte bei festen Eingriffen und bedingt auf ihren vollstaendigen alten
Zustand eine Produktverteilung der neuen Positionen. Dies ist nicht
automatisch Bell-Lokalitaet. Wenn ein lokal
gewaehlter Eingriff den aktuellen Kreuzgradienten veraendert, kann der
Mittelwert am anderen Objekt von dieser Einstellung abhaengen. Das Produkt
hat dann Faktoren der Form $p_A(\cdot\mid Z,a,b)$ und
$p_B(\cdot\mid Z,a,b)$ statt der benoetigten lokalen Abhaengigkeiten.
Die gegenwaertige Paar-API definiert solche unabhaengigen Einstellungen
$a,b$ noch nicht; hier wird nur die Verwechslung der beiden
Faktorisierungsbegriffe ausgeschlossen.

Umgekehrt ist eine gemeinsam vorbereitete, korrelierte Memory allein kein
Ausweg aus der lokalen CHSH-Schranke: Sie gehoert in den klassischen
Zustand **vor** der aktuellen Messwahl. Wenn nach dieser Wahl ausschliesslich
lokale Antwortfunktionen wirken und die Wahl unabhaengig ist, bleibt das
Argument aus [R0](foundation_feasibility.md#d-gedaechtnis-und-quantenkorrelationen)
anwendbar. Die zwischen Versuchen gespeicherte Vergangenheit aendert diese
bedingte Schranke nicht; siehe [Gill, Abschnitte 2--4](https://arxiv.org/pdf/quant-ph/0301059v2).
Weder gemeinsame Praeparation noch unabhaengiges Rauschen entscheiden die
Frage ohne den expliziten Informationszugriff nach der Messwahl.

## Abnahme und naechste Entscheidung

Die fuenf neuen synthetischen Ein-Schritt-Checks in den
[Frozen-Source-Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_frozen_source.py)
vergleichen Drift und Hesse-Antwort bei zwei Abstaenden, jeweils mit und
ohne Kreuzkopplung, pruefen das initial unveraenderte Ziel und die
Write-/Read-Reihenfolge sowie den Einfluss gemeinsamer Innovationen.
Sie verwenden keine Orbitkandidaten, Produktionscheckpoints oder Gate-Ziele.
Sie pruefen die Implementierungszuordnung, nicht die physikalische
Realisierbarkeit der zugelassenen Operationen.
Die 28 Tests fuer Frozen Source, direktes Paar und R0 sowie 14
Dokumentations-/Claim-Checks bestehen lokal mit NumPy 2.3.5, SciPy 1.16.3
und pytest 8.4.2. Ruff und der strikte Dokumentationsbuild bestehen ebenfalls.

**B1-Befund:** Klassische Uebergangsregel und Antwort sind fuer den genannten
Zweig spezifiziert. Welches Mehrsystemgesetz physikalisch gemeint ist und
wie Praeparation, Eingriff und Messung daraus folgen, bleibt unbestimmt.
Das ist ein konkreter Blocker einer gemeinsamen II-/III-Deutung, kein
Fehlen jeglicher mathematisch definierter Paarkopplung. B1 ist damit als
Bestandsanalyse abgeschlossen, nicht als Nachweis einer tragfaehigen
fundamentalen Architektur.

Die naechste Richtungsentscheidung betrifft den fundamentalen Pfad: Sollen
Teilsysteme und Messoperationen aus der unveraenderten Regel hergeleitet,
eine vorhandene Erweiterung explizit als physikalisches Modell gesetzt
oder neue mikroskopische Regeln erwogen werden? Fuer jeden Pfad sind
fehlende Herleitungen, Zusatzannahmen und erste Gegenpruefungen zu nennen;
keine neue Regel wird hier eingefuehrt. Der klassische Publikationsstrang
und die Neuheitspruefung fuer Paper I bleiben davon unabhaengig. Die
Arbeitsreihenfolge bleibt allein in den
[Projektprioritaeten](../status/project_priorities.md).
