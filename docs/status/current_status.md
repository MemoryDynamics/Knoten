# Aktueller Stand

Stand: 2026-10-26 (H=1200-Kreis normal linear instabil: exakter Vorzeichenbeleg aus Archivkoeffizienten; alte Schur-Pruefung unentschieden; Paper-I-Neuheit weiter offen).

Diese Seite berichtet nur den gegenwaertigen Befund. Die Arbeitsreihenfolge
steht ausschliesslich in den [Projektprioritaeten](project_priorities.md); der
vollstaendige vorherige Stand liegt im
[Repository-Archiv](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/current_status_through_2026-09-02.md).

## Evidenz

Die [Forschungsroadmap](research_roadmap.md) trennt das langfristige Ziel
von den offenen Verbindungen zu effektiver Dynamik, Quantenmechanik und
Gravitation. Der begrenzte [R0-Audit](../reference/foundation_feasibility.md)
ist dokumentiert: raeumliche Kreisphase, nichtkompakter direkter Gauss-Readout
und bedingte klassische Korrelationsgrenzen. Zwoelf synthetische Checks
pruefen die engen Aussagen und Gegenbeispiele gegen Ueberinterpretation.
Das ist kein allgemeines Go oder No-go fuer das Fernziel und keine neue
Produktions- oder FIFO-/P5-Evidenz. Die
[B1-Bestandsanalyse](../reference/operational_contract.md) spezifiziert
Zustand, Quellenvariation, Ein-Schritt-Antwort und bedingte Verteilung des
vorhandenen Frozen-Source-Zweigs. Fuenf neue synthetische Checks pruefen
seine Zuordnung zur Implementierung. Ein physikalischer Zwei-Stationen-
Vertrag mit begruendeter Wahl oder Herleitung des Mehrsystemgesetzes,
Aktuatoren und Detektoren fehlt weiter. Mathematisch definierte Paarkopplungen
existieren; ihre physikalische Auswahl folgt nicht aus dem analytischen Abschluss.

Die [FIFO-Strukturanalyse](../reference/fifo_structure_candidate.md)
identifiziert als begrenzten Arbeitskandidaten eine altersgeordnete
Memory-Schleife mit abgeleitetem Orientierungsrahmen. In gewaehltem 3D
sind die beiden ebenen Drehsinne durch eigentliche Rotation verbunden;
die $\mathbb Z_2$-Wegklassen des nichtentarteten Rahmenbereichs sind keine
zwei Teilchentypen. Im vollen FIFO-Raum laesst sich die Rotationsschleife
ueber erlaubte Rahmenentartungen kontrahieren. Ein separat hergeleiteter
Normalblock macht die gesondert zu pruefende Stabilitaet gegen Auslenkungen aus
der Ebene explizit. 26 kleine synthetische Checks bestehen, einschliesslich
einer kollapsfreien Kontraktion der Rahmenrotation in 4D. Diese synthetischen
Checks sind keine Zielmessung, geschuetzte topologische Ladung oder Wechselwirkungsidentifikation.

Der anschliessende
[Normalstabilitaets-Methodenvertrag](../reference/fifo_normal_stability_contract.md)
reduziert die offene lineare Frage auf den vollstaendigen Formquotienten
nach genau drei normalen Symmetriemoden. Ein Intervallprototyp der bekannten
Schur-Rekursion unterscheidet strikte Stabilitaet, Nicht-Striktheit und
Unentschiedenheit an synthetischen Kontrollen. Zusatzmoden nahe eins bleiben
erhalten; transiente Verstaerkung bleibt von asymptotischem Abklingen
getrennt. Die Rootbox-Anbindung ist jetzt mit frischer Krawczyk-Pruefung
und direkter Weitergabe binaerer Intervallgrenzen implementiert. 23 neue
Kontrollen umfassen konstruierte H=4-Roots mit abklingender und wachsender
Normalmode sowie den Produktionskernel. Der begrenzte H=1200-Ankertest
wurde nach ausdruecklicher Autorenfreigabe samt festen schraegen Stoerungen
einmalig ausgefuehrt. Die
[Auswertung mit Kurven und Rohdaten](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/analysis.md)
trennt zwei Ergebnisse: Beide frischen Rootzertifikate bestehen, aber die
80-/120-dps-Normaltests bleiben durch Intervallaufweitung unentschieden.
Die zehn float64-Arme ueber 2000 Updates zeigen Abklingen bei 0 Grad
(Endfaktor etwa 0.000462) und starke Formverstaerkung bei 30/45/60/90 Grad
(Endfaktoren etwa 1206/1705/2087/2409). Die ungestoerte Form driftet nur
um maximal abgetastet 2.09e-15. Das ist ein deutlicher begrenzter
Wachstumsbefund, noch kein asymptotischer Instabilitaetsbeweis und kein
allgemeiner 3D-Stabilitaetspass. Es gab keinen Timeout oder weiteren Versuch.
Vor Ausfuehrung bestanden 229 betroffene lokale Regressionstests,
einschliesslich 56 Runner-/Stoerungskontrollen, Lint, strikter
Dokumentationsbau und die vollstaendige GitHub-CI. Diese Softwaretests
enthalten selbst keine Zielauswertung. Die Versuchsgenehmigung ist verbraucht.

Die danach separat angeforderte
[120-Grad-Symmetriekontrolle](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25/report.md)
ist ebenfalls abgeschlossen. Beide neuen 120-Grad-Arme stimmen mit den
gespeicherten 60-Grad-Armen bei entgegengesetztem Gesamtvorzeichen an
allen 201 Abtastpunkten ueberein; die groesste absolute Formdistanzdifferenz
betraegt etwa 1.01e-16. Das plausibilisiert Code und Modellsymmetrie, nicht
allgemeine Stabilitaet oder reale Physik. Kein weiterer Normalzertifikatslauf.

Abschnitt 6 des [Methodenvertrags](../reference/fifo_normal_stability_contract.md)
enthaelt nun einen elementaren hinreichenden Vorzeichenbeleg fuer eine
reelle wachsende Normalmode, samt 20 synthetischen Gegenkontrollen.
Die danach separat freigegebene
[Archivauswertung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26/report.md)
belegt jetzt in beiden 80-/120-dps-Datensaetzen strikt
$S\approx-0.3276456990433840337505836<0$ mit ueberlappenden exakten
rationalen Intervallen. Damit existiert am unveraenderten H=1200-Kreis
eine reelle Normalformmode mit Multiplikator groesser als eins. Dieser
Kreis ist kein linear stabiler 3D-Baustein. Der Beleg uebernimmt die
urspruengliche Root-/Koeffizienten-Vertrauensbasis; es gab keine neue
Simulation oder Rootrechnung. Je ein Lauf dauerte 1.531/1.516 Sekunden;
198 lokale Tests, Lint und Dokumentationsbau bestanden vor Ausfuehrung.
Keine Wiederholung, Freigabe verbraucht. Andere FIFO-Strukturen und die
nichtlineare Folgeentwicklung sind dadurch nicht entschieden.

Eine getrennte [Paper-I-Forschungsnotiz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_memory_stationarity_2026-10-21.md)
begruendet fuer festes endliches $H$ und positives Gaussrauschen eine
eindeutige relative stationaere Verteilung des beschraenkten nichtlinearen
Drifts. Die Schranke ist nicht uniform fuer verschwindendes Rauschen oder
wachsenden Horizont. Ein exaktes Zweierzyklus-Gegenbeispiel verhindert,
lokale Stabilitaet mit globaler Branch-Selektion gleichzusetzen. Dies sind
analytische Forschungsbefunde, keine neue Radius- oder Transportevidenz.
Eine Ergaenzung derselben Notiz nutzt positive Mittelung, um stationaere
quadratische Momente bis Ordnung $\varepsilon^4$ mit Rest
$O(\varepsilon^6)$ bei festem endlichem $H$ zu begruenden. Alle archivierten
Modellkoeffizienten erfuellen diese zusaetzlichen Voraussetzungen; die
enormen Fehlerkonstanten bestaetigen weder das vorhandene endliche Rauschen
noch praktische Durchmischung, Transport oder den unendlichen Horizont.
Die anschliessende
[Kontraktionsnotiz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/weak_noise_validity_2026-10-21.md)
begruendet die stationaere Momententwicklung unter einer strengeren
globalen Bedingung auch fuer ungekuerztes exponentielles Gedaechtnis.
Alle aktiven archivierten Zellen liegen ausserhalb dieses hinreichenden
Bereichs; das beweist keine Instabilitaet. Ein zusaetzlicher summierbarer
Restterm begruendet nun auch die nichtlineare Transportkorrektur in diesem
engen Bereich, einschliesslich eines expliziten ungekuerzten Koeffizienten.
Numerische Transportvalidierung, Publikationsneuheit, die allgemeine
Gueltigkeit und der separate FIFO-Horizonttransfer bleiben offen.

Update 2026-10-22: Ein externes Zweitmodellreview hat einen konkreten
Transporttest vorgeschlagen. Der
[reproduzierbare Gegencheck](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/external_review_audit_2026-10-22.md)
bestaetigt dessen unendliche Koeffizienten, nicht die Panelreife:
Block-MSD bei Lag 100 und Langzeittransport sind verschieden; der
lineare Bias betraegt 37.17%. Korrekte unabhaengige Gaussreferenz-Skalierung
ergibt etwa 2.32 statt 13.5 Standardabweichungen. Eine anschliessende
[gepaarte Referenzrechnung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_transport_feasibility_2026-10-22.md)
kontrolliert den fuehrenden Endlichzeitbias mit einer Zweilaengen-Korrektur
und berechnet die Langblock-Varianz inklusive kubischem Gauss-Chaos.
Die anschliessende
[finite-Stichproben-Rechnung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_block_transport_bound_2026-10-22.md)
begrenzt Sampling plus Blockbias fuer den fuehrenden Koeffizienten beim
diskutierten Budget auf einen konservativen relativen 95%-Radius unter
8.8%. Dies ist eine analytische Referenzrechnung in Gleitkommaarithmetik,
keine Daten-Konfidenz oder Fehlergarantie fuer endliches Rauschen.
Die [Fortsetzung vom 2026-10-23](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_noise_transport_budget_2026-10-23.md)
liefert explizite Schranken fuer zufaelligen Schaetzerrest, Transportrest
und einen vollstaendig vorgefuellten flachen Start. Ein illustratives
10%-Gesamtbudget bei 95% Ueberdeckung ist in exakter Arithmetik fuer einen
sehr kleinen Rauschbereich hinreichend kontrolliert. Am oberen Rand
$\varepsilon\simeq4.46\,10^{-6}$ betraegt der fuehrende Kontrast nur
etwa $9.54\,10^{-10}$ des linearen Beitrags. Die Gleitkommaauswertung
ist kein Intervallzertifikat und bestaetigt weder die fruehere Rauschwahl
$0.007$ noch den bisherigen leeren Speicherstart. Die numerische
Differenzdarstellung wurde anschliessend als
[exakte skalierte Restrekursion](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_residual_precision_2026-10-23.md)
geprueft: Kleine deterministische Historien und ein H=600-Ein-Schritt-Test
stimmen mit direkten 80-/110-stelligen Vollkraftrechnungen ueberein.
Das ist keine Langlaufgarantie. Der reine Referenz-Mikrobenchmark misst
etwa 0.261 ms pro Paarupdate; naive serielle Hochrechnung ergibt rund
145 Stunden fuer die diskutierte Paarzahl, ohne RNG/Statistik/I/O.
Die [bedingte Fehlerfortpflanzung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_error_propagation_2026-10-23.md)
liefert inzwischen zeituniforme Zustandsschranken fuer vorgegebene lokale
Defekte und Laggrenzen sowie eine separat begrenzte skalare Mittelung.
Die benoetigten lokalen Fehlergrenzen des Simulators und dessen gesamte
Statistik-/Innovationsschnittstelle bleiben unvalidiert. Eine
[Entscheidungsvorlage fuer die fachliche Diskussion](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paper_i_decision_brief_2026-10-23.md)
fasst Resultatkandidat, Literaturabgrenzung und Aufwand zusammen. Sie ist
kein Fachreview und wurde nicht versendet. Praktische Kostenentscheidung,
Neuheitsvergleich und unabhaengiges Fachreview bleiben offen. Keine neue
Zielsimulation oder Panelautorisierung.

Der [Neuheits-Gegencheck vom 2026-10-24](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/gaussian_projection_audit_2026-10-24.md)
zeigt nun eine konkrete Identitaet: Bekannte statistische Linearisierung
reproduziert den gesamten ersten nichtlinearen Transportkoeffizienten.
Ein kubischer Rest mit nichtverschwindender Varianz bleibt dabei erhalten;
dies ist keine exakte lineare Reduktion und kein Nachweis einer gaussverteilten
nichtlinearen stationaeren Dynamik. Der moegliche
Publikationsbeitrag liegt damit in der kontrollierten Gueltigkeit, deren
Abgrenzung gegen rigorose Naeherungstheorie offen bleibt. 32 neue
deterministische Integral-/Matrix-/Projektionschecks bestehen; keine
Zieltrajektorien oder neue Physikevidenz.

Der anschliessende [Satzvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/linear_response_scope_audit_2026-10-24.md)
weist eine direkte Totalvariations-Anwendung auf den vollen Historienraum
zurueck, ohne der vorhandenen metrischen Kontraktion zu widersprechen.
Die ergaenzte direkte Poissonrechnung kontrolliert nun intern die
konkreten Observablen, den Korrelations-Resolvent und den Transportrest
uniform im Horizont. Sie behauptet keinen allgemeinen Satzimport und
keine Erweiterung des Gueltigkeitsbereichs. 14 neue synthetische
Matrix-/Quadraturchecks bestaetigen die getrennten Verteilungs- und
Korrelationsbeitraege zum Koeffizienten. Dies staerkt die Einordnung als
Anwendung bekannter Methoden, nicht die Behauptung eines neuen Mechanismus.
Unabhaengige Beweispruefung und Publikationsbewertung bleiben offen.

Der gelieferte [Aging-Volltext](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/aging_full_text_comparison_2026-10-25.md)
ist nun auf Modellebene abgeglichen. Die ungekuerzte lineare Regel ist
nach Parameter- und Startzuordnung exakt das Euler-Schema des Preprints;
sein kontinuierlicher Transportkoeffizient folgt im passend skalierten
Zeitschrittgrenzwert. Zwanzig neue deterministische Checks pruefen diese
Zuordnung, Resolvent und Koeffizienten sowie konkrete Inkonsistenzen der
gelieferten Fassung. Der Preprint behandelt keine nichtlineare
Schwachrauschkorrektur. Das schliesst die Zugriffsluecke, nicht die breitere
Neuheitsfrage oder den fehlenden fundamentalen Anschluss.

| Bereich | Reviewed Befund | Belastbare Lesart |
| --- | --- | --- |
| Paper 0 | technischer Anker | mathematischer Ausgangspunkt |
| Paper I, skalar | kontrollierte co-moving Relaxationswolke; observable-gematchter terminaler RMS-Vergleich | reproduzierbare Baseline, noch nicht PRE-einreichungsreif; Wolkenradius: 0.076% mediane / 0.984% maximale aktive Abweichung, 85 Seed-Traces; Transportvorhersage nicht numerisch validiert, nichtlineare Neuheit offen |
| Native Rotation | sechs lokal eindeutige finite-$H$-Roots; G5 besteht direkte Root-, Spektral- und Nichtlinearitaetsgates bei $H=2400$ | lokale numerische Stabilitaet des vorbereiteten Orbits, keine globale Eindeutigkeit, $H\to\infty$-Stabilitaet oder generische Formation |
| P4-R-S | `p4rs-anchor-scale-transfer-pass` | Zwei-Zellen-Skalentransfer, keine Replikation |
| N0 | `n0-noise-stability-window-bracketed-reviewed-pass` | endliche numerische Robustheitsklammer, keine Planck-Kalibrierung |
| P5-D | `p5d-inconclusive`; drei eigene Produktionsaufrufe technisch verbraucht | keine Interaktionsevidenz; der separate G5-Pass ist ein Single-Loop-Stabilitaetsbefund und keine P5-D-Aussage |
| Source-Audit | `referee-source-ready-with-major-claim-restrictions` | publication source mit offenen Hardening-Auflagen |

## Was der Kreisnachweis genau sagt

Fuer den Anchor mit
`alpha=0.01`, `H=1200`, `eta=0.15`, `A_att=3.5` reduziert das Einsetzen von
$x_n=R e^{in\theta}$ die unveraenderte Grundgleichung exakt auf zwei endliche
Balancesummen. Ein prospektiver Krawczyk-Test schliesst in seinem registrierten
lokalen Kasten genau einen Root ein. Die direkte 2400-dimensionale
mitrotierende Voll-FIFO-Map reproduziert die vorbereitete Historie mit
maximalem Komponentenfehler $2.46\times10^{-15}$; lokale Stoerungen
kontrahieren numerisch. Am spaeteren L3-Kandidaten erreichen zudem zehn
registrierte nichtkreisfoermige Arme den zugehoerigen Orbit.

Fuer diesen vorbereiteten Rotating-wave-FIFO wurde kein KnotScore erhoben.
Das ist derzeit keine fehlende Erfolgszahl: KnotScore v0.5/v0.6 bewertet
kontrollierte Metastabilitaet, Residence und Shape-Stationaritaet, waehrend
Root-, Stabilitaets- und Attraction-Panels eine vorbereitete Kreisloesung
testen. Eine zulaessige gemeinsame Score-/Formationauswertung braeuchte
deshalb ein eigenes prospektives Design mit `eta_zero`-Kontrolle; die
Einordnung steht im
[Experimentkatalog](../reference/experiment_catalog.md).

Das ist der fuer P5 benoetigte kandidatenbezogene Existenz- und
Identitaetsnachweis. Es ist kein globaler Einzigkeitsbeweis: $+\theta$ und
$-\theta$ sind Chiralitaetspartner, globale Rotationen parametrisieren
dieselbe ambiente $SO(2)$-Gruppenbahn, und weitere entfernte Roots sind nicht
ausgeschlossen. P5 darf deshalb einen fest registrierten Kreis als Input
verwenden, aber nicht behaupten, die Parameter erzeugten global nur einen
Kreis.

Der FIFO ist dabei nur eine endliche Alterswarteschlange und schreibt keine
raeumliche Ringtopologie vor. Krawczyk-Balancen, der kollabierende
$\eta=0$-Arm und zehn anziehende nichtkreisfoermige P3-Historien widerlegen
die enge Ringspeicher-Tautologie. Offen bleibt der staerkere Transfer: Die
registrierte Leiter haelt $H\alpha=12$ fest und zeigt nicht, dass Root und
Stabilitaet bei festem $\alpha$ den Grenzfall $H\to\infty$ erreichen. Deshalb
steht vor einer neuen P5-Zielautorisierung ein separates Horizontgate.

Dieses Gate ist inzwischen prospektiv spezifiziert. Es haelt
$\alpha=0.01$, $\eta=0.15$, $M_0$, Kernel und $\varepsilon=0$ fest, trennt
die Vorwaertsleiter bis $H=3600$ von der unteren $H=900,600$-Belastung und
fordert einen Tail-Krawczyk-Einschluss fuer den lokalen Root von
$F_\infty$. Ein negatives Review fand sechs Luecken einschliesslich eines
konstruktiv falschen binary64-Vergleichs; die Amendierung schliesst sie. Das
Suffizienzurteil lautet
`rotating-wave-horizon-transfer-protocol-sufficient-implementation-closed`.
Ergebnisvertrag und rote targetfreie Tests wurden danach getrennt committed;
die kleinste Infrastruktur bestand 40 fokussierte und 985 gesamte Tests. Das
Infrastruktururteil lautet
`rotating-wave-horizon-transfer-contract-infrastructure-pass-runner-incomplete-horizon-run-closed`.
Ein nachfolgendes Negativreview zeigte, dass v1 mehrere registrierte
Abbruchpfade nicht wahrheitsgetreu serialisieren konnte; v2 schloss diese
Nullsemantik. Ein weiteres Negativreview zeigte jedoch, dass positive
Zertifikats-, Spektral- und Trajektorienbeziehungen noch nicht vollstaendig
rekonstruierbar waren. v3 schliesst diese Luecken. Eine erste Linux-CI
falsifizierte dabei native `sin`-/`cos`-Starts als plattformunabhaengig; die
vor jedem Zielzugriff amendierte portable LCG-Konstruktion besteht 59
fokussierte und 1004 gesamte Tests sowie die exakte Linux-CI. Das
Reviewurteil ist
`rotating-wave-horizon-transfer-contract-v3-pass-runner-red-open-target-closed`.
Die anschliessende pure Orchestrierung bestand ihre Stopptests. Ein neuer
Counterexample zeigte jedoch, dass ein einzelnes ausgeschlossenes Halbblatt
als vollstaendige lokale Ausschlussdomain akzeptiert wurde. Validator und
Auditor rekonstruieren deshalb nun unabhaengig Rootbindung, deterministische
dyadische Leafpfade, Praefixfreiheit und vollstaendige Bedeckung. Eine
vollstaendige Ausschlusspartition bei gleichzeitig zertifiziertem Zielroot
wird als Widerspruch verworfen. 70 fokussierte und 1015 gesamte Tests sowie
die exakte Linux-CI sind gruen. Der anschliessende Backend-Bestandsaudit
korrigiert die pauschale Fehlstellenbeschreibung: finite Residuen/Jacobians,
Punkt-Newton, lokale Krawczyk-Boxen sowie FIFO-Map/Jacobian und
Quotientdistanz sind als Bibliothekskerne vorhanden. Der finite-Rootadapter
nutzt den bestehenden Acht-Schritt-Newton-/Krawczyk-Kern. Der anschliessende
Homotopieadapter erweitert denselben Intervallkern auf volle geschlossene
Parameterscheiben und erzwingt 64 Scheiben, strikten Einschluss,
Nachbarueberlappung sowie fail-closed Praefixstopps. Seine CI besteht 1029
Tests; keine registrierte Horizontkante wurde ausgewertet. Der lokale
Ausschlussadapter verwendet denselben Residual-/Krawczyk-Kern und bildet die
feste normalisierte FIFO-Teilung bis Tiefe 20 in den rekonstruierten v3-Record
ab. Er wurde nur an kontrollierten Antworten getestet; keine registrierte
Domain ist ausgeschlossen oder als Rootdomain klassifiziert. Seine
FIFO-kuratierte Implementierungs-CI besteht 1038 Tests. Das anschliessende
Tailzertifikat erweitert das endliche Residuum und beide Jacobi-Spalten um
die registrierten analytischen Normbounds und verwendet danach denselben
outward-rounded Krawczyk-Kern. Null-Tail-Reproduktion, Intervallerweiterung,
Typfehler und Nichtinklusion sind targetfrei getestet. Das damalige
Reviewurteil lautete
`horizon-tail-krawczyk-adapter-target-free-pass-g4-unmeasured`: Zu diesem
Zeitpunkt war kein $H=3600$-Kandidat eingesetzt worden. Offen sind
LCG-Arnoldi, Trajektorienabbildung und Backendkomposition. Die explizite
Nutzerfreigabe vom 2026-09-13 zog einen isolierten G4-Komponentenlauf vor.
Nach gruenem Readiness-Commit und exakter CI startete dieser genau einmal,
brach aber bei der nachgeschalteten Recordvalidierung an einer unzulaessig
exakten Kontrolle der outward-gerundeten aeusseren Box ab. Der Codepfad
rief zuvor mindestens das erste Tailpanel auf; mangels publiziertem Record
ist weder Panelpass noch -fail verwertbar. Ergebnisartefakte und
unabhaengiger Ergebnisaudit entstanden nicht. Der Ausgang ist
`g4-experiment-invalid-outward-box-validation`, nicht G4-Fail.
Die Boxpruefung ist targetfrei auf garantierte Umschliessung plus eng
praezisionsgebundenen Serialisierungsueberschuss korrigiert. Der separat
preregistrierte Retry auf Commit `fb1cc7d` besteht anschliessend beide
strikten 120/160-dps-Tailpanels; ihre Krawczyk-Bilder ueberlappen. Der
Standardbibliothek-Auditor rekonstruiert alle acht Checks und urteilt
`g4-independent-audit-agrees`. Damit ist G4 als isolierte lokale
$F_\infty$-Komponente `pass`. Die G1--G3-Branchverbindung, der
vollstaendige Horizontlauf und P5-D bleiben nicht belegt.

Das anschliessende G4-zu-G5-Meta-Review bestaetigt diese enge Claimgrenze und
findet keinen neuen kritischen G4-Defekt. Die daraus abgeleiteten
LCG-Arnoldi- und Trajektorienadapter bestehen targetfrei: der LCG-Start wird
unveraendert an ARPACK weitergegeben, Ritzvektoren werden v3-konform
gespeichert, Fehler behalten Nullsuffixe, und Instabilitaet verlangt nun das
tatsaechlich gematchte Paar beider Panels. Fortsetzungen bleiben bis zu
vollstaendigen Residual-, Symmetrie-, Panel- und Hashchecks geschlossen.
Der anschliessende Grundgleichungs-Preflight bindet ausserdem $q$, $H$,
$M_0$, $\eta$, Depositionsgewicht, direkte Gewichtssumme, native
Kreiskovarianz, mitrotierenden Fixpunkt, Voll-Jacobian und Symmetrien an
einen kanonisch hashbaren Record. Er bestaetigt targetfrei die beabsichtigte
Architektur: Nur Arnoldi ist linearisiert; die Stoerungsarme iterieren die
nichtlineare Voll-FIFO-Grundgleichung. Nach zwei getrennten
Publikationsincidents schloss Attempt 3 die Recordluecke mit einer dichten
Vollschrittspur. Der einmalige Ziellauf besteht beide Arnoldi-Panels und alle
drei nichtlinearen Stoerungsarme; der unabhaengige Auditor rekonstruiert
Record, Entscheidung und Publikationshashes. Das Ergebnis lautet
`g5-local-direct-stability-pass` fuer exakt $H=2400$. Dies ist kein
Intervallbeweis des vollen Spektrums und keine Aussage ueber
$H\to\infty$, Formation oder Interaktion.

## P5-D Code-Review und Remediation

Das Review trennte eine algebraisch konsistente Center-/Port-Konstruktion von
einer nicht belastbaren Ergebnisstrecke. Es reproduzierte folgende Blocker:

- Der Provenienzguard akzeptiert den inzwischen geschlossenen Ast weiterhin.
- Off-Arme erzeugen konstruktiv nichtendliche Sentinelwerte.
- Endlichkeitspruefung und Auditor sind fuer unbekannte Skalartypen fail-open.
- Die behauptete atomare Ausgabe zweier Dateien ist nicht paarweise atomar.
- Der Renderer setzt Diagnostik auch dann voraus, wenn die Antwort als nicht
  verfuegbar registriert wurde.
- Das Modellvokabular kollidiert zwischen Paper-I-Deposition, Centerfilter,
  Portgroessen und Maschinenrundung; der kanonische Notationsvertrag ist
  deshalb Teil der Remediation.

Die Recovery-Autorisierung ist verbraucht. Inzwischen bildet ein getrackter
maschinenlesbarer Governancezustand diese Schliessung ab; der Runner prueft
ihn vor der alten Provenienzstrecke und vor jeder Arm-Auswertung. Die zweite
targetfreie Teilkorrektur verwendet `null` fuer die nicht anwendbare
Off-Arm-Mobilitaetsmetrik, lehnt unbekannte Typen fail-closed ab und rendert
eine unverfuegbare Antwort ohne Diagnostikzugriff. Das exakte v2-Payloadschema,
die Manifest-zuletzt-Publikation, eine unabhaengige Manifestpruefung sowie die
einmalige CI-/Commit-gebundene Lease sind targetfrei implementiert und
adversarial geprueft. Das separate Readinessreview endete nach 929 lokalen
Tests und gruener CI fuer den exakten Implementierungscommit mit
`p5d-runner-ready-target-still-closed`. Eine danach ausdruecklich und einmalig
autorisierte dritte Ausfuehrung berechnete Panel, Response und Klassifikation,
scheiterte jedoch vor JSON-Encoding am strikten v2-Typvertrag: Die
Channel-off-Energieskala `numpy.finfo(float).tiny` wandelte sechs native
Nullquotienten in `numpy.float64` um. Receipt 3 existiert, Ergebnis, Report,
Manifest und Audit nicht. Damit ist auch dieser Lauf `p5d-inconclusive`, die
Readiness-Abdeckung falsifiziert und die Einmalfreigabe verbraucht. P5 bleibt
geschlossen.

Das danach getrennt geschriebene Produktionspfad-Protokoll wurde in einem
ersten Review wegen sechs Spezifikationsluecken abgelehnt, anschliessend
amendiert und im separaten Suffizienzreview als
`p5d-production-preflight-protocol-sufficient-target-closed` bewertet. Die
Amendierung friert neben drei wissenschaftlichen Quell-Blobs 41
wissenschaftliche Runner-Symbole per AST-Digest ein und oeffnet nur
target-gesperrte Fehltests sowie eine minimale P5-lokale Korrektur an der
vorhandenen Record-Grenze. Python-Standardbibliothek traegt den Datenvertrag;
NumPy-Skalare duerfen die numerische Schicht nicht ungeprueft verlassen. Eine
gemeinsame Projektbibliothek bleibt bis zu einem dokumentierten
Drei-Pipelines-Semantikvergleich gesperrt.

Diese Korrektur ist nun targetfrei abgeschlossen. Der echte Rueckgabepfad
konvertiert nur registrierte NumPy-Skalare werttreu in native Recordtypen und
validiert jeden vollstaendigen Off-/Aktivarm sofort gegen das v2-Schema. Der
reproduzierte Versuch-3-Nullquotient, ein adversariales Typenfeld, ein
synthetisches 64+768-Vollpanel, Publikation und unabhaengiger Auditor sind
gruen; ebenso 945 lokale Tests und CI fuer den exakten Implementierungscommit.
Das neue Review endet mit
`p5d-production-boundary-ready-target-closed-horizon-transfer-required`.
Das ist Infrastruktur-Readiness, keine Interaktionsevidenz und keine
Autorisierung fuer Versuch 4.

## Inferenz

Die Kreisloesungen sind eine geeignete Basis, um center-konjugierte Ports und
gegenseitige Kopplung mathematisch zu untersuchen. Aus den drei bisherigen
Ziellaeufen folgt jedoch nichts ueber reale Wechselwirkung oder Masse.

## Hypothesen

Interaktion, Ladung und Felder sowie Spin, Impuls, Traegheit und Masse bleiben
offen. Insbesondere ist eine zweite Differenz im sichtbaren Pfad noch kein
Nachweis einer positiven, zustandsunabhaengigen Masse. Der reziproke P5-D-Port
besitzt bei angehaltener nativer Centerbewegung exakt ein Relaxationsmodell
erster Ordnung. Ein gekoppelter harmonischer Oszillator ist daher ein
nachgelagerter Falsifikator fuer eine zusaetzliche, gedaechtnisinduzierte
Zustandsdimension und kein bereits eingebautes P5-D-Ergebnis.

## Claim-Grenze

Zulaessig ist: lokal zertifizierte bzw. numerisch kontrollierte Schleifen und
eine algebraisch definierte gegenseitige Center-Kopplung. Nicht zulaessig ist:
eine physikalische Deutung der P5-D-Infrastrukturfehler als positives oder
negatives Interaktionsergebnis.

## Quellen

- Modellreferenz: [Gleichungen](../reference/implemented_equations.md),
  [Rotating Waves](../reference/rotating_wave_foundation.md) und
  [Vokabular](../reference/model_vocabulary.md)
- [P5-D v2-Ergebnisvertrag](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json)
- [P5-D Versuch-3-Incident](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_attempt3_numpy_float_schema_failure_2026-09-05.md)
- [P5-D Produktionspfad-Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_loop_p5d_production_path_preflight_protocol_2026-09-06.md)
- P5-D Protokollreviews:
  [negatives Erstreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_review_2026-09-06.md)
  und
  [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_sufficiency_review_2026-09-06.md), danach das
  [Produktionsgrenzen-Readinessreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_readiness_review_2026-09-07.md)
- Horizontkette:
  [Finite-H Non-Tautology-/Horizont-Audit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_finite_h_non_tautology_audit_2026-09-07.md),
  [amendiertes Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_transfer_protocol_2026-09-08.md),
  [negatives Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_protocol_review_2026-09-08.md)
  und
  [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_protocol_sufficiency_review_2026-09-08.md), danach
  [RED-Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_red_contract_review_2026-09-08.md)
  und
  [Infrastrukturreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_infrastructure_review_2026-09-08.md)
  sowie das
  [v3-Vertragsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_v3_review_2026-09-09.md)
  und das korrigierende
  [Orchestrierungsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_runner_orchestration_review_2026-09-09.md)
  sowie den
  [Backend-Bestandsaudit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_backend_reuse_audit_2026-09-09.md)
  und das
  [finite-Rootadapter-Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_finite_root_adapter_review_2026-09-09.md)
  sowie das
  [Homotopie-/Intervallreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_homotopy_interval_review_2026-09-09.md)
  und das
  [lokale Ausschlussreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_local_exclusion_review_2026-09-09.md)
- [Claim-Register](paper_claims.md)
