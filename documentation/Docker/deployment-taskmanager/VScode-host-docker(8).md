# VScode, Host und Docker

Hier wird der Zusammenhang zwischen Host-Dateisystem, Docker Volume, Container-Dateisystem und VS Code dargestellt. Dabei wird insbesondere nachvollzogen, wie die Testdatei original.txt zwischen Projektverzeichnis, Docker-Image, Docker-Volume und Container bewegt beziehungsweise kopiert wird.

## Grundmodell

Linux-Host
    │
    ├── Host-Dateisystem
    │      │
    │      ├── ~/devops-learning/
    │      │       └── tests/docker-mount-test/
    │      │              └── original.txt
    │      │
    │      └── /var/lib/docker/
    │             └── volumes/
    │                    └── mount-copy-test/
    │                           └── _data/
    │                                  └── original.txt
    │
    ├── VScode
    │
    └── Docker Engine
           │
           ├── Images
           ├── Container
           └── Docker Volumes

Dabei ist wichtig, dass das Docker-Volume ein von Docker verwaltetes Speicherkonzept ist. Bei einem lokalen Docker-Volume liegt der zugehörige Speicher physisch auf dem Docker-Host. Das Volume 'mount-copy-test' z.B. befindet sich in diesem Beispiel unter '/var/lib/...'. Dieser Pfad gehört zur Docker-Verwaltung auf dem Host.

## Ursprungsdatei im Projektverzeichnis

Die ursprüngliche Datei wurde zunächst im Projektverzeichnis erstellt:

/<Pfad>/devops-learning/
└── tests/
    └── docker-mount-test/
        ├── Dockerfile
        └── original.txt

Die Datei wurde von einem Prozess auf dem Linux-Host erstellt. Damit ist sie zunächst eine ganz normale Datei des Host-Dateisystems.

    Host-Dateisystem
           │
           ▼
   ~/devops-learning/
           │
           ▼
tests/docker-mount-test/
           │
           ▼
      original.txt

VScode arbeitet dabei ebenfalls mit dem Host-Dateisystem. Die Datei kann deshalb direkt im VScode-Arbeitsbereich angezeigt und verändert werden.

## Erstellung des Docker Images

Das Dockerfile enthält:

```bash
FROM alpine
RUN mkdir /test
COPY original.txt /test/original.txt
```

Beim Build mit ```bash docker build -t mount-test-image . ``` wird 'original.txt' aus dem Build-Kontext gelesen.

Der entscheidende Punkt ist:

Host-Dateisystem
      │
      │ Build-Kontext
      ▼
Docker Build
      │
      │ COPY
      ▼
Docker Image
      │
      └── /test/original.txt

Dabei wird nicht dieselbe Datei in das Image verschoben. Docker erstellt eine Kopie des Inhalts und speichert sie als Bestandteil des Images. Damit existieren anschließend mindestens zwei voneinander unabhängige Dateien beziehungsweise Speicherobjekte:

Host:
 /home/.../original.txt

Image:
 /test/original.txt

Das erklärt auch die späteren stat-Ergebnisse: Unterschiedliche Inodes zeigen, dass es sich nicht um dieselbe Datei handelt.

## Container wird aus dem Image erzeugt

Beim Befehl ```bash docker run --rm mount-test-image cat /test/original.txt ``` wird ein Container aus dem Image erstellt.

Der Ablauf ist:

Docker Image
     │
     │ docker run
     ▼
 Container
     │
     └── /test/original.txt
              │
              ▼
             cat
              │
              ▼
          Terminalausgabe

Der Container erhält dabei seine Dateisystemsicht aus dem Image. Die Datei '/test/original.txt' stammt deshalb aus dem Image und nicht direkt aus dem ursprünglichen Projektverzeichnis.

## Änderung der Ursprungsdatei

Wird anschließend die Datei im Projektverzeichnis über VScode verändert:

          VScode
            │
            ▼
    Host-Dateisystem
            │
            ▼
/home/kath/.../original.txt

ändert sich nur die Datei im Host-Projektverzeichnis. Die bereits gebaute Image-Version bleibt unverändert.

Also:

  Host-Datei
      │
      │ Änderung
      ▼
"Bitte genauer"

Docker Image
    │
    └── weiterhin alter Stand

Erst ein erneuter Image-Build liest die aktuelle Datei erneut aus dem Build-Kontext und erzeugt ein aktualisiertes Image. Danach enthält ein neu gestarteter Container den neuen Inhalt.

## Kopieren der Datei in das Docker Volume

Das Docker Volume 'mount-copy-test' ist ein eigener Speicherbereich.

Vereinfacht:

Linux Host
    │
    ├── Projektverzeichnis
    │      └── original.txt
    │
    └── Docker Storage
           └── Volume
                └── mount-copy-test
                     └── _data
                          └── original.txt

Der Container kann das Volume beispielsweise unter '/test' einbinden:

```bash
docker run --rm \
  -v mount-copy-test:/test \
  alpine \
  ls -l /test
```

Im Container erscheint das Volume dann unter:

Container
    │
    └── /test
          │
          ▼
      Docker Volume
      mount-copy-test

Der Pfad '/test' im Container ist dabei nicht dasselbe Verzeichnis wie '/var/lib/...'. Es handelt sich um zwei verschiedene Pfade innerhalb zweier verschiedener Dateisystemsichten.

Das Volume stellt jedoch die Verbindung zwischen beiden her:

Host
/var/lib/docker/volumes/
    mount-copy-test/
        _data/
            original.txt
                ▲
                │
                │ Volume-Mount
                │
                ▼
        Container
        /test/original.txt

## VS Code und Docker Volume

Zwischen VScode und Docker ergibt sich der Zusammenhang über das Host-Dateisystem:

                Linux Host
                     │
    ┌────────────────┴────────────────┐
    │                                 │
    ▼                                 ▼
VS Code                         Docker Engine
    │                                 │
    │                                 ▼
    |                           Docker Volume
    │                                 │
    │                                 ▼
    │                      /var/lib/docker/volumes/
    │                                 │
    │                                 ▼
    │                         _data/original.txt
    │                                 |
    └─────── Host-Dateisystem ────────┘

VScode muss dafür nicht wissen, dass Docker diese Datei als Bestandteil eines Volumes betrachtet. Für das Betriebssystem ist der Pfad zunächst eine Datei im Host-Dateisystem. Docker verwendet diesen Speicherbereich für sein Volume. Die Datei    '/var/lib/.../original.txt' liegt auf dem Docker-Host. Der Host speichert dort die Daten des lokalen Docker-Volumes.
VScode arbeitet ebenfalls auf dem Host und kann, sofern die entsprechenden Dateisystemberechtigungen vorhanden sind, Dateien des Host-Dateisystems lesen. Denn nicht jeder Prozess auf dem Host darf auf alles zugreifen.
Auch hier entscheidet das Betriebssystem anhand der Identität des zugreifenden Prozesses und der geltenden Dateisystemberechtigungen.

## Vergleich der beiden 'original.txt'-Dateien

Anschließend werden die Projektdatei '/home/.../original.txt' und die Volume-Datei '/var/lib/.../original.txt' miteinander verglichen.
Mit dem Befehl ```bash sudo stat /<Pfad>/original.txt ``` können die Stats beider Dateien ausgegeben werden.
 
Stat zeigt im Vergleich:

      | Projektdatei  | Volume-Datei
------------------------------------
Inode | 22282478      | 22392031
UID   | 1000/user     | 0/root
GID   | 1000/user     | 0/root

Damit wird deutlich:

unterschiedlicher Inode
        ↓
nicht dieselbe Datei

Auch die Entstehungszeitpunkte unterscheiden sich. Die Projektdatei wurde bereits um 14:16 Uhr erstellt, während die Datei im Volume erst um 14:22 Uhr entstand.

Das passt zum beobachteten Ablauf:

14:16
Projektdatei wird erstellt
            │
            ▼
  /home/.../original.txt
            │
            │ späterer Docker-/Volume-Vorgang
            ▼
14:22
Datei im Volume entsteht
            │
            ▼
   /var/.../original.txt

Der gleiche Inhalt bedeutet deshalb nicht, dass es sich um dieselbe Datei handelt.

## Keine automatische Synchronisation

Eine weitere wichtige Erkenntnis entstand durch die Änderung der 'original.txt'-Datei in VScode. Die Projektdatei wird verändert, aber der Inhalt der Volume-Datei bleibt unverändert.

Damit wurde praktisch bestätigt:

Projektdatei
    │
    │ Änderung
    ▼
Host-Datei verändert

Volume-Datei
    │
    └── bleibt unverändert

Es findet also keine automatische Synchronisation zwischen beiden Dateien statt. Die beiden Dateien sind unabhängig voneinander. Das ist ein wichtiger Unterschied zu einem Bind-Mount.

## Bind-Mount im Vergleich

Bei einem Bind-Mount wird ein vorhandener Host-Pfad direkt in den Container eingebunden.

Vereinfacht:

Host
/home/.../taskmanager.db
          │
          │ Bind-Mount
          ▼
  Container
  /data/taskmanager.db

Container und Host greifen dabei auf dieselbe Host-Datei beziehungsweise denselben Host-Verzeichnisinhalt zu.

Beim Docker-Volume sieht das Modell anders aus:

Host
/var/lib/docker/volumes/
          │
          ▼
    Docker Volume
    mount-copy-test
          │
          ▼
   Container:/test

Der konkrete Host-Speicherort wird dabei von Docker verwaltet.

## Gesamtmodell des Tests

Der gesamte bisherige Ablauf lässt sich damit zusammenführen:

                  Linux Host
                      │
     ┌────────────────┼────────────────┐
     │                │                │
     ▼                ▼                ▼
Projektdatei       VS Code       Docker Engine
     │                                 │
     │ Build-Kontext                   │
     ▼                                 ▼
Docker Build                     Docker Volume
     │                          mount-copy-test
     ▼                                 │
   Image                               │
     │                                 │
     │ docker run                      │
     ▼                                 │
 Container                             │
     │                                 │
     └──────────── /test ──────────────┘
                     │
                     ▼
                original.txt

Dabei existieren mehrere voneinander getrennte Speicherobjekte:

- Projektdatei
  /home/.../original.txt

- Datei im Docker Image
  /test/original.txt

- Datei im Docker Volume
  /var/.../original.txt

- Datei im Container
  Sichtbar unter dem Mount-Pfad '/test'

Je nach Vorgang kann Inhalt von einem Bereich in einen anderen kopiert oder ein Speicherbereich über einen Mount in einen Container eingebunden werden.
Wichtiges Denkmodell

Für die weitere Arbeit mit Docker ist deshalb folgende Fragestellung besonders hilfreich:

      Welcher Prozess
             │
             ▼
greift mit welcher Identität
             │
             ▼
    auf welche Ressource
             │
             ▼
    über welchen Pfad
             │
             ▼
mit welchen Berechtigungen
             │
             ▼
            zu?

Es wird betrachtet, welcher Prozess tatsächlich auf welche Ressource zugreift und welche Regeln dabei vom Linux-System und von Docker angewendet werden.

## Ergebnis

Durch den Test wurde der Zusammenhang zwischen Host-Dateisystem, Docker-Image, Container, Docker-Volume und VScode praktisch nachvollzogen.

Dabei wurde insbesondere festgestellt:

- Die ursprüngliche original.txt liegt im Projektverzeichnis auf dem Host.
- COPY übernimmt den Inhalt der Datei in das Docker Image.
- Beim Erstellen eines Containers wird die Datei aus dem Image sichtbar.
- Eine Änderung der ursprünglichen Host-Datei verändert ein bereits vorhandenes Image 
  nicht.
- Ein erneuter Image-Build übernimmt den aktuellen Stand der Quelldatei.
- Ein Docker Volume besitzt einen eigenen Speicherbereich auf dem Docker Host.
- Der Speicherort eines lokalen Volumes wird von Docker verwaltet.
- Eine Datei im Volume und die ursprüngliche Projektdatei sind unterschiedliche Dateien.
- Dies wurde unter anderem anhand unterschiedlicher Inodes und Entstehungszeiten 
  nachgewiesen.
- Zwischen der Projektdatei und der Datei im Volume findet keine automatische 
  Synchronisation statt.
- VS Code benötigt keine spezielle Docker-Verbindung, um eine normale Datei des 
  Host-Dateisystems anzuzeigen.
- Dateisystemberechtigungen bestimmen, welcher Prozess auf welche Dateien und  
  Verzeichnisse zugreifen darf.
- Ein Container sieht ein Volume über den Mount-Pfad, während der zugehörige Speicher 
  auf dem Host liegt.

Damit lässt sich das bisherige Modell erweitern:

Linux Host
│
├── Host-Dateisystem
│   │
│   ├── Projektdateien
│   │      └── original.txt
│   │
│   └── Docker Storage
│          └── Docker Volume
│                 └── original.txt
│
├── VS Code
│
└── Docker Engine
       │
       └── Container
              │
              └── Mount
                    │
                    ▼
                 Volume