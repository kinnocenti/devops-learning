# Datenbankeinbindung

In diesem Abschnitt wird die Einbindung der Datenbank Schritt für Schritt durchlaufen. Damit wird die Brücke zwischen Datenbank und Webanwendung geschlagen. Die Aufgaben werden nicht mehr aus einer Python-Liste geladen, sondern per SQL aus SQLite abgefragt, von Flask verarbeitet und anschließend über Jinja im Browser dargestellt. Dabei lernen wir auch, wie auf einzelne Werte eines Datenbankdatensatzes zugriffen werden kann.

## SELECT-Abfrage und Ergebnis in Python einbinden

Folgenden Ablauf ist das Ziel:

          SQL (SELECT)
Python ─────────────────► SQLite
                             │
                             │ Ergebnis
                             ▼
Python ◄──────────────── cursor.fetchall()

Zum besseren Verständnis wird zunächst eine Testdatei erstellt, um das Abfragen der Daten aus der Datenbank zu verdeutlichen.

Im Ordner 'taskmanager' die Datei 'databasetest.py' erstellen und folgenden Code einfügen:

```bash
import sqlite3   # importiert das Python-Modul sqlite3

connection = sqlite3.connect("taskmanager.db")   # in der Variable 'connection' wird nach Ausführung des Moduls das erzeugte Verbindungs-Objekt abgespeichert

cursor = connection.cursor()   # Cursor holen, das aufgerufene Cursor-Objekt wird in der Variable 'cursor' abgespeichert

cursor.execute("SELECT * FROM tasks")   # Abfrage 'SELECT * FROM tasks' ausführen

tasks = cursor.fetchall()   # 'fetchall()' holt alle Ergebniszeilen der Abfrage vom Cursor, liefert sie an Python zurück und speichert sie in 'tasks'

print(tasks)   # Inhalt von 'tasks' im Terminal ausgeben

connection.close()   # bestehende Verbindung zur Datenbank wird geschlossen
```

Der Cursor ist eine Schnittstelle, über die Python SQL-Anweisungen an die Datenbank senden und Ergebnisse dieser Abfragen abrufen kann.

Im Terminal in den Ordner 'taskmanager' wechseln, die .venv aufrufen und den Code ausführen:

```bash
cd ~/>Pfad</taskmanager   # in den Ordner 'taskmanager' wechseln

source .venv/bin/activate   # die virtuelle Umgebung aufrufen

python databasetest.py   # den Code aus 'databasetest.py' ausführen
```

Da die Testdaten momentan aus fünf Aufgaben bestehen, wurden entsprechend fünf Tupel mit jeweils dem Inhalt aller Spalten der Tabelle 'task' aus der Datenbank abgefragt. 

Ausgabe (die Tupel stehen jeweils in den ()-Klammern):

[(1, 'Docker installieren', None, 'completed', 2, None, 1), (2, 'Docker Tutorial Teil 1', None, 'in_progress', 2, None, 1), (3, 'Docker Tutorial Teil 2', None, 'open', 3, '2026-08-12 20:00', 1), (4, 'Linuxbefehlsübersicht erstellen', None, 'open', 1, None, None), (5, 'Docker Compose Grundlagen', None, 'open', 2, None, 1)]

Hinweis: Die Connection ist die Verbindung zur Datenbank und der Cursor ist das Werkzeug, das über diese Verbindung für SQL-Abfragen verwendet wird.

Detaillierter Ablauf:

Python
  │
  │ cursor.execute()
  │
  │ "SELECT * FROM tasks"
  ▼
Cursor
  │
  │ über Connection
  ▼
SQLite
  │
  │ führt SELECT aus
  ▼
tasks-Tabelle
  │
  │ Ergebnis
  ▼
Cursor
  │
  │ fetchall()
  ▼
Python

## Von print() zu Flask und Jinja

In diesem Kapitel wird der Code aus 'databasetest.py' in die 'app.py'-Datei integriert. Damit wird die Datenbank eingebunden. Zudem wird die Python-Liste gelöscht, da die Daten aus der Datenbank abgefragt und nicht mehr hartkodiert werden. Im nächsten Schritt wird die index.htlml angepasst. 

Vorher ohne Flask:

SQLite
   ↓
SELECT
   ↓
Python
   ↓
tasks
   ↓
print()
   ↓
Terminal

Code der 'databasetest.py'-Datei wird in die Datei 'app.py' integriert.

Nach der Code-Integration:

SQLite
   ↓
SELECT
   ↓
Python
   ↓
tasks
   ↓
render_template()
   ↓
Jinja
   ↓
HTML
   ↓
Browser

In die 'app.py'-Datei wird wie folgt geändert:

```bash
import sqlite3   # sqlite3 wird importiert
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    connection = sqlite3.connect("taskmanager.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        name="Taskmanager",
        tasks=tasks
    )
```

Hinweis: Jetzt muss im Terminal in .venv ```bash flask --app app run ``` eingegeben werden, um den Code auszuführen und dann http://127.0.0.1:5000/ im Browser eingeben.

Ausgabe im Browser:

Taskmanager

Willkommen bei unserem Taskmanager!

    (1, 'Docker installieren', None, 'completed', 2, None, 1)
    (2, 'Docker Tutorial Teil 1', None, 'in_progress', 2, None, 1)
    (3, 'Docker Tutorial Teil 2', None, 'open', 3, '2026-08-12 20:00', 1)
    (4, 'Linuxbefehlsübersicht erstellen', None, 'open', 1, None, None)
    (5, 'Docker Compose Grundlagen', None, 'open', 2, None, 1)

Der Datenfluss nach der Änderung:

SQLite
   │
   │ SELECT * FROM tasks
   ▼
Cursor
   │
   │ fetchall()
   ▼
Python
   │
   │ tasks
   ▼
Flask
   │
   │ render_template()
   ▼
Jinja
   │
   │ for task in tasks
   ▼
HTML
   │
   ▼
Browser

## Wert aus einer Spalte ausgeben

Damit nur ein Wert aus einer Spalte im Tupel ausgegeben wird, muss entsprechend eine Eingrenzung der Ausgabewerte in der 'index.html'-Datei vorgenommen werden. Dazu wird bei der Variable 'task' der index [1] angehängt. Damit wird aus jedem Tupel nur der Wert von Position 1 ausgegeben.

Dafür muss in der Datei 'index.html' folgende Zeile geändert werden:

Voher:

```bash
    <li>{{ task }}</li>
```

Nachher:

```bash
    <li>{{ task[1] }}</li>   # Index [1] wird eingefügt
```

Ausgabe im Browser:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren
    Docker Tutorial Teil 1
    Docker Tutorial Teil 2
    Linuxbefehlsübersicht erstellen
    Docker Compose Grundlagen

Struktureller Vergleich der Ausgaben mit und ohne Index:

                 komplette Daten
                       │
                       ▼
SQLite ──→ Python ──→ tasks
                       │
                       ▼
                    Jinja
                       │
             ┌─────────┴─────────┐
             │                   │
        {{ task }}        {{ task[1] }}
             │                   │
             ▼                   ▼
      komplettes Tupel        nur Titel

## Vom Index [1] zur sqlite3.Row

Da die Verwendung von Indizes zu Problemen führen kann, wird das Zeilenformat 'sqlite3.Row' für die Ausgabe der Tupel verwendet. Dafür wird die Eigenschaft 'row_factory' bei dem Verbindungsobjekt 'connection' desetzt. 'sqlite3.Row' ist ein von Python bereitgestellter Typ für Datenbankzeilen, der es ermöglicht, die Werte über die Spaltennamen anzusprechen.
Zusammengefasst, 'row_factory' legt fest, wie SQLite die zurückgegebenen Datenbankzeilen in Python darstellen bzw. zugreifbar machen soll. Mit sqlite3.Row erhält man Zeilen, auf deren Spalten sowohl über Indizes als auch über Spaltennamen zugriffen werde kann.

In der Datei 'app.py' muss entsprechend eine Zeile hinzugefügt werden:

Vorher:

```bash
    connection = sqlite3.connect("taskmanager.db")
    cursor = connection.cursor()
```

Nachher:

```bash
    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row   # diese Zeile hinzufügen, bei dem Objekt 'connection' wird die Eigenschaft 'row_factory' gesetzt und das Zeilenformat 'sqlite3.Row' verwendet

    cursor = connection.cursor()
```

Die folgende Zeile der 'index.html'-Datei muss ebenfalls angepasst werden:

Vorher:

```bash
    <li>{{ task[1] }}</li>
```

Nachher:

```bash
    <li>{{ task["title"] }}</li>
```

Damit ist beim zukünftigen Lesen des Codes direkt ersichtlich welche Spalte/n abgerufen wird/werden. Mit einem Index müsste bekannt sein, welcher Spaltenname für die Zahl steht.

Ablauf mit 'sqlite3.Row':

SQLite-Ergebnis
      ↓
Connection
      ↓
row_factory
      ↓
sqlite3.Row
      ↓
Python bekommt benannte Zeilen

So können mehrere Spalten abgerufen werden:

```bash
<li>
    {{ task["title"] }} – {{ task["status"] }}
</li>
```

Ausgabe:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – completed
    Docker Tutorial Teil 1 – in_progress
    Docker Tutorial Teil 2 – open
    Linuxbefehlsübersicht erstellen – open
    Docker Compose Grundlagen – open

Es wird also nicht nur die Aufgabe, sondern auch der Status angezeigt.

Wie oben zu sehen, wurde ein Bindestrich der Browserausgabe hinzugefügt. Das kann zB. auch für Beschriftungen genutzt werden: 

```bash
<li>
    {{ task["title"] }}
    – Status: {{ task["status"] }}
    – Priorität: {{ task["priority"] }}
</li>
```

Ausgabe:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Status: completed – Priorität: 2
    Docker Tutorial Teil 1 – Status: in_progress – Priorität: 2
    Docker Tutorial Teil 2 – Status: open – Priorität: 3
    Linuxbefehlsübersicht erstellen – Status: open – Priorität: 1
    Docker Compose Grundlagen – Status: open – Priorität: 2

Weg vom Speichern bis zum Anzeigen:

┌─────────────────────┐
│ SQLite-Datenbank    │
│                     │
│ tasks               │
│ id                  │
│ title               │
│ status              │
│ priority            │
│ deadline            │
│ group_id            │
└──────────┬──────────┘
           │
           │ SELECT
           ▼
┌─────────────────────┐
│ Python / sqlite3    │
│                     │
│ connection          │
│ cursor              │
│ execute()           │
│ fetchall()          │
└──────────┬──────────┘
           │
           │ sqlite3.Row
           ▼
┌─────────────────────┐
│ Flask               │
│                     │
│ render_template()   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Jinja               │
│                     │
│ task["title"]       │
│ task["status"]      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ HTML                │
│                     │
│ <li>...</li>        │
└──────────┬──────────┘
           │
           ▼
        Browser