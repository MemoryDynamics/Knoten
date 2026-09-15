# Readinessreview: isolierter G5-Ausfuehrungskontext

Datum: 2026-09-15.

Implementation revision: `a196e324fe06993bcc8424c48ea5582706995cff`

Verdict: **`g5-implementation-ready-target-closed`**

Dieses Verdikt betrifft ausschliesslich die targetfreie Implementierung. Es
ist weder ein G5-Pass noch eine Autorisierung des $H=2400$-Ziellaufs.

## 1. Gepruefter Umfang

Geprueft wurden der eingefrorene Ergebnisvertrag, die fail-closed
Stufenkomposition, der numerikfreie Record-/Publikationsauditor, der
one-shot-Ausfuehrungseinstieg und die geschlossene maschinenlesbare
Governance. Kein Arnoldi-Zielpanel, keine nichtlineare Stoerungstrajektorie
und kein anderer G5-Zielwert wurden berechnet.

Der Ausfuehrungseinstieg ist beim Import passiv. Vor dem Laden des
numerischen Komponentenmoduls verlangt er gemeinsam:

1. eine spaetere Governance-only-Einmalfreigabe;
2. den reviewed Implementierungscommit samt unveraenderten geschuetzten
   Blobs und Ergebnisvertrag;
3. erfolgreiche offizielle CI fuer genau diesen Commit;
4. den festgeschriebenen Python-3.12-/NumPy-/SciPy-/mpmath-Kontext;
5. einen sauberen, exakt mit Upstream synchronisierten Arbeitsbaum und
   unbenutzte feste Zielpfade.

Erst danach wird exklusiv eine Attempt-1-Receipt erzeugt. Ein Fehler nach
diesem Punkt verbraucht den Versuch; ein Fehler davor erzeugt keine Receipt.
Ergebnis, Lesereport und Manifest werden anschliessend gegen Receipt,
Autorisierung und Hashes zurueckgeprueft.

## 2. Reproduzierbare Nachweise

- Lokale Vollregression: `1116 passed in 337.81s` unter Windows.
- Fokussierte G5-/Stabilitaetsregression: `42 passed in 7.85s`.
- Execution-Guard nach Commit: `9 passed`.
- Vollstaendiger Python-Lintumfang: Pass.
- Strikter MkDocs-Bau: Pass.
- Offizielle Linux-CI: [GitHub Actions run 34999550617](https://github.com/MemoryDynamics/Knoten/actions/runs/34999550617),
  `completed/success`, Head-SHA identisch zur Implementation revision.
- Ein synthetischer vollstaendiger Sieben-Ebenen-Record mit 60 komplexen
  Ritzvektoren der Laenge 4800 und drei Trajektorien zu je 501 Samples wurde
  ohne numerischen Zielzugriff assembliert, auditiert, manifest-last
  publiziert und erneut auditiert. Seine JSON-Groesse betrug `19,498,703`
  Bytes (`18.595 MiB`) und blieb unter dem registrierten 30-MiB-Canary.

Die Mutationssuite verwirft unter anderem eine falsche Remote-Head-SHA,
abweichende Dependencies, einen veraenderten geschuetzten Blob, einen
gemischten Freigabecommit, ein abweichendes Readinessverdikt, eine
manipulierte Receipt und einen Null-Ritzvektor. Alle Kontextmutationen stoppen
vor Receipt-Erzeugung. Bei geschlossener Governance wird auch das numerische
Modul nicht geladen.

## 3. Geschuetzte Implementierungsobjekte

- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g5_component_protocol_2026-09-14.md`: `9815604436b93054097c69c0de1b4d49cfee1778`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_schema_v1.json`: `8c3aa7582e1c693452906db840b68b369c603529`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_gate.py`: `c2e6f99e7fb167ebf5fd28068e4a5adc4bd69a66`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_audit.py`: `9370a94c0bfc6c078f16f93597199ed365625ece`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_execution.py`: `246458cfece122a7fe1978b316d0eeab059a40ca`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_gate.py`: `1f6ed63a92eb12812a4c7d31ad39b0d70b146eb9`
- Blob `src/emergenz_knoten/rotating_wave_horizon_stability.py`: `95788e2abf54f71646b4cbc3490624b53f4d6c62`
- Blob `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`
- Blob `src/emergenz_knoten/strict_json_contract.py`: `221372ea86f857aa4141e2609e46a0dc536c1ab4`
- Blob `tests/test_rotating_wave_horizon_g5_component.py`: `5d30e8fa8302ca8ab1a16d4e5f94cef3d6271058`
- Blob `tests/test_rotating_wave_horizon_g5_execution.py`: `f05b5208c3bd0af2f8fe7e4768aea14821ae50ee`

Der geschlossene Governance-Blob im Implementierungscommit ist
`45411c90d4c1ff50aac4d2d5ed3d034e4f5996e4`. Eine spaetere Freigabe muss
diesen Ausgangszustand binden; sie darf ausschliesslich den Governance-Record
aendern.

## 4. Kritische Grenzen

### Keine wissenschaftliche G5-Evidenz

Der echte finite Root, der Voll-Jacobian, beide Arnoldi-Panels und alle drei
nichtlinearen Arme bei $H=2400$ bleiben ungemessen. Die synthetische
Vollpublikation beweist nur die Tragfaehigkeit des Datenwegs.

### Begrenzte numerische Unabhaengigkeit

Der standardbibliotheksbasierte Auditor rekonstruiert Schema, Gates,
Schwellen, Panelmatch, Summaries, Receipt und Publikationshashes. Er berechnet
den sparse Jacobian, $Jv-\lambda v$ und die Symmetrieueberlappungen nicht aus
den gespeicherten Ritzvektoren neu. Ein spaeteres unabhaengiges numerisches
Replay bleibt staerkere Evidenz als dieser Audit.

### Ressourcen- und Plattformgrenze

Der 18.595-MiB-Canary deckt die JSON-Huelle ab, nicht Peak-RAM oder Laufzeit
des echten Eigensolvers. Paketversionen und die Python-3.12-Linie sind
gebunden; Python-Patchlevel, Betriebssystem und BLAS-Implementierung sind
nicht vollstaendig bitidentisch festgeschrieben. Deshalb bleiben gespeicherte
Vektoren, Residuen, Hashes und Panelvergleich unverzichtbar.

### Vertrauensbasis der Einmalfreigabe

Die technische Sperre ist eine Reproduzierbarkeitsgrenze, keine
Sicherheits-Sandbox. Sie vertraut auf Git-Objekte, die GitHub-API,
Dateisystem-Exklusivitaet und einen wahrheitsgemaess dokumentierten
Nutzerentscheid. Eine Freigabe ohne ausdruecklichen neuen Nutzerentscheid
waere trotz technisch gueltigem JSON methodisch unzulaessig.

## 5. Entscheidung

Es verbleibt kein Major- oder Critical-Codebefund, der die Vorbereitung eines
einzelnen G5-Zielversuchs blockiert. Die Implementation revision ist daher
targetfrei ausfuehrungsbereit. Die getrackte Governance bleibt absichtlich
geschlossen. Der naechste zulaessige Schritt ist ausschliesslich eine
ausdrueckliche Nutzerentscheidung ueber einen Governance-only-
Autorisierungscommit fuer Attempt 1; erst ein weiterer Turn darf danach den
einmaligen Zielzugriff ausloesen.
