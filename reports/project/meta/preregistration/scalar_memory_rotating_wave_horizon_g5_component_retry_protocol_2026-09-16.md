# Prospektives Retry-Protokoll: isolierte G5-Direktsimulation, Attempt 2

Datum: 2026-09-16.

Status: **outcome-blind eingefroren vor Attempt 2**.

## 1. Anlass und unveraenderter wissenschaftlicher Vertrag

Attempt 1 wurde vor jeder Ergebnispublikation durch einen binary64-Overlap
geringfuegig ausserhalb der mathematischen Recordgrenze $[0,1]$ beendet. Der
konkrete verworfene Wert wurde nicht persistiert. Deshalb ist die
Rundungsdiagnose stark gestuetzt, aber kein nachtraeglich gemessener
Zielbefund. Attempt 1 bleibt verbraucht und seine Receipt unveraendert.

Attempt 2 wiederholt exakt die im
[Erstprotokoll](scalar_memory_rotating_wave_horizon_g5_component_protocol_2026-09-14.md)
festgelegte wissenschaftliche Untersuchung. Unveraendert bleiben insbesondere

- Grundgleichung und FIFO-Shift;
- $\alpha=0.01$, $q=0.99$, $H=2400$, $M_0=1$, $\eta=0.15$ und
  $\varepsilon=0$;
- Kernelparameter, Newtonstart und beide Krawczykboxen;
- Grundgleichungs-Preflight, beide Arnoldi-Panels und LCG-Starts;
- Stoerungsrichtungen, Amplitude, Laufzeit, Sampling und Stopregeln;
- Stabilitaets-, Instabilitaets- und `inconclusive`-Schwellen;
- Claimgrenze und unabhaengiger Publikationsaudit.

Es gibt keinen Parameterscan, keinen alternativen Root, keine neue
Stoerungsrichtung und kein Ergebnis-Retuning.

## 2. Einzige numerische Remediation

Translations- und Rotationsoverlap sind normierte orthogonale Projektionen
und mathematisch auf $[0,1]$ beschraenkt. Vor Klassifikation und
Serialisierung wird ein roher binary64-Wert $o$ nun nur dann kanonisiert,
wenn

$$
-\tau_d\leq o\leq 1+\tau_d,
\qquad
\tau_d=8\frac{d u}{1-d u},
$$

wobei $d$ die Zustandsdimension und $u$ `numpy.float64.eps` ist. Fuer
$d=4800$ gilt $\tau_d\approx8.53\times10^{-12}$. Innerhalb dieses Budgets
wird auf $[0,1]$ begrenzt. Groessere Verletzungen, `NaN`, Unendlich und
ungueltige Dimensionen brechen fail-closed ab. Die Klassifikationsschwelle
$0.99$ bleibt unveraendert.

## 3. Attempt-2-Provenienz und Artefakte

Der Retry verwendet ausschliesslich:

- Receipt
  `scalar_memory_rotating_wave_horizon_g5_component_attempt_2_receipt.json`;
- Ergebnis
  `scalar_memory_rotating_wave_horizon_g5_component_attempt_2_2026-09-16.json`;
- gleichnamigen Lesereport und manifest-last-Publikationsrecord.

Der Guard muss Attempt 2, Implementierungscommit, exakte erfolgreiche CI,
Readinessreview, Dependencyversionen, geschuetzte Blobs, sauberen
Upstreamzustand und leere Attempt-2-Zielpfade binden. Die Attempt-2-Receipt
wird atomar vor jeder Zielnumerik erzeugt. Jeder spaetere Fehler verbraucht
Attempt 2. Vorhandene Attempt-1-Artefakte werden weder gelesen noch
ueberschrieben.

## 4. Falsifikation und Entscheidung

Vor Freigabe muessen Tests mindestens bestaetigen:

1. Ein-ulp-Ueberschreitungen werden exakt zu `1.0` kanonisiert.
2. Abweichungen von $10^{-8}$ sowie nichtendliche Werte werden verworfen.
3. Attempt-1- und Attempt-2-Pfade sind verschieden.
4. Falsche Attemptnummer, Blobdrift, gemischter Autorisierungscommit, rote CI,
   falsches Readinessreview und vorhandene Attempt-2-Zielpfade stoppen vor
   Receipt und Numerik.
5. Der geschlossene Importpfad erreicht kein numerisches Zielmodul.

Zulaessig bleiben ausschliesslich die vier Entscheidungen des Erstprotokolls:
lokaler Stabilitaetspass, reproduzierbar gestuetzte lokale Instabilitaet,
`inconclusive` oder bei Vertrags-/Provenienzfehlern `experiment-invalid`.

## 5. Stopregel

Ein Major-/Critical-Befund, rote exakte CI, unvollstaendiges Readinessreview,
schmutziger Arbeitsbaum oder unklare Abweichung vom Erstprotokoll stoppt vor
dem Zielzugriff. Sind Implementierung, Review und CI gruen, darf aufgrund der
ausdruecklichen Nutzerentscheidung vom 2026-09-16 ein einzelner
Governance-only-Autorisierungscommit fuer Attempt 2 erstellt und genau ein
Lauf gestartet werden. Es gibt keinen automatischen Attempt 3.
