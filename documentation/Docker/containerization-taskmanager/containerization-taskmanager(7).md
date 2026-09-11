# Containerisierung des Taskmanagers

Nachdem die Grundlagen für Docker geschaffen wurden, wird nun der Taskmanager containerisiert. Es werden also alle Schritte durchlaufen, die notwendig sind, um die Webanwendung in einem Container lauffähig zu machen. Es wird mit dem Build des Images begonnen.

Damit wird folgender Aufbau umgesetzt.

Linux-Host
    │
    └── Docker Engine
          │
          └── Container
                │
                └── Taskmanager
                      ├── Python
                      ├── Flask
                      ├── Anwendungscode
                      └── Abhängigkeiten

## Image-Build

Das Image muss zunächste zusammengebaut und damit erstellt werde, damit es als Image entsprechend bei der Containerisierung verwendet werden kann.

Im Terminal in das Taskmanager-Verzeichnis wechseln und folgenden Befehl, zur Erstellung des Images, eingeben:

```bash
docker build -t taskmanager .
```

Danach kann die Auflistung der vorhandenen Images mit ```bash docker images ``` angezeigt werden.  

## Datenbank

Damit der Container gestartet und die Webanwendung richtig läuft muss noch die Datenbank eingehängt werden, damit Flask im Container mit der Datenbank kommunizieren kann. 

WORKDIR /app
      ↓
sqlite3.connect("taskmanager.db")
      ↓
/app/taskmanager.db
      ↑
   Mount
      ↑
Host: .../taskmanager/taskmanager.db

Mit folgenden Befehl wird der Container gestartet:

```bash
docker run --name taskmanager -p 3001:5000 -v >Hostpfad</taskmanager.db:>Containerpfad</taskmanager.db taskmanager
```

In den folgenden Schritten wird der Befehl ausgeführt

docker run
│
├── --name taskmanager
│      → Container bekommt den Namen taskmanager
│
├── -p 3001:5000
│      → Hostport:3001 → Containerport:5000
│
├── -v HOST:CONTAINER
│      → Host-Datenbank anbinden in → /app/taskmanager.db
│
└── taskmanager
       → zu verwendendes Image

Hinweis: Mit '-v' wird in diesem Befehl ein Bind Mount eines Volumens durchgeführt. Das bedeutet, dass ein Verzeichnis oder eine Datei auf dem Host direkt mit einem Ordner im Docker-Container verbunden wird. 

Mit den beiden folgenden Befehlen kann geprüft werden, ob der Container auf die Verzeichnisse zugreifen und die darin enthaltenen Dateien korrekt eingefügt wurden mit dem Container-Build. Mit ```bash docker exec <Containername> <Befehl> ``` wird der Befehl im Container ausgeführt und die Ausgabe aus dem Container angezeigt.

Dafür die drei folgenden Befehle eingeben:

```bash
docker exec taskmanager ls -la /app

docker exec taskmanager ls -la /app/templates

docker exec taskmanager ls -la /app/static
```

Bevor der Taskmanager im Browser aufgerufen wird, wird mit 'curl' überprüft, ob der Container korrekt läuft und die Anwendung darin erreichbar ist. Darum folgenden Befehl eingeben:

```bash
curl http://localhost:3001
```

Im Browser http://localhost:3001 eingeben.

Ablauf, der sich daraus ergibt:

   Dockerfile
       ↓
   Image bauen
       ↓
Container starten
       ↓
      CMD
       ↓
     Flask
       ↓
  0.0.0.0:5000
       ↓
Docker Port Mapping
       ↓
 localhost:3001
       ↓
  Taskmanager

Und zusätzlich:

    Host: taskmanager.db
            │
            │ Bind Mount
            ▼
Container: /app/taskmanager.db