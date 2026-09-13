# Prospektives Protokoll: isolierter G4-Komponentenlauf

Datum: 2026-09-13.

Status: **eingefroren vor erstem G4-Zugriff**.

## 1. Frage und Abgrenzung

Der Komponentenlauf fragt ausschliesslich, ob die bereits registrierte
tail-augmentierte Krawczyk-Methode in einer festen lokalen Box einen Root von
$F_\infty$ zertifiziert. Er ist eine vorgezogene Messung von G4, weil G4
weder Arnoldi noch Trajektorien benoetigt.

Ein Pass ist kein vollstaendiger Fixed-alpha-Transferpass. Insbesondere sind
G1F, G2F, G3, G5 und G6 in diesem Lauf nicht gemessen. P5-D bleibt
geschlossen.

## 2. Eingefrorene Inputs

Es gelten $\alpha=0.01$, $q=0.99$, $M_0=1$, $\eta=0.15$,
$A_{\rm rep}=1$, $\sigma_{\rm rep}=1$, $A_{\rm att}=3.5$ und
$\sigma_{\rm att}=3$. Der endliche Kopf hat $H=3600$. Newton beginnt genau
bei der bereits publizierten Anchor-Koordinate
$(R,\theta)=(0.946517504804225,0.015770381717135)$.

Es gibt keine Parametersuche, keine adaptive Box, keinen alternativen Start
und keinen zweiten Versuch. Der endliche Root wird mit acht 120-dps-
Newtonschritten und den bereits implementierten endlichen Krawczykboxen
$10^{-8}$ und $10^{-30}$ berechnet. Das Tailpanel verwendet Halbbreite
$10^{-10}$ in beiden Koordinaten und die feste Domain
$[0.8,1.1]\times[0.01,0.022]$.

## 3. Ausfuehrungsfolge

Der Runner prueft zuerst sauberen Git-Stand, Protokollhash, Codecommit und
Dependency-Version. Danach berechnet er das endliche 120-dps-Rootpanel. Nur
bei dessen vollstaendigem Pass werden die Tailbounds und dann die 120- und
160-dps-Tailpanels in dieser Reihenfolge berechnet. Nach dem ersten fehlenden
oder nicht strikt einschliessenden Panel stoppt der abhaengige Pfad.

Die Bilder beider Tailpanels werden aus ihren Dezimalendpunkten geschnitten.
Der Runner publiziert Ergebnis-JSON und lesbaren Markdownbericht zuerst und
das gehashte Manifest zuletzt. Ein unvollstaendiger Satz ohne gueltiges
Manifest ist kein Ergebnis.

## 4. Ergebnis- und Auditvertrag

Die Artefakte liegen unter
`reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.{json,md,publication.json}`.
Der Standardbibliothek-Auditor schreibt
`reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g4_component_independent_audit_2026-09-13.json`.

Der Record besitzt fuenf Wurzeln: `identity`, `finite_root`, `infinite_tail`,
`classification` und `publication`. Unbekannte Felder, NumPy-Skalare,
nichtendliche Zahlen, falsche Kardinalitaeten und widerspruechliche
Zusammenfassungen sind unzulaessig. Der Auditor importiert den Runner nicht,
liest das Manifest zuerst, prueft Inhalts- und Protokollhashes, rekonstruiert
Bounds, Boxinklusionen, Panelschnitt und Entscheidung nur mit der
Standardbibliothek. Er ist kein zweiter Intervallbackend.

## 5. Entscheidung

`g4-local-infinite-root-pass` gilt genau dann, wenn das endliche Rootpanel
vollstaendig ist, beide Tailpanels die registrierten Praezisionen und Boxen
besitzen, beide Krawczyk-Bilder strikt im Boxinneren liegen und ihr Schnitt
nichtleer ist.

Ein regulaerer numerischer Fehlschlag ergibt `g4-inconclusive`. Ein
Provenienz-, Schema-, Typ-, Domain-, Hash- oder Publikationsfehler ergibt
`g4-experiment-invalid`. Ein Krawczyk-Fehlschlag beweist keine Nichtexistenz.

## 6. Falsifikation und Stopregeln

Vor Zielzugriff muessen Tests mindestens falsche Praezision, Root ausserhalb
der Domain, Nichtinklusion, disjunkte Bilder, mutierte Bounds, unbekannte
Felder, nichtendliche Zahlen, falsche Hashes und ein fehlendes Manifest
erkennen. Ein Code- oder Formelreview mit Major/Critical-Befund stoppt den
Lauf. Gleiches gilt fuer rote CI oder schmutzigen Arbeitsbaum.

Nach Zielzugriff sind Retuning, Boxvergroesserung, weiterer Newtonstart und
Wiederholung ohne neue Amendierung verboten. Unerwartete technische
Ausnahmen werden als invalid dokumentiert und nicht still repariert.

## 7. Autorisierung und Claimgrenze

Die explizite Nutzeranweisung vom 2026-09-13 autorisiert nach Code-Review den
einmaligen isolierten G4-Lauf. Sie autorisiert weder den vollstaendigen
Horizontlauf noch G5 oder P5-D-Versuch 4.

Ein spaeterer Pass darf als lokales, modell- und backendkonditionales
Existenzzertifikat von $F_\infty$ beschrieben werden. Branchidentitaet vom
Anchor bis $H=3600$, Stabilitaet, Formation, interne $S^1$-Topologie,
Interaktion und Masse bleiben davon unberuehrt.

