# Native rotating-wave pipeline

Stand: 2026-08-21.

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

## Claim-Grenze

Die Programme etablieren:

- eine exakte algebraische Kreisreduktion des nativen Updates;
- fuenf lokal eindeutige finite-H-Roots auf einem gematchten Ast;
- einen unabhaengig reproduzierten numerischen Kontinuumsroot;
- lokale numerische Stabilitaetsevidenz am Anchor.

Sie etablieren nicht:

- globale Rooteindeutigkeit oder ein all-alpha-Theorem;
- Nicht-Anchor-Stabilitaet oder vollstaendige Spektraleinschliessung;
- Formation, Basin, Rauschrobustheit oder Haendigkeitsselektion;
- internes S1 nach ambientem \(SO(2)\)-Quotient;
- Arbeit, Traegheit oder Masse.

## Versiegelter naechster Schritt

L5 mit

```text
alpha=0.00125, H=9600, eta=0.01875
```

ist dokumentiert, aber noch nicht implementiert oder ausgewertet. Vor dem
Lauf wird ein neues Protokoll mit Astkorridor, Intervallboxen,
Dezimalskalierung und First-order-Entscheidungsregel committed und gepusht.
Der Amplituden-Holdout `A_att=7` bleibt versiegelt.
