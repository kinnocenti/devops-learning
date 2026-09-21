# Testung des ersten Hardenings

Im nächsten Schritt wird das erste Hardening getestet und überprüft, ob der Taskmanager den Anforderungen entsprechend funktioniert. Damit dies getestet werden kann, muss der Image-Build neu ausgeführt werden.

## Image-Build und Ausführung des Taskmanagers

Mit dem folgenden Befehl den Image-Build neu ausführen:

```bash
docker build -t taskmanager .
```

Dann wird der vorherige Container mit ```bash docker rm taskmanager``` gelöscht und ein neuer Container mit dem neuen Image erstellt und ausgeführt. Dafür folgende Befehle eingeben:

```bash
docker run --name taskmanager -p 3001:5000 -v /<Pfad>/devops-learning/taskmanager/taskmanager.db:/app/taskmanager.db taskmanager   # neuen Container erstellen

curl http://localhost:3001   # testet die Verbindung zum lokalen Server auf Port 3001
```

Und im Browser mit http://localhost:3001 aufrufen.

## Testung des Taskmanagers

Zunächst funktioniert der Taskmanager weiterhin vollständig:

- Anwendung wird erreicht
- Seiten werden dargestellt
- Daten aus SQLite können gelesen werden
- Templates und CSS funktionieren

Beim Erstellen einer Aufgabe oder Gruppe tritt jedoch ein Fehler auf. Es können keine Aufgaben und Gruppen erstellt werden. In der Datenbank wurden auch keine Daten eingefügt. Dies weist auf Probleme der Schreibberechtigungen hin.  

## Fehlersuche 

Im ersten Schritt der Fehlersuche wird der Log des Taskmanagers untersucht. Darin werden die folgenden beiden Ausgaben angezeigt:

sqlite3.OperationalError: attempt to write a readonly database

sqlite3.OperationalError: database is locked

Der erste Fehler bestätigt die vorherige Vermutung. Es wurde versucht in eine readonly Datenbank zu schreiben. Die Leseberechtigung alleine ist nicht ausreichend. Die zweite Ausgabe zeigt, dass der Zugriff auf die Datenbank verweigert wird. Es muss also eine Schreibberechtigung eingerichtet werden.

### Untersuchung der Berechtigungen

Mit dem folgenden Befehl wird geprüft, unter welchem Benutzer der Container läuft:

```bash
docker exec taskmanager id
```

Ausgabe:

uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)

Damit wird bestätigt, dass Flask tatsächlich unter dem gewünschten Nicht-Root-Benutzer läuft. Anschließend werden die Berechtigungen des Arbeitsverzeichnisses untersucht:

```bash
docker exec taskmanager ls -ld /app
```

Ausgabe:

drwxr-xr-x 1 root root ... /app

'appuser' hat damit zwar Lese- und Ausführungsrechte auf /app, aber keine Schreibrechte. Die Datenbank selbst wurde mit folgenden Befehl untersucht:

```bash
docker exec taskmanager ls -la /app/taskmanager.db
```

Ausgabe:

-rw-rw-r-- 1 appuser appuser ... /app/taskmanager.db

Die Datenbankdatei selbst ist damit für appuser les- und schreibbar ('rw'). Für einen weiteren Test soll mit dem folgenden Befehl eine Datei mit dem Namen 'testfile' im Verzeichnis 'app' angelegt werden.

```bash
docker exec taskmanager sh -c 'touch /app/testfile'
```

Ausgabe:

touch: cannot touch '/app/testfile': Permission denied

Die Ausgabe bestätigt, dass 'appuser' keine Dateien im Verzeichnis 'app' anlegen kann.
Damit wird deutlich, dass nicht nur die Berechtigung der Datenbankdatei betrachtet werden darf. SQLite benötigt für bestimmte Schreiboperationen auch einen geeigneten beschreibbaren Bereich im Datenbankverzeichnis.

## Trennung von Anwendungscode und persistenten Daten

Statt das gesamte 'app'-Verzeichnis für 'appuser' beschreibbar zu machen, wird eine sauberere Struktur gewählt.

Der Anwendungscode verbleibt unter '/app':

/app
├── app.py
├── templates/
└── static/

Die veränderlichen persistenten Daten werden dagegen unter '/data' abgelegt:

/data
└── taskmanager.db

Damit entsteht eine klare Trennung:

/app
    Anwendungscode
    möglichst unveränderlich

/data
    persistente Anwendungsdaten
    beschreibbar

Diese Trennung ist auch aus Security-Sicht sinnvoll, da ein kompromittierter Anwendungsprozess dadurch nicht automatisch Schreibzugriff auf den gesamten Anwendungscode erhält.

## Anpassung der 'app.py'-Datei

In der Datei 'app.py' verwenden die Datenbankverbindungen bisher:

```bash
sqlite3.connect("taskmanager.db")
```

Damit 'taskmanager.db' im Verzeichnis 'data' verwendet werden kann, müssen alle 'sqlite3.connect'-Zeilen in 'app.py' wie folgt angepasst werden:

```bash
sqlite3.connect("/data/taskmanager.db")
```

Der Datenbankpfad ist damit innerhalb des Containers eindeutig vom Anwendungscode getrennt.

## Anpassung der Dockerfile

Für den Datenbereich wird auch die Dockerfile erweitert. In der letzten Dockerfile-Anpassung wurde folgender Befehl eingefügt:

```bash
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 appuser
```

Mit der folgenden Anpassung wird '/data' angelegt und 'appuser' als Besitzer dieses Verzeichnisses gesetzt. Dadurch kann der Flask-Prozess unter UID 1000 dort schreiben, ohne Schreibrechte auf das gesamte 'app'-Verzeichnis zu erhalten.

```bash
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 appuser \
    && mkdir /data \
    && chown appuser:appuser /data
```

## Anpassung des Bind-Mounts

Der bisherige Bind-Mount:

Host taskmanager.db
        ↓
/app/taskmanager.db

muss auch auf den neuen Datenpfad geändert werden:

Host
/<Pfad>/devops-learning/taskmanager/taskmanager.db
                        │
                        │Bind-Mount
                        ▼
              Container
              /data/taskmanager.db

Damit folgenden 'docker run'-Befehl angepasst verwenden:

```bash
docker run --name taskmanager -p 3001:5000 -v /<Pfad>/devops-learning/taskmanager/taskmanager.db:/data/taskmanager.db taskmanager
```

Der verwendete Mount kann weiterhin ohne explizites ':rw' angegeben werden, da in ein Bind-Mount standardmäßig read-write eingebunden wird.

Wichtig ist die Unterscheidung:

- Docker ':rw' bestimmt, ob der Mount grundsätzlich schreibbar eingebunden wird.
- Die Linux-Dateirechte bestimmen, ob der konkrete Prozess tatsächlich schreiben darf.

## Abschlusstest

Nach den Änderungen wird wieder ein Image-Build durchgeführt, der Container mit dem neuen Datenpfad gestartet und der Taskmanager im Browser aufgerufen.

Der Taskmanager funktioniert vollständig. Insbesondere kann:

- die Anwendung als 'appuser' ausgeführt werden
- auf die bestehende SQLite-Datenbank zugegriffen werden
- die Datenbank gelesen werden
- eine neue Gruppe erstellt werden
- die Änderung erfolgreich in SQLite gespeichert werden
- die neu erstellte Gruppe anschließend auch in DBeaver überprüft werden

Damit wurde praktisch nachgewiesen, dass die Anwendung für ihre Aufgabe keine Root-Rechte benötigt.

## Ergebnis

Der erste Security-Hardening-Schritt ist damit erfolgreich abgeschlossen:

Container
    │
    ▼
Flask läuft als appuser
UID 1000
    │
    ├── /app
    │     Anwendungscode
    │     möglichst nicht beschreibbar
    │
    └── /data
          persistente Daten
          beschreibbar

Das Prinzip Least Privilege wurde damit nicht nur theoretisch betrachtet, sondern anhand eines echten Problems praktisch umgesetzt und getestet.

Ein wichtiger Punkt ist außerdem die Unterscheidung zwischen:

   Docker Mount-Berechtigung
              vs.
Linux-Dateisystemberechtigungen

und zwischen:

         Anwendungscode
              vs.
veränderliche persistente Daten

Die Containerisierung bleibt damit weiterhin funktional, während gleichzeitig die Berechtigungen des laufenden Prozesses reduziert wurden.

## Gesamtablauf

Flask als root
│
▼
funktioniert
│
▼
Least Privilege
│
▼
Flask als appuser / UID 1000
│
▼
Lesen funktioniert
│
▼
Schreiben schlägt fehl
│
▼
"attempt to write a readonly database"
│
▼
Datei-Rechte untersucht
│
├── taskmanager.db → appuser: rw 
│
└── /app → appuser: kein write 
│
▼
Code und Daten getrennt
│
├── /app → Anwendung
│
└── /data → persistente Daten
│
▼
SQLite → /data/taskmanager.db
│
▼
appuser → schreiben 
│
▼
Gruppe erstellt
│
▼
DBeaver → Daten vorhanden 