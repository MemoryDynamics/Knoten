# Native rotating-wave pipeline

Stand: 2026-09-01.

Dieses Verzeichnis enthaelt die aktive, sequentielle Evidenzpipeline fuer
raeumliche Rotating waves des nativen skalaren finite-memory-Modells. Die
Programme sind keine austauschbaren Parameter-Scans. Jeder Schritt setzt die
eingefrorene Entscheidung des vorherigen Schritts voraus.

## Reihenfolge

| Stufe | Programm | Rolle | Status |
| --- | --- | --- | --- |
| 1 | `scalar_memory_rotating_wave_discovery.py` | vorregistrierte Kontinuumssuche, Kontrollen und erste native finite-H-Verfeinerung | abgeschlossen |
| 2 | `scalar_memory_rotating_wave_stability_gate.py` | voller mitrotierender FIFO-Jacobian und lokale Stoerungsfortsetzungen am P0-Anchor | lokaler numerischer Pass |
| 3 | `scalar_memory_rotating_wave_interval_certificate.py` | lokaler Krawczyk-Existenz-/Eindeutigkeitsbeweis des Anchor-Roots | Pass |
| 4 | `scalar_memory_rotating_wave_refinement_ladder.py` | fuenf gematchte und lokal zertifizierte Zellen L0--L4 | Roots Pass; historisches Target-Gate Fail |
| 5 | `scalar_memory_rotating_wave_continuum_reconciliation.py` | korrekt bei festem \(\eta/\alpha=15\) definierter Kontinuumsroot und Wiederanwendung der alten Skalierungsgates | Reconciliation-Pass |
| 6 | `scalar_memory_rotating_wave_foundation_audit.py` | kanonischer Git-Blob-/Vollhistoriencheck, unabhaengige finite-Summen-Replays, zwei Multipraezisions-Kontinuumspanels und Skalierungs-Replay | portability-scoped Reconciliation-Pass |
| 7 | `scalar_memory_rotating_wave_l5_existence_scaling.py` | prospektiver sechster Root bei \((\alpha,H,\eta)=(0.00125,9600,0.01875)\), zwei Krawczyk-Panels, direkter Summen-Replay und signierte First-order-Gates | scoped L5-Pass |
| 8 | `scalar_memory_rotating_wave_l3_stability_gate.py` | prospektiv gewaehlte L3-Zelle, zwei getrennte Arnoldi-Panels und sieben registrierte Voll-FIFO-Fortsetzungen | lokaler numerischer Pass; kritisch gehalten |
| 9 | `scalar_memory_loop_center_p2_gate.py` | voller matrixwertiger FIFO-Tangentenvergleich, drei Amplituden, zwei Richtungen und unabhaengige zero-net Wellenform am unveraenderten L3-Kandidaten | formaler P2-Fail nur an der absoluten Tail-Slope-Grenze; alle Linearitaets- und Resttermgates positiv |
| 10 | `scalar_memory_loop_center_p2r_long_recovery.py` | outcome-informierte, vor weiterer Zielantwort eingefrorene Verlaengerung derselben 16 Arme bis 20 Recovery-Memory-Zeiten | P2-R-Pass in allen 48 neuen sign-sensitiven Fenstern; historischer P2-Fail unveraendert |
| 11 | `scalar_memory_rotating_wave_p3_formation_basin.py` | drei target-informierte und zwei target-blinde nichtkreisfoermige Historienfamilien in beiden Chiralitaeten, vorbereitete Positiv- sowie eta=0-/achirale Negativkontrollen | reviewed P3-Full-Pass als finite-ensemble attraction; keine generische/spontane Formation |
| 12 | `scalar_memory_loop_p4_source_write_gate.py` | expliziter chirality-konditionierter Orbit-Center-Port, reziproker First-order-Aktuator und kompletter finite-H-Write-/Age-Ledger | formaler `p4-source-write-architecture-fail`; Ledger Pass, skalare Geradeausantwort falsifiziert |
| 13 | `scalar_memory_loop_p4r_phase_metrology_gate.py` | frischer Acht-Phasen-Holdout, cancellation-sichere lokale Identitaeten, Full-dot-Envelopes und diskrete Chiral-Klassifikation | reviewed `p4r-phase-averaged-chiral-response-pass`; vier spiegelverschiedene Phasenpaare, kein kontinuierlicher Phasenclaim |
| 14 | `scalar_memory_loop_p4r_result_audit.py` | Standardbibliothek-Neuberechnung des gespeicherten Roh-JSON ohne Target-Runner oder numerische Drittanbieterpakete | `p4r-independent-audit-agrees`; gemeinsame Simulation, keine externe Replikation |
| 15 | `scalar_memory_loop_p4rs_anchor_scale_gate.py` | gepaarter Anchor-Holdout bei gleicher Memory-Zeit mit geerbtem Port/Ledger und Trace-/Phasenprofil-Skalengates | reviewed `p4rs-anchor-scale-transfer-pass`; zwei vorbereitete Skalen, keine Replikation oder Konvergenzordnung |
| 16 | `scalar_memory_rotating_wave_noise_stress.py` und separater Ergebnis-Auditor | dimensionslose logarithmische N0-Klammer fuer binary64-Aufloesung und endliche orbitale Robustheit | reviewed `n0-noise-stability-window-bracketed-pass`; `chi=1e-4` besteht, `1e-3` scheitert lokal |
| 17 | `scalar_memory_loop_p5d_mutual_center_gate.py` und separater Ergebnis-Auditor | eingefrorenes Anchor--Anchor-Panel mit linearem gegenseitigem notched-Center-/Write-Port, Einwegablationen und Closed-loop-Kontrast | Erstaufruf am NumPy-Bool-JSON-Typ und einziger Recovery-Ersatzlauf am garantierten Channel-off-`inf`-Sentinel jeweils `p5d-inconclusive`; keine Artefakte/Entscheidung, Recovery verbraucht und P5-D geschlossen |

Die historische Entscheidung `certified-roots-nonconvergent` aus Stufe 4
bleibt unveraendert. Stufe 5 erklaert den vorab sichtbaren Gain-Mismatch des
alten Guides; sie benennt den alten Lauf nicht um.

## Foundation-Audit reproduzieren

Der Audit verlangt einen sauberen Arbeitsbaum, vollstaendige Git-Historie und
die exakt gehashten kanonischen Git-Blobs der historischen Inputs:

```bash
python experiments/current/dynamics/rotation/scalar_memory_rotating_wave_foundation_audit.py
```

Der erste Foundation-Auditlauf ist als Implementierungs-Fail archiviert. Sein
strikter binaerer Vergleich von `eta/alpha == 15` widersprach der
vorregistrierten exakten Dezimalarithmetik. Die aktuelle Version folgt dem
separat eingefrorenen Reconciliation-Protokoll, verwendet `Decimal` fuer die
zwei Skalierungsidentitaeten und rechnet alle anderen Gates vollstaendig neu.

Ein anschliessender Linux-CI-Lauf falsifizierte die Portabilitaet des ersten
lokalen Passes: Sechs Hashes bezogen sich auf CRLF-Arbeitsbaumbytes statt auf
die versionierten LF-Git-Blobs; der ein-Commit-Shallow-Checkout verbarg zudem
gueltige historische Revisionen. Ein zweites, vor der Korrektur eingefrorenes
Protokoll autorisierte ausschliesslich die Hashdomaene `HEAD:path`,
`fetch-depth: 0` und Regressionstests. Der aktuelle Voll-Re-Run besteht alle
A--E-Gates ohne Aenderung eines wissenschaftlichen Inputs oder Schwellenwerts.

## L5-Gate reproduzieren

Der L5-Runner verlangt ebenfalls einen sauberen Arbeitsbaum und vollstaendige
Historie. Er prueft die drei kanonischen Input-Blobs und den separat
publizierten Protokoll-Commit, bevor die Zielzelle geoeffnet wird:

```bash
python experiments/current/dynamics/rotation/scalar_memory_rotating_wave_l5_existence_scaling.py
```

Die lange Zielrechnung gehoert nicht in CI. CI prueft den Runner mit
synthetischen First-order-/Branch-Crossing-Falsifikatoren, off-target
Summenvergleich, Provenienz, Lint und Dokumentationsbau. Beide Zielpanels
verwenden `mpmath.iv` 1.3.0; sie sind keine unabhaengigen Intervallbackends.

## Claim-Grenze

Die Programme etablieren:

- eine exakte algebraische Kreisreduktion des nativen Updates;
- sechs lokal eindeutige finite-H-Roots auf einem gematchten Ast;
- einen unabhaengig reproduzierten numerischen Kontinuumsroot;
- lokale numerische Stabilitaetsevidenz am Anchor und an L3;
- finite-ensemble attraction fuer die zehn registrierten nichtkreisfoermigen
  P3-Arme am unveraenderten L3-Kandidaten.

Sie etablieren nicht:

- globale Rooteindeutigkeit oder ein all-alpha-Theorem;
- Stabilitaet der uebrigen Nicht-Anchor-Zellen oder vollstaendige
  Spektraleinschliessung;
- einen offenen Basin-Ball, generische/spontane Formation,
  Rauschrobustheit oder Haendigkeitsselektion aus symmetrischen Daten;
- internes S1 nach ambientem \(SO(2)\)-Quotient;
- Arbeit, Traegheit oder Masse.

## Naechster Schritt

L3 bei \((\alpha,H,\eta)=(0.005,2400,0.075)\) wurde vor Einsicht in ein neues
Spektrum als kleinste zertifizierte Zelle in der feineren Kontinuumsrichtung
ausgewaehlt. Der Lauf aus sauberem Implementierungscommit besteht beide
Arnoldi-Panels mit \(|\lambda_\perp|=0.99649340\); alle sechs gespiegelten
Stoerungsarme kontrahieren ueber 50 Memory-Zeiten. Das separate kritische
Review haelt nur lokale numerische Stabilitaet an dieser zweiten Skala
aufrecht.

Reproduktion des eingefrorenen Laufs:

```bash
python experiments/current/dynamics/rotation/scalar_memory_rotating_wave_l3_stability_gate.py
```

Reproduktion des eingefrorenen P2-Laufs:

```bash
python experiments/current/dynamics/rotation/scalar_memory_loop_center_p2_gate.py
```

Der P2-Lauf bleibt formal `loop-center-matrix-local-fail`: Die Antwort folgt
dem vollen Tangentenmodell sehr genau und klingt post hoc monoton ab, ist im
registrierten Endfenster aber nicht flach genug.

Reproduktion der eingefrorenen P2-R-Verlaengerung:

```bash
python experiments/current/dynamics/rotation/scalar_memory_loop_center_p2r_long_recovery.py
```

P2-R reproduziert alle 120 alten Entscheidungsmetriken exakt und besteht alle
48 neuen sign-sensitiven Fenster durch 20 Memory-Zeiten. Das kritische Review
haelt dies als outcome-informierte Reconciliation, nicht als unabhaengige
Replikation. Dieser historische Befund oeffnete nur die Vorregistrierung von
P3 Formation/Basin am unveraenderten L3-Kandidaten.

Reproduktion des eingefrorenen P3-Laufs:

```bash
python experiments/current/dynamics/rotation/scalar_memory_rotating_wave_p3_formation_basin.py
```

Alle zehn nichtkreisfoermigen Arme erreichen und halten den L3-Zielorbit; der
reviewed Claim bleibt finite-ensemble attraction aus fuenf Geometrien mit
gesetzter Chiralitaet. Dieser historische Pass oeffnete nur P4 fuer eine
mikroskopisch reziproke Single-Loop-Architektur mit geschlossenem
Arbeitsledger.

Reproduktion des eingefrorenen P4-Laufs erfordert den im Ergebnis genannten
Execution-Commit und einen sauberen Arbeitsbaum:

```bash
python experiments/current/dynamics/rotation/scalar_memory_loop_p4_source_write_gate.py
```

Der unveraenderliche Befund ist `p4-source-write-architecture-fail`. Der
finite-H-Write-/Age-Ledger schliesst, aber zwei cancellation-dominierte
Direktresiduen verfehlen ihre unter-binary64 skalierte Grenze und alle 24 Arme
zeigen eine zu grosse chirality-odd Querantwort. Der spaetere P4-R-Pass
benennt diesen historischen Fail nicht um.

Der P4-R-phi-Runner ist
`scalar_memory_loop_p4r_phase_metrology_gate.py`. Er implementiert die
eingefrorene Reihenfolge aus 16 phase-spezifischen channel-off- und 32 aktiven
Armen, lokale Increment-Metrologie, konservative binary64-Envelopes,
80-stellige Checkpoint-Replays sowie Spiegel- und Halbdrehungskovarianz. Der
unveraenderliche Befund ist `p4r-phase-averaged-chiral-response-pass` mit
`B_C=0.2084215772`, `B_Q=0.1537530855` und 8/8 positivem Phasensupport.
Die 32 Arme sind Kontrollen innerhalb einer diskreten Acht-Knoten-Quadratur,
keine Replikationen; vier Phasenpaare sind spiegelverschieden.

Der getrennte Auditor kann das gespeicherte Ergebnis ohne Target-Import neu
klassifizieren:

```bash
python experiments/current/dynamics/rotation/scalar_memory_loop_p4r_result_audit.py --output <absolute-temporary-json>
```

Das Gate-Review und das interne Source-Referee-Audit halten nur den engen
diskreten Port-/Ledger-/Antwortbefund aufrecht. Das Source-Urteil lautet wegen
eines einzelnen Intervallbackends, fehlendem vollstaendigem Hash-Lock und
fehlender Citation/Release
`referee-source-ready-with-major-claim-restrictions`. P4-R-S-Design und
Anchor-Protokoll froren danach targetfrei 2000 Anchor- gegen 4000 L3-Updates
ueber `tau=alpha*n`, skalenweise rekonstruiertes `G=nu` und
`epsilon_scale=0.05` fuer komplette Transienten, Phasenprofile und Endmittel
ein. Nach getrenntem Implementierungsreview wurde der erste registrierte Lauf
unveraendert ausgefuehrt. Alle 16 channel-off-, 32 aktiven Arme und 96
High-precision-Referenzen bestehen; die groesste Anchor--L3-Abweichung ist
`0.00232715` gegen `0.05`. Ein separat implementierter
Standardbibliothek-Auditor rekonstruiert die gespeicherte Entscheidung als
`p4rs-anchor-scale-transfer-pass` ohne Feldabweichung. Das Ergebnisreview
oeffnete nur P5-Design und prospektive Protokollierung; die nachgelagerte
Implementierung musste deshalb erneut targetfrei eingefroren und separat
reviewed werden. Interaktionsevidenz sowie Topologie-, Spin-, Impuls-,
Traegheits- und Masseclaims bleiben versiegelt.

Der N0-Runner `scalar_memory_rotating_wave_noise_stress.py` hebt den
deterministischen Ast danach mit expliziter Paper-I-Innovation an. Der einmalige
registrierte Lauf verwendet `chi=epsilon/(R sqrt(alpha))`, drei gemeinsame
Brownian-refinement-Pfade und getrennte binary64-Aufloesungsmetrologie. Das
reviewte Ergebnis ist `n0-noise-stability-window-bracketed-reviewed-pass`:
unaufgeloest bis `1e-16`, stabil von `1e-15` bis `1e-4`, Phasen-/
Chiralitaetsfail ab `1e-3`. Der getrennte Auditor
`scalar_memory_rotating_wave_noise_stress_result_audit.py` rekonstruiert alle
132 Zellen ohne Gateabweichung. Damit sind P5-D-Design und Protokoll
eingefroren. Pair-step, Runner, Standardbibliothek-Auditor und synthetische
Falsifikatoren sind targetfrei implementiert und CI-gruen. Das separate
Readinessreview pruefte alle zwoelf Vorbedingungen. Der erste autorisierte
P5-D-Aufruf erreichte die finale Serialisierung, scheiterte dort aber an einem
verschachtelten NumPy-Bool und hinterliess keine Standardartefakte oder
beobachtete Entscheidung. Die separat eingefrorene Recovery bestand Code- und
Readiness-CI; ihr einziger Ersatzlauf scheiterte danach am in jedem
Channel-off-Record garantierten `minimum_dissipation=inf` unter
`allow_nan=False`. Auch er hinterliess keine Artefakte oder Entscheidung.
Beide Aufrufe sind `p5d-inconclusive`, die Recovery-Autorisierung ist
verbraucht und P5-D geschlossen. Ein anschliessendes targetfreies
adversariales Code-Review bestaetigt die algebraischen Portgleichungen, findet
aber sieben Blocker der Ergebnisstrecke. Daher bleibt der Runner
`p5d-runner-not-ready-no-target-authorized`.
