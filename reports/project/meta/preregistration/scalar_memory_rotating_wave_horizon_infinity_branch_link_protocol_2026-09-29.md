# Prospektives Protokoll: uniformer Tail-Branch-Link $F_{3600}\to F_\infty$

Datum: 2026-09-29.

Status: **vor jeder neuen Branch-Link-Zertifikatsrechnung eingefroren**.

## 1. Frage und Abgrenzung

Der positive G1--G3-Lauf verbindet den lokalen endlichen Rootast bis zum
versiegelten G4-Root bei $H=3600$. G4 zertifiziert getrennt einen lokal
eindeutigen Root von $F_\infty$ in einer groesseren Box um denselben
Mittelpunkt. Dieses Gate fragt ausschliesslich, ob beide Roots durch die
natuerliche Tail-Homotopie zum selben lokalen Loesungsast gehoeren.

Ein Pass ist kein Stabilitaetsbeweis fuer $H=3600$ oder $H=\infty$ und kein
Nachweis von globaler Eindeutigkeit, Formation, Interaktion, interner Phase,
Spin, Traegheit oder Masse.

## 2. Eingefrorene Homotopie

Mit dem bereits analytisch begrenzten Rest

$$
T_{3600}(R,\theta)=F_\infty(R,\theta)-F_{3600}(R,\theta)
$$

wird ausschliesslich

$$
F_s(R,\theta)=F_{3600}(R,\theta)+sT_{3600}(R,\theta),
\qquad s\in[0,1]
$$

verwendet. Damit gilt exakt $F_0=F_{3600}$ und $F_1=F_\infty$. Der Parameter
$s$ skaliert nur die Speicherbeitraege der Alter $j\ge3600$; $q$, $g$,
$\alpha$, $\eta$, $M_0$, Kernel und die beiden Unbekannten $(R,\theta)$
bleiben unveraendert.

Es werden keine weiteren Horizonte, keine frei waehlbare
Gleichungsinterpolation und keine nach Ergebnis angepassten Slabs zugelassen.

## 3. Eingefrorene Inputs

Das Gate konsumiert read-only und hashgebunden:

1. G1--G3-Attempt-2-Resultat, Publikationsmanifest und unabhaengigen Audit;
2. G4-Resultat, Publikationsmanifest und unabhaengigen Audit;
3. den kanonischen Git-Blob der Intervallbibliothek und des neuen Gates;
4. `mpmath==1.3.0` als deklarierte Intervall-Trust-Base.

Die G1--G3-Koordinate bei $H=3600$ muss bytegenau der versiegelten
G4-Finite-Root-Koordinate entsprechen. Alle Publikationshashes und
Entscheidungen muessen vor der Zertifikatsrechnung erneut validiert werden.

## 4. Feste Parameter und Box

Es gelten die versiegelten G4-Parameter

$$
\alpha=0.01,\quad q=0.99,\quad \eta=0.15,\quad M_0=1,
\quad H=3600
$$

mit den bereits registrierten Kernelparametern. Mittelpunkt ist exakt der
120-dps-G4-Finite-Root. Fuer beide Koordinaten wird die gemeinsame Halbbreite

$$
h_R=h_\theta=10^{-10}
$$

verwendet. Die einzigen Praezisionspanels sind 120 und 160 Dezimalstellen.
Die Tailbounds werden mit den bestehenden geschlossenen Formeln neu
berechnet und muessen bytegenau den im G4-Record gespeicherten Bounds
entsprechen.

## 5. Uniformes Zertifikat

Fuer $X=[c-h,c+h]$ und $S=[0,1]$ werden die bestehenden Bounds

$$
\|T_{3600}\|_2\le b_0,\qquad
\|\partial_R T_{3600}\|_2\le b_R,\qquad
\|\partial_\theta T_{3600}\|_2\le b_\theta
$$

als outward-gerundete Komponentenintervalle verwendet. Der uniforme
Krawczyk-Operator muss fuer jedes Praezisionspanel

$$
K(X,S)=c-YF_S(c)+(I-YD F_S(X))(X-c)
\subset\operatorname{int}(X)
$$

erfuellen. Zusaetzlich muss fuer das gesamte Intervall-Jacobian gelten

$$
\rho_\infty=
\sup_{A\in D F_S(X)}\|I-YA\|_\infty < 1.
$$

Die zweite Bedingung macht die fuer die Astidentitaet benoetigte uniforme
Regularitaet und lokale Eindeutigkeit explizit, statt sie nur aus einer
Ergebnisbezeichnung abzulesen.

Die 120-/160-dps-Krawczyk-Bilder muessen sich koordinatenweise schneiden.
Ein gemeinsamer Ein-Box-Pass ist erforderlich. Wenn er scheitert, ist das
Ergebnis `inconclusive`; dieses Protokoll autorisiert keine nachtraegliche
Boxaufweitung, Slabzerlegung oder Parametersuche.

## 6. Endpunkt- und Astlemma

Der Ergebnisvalidator muss folgende logische Kette explizit rekonstruieren:

1. Die uniformen Inklusionen liefern fuer jedes $s\in[0,1]$ einen Root in
   $X$.
2. $\rho_\infty<1$ liefert lokale Eindeutigkeit und Regularitaet in derselben
   Box fuer jedes $s$.
3. Stetigkeit von $F_s$ und Eindeutigkeit implizieren eine stetige
   Rootabbildung $x(s)$.
4. Bei $s=0$ stimmt der eindeutige Root mit dem versiegelten endlichen
   G4-/G1--G3-Root ueberein.
5. Bei $s=1$ stimmt er mit dem durch G4 zertifizierten lokalen
   $F_\infty$-Root ueberein.

Nur wenn alle fuenf Aussagen maschinenlesbar aus den Inputs und
Zertifikatsfeldern folgen, darf Branchidentitaet berichtet werden.

## 7. Gates und Klassifikation

Ein Pass verlangt gleichzeitig:

- **U0 Provenienz:** alle sechs versiegelten Inputs, Git-Blobs und
  Entscheidungen stimmen;
- **U1 Modellidentitaet:** $F_0=F_{3600}$, $F_1=F_\infty$ und die
  Tailbound-Replays stimmen;
- **U2 Uniformer Einschluss:** beide Praezisionspanels sind strikt;
- **U3 Regularitaet:** beide Panels haben $\rho_\infty<1$;
- **U4 Endpunktbindung:** finite und unendliche G4-Zertifikate liegen in der
  gemeinsamen Box und sind ueber Eindeutigkeit gebunden;
- **U5 Reproduktion:** die beiden Krawczyk-Bilder ueberlappen;
- **U6 Audit:** der getrennte Standardbibliotheksauditor rekonstruiert
  Schema, Hashes, Dezimalrelationen, Gates und Entscheidung.

Nur dann lautet die Entscheidung
`g-infinity-uniform-tail-branch-link-pass`. Ein vollstaendiger, gueltiger
Record mit mindestens einem negativen U1--U5-Gate lautet
`g-infinity-branch-link-inconclusive`. Schema-, Provenienz-,
Publikations- oder Auditwidersprueche sind `invalid` und duerfen nicht als
physikalischer Negativbefund interpretiert werden.

## 8. Falsifikationstests vor einem Ergebnislauf

Mindestens folgende Mutationen muessen fail-closed getestet werden:

1. vertauschtes Tailvorzeichen oder ein Endpunkt ungleich $s=0/1$;
2. zu kleine, nicht finite oder inward-gerundete Tailbounds;
3. unvollstaendige $s$-Abdeckung;
4. Krawczyk-Bild auf oder ausserhalb des Boxrandes;
5. $\rho_\infty\ge1$ oder falsch zusammengefasste Regularitaet;
6. disjunkte 120-/160-dps-Bilder;
7. veraenderte G4-/G1--G3-Koordinate, Hash, Entscheidung oder Manifest;
8. vorbestehender Ergebnis-, Receipt-, Audit- oder Manifestpfad.

Der Auditor darf weder Produktionsvalidator noch Produktionsklassifikator
importieren. Er ist ein unabhaengiger Record-/Dezimalauditor, aber weiterhin
kein zweiter Intervallbackend.

## 9. Ausfuehrungsgrenze

Protokoll, Schema, Validator, Auditor, Runner, rote Tests und Reviews werden
vor jeder neuen Zertifikatsrechnung separat committed und durch die
offizielle CI gebunden. Die Governance bleibt bis zu einer spaeteren
expliziten Einmalfreigabe geschlossen. Dieses Protokoll selbst autorisiert
keinen Targetlauf und keine Ergebnisdatei.

## 10. Erlaubte Sprache nach einem Pass

Zulaessig waere:

> Der lokal zertifizierte finite Rootast bis $H=3600$ setzt sich unter der
> natuerlichen, uniform Krawczyk-zertifizierten Tail-Homotopie stetig und
> lokal eindeutig zum separat zertifizierten Root von $F_\infty$ fort.

Nicht zulaessig blieben insbesondere $H\to\infty$-Stabilitaet, globale
Eindeutigkeit, generische Formation, Interaktion, Spin, Traegheit oder
physikalische Masse.
