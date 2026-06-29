# Markov-/Transferoperator-Schicht: Anforderungen

Stand: 2026-06-29.

Dieses Dokument beschreibt, was die Markov-Schicht leisten muss, bevor darauf
weitere Evidenztabellen oder physikalischere Claims aufgebaut werden.

## Ziel

Die Schicht soll eine reproduzierbare, indexbasierte Pipeline bereitstellen,
mit der metastabile Regime des augmentierten Prozesses numerisch untersucht
werden koennen.

Sie soll nicht beweisen, dass die reduzierte Feature-Projektion exakt
markovsch ist. Sie soll messbar machen, wann diese Projektion als praktische
Operatorapproximation brauchbar oder unbrauchbar ist.

## Begriffliche Anforderungen

REQ-C1: Die API muss Update-Indizes und Sample-Indizes trennen.

- `n` bezeichnet Simulationsupdates.
- `i` bezeichnet gespeicherte Samples.
- `sample_lag` bezeichnet Sample-Abstand.
- `lag_updates` bezeichnet Update-Abstand.

REQ-C2: Die API darf keine physikalische Zeit voraussetzen.

- Namen wie `t`, `tau_phys` oder `physical_time` gehoeren nicht in die
  Basisschicht.
- `lag_time` darf nur als numerischer Nenner fuer Raten verwendet werden und
  muss so dokumentiert sein.

REQ-C3: Reduzierte Features muessen als verlustbehaftet markiert bleiben.

- `augmented_features` sind diagnostische Reprasentationen von `z_n`.
- Sie ersetzen nicht den vollstaendigen Zustand `(x_n, rho_n)`.

## Funktionale Anforderungen

REQ-F1: Feature-Bildung

Die Schicht muss aus Position, Memory-Buffer und Memory-Gewichten eine stabile
Feature-Matrix erzeugen koennen.

Akzeptanz:

- leere oder masselose Memory-Buffer werden definiert behandelt;
- negative Gewichte werden abgewiesen;
- Dimensionen werden validiert;
- Feature-Namen sind reproduzierbar.

REQ-F2: Lagged Dataset

Die Schicht muss Sample-Paare `(z_i, z_{i+ell})` erzeugen koennen.

Akzeptanz:

- `sample_lag >= 1` wird erzwungen;
- zu kurze Trajektorien werden abgewiesen;
- optionale `sample_steps` liefern `lag_updates`, wenn der Abstand konstant
  ist;
- nichtkonstante Update-Abstaende werden nicht stillschweigend zu einer
  falschen Zahl verdichtet.

REQ-F3: Transition Counts und Operator

Die Schicht muss aus diskreten Labels Transition Counts und zeilenstochastische
Matrizen bilden.

Akzeptanz:

- negative Labels werden abgewiesen;
- terminale leere Zeilen werden explizit behandelt;
- `empty_row="self"` und `empty_row="zero"` sind unterscheidbar;
- die Zahl leerer Zeilen bleibt im Ergebnis sichtbar.

REQ-F4: Validierung

Die Schicht muss mindestens einfache Operator-Diagnostiken liefern.

Akzeptanz:

- Eigenwerte werden nach Betrag sortiert;
- Unit-Modus und nichttriviale Modi werden unterscheidbar behandelt;
- implied timescales und relaxation rates akzeptieren einen numerischen Lag;
- Chapman-Kolmogorov-Fehler koennen fuer bekannte Matrizen getestet werden.

REQ-F5: Kompatibilitaet

Bestehende Paper-0-Imports ueber `emergenz_knoten.anchor` duerfen nicht
brechen.

Akzeptanz:

- `anchor.py` re-exportiert die relevanten Funktionen;
- die Paper-0-Pipeline importiert direkt aus `emergenz_knoten.markov`;
- bestehende Tests fuer `anchor.py` bleiben gruen.

## Nichtfunktionale Anforderungen

REQ-N1: Reproduzierbarkeit

Jeder experimentelle Lauf, der als Evidenz genutzt wird, muss mindestens
Parameter, Seeds, Git-Revision oder Arbeitsbaumstatus, Runtime-Hinweis und
Outputpfad dokumentieren.

REQ-N2: Kleine Abhaengigkeitsflaeche

Die Basisschicht bleibt NumPy-basiert. Methoden mit schwereren Abhaengigkeiten
wie PCCA, HMM, PMM, TICA oder EDMD duerfen spaeter additiv entstehen, aber
nicht den Minimalpfad blockieren.

REQ-N3: Testbarkeit

Neue Funktionen brauchen kleine deterministische Tests. Lange Simulationen
gehoeren nicht in die normale Testsuite.

REQ-N4: Claim-Hygiene

Operator-Spektren aus Transition-Matrizen duerfen nicht mit der bestehenden
geometrischen `spectral_dimension` verwechselt werden.

## Validierungsanforderungen vor P0.2

Bevor die naechste Evidenztabelle gebaut wird, muss die Schicht folgende
Checks bestehen:

1. Unit-Tests fuer Features, Lagged Datasets, Transition Counts, Matrix-
   Normalisierung, implied timescales und CK-Fehler.
2. Paper-0-Anchor-Pipeline laeuft mit Imports aus `emergenz_knoten.markov`.
3. MkDocs baut mit `--strict`.
4. Kuratierte Doku verwendet `z_n` fuer Update-Zustaende und `z_i` fuer
   Sample-Zustaende.
5. Historische Chatnotizen duerfen abweichen, werden aber nicht als
   kuratierte Quelle behandelt.

## Anforderungen an P0.2

Die spaetere Evidenztabelle muss mindestens enthalten:

- mehrere Seeds pro Parameterpunkt;
- explizites `sample_lag` und `lag_updates`;
- eine Lag-Sensitivitaetsvariante;
- eine Voxel- oder Feature-Sensitivitaetsvariante;
- eine Negativkontrolle, zum Beispiel `eta=0` oder shuffelte Memory-Features;
- maschinenlesbares Ergebnis unter `data/processed/anchor_paper/`;
- kurzer Report unter `reports/`.

## Definition of Done fuer die aktuelle Dokumentationsrunde

- Architektur- und Anforderungsdokumente sind in MkDocs verlinkt.
- README oder Startseite zeigt auf diese Dokumente.
- Tests, Anchor-Pipeline und MkDocs-Build wurden erneut ausgefuehrt.
- Die Aenderung ist gepusht, damit GitHub-Links verwendet werden koennen.
