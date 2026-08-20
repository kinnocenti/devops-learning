# SQL-Kram

Bisher wurde nur mit den Daten aus der Tabelle 'tasks' gearbeitet. Damit Daten auch aus 'groups' genutzt werden können, muss natürlich die SQL-Abfrage in der 'app.py'-Datei angepasst werden. Zudem folgen natürlich auch Änderungen in der Datei 'index.html'.

## Mit JOIN auch Gruppennamen im Browser ausgeben 

In der Browserausgabe sollen als nächstes auch die Gruppennamen angezeigt werden. Dafür wird die SQL-Abfrage ```bash SELECT * FROM tasks;``` in 'app.py' mit einem LEFT JOIN erweitert.  

Die SQL-Abfrage in der 'app.py'-Datei muss durch folgende SQL-Abfrage mit JOIN ersetz werden:

```bash
    cursor.execute("""
    SELECT
        tasks.*,
        groups.name
    FROM tasks
    LEFT JOIN groups
        ON tasks.group_id = groups.id
    """)
```

In index.html' müssen unter der Codezeile ```bash {{ task["title"] }} ``` folgende Zeile hinzufügen werden:

```bash 
        – Gruppe:
        {% if task["name"] == None %}
        /
        {% else %}
        {{ task["name"] }}
        {% endif %}
```

Browserausgabe:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Gruppe: Docker – Status: Erledigt – Priorität: Mittel – Deadline: /
    Docker Tutorial Teil 1 – Gruppe: Docker – Status: In Bearbeitung – Priorität: Mittel – Deadline: Freitag
    Docker Tutorial Teil 2 – Gruppe: Docker – Status: Offen – Priorität: Hoch – Deadline: 2026-08-12 20:00
    Linuxbefehlsübersicht erstellen – Gruppe: / – Status: Offen – Priorität: Niedrig – Deadline: 30.09.2026
    Docker Compose Grundlagen – Gruppe: Docker – Status: Offen – Priorität: Mittel – Deadline: /

Hinweis: Für eine bessere Leserlichkeit wurde bei Nichteingabe als Platzhalter '/', statt '–' gesetzt.

## Gezielt Spalten auch in 'tasks' abfragen

Zuvor wurde mit dem '*' in der Tabelle 'tasks' alle Spalten abgefragt. In der Ausgabe im Browser werden aber nur ausgewählte angezeigt, um dies zu optimieren, werden die Spalten mit der SQL-Abfrage abgefragt, die benötigt werden. Hier gilt der Grundsatz: So viele Daten wie nötig, so wenige Daten, wie möglich.

Darum muss die SQL-ABfrage in 'app.py' entsprechend angepast werden:

```bash
    cursor.execute("""
    SELECT
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name
    FROM tasks
    LEFT JOIN groups
        ON tasks.group_id = groups.id
    """)
```

Die Browserausgabe ändert sich damit nicht im Vergleich zur vorherigen Ausgabe mit '*' in der SQL-Abfrage.

## Abhängigkeiten der Aufgaben integrieren und anpassen

Jetzt wird ein großer Sprung in der SQL-Abfrage gemacht. Grundlegendes wurde bereits erklärt und kleinschrittig geändert. Bei der Abfrage nach den Abhängigkeiten der Aufgaben wird die SQL-Abfrage entsprechend umfangreicher angepasst. Zum besseren Verständnis wurden umfangreiche Kommentare hinzugefügt.

In der 'app.py'-Datei die SQL-Abfrage entsprechend ändern:

```bash
    cursor.execute("""
    SELECT
        # Benötigte Spalten aus der Tabelle tasks
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,

        # Gruppenname aus der Tabelle groups
        groups.name,

    # Ermittelt die Aufgaben, von denen der aktuelle Task abhängt.
    # GROUP_CONCAT fasst mehrere Treffer zu einem Ergebnis zusammen.
    # Der Alias erzeugt im Ergebnis der Abfrage die Spalte
    # "depends_on_titles".
    GROUP_CONCAT(DISTINCT depends_on.title) AS depends_on_titles,

    # Ermittelt die Aufgaben, die von dem aktuellen Task abhängen.
    # Der Alias erzeugt im Ergebnis die Spalte "dependent_titles".
    GROUP_CONCAT(DISTINCT dependent.title) AS dependent_titles

    FROM tasks

    # Verknüpft die Tasks mit ihrer Gruppe.
    LEFT JOIN groups
        ON tasks.group_id = groups.id

    # Verknüpft die Tasks mit der Zwischentabelle,
    # in der die Abhängigkeiten zwischen Tasks gespeichert sind.
    LEFT JOIN task_dependencies
        ON tasks.id = task_dependencies.task_id

    # Zweite Verwendung der Tabelle tasks.
    # "depends_on" ist ein Alias und steht hier für die Aufgabe,
    # von der der aktuelle Task abhängt.
    LEFT JOIN tasks AS depends_on
        ON task_dependencies.depends_on_task_id = depends_on.id

    # Zweite Verwendung der Zwischentabelle für die umgekehrte Richtung.
    # Dadurch können auch die Tasks ermittelt werden,
    # die von dem aktuellen Task abhängen.
    LEFT JOIN task_dependencies AS reverse_dependencies
        ON tasks.id = reverse_dependencies.depends_on_task_id

    # "dependent" ist ein Alias für die zweite Verwendung von tasks.
    # Hier werden die Aufgaben ermittelt, die vom aktuellen Task abhängen.
    LEFT JOIN tasks AS dependent
        ON reverse_dependencies.task_id = dependent.id

    # GROUP_CONCAT benötigt eine Gruppierung der Ergebniszeilen.
    # Die übrigen ausgewählten Spalten werden deshalb ebenfalls angegeben.
    GROUP BY
        tasks.id,
        tasks.title,
        tasks.status,
        tasks.priority,
        tasks.deadline,
        groups.name
    """)
```

Hinweis: depends_on_titles → Von welchen Aufgaben hängt dieser Task ab?
dependent_titles → Welche Aufgaben hängen von diesem Task ab?

Entsprechend müssen auch Anpassungen in der 'index.html'-Datei vorgenommen werden. Dafür werden folgende Codezeilen unter die if-Anweisung von Deadline eingefügt:

```bash
        – Abhängig von:
        {{ task["depends_on_titles"] }}

        – Wird benötigt von:
        {{ task["dependent_titles"] }}
```

Browserausgabe:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Gruppe: Docker – Status: Erledigt – Priorität: Mittel – Deadline: / – Abhängig von: None – Wird benötigt von: None
    Docker Tutorial Teil 1 – Gruppe: Docker – Status: In Bearbeitung – Priorität: Mittel – Deadline: Freitag – Abhängig von: None – Wird benötigt von: Docker Tutorial Teil 2,Docker Compose Grundlagen
    Docker Tutorial Teil 2 – Gruppe: Docker – Status: Offen – Priorität: Hoch – Deadline: 2026-08-12 20:00 – Abhängig von: Docker Tutorial Teil 1 – Wird benötigt von: Docker Compose Grundlagen
    Linuxbefehlsübersicht erstellen – Gruppe: / – Status: Offen – Priorität: Niedrig – Deadline: 30.09.2026 – Abhängig von: None – Wird benötigt von: None
    Docker Compose Grundlagen – Gruppe: Docker – Status: Offen – Priorität: Mittel – Deadline: / – Abhängig von: Docker Tutorial Teil 1,Docker Tutorial Teil 2 – Wird benötigt von: None

Das Ganze ist noch sehr unübersichtlich und wird im nächsten Schritt angepasst, aber die Abhängikeiten der Aufgaben werden wie gewünscht angezeigt.

Anhand dieser Anpassung ist folgend der Ablauf aufgezeigt:

task_dependencies
        ↓
    SQL JOINs
        ↓
  GROUP_CONCAT()
        ↓
 depends_on_titles
 dependent_titles
        ↓
Python / sqlite3.Row
        ↓
      Jinja
        ↓
     Browser

## Weitere Anpassungend er Darstellung

Es wurde eine weitere Designentscheidung getroffen. Bisher wurde ein '>Bezeichnung<: /' angezeigt wenn nichts eingetragen wurde. Das ist zu unübersichtlich und unnötig. Darum soll nichts mehr angezeigt werden, wenn User nichts eintragen. Wird z.B. keine Deadline eingetragen, dann wird Deadline auch nicht angezeigt. Dementsprechend wird im Folgenden der Code angepasst. Der viele Änderungen vorgenommen werden, wird der ganze Code eingefügt.

Die Änderungen in der 'index.html'-Datei wurden im folgenden Code mit Kommentaren hervorgehoben. Da die Änderungen immer dem selben Muster folgen, wird die erste Änderung erklärt und auf die weiteren Änderungen nur hingewiesen.

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Taskmanager</title>
</head>

<body>
    <h1>{{ name }}</h1>
    <p>Willkommen bei unserem Taskmanager!</p>
</body>

<ul>
    {% for task in tasks %}
    <li>
        {{ task["title"] }}

        {% if task["name"] != None %}   # wenn Gruppenname nicht vorhanden ist, also None ist, zeige überhaupt nichts an
        – Gruppe: {{ task["name"] }}   # Gruppe ist vorhanden, zeige – Gruppe: >Gruppenname< an
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

        {% if task["deadline"] != None %}   # Hier auch anpassen
        – Deadline: {{ task["deadline"] }}
        {% endif %}   

        {% if task["depends_on_titles"] != None %}   # Hier auch anpassen
        – Abhängig von: {{ task["depends_on_titles"] }}
        {% endif %}

        {% if task["dependent_titles"] != None %}   # Hier auch anpassen
        – Wird benötigt von: {{ task["dependent_titles"] }}
        {% endif %}
    </li>
    {% endfor %}
</ul>

</html>
```

Browserausgabe:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Gruppe: Docker – Status: Erledigt – Priorität: Mittel
    Docker Tutorial Teil 1 – Gruppe: Docker – Status: In Bearbeitung – Priorität: Mittel – Deadline: Freitag – Wird benötigt von: Docker Tutorial Teil 2,Docker Compose Grundlagen
    Docker Tutorial Teil 2 – Gruppe: Docker – Status: Offen – Priorität: Hoch – Deadline: 2026-08-12 20:00 – Abhängig von: Docker Tutorial Teil 1 – Wird benötigt von: Docker Compose Grundlagen
    Linuxbefehlsübersicht erstellen – Status: Offen – Priorität: Niedrig – Deadline: 30.09.2026
    Docker Compose Grundlagen – Gruppe: Docker – Status: Offen – Priorität: Mittel – Abhängig von: Docker Tutorial Teil 1,Docker Tutorial Teil 2

Im nächsten Schritt soll die Benutzeroberfläche weiter geplant und umgesetzt werden. Darum wird die 'index.html'-Datei zuvor "aufgeräumt":

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
            {{ task["title"] }}

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

Browserausgabe:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Gruppe: Docker – Status: Erledigt – Priorität: Mittel
    Docker Tutorial Teil 1 – Gruppe: Docker – Status: In Bearbeitung – Priorität: Mittel – Deadline: Freitag – Wird benötigt von: Docker Tutorial Teil 2,Docker Compose Grundlagen
    Docker Tutorial Teil 2 – Gruppe: Docker – Status: Offen – Priorität: Hoch – Deadline: 2026-08-12 20:00 – Abhängig von: Docker Tutorial Teil 1 – Wird benötigt von: Docker Compose Grundlagen
    Linuxbefehlsübersicht erstellen – Status: Offen – Priorität: Niedrig – Deadline: 30.09.2026
    Docker Compose Grundlagen – Gruppe: Docker – Status: Offen – Priorität: Mittel – Abhängig von: Docker Tutorial Teil 1,Docker Tutorial Teil 2

Zum Schluss der bisher erarbeitete Gesamtablauf:

SQLite
  ↓
task_dependencies / groups / tasks
  ↓
SQL mit JOINs + GROUP_CONCAT()
  ↓
Ergebnis-Spalten
  ↓
Python / sqlite3.Row
  ↓
Jinja
  ↓
bedingte Darstellung
  ↓
HTML-Liste
  ↓
Browser