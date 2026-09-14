# Meta-Review: vom isolierten G4-Beleg zu G5

Datum: 2026-09-14.

Ausgangsrevision: `625b822d03ab64cdb2965b5820227a57387c00b8`.

Verdict:
**`g4-evidence-chain-reviewed-local-pass-g5-red-remediation-required`**.

## 1. Gegenstand und Methode

Geprueft wurden die registrierte G4-Mathematik, Komponentenrunner,
Ergebnisvalidator, Standardbibliothek-Auditor, Publikationsmanifest und
Claimabbildung. Fuer den Uebergang zu G5 wurden ausserdem der gemeinsame
Voll-FIFO-Jacobian, die Arnoldi-/Fortsetzungsbibliothek, der v3-
Horizontvertrag, die Orchestrierung und deren synthetische Tests verfolgt.

Es wurde weder der G4-Ziellauf wiederholt noch ein H=2400-Spektrum oder eine
Stoerungstrajektorie ausgewertet. Dieses Review ist zugleich die RED-
Spezifikation fuer den naechsten targetfreien Codeblock.

## 2. G4-Evidenzkette

Der korrigierte Retry ist an den Ausfuehrungscommit `fb1cc7d` und den Hash
des separaten Retry-Protokolls gebunden. Ergebnis-JSON und Lesereport sind im
Manifest gehasht. Zwei 120-/160-dps-Rechnungen desselben Intervallbackends
ergeben strikte, ueberlappende Krawczyk-Bilder mit deutlichem Abstand zum
Rand der registrierten Box. Der getrennte Auditor rekonstruiert Schema,
Hashes, Tailbounds, Inklusionen, Ueberlappung und Entscheidung ohne Import
des Runners.

Kein kritischer Implementierungs- oder Claimfehler wurde in dieser Kette
gefunden. Tragbar bleibt ausschliesslich lokale Existenz und lokale
Eindeutigkeit des Roots von $F_\infty$ unter den registrierten Tailbounds und
der Trust Base `mpmath.iv==1.3.0`.

## 3. Verbleibende G4-Grenzen

Die 120-/160-dps-Panels sind eine Praezisionskontrolle, keine unabhaengige
Intervallreplikation. Der Standardbibliothek-Auditor prueft den Record, fuehrt
aber keine zweite Intervallrechnung aus. G1--G3 verbinden den isolierten
$F_\infty$-Root noch nicht mit der gesamten endlichen Leiter. G4 beweist
weder dynamische Stabilitaet noch Attraktion, Formation, Schleifentransfer,
Interaktion, interne $S^1$-Phase, Traegheit oder Masse.

Die Publikationsrevision `625b822` ist notwendig spaeter als der gebundene
Ausfuehrungscommit: Der Lauf erzeugte erst die anschliessend reviewten
Artefakte. Das Manifest macht diese zweistufige Provenienz explizit; sie ist
kein Selbstbeleg des Ergebniscommits.

## 4. G5-Codebefunde

1. **Hoch -- wissenschaftlicher Adapter fehlt.** Die Orchestrierung besitzt
   nur ein injiziertes Backendinterface und synthetische Donorrecords. Es
   existiert noch keine schmale Abbildung vom gemeinsamen sparse Voll-FIFO-
   Jacobian und der Fortsetzungsbibliothek in den v3-Record. Ein aktueller
   Zielaufruf koennte daher keinen reproduzierbaren wissenschaftlichen G5-
   Record erzeugen.
2. **Hoch -- vorgeschriebener Arnoldi-Start erreicht ARPACK noch nicht.**
   `run_eigen_panel` erzeugt intern die historischen trigonometrischen
   Starts `S1/S2`. G5 verlangt stattdessen die zwei eingefrorenen 32-bit-LCG-
   Vektoren unveraendert als `v0`. Der vorhandene Kern kann diese Vektoren
   noch nicht entgegennehmen.
3. **Hoch -- v3-Ritzvektoren fehlen am Bibliotheksrand.** Der gemeinsame
   Klassifikator speichert Eigenwert, Residuum und Symmetrieueberlappung,
   aber nicht den zugehoerigen komplexen Ritzvektor. Der v3-Vertrag verlangt
   fuer jedes der 24/36 Slots einen 4800-komponentigen Vektor oder explizit
   `null`; ohne opt-in Vektorausgabe ist der Nachweisrecord unvollstaendig.
4. **Mittel -- Instabilitaetsbezug ist zu locker.** Runner und Auditor
   verlangen bisher je Panel irgendeinen transversalen Modul oberhalb
   `1+1e-6`, waehrend die Paneluebereinstimmung ein bestimmtes primaeres
   Ritzpaar matched. Damit koennte theoretisch ein anderes, ungematchtes
   Konvergenzpaar die Instabilitaet liefern. Der Claim muss an dasselbe
   gematchte Paar in beiden Panels gebunden werden.
5. **Mittel -- Fortsetzungen werden zu frueh freigegeben.** Die
   Orchestrierung startet Stoerungsarme bereits, wenn beide Backends
   `status=complete` melden. Kardinalitaet, Vektoren, Residuen,
   Symmetriemoden und Panelmatch werden erst spaeter validiert. Vor einer
   Zielrechnung muessen diese Voraussetzungen fail-closed geprueft werden.
6. **Niedrig -- Portabilitaetsgrenze der Vollhistorien-Stoerung.** Ihr
   vorgeschriebenes `sin`/`cos`-Profil wird zwar mit geordneter `fsum`-
   Projektion rekonstruiert, bleibt aber libm-abhaengig. Vor dem Ziel ist
   mindestens ein Cross-Process-Hash-Replay auf derselben Plattform und eine
   dokumentierte Cross-Platform-Grenze erforderlich; ein Plattformvergleich
   darf nicht stillschweigend behauptet werden.

## 5. Targetfreie Remediation

Der kleinste zulaessige G5-Codeblock muss:

1. den gemeinsamen Arnoldi-Kern rueckwaertskompatibel um einen expliziten,
   validierten Startvektor und opt-in Ritzvektorspeicherung erweitern;
2. einen registrierten H=2400-Adapter bauen, der exakt 24/36 Slots,
   Solverparameter, LCG-Hashes, Status und Nullsuffixe erzeugt;
3. die drei registrierten Stoerungsvektoren sowie den exakten Arm durch den
   gemeinsamen Fortsetzungskern in je 501 positionsgebundene Samples
   abbilden;
4. Instabilitaet nur aus dem tatsaechlich gematchten Ritzpaar beider Panels
   ableiten;
5. Fortsetzungen nur nach strukturell vollstaendigen, residualgueltigen,
   symmetriekonsistenten und gematchten Panels starten;
6. dieselbe Entscheidungslogik getrennt in Runner und Auditor korrigieren;
7. alle Schritte mit kleinen synthetischen Positiv- und Mutationszeugen
   pruefen, ohne den registrierten H=2400-Kandidaten zu oeffnen.

## 6. Falsifikationstests vor einem Zielzugriff

Ein targetfreier Pass verlangt mindestens: bitgenaue LCG-Weitergabe bis zum
gemockten ARPACK-Aufruf; Ablehnung falscher Dimension, NaN, Nullvektor und
mutiertem LCG-Start; vollstaendige komplexe Vektorserialisierung; korrekte
Statusabbildung fuer partielle Eigenpaare, fehlende Vektoren, nichtendliche
Werte und Residualfehler; kein Fortsetzungsaufruf nach jedem dieser Fehler;
Ablehnung einer Instabilitaet, die nur von einem ungematchten zweiten
Panelpaar getragen wird; korrekte Nullsuffixe nach fruehem Trajektorienstopp;
und Uebereinstimmung von Runner- und Auditorentscheidung auf denselben
Mutationen.

## 7. Entscheidung

Der isolierte G4-Beleg bleibt nach Meta-Review bestehen. G5 ist dagegen
weiterhin ungemessen und nicht zielbereit. Autorisiert ist ausschliesslich
die targetfreie Remediation aus Abschnitt 5 mit den Falsifikatoren aus
Abschnitt 6. Erst ein separates Readinessreview nach gruener exakter CI darf
ueber einen H=2400-Zugriff entscheiden. Der vollstaendige Horizontlauf,
P5-D-Versuch 4 und der historische Zwei-Knoten-G4-Transfer bleiben
geschlossen.
