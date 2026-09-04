# Erstellung der 'requirements.txt'-Datei

Die 'requirements.txt'-Datei ist eine einfache Textdatei in der Programmiersprache Python, die alle externen Pakete und Bibliotheken auflistet, die ein Projekt zum Laufen benötigt. Dafür im ordner 'taskmanager' die Datei 'requirements.txt' anlegen.
Damit wirklich verstanden wird, warum etwas in diese Datei eingetragen wird, muss teilweise etwas ausgeholt werden.

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

Darum in 'requirements.txt' folgende Zeile einfügen:

```bash
FROM python:3.12-slim-trixie
```

## Zweite Zeile

Für den Container benötigen wir auch Flask als Webframework. Dies muss entsprechend installiert werden. Damit es beim Image-Build installiert wird, wird 'RUN' verwendet. 'RUN' bedeutet ausführen, aber nur im Image-Build. Es ist also kein 'docker run'. Da auf dem Host Flask version 3.1.3 verwendet wird, wird auch diese Version im Image-Build installiert und folgende Zeile in 'requirements.txt' eingefügt:  

```bash
RUN pip install Flask==3.1.3
```

Hinweis: Bei der Versionswahl ist auch immer zu beachten welche Verion auf dem Host verwendet wird, es muss nicht zwangsläufig die selbe Version sein, aber sie muss kompatibel sein und den Anfordeungen entsprechen. Dies gilt generell.

Damit ergibt sich folgender vereinfachter Ablauf:

Dockerfile
   │
   ├── FROM python:3.12-slim-trixie
   │
   └── RUN pip install Flask==3.1.3│
             ↓
      Befehl wird beim BUILD ausgeführt
             ↓
      Flask landet im Image

## Dritte Zeile

Mit 'COPY' werden Dateien oder Verzeichnisse aus dem Build-Kontext in das Image kopiert. Die erstellte 'requirements.txt' muss also, damit sie im Image angewendet werden kann mit 'COPY' in das entstehende Image kopiert werden. Darum folgendes einfügen:

```bash
COPY requirements.txt .   # Syntax: COPY <Quelle> <Ziel>
```

## Vierte Zeile

Damit die mit 'COPY' kopierte 'requirements.txt' im entstehenden Image ausgeführt werden kann, muss auch hier mit 'RUN' gearbeitet werden und folgende Zeile eingefügt werden:

```bash
RUN pip install -r requirements.txt
```

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

Neben 'requirements.txt' werden natürlich noch weitere Dateien aus dem Ordner 'taskmanager' benötigt.





Gesamtablauf:

Dockerfile
   │
   ↓
FROM python:3.12-slim-trixie
   │
   ↓
Build
   │
   ↓
Docker Image
   │
   ↓
docker run
   │
   ↓
Container