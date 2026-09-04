# Erstellung der Dockerfile

Die Grundlage eines Docker Image ist die Dockerfile, eine einfache Textdatei mit Anweisungen und Befehlen. Die Erstellung der Dockerfile wird Zeile für Zeile erklärt.

Hinweis: Die folgenden Zeilen werden immer unter einander in die Datei eingefügt.

## Erste Zeile

Die Datei beginnt mit 'FROM'. Hier muss bestimmt werden welches Ausgangs/Basis-Image oder Image verwendet werden soll. In dieser Zeile wird Docker also das Ausgangs/Basis-Image übergeben. Dafür muss das passende Ausgangs/Basis-Image für die Anforderungen entsprechend ausgewählt werden. 

Für den Taskmanager wird ein Basis-Image ausgewählt. Da für den Taskmanager auf dem Host Python version 3.12.3 verwendet wird, fällt entsprechend die Wahl auf ein Python 3.12, dabei stehen folgende zur Auuswahl:

python:3.12
python:3.12-slim
python:3.12-trixie
python:3.12-slim-trixie
python:3.12-bookworm
python:3.12-slim-bookworm

Für den einfachen Flask-Taskmanager ist python:3.12-slim-trixie eine gute Wahl:

- Python 3.12 entspricht unserer bisher getesteten Major/Minor-Version
- Debian ist eine etablierte allgemeine Linux-Basis
- Trixie ist eine aktuell verfügbare Debian-Basis des offiziellen Python-Images
- 'slim' hält das Image relativ klein
- Wir benötigen keine umfangreiche Build-/Entwicklungsumgebung

Darum in 'Dockerfile' folgende Zeile einfügen:

```bash
FROM python:3.12-slim-trixie
```

Hinweis: Bei der Versionswahl ist auch immer zu beachten welche Verion auf dem Host verwendet wird, es muss nicht zwangsläufig die selbe Version sein, aber sie muss kompatibel sein und den Anfordeungen entsprechen. Dies gilt generell.

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

Hinweis: 'RUN' passiert beim Bauen des Images und ist nicht zu verwechseln mit 'docker run'.

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

## Fünfte Zeile

Neben 'requirements.txt' werden natürlich noch weitere Dateien aus dem Ordner 'taskmanager' benötigt. Darum werden 'app.py' und die beiden Ordner 'templates' und 'static' installiert

```bash
COPY app.py templates/ static/ /app/
```

Hinweis: Wenn mehrere Quellen angegeben werden, können diese einfach mit einem Leerzeichen getrennt hintereinander weg geschrieben werden und das Ziel muss eindeutig als Verzeichnis angegeben werden.

## Sechste Zeile

Mit 'CMD' wird festgelegt welcher Prozess standardmäßig gestartet werden soll, wenn aus diesem Image ein Container entsteht. Wenn auf dem Host in der .venv der Taskmanager gestartet werden soll, wird im Terminel entsprechend ```bash flask --app app run ``` eingegeben. Da im Container eine eigene Umgebung besteht, muss dieser Befehl im Container aufgerufen werden. Darum folgende Zeile einfügen:

```bash
CMD ["flask", "--app", "app", "run"]
```