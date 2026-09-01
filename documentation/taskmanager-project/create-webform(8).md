# Erstellung der Eingabemasken

Für die Erstellung von Aufgaben und Gruppen wird eine Eingabemaske benötigt. 

## HTML-Dateien erstellen

Da es eine Eingabemaske für Aufgabenerstellung und eine für Gruppenerstellung geben soll, müssen entsprechend zwei HTML-Dateien erstellt werden. 
Im Ordner 'templates' die Dateien 'create_task.html' und 'create_group.html' anlegen.

Folgenden Code in 'create_group.html' einfügen:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Gruppe erstellen</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body class="task-detail">

    <h1>♦ Gruppe erstellen</h1>

    <form method="post">

        <p>
            <label for="name">Gruppenname:</label>
            <input type="text" id="name" name="name" required>
        </p>

        <p>
            <button type="submit">Gruppe erstellen</button>
        </p>

    </form>

    <p>
        <a href="/">← Zurück</a>
    </p>

</body>

</html>
```

Folgenden Code in 'create_task.html' einfügen:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Aufgabe erstellen</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body class="task-detail">

    <h1>♦ Aufgabe erstellen</h1>

    <form method="post">

        <p>
            <label for="title">Titel:</label>
            <input type="text" id="title" name="title" required>
        </p>

        <p>
            <label for="description">Beschreibung:</label>
            <textarea id="description" name="description"></textarea>
        </p>

        <p>
            <label for="priority">Priorität:</label>
            <select id="priority" name="priority">
                <option value="1">Niedrig</option>
                <option value="2" selected>Mittel</option>
                <option value="3">Hoch</option>
            </select>
        </p>

        <p>
            <label for="status">Status:</label>
            <select id="status" name="status">
                <option value="open">Offen</option>
                <option value="in_progress">In Bearbeitung</option>
                <option value="completed">Erledigt</option>
            </select>
        </p>

        <p>
            <label for="deadline">Deadline:</label>
            <textarea id="deadline" name="deadline"></textarea>
        </p>

        <p>
            <label for="group_id">Gruppe:</label>
            <select id="group_id" name="group_id">
                <option value="">Keine Gruppe</option>

                {% for group in groups %}
                <option value="{{ group['id'] }}">{{ group['name'] }}</option>
                {% endfor %}

            </select>
        </p>

        <p>
            <button type="submit">Aufgabe erstellen</button>
        </p>

    </form>

    <p>
        <a href="/">← Zurück</a>
    </p>

</body>

</html>
```

Damit sind zunächst nur die Formulare erstellt. Die Formulare können aber noch nichts speichern, dafür braucht es Flask-Routes. Diese müssen in 'app.py' eingefügt werden.

## Anpassungen in 'app.py' und 'index.html'

Die beiden folgenden Flask-Routen unter dem bestehenden Code in 'app.py' einfügen:

Flask-Route für die Gruppenerstellung:

```bash
@app.route("/create-group", methods=["GET", "POST"])
def create_group():

    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]

        cursor.execute(
            """
            INSERT INTO groups (name)
            VALUES (?)
            """,
            (name,)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    connection.close()

    return render_template(
        "create_group.html"
    )
```

Flask-Route für die Aufgabenerstellung:

```bash
@app.route("/create-task", methods=["GET", "POST"])
def create_task():

    connection = sqlite3.connect("taskmanager.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]
        deadline = request.form["deadline"]
        group_id = request.form["group_id"]

        if group_id == "":
            group_id = None

        cursor.execute(
            """
            INSERT INTO tasks (
                title,
                description,
                priority,
                status,
                deadline,
                group_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                description,
                priority,
                status,
                deadline,
                group_id
            )
        )

        connection.commit()
        connection.close()

        return redirect("/")

    cursor.execute(
        """
        SELECT id, name
        FROM groups
        ORDER BY name
        """
    )

    groups = cursor.fetchall()

    connection.close()

    return render_template(
        "create_task.html",
        groups=groups
    )
```

Hinweis: Oben in 'app.py' müssen die benötigten Flask-Funktionen importiert werden. Entsprechend müssen 'request' und 'redirect' hinzugefügt werden. 
Dafür muss die folgende Zeile in 'app.py':

```bash 
from flask import Flask, render_template 
```

geändert werden in:

```bash 
from flask import Flask, render_template, request, redirect 
```

In index.html direkt unter dem Willkommenssatz ```bash <p>Willkommen bei unserem Taskmanager!</p> ``` folgendes einfügen:

```bash
<p>
    <a href="/create-task">Aufgabe erstellen</a>   # Link 'Aufgabe erstellen' einfügen
    |
    <a href="/create-group">Gruppe erstellen</a>   # Link 'Gruppe erstellen' einfügen
</p>
```