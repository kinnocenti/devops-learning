# Container-Dateisystem, Image-Layer und Copy-on-Write

Nachdem die Unterschiede zwischen Bind Mounts und Docker Volumes praktisch untersucht wurden, wird im nächsten Schritt betrachtet, wie das Dateisystem eines Containers grundsätzlich aufgebaut ist. Dabei wird insbesondere der Zusammenhang zwischen Image-Layern, dem beschreibbaren Container-Layer und persistentem Storage betrachtet.

Das bisherige Modell:

Dockerfile
    ↓
  Image
    ↓
 Container

wird dadurch erweitert:

Docker Image
    │
    ├── Image-Layer
    │
    ▼
beschreibbarer Container-Layer
    │
    ├── /app
    │
    └── /data → Docker Volume

Damit lässt sich besser verstehen, warum Änderungen innerhalb eines Containers möglich sind, obwohl die zugrunde liegenden Image-Layer unveränderlich bleiben.

## Image-Layer

Ein Docker Image besteht aus mehreren Layern. Diese entstehen unter anderem durch die Anweisungen im Dockerfile und enthalten die für die Anwendung benötigten Dateien und Bestandteile der Laufzeitumgebung.

Beim Taskmanager wird beispielsweise mit ```bash FROM python:3.12-slim-trixie ``` ein bestehendes Base Image verwendet. Weitere Anweisungen des Dockerfiles fügen anschließend benötigte Dateien und Abhängigkeiten hinzu.

Vereinfacht kann das Image als mehrere Ebenen betrachtet werden:

Image
├── grundlegende Linux-Dateien
├── Python-Laufzeitumgebung
├── installierte Python-Abhängigkeiten
└── Taskmanager-Anwendung
      ├── app.py
      ├── templates/
      └── static/

Die Image-Layer sind nach ihrer Erstellung grundsätzlich unveränderlich. Ein laufender Container verändert nicht direkt das Image. Das ist wichtig, weil mehrere Container aus demselben Image erstellt werden können, ohne dass Änderungen eines Containers das gemeinsame Image verändern.

## Beschreibbarer Container-Layer

Beim Erstellen eines Containers aus einem Image kommt zusätzlich eine beschreibbare Ebene hinzu.

Vereinfacht:

Container
┌────────────────────────────┐
│ beschreibbarer Layer       │
├────────────────────────────┤
│ Image-Layer                │
├────────────────────────────┤
│ Image-Layer                │
├────────────────────────────┤
│ Image-Layer                │
└────────────────────────────┘

Die Image-Layer stellen den unveränderlichen Ausgangszustand bereit. Der beschreibbare Container-Layer ermöglicht es dem laufenden Container, Dateien zu erzeugen, zu verändern oder zu löschen. 
Dieser Layer ist jedoch an den Lebenszyklus des Containers gebunden. Wird der Container gelöscht, wird auch sein beschreibbarer Container-Layer gelöscht. Das bedeutet nicht, dass ein beschreibbarer Container-Layer grundsätzlich unnötig ist. Eine Anwendung muss während ihrer Laufzeit Dateien verändern oder temporäre Daten erzeugen können. Nicht alle Daten müssen dauerhaft gespeichert werden.
Beispielsweise können temporäre Dateien oder Zwischenergebnisse während der Verarbeitung im Container-Layer abgelegt werden.

Vereinfacht gilt daher:

Flüchtige Daten
       ↓
Container-Layer

und:

    Persistente Daten
            ↓
Docker Volume / Bind Mount

Der Container-Layer ermöglicht somit die normale Laufzeit der Anwendung, während ein Volume oder Bind-Mount für Daten verwendet wird, die den Lebenszyklus des Containers überleben sollen.

## Copy-on-Write

Für die Zusammenarbeit zwischen Image-Layern und dem beschreibbaren Container-Layer wird unter Linux bei typischen Docker-Konfigurationen ein Overlay-Dateisystem verwendet. Ein wichtiges Prinzip dabei ist Copy-on-Write, kurz CoW.
Die Grundidee besteht darin, dass vorhandene Dateien aus den Image-Layern zunächst gelesen werden können, ohne dass der unveränderliche Image-Layer verändert werden muss. Wird eine solche Datei innerhalb des Containers verändert, wird die Änderung in der beschreibbaren Ebene des Containers abgebildet. Der Image-Layer bleibt dabei unverändert.

Vereinfacht:

Image-Layer
└── /etc/example.conf
        │
        │ Lesen
        ▼
Container sieht die Datei

Änderung durch den Container
        │
        ▼
beschreibbarer Container-Layer
└── /etc/example.conf
        │
        ▼
Container sieht die geänderte Version

Das Image selbst bleibt weiterhin unverändert.

Dieses Verhalten kann praktisch mit einem Alpine-Container untersucht werden. Dafür wird mit dem folgenden Befehl ein Alpine-Container erstellt:

```bash
docker run -it --name cow-test alpine sh
```

Befehlserklärung:

'-it' → sorgt dafür, dass diese Shell interaktiv bleibt und Sie Befehle direkt 
         eintippen können
'sh'  → startet die Standard-Kommandozeile (Shell) innerhalb des 
         Alpine-Linux-Containers

Damit können Befehle eingegeben werden. Zunächst wird eine Datei aus dem Image gelesen:

```bash
cat /etc/alpine-release
```

Ausgabe:

3.24.2

Anschließend wird der Inhalt innerhalb des Containers verändert:

```bash
echo "Meine Änderung" > /etc/alpine-release
```

Die Änderung kann dann mit folgenden Befehl angezeigt werden: 

```
bash cat /etc/alpine-release
```

Ausgabe:

Meine Änderung

Danach liefert die Datei innerhalb dieses Containers den geänderten Inhalt. Das Alpine-Image selbst wird dadurch jedoch nicht verändert.
Nach dem Löschen des Containers wird ein neuer Container aus demselben Image gestartet:

```bash
docker run --rm alpine cat /etc/alpine-release
```

Der neue Container zeigte wieder den ursprünglichen Inhalt der Datei '3.24.2'.

Damit wurde praktisch bestätigt:

Image
└── ursprüngliche Datei
        │
        ├── Container A
        │      └── Änderung im Container-Layer
        │
        └── Container B
               └── unveränderte Datei aus dem Image

Die Änderung von Container A wird somit nicht in das Image zurückgeschrieben. Deshalb beeinflussen sich Container nicht gegenseitig bei Änderungen im Container-Layer und mehrere Container können dasselbe Image als gemeinsame Grundlage verwenden.

Vereinfacht:

                 Image
              /         \
             ▼           ▼
      Container A   Container B
           │             │
      eigener Layer   eigener Layer

Wenn Container A eine Datei verändert, wird die Änderung in seinem eigenen beschreibbaren Bereich gespeichert. Container B verwendet weiterhin seine eigene Dateisystemsicht.

Beispielsweise:

Image
└── /etc/example.conf
       "Original"

Container A
└── eigener Container-Layer
       "Änderung A"

Container B
└── eigener Container-Layer
       "Änderung B"

Container A und Container B können damit unabhängig voneinander Änderungen an derselben Datei vornehmen. Das Image bleibt unverändert. Diese Isolation der beschreibbaren Container-Layer ist ein wichtiger Unterschied zu einem gemeinsam eingebundenen persistenten Speicher.

## Abgrenzung zu Docker Volumes

Beim Taskmanager wird die Datenbank nicht im normalen Container-Layer gespeichert.

Die Anwendung verwendet '/data/taskmanager.db' und unter '/data' ist das Docker Volume 'taskmanager-data' eingebunden.

Damit entsteht ein anderes Modell:

  Container A
       │
       ▼
     /data
       │
       ▼
taskmanager-data
       ▲
       │
     /data
       ▲
       |
  Container B

Wenn mehrere Container dasselbe Volume einbinden, greifen sie auf denselben persistenten Speicherbereich zu.

Damit gilt:

    Container-Layer
           ↓
pro Container getrennt
           ↓
        flüchtig

                 Docker Volume
                       ↓
kann von mehreren Containern eingebunden werden
                       ↓
                   persistent

Beim Taskmanager sorgt das Volume dafür, dass die SQLite-Datenbank unabhängig vom Lebenszyklus des Containers erhalten bleibt.

## Container-Layer und Docker Volume im Taskmanager

Für den aktuellen Taskmanager ergibt sich damit folgendes Gesamtmodell:

            Taskmanager-Container
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
    /app                          /data
      │                             │
      ▼                             ▼
Anwendungscode                 Docker Volume
      │                      taskmanager-data
      │                             │
      ▼                             ▼
 app.py usw.                  taskmanager.db

Die Anwendung selbst wird über das Image bereitgestellt. Veränderliche und persistente Daten werden dagegen über den separaten Datenbereich '/data' bereitgestellt. Dadurch werden Anwendungscode und Anwendungsdaten sowohl technisch als auch unter Sicherheitsgesichtspunkten voneinander getrennt.

## Zusammenhang mit Dateirechten und Least Privilege

Die Trennung von '/app' und '/data' unterstützt außerdem das bereits eingeführte Prinzip Least Privilege.
Die Anwendung muss ihren eigenen Programmcode normalerweise nicht verändern. Für den Taskmanager ist deshalb folgende Aufteilung sinnvoll:

/app
    Anwendungscode
    möglichst nur lesbar

/data
    SQLite-Datenbank
    notwendigerweise beschreibbar

Der Prozess 'appuser' benötigt damit Schreibrechte auf den Datenbereich, aber nicht auf den gesamten Anwendungscode. Dies entspricht dem bereits praktisch untersuchten Prinzip. Ein Prozess soll nur die Berechtigungen besitzen, die er für seine Aufgabe tatsächlich benötigt.
Die Trennung von Anwendungscode und veränderlichen Daten ist daher nicht nur eine Frage der Persistenz, sondern unterstützt gleichzeitig eine sauberere Sicherheitsstruktur.

## Temporäre Dateien und der Container-Layer

Der beschreibbare Container-Layer ist nicht ausschließlich für Änderungen an bestehenden Dateien vorgesehen. Anwendungen können dort auch temporäre Dateien erzeugen. Ein typischer Linux-Speicherort für temporäre Dateien ist z.B. '/tmp'. Eine dort erzeugte Datei kann während der Laufzeit eines Containers verwendet werden, ohne dass sie dauerhaft erhalten bleiben muss.
Wird der Container gelöscht, verschwinden solche Daten zusammen mit dem Container-Layer. Dies ist beispielsweise für temporäre Verarbeitungsschritte sinnvoll. Für Daten, die nach einem Container-Neustart oder einer Neuerstellung weiterhin benötigt werden, ist dagegen ein persistenter Speicher wie ein Docker Volume erforderlich.

## Ergebnis

Durch die Untersuchung des Container-Dateisystems wurde das bisherige Verständnis von Images, Containern und persistentem Storage erweitert.

Dabei wurden folgende Zusammenhänge praktisch und theoretisch nachvollzogen:

- Ein Docker Image besteht aus mehreren Layern.
- Image-Layer sind grundsätzlich unveränderlich.
- Ein Container erhält zusätzlich eine beschreibbare Ebene.
- Änderungen innerhalb eines Containers verändern nicht das zugrunde liegende Image.
- Copy-on-Write ermöglicht Änderungen an Dateien aus den Image-Layern, ohne diese 
  Image-Layer selbst zu verändern.
- Der beschreibbare Container-Layer gehört zum Lebenszyklus des Containers.
- Wird der Container gelöscht, wird auch sein beschreibbarer Layer entfernt.
- Mehrere Container können dasselbe Image verwenden und besitzen trotzdem voneinander 
  getrennte beschreibbare Layer.
- Ein Docker Volume befindet sich außerhalb des normalen Container-Layers und besitzt 
  einen eigenen Lebenszyklus.
- Mehrere Container können dasselbe Volume einbinden und dadurch auf gemeinsame 
  persistente Daten zugreifen.
- Im Taskmanager werden Anwendungscode und persistente Daten bewusst über '/app' und 
  '/data' getrennt.
- Diese Trennung unterstützt sowohl Persistenz als auch das Prinzip Least Privilege.

Damit ergibt sich für den Taskmanager folgendes vereinfachtes Modell:

Docker Image
     │
     ▼
 Container
     │
     ├── Container-Layer
     │      └── flüchtige Änderungen
     │
     ├── /app
     │      └── Anwendungscode aus dem Image
     │
     └── /data
            │
            ▼
      Docker Volume
      taskmanager-data
            │
            ▼
      taskmanager.db

Der nächste Lernschritt kann damit auf einem erweiterten Verständnis des Container-Dateisystems aufbauen. Anschließend können die bisher einzeln untersuchten Komponenten – Container, Netzwerk, Storage und mehrere Dienste – mit Docker Compose zu einer gemeinsamen Anwendungskonfiguration zusammengeführt werden.