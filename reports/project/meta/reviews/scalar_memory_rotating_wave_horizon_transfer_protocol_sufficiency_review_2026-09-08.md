# Suffizienzreview: Rotating-wave-Horizonttransfer-Protokoll

Datum: 2026-09-08.

Gepruefte amendierte Protokollrevision:
`f817574a5562ca6cd012752eeb414d5b5ecd555f`.

Gepruefter Protokollblob:
`401f12d6572ecac943e0a0cc3ca19edf6236915a`.

Geprueftes negatives Review: Revision
`c1ee529d969ebafed7a557e3db47eba95a38af17`, Blob
`11b3f86320d976cb9d77f50d79cc69c5c48cd971`.

Gepruefte CI:
[GitHub Actions run 34186699863](https://github.com/MemoryDynamics/Knoten/actions/runs/34186699863),
erfolgreich fuer den finalen amendierten Protokollstand. Die vorausgehenden
Amendierungs- und Reviewrevisionen besitzen ebenfalls gruene CI.

Verdict:
**`rotating-wave-horizon-transfer-protocol-sufficient-implementation-closed`**.

Das amendierte Protokoll schliesst HT-P01--HT-P06 und definiert einen
falsifizierbaren lokalen Roottransfer von der exakten finite-$H$-Map zur
unendlichen exponentiellen Erinnerung. Es autorisiert als naechstes nur den
getrackten Ergebnisvertrag und zunaechst rote targetfreie Tests. Runnercode,
neue Rootberechnung, Horizonttrajektorie und P5-D-Versuch 4 bleiben bis zu den
jeweils registrierten spaeteren Schritten geschlossen.

## 1. Schliessung der sechs Findings

### HT-P01 -- geschlossen

Exaktes dezimales `q_dec=0.99`, produktives
`q64=1.0-float("0.01")` und die `log1p`-Diagnostik sind nun getrennte
Repraesentationen. Nur semantisch identische binary64-Pfade entscheiden das
Kontrollgate: `q64**H` gegen `exp(H*log(q64))` mit zwei ULP Toleranz.

Eine targetfreie Standardbibliothek-Auswertung der sieben registrierten
Horizonte ergibt fuer diesen Vergleich null oder einen ULP. Der verworfene
Vergleich mit `log1p(-alpha64)` weicht dagegen relativ um etwa
`5.23e-15` bis `2.85e-14` ab und bleibt korrekt als
Repraesentationsdiagnostik sichtbar. Die Amendierung lockert damit keine
Schwelle, sondern vergleicht erstmals dieselbe Zahlensemantik.

### HT-P02 -- geschlossen

Die Driftgates verwenden outward-rounded Suprema der Differenzen der
geschnittenen 80-/120-dps-Rootintervalle. Die Nenner sind die festen,
positiven publizierten Anchor-Skalen $R_\star$ und $\theta_\star$; damit ist
die Metrik auch unabhaengig von Intervallvorzeichen und -breite definiert.
Mittelpunktdrift ist nur Diagnostik. Eine obligatorische Breitenmutation
falsifiziert den Pass.

### HT-P03 -- geschlossen

Die Circular-FIFO-Kontrolle muss `head`, modulare Altersadressierung,
Kraftakkumulation und Overwrite-after-read selbst implementieren. Sie darf
weder vor der Kraftrechnung materialisieren noch `native_fifo_step`
aufrufen. Alters-Hash, neuer Punkt und kompletter Folgezustand werden mit
definierter symmetrischer Relativnorm verglichen. Drei Index-/Overwrite-
Mutationen sind vorregistriert.

### HT-P04 -- geschlossen

Der Ergebnisvertrag besitzt genau sieben semantische Rootobjekte und
fail-closed Typen, Kardinalitaeten und `null`-Semantik. Er muss zusammen mit
roten Tests vor dem Runnercode committed werden. JSON und Markdown sind die
genau zwei vor dem Manifest erzeugten und gehashten Inhaltsartefakte; das
Manifest ist Commitpunkt und hasht sich nicht selbst. Der Auditoroutput ist
ein eigener, danach erzeugter Pfad.

Der Standardbibliothek-Auditor prueft Manifest, Hashes und Vertrag zuerst und
rekonstruiert Parameter, $q$-Repraesentationen, Tailbounds,
Intervall-Driftobergrenzen und Entscheidung unabhaengig. Krawczyk, Arnoldi und
Trajektorien bleiben ausdruecklich numerische Runner-Vertrauensgrenzen. Es
wird keine unabhaengige wissenschaftliche Reproduktion behauptet.

### HT-P05 -- geschlossen

Die zwei Arnoldi-Panels muessen exakt 24 und 36 endliche Eigenpaare mitsamt
Vektoren und Residuen liefern. Partielle ARPACK-Ausgaben, fehlende Vektoren,
falsche Kardinalitaet oder ein zu grosses Residuum sind G5-inconclusive.
Numerische Instabilitaet verlangt zusaetzlich vollstaendige Panels,
Symmetrie-/Panelkontrollen und den registrierten Faktor-100-Wachstumsarm.

### HT-P06 -- geschlossen

Der Ausschlussausgang heisst nun
`registered-local-horizon-branch-loss` und kann keinen globalen Rootverlust
suggerieren. Nur der vollstaendige Roottransferpass mit Large-H-
Stabilitaetsstuetzung darf spaeter ein getrenntes P5-D-Governancereview
oeffnen. Alle anderen Ausgaenge halten P5-D geschlossen; selbst der Pass
ersetzt weder Nutzerentscheidung noch neue UUID, Receiptpfad oder
Governance-only-Commit.

## 2. Wissenschaftliche Suffizienz

Die Horizonfrage wird von zwei angrenzenden, aber schwaecheren Befunden
getrennt:

1. Der fruehere $C=6,9,12$-Test betrifft einen retunten linearen
   Center-Relaxationsmodus, nicht den nichtlinearen Kreisroot.
2. Der bestehende $H\alpha=12$-Skalenast variiert $\alpha$ und $H$
   gemeinsam, nicht $H$ bei festem Vergessen.
3. Der neue Vorwaertsast haelt erstmals $\alpha$, $\eta$, $M_0$, Kernel und
   $\varepsilon=0$ fest.
4. Lokale finite Roots, Branchhomotopie, Drift und unendlicher Tail besitzen
   getrennte Gates.
5. Roottransfer und numerische Large-H-Stabilitaet koennen getrennt positiv,
   negativ oder inconclusive ausfallen.
6. Die tiefere $H=900,600$-Belastung bleibt sichtbar, kann aber den logisch
   anderen Grenzuebergang nach oben nicht allein falsifizieren.

Die analytischen Residual- und Jacobiantailbounds wurden im negativen Review
direkt hergeleitet und blieben unveraendert. Ein strikt inneres
Tail-Krawczyk-Bild bei `H=3600` ist ausreichend fuer einen lokalen Root von
$F_\infty$ in der registrierten Box, konditional auf den Intervallbackend.
Der feste $s$-Schlauch verhindert, dass ein erfolgreicher Endpunktfit ohne
Branch-Identitaet als Fortsetzung zaehlt.

## 3. Verbleibende Claimgrenzen

- Die feste Homotopiebox und 64 $s$-Scheiben koennen zu eng sein. Ein
  Zertifikatsfehler ist dann inconclusive und darf nicht post hoc repariert
  werden.
- `mpmath.iv` ist derselbe getrackte Intervallbackend wie zuvor, kein
  unabhaengiger zweiter Beweiskern.
- Das H=2400-Panel liefert lokale numerische Stabilitaetsstuetzung, keine
  vollstaendige Spektraleinschliessung oder Stabilitaet des unendlichen
  Feldzustands.
- Ein Anchor-Branch belegt weder globale Eindeutigkeit noch generische
  Formation oder eine stabile Parameterfamilie.
- Weder Root noch Stabilitaet implizieren Interaktion, harmonischen
  Oszillator, Traegheit oder Masse.

Diese Einschraenkungen sind im Protokoll entscheidungswirksam oder als
obligatorische Claimgrenze festgehalten und blockieren deshalb nicht die
narrowe Implementierungsfreigabe.

## 4. Autorisierte naechste Grenze

Der naechste Commit darf ausschliesslich den registrierten
`scalar_memory_rotating_wave_horizon_transfer_result_schema_v1.json` und
zunaechst fehlschlagende targetfreie Tests fuer Schema, Formeln, Tail,
Intervall-Drift, Homotopie, partielle Arnoldi-Ausgaben, unabhaengiges
Circular-FIFO, Entscheidung, Publikation und Auditor enthalten.

Er darf keine neue Rootmitte berechnen, keine registrierte Horizontgeschichte
fortsetzen, keinen Arnoldi-Holdout auswerten und keinen Ergebnis- oder
Manifestpfad schreiben. Erst ein dokumentierter RED-Zustand oeffnet die
kleinste protokollkonforme Implementierung; danach sind Gesamttests, Ruff,
strikte Dokumentation, separates Readinessreview und gruenes CI erforderlich.

Das positive Protokollurteil ist somit eng:
**`rotating-wave-horizon-transfer-protocol-sufficient-implementation-closed`**.
