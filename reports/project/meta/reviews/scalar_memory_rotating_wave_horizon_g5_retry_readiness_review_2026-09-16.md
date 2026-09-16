# Readinessreview: isolierter G5-Retry, Attempt 2

Datum: 2026-09-16.

Implementation revision: `319c0b1f1e9a47e1791acfa145e97ed70788c9bb`

Verdict: **`g5-implementation-ready-target-closed`**

Dieses Verdikt betrifft ausschliesslich den outcome-blind vorbereiteten
Attempt-2-Pfad. Es ist weder ein G5-Ergebnis noch selbst eine technische
Zielautorisierung.

## 1. Gepruefter Umfang

Das Erstprotokoll, alle wissenschaftlichen Parameter, Rootboxen,
Arnoldi-Panels, Stoerungsarme, Schwellen und Stopregeln bleiben unveraendert.
Der Retry aendert nur

1. die bereits separat reviewte binary64-Kanonisierung normierter
   Projektionsoverlaps innerhalb des dimensionsskalierten Rundungsbudgets;
2. Attemptnummer, Receipt und Ergebnisnamen von Attempt 1 auf Attempt 2;
3. die Blobbindung an Retry-Protokoll, Erstprotokoll und den korrigierten
   Standardbibliothekskern.

Attempt 1 und seine Receipt bleiben erhalten. Ergebnis, Lesereport, Manifest
und Receipt von Attempt 2 besitzen getrennte, vor dem Zielzugriff verlangte
leere Pfade.

## 2. Code- und Methodenreview

Der Guard ist beim Import passiv und akzeptiert ausschliesslich
`REGISTERED_ATTEMPT = 2`. Komponentengate und unabhaengiger Auditor verlangen
dieselbe Attemptnummer und denselben Receiptpfad. Eine falsche Attemptnummer,
Dependency- oder Blobdrift, ein gemischter Autorisierungscommit, falsche
Remote-CI, ein abweichendes Readinessreview, nichtleere Zielpfade oder ein
schmutziger beziehungsweise nicht synchronisierter Arbeitsbaum stoppen vor
Receipt und Numerik.

Die Receipt wird weiterhin atomar vor dem Laden des numerischen
Komponentenmoduls erzeugt. Der bestehende Attempt-1-Pfad wird dabei weder
gelesen noch als Blocker behandelt. Ein Fehler nach Receipt-Erzeugung
verbraucht Attempt 2; ein weiterer Retry ist nicht registriert.

Die Overlap-Korrektur liegt in der wiederverwendbaren
Horizon-Stabilitaetsbibliothek vor Klassifikation und Serialisierung. Der
Resultatvertrag und der unabhaengige Auditor akzeptieren weiterhin nur das
exakte Intervall $[0,1]$; Abweichungen von $10^{-8}$, `NaN` und Unendlich
werden verworfen. Kein Major- oder Critical-Befund verbleibt.

## 3. Reproduzierbare Nachweise

- Fokussierte Attempt-2-/Vertrags-/Governance-Regression: `47 passed` vor
  den zusaetzlichen Receipt-Pfadtests; diese bestanden anschliessend mit der
  fokussierten Suite `30 passed in 7.71s`.
- Lokale Vollregression vor den letzten reinen Testergänzungen:
  `1126 passed in 332.20s`.
- Offizielle Linux-CI mit allen finalen Tests:
  [GitHub Actions run 35135707220](https://github.com/MemoryDynamics/Knoten/actions/runs/35135707220),
  `1129 passed in 382.77s`, Lint Pass und strikter Doku-Build Pass.
- Reale Closed-Probe am Implementierungscommit: Abbruch vor Receipt und
  Zielmodul mit `G5 target sealed by machine governance`.
- Laufzeitbindung: Python 3.12, NumPy 2.3.5, SciPy 1.17.1 und mpmath 1.3.0.

## 4. Geschuetzte Implementierungsobjekte

- Blob `requirements.txt`: `257723e469e56d5e1db0efcaff57c26e71a9ebf5`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g5_component_retry_protocol_2026-09-16.md`: `44e6378f9e8d62f2a42db0a56115a9729f1eb237`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g5_component_protocol_2026-09-14.md`: `9815604436b93054097c69c0de1b4d49cfee1778`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_schema_v1.json`: `8c3aa7582e1c693452906db840b68b369c603529`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_gate.py`: `ea7621950886cfc1c91ff8767bb4dd50ed35cf08`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_audit.py`: `643050b85e6d3a93b44fce07f4dce81bb86fc3c6`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_execution.py`: `75c3bf2b883c0240cca2a34ab235756467da0047`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_gate.py`: `1f6ed63a92eb12812a4c7d31ad39b0d70b146eb9`
- Blob `src/emergenz_knoten/rotating_wave.py`: `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d`
- Blob `src/emergenz_knoten/rotating_wave_interval.py`: `e269e729c68c8030a6aae222fb4fa67069dd46fd`
- Blob `src/emergenz_knoten/rotating_wave_horizon_stability.py`: `376f263af4891869a7e81969ca05e11ba86735a5`
- Blob `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`
- Blob `src/emergenz_knoten/rotating_wave_stability_gate.py`: `630beb9952abefea823d91388dcbb2de8f1a2927`
- Blob `src/emergenz_knoten/strict_json_contract.py`: `221372ea86f857aa4141e2609e46a0dc536c1ab4`
- Blob `tests/test_rotating_wave_horizon_g5_component.py`: `48c38312eb4d9cf6c6dbd67cfff43ae189faaed2`
- Blob `tests/test_rotating_wave_horizon_g5_execution.py`: `1a875ff0f26425037a0fb090f9066d822b026c38`
- Blob `tests/test_rotating_wave_horizon_stability.py`: `54669ebd8d37ff5821decd40f47c7bc3394962b3`

Der geschlossene Governance-Blob im Implementierungscommit ist
`3c8e5fda7e4f96bd4cca8c08f8883cecbc7b702b`. Eine Freigabe muss genau diesen
Ausgangszustand binden und darf ausschliesslich den Governance-Record aendern.

## 5. Kritische Grenzen

Der konkrete beim Erstversuch verworfene Overlap ist unbekannt. Die
Remediation ist daher durch mathematische Grenze, targetfreie Reproduktion
und Falsifikation begruendet, nicht durch Rekonstruktion des verlorenen
Zielwerts. Das Review garantiert nicht, dass Attempt 2 alle numerischen
Stufen abschliesst oder ein entscheidendes G5-Ergebnis liefert.

Der Auditor rekonstruiert Vertrag, Hashes, Schwellen, Panelmatch,
Trajektoriensummaries und Publikation, berechnet aber sparse Ritzresiduen und
Overlaps nicht mit einem unabhaengigen zweiten Eigensolver neu. Ein
erfolgreicher Lauf bleibt deshalb lokale numerische Evidenz mit der im
Erstprotokoll festgelegten Claimgrenze.

## 6. Entscheidung

Es verbleibt kein Major- oder Critical-Befund. Attempt 2 ist targetfrei
ausfuehrungsbereit, aber technisch geschlossen. Aufgrund der ausdruecklichen
Nutzerentscheidung vom 2026-09-16 ist als naechster Schritt genau ein
Governance-only-Autorisierungscommit zulaessig. Erst nach dessen Push und
vollstaendiger Guardpruefung darf genau eine Attempt-2-Receipt erzeugt und der
Run gestartet werden.
