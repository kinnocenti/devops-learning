# Erstellung der Dockerfile

Die Grundlage eines Docker-Images ist die Dockerfile, eine einfache Textdatei mit Anweisungen und Befehlen. Die Erstellung der Dockerfile wird Zeile für Zeile erklärt.
Dafür im Ordner 'taskmanager' die Datei 'Dockerfile' anlegen.

Hinweis: Die folgenden Zeilen werden immer unter einander in die Datei eingefügt.

## Erste Zeile

Die Datei beginnt mit 'FROM'. Hier muss bestimmt werden welches Ausgangs/Basis-Image verwendet werden soll. In dieser Zeile wird Docker also das Ausgangs/Basis-Image übergeben. Dafür muss das passende Ausgangs/Basis-Image, den Anforderungen entsprechend, ausgewählt werden. 

Für den Taskmanager wird ein Basis-Image ausgewählt. Da für den Taskmanager auf dem Host Python version 3.12.3 verwendet wird, fällt entsprechend die Wahl auf Python 3.12, dabei stehen folgende Versionen zur Auswahl:

python:3.12
python:3.12-slim
python:3.12-trixie
python:3.12-slim-trixie
python:3.12-bookworm
python:3.12-slim-bookworm

Für den einfachen Flask-Taskmanager ist python:3.12-slim-trixie eine gute Wahl:

- Python 3.12 entspricht den bisher getesteten Major/Minor-Version
- Debian ist eine etablierte allgemeine Linux-Basis
- Trixie ist eine aktuell verfügbare Debian-Basis des offiziellen Python-Images
- 'slim' hält das Image relativ klein
- Es wird keine umfangreiche Build-/Entwicklungsumgebung benötigt

Darum in 'Dockerfile' folgende Zeile einfügen:

```bash
FROM python:3.12-slim-trixie
```

Hinweis: Bei der Versionswahl ist auch immer zu beachten welche Version auf dem Host verwendet wird, es muss nicht zwangsläufig die selbe Version sein, aber sie muss kompatibel sein und den Anforderungen entsprechen. Dies gilt generell.

## Zweite Zeile

WORKDIR ist eine Anweisung in einem Dockerfile, die das Arbeitsschwerpunkt-Verzeichnis (Working Directory) für alle nachfolgenden Befehle festlegt. Sie bestimmt, in welchem Ordner des Containers Befehle wie RUN, CMD, ENTRYPOINT, COPY und ADD ausgeführt werden. Wenn das angegebene Verzeichnis im Container noch nicht existiert, wird es von Docker automatisch erstellt. 'WORKDIR /app' legt also für die folgenden Dockerfile-Anweisungen und später für Prozesse im Container das Arbeitsverzeichnis auf /app fest. Die folgende Zeile in 'Dockerfile' eingefügt:  

```bash
WORKDIR /app
```

## Dritte Zeile

Mit 'COPY' werden Dateien oder Verzeichnisse aus dem Build-Kontext in das Image kopiert. Die erstellte 'requirements.txt' muss also, damit sie im Image angewendet werden kann mit 'COPY' in das entstehende Image kopiert werden. Darum folgendes einfügen:

```bash
COPY requirements.txt .   # Syntax: COPY <Quelle> <Ziel>
```

## Vierte Zeile

Damit die mit 'COPY' kopierte 'requirements.txt' beim Image-Build ausgeführt werden kann, wird 'RUN' verwendet und folgende Zeile eingefügt:

```bash
RUN pip install -r requirements.txt
```

Hinweis: 'RUN' passiert beim Bau des Images und ist nicht zu verwechseln mit 'docker run'.

Ablauf der dritten und vierten Zeile:

HOST
│ requirements.txt
↓
COPY
↓
IMAGE
│ requirements.txt
↓
RUN pip install -r requirements.txt
↓
Flask + Abhängigkeiten

Hinweis: 'requirements.txt' muss vor den anderen notwendigen Dateien des Taskmanagers für das Image eingefügt werden.
Denn damit werden:

- die Abhängigkeiten definiert
- sie installiert
- anschließend den sich häufiger ändernden Anwendungscode kopiert

## Fünfte bis siebte Zeile

Neben 'requirements.txt' werden natürlich noch weitere Dateien aus dem Ordner 'taskmanager' benötigt. Darum werden 'app.py' und die beiden Ordner 'templates' und 'static' in den Container kopiert. Da es drei unterschiedliche Ziele gibt, werden auch drei COPY-Anweisungen eingefügt:

```bash
COPY app.py /app/   # kopiere die Datei 'app.py' in das Verzeichnis 'app' 
COPY templates/ /app/templates/   # kopiere das Verzeichnis 'templates' in das Unterverzeichnis 'templates' im Verzeichnis 'app'
COPY static/ /app/static/   # kopiere das Verzeichnis 'static' in das Unterverzeichnis 'static' im Verzeichnis 'app'
```

Hinweis: Wenn mehrere Quellen angegeben werden, können diese einfach mit einem Leerzeichen getrennt hintereinander weg geschrieben werden und das Ziel muss am Ende des Befehls als eindeutiges Verzeichnis angegeben werden.

## Achte Zeile

Mit 'CMD' wird festgelegt welcher Prozess standardmäßig gestartet werden soll, wenn aus diesem Image ein Container entsteht. Wenn auf dem Host in der .venv der Taskmanager gestartet werden soll, wird im Terminal entsprechend ```bash flask --app app run ``` eingegeben. 
Da im Container eine eigene Umgebung besteht, muss dieser Befehl im Container aufgerufen werden. Das wäre nach Syntax ```bash CMD ["flask", "--app", "app", "run"] ```, aber der Befehl aus der .venv kann nicht eins zu eins übernommen werden. 
Würde der Befehl so eingegeben, könnte keine Verbindung aufgebaut werden. Es muss eine IP des Hosts übergeben werden und ein Port, auf den Flask lauschen soll. Als IP wird 0.0.0.0 übergeben, damit Flask auf allen IP-Schnittstellen lauscht. Zudem wird Port 5000 als Containerport übergeben.

Hinweis: Die Ports 0 bis 1023 sind unter Linux privilegierte Ports. Sie brauchen eine Berechtigung, damit sie genutzt werden können. Manche Anforderungen benötigen einen privilegierten Port, aber bei dem Taskmanager ist Best Practice und Least Privilege die Verwendung eines nicht-privilegierten Ports. In diesem Fall gilt,  warum extra eine Berechtigung erteilen, wenn genug Ports zur Verfügung stehen, die keine benötigen.

Hinweis: Jedes Argument muss einzeln mit CMD übergeben werden, damit der Befehl im Container ausgeführt werden kann. Zum Beispiel, darf nicht "--app app" übergeben werden, sondern "--app" "app". 

Hinweis: Wenn in einer Dockerfile mehrere CMD-Anweisungen stehen, werden sie von oben nach unten durchgegangen und die Vorherige immer mit der Folgenden überschrieben. Also wird die unterste CMD-Anweisung ausgeführt.

Damit die IP-Adresse und der Port weitergegeben werden können, müssen folgende Argumente verwendet werden:

- IP-Adresse → --host 0.0.0.0
- Port       → --port 5000

Damit muss folgende Zeile einfügt werden:

```bash
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]
```

Erklärung der Befehlselemente:

- flask           → Flask CLI starten
- --app, app      → Anwendung app.py verwenden
- run             → Entwicklungsserver starten
- --host, 0.0.0.0 → auf allen IPv4-Interfaces lauschen
- --port, 80      → auf Port 80 lauschen

Ablauf vom Browser zu Flask im Container:

  Browser
     │
     │ localhost:3001
     ▼
    Host
     │
     │ Docker Port Mapping
     │ 3001 → 5000
     ▼
 Container
     │
     │ Netzwerkinterface
     ▼
   Flask
0.0.0.0:5000

Gesamte Dockerfile:

```bash
FROM python:3.12-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py /app/

COPY templates/ /app/templates/

COPY static/ /app/static/

CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]
```

Hinweis: 'FROM', 'WORKDIR', 'COPY' und 'RUN' werden während des Container-Builds und CMD wird beim Start des Containers ausgeführt.

Damit ist die Dockerfile fertig und es kann im nächsten Schritt mit der Containerisierung begonnen werden.