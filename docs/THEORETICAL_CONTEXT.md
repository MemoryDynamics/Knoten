# Theoretical Context

Stand: 2026-06-14.

Diese Datei fasst den kuratierten theoretischen Kontext des Projekts zusammen.
Rohnotizen und Chatverlaeufe bleiben unter `docs/ChatGPT Chatverläufe/`, sind
aber keine zitierfaehige Fassung.

## Minimaler Modellkern

Das Modell startet mit einem sichtbaren Punktprozess `x_n` und einem
relaxierenden Speicherzustand `rho_n` bzw. einem endlichen History-Buffer.

Sichtbarer Update:

```text
x_{n+1} = x_n + epsilon * noise_n - eta * grad Phi_n(x_n)
```

Memory-Update:

```text
rho_{n+1} = (1 - alpha) rho_n + alpha G(x_{n+1})
```

Der sichtbare Prozess `x_n` ist nichtmarkovsch. Der augmentierte Zustand
`(x_n, rho_n)` ist die natuerliche Markov-Einbettung.

## Zentrale Claims

### Zeit

Arbeitsclaim:

- Eine interne Update-Richtung entsteht aus dem irreversiblen
  Speicherupdate.
- `alpha^{-1}` ist eine Persistenz- bzw. Relaxationsskala des Speichers.
- Grobkoernungen wie `t = alpha n` sind Hilfsparameter der internen
  Speicherpersistenz, keine postulierte fundamentale Zeit.

Status: gut als Modellstruktur formulierbar, aber bei Paper-I-Texten muss die
Rolle von `t` konsequent operational bleiben.

### Knoten

Arbeitsclaim:

- Metastabile Strukturen entstehen in bestimmten Parameterregimen durch das
  Zusammenspiel von Rauschen, Repulsion, Attraction und relaxierendem Speicher.
- Knoten duerfen nicht nur visuell definiert werden.

Noetige Operationalisierung:

- Residence-Verteilungen.
- Rueckkehrzeiten.
- lokale Relaxationsraten.
- spaeter metastabile Memberships eines Uebergangsoperators.

### Effektive Dimension

Arbeitsclaim:

- Es gibt archivierte Hinweise auf niedrige effektive Dimensionen und ein
  Near-3-Signal in langen Finite-Size-Laeufen.

Aktueller belastbarer Befund:

- Staerkster Archivpunkt:
  `embedding dim = 5`, `N = 60,000,000`, fuenf Runs,
  `mean D_occ = 2.810559`.

Status:

- vielversprechend;
- noch kein Beweis eindeutiger 3D-Selektion;
- braucht frische Seed-Ensembles, Negativkontrollen und gemeinsame Berichte
  von `D_occ`, `D_cov` und dynamischen Operator-Diagnostiken.

### Masse und Relaxation

Arbeitsclaim:

- "Masse" ist vorerst ein Relaxations- oder Konfinierungsproxy von
  metastabilen Knoten.
- Eine moegliche Verbindung zwischen Speicherlaenge, Relaxationsrate und
  effektiver Masse ist eine Arbeitshypothese, keine Folgerung.

Paper-I-Sprache:

- `mass proxy`, `relaxation scale` oder `confinement scale` bevorzugen, bis
  die physikalische Kalibrierung tragfaehig ist.

### Raum, Propagation und Lorentz-Kinematik

Arbeitsclaim:

- Endliche Speicherreichweite und gekoppelte Knoten koennen endliche
  Antwortzeiten und einen operationalen Lichtkegel nahelegen.

Status:

- konzeptionell wichtig fuer Paper II;
- aktuell noch staerker als Konsistenzprogramm denn als harter Befund;
- sollte nach Paper 0/I-Haertung weiter getestet werden.

## Experiment-Mapping

| Claim | Primaere Orte | Aktueller Status |
| --- | --- | --- |
| Minimaler Speicherprozess | `src/emergenz_knoten/core.py`, `kernels.py` | implementiert |
| Geometrische Diagnostik | `src/emergenz_knoten/diagnostics.py` | implementiert, aber nicht operatorisch |
| Referenzlauf | `experiments/reference_experiment.py` | aktiv |
| Archivierter Dimensionsclaim | `experiments/fractal_analysis/Fraktale/resultsN.csv` | auditiert |
| Reproduktionspfad | `experiments/fractal_analysis/reproduce_dimension_pilot.py` | aktiv |
| Propagation | `experiments/propagation_speed/` | historisch, noch zu haerten |
| Non-Markovian Basis | `docs/non_markovian_basis.md` | kuratiert, Implementierung offen |

## Methodische Andockpunkte

Naheliegende Literatur- und Methodenfamilien:

- self-interacting diffusions;
- reinforced random walks und self-repelling processes;
- generalized Langevin equations mit exponentiellen Memory-Kernen;
- Markovian embeddings;
- transfer operators und Markov State Models;
- PCCA/PCCA+ fuer metastabile Mengen;
- HMM/PMM, wenn die Projektion auf sichtbare Cluster nicht markovsch ist.

Quantum-non-Markovianity, Renewal-Prozesse und Process-Tensor-Literatur sind
spaeter relevant, aber nicht der direkteste Ausgangspunkt fuer Paper I, weil
sie meist bereits vorhandene Quantenzustaende voraussetzen.

## Sprachregel

Bis zur Haertung:

- "We define" fuer Modellannahmen.
- "We observe numerically" fuer reproduzierbare Simulationsergebnisse.
- "We conjecture" fuer Weltmodell-, Lorentz-, Quanten- oder
  Standardmodell-Bruecken.

Nicht vermischen:

- geometrische Spektraldiagnostik und Transferoperator-Spektrum;
- sichtbaren nichtmarkovschen Prozess und augmentierten Markov-Zustand;
- Archivbefund und frisch reproduzierte Evidenz;
- Relaxationsproxy und physikalische Masse.
