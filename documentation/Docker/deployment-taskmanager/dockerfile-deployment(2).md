# Anpassung der Dockerfile für das Deployment

Für das Deployment muss die Dockerfile angepasst werden. Zunächst wird theoretisch hergeleitet, warum die Anpassungen vorgenommen werden müssen. Dann werden die notwendigen Zeilen eingefügt und die Befhle erklärt.

## Warum wird angepasst?

Der Container soll als Nicht-Root-Benutzer laufen. Beim bisherigen Containerstart lief die Flask-Anwendung als root:

uid=0(root) gid=0(root)

Das funktioniert technisch, ist für eine Anwendung aber nicht notwendig. Ein kompromittierter Anwendungsprozess würde dadurch mit mehr Rechten laufen, als er für seine eigentliche Aufgabe benötigt.
Hier greift das Prinzip Least-Privilege. Ein Prozess soll nur die Berechtigungen besitzen, die er für seine Aufgabe tatsächlich benötigt. Deshalb soll Flask künftig nicht mehr als root, sondern als normaler Benutzer im Container laufen.

### Zusammenhang mit dem Bind Mount

Die SQLite-Datenbank liegt auf dem Host und wird in den Container eingebunden:

       Host
  taskmanager.db
     UID 1000
         │
         │ Bind Mount
         ▼
     Container
/app/taskmanager.db

Die Host-Datei gehört dem Benutzer 'user' mit:

uid=1000(user)
gid=1000(user)

und besitzt die Rechte:

-rw-rw-r--

Für den Besitzer bedeutet das:

r = lesen
w = schreiben
- = nicht ausführen

Linux ordnet Dateirechte dabei anhand von UIDs und GIDs zu. Der Benutzername ist lediglich die lesbare Darstellung dieser numerischen Identität. Damit ein nicht privilegierter Prozess im Container die Datenbank weiterhin schreiben kann, soll der Anwendungsbenutzer deshalb die UID 1000 erhalten. Das bedeutet nicht, dass der Benutzer im Container 'user' heißen muss. Entscheidend ist die numerische UID:

  HOST                      CONTAINER
  user                       appuser
UID 1000                     UID 1000
   │                            │
   └──────── gleiche UID ───────┘
                 │
                 ▼
          taskmanager.db

Da die Datenbankdatei dem Besitzer mit UID 1000 Schreibrechte gewährt, kann der Flask-Prozess auch als UID 1000 auf die Datei zugreifen.

Die GID 1000 ist für diesen konkreten Schreibzugriff zunächst nicht erforderlich, da der Zugriff über die Owner-Rechte der Datei erfolgt. Gruppenrechte werden später relevant, wenn mehrere Prozesse oder Benutzer bewusst über eine gemeinsame Gruppe auf Dateien zugreifen sollen.

### Ziel der Änderung

Aus:

root (UID 0)
     ↓
   Flask
     ↓
   SQLite

wird:

appuser (UID 1000)
       ↓
     Flask
       ↓
     SQLite

Also:

   Bind Mount
        ↓
   Host-Datei
        ↓
 Linux-Dateirechte
        ↓
    UID 1000
        ↓
Nicht-Root-Benutzer
        ↓
  Least Privilege

Damit wird der Anwendungsprozess mit deutlich weniger Rechten ausgeführt, während der notwendige Zugriff auf die persistente Datenbank erhalten bleibt. Die Dockerfile wird dafür um zwei wesentliche Elemente ergänzt:

- einen Benutzer mit UID 1000 und GID 1000 (da Gruppen später behandelt werden, wird auch schon die GID festgelegt) anlegt
- festlegen, dass die Anwendung künftig unter einem Benutzer läuft

## Anpassungen in der Dockerfile

Zuerst wird mit dem RUN-Befehl eine Gruppe mit der GID 1000 und dem Namen 'appuser'. Zudem wird ein Benutzer mit der UID 1000 angelegt und der Gruppe mit der GID 1000 hinzugefügt und bekommt den Namen appuser. Dafür wird folgender Befehl in die Dockerfile unter WORKDIR eingefügt: 

```bash
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 appuser
```

Damit die Anwendung zukünftig unter dem Benutzer 'appuser' läuft, muss folgender Befehl über CMD einfügt werden:

```bash
USER appuser
```

## Aktuelle Dockerfile

```bash
FROM python:3.12-slim-trixie

WORKDIR /app

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 appuser

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py /app/

COPY templates/ /app/templates/

COPY static/ /app/static/

USER appuser

CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]
```