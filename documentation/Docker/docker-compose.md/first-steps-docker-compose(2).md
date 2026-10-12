# Docker Compose – Praktische Umsetzung und Datenpersistenz

Nachdem Docker-Compose theoretisch erarbeitet wurde, wird im folgenden Abschnitt die erste 'compose.yaml'-Datei erstellt und ausgeführt. 

## Bestandsaufnahme und Bereinigung

Zu Beginn wurden vorhandene Container, Volumes und Netzwerke überprüft:

```bash
docker ps -a

docker volume ls

docker network ls
```

Nicht mehr benötigte Testcontainer und die Test-Volumes 'mount-test-data' und 'mount-copy-test' wurden entfernt. Der bisherige Taskmanager-Container wurde ebenfalls gelöscht, da er noch das Standardnetzwerk 'bridge' verwendete und damit nicht der vorgesehenen Deployment-Konfiguration entsprach.

Beibehalten wurden:

- Docker-Volume taskmanager-data
- Netzwerk taskmanager-net
- Netzwerk test-net
- Docker-Standardnetzwerke

Die Test-Volumes wurden vor dem Entfernen mit 'docker volume inspect' überprüft. Die Entscheidung beruhte auf ihrer Zuordnung zu abgeschlossenen Lernversuchen und der vorhandenen Dokumentation. Nach der Bereinigung waren keine Container mehr vorhanden. Das Datenbank-Volume blieb erhalten.

## Compose-Konfiguration erstellen

Die Datei 'compose.yaml' wurde im Hauptverzeichnis des Repositorys angelegt. Damit liegt die Konfiguration des Anwendungsstacks außerhalb des Anwendungsverzeichnisses 'taskmanager'.

Verzeichnisstruktur
devops-learning/
├── compose.yaml
├── documentation/
├── taskmanager/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── templates/
│   └── static/
└── tests/

Inhalt der compose.yaml:

```bash
services:
  taskmanager:
    build:
      context: ./taskmanager
      dockerfile: Dockerfile
    ports:
      - "3001:5000"
    volumes:
      - taskmanager-data:/data
    networks:
      - taskmanager-net

volumes:
  taskmanager-data:
    external: true

networks:
  taskmanager-net:
    external: true
```

Erläuterung der Konfiguration:

Einstellung       | Bedeutung
-------------------------------------------------------------------------------------
services          | Beschreibt die Dienste des Anwendungsstacks
taskmanager       | Name des Compose-Service
build.context     | ./taskmanager ist der Build-Kontext für das Dockerfile und die 
                  | benötigten Dateien
build.dockerfile  | Gibt das Dockerfile relativ zum Build-Kontext an
ports             | Veröffentlicht Container-Port 5000 über Host-Port 3001
volumes           | Bindet taskmanager-data nach /data ein
networks	        | Verbindet den Service mit taskmanager-net
external: true	  | Verwendet das bereits vorhandene Volume beziehungsweise Netzwerk

Ein separates Datenbank-Service wurde bewusst nicht angelegt. SQLite ist eine dateibasierte Datenbank, auf die Flask direkt zugreift. Ein eigener Datenbankcontainer wäre für die aktuelle Architektur nicht erforderlich.

## Konfiguration überprüfen

Die Konfiguration von Compose wird mit dem folgenden Befehl abgefragt:

```bash
docker compose config
```

Die Ausgabe bestätigte unter anderem den aufgelösten Build-Kontext, die Portzuordnung, das vorhandene Volume und das externe Netzwerk. Der Befehl überprüft die aufgelöste Konfiguration, startet aber noch keine Container.

## Build und Start des Taskmanagers

Der Stack wurde mit folgendem Befehl gestartet:

```bash
docker compose up --build -d
```

Die Ausgabe bestätigte den erfolgreichen Build und Start:

✔ Image devops-learning-taskmanager Built
✔ Container devops-learning-taskmanager-1 Started

Der erzeugte Container heißt 'devops-learning-taskmanager-1'. Der Name wird von Compose standardmäßig aus Projektname, Service-Name und Instanznummer gebildet.

## Laufzeit und Netzwerk prüfen

Folgende Befehle zur Überprüfung eingeben:

```bash
docker ps

docker compose ps

docker network inspect taskmanager-net
```

Die Prüfungen bestätigten:

- Der Container läuft
- Host-Port 3001 wird auf Container-Port 5000 weitergeleitet
- Der Container ist mit 'taskmanager-net' verbunden

Die bei der Prüfung angezeigte Container-IP war 172.18.0.2. Sie beschreibt den aktuellen Zustand und wird nicht als feste Adresse vorausgesetzt.

## Funktionstest im Browser

Der Taskmanager wurde unter http://localhost:3001 geöffnet.

Folgende Tests waren erfolgreich:

- Vorhandene Aufgaben und Gruppen wurden angezeigt
- Die Aufgabe 'Testungsaufgabe' wurde erstellt und der Gruppe 'Testung' zugeordnet
- Die Gruppe 'Testungsgruppe' wurde erstellt
- Beide neuen Einträge erschienen anschließend auf der Startseite

Damit funktionierte die Anwendung im Compose-Container zunächst wie erwartet. Bei einer anschließenden Kontrolle mit DBeaver waren die neuen Einträge dort jedoch nicht sichtbar. Deshalb wurde der Datenbankzugriff genauer untersucht.

## Datenpersistenz untersuchen

Volume-Einbindung überprüfen mit:

```bash
docker inspect devops-learning-taskmanager-1 \
  --format '{{json .Mounts}}'
```

Die Ausgabe bestätigte folgende Zuordnung:

Type:        volume
Name:        taskmanager-data
Destination: /data
RW:          true

Das vorhandene Docker-Volume ist somit beschreibbar unter '/data' eingebunden.

## Datenbankpfad im Anwendungscode

Die untersuchten Flask-Routen verwenden 'sqlite3.connect("/data/taskmanager.db")'. Das gilt für die Startseite, die Detailansicht und die Routen zur Erstellung von Aufgaben und Gruppen.
Die Schreib-Routen führen nach ihren INSERT-Anweisungen außerdem 'connection.commit()' aus. Ein fehlender Commit war damit in den untersuchten Codeabschnitten nicht die Ursache.

## Datenbank direkt im Container abfragen

Um den tatsächlichen Datenbankinhalt zu überprüfen, wurde SQLite direkt im laufenden Container abgefragt:

```bash
docker exec devops-learning-taskmanager-1 \
  python -c "import sqlite3; c=sqlite3.connect('/data/taskmanager.db'); print(c.execute('SELECT id, name FROM groups ORDER BY id').fetchall()); print(c.execute('SELECT id, title FROM tasks ORDER BY id').fetchall()); c.close()"
```

Die Ausgabe enthielt unter anderem:

(9, 'Testungsgruppe')
(9, 'Testungsaufgabe')

Damit wurde bestätigt, dass beide Datensätze in der vom Container verwendeten Datenbank vorhanden sind.

Zusammen mit der bestätigten Volume-Einbindung ergibt sich folgender Datenfluss:

            Flask
              |
              v
     /data/taskmanager.db
              |
              v
Docker Volume: taskmanager-data
              |
              v
     Persistenter Storage

Die Anwendung speichert die Daten somit erfolgreich in der Datenbankdatei im Volume.

## Ursache der abweichenden DBeaver-Anzeige

In DBeaver wurde als Datenbankpfad folgender lokaler Dateipfad festgestellt:

/home/.../taskmanager.db

Die Flask-Anwendung verwendet dagegen:

/data/taskmanager.db

Es handelt sich um zwei unterschiedliche SQLite-Dateien. Die lokale Projektdatei wird nicht automatisch mit dem Docker-Volume synchronisiert.

Der von Docker gemeldete Mountpoint des Volumes lautet:

/var/lib/.../_data

Die Datenbankdatei im Volume liegt entsprechend unter:

/var/lib/.../taskmanager.db

Ergebnis: Die neuen Datensätze sind in der Datenbank im Docker-Volume vorhanden. DBeaver untersucht derzeit eine andere Datei. Die Ursache der unterschiedlichen Anzeigen ist damit geklärt; ein Datenverlust oder ein Fehler beim Speichern wurde nicht festgestellt. Der Datenbankzugriff über DBeaver auf die tatsächlich verwendete Datenbank ist noch nicht eingerichtet.

## Nächste Schritte

Als Nächstes wird die Datenbank aus dem laufenden Compose-Container exportiert und anschließend in DBeaver geöffnet. Dabei sollen die exportierten Daten mit der Datenbank im Container verglichen werden. Optional wird danach auch der direkte Lesezugriff auf die Datei im Docker-Volume untersucht.
Anschließend wird der Compose-Lifecycle und die Persistenz untersucht, insbesondere ob die Daten nach einem erneuten Erstellen des Containers erhalten bleiben. Die bestehende Compose-Konfiguration und das Volume 'taskmanager-data' bleiben bis dahin unverändert.