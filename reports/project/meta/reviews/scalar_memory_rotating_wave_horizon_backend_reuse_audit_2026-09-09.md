# Audit: vorhandene Numerik fuer den Rotating-wave-Horizonttransfer

Datum: 2026-09-09.

Ausgangsrevision: `714f53d21c39ec5c074cf33245ac5b91fbe6fe86`.

Verdict:
**`horizon-backend-core-reuse-confirmed-protocol-adapters-incomplete-target-closed`**.

## 1. Frage und Methode

Geprueft wurde, ob die im Orchestrierungsreview pauschal als fehlend
bezeichneten wissenschaftlichen Backends bereits ganz oder teilweise im
Repository existieren. Ausgangspunkt war der kanonische
`docs/reference/experiment_catalog.md`; danach wurden die dort genannten
Runner, Bibliotheksimporte und direkten Tests bis zu ihren numerischen
Quellen verfolgt. Es wurde kein Root, Spektrum oder Trajektorienarm des neuen
Horizonttargets ausgewertet und kein reservierter Ergebnispfad geoeffnet.

Gebundene Ausgangsblobs:

- `src/emergenz_knoten/rotating_wave.py`: `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d`;
- `src/emergenz_knoten/rotating_wave_interval.py`: `58ce9b0862f980c17c691c4555557e8e363468a4`;
- `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`;
- `src/emergenz_knoten/rotating_wave_stability_gate.py`: `630beb9952abefea823d91388dcbb2de8f1a2927`;
- Fixed-gain-Kontinuumsrunner: `b1a9ac4c52ead908721bba51d3e4b8f83f3fca7f`;
- L3-Stabilitaetsrunner: `7fedba8309f9003bc7886e33361e2a5bde5122f3`;
- Horizont-v3-Gate: `3d349f6ef4190a75d2e31bdd718acae3c56ba463`.

## 2. Evidenz

1. Die exakte finite Summe, ihr analytischer 2x2-Jacobian, feste
   Multipraezisions-Newtoniterationen und lokale Krawczyk-Zertifikate sind
   bereits in `rotating_wave_interval.py` implementiert. Die Anchor-, Leiter-
   und L5-Experimente nutzen denselben Kern. Fuer das Horizontgate fehlt hier
   kein zweiter Solver, sondern ein schmaler Adapter fuer exakt acht Schritte,
   zwei feste Boxbreiten und den v3-Record.
2. Kreisgeschichte, native und mitrotierende FIFO-Map, exakter sparse
   Voll-FIFO-Jacobian und Quotientdistanz liegen in
   `rotating_wave_stability.py`. Arnoldi-Klassifikation und
   Stoerungsfortsetzung liegen in `rotating_wave_stability_gate.py` und wurden
   bereits am Anchor sowie an L3 eingesetzt.
3. Der vorhandene Arnoldi-Wrapper ist nicht unveraendert zulaessig: Er erzeugt
   seinen Start intern mit `sin`/`cos`. Genau diese Plattformannahme wurde im
   Horizont-v3-Vertrag falsifiziert. Der neue Adapter muss den eingefrorenen
   ganzzahligen LCG-Start direkt an ARPACK uebergeben; die anschliessende
   Klassifikation kann wiederverwendet werden.
4. Die Kontinuums-Reconciliation besitzt Multipraezisions-Newton und zwei
   Quadraturfamilien, aber kein outward-rounded Tail-Zertifikat. Sie ist eine
   wertvolle unabhaengige numerische Kontrolle, nicht der im Protokoll
   verlangte Existenzbeweis.
5. Fuer den 64-Scheiben-Homotopieschlauch, die vollstaendige lokale
   Ausschlusssuche und das tail-augmentierte Krawczyk-Panel existiert kein
   fertiger Backendadapter. Der Intervallkern ist jedoch vorhanden und soll
   erweitert statt dupliziert werden.

## 3. Korrektur der bisherigen Aussage

Die Formulierung, Newton-, Krawczyk-, Arnoldi- und Trajektorienbackends
"fehlten", war zu grob. Richtig ist:

- **vorhanden und direkt wiederverwendbar:** finite Residuen/Jacobians,
  Punkt-Newton, finite Krawczyk-Boxen, FIFO-Map/Jacobian und
  Quotientdistanz;
- **vorhanden, aber protokollwidrig zu konfigurieren:** Arnoldi wegen des
  historischen libm-Starts sowie die bisher anders registrierten
  Stoerungsarme;
- **neu zu implementieren:** Homotopieintervalle, Ausschlussbaum,
  tail-augmentiertes Krawczyk-Zertifikat und die strikten v3-Recordadapter.

Historische Ergebnisrecords duerfen nicht als Backendwitnesses kopiert
werden. Wiederverwendung bedeutet erneute Berechnung durch gemeinsame
Bibliotheksfunktionen unter den eingefrorenen Parametern.

## 4. Folgerung und Stopregel

Die naechste RED-Stufe soll zuerst die gemeinsame Bibliotheksgrenze pruefen:
ein Rootadapter muss exakt die bestehenden Newton-/Krawczyk-Funktionen
aufrufen und v3-konform abbilden; Homotopie und Ausschluss muessen denselben
Intervallauswerter nutzen; Arnoldi muss den uebergebenen LCG-Vektor wirklich
bis ARPACK durchreichen. Erst danach folgen targetfreie Adapterimplementierung
und ein neues Readinessreview.

Dieser Audit ist Bestands- und Architekturbeleg. Er ist kein
Horizonttransfer-, Stabilitaets- oder P5-D-Ergebnis und autorisiert weder
einen registrierten Horizontlauf noch P5-D-Versuch 4.
