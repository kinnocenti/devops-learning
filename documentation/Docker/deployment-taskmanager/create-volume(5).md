# Erstellung des Taskmanager-Volumes

Im nächsten Schritt wird das Volume für den Taskmanager erstellt, eingebunden und getestet. Mit ```bash docker volume create taskmanager-data ``` wurde bereits das Volume erstellt. Dieses enthält aber noch nicht die Datenbank, was im weiteren konfiguriert wird.

## Übertragung der bestehenden Datenbank in das Volume

Das neu erstellte Volume ist zunächst leer und enthält noch nicht die bereits vorhandene SQLite-Datenbank des Taskmanagers. Bevor der laufende Taskmanager auf das neue Volume umgestellt wird, wird deshalb zunächst die bestehende Datenbank in das Volume übertragen. Der laufende Taskmanager wird zu diesem Zeitpunkt noch nicht verändert. Dadurch bleibt der bisher funktionierende Zustand mit dem Bind-Mount erhalten, bis die Daten erfolgreich übertragen und überprüft wurden.

Für die Übertragung wird ein temporärer Container aus dem bereits vorhandenen taskmanager-Image verwendet. Dabei werden zwei Speicherbereiche eingebunden:

Host
/home/kath/Projects/devops-learning/taskmanager/taskmanager.db
        │
        │ Bind-Mount, read-only
        ▼
temporärer Container
/source/taskmanager.db

Docker Volume
taskmanager-data
        │
        ▼
temporärer Container
/data

Die bestehende Datenbank wird anschließend mit cp in das Volume kopiert:

```bash
docker run --rm \
  -v taskmanager-data:/data \
  -v /home/kath/Projects/devops-learning/taskmanager/taskmanager.db:/source/taskmanager.db:ro \
  taskmanager \
  cp /source/taskmanager.db /data/taskmanager.db
```

Der Bind Mount der bestehenden Datenbank wird dabei mit ':ro' als read-only eingebunden. Der temporäre Container kann die vorhandene Datenbank somit lesen, aber nicht verändern. Das Schreiben erfolgt ausschließlich in das Docker Volume.

Mit '--rm' wird der temporäre Container nach Abschluss des Kopiervorgangs automatisch entfernt. Das Volume bleibt davon unabhängig bestehen.

Anschließend wird überprüft, ob die Datenbank im Volume vorhanden ist:

```bash
docker run --rm \
  -v taskmanager-data:/data \
  taskmanager \
  ls -lh /data
```

Die Ausgabe zeigt:

-rw-r--r-- 1 appuser appuser 24K ... taskmanager.db

Die Datenbank gehört damit dem Benutzer 'appuser', unter dem auch Flask im Taskmanager-Container ausgeführt wird.

Zusätzlich wird das übergeordnete Datenverzeichnis überprüft:

```bash
docker run --rm \
  -v taskmanager-data:/data \
  taskmanager \
  ls -ld /data
```

Ausgabe:

drwxr-xr-x 2 appuser appuser ... /data

Damit sind die bereits beim Non-Root-Container berücksichtigten Dateirechte auch für das Docker Volume passend eingerichtet. Der Benutzer 'appuser' besitzt die erforderlichen Zugriffsrechte auf das Datenverzeichnis und die Datenbankdatei.
Erst nachdem die Datenbank erfolgreich in das Volume übertragen und die Berechtigungen überprüft wurden, wird der eigentliche Taskmanager-Container vom bisherigen Bind-Mount auf das Docker Volume umgestellt.

## Umstellung des Taskmanagers vom Bind Mount auf das Docker Volume

Nachdem die bestehende Datenbank erfolgreich in das Volume übertragen und die Zugriffsrechte überprüft wurden, kann der Taskmanager vom bisherigen Bind-Mount auf das Docker Volume umgestellt werden.

Zunächst wird der bisherige Container gestoppt und entfernt:

```bash
docker stop taskmanager
docker rm taskmanager
```

Dabei wird ausschließlich der Container entfernt. Die bisherige Datenbank auf dem Host und das Docker Volume 'taskmanager-data' bleiben erhalten. Der Taskmanager wird anschließend mit dem Docker Volume neu gestartet:

```bash
docker run -d \
  --name taskmanager \
  -p 3001:5000 \
  -v taskmanager-data:/data \
  taskmanager
```

Der entscheidende Unterschied zum bisherigen Containerstart besteht beim Mount:

Bisher:

Host
/home/kath/Projects/devops-learning/taskmanager/taskmanager.db
                               │
                               │ Bind Mount
                               ▼
                     Container
                     /data/taskmanager.db

Nach der Umstellung:

Docker Volume
taskmanager-data
    │
    ▼
Container
/data
    │
    └── taskmanager.db

Der Container verwendet damit nicht mehr den konkreten Host-Pfad der Datenbank. Stattdessen wird das Volume 'taskmanager-data' unter '/data' eingebunden.
Die Anwendung selbst bleibt unverändert. Flask läuft weiterhin als 'appuser' mit UID 1000 und verwendet '/data/taskmanager.db' als Datenbankpfad.

## Funktionstest

Nach dem Start des Containers wird zunächst überprüft, ob der Taskmanager erreichbar ist und die vorhandenen Daten weiterhin angezeigt werden. Anschließend wird im Taskmanager eine neue Aufgabe erstellt und einer bereits vorhandenen Gruppe zugeordnet. Nach der Rückkehr zur Startseite wird überprüft, ob die neue Aufgabe innerhalb der Gruppe angezeigt wird.

Damit wird die gesamte Verarbeitungskette getestet:

       Browser
          ↓
        Flask
          ↓
  Python / sqlite3
          ↓
/data/taskmanager.db
          ↓
    Docker Volume

Die neu erstellte Aufgabe wird nach dem Zurückkehren zur Startseite korrekt innerhalb der Gruppe angezeigt. Damit ist nachgewiesen, dass der Taskmanager die Datenbank aus dem Docker Volume lesen und auch Änderungen darin speichern kann.

## Persistenztest nach Löschen des Containers

Um zusätzlich den unterschiedlichen Lebenszyklus von Container und Volume praktisch nachzuweisen, wird der laufende Taskmanager-Container gelöscht:

```bash
docker rm -f taskmanager
```

Das Volume 'taskmanager-data' wird dabei nicht gelöscht. Anschließend wird ein neuer Taskmanager-Container mit demselben Volume gestartet:

```bash
docker run -d \
  --name taskmanager \
  -p 3001:5000 \
  -v taskmanager-data:/data \
  taskmanager
```

Nach dem erneuten Aufruf des Taskmanagers im Browser ist die zuvor erstellte Aufgabe weiterhin vorhanden.

Damit wurde praktisch nachgewiesen:

      Container A
           ↓
     schreibt Daten
           ↓
    taskmanager-data
           ↓
Container A wird gelöscht
           ↓
  Volume bleibt erhalten
           ↓
Container B wird erstellt
           ↓
    gleiches Volume
           ↓
Daten weiterhin vorhanden

Der Container und der persistente Storage besitzen somit unterschiedliche Lebenszyklen. Der Container kann ersetzt oder gelöscht werden, ohne dass die im Docker Volume gespeicherten Anwendungsdaten dadurch verloren gehen.

## Ergebnis

Der Taskmanager wurde erfolgreich vom bisherigen Bind Mount auf das Docker Volume taskmanager-data umgestellt.

Dabei wurden folgende Punkte praktisch bestätigt:

- Das Volume kann als persistenter Speicher für den Taskmanager verwendet werden.
- Die bestehende SQLite-Datenbank kann in das Volume übertragen werden.
- Die Zugriffsrechte sind für den Non-Root-Benutzer appuser passend eingerichtet.
- Der Taskmanager kann Daten aus dem Volume lesen und darin speichern.
- Das Löschen des Containers führt nicht zum Verlust der Daten im Volume.
- Ein neuer Container kann mit demselben Volume auf die vorhandenen Daten zugreifen.
- Der Taskmanager verwendet damit nun für den praktischen Test das Docker Volume als persistenten Datenspeicher.