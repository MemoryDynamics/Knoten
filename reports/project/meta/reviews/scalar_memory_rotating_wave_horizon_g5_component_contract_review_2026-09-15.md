# Review: isolierter G5-Komponentenvertrag

Datum: 2026-09-15.

Verdikt: **target-free pass; G5 ungemessen; Zielzugriff nicht bereit**.

## 1. Gepruefter Umfang

Das Review umfasst den neuen exakten Sieben-Ebenen-Vertrag `identity`,
`finite_root`, `preflight`, `arnoldi`, `trajectories`, `classification` und
`publication`, seine targetfreie Stufenkomposition, den
standardbibliotheksbasierten Auditor und die manifest-last-Publikationsgrenze.
Es wurde kein $H=2400$-Arnoldilauf und keine nichtlineare Zieltrajektorie
ausgefuehrt.

Die Dokumentation schreibt den nativen FIFO-Shift nun indexgenau aus:

$$
h_{n+1}^{(0)}=x_{n+1},\qquad
h_{n+1}^{(j)}=h_n^{(j-1)}\quad(1\leq j<H).
$$

Damit ist explizit getrennt: Der FIFO ordnet die endliche Erinnerung nach
Alter, ein zirkulaerer Puffer waere nur eine Speicheroptimierung, und die
nachfolgende Drehung um $-\theta$ ist nur ein Koordinatenwechsel. Keine dieser
Operationen erzwingt eine raeumliche Kreisbahn.

## 2. Positive Befunde

1. Fehlender finite Root schliesst Preflight, Arnoldi und Trajektorien.
2. Ein nicht bestandener, intern konsistenter Grundgleichungs-Preflight
   schliesst beide Arnoldi-Panels.
3. Unvollstaendige, schlecht residuierte oder symmetriseitig unplausible
   Panels koennen keine nichtlinearen Arme oeffnen.
4. Panelgroessen 24/36, Vektorlaenge 4800, Samplelaenge 501, LCG-Starts,
   Stoerungsvektoren, Hashes und Null-Praefixe sind vertraglich fixiert.
5. Stabilitaet verlangt gleichzeitig gematchtes Spektrum, Residuen,
   Symmetrien, drei vollstaendige Fortsetzungen, transiente Verstaerkung
   hoechstens 10, Endverhaeltnis hoechstens 0.1 und exakte Kontrolle.
6. Der Auditor importiert weder Runner noch NumPy, SciPy, mpmath oder einen
   Eigensolver. Er rekonstruiert Vertrag, Preflight, Panelmatch,
   Trajektoriensummaries, Entscheidung und Publikationshashes.
7. Ergebnis und Lesereport werden vor dem zuletzt erzeugten Manifest
   geschrieben; atomare Hardlink-Erzeugung verhindert Ueberschreiben auch
   bei einem konkurrierenden Zielnamen.

## 3. Kritische Grenzen

### Offen, hoch: Execution-Context-Guard

Der numerische Adapter ist absichtlich nur lazy erreichbar und wird beim
Import nicht ausgefuehrt. Es fehlt aber noch der schmale autorisierte
Ausfuehrungseinstieg, der sauberen Commit, unveraenderte Protokoll- und
Schema-Bytes, feste Dependency-Versionen, gruene exakte CI und noch nicht
existierende Zielartefakte gemeinsam prueft. Ohne diesen Guard gibt es kein
Readiness-Pass und keinen Zielzugriff.

### Begrenzte Unabhaengigkeit, mittel

Runner und Auditor verwenden denselben kleinen strukturellen
Standardbibliotheksvalidator. Ihre semantische Rekonstruktion ist getrennt
implementiert. Der Auditor berechnet jedoch weder den sparse Jacobian noch
$Jv-\lambda v$ oder die gespeicherten Symmetrieueberlappungen neu. Er prueft
nur deren Hash-, Schwellen- und Klassifikationskonsistenz. Ein spaeterer
zweiter numerischer Backend waere staerkere Evidenz.

### Artefaktgroesse, niedrig bis mittel

Die 60 komplexen Ritzvektoren werden vollstaendig gespeichert. Das erhoeht
Pruefbarkeit und erlaubt spaetere Residuenreplays, erzeugt aber einen grossen
JSON-Record. Vor Freigabe muss ein targetfreier Groessen-/Serialisierungstest
zeigen, dass die atomare Publikation im CI- und Nutzerpfad praktikabel bleibt;
eine nachtraegliche Kompression darf den eingefrorenen Vertrag nicht still
aendern.

## 4. Falsifikationstests

Die neue Suite erkennt unter anderem unbekannte Felder, NumPy-Skalare,
inkonsistente Preflight-Gates, falsche Recordhashes, Null-Loecher,
erfundene Pass-Entscheidungen, geoeffnete Folgestufen ohne Voraussetzung,
veraenderte Begleitreports und Ueberschreibversuche. Der bereits vorhandene
Produktionskern-Test zeigt ausserdem direkt `expected[1:] = history[:-1]` und
bindet damit die ausgeschriebene FIFO-Alterung an den Code.

## 5. Schlussfolgerung

Der Komponentenvertrag ist als targetfreie Infrastruktur belastbar genug,
um zum Execution-Context-Hardening ueberzugehen. Dies ist kein G5-Befund:
Spektrum und nichtlineare Fortsetzungen bei $H=2400$ bleiben ungemessen. Erst
ein weiteres kritisches Readinessreview darf einen einzelnen isolierten
Zielzugriff zur ausdruecklichen Nutzerfreigabe vorschlagen.
