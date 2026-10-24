# Entscheidung nach R0/B1

Stand: 2026-10-21, Grundlage `f3f892f`. Entscheidungsvorlage, keine
Modellfreigabe und keine neue Physikevidenz. Die aktive Arbeitsfolge steht
in den [Projektprioritaeten](project_priorities.md).

## Entscheidung in einem Satz

**Empfehlung:** Die bestehende Mikrodynamik vorerst unveraendert lassen,
Paper I als eigenstaendige klassische Arbeit weiterpruefen und fuer den
fundamentalen Pfad zuerst festlegen, welche Teilsysteme und Messoperationen
aus dieser Regel folgen sollen. Neue Felder oder Quantenpostulate nur nach
einer ausdruecklichen Autorenentscheidung einfuehren. Dies ist die
annahmensparsame Arbeitswahl, keine Aussage ueber die Erfolgschance.

[R0](../reference/foundation_feasibility.md) und
[B1](../reference/operational_contract.md) haben keine Route zum
Standardmodell oder zur Gravitation nachgewiesen. Sie zeigen aber, welche
Abkuerzungen nicht tragen. Der klassische Publikationsstrang und die
fundamentale Forschungsfrage koennen parallel bestehen; ein negatives
Ergebnis auf einem Pfad entscheidet nicht automatisch den anderen.

## Drei unterschiedliche Wege

| Weg | Was bleibt / kommt hinzu? | Erstes entscheidendes Ergebnis | Gegenbefund und Konsequenz |
| --- | --- | --- | --- |
| A: bestehende Regel ausschoepfen | Einzelprozess, skalare Memory, vorhandene Geometrie und Noise bleiben Inputs. Keine neue Kreuzkopplung, Messregel oder Feldgleichung. | Eine konkrete Abbildung des vollen Zustands auf zwei Teilsysteme, deren Praeparation, Einstellungen und Readouts; Informationszugriff nach der Messwahl explizit. Dieselbe Regel muss diese Beschreibung tragen. | Fehlt die Abbildung, bleibt die II-/III-Deutung unbestimmt. Ist sie Bell-lokal bei unabhaengiger Messwahl, kann sie die betreffenden Quantenkorrelationen nicht liefern. Das beendet diesen Anspruch fuer die betreffende Abbildung, nicht alle klassischen Anwendungen oder jede denkbare andere Abbildung. |
| B: klassisches Mehrsystem-/Feldmodell setzen | Eine vorhandene Paarkopplung wird explizit als physikalische Regel gewaehlt, oder ein neues dynamisches Feld mit Quellen, Rueckwirkung und Anfangsdaten wird hinzugefuegt. | Vor einem Lauf die vollstaendige Antwort aller Uebertragungskanaele ableiten: direkter Zugriff, Feld, bewegte Traeger, Updatezeit. Einen behaupteten Kausalbereich samt Fehlerkontrolle und Bilanzen pruefen. | Direkte Gaussantwort und das vorhandene Relaxations-Diffusionsfeld tragen keinen harten Signalkegel. Ein lokal-kausaler klassischer Vertrag loest unter den Bell-Voraussetzungen weiterhin nicht die Quantenfrage. Keine Gleichsetzung eines Propagationspasses mit einer gemeinsamen fundamentalen Theorie. |
| C: Quantenstruktur voraussetzen | Hilbertraum, Zustaende, Messregel und quantenmechanische Zeitentwicklung werden Inputs statt abgeleitete Ergebnisse. | Ein wohldefiniertes Modell und ein kontrollierter Bezug zur klassischen Memory-Dynamik, ohne ihre Koeffizienten nur nachtraeglich zu fitten. | Eine eingefuehrte Born-Regel ist keine emergente Born-Regel. Ein funktionierendes Quantenspielzeug liefert weder Gravitation noch das chirale Standardmodell. Die Herkunft der Quantenmechanik waere nicht mehr Ergebnis dieses Programms. |

Bei A ist Bell-Lokalitaet gesondert zu pruefen: Der vorhandene direkte
Readout kann von entfernten Eingriffen abhaengen. Eine Beschreibung, die
solche Eingriffe zulaesst, muss beobachtbares Nicht-Signalisieren und die
richtige Korrelationsstruktur erklaeren. Eine hohe CHSH-Zahl allein
genuegt nicht. Auch abweichende
Annahmen zur Messwahl oder Zeitordnung waeren offen zu deklarieren, nicht
als automatisch durch Memory geloest zu behandeln.

## Zwei analytische Grenzen

**Coarse-graining beseitigt eine lokale Schranke nicht.** Fuer lokale
Auswertungen einer bereits Bell-lokalen Beschreibung gilt beispielsweise

$$
p(A\mid a,\lambda)
=\int M_A(A\mid a,z_A)\,p(dz_A\mid a,\lambda),
$$

analog fuer B. Normierte lokale Auswertungskerne liefern wieder lokale
Antwortwahrscheinlichkeiten. Bei messwahlunabhaengiger Verteilung des
vollstaendigen Zustands $\lambda$ bleibt das R0-CHSH-Argument anwendbar.
Ein Symmetriequotient, eine reduzierte Dimension oder eine verborgene
Historie allein aendert diese Voraussetzung nicht. Setting-/outcome-
abhaengige Auswahl von Versuchen ist keine solche normierte lokale
Auswertung aller Versuche und darf nicht stillschweigend eingefuehrt werden.
Der Memory-Aspekt ist auch Gegenstand von
[Gill, Abschnitte 2--4](https://arxiv.org/pdf/quant-ph/0301059v2).

**Ein lokaler Differentialoperator ist noch kein harter Kausalrand.** Die
bereits untersuchte Gleichung
$\tau\partial_t\phi=D\Delta\phi-\mu\phi+g\rho$
hat fuer eine Raumzeit-Punktquelle auf $\mathbb R^d$, $D,\tau,g>0$ und
verschwindendes Anfangsfeld die retardierte Antwort

$$
G(x,t)=\frac{g}{\tau}\,e^{-\mu t/\tau}
\left(\frac{4\pi Dt}{\tau}\right)^{-d/2}
\exp\!\left(-\frac{\tau |x|^2}{4Dt}\right),\qquad t>0.
$$

Sie ist fuer jedes endliche $x$ und jedes $t>0$ positiv. Raeumlich lokal
und zeitlich retardiert bedeutet hier deshalb nicht endliche
Ausbreitungsgeschwindigkeit. Eine hyperbolische Erweiterung waere eine
neue Dynamik mit zusaetzlichen Voraussetzungen; auch sie muesste alle
anderen Uebertragungskanaele beruecksichtigen. Eine kontrollierte effektive
Kausalstruktur ist eine andere, noch offene Frage.

Der [Feld-Audit vom Juli](https://github.com/MemoryDynamics/Knoten/blob/f3f892f/reports/kernels/field/field_equation_bridge_2026-07-18.md)
trennt bereits die Hilfskoordinate der Gaussglaettung von physikalischer
Zeit. Der [Write-/Read-Audit](https://github.com/MemoryDynamics/Knoten/blob/f3f892f/reports/kernels/field/write_read_reparameterization_audit_2026-07-30.md)
zeigt eine exakte lineare Umparametrisierung, keine neue Felddynamik.
Diese alten Befunde werden hier eingeordnet, nicht als neue Ergebnisse
oder aktuelle Ausfuehrungsfreigaben ausgegeben.

## Literaturgrenzen und Auftrag

[Levin und Wen](https://arxiv.org/abs/cond-mat/0404617v2) geben ein
Vorbild fuer emergente Eichbosonen und Fermionen aus bereits
quantenmechanischen Modellen, nicht fuer die Herleitung von Quantenmechanik
aus unserer skalaren Memory. Die im R0-Audit geprueften Hilbertraum- und
Hamiltonannahmen bleiben Inputs. Das ist ein Vergleichspunkt fuer C, keine
Begruendung, C hier automatisch zu waehlen.

[Wallstroms Verlagsabstract](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.49.1613)
warnt vor der Gleichsetzung einer hydrodynamischen Umformulierung mit der
vollen Schroedinger-Theorie ohne zusaetzliche Quantisierungsbedingung.
Geprueft ist hier der Abstract, nicht der Volltext; daraus wird kein
allgemeines Verbot stochastischer Quantenansaetze abgeleitet. Beide
Primaerquellen wurden am 2026-10-21 erneut kontrolliert.

**Autorentscheidung:** A als begrenzten Herleitungsversuch fortsetzen,
B als explizite klassische Erweiterung zulassen oder C als geaenderten
Ausgangspunkt untersuchen? Keine Option ist bereits als Weg zum Fernziel
validiert. Bis zur Entscheidung werden keine neuen Modellregeln gesetzt.
Die Literatur- und Gueltigkeitspruefung von Paper I bleibt bearbeitbar.
Keine neue FIFO-/P5-Autorisierung, keine Zieloptimierung und kein Zusammenlegen
der Paper, um fehlende Neuheit zu verdecken.
