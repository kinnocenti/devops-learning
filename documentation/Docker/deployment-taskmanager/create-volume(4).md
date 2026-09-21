# Vom Bind Mount zum Docker Volume

Ausgangssituation

Unser Taskmanager verwendet aktuell einen Bind Mount, um die SQLite-Datenbank persistent außerhalb des Containers zu speichern.
Aktueller Bind Mount

    Aufbau

    Source

    Destination

    RW

    docker inspect

    konkrete Abhängigkeit vom Host-Pfad

Warum Docker Volumes?

    Docker verwaltet den Speicher

    Anwendung muss keinen konkreten Host-Pfad kennen

    Container und Storage werden stärker voneinander entkoppelt

    trotzdem bleibt der Speicher bei einem lokalen Volume auf dem Docker Host

    Linux-Dateirechte verschwinden nicht automatisch

Erstellen eines Docker Volumes

docker volume create taskmanager-data
docker volume ls

Untersuchung des Volumes

docker volume inspect taskmanager-data

mit Erklärung von:

    CreatedAt

    Driver

    Mountpoint

    Name

    Options

    Scope

Einbindung in einen Container

docker run --name volume-test \
  -v taskmanager-data:/data \
  alpine

inklusive Erklärung des Unterschieds zwischen:

-v /host/pfad:/container/pfad

und

-v volume-name:/container/pfad

Persistenztest

Erzeugen:

docker run --rm \
  -v taskmanager-data:/data \
  alpine \
  sh -c 'echo "Hallo Volume!" > /data/test.txt'

Auslesen:

docker run --rm \
  -v taskmanager-data:/data \
  alpine \
  cat /data/test.txt

Ergebnis:

Hallo Volume!

Praktischer Nachweis des unterschiedlichen Lebenszyklus

Container wird gelöscht → Volume bleibt → neuer Container kann dieselben Daten lesen.
Bind Mount vs. Docker Volume

Eine ausführliche Gegenüberstellung.
Storage vs. Netzwerk

Besonders wichtig:

Reverse Proxy
    ↓
Netzwerk
    ↓
Anwendung

ist unabhängig von:

Anwendung
    ↓
Volume
    ↓
Storage

Ergebnis

Was wir praktisch nachgewiesen haben und was sich daraus für das spätere Deployment ergibt.