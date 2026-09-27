# G1--G3 Attempt 2: Execution-Readinessreview

Datum: 2026-09-28.

Implementation revision: `bdc033293b74ce2115a3006d13d1ba749bb3ef93`

Verdict: **`g1-g3-implementation-ready-target-closed`**.

## Gegenstand und Claimgrenze

Dieses Review bewertet den exakten targetfreien Implementierungscommit fuer
einen moeglichen zweiten G1--G3-Brueckenversuch. Es ist weder eine
Zielautorisierung noch numerische Evidenz fuer einen finite-$H$-Root,
Branchverbindung, Driftpass, $H\to\infty$-Stabilitaet, Formation,
Interaktion, Traegheit oder Masse.

Versuch 1 bleibt als vor Publikation verbrauchter Pipeline-Incident erhalten.
Sein Receipt wird nicht ueberschrieben. Versuch 2 hat eigene Pfade und ist in
Governance, Receipt und Ergebnispayload durch `attempt=2` gebunden.

## Behobene Readiness-Luecke

Der erste Zielversuch falsifizierte die Annahme, outward-gerundete
Intervallrecords seien exakt symmetrisch um das angeforderte Zentrum. Der
v2-Vertrag verlangt stattdessen beidseitigen Einschluss des beabsichtigten
Kastens und begrenzt jede zusaetzliche Aufweitung durch
$\max(|c|,1)10^{4-p}$. Einwaertsrundung und groessere Aufweitung bleiben
harte Fehler. Dieselbe Semantik ist getrennt im Produktionsvalidator und im
standardbibliotheksbasierten Auditor implementiert, einschliesslich des zuvor
verdeckten Rootzertifikatspfads.

## Falsifikation und Reproduktion

- fokussierter hashstabiler Lauf: **150 passed**;
- vollstaendiger lokaler Lauf: **1199 passed** in 373.52 s;
- exakter CI-Ruff-Scope: bestanden;
- strikter MkDocs-Bau: bestanden;
- offizielle Linux-CI fuer den exakten Implementierungscommit: [Run
  36354118411](https://github.com/MemoryDynamics/Knoten/actions/runs/36354118411),
  `completed/success` mit Lint, Tests und strict Docs;
- targetfreie Grenztests akzeptieren kleine asymmetrische Auswaertsrundung,
  verwerfen Einwaertsschrumpfung und verwerfen eine Aufweitung oberhalb der
  praezisionsgebundenen Schranke in beiden Validatoren.

Ein zusaetzlicher, absichtlich breiter `ruff check .` meldet 24 bestehende
Legacy-/Paper-Befunde ausserhalb des in `.github/workflows/ci.yml`
festgelegten Scopes. Keiner betrifft einen geaenderten oder geschuetzten
G1--G3-Pfad; dieses Review wertet sie nicht als neue Remediationbefunde.

## Geschuetzte Git-Blobs

Die spaetere einmalige Autorisierung muss exakt die folgende Tabelle binden:

- Blob `requirements.txt`: `257723e469e56d5e1db0efcaff57c26e71a9ebf5`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g1_g3_bridge_protocol_2026-09-27.md`: `2a6f0988240fe625a26ef72d42d40a7a4840f940`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_schema_v2.json`: `078bab40cf4cac32c030bfee4af2d66dcc50835d`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_gate.py`: `73ac3541b71028fbdd8273669ce0c192aba55c3b`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_audit.py`: `91d5b889db86f725d0f327034b893ca3aa9d634a`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_execution.py`: `182e6e57874f9038f26a69780a4f60b816b5ea12`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_gate.py`: `56e0c525df4910f78ab14793368b4ce92f176519`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_result_audit.py`: `cbb7614cdfd5a2adcd423c1a8f6ec5d85e0b684d`
- Blob `src/emergenz_knoten/rotating_wave.py`: `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d`
- Blob `src/emergenz_knoten/rotating_wave_dense_continuation.py`: `26043400e721855dc47c512bc36524555d09b089`
- Blob `src/emergenz_knoten/rotating_wave_horizon_stability.py`: `376f263af4891869a7e81969ca05e11ba86735a5`
- Blob `src/emergenz_knoten/rotating_wave_interval.py`: `e269e729c68c8030a6aae222fb4fa67069dd46fd`
- Blob `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`
- Blob `src/emergenz_knoten/rotating_wave_stability_gate.py`: `630beb9952abefea823d91388dcbb2de8f1a2927`
- Blob `src/emergenz_knoten/strict_json_contract.py`: `221372ea86f857aa4141e2609e46a0dc536c1ab4`
- Blob `tests/test_rotating_wave_horizon_g1_g3_bridge.py`: `ff03773e768ff97d49c369292f5350254cd7fccf`
- Blob `tests/test_rotating_wave_horizon_g1_g3_execution.py`: `fc3632b4b3d3a182cb9faca8c870cce9dcae9922`
- Blob `tests/test_rotating_wave_horizon_transfer.py`: `6fe72c69c00cbabc02b9f9395cf92b5cbad4cbd0`

## Readinessentscheidung

Es liegt kein Critical- oder Major-Codebefund im geschuetzten Pfad vor. Die
Readiness-Luecke aus Versuch 1 ist adversarial abgedeckt, die
wissenschaftlichen Parameter und Schwellen sind unveraendert, und die
Ausgabepfade koennen Versuch 1 nicht ueberschreiben.

Damit ist der Implementierungscommit fuer **genau einen** moeglichen
Attempt-2-Zugriff bereit. Governance bleibt dennoch geschlossen. Ein Lauf
erfordert weiterhin eine neue ausdrueckliche Nutzerfreigabe, eine frische
UUID und einen governance-only Autorisierungscommit, der diesen
Implementierungscommit, diesen Readinessreview, die Blobtabelle und CI-Run
`36354118411` bindet.
