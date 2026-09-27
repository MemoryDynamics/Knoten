# Prospektives Protokoll: G1--G3-Horizontbruecke

Datum: 2026-09-27.

Status: **outcome-blind fuer den neuen G1--G3-Zugriff; Target geschlossen**.

Dieses Protokoll ersetzt keinen bereits publizierten G4- oder G5-Lauf. Es
isoliert die noch fehlende endliche Horizontleiter und komponiert ihr spaeteres
Ergebnis nur hashgebunden mit den versiegelten G4-/G5-Artefakten. Bis zu einem
separaten Readinessreview, gruener exakter CI und einer neuen ausdruecklichen
Nutzerfreigabe darf kein Root der registrierten Leiter berechnet und kein
reservierter Ergebnis-, Manifest-, Receipt- oder Auditpfad beschrieben werden.

## 1. Wissenschaftliche Frage

Der isolierte G4-Pass belegt einen lokalen Root von $F_\infty$ in der
registrierten Tailbox. Der isolierte G5-Pass stuetzt lokale direkte
FIFO-Stabilitaet bei genau $H=2400$. Getrennt beweisen diese Resultate nicht,
dass sie zu demselben Loesungsast gehoeren.

Die neue Frage lautet daher:

> Laesst sich der lokale finite-$H$-Root bei festem $\alpha=0.01$ von
> $H=1200$ ueber die registrierte Leiter eindeutig bis $H=3600$ fortsetzen,
> schrumpft seine zertifizierte Drift, und sind seine Endpunktzertifikate mit
> den bereits versiegelten G5- beziehungsweise G4-Rootpanels identisch?

Ein positiver Ausgang stuetzt nur eine lokale Rootast-Verbindung mit lokaler
Stabilitaetsevidenz an einem endlichen Astpunkt. Er beweist weder
$H\to\infty$-Stabilitaet noch globale Eindeutigkeit, Formation, Interaktion,
internen Spin, Traegheit oder physikalische Masse.

## 2. Eingefrorene Herkunft und Komponenten

Die G1--G3-Definitionen, Parameter und Schwellen werden unveraendert aus dem
vierfach amendierten Gesamtprotokoll uebernommen:

- Pfad:
  `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_transfer_protocol_2026-09-08.md`;
- SHA-256:
  `f4fafc69bb2937db1ab74fb8a923c82b98dc8e44ddaf78c1d8b68fe6d1755710`;
- Git-Blob:
  `671e931a8337b1c31923dbd122085167185e9091`.

Die unveraenderten Modellparameter sind

$$
\alpha=0.01,\quad q=0.99,\quad M_0=1,\quad \eta=0.15,
$$

$$
\sigma_{\rm rep}=1,\quad \sigma_{\rm att}=3,\quad
A_{\rm rep}=1,\quad A_{\rm att}=3.5,\quad \varepsilon=0.
$$

Die versiegelten positiven Komponenten werden nicht neu berechnet:

| Komponente | gebundener Pfad | SHA-256 |
| --- | --- | --- |
| G4-Ergebnis | `reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.json` | `783328382545dbf4a08698ebd7a8ba7f3ef06ac344630f2b04e4ef7dd54c5a88` |
| G4-Manifest | gleicher Basispfad mit Suffix `.publication.json` | `63a54a572e4af3067609e93caea503b30f46013d89d968c4fdb2d9719a6597da` |
| G4-Audit | `reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g4_component_independent_audit_2026-09-13.json` | `366d221e6d14093da48f7a8f4ea1a439d4b26e5635b65c95bcb763bc968a2aa5` |
| G5-Ergebnis | `reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.json` | `3321ee6392a6eb2a3c5098fa437cb41bb57b9da7e1c0ada521bdd1e894f4ec39` |
| G5-Manifest | gleicher Basispfad mit Suffix `.publication.json` | `62ed914737028678be360633f4c97b8cb28cd0ef9fae6e7077684fa272a9df8e` |

Der Kompositionsvalidator muss Manifest und Inhaltsartefakte erneut hashen,
die jeweiligen Schemata und Entscheidungen rekonstruieren und insbesondere
`g4-local-infinite-root-pass` sowie `g5-local-direct-stability-pass`
verlangen. Ein gespeichertes Pass-Boolfeld allein genuegt nicht. Der
G5-Rohrecord bleibt wegen seiner dokumentierten Transzendentalsemantik
same-platform; seine Bytes und sein Manifest sind plattformuebergreifend
hashbar.

## 3. G0, Leiter und lokale Zertifikate

Die registrierten Horizonte bleiben

```text
H = (600, 900, 1200, 1500, 1800, 2400, 3600)
```

mit der primaeren Vorwaertsleiter
`1200 -> 1500 -> 1800 -> 2400 -> 3600` und dem getrennten Stressast
`1200 -> 900 -> 600`.

G0 verlangt die bisherigen direkten Summenreplays, endliche Werte und die
registrierten zwei-ULP-$q$-Identitaeten. Jeder Root wird weiterhin durch
genau acht Newtonschritte in getrennten 80-/120-dps-Panels vom unmittelbar
vorherigen Panelmittelpunkt erzeugt. Globale Suche, alternative Startwerte,
Retuning, adaptive Schrittwahl oder eine zweite Chance nach Sichtung eines
Ergebnisses bleiben verboten.

Jedes Panel verwendet die unveraenderten aeusseren und inneren
Krawczyk-Halbbreiten $10^{-8}$ und $10^{-30}$. Beide Praezisionspanels
muessen strikt einschliessen, ihre Mittelpunkte je Koordinate bis
$10^{-50}$ uebereinstimmen und ihre inneren Bilder schneiden.

- `G1F=pass` verlangt alle fuenf Vorwaertspanels.
- `G1R=pass` verlangt die beiden zusaetzlichen tieferen Panels und wird als
  Stressbefund getrennt berichtet.
- Ein Zertifikatsfehler ist `inconclusive`, solange der registrierte lokale
  Ausschlussbaum keinen vollstaendigen Residualausschluss beweist.

## 4. G2: Astidentitaet

Die sechs alten Kanten und ihre Richtung bleiben unveraendert. Jede Kante
wird mit der affinen Homotopie

$$
F_{a,b}(R,\theta;s)=F_a(R,\theta)
+s\,[F_b(R,\theta)-F_a(R,\theta)],\qquad 0\le s\le1,
$$

in exakt 64 nichtadaptiven geschlossenen Scheiben geprueft. Radius- und
Winkelhalbbreite bleiben $10^{-4}$ beziehungsweise $10^{-6}$. Jede Scheibe
muss ein strikt inneres Krawczyk-Bild fuer das volle $s$-Intervall besitzen;
benachbarte Bilder muessen sich schneiden.

- `G2F=pass` verlangt alle vier Vorwaertskanten.
- `G2R=pass` verlangt beide tieferen Stresskanten und bleibt getrennt.
- Ein fehlender Einschluss oder Bildschnitt ist numerisch `inconclusive`,
  nicht automatisch Branchverlust.

Nur nach einem Vorwaertsfehler darf der unveraenderte lokale
Ausschlussfalsifikator bis Tiefe 20 laufen. `registered-local-horizon-branch-loss`
ist ausschliesslich bei einer vollstaendigen dyadischen Partition aus
residualausschliessenden Blaettern zulaessig. Ein anderer Root oder ein
ungeloestes Blatt schliesst diesen Claim.

## 5. G3: zertifizierte Drift

Die Drift wird weiterhin aus outward-rounded Differenzen der geschnittenen
80-/120-dps-Innenintervalle berechnet:

$$
d_{a,b}^{\rm up}=\max\!\left(
\frac{\sup|I_R^{(b)}-I_R^{(a)}|}{0.946517504804225},
\frac{\sup|I_\theta^{(b)}-I_\theta^{(a)}|}{0.015770381717135}
\right).
$$

`G3=pass` verlangt unveraendert

$$
d_{2400,3600}^{\rm up}\le10^{-8}
$$

und

$$
d_{2400,3600}^{\rm up}
\le0.01d_{1800,2400}^{\rm up}+10^{-14}.
$$

Mittelpunktdrift bleibt reine Diagnostik. Fehlende Intervalle ergeben
`inconclusive`; eine vollstaendige Auswertung oberhalb der Schwelle ergibt
`rotating-wave-horizon-branch-drift`.

## 6. Neue, notwendige Endpunktidentitaet

Ein G1--G3-Pass wird erst komponierbar, wenn die neuen Endpunkte mit den
bereits zertifizierten Komponenten dieselben lokalen Roots bezeichnen.
Koordinatennaehe oder sich bloss schneidende Boxen genuegen dafuer nicht.

Fuer $H=2400$ wird das neue 80-/120-dps-Innenbild $I_{2400}$ gegen das
versiegelte G5-Panel geprueft; fuer $H=3600$ wird $I_{3600}$ gegen das
versiegelte G4-Panel geprueft. An jedem Endpunkt muessen beide exakten
Dezimalinklusionen gelten:

1. das neue geschnittene Innenbild liegt vollstaendig in der aeusseren
   Komponentenbox;
2. das innere Krawczyk-Bild der Komponente liegt vollstaendig in der neuen
   120-dps-Aussenbox.

Damit liegt jeder der beiden lokal eindeutigen Roots in der
Eindeutigkeitsbox des anderen. Die Schlussfolgerung ist weiterhin
konditional auf denselben `mpmath.iv`-Vertrauenskern und keine unabhaengige
Intervallreplikation.

Ein fehlender Endpunktschluss ergibt
`sealed-component-endpoint-mismatch`, niemals einen Globalclaim ueber
Nichtexistenz.

## 7. G6 und Entscheidungslogik

G6 wird im neuen Komponentenlauf erneut ausgefuehrt, weil es die endliche
Speicherimplementierung der Leiter kontrolliert. Es verlangt fuer alle sieben
Horizonte die unabhaengige Shift-/Circular-FIFO-Aequivalenz sowie den
$\eta=0$-Kollaps. Die Circular-Implementierung darf weder die native
FIFO-Schrittfunktion aufrufen noch vor dem Lesen materialisieren.

Die Entscheidungen besitzen folgende Praezedenz:

1. G0 oder G6 scheitert:
   `g1-g3-bridge-experiment-invalid`;
2. vollstaendiger lokaler Residualausschluss:
   `registered-local-horizon-branch-loss`;
3. G1F oder G2F ist unvollstaendig:
   `g1-g3-bridge-inconclusive`;
4. G3 scheitert bei vollstaendiger Drift:
   `rotating-wave-horizon-branch-drift`;
5. Endpunktidentitaet zu G4 oder G5 scheitert:
   `sealed-component-endpoint-mismatch`;
6. G0, G1F, G2F, G3, beide Endpunktidentitaeten, versiegeltes G4,
   versiegeltes G5 und G6 bestehen:
   `rotating-wave-root-branch-connected-with-h2400-local-stability-support`.

Der lower-tail-Stressast wird separat als `pass`, `inconclusive` oder
`registered-local-loss` berichtet und kann den logisch aufwaerts gerichteten
Grenztransfer nicht allein widerlegen.

## 8. Ergebnisvertrag, Audit und Stopregeln

Der neue Record speichert primitive Rootpanels, Homotopiescheiben,
Ausschlussleaves, Driftintervalle, G0-/G6-Kontrollen, die vier gebundenen
G4-/G5-Inhaltshashes, Endpunkt-Inklusionszeugen und die Entscheidungsinputs.
Validator und ein standardbibliotheksbasierter Auditor rekonstruieren
Kardinalitaeten, Intervallinklusionen, dyadische Vollstaendigkeit, Drift,
Hashes und Entscheidung getrennt. Der Auditor ist kein zweiter Newton- oder
Intervallbackend.

Reservierte Publikationspfade:

- `reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_2026-09-27.json`;
- gleicher Basispfad mit `.md` und `.publication.json`;
- `reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g1_g3_bridge_independent_audit_2026-09-27.json`;
- `reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_review_2026-09-27.md`.

Vor jeder Zielautorisierung sind erforderlich:

1. separates kritisches Review dieses Protokolls;
2. RED-Tests vor Ergebnisvertrag und Komponentenrunner;
3. targetfreie Falsifikation aller Gate-, Endpunkt-, Hash-, Abbruch- und
   Publikationspfade;
4. separates Code-/Readinessreview ohne Zugriff auf die neue Leiter;
5. sauberer Commit und gruene exakte Linux-CI;
6. neue Nutzerfreigabe, frische UUID, einmalige Governance und Receipt.

Jeder neue Suchstart, jede Schwellenlockerung, adaptive Homotopie, neue
Abhaengigkeit, nachtraegliche Boxaenderung, Drift eines versiegelten
Komponentenhashes oder vorzeitiger Targetzugriff stoppt die Arbeit fuer eine
erneute Amendierung. Ein Pass autorisiert weder einen weiteren G5-/P5-D-Lauf
noch Interaktions-, Traegheits- oder Masseclaims.
