# Review: targetfreie Horizont-Runner-Orchestrierung

Datum: 2026-09-09.

Gepruefte Revision:
`39c60cfc37ff4c774db908e8cc7512f708f5eaa5`.

Gepruefte CI:
[GitHub Actions run 34379011031](https://github.com/MemoryDynamics/Knoten/actions/runs/34379011031).

Verdict:
**`rotating-wave-horizon-orchestration-pass-scientific-backends-incomplete-target-closed`**.

Dieses Urteil betrifft ausschliesslich die targetfreie Orchestrierung und die
Rekonstruktion ihrer gespeicherten Evidenzbeziehungen. Es ist kein Root-,
Horizonttransfer-, Stabilitaets- oder P5-D-Ergebnis.

## 1. RED-Grenzen

Die drei ersten Orchestrierungstests wurden an Revision
`c61b822` vor dem Symbol `orchestrate_horizon_transfer` eingefroren. Der
fokussierte Lauf bestand 46 Altfaelle und scheiterte exakt an den drei neuen
Faellen. Geprueft wurden die registrierte Stufenreihenfolge ohne Publikation,
ein Newtonstopp mit unabhaengiger Rueckwaertsbelastung und partielle
Arnoldi-Ausgabe ohne erfundene Trajektorien.

Weitere Tests decken Homotopie-Praefixstopp, Tailpanel-Abbruch und fruehen
Trajektorienstopp ab. Der Orchestrator erhaelt primitive Backendrecords und
rekonstruiert Rootpanels, Schnitte, Drift, Tailvergleich,
Arnoldi-Panelvergleich, Gates und finale Praezedenz selbst. Eine fertige
Pass-Payload kann das Backend nicht einspeisen. Ohne expliziten
Publikationsaufruf wird kein Pfad geschrieben.

## 2. Korrektur des vorausgehenden v3-Reviews

Ein Referee-Counterexample nach der ersten gruenen Orchestrierung zeigte,
dass Validator und Auditor zwar jeden Ausschlussleaf prueften, aber nicht die
lueckenlose Partition der lokalen Domain. Ein einzelnes korrekt
residualausschliessendes Halbblatt wurde deshalb faelschlich als vollstaendiger
lokaler Branchverlust akzeptiert. Der rote Counterexample ist Revision
`9f4e750`.

Damit war das vorausgehende v3-Vertragsreview hinsichtlich negativer
Branch-loss-Evidenz zu positiv. Die gespeicherten v3-Felder reichen jedoch zur
Korrektur aus; Schema und wissenschaftliches Protokoll mussten nicht geaendert
werden.

Validator und unabhaengiger Standardbibliothek-Auditor rekonstruieren nun
getrennt:

- die exakte, am 120-dps-Vorgaengerroot gebundene und mit der Domain
  geschnittene Ausschlussbox;
- jeden Leafpfad der festen Halbierung entlang der laengeren normalisierten
  Kante bis zur gespeicherten Tiefe;
- Praefixfreiheit der dyadischen Pfade;
- exakte Vollstaendigkeit ueber die Summe ihrer dyadischen Gewichte;
- den Widerspruch zwischen vollstaendigem Ausschluss und einem zertifizierten
  Zielroot innerhalb derselben Domain.

Die diskriminierende Testmatrix verwirft eine Halbpartition, akzeptiert eine
vollstaendige Zwei-Blatt-Partition nach Rootstopp und verwirft dieselbe
Partition bei vorhandenem Zielroot.

## 3. Verifikation und Bindung

- 70/70 fokussierte Validator-, Orchestrierungs- und Auditor-Tests bestanden
  lokal;
- 1015/1015 Repositorytests bestanden in der offiziellen Linux-CI;
- Ruff und strikter MkDocs-Bau bestanden dort ebenfalls;
- Gate-/Orchestratorblob:
  `3d349f6ef4190a75d2e31bdd718acae3c56ba463`;
- unabhaengiger Auditorblob:
  `12aa7285394b11d0887374f7d490ef23e8762767`;
- Gate-/Orchestrierungstestblob:
  `7ea06bb4dd645b17781432ab26cc09599b402c0a`;
- Auditor-Testblob:
  `cfca89af5c4dbf1289fe021743578cd5962233d2`.

Ergebnis-JSON, lesbarer Ergebnisbericht, Publikationsmanifest,
Audit-Ergebnis und Ergebnisreview blieben abwesend.

## 4. Verbleibende Grenze

Die injizierten Donorbackends sind synthetische Testfixtures. Es fehlen die
wissenschaftlichen Implementierungen fuer Newtonpanels, Krawczyk-Root- und
Homotopiezertifikate, den Ausschlussbaum, Tailzertifikate, Arnoldipanels und
Trajektorienarme. Der unabhaengige Auditor reproduziert diese Numerik nicht.

Naechster zulaessiger Schritt ist ausschliesslich die targetfreie
Implementierung und Falsifikation dieser wissenschaftlichen Backends gegen
die bestehende Orchestrierung. Danach sind ein separates Readinessreview,
ein sauberer Commit und gruene exakte CI erforderlich. Horizontlauf und
P5-D-Versuch 4 bleiben geschlossen.
