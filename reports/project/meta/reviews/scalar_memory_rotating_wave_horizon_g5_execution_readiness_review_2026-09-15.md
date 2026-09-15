# Readinessreview: isolierter G5-Ausfuehrungskontext

Datum: 2026-09-15.

Implementation revision: `060fcf3a6bb261738973bc2fcb07d687e2173107`

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

## 2. Finales Skript-Metareview

Der tatsaechliche Zielpfad wurde Datei fuer Datei und entlang seiner
Aufrufreihenfolge erneut geprueft:

1. `scalar_memory_rotating_wave_horizon_g5_execution.py` prueft Governance,
   Review, CI, Git-/Upstreamzustand, Dependencies und Zielpfade vor jeder
   Numerik und erzeugt erst danach exklusiv die Attempt-Receipt.
2. Komponentengate, Ergebnisschema, strikter JSON-Validator und unabhaengiger
   Auditor erzwingen exakte Felder, fail-closed Stufen, Receiptbindung,
   Entscheidungsrekonstruktion und manifest-last-Publikation.
3. `scalar_memory_rotating_wave_horizon_transfer_gate.py` bildet den
   isolierten G5-Aufruf auf finite Rootzertifikate, Grundgleichungs-Preflight,
   zwei Arnoldi-Panels und vier Voll-FIFO-Fortsetzungen ab.
4. `rotating_wave.py` und `rotating_wave_interval.py` liefern Kernelgradient,
   exakte finite Balance, Newtonverfeinerung und Krawczyk-Intervallrechnung.
5. `rotating_wave_stability.py`, `rotating_wave_horizon_stability.py` und
   `rotating_wave_stability_gate.py` liefern nativen FIFO-Shift,
   mitrotierenden Voll-Jacobian, Symmetriebasen, LCG-Arnoldi und nichtlineare
   Fortsetzung.
6. `requirements.txt` und der Laufzeitcheck binden Python 3.12 sowie NumPy
   2.3.5, SciPy 1.17.1 und mpmath 1.3.0; lokal wurden Python 3.12.14 und genau
   diese Paketversionen geladen.
7. Komponenten-, Execution-, Intervall-, Voll-FIFO- und Stabilitaetstests
   decken positive Vertragsanwendung und adversariale Abweichungen ab.

Das Review fand zunaechst einen Major-Befund: Intervallkern,
Stabilitaets-Gate-Kern und `rotating_wave.py` waren direkte beziehungsweise
transitive Laufzeitabhaengigkeiten, aber noch nicht explizit in der
Blob-Sperre enthalten. Die Remediation nimmt diese Dateien und
`requirements.txt` auf. Zusaetzlich verwirft der Guard nun jede seit der
Implementation revision geaenderte Nicht-Markdown-Datei ausser dem
Governance-Record. Der neue Mutationsfall `source-drift` bestaetigt den
Abbruch vor Receipt. Nach dieser Korrektur verbleibt kein Major- oder
Critical-Codebefund.

## 3. Reproduzierbare Nachweise

- Lokale Vollregression: `1118 passed in 340.40s` unter Windows.
- Fokussierte G5-Abhaengigkeitsregression: `65 passed in 10.51s`.
- Vollstaendiger Python-Lintumfang: Pass.
- Strikter MkDocs-Bau: Pass.
- Offizielle Linux-CI: [GitHub Actions run 35018526023](https://github.com/MemoryDynamics/Knoten/actions/runs/35018526023),
  `completed/success`, Head-SHA identisch zur Implementation revision.
- Reale Closed-Probe in der vorgesehenen Laufzeit: Abbruch vor Modulimport,
  Receipt und Zielartefakten mit `G5 target sealed by machine governance`.
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

## 4. Geschuetzte Implementierungsobjekte

- Blob `requirements.txt`: `257723e469e56d5e1db0efcaff57c26e71a9ebf5`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g5_component_protocol_2026-09-14.md`: `9815604436b93054097c69c0de1b4d49cfee1778`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_schema_v1.json`: `8c3aa7582e1c693452906db840b68b369c603529`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_gate.py`: `c2e6f99e7fb167ebf5fd28068e4a5adc4bd69a66`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_result_audit.py`: `9370a94c0bfc6c078f16f93597199ed365625ece`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_execution.py`: `b8bd15b8d6ac465f1cd32b608a7af4275ca04c2b`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_gate.py`: `1f6ed63a92eb12812a4c7d31ad39b0d70b146eb9`
- Blob `src/emergenz_knoten/rotating_wave.py`: `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d`
- Blob `src/emergenz_knoten/rotating_wave_interval.py`: `e269e729c68c8030a6aae222fb4fa67069dd46fd`
- Blob `src/emergenz_knoten/rotating_wave_horizon_stability.py`: `95788e2abf54f71646b4cbc3490624b53f4d6c62`
- Blob `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`
- Blob `src/emergenz_knoten/rotating_wave_stability_gate.py`: `630beb9952abefea823d91388dcbb2de8f1a2927`
- Blob `src/emergenz_knoten/strict_json_contract.py`: `221372ea86f857aa4141e2609e46a0dc536c1ab4`
- Blob `tests/test_rotating_wave_horizon_g5_component.py`: `5d30e8fa8302ca8ab1a16d4e5f94cef3d6271058`
- Blob `tests/test_rotating_wave_horizon_g5_execution.py`: `0319513f9ab1dade8bed55c97e53ab99f37cf9c1`

Der geschlossene Governance-Blob im Implementierungscommit ist
`45411c90d4c1ff50aac4d2d5ed3d034e4f5996e4`. Eine spaetere Freigabe muss
diesen Ausgangszustand binden; sie darf ausschliesslich den Governance-Record
aendern.

## 5. Kritische Grenzen

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

## 6. Entscheidung

Es verbleibt kein Major- oder Critical-Codebefund, der die Vorbereitung eines
einzelnen G5-Zielversuchs blockiert. Die Implementation revision ist daher
targetfrei ausfuehrungsbereit. Die getrackte Governance bleibt absichtlich
geschlossen. Der naechste zulaessige Schritt ist ausschliesslich eine
ausdrueckliche Nutzerentscheidung ueber einen Governance-only-
Autorisierungscommit fuer Attempt 1; erst ein weiterer Turn darf danach den
einmaligen Zielzugriff ausloesen.

## 7. Erneuter Gesamtpfadreview nach Nutzerentscheid

Nach Offenlegung der behobenen Provenienzluecke hat der Nutzer am 2026-09-15
die Autorisierung fuer denselben Ablauf ausdruecklich erneuert. Daraufhin
wurde der targetfreie Importpfad ein weiteres Mal real geladen. Durch die
eager Exporte in `emergenz_knoten.__init__` wurden dabei 60 lokale Module
importiert; nur die in Abschnitt 2 genannten Rotating-Wave-Module sind am
numerischen Zielpfad beteiligt. Der breite Import ist eine verbleibende
Hygienegrenze, aber kein Ergebnis- oder Readinessblocker: Zwischen
Implementation revision und aktuellem Review besteht fuer keine Python-Datei
und nicht fuer `requirements.txt` ein Drift, und der Guard erzwingt dies vor
Receipt-Erzeugung erneut.

Die fokussierte Suite besteht im Wiederholungslauf mit `65 passed in 8.05s`.
Es trat kein weiterer Major- oder Critical-Befund auf. Damit ist als naechster
Schritt der Governance-only-Autorisierungscommit fuer Attempt 1 zulaessig.
Bis zu dessen erfolgreicher Validierung bleiben Receipt, Ziellauf und
G5-Ergebnis weiterhin ausstehend.
