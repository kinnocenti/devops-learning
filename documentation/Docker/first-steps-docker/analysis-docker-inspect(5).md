# Untersuchung eines Docker-Containers mit docker inspect

Hier wird vertieft auf die Ausgabe von ```bash docker inspect webserver``` eingegangen. Es macht Sinn die Ausgabe des laufenden Containers mit der Ausgabe des gestoppten Containers zu vergleichen, so wird deutlich welche Änderungen und Einträge umgesetzt wurden.

## Zu Beginn

Um den Aufbau und den Zustand eines Docker-Containers besser zu verstehen, wird zunächst ein Nginx-Container erstellt:

```bash
docker run -d --name webserver -p 3000:80 nginx
```

Anschließend wird der Container mit ```bash docker inspect webserver ``` untersucht. 'docker inspect' liefert eine umfangreiche JSON-Ausgabe mit Informationen über den Container. Für die Untersuchung wurden insbesondere Image, Config, State, NetworkSettings, HostConfig, Storage und Mounts betrachtet.

## Image

Im Bereich Image befindet sich beispielsweise:

"Image": "sha256:5188c0c45479443d7be2eadc894b4ed0a9801baa03d97a5760ae13b5ce005932"

Der Wert ist ein SHA-256-Digest und dient zur eindeutigen Identifizierung des konkreten Image-Inhalts. Der Digest ermöglicht unter anderem die Überprüfung der Integrität eines Images. Bei SHA-256 handelt es sich um einen Hashwert (kurz Hash). Dies ist der digitale „Fingerabdruck“ einer Datei, eines Textes oder von Daten, der durch eine mathematische Funktion (Hashfunktion) erzeugt wird.

## Config

Config enthält Konfigurationsinformationen des Containers. Beispielsweise besitzt der Container einen eigenen Hostnamen: '"Hostname": "2d153fa6f2f4"'

Außerdem ist Port 80/TCP als vorgesehener Container-Port angegeben:

```bash
"ExposedPorts": {
    "80/tcp": {}
}
```

Hier muss zwischen einem exponierten Port und einer Portweiterleitung unterschieden werden. Der Container wurde mit '-p 3000:80' gestartet. Dadurch wird Port 3000 des Docker-Hosts auf Port 80 des Containers weitergeleitet:

Host
Port 3000
    ↓
Container
Port 80
    ↓
Nginx

ExposedPorts beschreibt den vorgesehenen Container-Port. Die Option '-p' richtet dagegen die tatsächliche Portweiterleitung zwischen Host und Container ein.

In Config sind außerdem Entrypoint und Cmd zu finden:

```bash
"Entrypoint": [
    "/docker-entrypoint.sh"
],
"Cmd": [
    "nginx",
    "-g",
    "daemon off;"
]
```

Damit lässt sich nachvollziehen, was beim Start des Containers ausgeführt wird (Startprozess).

Vereinfacht:

ENTRYPOINT
/docker-entrypoint.sh
       +
      CMD
nginx -g "daemon off;"
       ↓
Nginx-Prozess

'daemon off;' sorgt dafür, dass Nginx im Vordergrund läuft. Dies ist für einen Container wichtig, da der laufende Hauptprozess den Container am Leben hält.

## State

Der Bereich State beschreibt den aktuellen Zustand des Containers. 

Nach dem Stoppen des Containers ist zu sehen:

```bash
"Status": "exited",
"Running": false
```

Nach einem erneuten Start:

```bash
"Status": "running",
"Running": true
```

Auch StartedAt wurde beim erneuten Start aktualisiert. Damit wird praktisch nachvollzogen, dass 'docker inspect' unter anderem den aktuellen Zustand des Containers beschreibt und sich diese Informationen entsprechend verändern. Weitere Werte wie Pid, ExitCode und Error geben zusätzliche Informationen über den Zustand bzw. den Prozess des Containers.

Im Beispiel war ```bash "ExitCode": 0 ``` vorhanden. Der Prozess wurde somit ohne Fehlercode beendet.

## HostConfig und Portweiterleitung:

Unter HostConfig ist die beim Erstellen des Containers konfigurierte Portweiterleitung zu erkennen:

```bash
"PortBindings": {
    "80/tcp": [
        {
            "HostPort": "3000"
        }
    ]
}
```

Damit ist nachvollziehbar, dass die beim Start angegebene Option '-p 3000:80' als Konfiguration des Containers hinterlegt wurde. HostConfig beschreibt dabei unter anderem Einstellungen, mit denen der Container gestartet bzw. konfiguriert wurde.

## NetworkSettings

NetworkSettings enthält Informationen über die aktuelle Netzwerkanbindung. Der Container ist dem Docker-Netzwerk bridge zugeordnet.

Beim laufenden Container sind unter anderem folgende Werte vorhanden:

```bash
"Gateway": "172.17.0.1",
"IPAddress": "172.17.0.2",
"MacAddress": "f6:13:4a:5f:ce:65"
```

Der Container besitzt damit innerhalb des Docker-Netzwerks eine eigene IP-Adresse.

Vereinfacht:

Docker-Host
    │
    └── Docker bridge
          │
          └── Container
              IP: 172.17.0.2

Bei einem gestoppten Container sind die Werte für EndpointID, Gateway, IPAddress und weitere aktuelle Netzwerkparameter dagegen leer. Beim Start des Containers wird die aktive Netzwerkumgebung wieder eingerichtet. Dadurch werden die entsprechenden Werte in NetworkSettings wieder angezeigt.

Ausgehend vom Host erfolgt der Zugriff auf Nginx über:

localhost:3000

Die Portweiterleitung führt anschließend zum Port 80 des Containers:

Client / Browser / curl
        │
        │ localhost:3000
        ▼
   Docker-Host
        │
        │ Portweiterleitung
        ▼
    Container
  172.17.0.2:80
        │
        ▼
      Nginx

## Mounts und Container-Dateisystem

Der Bereich Mounts enthielt ```bash "Mounts": [] ```. Das bedeutet, dass für den Container keine zusätzlichen Docker-Mounts konfiguriert wurden. Dies bedeutet nicht, dass der Container kein Dateisystem besitzt. Der Container verfügt weiterhin über die Dateien und Verzeichnisse, die aus seinem Image stammen.
Ein zusätzlicher Mount stellt dagegen beispielsweise eine Verbindung zwischen einem Host-Verzeichnis bzw. einem Docker-Volume und einem Verzeichnis innerhalb des Containers her.

Der untersuchte Container verwendete als Storage-Treiber ```bash "Driver": "overlayfs" ```. Damit wird das Dateisystem des Containers auf Basis der Image-Layer bereitgestellt. Die Unterscheidung zwischen dem normalen Container-Dateisystem und zusätzlichen Mounts wird später bei der Betrachtung von Volumes und Persistenz wichtig.

## RestartPolicy

Unter HostConfig war außerdem zu sehen:

"RestartPolicy": {
    "Name": "no"
}

Damit war für den Container keine automatische Neustartstrategie konfiguriert. Der Container bleibt nach seinem Ende beendet, solange er nicht manuell erneut gestartet wird.

## Container-Runtime und Linux-Mechanismen

Weitere interessante Einstellungen sind ```bash "Runtime": "runc" ```, ```bash "AppArmorProfile": "docker-default" ``` und ```bash "CgroupnsMode": "private" ```. Damit wird sichtbar, dass Docker für die Ausführung und Isolation von Containern verschiedene Linux-Mechanismen nutzt. 'runc' ist die Container-Runtime, die den Containerprozess entsprechend der Docker-Konfiguration startet.
Dies zeigt bereits einen wichtigen Zusammenhang, die Isolation eines Containers ist keine vollständig eigene Technologie von Docker. Docker nutzt dafür vorhandene Funktionen des Linux-Systems.

## Gesamtbild

Durch die Untersuchung mit 'docker inspect' kann ein Container als Zusammenspiel verschiedener Komponenten betrachtet werden:

             Docker Engine
                  │
                  ▼
              Container
    ┌─────────────┼─────────────┐
    │             │             │
 Config         State        Network
    │             │             │
    │             │             ├── IP
    │             │             ├── Gateway
    │             │             └── Netzwerk
    │             │
    │             └── Prozesszustand
    │
    ├── Image
    ├── Entrypoint
    ├── Cmd
    └── weitere Konfiguration
                  │
                  ▼
             Container-Prozess
                  │
                  ▼
                Nginx

Damit ergibt sich folgendes Gesamtbild:

                         Docker Engine
                              │
               ┌──────────────┴──────────────┐
               │                             │
         Container-Konfiguration        Laufzeitumgebung
               │                             │
       ┌───────┼────────┐             ┌───────┼────────┐
       │       │        │             │       │        │
    Image   Config   PortBinding    State  Network  Storage
       │                │             │       │
       │                │             │       │
       ▼                ▼             ▼       ▼
    nginx          3000 → 80       running  172.17.0.2
       │
       ▼
 /docker-entrypoint.sh
       │
       ▼
 nginx -g "daemon off;"

Der Container ist somit nicht lediglich „ein Programm in einer Box“. Die Docker Engine stellt zusätzlich eine konfigurierte Laufzeitumgebung bereit, zu der unter anderem Prozess-, Netzwerk-, Speicher- und Sicherheitsaspekte gehören.

## Übergang zum eigenen Taskmanager-Container

Der Nginx-Container wurde als fertiges Beispiel untersucht. Als nächster Schritt soll der bereits vorhandene Taskmanager selbst containerisiert werden. Dafür muss zunächst ermittelt werden, welche Bestandteile die Anwendung benötigt:

Taskmanager
├── Python / Flask
├── app.py
├── Templates
├── statische Dateien / CSS
├── benötigte Python-Abhängigkeiten
└── SQLite-Datenbank

Dabei ist zwischen Anwendungsdateien und persistenten Daten zu unterscheiden. Die Anwendungsdateien werden Bestandteil des Docker-Images. Die Frage, wie die SQLite-Datenbank dauerhaft erhalten bleibt, wird später beim Thema Volumes und Persistenz behandelt. Für den Bau des eigenen Images wird eine Dockerfile verwendet.

Der grundlegende Zusammenhang lautet:

Dockerfile
    │
    │ docker build
    ▼
Docker Image
    │
    │ docker run
    ▼
Container
    │
    ▼
Taskmanager

Damit wechselt der Lernschritt von der Untersuchung eines fertigen Containers zum eigenständigen Erstellen eines Containers für die eigene Anwendung.