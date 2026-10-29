# Native Paararchive: Lagstatistik noch nicht auswertbar

Stand: 2026-10-29. **Archivpruefung, kein neuer Lauf oder Replay.**
Anschluss an die
[bedingte gemittelte Reziprozitaet](../../docs/reference/memory_pair_finite_separation.md).

## Befund und Reichweite

Die geprueften direkten Paararchive enthalten keine gleichzeitig
aufgeloesten Einzelbahnen beider Knoten samt rekonstruierbarer Historie.
Damit laesst sich die neue Lagbilanz aus diesen Ausgaben nicht nachtraeglich
messen. Das ist ein Datenverfuegbarkeitsbefund, **kein Scheitern der
Mittelungshypothese** und keine Revision der alten Moden-/Formbefunde.

Das [maschinenlesbare Inventar](memory_pair_archive_inventory_2026-10-29.json)
enthaelt Byte-Hashes, alle JSON-Wurzelfelder, die ueber alle Zeilen
gesammelten Bedingungsfelder und die laengsten JSON-Listen. Bei NPZs
werden alle Arrays ohne Pickle gelesen und nach Form/Datentyp gruppiert;
je Gruppe stehen Anzahl und bis zu drei Beispielnamen im Inventar.
`sha256` bezieht sich auf lokale Arbeitsbaum-Bytes; `sha256_utf8_lf`
normalisiert bei Texten Zeilenenden nach LF fuer den GitHub-Vergleich.
Der [Inventarisierer](../../experiments/current/reference/memory_pair_archive_inventory.py)
importiert keinen Simulator. Auswahl: drei native/retardierte Paarberichte,
deren Anfangszustand, zwei naheliegende Response-NPZs und sechs Codequellen.
Dies ist keine vollstaendige Inventur aller lokalen Dateien. Nicht lesbare
alte pytest-Temporaerverzeichnisse wurden nicht als Experimentarchive
ausgegeben oder fuer den Negativbefund benoetigt.

| Geprueft | Tatsachlich vorhanden | Fuer die Lagbilanz fehlend |
| --- | --- | --- |
| [P3.1 direkt, 2026-08-04](../response/reciprocal/reciprocal_full_knot_gate_2026-08-04.json) | 5 Zukunftsrauschpfade, 50 000 Updates, Paar-Abtastrate 1; JSON mit Fitsegmenten, Form-/Responsekennzahlen und Endabstand | Die im Lauf berechneten Einzelbahnen sind nicht im JSON; die laengste Liste hat 5 Eintraege |
| [P3.2, 2026-08-04](../response/reciprocal/retarded_reciprocal_full_knot_gate_2026-08-04.json) | 5 Pfade, 50 000 Updates, Abtastrate 1; nativer direkter Kontrollarm plus retardierte Arme | Ebenfalls nur aggregierte Kennzahlen, keine gepaarte dichte Bahn; laengste Liste 5 |
| [P3.2-500k, 2026-08-06](../response/reciprocal/p32_accumulation_control_N500k_2026-08-06.json) | 2 Pfade, 500 000 Updates, Abtastrate 10; Fensterstatistiken und eingebetteter Basisbericht | Keine dichten Einzelbahnen; laengste Liste 4. Abtastrate 10 waere allein ohnehin nicht fuer alle FIFO-Lags ausreichend |
| Gemeinsamer N=100M-Anfangscheckpoint | `x[3]`, `memory[600,3]`, `weights[600]`, Manifest | Nur ein Zustand vor Platzierung/Kopie, keine spaetere gekoppelte Bahn |
| [P3.8e-Response-NPZ](../memory/closure/emergent_modal_state_reconciliation_2026-08-13.responses.npz) | 148 Arrays, insbesondere Features `[161,5,3]` und Moden `[161,5,5]` | Kein nativer Paarlauf; der [zugehoerige Bericht](../memory/closure/emergent_modal_state_reconciliation_2026-08-13.md) kennzeichnet `two-node-transfer-channel` als `not-run` |
| P3.8f, Seed-1-Shard | 147 Arrays, darunter `branch_positions[801,2,3]` | Die Achse der Laenge 2 bezeichnet Plus-/Minus-Stoerungen eines Knotens, nicht zwei wechselwirkende Knoten |

Die P3.8f-Zuordnung folgt aus
[`canonical_write_port.py`](https://github.com/MemoryDynamics/Knoten/blob/d09306bf37646d5e7d4c8f9662b662edf85ebc0a/src/emergenz_knoten/canonical_write_port.py):
drei getrennte Pfade mit Vorzeichen +1, -1 und 0; der Writer persistiert
die ersten beiden als `branch_positions`. Die Arrayform allein waere
kein ausreichender Nachweis dieser Semantik.

Die historischen `main()`-Ausgabepfade wurden an den **im jeweiligen
JSON genannten** sauberen Revisionen gelesen:
[P3.1: 3a68e58](https://github.com/MemoryDynamics/Knoten/blob/3a68e582fbf800ed9e620249c6da3fb22027ca68/experiments/current/memory/synchronization/reciprocal_full_knot_gate.py),
[P3.2: 9b6bd5e](https://github.com/MemoryDynamics/Knoten/blob/9b6bd5eeedd8ad969afd307539b61bf9c0d63693/experiments/current/memory/synchronization/retarded_reciprocal_full_knot_gate.py),
[500k: 72ae145](https://github.com/MemoryDynamics/Knoten/blob/72ae14528e7a807e9484093c1503e2ec9f3f72a9/experiments/current/memory/synchronization/p32_accumulation_control.py).
Sie schreiben JSON-Payload, PNG und Markdown; `traces` werden an den
Plotter uebergeben, nicht als Roharchiv geschrieben. Der heutige
Payload-/Trace-Aufbau ist damit konsistent: Die Plottraces sind bereits
ausgeduennt und enthalten relative Punkt-/Centerkoordinaten nur entlang
einer Achse, nicht die beiden vollstaendigen Punktbahnen.

Die Aussage im alten 500k-Bericht, jeder zehnte Update werde "stored",
bezeichnet daher keine vollstaendige persistierte Rohbahn. Der historische
Bericht bleibt unveraendert; diese Archivierungsgrenze wird hier ergaenzt.
Die Seed-Angaben erlauben allenfalls eine erneute Ausfuehrung des
Simulators unter passender Umgebung. Das waere ein **Replay mit neu
berechneten Daten**, keine reine Archivauswertung und ist nicht freigegeben.

## Minimaler Datenvertrag fuer eine kuenftige Messung

Die unveraenderte native Regel liest beide alten Historien, berechnet
beide neuen Punkte und schreibt diese dann in ihre FIFOs. Fuer jeden
Knoten reichen deshalb: vollstaendige **platzierte** Anfangshistorie
$Y_i(0)$ in Altersreihenfolge, Anfangspunkt $x_i(0)$, alle danach
geschriebenen Punkte $x_i(1),\ldots,x_i(N)$, Gewichte und Parametersatz.
Eine neue Integration ist zur Historienrekonstruktion nicht erforderlich:

$$
y_{i\ell}(n)=
\begin{cases}
x_i(n-\ell),&0\leq\ell<n,\\
y_{i,\ell-n}(0),&n\leq\ell<H_i.
\end{cases}
$$

Die erste Zeile gilt ebenfalls nur fuer $\ell<H_i$. Bei $n=0$ bleibt die
Anfangshistorie unangetastet; $x_i(0)=y_{i0}(0)$ wird nicht stillschweigend
vorausgesetzt. Bei $n\geq H_i$ besteht sie vollstaendig aus gespeicherten
Punkten. Center, Formen und die direkten Kreuzgradienten sind daraus
erneut auswertbar. Erforderliche Metadaten sind Synchronisierung,
Updateindizes, Achsen-/Bedingungs-/Seed-Bedeutung, Kernel samt Deposition,
Kopplung, Code-/Eingabehashes und Abbruchstatus. Separate Innovationen sind
fuer diese FIFO-Rekonstruktion nicht noetig, fuer eine unabhaengige
Pruefung der stochastischen Updategleichung jedoch zusaetzlich zu sichern.
Ein Mediator mit eigenem Zustand waere separat zu archivieren; er gehoert
nicht zum hier betrachteten nativen direkten Zweig.

Zwei Informationsverluste sind konkret getestet:

- Gleiche ausgeduennte Punktbahnen koennen verschiedene ausgelassene
  Historienpunkte und daher verschiedene Kreuzgradienten besitzen.
- Eine gemeinsame zeitabhaengige Verschiebung $a(n)$ laesst den
  gleichzeitigen Paarabstand unveraendert, aendert aber
  $x_A(n)-x_B(n-\ell)$ um $a(n)-a(n-\ell)$. Relativbahnen allein reichen
  somit nicht. Eine konstante gemeinsame Translation bleibt dagegen
  eine exakte Symmetrie. Dies ist keine Behauptung, beide konstruierten
  Bahnen loesten dieselbe native Dynamik.

## Endliche Fenster sind keine stationaeren Erwartungswerte

Die Lagidentitaet im Theorieanschluss benutzt gemeinsame Stationaritaet.
Ein empirisches Fenster darf diese Voraussetzung nicht durch blosses
Umbenennen der Summationsindizes vortaeuschen. Setze bei festen
Referenzcentern $h_\ell(t)=g(R+v_A(t)-v_B(t+\ell))$ und
$\langle h\rangle_{[a,b)}=(b-a)^{-1}\sum_{t=a}^{b-1}h(t)$. Dann gilt exakt

$$
\left\langle g(R+v_A(t-\ell)-v_B(t))\right\rangle_{[a,b)}
=\langle h_\ell\rangle_{[a,b)}+B_\ell,
\quad
B_\ell=\frac{\sum_{t=a-\ell}^{a-1}h_\ell(t)
-\sum_{t=b-\ell}^{b-1}h_\ell(t)}{b-a}.
$$

Bei $|g|\leq M_g$ ist $|B_\ell|\leq2\ell M_g/(b-a)$; diese einfache
Schranke kann grob sein. Der konkrete Randterm ist mit auszuwerten,
einschliesslich noetiger Daten vor und nach dem Messfenster. Ein passender
Fensterzuschnitt oder ausdruecklich verschobene Gegenfenster vermeiden
fehlende Daten, beweisen aber keine Stationaritaet, Mischung oder kleine
statistische Unsicherheit. Ein synthetischer Test prueft die exakte
Randidentitaet mit absichtlich nichtstationaeren Bahnen.

## Konsequenz

Die naechste Entscheidung benoetigt eine neue, vorab spezifizierte
Diagnose mit dichter Roharchivierung, getrennten Balance-/Produktvergleichs-
und Centerbewegungsfehlern sowie kontrollierten Fensterraendern.
Ein kleiner Mittelwert der Unwucht allein bestaetigt weder Unabhaengigkeit
noch die Produktfaltung. Statistik- und Stationaritaetskriterien,
Laufzeitgrenze und Ausfuehrungsfreigabe stehen noch aus; kein neuer Lauf
wird aus dieser Archivpruefung abgeleitet. Die einzige Arbeitsreihenfolge
bleibt in den [Projektprioritaeten](../../docs/status/project_priorities.md).

Neun neue [synthetische/Dateiformat-Tests](../../tests/test_memory_pair_archive_contract.py)
bestehen: drei Inventarchecks, FIFO-Rekonstruktion fuer H=1/3/5 und die
drei genannten Informationsverlust-/Fensterkontrollen. Kein Test startet
einen Zielsimulator oder rekonstruiert eine fehlende Produktionsbahn.
Die wissenschaftliche Frage nach effektiver Paarmechanik und der
physikalischen Energie bleibt offen. AL1, FIFO/P5 und Paper I sind
unveraendert; die verbrauchten Ausfuehrungsfreigaben bleiben geschlossen.

Verifikation: **142 betroffene Tests bestanden in 3.69 s**, einschliesslich
der neun neuen Kontrollen, bisheriger Paar-/Kerneltests, AL1-Archivchecks
und Dokumentationsregressionen. Konfigurierter Lintcheck und strikter
MkDocs-Bau bestehen. Keine vollstaendige Repository-Testsuite und keine
statistische Validierung nativer gekoppelter Bahnen.
