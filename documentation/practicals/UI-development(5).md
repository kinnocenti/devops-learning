# Entwicklung der Benutzeroberfläche (UI)

In diesem Abschnitt wird die UI weiter geplant und entwickelt. Links werden integriert, APIs angebunden, usw.

## Link erstellen

In der UI soll es natürlich auch Links geben. Diese werden in diesem Kapitel erstellt und erklärt.

In 'app.py' wird in die SQL-Abfrage die Spalte 'id' aus der Tabelle 'tasks' eingefügt:

```bash
    SELECT
        tasks.id,
```

In 'index.html' muss eine Zeile geändert werden:

Vorher:

```bash
            {{ task["title"] }}
```

Nachher:

```bash
            <a href="/task/{{ task['id'] }}">{{ task['title'] }}</a>
```

Hinweis: Die Anführungsstriche in den []-Klammern geändert werden müssen, damit es keine Kollision mit "-Anführungsstrichen von 'href' gibt.

Nach den beiden Änderungen werden die Aufgabentitel im Browser als Link angezeigt. Wenn sie angeklickt werden zeigen sie noch den Fehler 404 an, aber der wird im nächsten Schritt behoben.

Damit vom Browser aus der "Rückweg" gefunden werden kann muss eine weitere Flask-Route gesetzt werden. Darum muss unten nach dem Ende des Codes eine weitere Route in 'app.py' einfügt werden:

```bash
@app.route("/task/<int:task_id>")
def task_detail(task_id):
    return f"Task-ID: {task_id}"
```

Wenn man im Browserausgabe auf 'Docker Tutorial Teil 2' klickt, wird eine neue Seite mit folgender Ausgabe angezeigt: Task-ID: 3. Die Route funktioniert also. 

Damit liegt folgende Ablauf vor:

Browser
   │
   │ Klick auf "Docker Tutorial Teil 2"
   ↓
HTML/Jinja
   │
   │ erzeugt:
   │ /task/3
   ↓
Flask Routing
   │
   │ erkennt:
   │ <int:task_id>
   ↓
Python
   │
   │ task_id = 3
   ↓
return f"Task-ID: {task_id}"
   ↓
Browser
   │
   ↓
Task-ID: 3

## Link erweitern

Wenn der Link angeklickt wird, soll nicht nur die ID, sondern auch der Titel der Aufgabe angezeigt werden. Anhand dieses Schrittes wird das Vorgehen aufgezeigt. Im Anschluss werden dann alle notwendigen Daten mit hinzugefügt. 

Eine neue Datei mit der Bezeichnung 'task.html' unter ~/taskmanager/templates erstellen. Und folgenden Code einfügen:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Aufgabe</title>   # die Bezeichnung, die oben im Tab steht
</head>

<body>
    <h1>{{ task["title"] }}</h1>   # Aufgabentitel wird abgerufen

    <p>Task-ID: {{ task["id"] }}</p>   # ID der Aufgabe wird abgerufen
</body>

</html>
```

In 'app.py' zum Schluss folgende Zeile ersetzten:

Vorher:

```bash
return f"Task-ID: {task_id}"
```

Nachher:

```bash
return render_template(
    "task.html",
    name="Aufgabe",
    task=task
)
```

Im Brower steht oben im Tab entsprechend Aufgabe und im Browser erscheint folgende Ausgabe:

Docker Tutorial Teil 2

Task-ID: 3

Es wird also wie gewünscht der Titel der Aufgabe angezeigt und darunter die ID dieser.

Damit ergibt sich der folgende Ablauf:

Browser
   ↓
Klick auf "Docker Tutorial Teil 2"
   ↓
/task/3
   ↓
Flask
   ↓
task_id = 3
   ↓
SQL: WHERE tasks.id = ?
   ↓
SQLite
   ↓
fetchone()
   ↓
task
   ↓
render_template("task.html", task=task)
   ↓
Jinja
   ↓
HTML
   ↓
Browser

Damit für den abschlie0ßenden Schritt die weiteren Daten auch angezeigt werden, muss der Code in 'task.html' entsprechend geändert werden. Die Syntax ist aus der 'index.html' bekannt, hier der gesamte Code:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Aufgabe</title>
</head>

<body>

    <h1>{{ task["title"] }}</h1>

    <p>Status: {{ task["status"] }}</p>
    <p>Priorität: {{ task["priority"] }}</p>

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

Ablauf:

Übersicht
   ↓
Task anklicken
   ↓
/task/3
   ↓
Flask erkennt die ID
   ↓
SQL sucht genau diesen Task
   ↓
fetchone()
   ↓
Python übergibt task an Jinja
   ↓
task.html
   ↓
Browser zeigt die Details
   ↓
← Zurück
   ↓
Übersicht

Damit der aktuelle Stand der anderen beiden Dateien:

Die 'index.html'-Datei:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Taskmanager</title>
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

            {% if task["depends_on_titles"] != None %}
            – Abhängig von: {{ task["depends_on_titles"] }}
            {% endif %}

            {% if task["dependent_titles"] != None %}
            – Wird benötigt von: {{ task["dependent_titles"] }}
            {% endif %}

        </li>

        {% endfor %}
    </ul>
</body>

</html>
```

Die 'app.py'-Datei:

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