# Entwicklung der Benutzeroberfläche (UI) - Second Step

Damit die UI-Practicals nicht zu lang wird geht es an dieser Stelle weiter. Zunächst werden weitere Anpassungen vorgenommen, die auch schon zuvor durchgeführt wurden. Werden neue Schritte gemacht, wird auf diese tiefergehend und mit Kommentar im Code eingegangen.

## Beschreibung in Detailansicht integrieren 

Mit der Beschreibung wird die letzte Kategorie der Detailansicht integriert.

In der 'app.py'-Datei in der SQL-Abfrage für 'task-detail' in beiden SELECT-Abschnitten folgende Zeile einfügen:

```bash
tasks.description,
```

In 'task.html' folgenden Block nach ```bash <p>Status: {{ task["status"] }}</p>
    <p>Priorität: {{ task["priority"] }}</p> ``` einfügen:

```bash
{% if task["description"] != None %}
    <p>Beschreibung: {{ task["description"] }}</p>
    {% endif %}
```

Dann muss zusätzlich eine Beschreibung in DBeaver eingefügt werden, wenn noch nicht vorhanden, mit folgendem SQL-UPDATE:

```bash
UPDATE tasks
SET description = 'Auf keinen Fall vergessen!'
WHERE id = 4;
```

ID 4 ist die Aufgabe 'Linuxbefehlsübersicht erstellen', wenn diese angeklickt wird, erscheint im Browser folgende Detaiansicht:

Linuxbefehlsübersicht erstellen

Status: open

Priorität: 1

Beschreibung: Auf keinen Fall vergessen!

Deadline: 30.09.2026

← Zurück

## Übersetzung der Status- und Prioritäts-Werte in der Detailansicht

Damit auch in der Detailansicht die Ststus- und Prioritätswerte wie auf der Startseite übersetzt werden, muss der Status-Abschnitt ersetzt werden und der Prioritäts-Abschnitt eingefügt werden:

```bash
    <p>Status:
        {% if task["status"] == "open" %}
        Offen
        {% elif task["status"] == "in_progress" %}
        In Bearbeitung
        {% elif task["status"] == "completed" %}
        Erledigt
        {% endif %}
    </p>

    <p>Priorität:
        {% if task["priority"] == 1 %}
        Niedrig
        {% elif task["priority"] == 2 %}
        Mittel
        {% elif task["priority"] == 3 %}
        Hoch
        {% endif %}
    </p>
```

Detailansicht in Browser:

Linuxbefehlsübersicht erstellen

Status: Offen

Priorität: Niedrig

Beschreibung: Auf keinen Fall vergessen!

Deadline: 30.09.2026

← Zurück

Aktuelle Architektur:

          ┌──────────────┐
          │    SQLite    │
          └──────┬───────┘
                 │
            SQL-Abfragen
                 │
                 ▼
          ┌──────────────┐
          │ Python/Flask │
          └──────┬───────┘
                 │
            Jinja-Daten
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
index.html                 task.html
    │                         │
    └────────────┬────────────┘
                 ▼
              Browser

## Einstieg in CSS

CSS (Cascading Style Sheets) ist eine Stylesheet-Sprache, die das Aussehen und das Design von Webseiten bestimmt. HTML bestimmt den Inhalt und die Struktur einer Website, während CSS festlegt, wie dieser Inhalt aussieht (Farben, Schriftarten, Abstände und das Layout). 

Im Zuge der Beschäftigung mit CSS haben sich weitere Entscheidungen bezüglich des UI-Design-Konzept ergeben. Es wurde z.B. entschieden, das auf der Startseite nur die Kategorien Priorität, Status und Deadline der Aufgaben angezeigt werden und in der Detailansicht alle weiteren. Zudem wurde die Struktur übersichtlicher gestaltet. Darum werden zunächst die .html- und .py-Dateien entsprechend angepasst und dann wird mit CSS begonnen.

## Anpassung der 'index.html'-Datei

Für die Umsetzung des neuen UI-Konzepts müssen grundlegende strukturelle Änderungen an der 'index.html'-Datei vorgenommen werden. 
Diese sind dem folgenden Vorher-Nachher-Vergleich zu entnehmen:

'index.html' vorher:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Taskmanager</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body>
    <h1>{{ name }}</h1>
    <p>Willkommen bei unserem Taskmanager!</p>

    <ul>
        {% for task in tasks %}

        <li>
            <a href="/task/{{ task['id'] }}">{{ task['title'] }}</a>

            {% if task["name"] != None %}
            – Gruppe: {{ task["name"] }}
            {% endif %}

            – Status:
            {% if task["status"] == "open" %}
            Offen
            {% elif task["status"] == "in_progress" %}
            In Bearbeitung
            {% elif task["status"] == "completed" %}
            Erledigt
            {% endif %}

            – Priorität:
            {% if task["priority"] == 1 %}
            Niedrig
            {% elif task["priority"] == 2 %}
            Mittel
            {% elif task["priority"] == 3 %}
            Hoch
            {% endif %}

            {% if task["deadline"] != None %}
            – Deadline: {{ task["deadline"] }}
            {% endif %}

        </li>

        {% endfor %}
    </ul>
</body>

</html>
```

'index.html' nachher:

```bash
<!DOCTYPE html>
<html>

<head>

    # Seitentitel, der im Browser-Tab angezeigt wird
    <title>Taskmanager</title>   
    
    # Einbindung der externen CSS-Datei aus dem Flask-Static-Verzeichnis
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">   
     
</head>

<body>

    # Gibt den Namen des Taskmanagers aus. Die Variable 'name' wird von Flask/Jinja2 an das Template übergeben.
    <h1>{{ name }}</h1>

    # Begrüßungstext auf der Startseite
    <p>Willkommen bei unserem Taskmanager!</p>

    # Legt eine Jinja2-Namespace-Variable an. 'current_group.name' speichert den Namen der zuletzt ausgegebenen Gruppe. Dadurch kann später geprüft werden, ob eine neue Gruppe begonnen hat.
    {% set current_group = namespace(name=None) %}

    # Durchläuft alle Aufgaben, die von Flask an das Template übergeben wurden. Jede Aufgabe enthält unter anderem Titel, ID, Gruppe, Priorität, Status und gegebenenfalls eine Deadline.
    {% for task in tasks %}

        # Prüft, ob sich die Gruppe der aktuellen Aufgabe von der zuletzt verarbeiteten Gruppe unterscheidet.
        {% if task["name"] != current_group.name %}

            # Falls die Aufgabe einer Gruppe zugeordnet ist, wird eine Überschrift für diese neue Gruppe ausgegeben. Aufgaben ohne Gruppe erhalten keine Gruppenüberschrift.
            {% if task["name"] != None %}
                <h2 class="group">
                    ♦ {{ task["name"] }}
                </h2>
            {% endif %}

            # Speichert die aktuelle Gruppe als zuletzt verarbeitete Gruppe. Bei der nächsten Aufgabe wird dieser Wert für den Vergleich verwendet.
            {% set current_group.name = task["name"] %}

        {% endif %}

        # Container für eine einzelne Aufgabe. Wenn die Aufgabe zu einer Gruppe gehört, wird zusätzlich die CSS-Klasse 'grouped-task' gesetzt.
        <div class="task {% if task['name'] != None %}grouped-task{% endif %}">

            # Symbol zur visuellen Kennzeichnung der Aufgabe
            <span class="task-marker">♦</span>

            # Link zur Detailseite der jeweiligen Aufgabe. Die Aufgaben-ID wird dynamisch in die URL eingesetzt.
            <a href="/task/{{ task['id'] }}">{{ task['title'] }}</a>

            # Anzeige der Priorität der Aufgabe
            <span class="priority">

                # Priorität 1 = niedrig
                {% if task["priority"] == 1 %}
                    ● Niedrig

                # Priorität 2 = mittel
                {% elif task["priority"] == 2 %}
                    ● Mittel

                # Priorität 3 = hoch
                {% elif task["priority"] == 3 %}
                    ● Hoch
                {% endif %}

            </span>

            # Anzeige des aktuellen Bearbeitungsstatus
            <span class="status">

                # Aufgabe wurde noch nicht begonnen
                {% if task["status"] == "open" %}
                    ■ Offen

                # Aufgabe befindet sich aktuell in Bearbeitung
                {% elif task["status"] == "in_progress" %}
                    ■ In Bearbeitung

                # Aufgabe wurde abgeschlossen
                {% elif task["status"] == "completed" %}
                    ■ Erledigt
                {% endif %}

            </span>

            # Die Deadline wird nur angezeigt, wenn für die Aufgabe tatsächlich ein Datum hinterlegt wurde.
            {% if task["deadline"] != None %}
                <span class="deadline">
                    – Deadline: {{ task["deadline"] }}
                </span>
            {% endif %}

        </div>

    # Ende der Schleife über alle Aufgaben
    {% endfor %}

</body>

</html>
```

Ausgabe im Browser nach Änderung:

Taskmanager

Willkommen bei unserem Taskmanager!
♦ Docker
♦ Docker Compose Grundlagen ● Mittel ■ Offen
♦ Docker Tutorial Teil 1 ● Mittel ■ In Bearbeitung – Deadline: Freitag
♦ Docker Tutorial Teil 2 ● Hoch ■ Offen – Deadline: 2026-08-12 20:00
♦ Docker installieren ● Mittel ■ Erledigt
♦ Linuxbefehlsübersicht erstellen ● Niedrig ■ Offen – Deadline: 30.09.2026 

## Anpassung der 'task.html'-Datei

Auch in der 'task.html' müssen grundlegende strukturelle Änderungen vorgenommen werden. Diese sind dem folgenden Vorher-Nachher-Vergleich zu entnehmen:

'task.html' vorher:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Aufgabe</title>
</head>

<body>

    <h1>{{ task["title"] }}</h1>

    <p>Status:
        {% if task["status"] == "open" %}
        Offen
        {% elif task["status"] == "in_progress" %}
        In Bearbeitung
        {% elif task["status"] == "completed" %}
        Erledigt
        {% endif %}
    </p>

    <p>Priorität:
        {% if task["priority"] == 1 %}
        Niedrig
        {% elif task["priority"] == 2 %}
        Mittel
        {% elif task["priority"] == 3 %}
        Hoch
        {% endif %}
    </p>

    {% if task["description"] != None %}
    <p>Beschreibung: {{ task["description"] }}</p>
    {% endif %}

    {% if task["name"] != None %}
    <p>Gruppe: {{ task["name"] }}</p>
    {% endif %}

    {% if task["deadline"] != None %}
    <p>Deadline: {{ task["deadline"] }}</p>
    {% endif %}

    {% if task["depends_on_titles"] != None %}
    <p>Abhängig von: {{ task["depends_on_titles"] }}</p>
    {% endif %}

    {% if task["dependent_titles"] != None %}
    <p>Wird benötigt von: {{ task["dependent_titles"] }}</p>
    {% endif %}

    <p><a href="/">← Zurück</a></p>

</body>

</html>
```

'task.html' nachher:

```bash
<!DOCTYPE html>
<html>

<head>
    # Titel der Seite, der im Browser-Tab angezeigt wird.
    <title>Aufgabe</title>
</head>

<body>

    # Überschrift der Detailseite. Der Titel der Aufgabe wird aus der Datenbank geladen.
    <h1>
        ♦ {{ task["title"] }}
    </h1>

    # Priorität der Aufgabe anzeigen. Der Zahlenwert aus der Datenbank wird hier in einen verständlichen deutschen Text übersetzt: 1 = Niedrig, 2 = Mittel, 3 = Hoch
    <p>
        ●
        {% if task["priority"] == 1 %}
        Niedrig
        {% elif task["priority"] == 2 %}
        Mittel
        {% elif task["priority"] == 3 %}
        Hoch
        {% endif %}
    </p>

    # Status der Aufgabe anzeigen. Die gespeicherten englischen Statuswerte werden für die Benutzeroberfläche ins Deutsche übersetzt.
    <p>
        ■
        {% if task["status"] == "open" %}
        Offen
        {% elif task["status"] == "in_progress" %}
        In Bearbeitung
        {% elif task["status"] == "completed" %}
        Erledigt
        {% endif %}
    </p>

    # Die Deadline wird nur angezeigt, wenn tatsächlich ein Wert in der Datenbank vorhanden ist.
    {% if task["deadline"] != None %}
    <p>
        Deadline: {{ task["deadline"] }}
    </p>
    {% endif %}

    # Die Gruppe wird nur angezeigt, wenn die Aufgabe einer Gruppe zugeordnet ist.
    {% if task["name"] != None %}
    <p>
        Gruppe: {{ task["name"] }}
    </p>
    {% endif %}

    # Die Beschreibung wird nur angezeigt, wenn eine Beschreibung für die Aufgabe vorhanden ist.
    {% if task["description"] != None %}
    <p>
        Beschreibung: {{ task["description"] }}
    </p>
    {% endif %}

    # Zeigt die Aufgaben an, von denen die aktuelle Aufgabe abhängig ist.
    {% if task["depends_on_titles"] != None %}
    <p>
        Abhängig von: {{ task["depends_on_titles"] }}
    </p>
    {% endif %}

    # Zeigt die Aufgaben an, die von der aktuellen Aufgabe abhängig sind.
    {% if task["dependent_titles"] != None %}
    <p>
        Wird benötigt von: {{ task["dependent_titles"] }}
    </p>
    {% endif %}

    # Link zurück zur Startseite bzw. Aufgabenübersicht.
    <p>
        <a href="/">← Zurück</a>
    </p>

</body>

</html>
```

## Anpassung der 'app.py'-Datei

In 'app.py' müssen vor allem Änderungen an den SQL-Abfragen vorgenommen werden. 
Diese sind auch dem Vorher-Nachher-vergleich zu entnehmen:

'app.py' vorher:

```bash
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row
    
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name,

        GROUP_CONCAT(DISTINCT depends_on.title) AS depends_on_titles,
        GROUP_CONCAT(DISTINCT dependent.title) AS dependent_titles

    FROM tasks

    LEFT JOIN groups
        ON tasks.group_id = groups.id

    LEFT JOIN task_dependencies
        ON tasks.id = task_dependencies.task_id

    LEFT JOIN tasks AS depends_on
        ON task_dependencies.depends_on_task_id = depends_on.id

    LEFT JOIN task_dependencies AS reverse_dependencies
        ON tasks.id = reverse_dependencies.depends_on_task_id

    LEFT JOIN tasks AS dependent
        ON reverse_dependencies.task_id = dependent.id

    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name
    """)

    tasks = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        name="Taskmanager",
        tasks=tasks
    )

@app.route("/task/<int:task_id>")
def task_detail(task_id):
    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name,

        GROUP_CONCAT(DISTINCT depends_on.title) AS depends_on_titles,
        GROUP_CONCAT(DISTINCT dependent.title) AS dependent_titles

    FROM tasks

    LEFT JOIN groups
        ON tasks.group_id = groups.id

    LEFT JOIN task_dependencies
        ON tasks.id = task_dependencies.task_id

    LEFT JOIN tasks AS depends_on
        ON task_dependencies.depends_on_task_id = depends_on.id

    LEFT JOIN task_dependencies AS reverse_dependencies
        ON tasks.id = reverse_dependencies.depends_on_task_id

    LEFT JOIN tasks AS dependent
        ON reverse_dependencies.task_id = dependent.id

    WHERE tasks.id = ?

    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name
    """, (task_id,))

    task = cursor.fetchone()

    connection.close()

    return render_template(
    "task.html",
    name="Aufgabe",
    task=task
)
```

'app.py' nachher:

```bash
# SQLite wird für die Verbindung zur lokalen Datenbank verwendet.
import sqlite3

# Flask stellt die Webanwendung bereit. 'render_template' wird verwendet, um HTML-Dateien aus dem 'templates'-Ordner zu laden.
from flask import Flask, render_template


# Erstellt die Flask-Anwendung.
app = Flask(__name__)


# --------------------------------------------------
# Startseite / Übersicht aller Aufgaben
# --------------------------------------------------

@app.route("/")
def home():
    # Verbindung zur SQLite-Datenbank herstellen.
    connection = sqlite3.connect("taskmanager.db")

    # Die Ergebnisse der SQL-Abfrage können dadurch über den Spaltennamen angesprochen werden, z. B. 'task["title"]'.
    connection.row_factory = sqlite3.Row

    # Cursor erstellen, um SQL-Abfragen auszuführen.
    cursor = connection.cursor()

    # Alle Aufgaben mit ihren wichtigsten Informationen abrufen. Zusätzlich wird der Name der zugehörigen Gruppe geladen.
    cursor.execute("""
    SELECT
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name

    FROM tasks

    # LEFT JOIN sorgt dafür, dass auch Aufgaben ohne Gruppe angezeigt werden. In diesem Fall ist 'groups.name' NULL.
    LEFT JOIN groups
        ON tasks.group_id = groups.id

    # Die Ergebnisse werden anhand der Aufgabe und Gruppe gruppiert. Dadurch können die Ergebnisse eindeutig zusammengefasst werden.
    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name

    # Sortierung der Aufgaben: 1. Aufgaben mit einer Gruppe werden zuerst angezeigt. 2. Danach wird nach dem Gruppennamen sortiert. 3. Innerhalb einer Gruppe werden die Aufgaben alphabetisch nach ihrem Titel sortiert.
    ORDER BY
        groups.name IS NULL,
        groups.name,
        tasks.title
    """)

    # Alle gefundenen Aufgaben aus der Datenbank laden.
    tasks = cursor.fetchall()

    # Datenbankverbindung schließen, da sie nicht mehr benötigt wird.
    connection.close()

    # Die Startseite mit den geladenen Aufgaben rendern. 'tasks' wird an das HTML-Template übergeben und kann dort für die Darstellung der Aufgaben verwendet werden.
    return render_template(
        "index.html",
        name="Taskmanager",
        tasks=tasks
    )

# --------------------------------------------------
# Detailansicht einer einzelnen Aufgabe
# --------------------------------------------------

@app.route("/task/<int:task_id>")
def task_detail(task_id):

    # Verbindung zur SQLite-Datenbank herstellen.
    connection = sqlite3.connect("taskmanager.db")

    # Ergebnisse können über die Spaltennamen angesprochen werden.
    connection.row_factory = sqlite3.Row

    # Cursor zum Ausführen der SQL-Abfrage erstellen.
    cursor = connection.cursor()

    # Informationen zu einer bestimmten Aufgabe abrufen. Zusätzlich werden Gruppe und Abhängigkeiten der Aufgabe geladen.
    cursor.execute("""
    SELECT
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        tasks.description,
        groups.name,

        # 'GROUP_CONCAT' fasst mehrere abhängige Aufgaben zu einem einzelnen Text zusammen. 'DISTINCT' verhindert doppelte Einträge.
        GROUP_CONCAT(DISTINCT depends_on.title) AS depends_on_titles,

        # Hier werden Aufgaben gesammelt, die von der aktuellen Aufgabe abhängig sind.
        GROUP_CONCAT(DISTINCT dependent.title) AS dependent_titles

    FROM tasks

    # Die Gruppe der Aufgabe laden. Auch Aufgaben ohne Gruppe sollen angezeigt werden.
    LEFT JOIN groups
        ON tasks.group_id = groups.id

    # Verknüpfung zwischen Aufgaben und ihren Abhängigkeiten.
    LEFT JOIN task_dependencies
        ON tasks.id = task_dependencies.task_id

    # Die Aufgaben laden, von denen die aktuelle Aufgabe abhängig ist. 'tasks AS depends_on' gibt der tasks-Tabelle einen zusätzlichen Namen, damit sie in derselben Abfrage ein zweites Mal verwendet werden kann.
    LEFT JOIN tasks AS depends_on
        ON task_dependencies.depends_on_task_id = depends_on.id

    # Die Abhängigkeit wird hier in die entgegengesetzte Richtung betrachtet: Welche Aufgaben hängen von der aktuellen Aufgabe ab?
    LEFT JOIN task_dependencies AS reverse_dependencies
        ON tasks.id = reverse_dependencies.depends_on_task_id

    # Die tatsächlich abhängigen Aufgaben laden.
    LEFT JOIN tasks AS dependent
        ON reverse_dependencies.task_id = dependent.id

    # Es soll nur die Aufgabe mit der übergebenen ID geladen werden. Das '?' ist ein Platzhalter für task_id. Der Wert wird anschließend als Parameter übergeben.
    WHERE tasks.id = ?

    # Gruppierung der Ergebnisse, damit 'GROUP_CONCAT' die verschiedenen Abhängigkeiten korrekt zusammenfassen kann.
    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        tasks.description,
        groups.name
    """, (task_id,))

    # Die erste gefundene Aufgabe aus der Datenbank laden. Da 'task_id' eindeutig ist, wird normalerweise genau eine Aufgabe zurückgegeben.
    task = cursor.fetchone()

    # Datenbankverbindung schließen.
    connection.close()

    # Detailseite der Aufgabe rendern und die geladene Aufgabe an das HTML-Template übergeben.
    return render_template(
        "task.html",
        name="Aufgabe",
        task=task
    )
```