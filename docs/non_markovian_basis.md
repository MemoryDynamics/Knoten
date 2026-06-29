# Non-Markovian Basis

Stand: 2026-06-24.

Diese Seite ist die kuratierte Arbeitsbasis fuer Paper 0 oder die
Paper-I-Ueberarbeitung. Sie ersetzt nicht die Literaturarbeit, sondern legt
fest, wie das vorhandene Modell inhaltlich und softwareseitig an eine
nichtmarkovsche bzw. markov-eingebettete Sprache angeschlossen wird.

## Kernthese

Der Prozess `x_n` allein ist nichtmarkovsch:

```text
x_{n+1} = x_n + epsilon * noise_n - eta * grad Phi_n(x_n)
```

Der Gradient `grad Phi_n` wird aus gespeicherter Vergangenheit gebildet. Damit
haengt der naechste sichtbare Schritt nicht nur von `x_n`, sondern von einem
Memory-Zustand ab.

Der augmentierte Zustand ist dagegen markovsch:

```text
z_n = (x_n, rho_n)
```

oder in der konkreten Implementierung:

```text
z_n = (x_n, history_n, weights_n)
```

Wenn `z_n` und der neue Rauschterm bekannt sind, ist `z_{n+1}` bestimmt. Das
ist die zentrale Bruecke: sichtbar nichtmarkovsch, im erweiterten Zustand
markovsch.

Notation:

- `z_n` bezeichnet den augmentierten Markov-Zustand.
- `G_sigma` bezeichnet weiterhin den Glattungs-/Depositionskernel mit Breite
  `sigma`.

Diese Trennung verhindert die alte Kollision zwischen `sigma_n` als
Zustandsnotation und `G_sigma` als Kernelnotation.

## Operatoralgebraische Lesart

Auf dem augmentierten Zustandsraum `Sigma` definiert die Dynamik einen
Markov-Kern:

```text
P(z, A) = Prob(z_{n+1} in A | z_n = z)
```

Fuer Observablen `f` wirkt derselbe Prozess als Markov-/Koopman-Operator:

```text
(U f)(z) = E[f(z_{n+1}) | z_n = z]
```

Dieser Operator ist linear, positiv und unital (`U 1 = 1`). Seine Iterierten
bilden eine Halbgruppe:

```text
U^{m+n} = U^m U^n
```

Im stochastischen Fall ist `U` im Allgemeinen nicht multiplikativ, also kein
deterministischer Algebra-Automorphismus. Genau diese Unterscheidung ist
wichtig: Die algebraische Sprache ist passend, aber sie ist die Sprache
positiver Markov-Operatoren bzw. Transferoperatoren, nicht die Sprache einer
reversiblen Symmetriegruppe.

Konsequenz fuer Knoten:

- lokal: Hessian-/OU-Spektrum als Relaxationsdiagnostik;
- global: slow modes, spectral gaps, almost-invariant sets und metastabile
  Memberships des Operators;
- spaeter: Symmetrie- oder Stabilisatorgruppen robuster Knotentypen, nicht
  als Eingabe, sondern als emergente Struktur.

## Speicherform

Die konzeptionelle Memory-Gleichung lautet:

```text
rho_{n+1} = (1 - alpha) rho_n + alpha G(x_{n+1})
```

Ausgerollt:

```text
rho_n = alpha * sum_{k>=0} (1 - alpha)^k G(x_{n-k})
```

bis auf Anfangs- und Cutoff-Effekte. Im Code wird diese Struktur durch einen
endlichen History-Buffer und Gewichte

```text
w_k = alpha * (1 - alpha)^k
```

realisiert. Der effektive Speicherhorizont ist:

```text
horizon = min(max_memory, max(1, int(memory_factor / alpha)))
```

Das macht `alpha` doppelt wichtig: Es steuert die Relaxation und, ueber den
Horizon, die effektive gespeicherte Vergangenheit.

## Literatur-Andockpunkte

Die naechste Literaturarbeit sollte die Modellklasse nicht primaer in
Quantengravitation suchen, sondern in diesen Nachbarschaften:

- Self-interacting diffusions.
- Reinforced random walks und true/self-repelling motions.
- Self-repelling Brownian polymer.
- Generalized Langevin equations mit exponentiellen Memory-Kernen.
- Markovian embeddings fuer Prozesse mit endlicher Erinnerung.
- Transferoperatoren, Markov State Models, PCCA/PCCA+ und HMM/PMM fuer
  metastabile Grobstruktur.

Die aktuelle Arbeitsvermutung:

> Das Neue ist wahrscheinlich nicht "ein Prozess mit Gedaechtnis" an sich,
> sondern die Kombination aus exponentiell endlichem Speicher,
> selbstinduziertem Potential, metastabilen Attraktoren und physikalischer
> Interpretation der entstehenden Relaxationsskalen.

## Abgrenzung zu Quantum Non-Markovianity

Papers zu nichtmarkovschen offenen Quantensystemen, Quantum Renewal Processes
oder Process Tensors sind spaeter relevant, aber nicht der primaere Ursprung
von Paper I.

Unterschied:

- Dort sind Hilbertraum, Dichtematrix, Quantensystem und Umgebung meist schon
  vorausgesetzt.
- Hier sollen Zeit, Knoten, effektive Masse, Raum- oder spaeter
  Quantennormalformen aus einer tieferen Speicher- und Punktprozessdynamik
  entstehen.

Diese Literatur ist daher eher Brueckensprache fuer spaetere effektive
Quantendynamik, nicht die direkteste mathematische Basis des Kernmodells.

## Implementationskonsequenz

Der aktuelle `SimulationResult` reicht fuer geometrische Diagnostik, aber noch
nicht fuer Operator- oder MSM-Analysen. Fuer die Non-Markovian-Schiene muessen
wir entlang der Trajektorie rekonstruierbare augmentierte Features speichern.

Minimale Erweiterung:

```text
samples            (T, dim)
sample_steps       (T,)
memory_mean        (T, dim)
memory_variance    (T, dim)
memory_mass        (T,)
optional history   (T, horizon, dim)
```

Danach:

```text
features -> lagged dataset -> state assignment -> transition counts
         -> transition matrix -> validation -> metastable memberships
```

## Erste Markov-Schiene

Reihenfolge fuer eine schlanke Implementierung:

1. `build_augmented_features`: Modi `raw`, `delay`, `memory_summary`.
2. `make_lagged_dataset`: Sample-Paare `(z_i, z_{i+ell})` mit separat dokumentiertem Update-Lag.
3. `assign_states`: zunaechst einfache Voxel/Cluster-Prototypen.
4. `transition_counts`: Zaehle Label-Uebergaenge.
5. `transition_matrix`: zeilenstochastische Normalisierung.
6. `implied_timescales`: Eigenwerte gegen Lag-Gitter.
7. `chapman_kolmogorov_error`: pruefe Mehrschritt-Konsistenz.
8. `spectral_gap`: begruende Anzahl metastabiler Zustaende.
9. PCCA-/HMM-Fallback erst nach dieser Basis.

## Validierungskriterien

Ein operatorischer "Knoten" ist erst belastbar, wenn mehrere Ebenen
zusammenpassen:

- lange Verweilzeiten oder Rueckkehrzeiten im Residence-Sinn;
- metastabile Membership oder klarer spectral gap im Uebergangsoperator;
- stabile implied timescales ueber ein Lag-Gitter;
- bessere CK-Konsistenz als passende Negativkontrollen;
- robuste Ergebnisse ueber Seeds, Burn-in, Sampling und State-Assignment.

## Paper-0-Arbeitshypothese

Eine robuste Paper-0-Formulierung waere:

> We study a finite-memory self-interacting stochastic process whose visible
> coordinate is non-Markovian but admits a natural Markovian embedding in an
> augmented memory state. The central question is whether metastable structures
> and relaxation scales of this embedded process can be operationally linked to
> effective geometric or physical observables.

Noch nicht behaupten:

- eindeutige 3D-Selektion;
- direkte Herleitung von Quantenmechanik;
- Masse als bereits bewiesene Funktion der Speicherlaenge;
- Lorentz-Kinematik als Ergebnis der aktuellen Kurzlaeufe.

## Paper-I-Anschluss

Fuer Paper I sollten folgende Stellen inhaltlich andocken:

- Minimal model: `x_n` als sichtbarer nichtmarkovscher Prozess, `rho_n` als
  Markov-Embedding-Variable.
- Emergent time: `alpha^{-1}` als interne Persistenzskala, nicht als
  fundamentale Zeit.
- Knoten: metastabile Mengen muessen operational ueber Residence,
  Relaxation und spaeter Transferoperatoren definiert werden.
- Mass proxy: Relaxationsrate/Curvature als Arbeitsdefinition, noch keine
  physikalische Masse.
- Diagnostics: klare Trennung von geometrischem Spektrum und dynamischem
  Operator-Spektrum.
