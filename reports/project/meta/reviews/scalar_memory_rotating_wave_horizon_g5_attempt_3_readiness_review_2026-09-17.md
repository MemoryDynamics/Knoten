# G5 Attempt 3: Readiness- und Meta-Review

Stand: 2026-09-17.

Implementation revision: `059ff8e18630bfe1c64e533f17832a8bb3b25b3c`

Verdict: **`g5-implementation-ready-target-closed`**

Dieses Review bewertet ausschliesslich die technische Messkette. Es ist weder
ein G5-Ergebnis noch Evidenz fuer Horizonttransfer, Stabilitaet oder
Interaktion. Der Targetzugriff blieb waehrend des gesamten Reviews geschlossen;
es existiert weder ein Attempt-3-Receipt noch ein Attempt-3-Ergebnis.

## 1. Falsifikation und Remediation

Der vorregistrierte RED-Test setzt das Distanzmaximum absichtlich zwischen
zwei publizierte Zehnersamples. Die alte Attempt-2-Semantik wurde damit exakt
falsifiziert: Der Integrator kannte das Vollschrittmaximum, der Validator konnte
es aus dem ausgeduennten Record nicht rekonstruieren.

Schema v2 speichert deshalb fuer genau 5001 Integratorschritte eine dichte
Distanzspur: einen endlichen, nichtnegativen Praefix und nach einem Abbruch nur
`null`. Maximum, Maximumschritt sowie Anfangs- und Endverhaeltnis werden in
Runner und unabhaengigem Auditor jeweils neu aus dieser Spur berechnet. Die
weiterhin publizierten Zehnersamples muessen deren exakte Projektion sein. Kein
physikalischer Parameter, Schwellenwert oder Gateentscheid wurde geaendert.

## 2. Kritischer Codebefund

Die erste Implementierung veraenderte versehentlich den eingefrorenen
historischen Fortsetzungskern. Die Provenienztests entdeckten dies in den
CI-Laeufen 35164441484 und 35164813765; beide Laeufe scheiterten, und der
Targetzugriff blieb geschlossen. Die Remediation stellte den Altblob exakt
wieder her und fuegte die dichte Recordsemantik als separates
Standardbibliotheksmodul hinzu.

Zwei numerische Paritaetstests vergleichen Alt- und Neukern bitweise fuer
exakte und radiale synthetische Faelle. Ein zusaetzlicher AST-Test entfernt nur
Funktionsnamen, Docstring und die neuen Trace-Operationen und verlangt danach
identische Kontrollflussbaeume. Damit ist die wissenschaftliche Dynamik des
neuen Pfads gegen unbeabsichtigte Abweichung vom eingefrorenen Kern gesperrt.

## 3. Verifikation

- Der finale GitHub-Lauf
  [35166339027](https://github.com/MemoryDynamics/Knoten/actions/runs/35166339027)
  pruefte exakt die unten gebundene Revision erfolgreich.
- Ergebnis: 1145 Tests bestanden; Python-Lint und strikter Dokumentationsbau
  bestanden ebenfalls.
- Die historischen P3-/P4-/P4R-/P4RS-Blobtests bestanden wieder unveraendert.
- Ein echter Closed-Gate-Probelauf brach vor Receipt und Targetzugriff mit der
  erwarteten Governance-Sperre ab.

## 4. Verbleibende Grenzen

Der Auditor prueft Record, Rekonstruktion und Publikationsartefakte unabhaengig,
berechnet aber die 4800-dimensionale Dynamik und den Eigenloeser nicht nochmals
mit einem zweiten Backend. Der dichte Fortsetzungskern dupliziert bewusst den
eingefrorenen Schleifenkern; numerische und strukturelle Paritaet begrenzen
diese Duplikation, ersetzen jedoch keine formale Programmverifikation. Diese
Punkte sind methodische Restgrenzen, keine verdeckten G5-Befunde.

Es verbleibt kein Major- oder Critical-Codebefund fuer den einmaligen
Attempt-3-Lauf. Die explizite Nutzerfreigabe vom 2026-09-17 erlaubt als
naechsten Schritt genau einen Governance-only-Autorisierungscommit und danach
genau einen Lauf. Sie autorisiert weder einen Parameterwechsel noch Attempt 4.

## 5. Gebundene Implementationsblobs

- Blob `requirements.txt`: `257723e469e56d5e1db0efcaff57c26e71a9ebf5`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_protocol_2026-09-17.md`: `f194ae9f1f08278378ab6de9965192051dd04803`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g5_component_retry_protocol_2026-09-16.md`: `44e6378f9e8d62f2a42db0a56115a9729f1eb237`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g5_component_protocol_2026-09-14.md`: `9815604436b93054097c69c0de1b4d49cfee1778`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_schema_v2.json`: `0f635c5bb8249199fda4ae5e9d76a71e7adaae05`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_schema_v1.json`: `8c3aa7582e1c693452906db840b68b369c603529`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_gate.py`: `552216a26c6b046c62e8d9440ea3c47dfd396376`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_audit.py`: `7ea87a435d5b148502a5660f058630b79f165509`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_execution.py`: `e8a45b5019e2493fba1130bba9449f1e9068ca3c`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_gate.py`: `71ea20baa0bb8cd5eab11be94a3bd91d9a6049bf`
- Blob `src/emergenz_knoten/rotating_wave.py`: `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d`
- Blob `src/emergenz_knoten/rotating_wave_dense_continuation.py`: `26043400e721855dc47c512bc36524555d09b089`
- Blob `src/emergenz_knoten/rotating_wave_interval.py`: `e269e729c68c8030a6aae222fb4fa67069dd46fd`
- Blob `src/emergenz_knoten/rotating_wave_horizon_stability.py`: `376f263af4891869a7e81969ca05e11ba86735a5`
- Blob `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`
- Blob `src/emergenz_knoten/rotating_wave_stability_gate.py`: `630beb9952abefea823d91388dcbb2de8f1a2927`
- Blob `src/emergenz_knoten/strict_json_contract.py`: `221372ea86f857aa4141e2609e46a0dc536c1ab4`
- Blob `tests/test_rotating_wave_horizon_g5_component.py`: `64fe5c93d8d55021dcc2f45776fe2c7a4d69cd21`
- Blob `tests/test_rotating_wave_horizon_g5_execution.py`: `cb72c505dcc6f1120c1acc0d46a37b012a58580b`
- Blob `tests/test_rotating_wave_horizon_stability.py`: `54669ebd8d37ff5821decd40f47c7bc3394962b3`
- Blob `tests/test_rotating_wave_horizon_transfer.py`: `dff5c1dd4de34868dbc77acf1b7e0f7fb9af8942`
- Blob `tests/test_rotating_wave_dense_continuation.py`: `ba58534978d335a80f6fb2ede7b54b68ba2df697`
- Blob `tests/test_rotating_wave_stability_gate.py`: `574a4e7b6aa62b6a21619e628882df2be967585a`

