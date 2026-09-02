# Archivierte Frontdoor bis 2026-09-02

Stand: 2026-09-01.

Diese Dokumentation ist die kuratierte Frontdoor fuer das Projekt. Sie ist
bewusst klein gehalten: aktive Orientierung laeuft ueber zehn Dokumente.
Historische Chatverlaeufe, alte Paper-Artefakte und Rohnotizen bleiben im
Repository, gelten aber nicht als kuratierte Quelle.

## Projekt in einem Satz

`Emergenz Knoten` untersucht einen selbstinteragierenden stochastischen
Prozess mit relaxierendem Gedaechtnis. Der sichtbare Prozess `x_n` ist im
Allgemeinen nichtmarkovsch; der augmentierte Zustand `z_n=(x_n,rho_n)` bzw.
eine explizite Memory-Reprasentation ist die Markov-Einbettung. Metastabile
Knoten sollen ueber Residence-Zeiten, Operator-Moden und Kontrollen messbar
werden, nicht ueber Einzelbilder.

## Die zehn aktiven Dokumente

1. [Aktueller Stand](status/current_status.md) - Was ist jetzt wahr, was laeuft, was ist offen?
2. [Prioritaeten](status/project_priorities.md) - Die einzige prospektive Gate-Folge.
3. [P4-R-S allgemein erklaert](status/p4rs_plain_language_summary.md) - Was der Zwei-Zellen-Pass bedeutet und was nicht.
4. [Theoretical Context](reference/THEORETICAL_CONTEXT.md) - Modellkern, Markov-Schicht, Claim-Grenzen.
5. [Center-Filter und Rotation](reference/scalar_memory_center_filter.md) - lesbare \(B_H\)-Algebra, Grundgroessen und Rotationsbruecke.
6. [Native Rotating Waves](reference/rotating_wave_foundation.md) - exakte Kreisgleichung, Evidenzleiter und Reviewergrenzen.
7. [Repository Map](reference/repository_map.md) - Mermaid-Uebersicht ueber Code, Daten, Paper und Doku.
8. [Experiment-Katalog](reference/experiment_catalog.md) - Entry-Points, Ergebnisse, Kontrollen, Reproduzierbarkeit.
9. [Paper-Claims](status/paper_claims.md) - Claim-Register fuer Paper 0/I/II/III.
10. Diese Startseite.

Damit ersetzt diese Struktur die alten Parallelseiten `action_matrix`,
`hardening_plan`, `markov_architecture`, `markov_requirements`,
`non_markovian_basis`, `project_map`, `architecture_overview`,
`reproducibility_status` und `long_run_metastability_plan`.

## Aktuelle Entscheidung

Paper 0 bleibt der mathematische Anker bzw. ein moegliches Supplement. Paper I
soll weiterhin den belastbaren Minimalmechanismus tragen, aber die numerische
Evidenz wird nach der Kernelgradient-Korrektur neu aufgebaut.

Ein davon getrennter nativer `d=2`-Ast besitzt inzwischen sechs lokal
existenzzertifizierte finite-H-Kreisroots bei gematchtem `H*alpha=12` und
`eta/alpha=15`. Ein separat implementierter Foundation-Audit reproduziert die Summen,
den Fixed-gain-Kontinuumsroot und die First-order-Skalierung; der prospektive
L5-Holdout besteht zusaetzlich die direkten Summen- und signierten
Skalierungsgates. Der anschliessend prospektierte P1-Test stuetzt lokale
numerische Stabilitaet am Anchor und an L3 mit
\(|\lambda_\perp|=0.99306035\) beziehungsweise 0.99649340. Beide
Intervallpanels teilen denselben `mpmath.iv`-Backend, und ARPACK schliesst das
volle Spektrum nicht ein. Die belastbare Lesart ist daher „vorbereitete
raeumliche Schleifenbasis mit zwei lokal getesteten Skalen“. Der spaetere P3-
Pass erweitert dies eng auf finite-ensemble attraction aus fuenf
nichtkreisfoermigen Geometrien in beiden gesetzten Chiralitaeten, nicht auf
generische Formation, internes S1, physische Arbeit oder Masse.

Der getrennte Center-Ast besitzt zugleich eine exakte \(B_H\)-Reduktion,
einen passiven effektiven finite-\(H\)-Port und die eng getestete
Filtertraegheit \(m_{\rm filter}=\tau/\mu\). Er identifiziert aber weder einen
materiellen Schwerpunkt noch den mikroskopischen Aktuator fuer physische
Arbeit. P4 konstruiert danach erstmals einen expliziten Source-/Write-Port mit
geschlossenem finite-H-Age-Ledger, besteht aber sein Gesamtgate nicht: Alle 24
Arme zeigen eine vorregistriert zu grosse chirality-odd Querantwort. Gemeinsame
Modellherkunft und ein algebraischer Ledger sind deshalb noch keine
mechanische Objektevidenz. Der frische P4-R-phi-Holdout bestaetigt diese
Querantwort in der registrierten diskreten Acht-Phasen-Quadratur mit
`B_C=0.2084215772`, `B_Q=0.1537530855` und 8/8 positivem Phasensupport.
Vier Phasenpaare sind spiegelverschieden; dies sind keine Replikationen und
kein kontinuierlicher Phasen-, Spin-, Traegheits- oder Massebefund.

Die Programme werden ueber eine einzige falsifizierbare Kette gefuehrt. P2
bleibt formal gescheitert, P2-R haelt nur die lange Rueckkehr aufrecht, P3
besteht scoped, und P4 bleibt formal
`p4-source-write-architecture-fail`. P4-R-phi besteht separat und sein
kritisches Review haelt den engen diskreten Port-/Ledger-/Antwortbefund
aufrecht. Das interne Source-Referee-Audit reproduziert alle
wissenschaftlichen Felder in zwei NumPy/SciPy-Stacks exakt, urteilt wegen
eines einzelnen `mpmath.iv`-Intervallbackends, fehlendem vollstaendigem
Hash-Lock und fehlender Citation/Release aber nur
`referee-source-ready-with-major-claim-restrictions`. Der danach prospektiv
eingefrorene P4-R-S-Anchor-Holdout ist inzwischen unveraendert ausgefuehrt und
separat reviewed. Alle 16 channel-off- und 32 aktiven Anchor-Arme bestehen;
die groesste registrierte Anchor--L3-Abweichung ist `0.00232715` bei
`epsilon_scale=0.05`. Ein unabhaengig implementierter Standardbibliothek-
Auditor rekonstruiert die komplette Entscheidung ohne Feldabweichung. Der
darauf folgende N0-Stress klammert ein aufgeloestes stabiles Fenster
`chi=1e-15..1e-4` ein; `1e-3` und `1e-2` scheitern am lokalen
Phasen-/Chiralitaetsgate. P5-D-Design und ein getrenntes prospektives
Protokoll sind nun targetfrei eingefroren. Sie verwenden eine lineare
gegenseitige notched-Center-/adjungierte Write-Kopplung und verlangen einen
Closed-loop-Kontrast gegen beide Einwegantworten. Implementierung,
Standardbibliothek-Auditor und zwoelf Pre-target-Falsifikatoren sind nun
CI-gruen und wurden getrennt reviewed. Der erste autorisierte Standardaufruf
scheiterte erst bei der finalen JSON-Serialisierung eines NumPy-Bools; er
erzeugte weder Standardartefakte noch eine beobachtbare Entscheidung und ist
formal `p5d-inconclusive`. Die separat eingefrorene Serializer-Recovery
bestand Implementierungs- und Readiness-CI. Ihr einziger autorisierter
Ersatzlauf scheiterte jedoch ebenfalls fail-closed: Die Produktionsstruktur
enthaelt fuer jeden Channel-off-Arm den nicht anwendbaren Sentinel
`minimum_dissipation=inf`, den `allow_nan=False` korrekt ablehnt. Auch dieser
Lauf erzeugte kein Artefakt und keine beobachtbare Entscheidung. P5-D ist
damit ohne neues prospektives Governance-Protokoll geschlossen;
Interaktionsevidenz existiert weiterhin nicht. Spin, Impuls, Traegheit und
Masse folgen nicht.

Historische Long-Run-Evidenz bleibt mit KnotScore v0.5 ausgewiesen. Fuer neue interaktionsfaehige Checkpoints ergaenzt v0.6 ein explizites Stationaritaets-Zulassungsgate; Details stehen im Experiment-Katalog. Alte matched-/zero-mean-/rep-zero-Evidenz vor der Kernelkorrektur ist `legacy-sign`-Auditmaterial.

Der Kernel-Familienvergleich macht die Reduktion explizit: fuer den q=3-
Zweiskalenkernel gilt bei gleicher lokaler Kruemmung exakt
`A_eff=A_att-9`. Auf dieser Achse kollabieren Ein- und Zweiskalen-Kurven bis
auf numerisches Rauschen. Die alte Grenze bei `A_att~=7.9` gehoert zum
rauschstaerkeren historischen Zweiskalen-Slice und darf nicht als neue
Ein-Kernel-Schwelle um sechs gelesen werden.

Die vorhandenen `N=30M/300M`-Radien und das vorregistrierte feste-`g`-Gate
bestaetigen den linearen Kern mit einer kleinen glatten Korrektur: bei
`R_linear/L=0.3` liegt der Radius seed-stabil etwa `6.2%` ueber der linearen
Skalierung, ohne relevante Aenderung von `D_mem` oder Roundness. Residence
und KnotScore sind ueber diese Radiusachse skalenempfindlich; die co-moving
Alternative ist auch fuer `eta=0` gesaettigt und daher nicht diskriminierend.

Die aktuelle Paper-I-Lesart bleibt deshalb eng: kontrollierte co-moving
skalare Relaxationswolke, keine isolierte nichtlineare Metastabilitaet und
kein Dimensionsclaim. Weitere skalare Amplituden- oder kleinere-Epsilon-
Sweeps sind nicht priorisiert.

Die Spektralfeldschicht stellt dasselbe exponentielle rho mit 64 Moden und
rund 1 KB Zustandspeicher dar; eine endliche Realraumhistorie validiert die
Kraft bis zum erwarteten Memory-Tail. Low-Mode-/AR-Closure, Box-/Modenzahlgate
und ein N=1M-Lauf stuetzen eine reduzierte Vorhersagebeschreibung. Der
Eigenvektor-/Zeitsegmentaudit isoliert jedoch keinen stabilen einzelnen
reellen Modus; komplexe aktive und `eta=0`-Subraeume sind praktisch
identisch. Damit kein Oszillator-, Photon-, Metastabilitaets- oder
Propagationsbefund.

Der erste One-Way-Quelltest bleibt ebenfalls negativ, ist nun aber methodisch
schaerfer: Der N100M-Checkpoint besteht ein explizites Vorlauf-
Stationaritaetsgate. Ein externer Punkt-Drive bewegt die Source
radiusbeschraenkt, aber nicht in allen Seeds durchgehend spektral
formkohaerent, und erzeugt nur eine sub-threshold Targetantwort. Naechster
Mechanismusschritt ist deshalb shape-bounded/coherent Source-Transport oder
ein lokaler/retardierter Feldkanal. Reziproke Kopplung bleibt bis dahin
gesperrt.

Der Interaction-Age-Audit bis N=103M trennt die Kanaele weiter: Die
Zentrumantwort akkumuliert ueber +3M Updates nahezu linear auf 20.84
Knotenradien. Die scheinbare Shape-Halbwelle ist real, aber mit der freien
Kontrolle nahezu identisch (Korrelation 0.999953); der gepaarte Differenzspan
betraegt nur 0.142 Prozent des absoluten Shape-Spans. Es gibt damit in diesem
skalaren Fernkanal keinen Befund eines langsam entstehenden neuen Knotentyps
oder einer wechselwirkungsinduzierten Oszillation.

Der daraufhin als eigener Mechanismus eingefuehrte persistente orientierte
One-Way-Kanal besteht zuerst das geklonte Gate und danach bei einem einzigen
globalen `eta_v=5.079e-6` auch das feste-Kopplungs-/Distanzgate in 6/6
zyklisch unabhaengigen Paaren. Die Nahantwort ist gegen 64 Random-Sign-Pfade
und Ein-Schritt-Memory getrennt; Flip und Shape-Huelle bestehen. Das haertet
den konstruierten relationalen Kanal gegen seedweises Retuning.

Die nachgeschaltete lokale Mediatorpruefung besteht fuer beide eingesetzten
Regeln je 5/5 Holdout-Paare. Das ist ein Architekturpass, keine Auswahl:
Relaxations-Diffusion und Telegraph erzeugen jeweils das Verhalten, das ihre
Gleichung vorgibt. Das nachfolgende Spektralgate besteht mit 6/6 autonomen
Sources an allen 18 geerbten Abstaenden. Die Regeln sind breitbandig
unterscheidbar; der persistente und Ein-Schritt-Transferkontrast ist mit
Median `0.991` jedoch nahezu gleich. Das oeffnet nur einen dynamischen
Common-Source-Holdout und ist keine Evidenz fuer Vektorpersistenz oder ein
physikalisches Feldgesetz. Reziprozitaet, `d=3`-Selektion und QFT-Sprache
bleiben gesperrt.

Der dynamische Common-Source-Holdout ist inzwischen negativ abgeschlossen:
Beide lokalen Regeln bestehen die Response-/Shape-Gates, trennen sich aber nur
in 4/6 statt 5/6 Paaren robust. Die anschliessende analytische Rang-Null zeigt
fuer den komponentenweisen Transfer exakt `T=H I_d`; er kann aus einem
vollrangigen Source-Raum keine drei Richtungen selektieren.

Der lokale Feldoperator-Audit ersetzt freie Kernelwahl durch eine
eingeschraenkte Ableitungsentwicklung. Die bisherige Gaussantwort wird bis
`k^4` als Nullfamilie reproduziert, und `s0=0` setzt den Nullmodus exakt auf
null. Eine bevorzugte endliche Wellenzahl verlangt dagegen die neue Annahme
`a2<0` in `1+a2 u^2+u^4`. Ein spaeterer positiver Pilot waere klassische
Musterbildung, noch keine Quantisierung, QFT- oder `d=3`-Evidenz.

Die lineare Write-/Read-Faktorisierung ist geschlossen: In drei Seeds liefern
`rho` mit nachgeschaltetem `K` und das signierte Potentialmemory `phi=K*rho`
mit Dirac-Readout bis `1.5e-14` dieselben Pfade, Felder und Gradienten. Ein
konstantes `K=1` behaelt dagegen nur den Nullmodus und ist kraftfrei. Erst ein
zusaetzlicher lokaler Operator im `phi`-Update macht das Feld selbst-dynamisch.
Genau dieses skalare Delta-Quellfeld ist das naechste Gate. Vektor-,
Chiralitaets- und stringartige Defektmodelle bleiben gesperrte
Paper-III-Kandidaten.

## Nicht ueberclaimen

- Keine eindeutige `d=3`-Selektion aus den bisherigen Daten.
- Keine harte endliche Signalgeschwindigkeit aus exponentiellem Gedaechtnis
  allein.
- Keine Identifikation von Relaxationsraten mit physikalischer Masse.
- Keine Lorentz-, Quanten- oder Standardmodell-Claims in Paper 0/I ausser als
  Future Work.

## Build

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs serve
python -m mkdocs build --strict
```

ReadTheDocs nutzt `.readthedocs.yaml` und `mkdocs.yml`.
