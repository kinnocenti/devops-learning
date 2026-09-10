# Erste Schritte mit Docker

Nachdem die Webanwendung fertig gestellt wurde beginnt nun der Lernabschnitt Docker. Zunächst werden erste Schritte mit Docker gemacht. Dabei werden auch immer wieder Erklärungen in die Dokumentation mit einfließen, damit ein Gesamtverständnis für Docker entsteht.

## Was kommt jetzt?

Damit Docker im bisherigen Ablauf eingeordnet werden kann. Hier eine kurze Einordnung:

Bisher:

     Browser
        ↓
HTML / CSS / Jinja
        ↓
  Flask / Python
        ↓
      SQLite

Jetzt kommt eine weitere Ebene dazu:

    Browser
       ↓
 Flask-Anwendung
       ↓
    SQLite
       ↓
----------------
Docker Container
----------------
       ↓
  Docker Engine
       ↓
  Linux-System

Was passiert bei der Eingabe eines Docker-Befehls?

              docker-Befehl
                    ↓
              Docker Client
                    ↓
               Docker API
                    ↓
           Docker Engine / Daemon
                    ↓
Container / Images / Netzwerke / Volumes ...

## Erste Docker-Befehle

Zunächst wird der aktuelle Stand von Docker abgefragt und die wichtigsten Infos abgerufen.

docker --version → die aktuelle Version von Docker wird abgefragt

docker info      → zeigt eine systemweite Übersicht über den aktuellen Zustand und die
                   Konfigurationen der lokalen Docker-Umgebung 

docker image ls  → listet alle auf dem lokalen System vorhandenen Docker-Images auf

docker ps        → zeigt alle auf dem lokalen System laufenden Container an

docker ps -a     → zeigt alle auf dem System befindlichen Container an

Dabei stellt sich die Frage, was eigentlich bei der Eingabe eines Docker-Befehls passiert. Wenn ein Docker-Befehl eingegeben wird, ist nicht das Terminal selbst der Containerverwalter, sondern wenn ein Docker-Befehl ausgeführt wird, durchläuft dieser mehrere Komponenten:

Docker-Befehl
Es wird z.B. 'docker ps' in der Kommandozeile eingegeben.

Docker Client
Der Docker Client nimmt den eingegebenen Befehl entgegen und übersetzt ihn in eine Anfrage an die Docker API.

Docker API
Über die Docker API wird die Anfrage an die Docker Engine weitergeleitet. Sie dient als Schnittstelle zwischen Client und Docker Engine.

Docker Engine / Daemon
Der Docker Daemon empfängt die Anfrage und führt die gewünschte Aktion aus. Er verwaltet dabei unter anderem Container, Images, Netzwerke und Volumes.

Docker-Ressourcen
Abhängig vom Befehl werden die entsprechenden Docker-Ressourcen erstellt, gestartet, verändert oder abgefragt – beispielsweise Container, Images, Netzwerke oder Volumes.

Kurz gesagt:

Der Docker Client stellt die Anfrage, die Docker API übermittelt sie an die Docker Engine und der Docker Daemon führt die gewünschte Aktion auf den entsprechenden Docker-Ressourcen aus.

Ablauf:

              Docker-Befehl
                    ↓
              Docker Client
                    ↓
                Docker API
                    ↓
           Docker Engine / Daemon
                    ↓
Container / Images / Netzwerke / Volumes ...

## Ersten Container starten

Der erste Container wird mit dem Image Nginx gestartet. Nginx ist ein Webserver, der auch als Reverse-Proxy und Load-Balancer genutzt werden kann. Im weiteren Verlauf sollen nicht einfach nur Befehle eingegeben werden, sondern verstanden werden was abläuft. Mit dem Befehl ```bash docker run <image> ``` wird ein Container aus dem angegebenen Image erstellt und gestartet.

Folgenden Befehl eingeben:

```bash
docker run nginx
```

Hinweis: Das Image muss nicht zuvor mit 'pull' heruntergeladen werden, weil es mit dem run-Befehl automatisch heruntergeladen wird, wenn nicht vorhanden.

Ablauf:

  Image
    ↓
docker run
    ↓
 Container
    ↓
 Prozess
    ↓
  Nginx

Das Terminal wird danach vermutlich nicht wieder zur Eingabeaufforderung zurückkehren. Wenn alles funktioniert, läuft Nginx im Vordergrund und Docker zeigt möglicherweise Log-Ausgaben.

Wenn jetzt im Browser ```bash http://localhost ``` eingegeben wird, erscheint die Fehlermeldung "Verbindung fehlgeschlagen Firefox kann sich nicht mit dem Server auf localhost verbinden...". Dies ist darauf zurückzuführen, dass kein Docker-Port-Mapping gemacht wurde. 
Wenn mit dem run-Befehl der Hostport und der Containerport festgelegt wird, wird die Portweiterleitung vom Host zum Container eingerichtet.   

## run-Befehl und Portweiterleitung

Der run-Befehl wird entsprechend um die Einrichtung der Portweiterleitung erweitert '-p 3000:80' und dem Container wird mit '--name webserver' der Name 'webserver' gegeben. Dabei steht '-d' für detached, der Container läuft also im Hintergrund weiter und blockiert nicht das Terminal. 
Der Name und der Hostport dürfen nur einmalig vergeben werden. Der Name aufgrund der fehlerfreien Identifizierung und die Vergabe eines doppelten Hostports würde zu einer Kollision der Datenpakete führen. 

```bash
docker run -d --name webserver -p 3000:80 nginx
```

Hinweis: Es wird automatisch TCP als Übertragungsprotokoll verwendet. Soll UDP verwendet werden, muss entsprechend '-p 3000:80/udp' eingegeben werden. Wenn beide Übertragungsprotokolle verwendet werden sollen, dann muss '-p 3000:80/udp - p 3000:80/tcp' eingegeben werden. Zudem besteht die Syntax <Hostport>:<Containerport>.

Damit entsteht:

         Linux Host
┌────────────────────────────┐
│  localhost:3000            │
│       │                    │
│       ↓                    │
│  Docker Port Mapping       │
│       │                    │
│       ↓                    │
│  ┌──────────────────────┐  │
│  │ Container: webserver │  │
│  │                      │  │
│  │              Nginx   │  │
│  │               :80    │  │
│  └──────────────────────┘  │
└────────────────────────────┘

In den Browser eingeben:

```bash
http://localhost:3000/
```

Ausgabe:
Welcome to nginx! ...

Damit findet folgender Ablauf statt:

   Docker Image
        ↓
    Container
        ↓
   Nginx-Prozess
        ↓
Container-Port 80
        ↓
   Port-Mapping
        ↓
  Host-Port 3000
        ↓
       curl
        ↓
     Browser

Mit ```bash docker port webserver ``` können die verwendeten Ports des Containers 'webserver' abgefragt werden: 

Ausgabe:

80/tcp -> 0.0.0.0:3000
80/tcp -> [::]:3000

Erklärung:

80/tcp       → Port 80 des Containers/Übertragungsprotokoll TCP
0.0.0.0:3000 → IPv4-Adresse/alle Host-Interfaces auf Port 3000
[::]:3000    → IPv6, ebenfalls Port 3000

## Was steckt in einem Image?

Als Beispiel nehmen wir das bereits verwendete Image 'nginx:latest'. Es enthält vereinfacht gesagt alles, was Nginx braucht, damit es innerhalb eines Containers ausgeführt werden kann:

nginx Image
│
├── Nginx
├── Konfiguration
├── benötigte Bibliotheken
├── benötigte Dateien
├── Webinhalte
└── weitere Bestandteile

Hinweis: Nicht enthalten ist ein eigener Linux-Kernel. Da sich Container den Kernel des Hostbetriebssystems teilen. Daher benötigen Container, im Gegensatz zu virtuellen Maschinen, keinen eigenen Kernel.

Images bestehen aus Layern. In der Ausgabe von ```bash docker info ``` war 'Storage Driver: overlayfs' zu sehen. Dies bezieht sich auf die Layer des Docker-Images.

Vereinfacht kann man sich das Nginx-Image so vorstellen:

┌──────────────────────────┐
│ Layer 4: Nginx           │
├──────────────────────────┤
│ Layer 3: Konfiguration   │
├──────────────────────────┤
│ Layer 2: Bibliotheken    │
├──────────────────────────┤
│ Layer 1: Basis-System    │
└──────────────────────────┘

Jede Schicht baut auf der vorherigen auf. Das hat einen sehr praktischen Vorteil. Wenn mehrere Images dieselben unteren Layer benötigen, müssen diese nicht mehrfach gespeichert werden. Beispielsweise könnten zwei Images beide auf einer bestimmten Ubuntu- oder Debian-Basis aufbauen. Docker kann gemeinsame Layer wiederverwenden. Das ist einer der Gründe, warum Images nicht einfach als riesige, unabhängige Dateien behandelt werden.

Man kann sich die Historie des Images ausgeben lassen. Dafür folgenden Befehl eingeben:

```bash
docker image history nginx
```

Die Ausgabe beginnt unten mit der Basis, im Fall von Nginx ist es 'trixie'. Der Codename der Debian-Version, auf der das Nginx-Image basiert. Darauf bauen die weiteren Schritte auf. 
In der Datei 'history-nginx-image.md' findet sich die Ausgabe des Befehls und eine Erläuterung dieser.

## Ein Überblick des Erarbeiteten

Damit wurde das Docker-Grundmodell aufgebaut:

     Dockerfile
         ↓
       Build
         ↓
┌─────────────────┐
│      Image      │
│                 │
│     mehrere     │
│      Layer      │
└────────┬────────┘
         ↓
     docker run
         ↓
┌─────────────────┐
│    Container    │
│                 │
│   ENTRYPOINT    │
│        ↓        │
│       CMD       │
│        ↓        │
│     Prozess     │
└────────┬────────┘
         ↓
     Anwendung

Docker-Lifecycle:

 nginx Image vorhanden
            ↓
       docker run
            ↓
     Container erstellt
            ↓
      Nginx läuft
            ↓ 
         Strg+C
            ↓
     Container beendet
            ↓
        docker ps
            ↓
    nicht mehr sichtbar
            ↓
      docker ps -a
            ↓
Container noch vorhanden

Dann:

docker run -d --name webserver -p 3000:80 nginx
                       ↓
        Container läuft im Hintergrund
                       ↓
                Host-Port 3000
                       ↓
                Container-Port 80
                       ↓
                     Nginx
                       ↓
          curl http://localhost:3000
                       ↓
            http://localhost:3000
                       ↓
              Welcome to nginx!