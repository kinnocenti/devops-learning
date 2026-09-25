# Container-Dateisystem und Mounts

Im bisherigen Verlauf des Docker-Lernprojekts wurden bereits Image-Layer, Container-Layer, Copy-on-Write, Bind-Mounts und Docker Volumes praktisch untersucht. Dabei entstand zunächst folgendes vereinfachtes Modell:

   Dockerfile
       ↓
     Image
       ↓
   Container
       ↓
Container-Layer

Für persistente Daten wurde dieses Modell anschließend erweitert:

Container
    │
    ├── Container-Layer
    │       ↓
    │    flüchtige Daten
    │
    └── Mount
          ↓
      persistenter Storage

Mit den bisherigen Tests wurde bereits festgestellt:

- Änderungen im Container-Layer gehören zum Lebenszyklus des Containers.
- Beim Löschen eines Containers wird dessen Container-Layer entfernt.
- Image-Layer bleiben erhalten und können für neue Container verwendet werden.
- Daten in einem Docker Volume bleiben unabhängig vom Container bestehen.
- Ein Volume kann von einem neuen Container erneut eingebunden werden.
- Ein Mount stellt einen externen Speicherbereich an einem bestimmten Pfad innerhalb 
  des Containers bereit.

Der nächste Lernschritt diente dazu, diese Zusammenhänge noch genauer zu verstehen.

## Das Container-Dateisystem

Ein Container besitzt aus Sicht der Anwendung ein eigenes Dateisystem. Beispielsweise kann ein Alpine-Container folgende Verzeichnisse enthalten:

/
├── bin
├── dev
├── etc
├── home
├── lib
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── sbin
├── srv
├── sys
├── tmp
├── usr
└── var

Diese Verzeichnisstruktur ist innerhalb des Containers sichtbar. Sie bedeutet jedoch nicht, dass der Container einen eigenen vollständigen Linux-Kernel oder einen eigenen physischen Computer besitzt. Die Prozesse des Containers verwenden weiterhin den Kernel des Docker Hosts. Das Container-Dateisystem ist daher Teil der isolierten Laufzeitumgebung des Containers.

## Dateien im Container-Layer

Um den Container-Layer praktisch zu untersuchen, wird ein temporärer Alpine-Container gestartet:

```bash
docker run --rm -it --name mount-test alpine sh
```

Innerhalb des Containers wird anschließend ein neues Verzeichnis angelegt:

```bash
mkdir /test
```

Danach wird eine Datei erzeugt:

```bash
echo "Ich komme aus dem Container-Layer" > /test/datei.txt
```

Die Datei kann anschließend gelesen werden:

```bash
cat /test/datei.txt
```

Ausgabe:

Ich komme aus dem Container-Layer

Auch die Dateirechte können untersucht werden:

```bash
ls -l /test
```

Die Datei befindet sich zu diesem Zeitpunkt ausschließlich im beschreibbaren Bereich des Containers.

Vereinfacht:

Image
  │
  ▼
Container
  │
  └── Container-Layer
          │
          └── /test/datei.txt

Die Datei gehörte damit zum Lebenszyklus dieses Containers. Wurde der Container gelöscht, wurde auch der zugehörige Container-Layer gelöscht. Die Datei 'datei.txt' existierte danach nicht mehr.

## Container-Layer und Image-Layer

Dabei ist eine wichtige Unterscheidung notwendig.

Ein Image besteht aus seinen Image-Layern:

Image
├── Layer 1
├── Layer 2
└── Layer 3

Beim Erstellen eines Containers kommt ein beschreibbarer Container-Layer hinzu:

Image
├── Layer 1
├── Layer 2
└── Layer 3
        │
        ▼
Container-Layer

Änderungen, die während der Laufzeit vorgenommen werden, landen grundsätzlich im beschreibbaren Container-Layer und verändern nicht das zugrunde liegende Image. Daher kann dasselbe Image später wieder für einen neuen Container verwendet werden. Das wurde bereits mit Copy-on-Write praktisch nachvollzogen.

Beispiel:

Image
  │
  ├── Container A
  │      └── Datei verändert
  │
  └── Container B
         └── ursprünglicher Zustand

Container A und Container B besitzen jeweils eigene beschreibbare Container-Layer.

## Der Container-Layer ist flüchtig

Die Datei 'datei.txt' zeigte praktisch:

Container A
    │
    └── /test/datei.txt
            │
            ▼
      Container-Layer
            │
            ▼
    Container wird gelöscht
            │
            ▼
      Container-Layer gelöscht
            │
            ▼
       Datei gelöscht


Damit wurde das bisherige Verständnis bestätigt. Der Container-Layer besitzt grundsätzlich denselben Lebenszyklus wie der Container. Das bedeutet nicht, dass Container grundsätzlich keine Dateien schreiben können. Sie können sehr wohl Dateien erzeugen und verändern.
Daten, die ausschließlich im Container-Layer liegen, sind also nicht für eine dauerhafte Speicherung über den Lebenszyklus des Containers hinweg geeignet.

## Mounts

Ein Mount verändert dieses Modell. Ein Speicherbereich außerhalb des Container-Layers kann an einem bestimmten Pfad innerhalb des Containers bereitgestellt werden.

Beispielsweise:

Docker Volume
     │
     ▼
Container:/data

Innerhalb des Containers sieht die Anwendung dann '/data'. Die Anwendung muss dabei nicht wissen, wie der Speicher außerhalb des Containers technisch organisiert ist. Für den Taskmanager wurde genau dieses Prinzip verwendet:

Taskmanager
    │
    ▼
/data/taskmanager.db
    │
    ▼
Docker Volume
taskmanager-data

Damit liegt die Datenbank nicht im flüchtigen Container-Layer.

## Volume auf einen vorhandenen Pfad mounten

Ein besonders wichtiger Test kann mit einem eigenen Test-Image durchgeführt werden. Das Test-Image enthält bereits eine Datei '/test/original.txt'. Der Inhalt der Datei lautete 'Ich komme aus dem Image'. Das wird zunächst ohne Volume überprüft:

```bash
docker run --rm mount-test-image cat /test/original.txt
```

Ausgabe:

Ich komme aus dem Image

Damit wird bestätigt, dass sich die Datei tatsächlich im Image befindet.

## Ein leeres Volume wird erstmals eingebunden

Anschließend wurde ein neues Docker Volume erstellt:

```bash
docker volume create mount-copy-test
```

Das Volume war zu diesem Zeitpunkt leer. Es wurde anschließend auf '/test' eingebunden:

```bash
docker run --rm \
  -v mount-copy-test:/test \
  mount-test-image \
  ls -l /test
```

Die Datei 'original.txt' war sichtbar.

Das allein würde noch nicht vollständig zeigen, ob die Datei weiterhin aus dem Image stammt oder bereits im Volume vorhanden ist.

Deshalb wurde ein zweiter Test durchgeführt.

## Nachweis, dass die Datei im Volume liegt

Für den zweiten Test wird nicht mehr das eigene Test-Image verwendet, sondern ein reines Alpine-Image:

```bash
docker run --rm \
  -v mount-copy-test:/test \
  alpine \
  ls -l /test
```

Es wird 'original.txt' angezeigt. Alpine selbst enthält diese Datei nicht. Damit wurde praktisch nachgewiesen, dass sich original.txt inzwischen im Docker Volume befindet.

Vereinfacht:

Test-Image
    │
    │ enthält
    ▼
/test/original.txt
    │
    │ erster Mount auf leeres Volume
    ▼
mount-copy-test
    │
    └── original.txt

Docker kann ein neues, leeres Volume beim ersten Mount auf ein Verzeichnis mit bereits vorhandenem Inhalt initial mit diesem Inhalt befüllen. Wichtig ist dabei, diese Initialisierung bedeutet nicht, dass bei jedem späteren Containerstart erneut aus dem Image kopiert wird. Ist das Volume bereits vorhanden und enthält Daten, bleibt dieser Inhalt bestehen.

## Bereits vorhandenes Volume

Das Verhalten lässt sich anschließend so darstellen:

Container A
    │
    │ mount-copy-test:/test
    ▼
mount-copy-test
    │
    └── original.txt

Wird Container A gelöscht:

Container A
     ↓
  gelöscht

mount-copy-test
        ↓
bleibt bestehen

Ein neuer Container kann dasselbe Volume wieder einbinden:

Container B
    │
    │ mount-copy-test:/test
    ▼
mount-copy-test
    │
    └── original.txt

Die Datei ist weiterhin vorhanden. Damit ist erneut der unterschiedliche Lebenszyklus von Container und persistentem Storage sichtbar.

## Mounts und das Sichtbare am Mountpoint

Ein Mount stellt den eingebundenen Speicher an einem bestimmten Pfad innerhalb des Containers bereit.

Beispiel:

Volume
mount-copy-test
      │
      ▼
Container:/test

Für Prozesse innerhalb des Containers ist '/test' damit der Ort, an dem der Inhalt des Volumes sichtbar ist. Das führt zu einem wichtigen mentalen Modell:

Container-Dateisystem

/app
    │
    └── Container-/Image-Dateisystem

/test
    │
    └── gemounteter Speicher

Der Mountpoint ist daher eine Art Übergang zwischen dem Dateisystem des Containers und einem extern bereitgestellten Speicherbereich.

## Container-Layer und Volume im direkten Vergleich

Container-Layer
Container
    │
    ▼
Container-Layer
    │
    └── datei.txt

Eigenschaften:

- beschreibbar
- gehört zum Container
- Änderungen verändern nicht das Image
- wird beim Löschen des Containers entfernt
- für flüchtige Laufzeitdaten geeignet

Docker Volume
Container
    │
    ▼
  /data
    │
    ▼
Docker Volume
    │
    └── taskmanager.db

Eigenschaften:

- außerhalb des Container-Layers
- eigener Lebenszyklus
- bleibt beim Löschen des Containers bestehen
- kann von einem neuen Container wieder eingebunden werden
- für persistente Daten geeignet

## Bind Mount und Volume

Auch die bereits zuvor untersuchten Bind Mounts lassen sich jetzt in das Gesamtmodell einordnen.

Bind Mount
Host-Dateisystem
/home/kath/.../taskmanager.db
            │
            ▼
       Bind Mount
            │
            ▼
Container:/data/taskmanager.db

Ein konkreter Host-Pfad wird verwendet.

Docker Volume
Docker Host
    │
    ▼
Docker verwalteter Storage
    │
    ▼
taskmanager-data
    │
    ▼
Container:/data

Beim Volume wird der Speicher von Docker verwaltet. Beide Varianten befinden sich außerhalb des eigentlichen Container-Layers und können daher Daten über den Lebenszyklus des Containers hinaus speichern.

## Security-Zusammenhang

Die Unterscheidung zwischen Container-Layer und Mounts ist auch unter Sicherheitsgesichtspunkten relevant. Beim Taskmanager wurde bewusst zwischen Anwendungscode und veränderlichen Daten getrennt:

/app
    │
    ├── app.py
    ├── templates/
    └── static/

        Anwendungscode

/data
    │
    └── taskmanager.db

        veränderliche Daten

Die Anwendung benötigt Schreibrechte auf '/data', aber nicht grundsätzlich auf den gesamten Anwendungscode. Zusammen mit dem Non-Root-Benutzer 'appuser UID 1000 GID 1000' unterstützt diese Trennung das Prinzip Least Privilege. Damit ist die Wahl eines Mounts nicht ausschließlich eine Frage der Persistenz. Auch die Frage, welche Anwendung darf welchen Speicher verändern, ist Teil der technischen und sicherheitsbezogenen Betrachtung.

## Wichtige Erkenntnisse

Durch die praktischen Tests wurde das bisherige Dateisystemmodell weiter vervollständigt.

                  Image-Layer
                  Image
                    ↓
        unveränderliche Grundlage
                    ↓
kann für mehrere Container verwendet werden

        Container-Layer
        Container
            ↓
    beschreibbarer Layer
            ↓
Änderungen während der Laufzeit
            ↓
        flüchtig

    Mount
    externer Storage
            ↓
          Mount
            ↓
Pfad innerhalb des Containers

Volume
Docker verwalteter Storage
            ↓
unabhängiger Lebenszyklus
            ↓
     persistente Daten

Das Gesamtmodell lautet damit:

             Image
               │
      ┌────────┴────────┐
      ▼                 ▼
Container A       Container B
      │                 │
Container-Layer   Container-Layer
      │                 │
      └───────┐ ┌───────┘
              │ │
              ▼ ▼
             Mount
               │
               ▼
         Docker Volume
               │
               ▼
        persistente Daten

Nicht jeder Container benötigt einen Mount. Wenn Daten jedoch den Lebenszyklus des Containers überleben müssen, wird ein geeigneter persistenter Speicher benötigt.

## Bezug zum Taskmanager

Der Taskmanager verwendet inzwischen das folgende Modell:

            Browser
               │
               ▼
           Host:3001
               │
          Port Mapping
               │
               ▼
     Taskmanager-Container
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
    /app              /data
      │                 │
      │                 ▼
      │          taskmanager-data
      │                 │
      │                 ▼
      │          taskmanager.db
      │
      ▼
Anwendungscode

Der Anwendungscode befindet sich im Image beziehungsweise Container-Dateisystem. Die Datenbank befindet sich dagegen im persistenten Docker Volume. Dadurch können Container ersetzt werden, ohne dass die Datenbank verloren geht. Das wurde bereits praktisch überprüft:

Taskmanager-Container A
        │
        │ erstellt Aufgabe
        ▼
taskmanager-data
        │
        │ Container gelöscht
        ▼
taskmanager-data bleibt erhalten
        │
        ▼
Taskmanager-Container B
        │
        ▼
Aufgabe weiterhin vorhanden

## Fazit

Dieser Lernschritt hat das Verständnis des Container-Dateisystems von einzelnen Docker-Konzepten zu einem zusammenhängenden Modell erweitert.

- Ein Docker Image stellt die unveränderliche Grundlage bereit.
- Ein Container erhält zusätzlich einen eigenen beschreibbaren Container-Layer. Dieser 
  Layer gehört zum Lebenszyklus des Containers und ist deshalb für dauerhafte Daten ungeeignet.
- Mounts ermöglichen es dagegen, externen Speicher innerhalb des Containers 
- bereitzustellen.
- Bei einem Docker Volume verwaltet Docker den Speicher und dessen Einbindung. 
- Das Volume besitzt einen vom Container unabhängigen Lebenszyklus.

Eine wichtige Besonderheit wurde ebenfalls praktisch nachgewiesen:

- Wird ein neues, leeres Volume erstmals auf ein Verzeichnis mit vorhandenen Dateien 
  eingebunden, kann Docker den vorhandenen Inhalt des Image-Verzeichnisses zur Initialisierung des Volumes verwenden.
- Anschließend liegt die Datei im Volume und bleibt dort unabhängig vom verwendeten 
  Container erhalten.

Damit lässt sich der zentrale Zusammenhang zusammenfassen:

          Image
            ↓
unveränderliche Grundlage

    Container-Layer
          ↓
flüchtige Änderungen

            Mount
              ↓
Verbindung zu externem Storage

     Volume
        ↓
persistente Daten

Das Verständnis dieser Ebenen bildet die Grundlage für die nächsten Docker-Themen. Insbesondere beim späteren Einsatz mehrerer Container wird wichtig, dass Anwendungscode, temporäre Laufzeitdaten und persistente Daten unterschiedliche Lebenszyklen besitzen können.
Der nächste größere Lernschritt ist Docker Compose. 