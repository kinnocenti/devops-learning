# Vom Bind Mount zum Docker Volume

Der Taskmanager verwendet aktuell einen Bind-Mount, um die SQLite-Datenbank persistent außerhalb des Containers zu speichern. Dieser ist für den ersten lokalen Taskmanager sehr transparent und praktisch. Für einen späteren Deployment-Ansatz kann ein Docker Volume jedoch Vorteile bei der Verwaltung persistenter Daten bieten.

## Warum Bind-Mount

Für eine Webanwendung in einem Docker-Container sind Volumes meist die bessere Wahl als Bind Mounts, da sie vollständig von Docker verwaltet werden, sicherer sind und eine deutlich höhere Performance auf Nicht-Linux-Systemen (wie macOS oder Windows) bieten.Während Bind Mounts direkt von der Ordnerstruktur des Host-Betriebssystems abhängen, sind Volumes isoliert und speziell für die Anforderungen von Containern optimiert.

Also:

- Docker verwaltet den Speicher
- Anwendung muss keinen konkreten Host-Pfad kennen
- Container und Storage werden stärker voneinander entkoppelt
- trotzdem bleibt der Speicher bei einem lokalen Volume auf dem Docker Host
- Linux-Dateirechte verschwinden nicht automatisch

## Vergleich von Bind-Mount und Volume

Bind Mount                        |  Docker Volume
------------------------------------------------------------------------------------
konkreter Host-Pfad               |  Volume-Name
/<Pfad>/taskmanager.db            |  taskmanager-data
Host-Pfad wird direkt angegeben   |  Docker verwaltet den Speicherort
sehr transparent                  |  weniger abhängig von einem konkreten Host-Pfad
Host-Dateirechte direkt relevant	|  ebenfalls Berechtigungen relevant
gut für Entwicklung/              |  gut für Docker-verwalteten persistenten Storage
gezielten Host-Dateizugriff       |  

## Erstellen eines Docker Volumes

Damit das Volume verwendet werden kann, muss es zunächst erstellt werden mit dem folgenden Befehl:

```bash
docker volume create taskmanager-data
```

Mit dem nächsten Befehl kann überprüft werden, ob das Volume angelegt wurde:

```bash
docker volume ls
```

Ausgabe:

DRIVER    VOLUME NAME
local     taskmanager-data

Weitere Untersuchung des Volumes ist mit 'docker volume inspect' möglich:

```bash
docker volume inspect taskmanager-data
```

Ausgabe:

[
    {
        "CreatedAt": "2026-09-21T17:58:37+02:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/taskmanager-data/_data",
        "Name": "taskmanager-data",
        "Options": null,
        "Scope": "local"
    }
]

Das erstellte Docker-Volume 'taskmanager-data' verwendet den lokalen Volume-Treiber (local). Die Daten werden unter dem Mountpoint '/var/lib/docker/volumes/taskmanager-data/_data' auf dem Host gespeichert. Das Volume besitzt keine zusätzlichen Optionen oder Labels und ist nur auf dem lokalen Docker-System verfügbar (Scope: local).

## Einbindung in einen Container

Im folgenden Beispiel wird das Image 'alpine' (leichtgewichtig und sehr gut geeignet für Tests) verwendet. Der damit erzeugte Container soll im weiteren nur die Persistenz der Daten des Volumes darlegen und die Syntax des 'docker run'-Befehls aufzeigen. Dafür wird mit dem folgenden Befehl ein Testcontainer gestartet:

```bash
docker run --name volume-test \
  -v taskmanager-data:/data \   # nicht Host-Pfad, sondern Volume-Name wird verwendet 
  alpine
```

Damit ist das Volume 'taskmanager-data' in den Container eingebunden.

## Persistenztest

Mit dem folgenden Befehl wird die Datei 'test.txt' im Volume erstellt und 'Hallo Voume!' in 'test.txt' geschrieben.  

```bash
docker run --rm \
  -v taskmanager-data:/data \
  alpine \
  sh -c 'echo "Hallo Volume!" > /data/test.txt'
```

Auslesen wird die Datei 'test.txt' dann mit:

```bash
docker run --rm \
  -v taskmanager-data:/data \
  alpine \
  cat /data/test.txt
```

Ausgabe:

Hallo Volume!

Damit wurde praktisch der unterschiedliche Lebenszyklus der Container nachgewiesen und zugleich die Persitenz der Daten im Volume. Container wird gelöscht → Volume bleibt → neuer Container kann dieselben Daten lesen.