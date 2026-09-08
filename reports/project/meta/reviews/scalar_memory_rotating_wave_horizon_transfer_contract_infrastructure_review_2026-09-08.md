# Infrastrukturreview: Rotating-wave-Horizonttransfer-Vertrag

Datum: 2026-09-08.

Gepruefte Implementierungsrevision:
`f19c6cf229c96606761387399294a6247dde6408`.

Gepruefte CI:
[GitHub Actions run 34195396985](https://github.com/MemoryDynamics/Knoten/actions/runs/34195396985),
erfolgreich fuer die exakte Implementierungsrevision.

Verdict:
**`rotating-wave-horizon-transfer-contract-infrastructure-pass-runner-incomplete-horizon-run-closed`**.

Die targetfreie Infrastruktur setzt Ergebnisvertrag, Formeln,
Speicherfalsifikatoren, Entscheidung und Publikationsgrenze hinreichend um.
Sie ist noch kein ausfuehrbarer wissenschaftlicher Horizont-Runner: feste
Newtonleiter, Krawczyk-Homotopie, Tail-Zertifizierung, Arnoldi-Holdout und
Stoerungstrajektorien fehlen weiterhin. Dieses Urteil ist keine numerische
Horizont-, Root-, Stabilitaets- oder Interaktionsevidenz. Horizontlauf, P5-D
und Versuch 4 bleiben geschlossen.

## 1. Gebundene Implementierung

- Ergebnisvertrag, Blob `959630a5057eac7f756a5b844b24319436457106`;
- targetfreies Gate-Modul, Blob `afe11fad01c953e7efdf9442f578f5cc01636c04`;
- unabhaengiger Auditor, Blob `cdd0adfee06f2de3ea3341c60799725bfccf7ff8`;
- Gate-Tests, Blob `e94881684483932a1d281e1119db27fae4cc09cd`;
- Auditor-Tests, Blob `715c9be5bef340b399dd640f48bfcb49f872154e`;
- vorausgehendes RED-Review, Blob
  `bc3dbe4db4b467476c814ebfdb73137238c78be1`.

Die prospektive Evidenzrevision, sieben Inputblob-IDs, Protokollrevision und
Protokollblob sind im Vertrag als Konstanten gebunden. Unbekannte Felder,
NumPy-Skalare auch innerhalb konstanter Listen, nichtendliche Zahlen,
falsche Kardinalitaeten und nichtregistrierte Pfade schliessen fail-closed.

## 2. Failing-to-passing evidence

Der isolierte RED-Commit `66644f4b0c708bf71f250610e47d759ecb8e4679`
bestand genau zwei reine Vertragsstrukturtests und scheiterte an 28
benannten, noch fehlenden Implementierungsgrenzen. Der unveraenderte
Bestandstest bestand separat mit 945 Tests.

Nach Implementierung und Review-Hardening bestehen:

- 40/40 targetfreie Horizonttransfer- und Auditor-Tests;
- 985/985 Repositorytests;
- der vollstaendige in CI konfigurierte Ruff-Umfang;
- strikter MkDocs-Bau;
- die offizielle CI auf der exakten Implementierungsrevision.

Die vier registrierten Ergebnis-, Report-, Manifest- und Auditpfade waren
vor und nach den Tests abwesend. Statische Inspektion findet im neuen
Gate-Modul weder Root-Refiner noch Krawczyk-Aufruf, Eigenwertsolver,
`run_gate`, Programmeinstieg oder registrierten Ausgabepfad.

## 3. Geschlossene Infrastrukturgrenzen

### 3.1 Formeln und Repraesentationen

Das finite Residual und sein analytischer Jacobian werden an einer kleinen,
nicht registrierten H=17-Zelle gegen direkte Summe und zentrale Differenzen
geprueft. `q64**H` und `exp(H*log(q64))` stimmen ueber die sieben Horizonte
innerhalb zwei ULP ueberein; `log1p` bleibt eine nicht entscheidende
Diagnostik.

Weil `0.99^H=99^H/100^H` endlich dezimal ist, speichert die Infrastruktur
diese Potenz fuer jeden Horizont vollstaendig und rundungsfrei. Die drei
Tailbounds werden aus Decimal-Arithmetik berechnet und als kleinster
darstellbarer konservativer binary64-Oberwert serialisiert.

### 3.2 Intervalle, Spektrum und Entscheidung

Die Drift verwendet Dezimalendpunkte und verliert deshalb auch
Zertifikatsbreiten unterhalb der binary64-Aufloesung nicht. Beide Komponenten
und ihr Maximum werden unabhaengig rekonstruiert. Eine Breitenmutation
schliesst das Driftgate.

Homotopieunterbrechungen werden ohne vollstaendigen lokalen Ausschluss nur
`inconclusive`. Arnoldi-Panels koennen nur mit exakt 24 beziehungsweise 36
endlichen Eigenpaaren, vollstaendigen 4800-komponentigen Vektoren und
Residuen bis `1e-8` bestehen. Partielle ARPACK-Ausgabe, fehlende Vektoren,
falsche Kardinalitaet und Grenzverletzung bleiben unentschieden.

Alle sieben Entscheidungsraenge sind getestet. Nur
`rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support`
setzt das Feld `p5_governance_review_open`; es autorisiert P5 dennoch nicht
selbst.

### 3.3 Speicher und Publikation

Das zyklische FIFO besitzt einen eigenen Head-, Modulo-, Kraftsummen- und
Overwrite-after-read-Pfad und ruft den Shift-Schritt nicht auf. Es stimmt an
zwei nichtkreisfoermigen Historien und den sieben publizierten
Anchor-Kreisgeschichten mit der Shift-Semantik ueberein. Reverse-Modulo,
Overwrite-before-read und falscher aeltester Slot werden diskriminiert. Alle
sieben Anchor-Historien kollabieren bei `eta=0` nach `H+1` Shifts auf den
neuesten Punkt.

JSON und Markdown werden vor dem Manifest atomar geschrieben und gehasht;
das Manifest enthaelt genau diese zwei Hashes und keinen Selbsthash. Der
Standardbibliothek-Auditor liest und hasht dasselbe zuerst gelesene Manifest,
prueft danach beide Inhaltshashes und erst anschliessend Schema und
Rekonstruktionen. Er importiert weder Runner noch Projekt-, NumPy-, SciPy-
oder mpmath-Code.

## 4. Testremediation nach dem RED-Commit

Zwei vorab committed Tests mussten vor dem Endurteil korrigiert werden. Beide
Korrekturen waren targetfrei und verschaerfen die Falsifikation:

1. Das erste Tail-Oracle verglich die hochpraezise Decimal-Schranke mit einer
   bereits gerundeten binary64-Naeherung von `exp(-1/2)`. Die korrekte
   Implementierung lag dadurch etwa `5e-15` konservativer als die zu enge
   Testobergrenze. Das neue Oracle verlangt, dass der publizierte Float ueber
   dem hochpraezisen Wert liegt und sein direkter Vorgaenger darunter.
2. Die erste Overwrite-before-read-Mutation verwendete einen aeltesten Punkt
   weit ausserhalb der effektiven Gauss-Kernelreichweite. Sein Beitrag war
   numerisch null und die Mutation nicht diskriminierbar. Die Ersatzhistorie
   bleibt nichtkreisfoermig, liegt aber im wirksamen Kernelbereich und laesst
   genau diese Mutation scheitern.

Zusaetzlich wurden nach dem RED-Review Provenienzkonstanten,
Sub-binary64-Drift, sieben Anchor-Horizonte und ein vollstaendiger
Auditor-Publikationsreplay als strengere Tests ergaenzt. Keine Aenderung
verwendete einen registrierten Root oder ein Horizontergebnis.

## 5. Verbleibende Grenzen und blockierender Befund

- Vertrag und Validator sind projektspezifisch, kein allgemeines
  JSON-Schema.
- Runner und Auditor duplizieren bewusst q-, Tail-, Drift- und
  Entscheidungslogik. Das reduziert Softwarekopplung, ersetzt aber keine
  mathematisch unabhaengige Herleitung.
- Vollstaendige komplexe Eigenvektoren machen das spaetere Ergebnis gross;
  das folgt aus der vorregistrierten Nachweispflicht.
- Der Auditor rekonstruiert keine Krawczyk-, Arnoldi- oder
  Trajektoriennumerik. Diese bleiben explizite Runner-Vertrauensgrenzen.
- Der bisherige Code implementiert nur die geprueften Infrastrukturteile.
  Die eigentliche feste Newtonleiter, 64-Slab-Homotopie,
  Tail-Krawczyk-Zertifizierung, H=2400-Arnoldi-Auswertung und
  Stoerungstrajektorien besitzen noch keinen Runnercode. Sie koennen deshalb
  auch nach einer Nutzerfreigabe derzeit nicht protokollkonform ausgefuehrt
  werden.

## 6. Entscheidungsgrenze

Der naechste Schritt ist die targetfreie Implementierung des fehlenden
wissenschaftlichen Runners hinter Tests, die jede Ausfuehrung registrierter
Roots, Arnoldi-Panels, Trajektorien und Ausgabepfade abfangen. Erst ein
weiteres separates Readinessreview auf einem gruenen exakten Commit kann
einen einzelnen Horizontlauf zur ausdruecklichen Nutzerentscheidung stellen.

Vor einer solchen spaeteren Autorisierung duerfen weder registrierte
Rootmittelpunkte noch Ergebnisartefakte erzeugt werden.

Ein Horizontpass koennte spaeter lediglich ein getrenntes
P5-D-Governancereview oeffnen. Er rekonstruiert Versuch 3 nicht und
autorisiert Versuch 4 weder automatisch noch rueckwirkend.
