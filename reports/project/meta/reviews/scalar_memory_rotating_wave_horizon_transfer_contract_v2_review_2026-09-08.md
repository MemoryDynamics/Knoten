# Review: Horizonttransfer-Ergebnisvertrag v2

Datum: 2026-09-08.

Gepruefte Implementierungsrevision:
`b7b75be328de766de73fed61407b13dd67315060`.

Gepruefte CI:
[GitHub Actions run 34277675627](https://github.com/MemoryDynamics/Knoten/actions/runs/34277675627),
erfolgreich fuer die exakte Implementierungsrevision.

Verdict:
**`rotating-wave-horizon-transfer-contract-v2-pass-runner-red-open-target-closed`**.

Der v2-Vertrag schliesst die im vorausgehenden Negativreview gefundenen
Serialisierungswidersprueche. Er kann vollstaendige und abgebrochene
Experimente ohne erfundene numerische Werte darstellen. Der
wissenschaftliche Runner fehlt weiterhin; weder dieser Review noch der
Vertrag autorisiert einen Horizontlauf oder P5-D.

## 1. Prospektive Reihenfolge und Bindung

Der negative Befund wurde zuerst separat an Revision
`adb5c2445a63265b96ceee1c1cfd98a1f7017c` festgehalten. Danach wurde die
Null-/Abbruchsemantik prospektiv amendiert und der neue Schemapfad in
Revision `a3c244335bc281dd6ed11a9eeb98275bddfd5a45` eingefroren. Der v2-Vertrag
bindet genau diese Protokollrevision und den Protokollblob
`4a24d536275eecc91aea0dcc670feb34152111fb`.

Gebundene v2-Artefakte:

- Gate-/Validatorblob: `b7cd43664ffb5aa7180e9e86c597bed068a8af51`;
- unabhaengiger Auditorblob: `74111ed641e88099ca7f705fa571b04c604493fb`;
- Schemablob: `0557498a24afa68e5cdc0babac5725d6a0545342`;
- Gate-Testblob: `72304311eb4972cef91c883713aefa4e88f6a6b5`;
- Auditor-Testblob: `ea680fbebfd5c86f26968ff58ce4114ab884943c`.

Die Blobwerte wurden am Reviewcommit erneut gegen die gepruefte Revision
ermittelt. Der historische v1-Vertrag wurde nicht still umgedeutet, sondern
durch den expliziten v2-Pfad ersetzt.

## 2. Geschlossene Befunde

### 2.1 Abhaengige Root- und Homotopieabbrueche

Die sieben Rootslots bleiben horizontgebunden. Vorwaerts- und
Rueckwaertsabhaengigkeiten verbieten innere Luecken, lassen die getrennte
lower-tail-Leiter aber unabhaengig auswerten. Die sechs Homotopieslots sind
an ihre Kanten gebunden; innerhalb jeder 64-Scheiben-Homotopie bilden
ausgewertete Scheiben ein nicht-null Praefix. Ein Pass erfordert alle 64
streng inneren, paarweise ueberlappenden Einschluesse.

Der lokale Ausschlussfalsifikator besitzt nun vier positionsgebundene
Vorwaertsslots und einen vollstaendigen terminalen Leafrecord. Nur wenn alle
Leaves als Residualausschluss klassifiziert sind, darf
`local_branch_excluded=true` werden. Ein anderer Krawczyk-Root oder ein
ungeloestes Leaf verhindert den Branch-loss-Claim.

### 2.2 Partielle Arnoldi- und Trajektorienausgaben

Die festen 24/36 Eigenpaarslots erlauben jetzt `null` fuer nicht
zurueckgegebene Paare und `vector=null` fuer einen fehlenden Vektor. Nicht-null
Paare muessen ein Praefix bilden. `status=complete` verlangt volle
Kardinalitaet und alle Vektoren.

Jeder Trajektorienarm behaelt 501 feste Sampleslots. Bei einem fruehen Stopp
bleibt nur das tatsaechlich berechnete Praefix belegt; spaetere Slots sind
`null`. Ein kompletter Arm verlangt alle Samples und `stopped=false`.

### 2.3 Summary- und Gate-Rekonstruktion

Runner-Validator und Standardbibliothek-Auditor rekonstruieren unabhaengig:

- q-Darstellungen, Tailbounds und beide Driftobergrenzen;
- Root-, Homotopie- und Tail-Voraussetzungen;
- Panelvollstaendigkeit und Ritzresiduen bis `1e-8`;
- stabile transversale Moduli, Kontraktion, exakten Arm sowie die gemeinsame
  Spektrum-plus-Wachstumsbedingung fuer Instabilitaet;
- neun Shift/Circular-Faelle, sieben `eta=0`-Faelle und alle vier
  registrierten Mutationen;
- `local_branch_excluded`, `large_h_instability_supported`,
  `finite_large_h_stability_only` und die siebenstufige finale
  Entscheidungsrangfolge.

Ein manuell gesetztes positives Summary- oder Gatefeld kann fehlende
Evidenz daher nicht ersetzen. Null-Loch-, False-G1F-, falsche
Stability-Summary-, falsche Control-Summary- und falsche Instabilitaetsfelder
werden in targetfreien Mutationstests verworfen.

## 3. Verifikation

- 47/47 fokussierte Vertrags- und Auditor-Tests bestanden;
- 992/992 Repositorytests bestanden lokal;
- der konfigurierte Ruff-Umfang bestand;
- die offizielle CI bestand Tests und strikten Dokumentationsbau auf der
  exakten Implementierungsrevision;
- Ergebnis-JSON, lesbarer Bericht, Publikationsmanifest und unabhaengiger
  Auditoutput waren vor und nach allen Tests abwesend.

## 4. Verbleibende Grenzen

- Der Vertrag validiert gespeicherte Krawczyk-Bilder, Eigenpaare und
  Trajektorienkonsistenz, reproduziert deren wissenschaftliche Numerik aber
  nicht. Diese Vertrauensgrenze bleibt bis zum Runner- und Ergebnisreview
  ausdruecklich offen.
- Ein struktureller `inconclusive`-Record beweist keinen Branchverlust und
  keine Instabilitaet.
- Der lokale Ausschlussbaum kann im Extremfall gross werden; seine feste
  Tiefengrenze und nichtadaptive FIFO-Reihenfolge duerfen im Runner nicht
  optimiert oder ersetzt werden.
- Der Vertrag enthaelt noch keine wissenschaftliche Zahl aus dem
  Horizontpanel. Alle Passdaten der Tests sind synthetische Witnesses.

## 5. Naechste Grenze

Geoeffnet ist ausschliesslich ein neuer targetfreier RED-Schritt fuer die
Runner-Orchestrierung. Die Tests muessen feste Newtonstarts und
Praezisionspfade, 64-Scheiben-Stopp, Ausschlussbaum, Tail-Krawczyk,
H=2400-Arnoldi-Konfiguration, drei Stoerungsarme und den exakten Arm mit
synthetischen Backends pruefen. Registrierte Roots, Trajektorien und
Ausgabepfade muessen dabei durch Traps geschlossen bleiben.

Erst nach Implementierung, separatem Readinessreview, sauberem Commit und
gruener exakter CI kann genau ein Horizontlauf zur ausdruecklichen
Nutzerentscheidung gestellt werden. P5-D-Versuch 4 bleibt davon getrennt
und geschlossen.
