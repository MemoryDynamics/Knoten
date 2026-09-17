# G5 Pre-Merge-Review aus Referee-Perspektive

Stand: 2026-09-17.

Verdict: **`g5-premerge-referee-pass-major-remediated-claim-restricted`**

Dieses interne Referee-Review ist keine unabhaengige externe Replikation. Es
prueft den bereits versiegelten Attempt-3-Record, seine Code- und
Publikationskette sowie die Zulassungsfaehigkeit des kumulativen Branches fuer
die Mainline. Fruehere wissenschaftliche Bloecke bleiben durch ihre eigenen
Reviews gedeckt; hier liegt der Schwerpunkt auf G5 und seiner Integration.

## 1. Gepruefter Befund

Der vorregistrierte Attempt 3 bleibt korrekt als
`g5-local-direct-stability-pass` klassifiziert. Beide vollstaendigen
Largest-modulus-Arnoldi-Panels finden dasselbe fuehrende transversale Paar
bei Betrag ungefaehr `0.9930442`; ihre Abweichung ist
`1.6755588669714317e-10`. Alle gespeicherten Ritzresiduen, Symmetriemoden,
drei nichtlinearen Stoerungsarme und die ungestoerte Kontrolle bestehen ihre
eingefrorenen Grenzen. Receipt, Ergebnis, Lesereport und Manifest stimmen
hashbasiert ueberein.

Der Record wurde nicht neu erzeugt und keine wissenschaftliche Zahl wurde
geaendert. Der Execution-Commit, der historische Auditorblob und die
Autorisierungs-UUID bleiben im Record und in der Git-Historie erhalten.

## 2. Falsifizierender Codebefund und Remediation

Das Review fand einen Major-Befund in der beschriebenen, nicht in der
numerischen Unabhaengigkeit: Der G5-Auditor importierte den gemeinsamen
`strict_json_contract` ueber `emergenz_knoten`. Python fuehrte dadurch
transitiv das Paket-`__init__` aus und benoetigte NumPy/SciPy, obwohl der
Auditor selbst keine numerische Bibliothek verwendete. Der vorhandene
AST-Test erkannte direkte numerische Imports, aber nicht diesen transitiven
Pfad.

Ein neuer RED-Test reproduzierte beide Fehler: den Paketimport im AST und das
Scheitern des Auditorimports in einem isolierten Standardbibliotheksprozess.
Die Remediation laedt ausschliesslich den gemeinsamen generischen
JSON-Vertragsvalidator direkt per `importlib` aus seiner Datei. Sie aendert
weder Schwellen noch Rekonstruktion, Entscheidung oder Ergebnisartefakte.

Nach der Korrektur bestehen:

1. der AST-Test ohne Paket- oder numerischen Import;
2. der isolierte Auditorimport mit Python `-I`;
3. der vollstaendige Audit des getrackten Attempt-3-Records im selben
   isolierten Prozess;
4. alle 30 G5-Komponenten- und Auditor-Tests.

Der Auditor teilt weiterhin den rein generischen Vertragsinterpreter mit dem
Runner. Seine Schwellen-, Hash-, Panel-, Trajektorien- und
Entscheidungsrekonstruktion bleibt separat implementiert. Das ist logische
Unabhaengigkeit, keine zweite numerische Implementierung.

## 3. Referee-Grenzen

- ARPACK liefert numerische Largest-modulus-Panels, keine rigorose
  Intervallschranke fuer alle 4800 Eigenwerte.
- Drei registrierte Stoerungsrichtungen und 5000 Schritte belegen lokale
  endliche Kontraktion, keinen offenen Basin-Ball oder asymptotischen Satz.
- G4 zertifiziert lokal einen Root von (F_\infty); G5 stuetzt Stabilitaet
  bei genau (H=2400). Ohne G1--G3 folgt daraus keine Branchverbindung und
  keine (H\to\infty)-Stabilitaet.
- Der 30,7-MB-Rohrecord ist unterhalb der GitHub-Einzeldateigrenze und
  manifestgebunden, vergroessert aber das Repository dauerhaft. Weitere
  Vollvektorrecords brauchen vorab eine Archivierungsstrategie.
- Die binary64-Transzendentalevidenz bleibt als same-platform gekennzeichnet.

Damit bleiben Formation, Interaktion, internes (S^1), Spin, Traegheit und
physikalische Masse gesperrt.

## 4. Integrationsurteil

Der Branch ist ein direkter Nachfahre von `main`; es gibt keine divergente
Mainline und keinen Mergekonflikt. Die frueheren Bloecke sind in getrennten
Protokollen und Reviews dokumentiert. Fuer G5 verbleibt nach der beschriebenen
Remediation kein Critical- oder Major-Codebefund.

Nach gruener exakter Branch-CI darf der kumulative Stand in `main`
fast-forward integriert werden. Der naechste wissenschaftliche Block ist
G1--G3 samt G0-/G6-Integration. Ein neuer G5-Lauf, P5-D-Lauf oder
Parameter-Retuning ist dadurch nicht autorisiert.

