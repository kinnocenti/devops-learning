# CSS

CSS (Cascading Style Sheets) ist eine Stylesheet-Sprache, die das Aussehen und das Design von Webseiten bestimmt. HTML bestimmt den Inhalt und die Struktur einer Website, während CSS festlegt, wie dieser Inhalt aussieht (Farben, Schriftarten, Abstände und das Layout). 

## Erste Schritte mit CSS

Die ersten Schritte mit CSS befassen sich mit der Anpassung der Abstände, der Schriftgröße und den Farben verschiedener Elemente. So wird mit den CSS die Browserausgabe übersichtlicher, strukturierter und userfreundlicher. 

## Erstellung der CSS-Struktur im Repository

Damit Klassen aus HTML in CSS aufgerufen werden können, müssen diese in HTML definiert werden. Dafür muss in 'index.html' und 'task.html' jeweils der Start-Tag '<body>' geändert werden.

In 'index.html' ```bash <body class="home"> ``` und in 'task.html' ```bash <body class="task-detail"> ``` anstelle von '<body>' einfügen.

Im Ordner 'taskmanger' den Ordner 'static' anlegen und darin die Datei 'style.css' und folgenden Code einfügen:

```bash
body {
    margin: 0;   # Der Außenrand des Browserfensters wird auf 0 gesetzt
    font-family: "Liberation Mono", monospace;   # Schriftart wird festgelegt
    color: #d6d6d6;   # Farbe der Schriftart
}

.home {
    background-color: #2b2b2b;   # Hintergrundfarbe der Startseite
}

.task-detail {
    background-color: #353535;   # Hintergrundfarbe der Detailansicht
}
```

## Abstände festlegen

Der Außenabstand kann nun vorgegeben werden. Hier wurde sich für 40px entschieden darum muss im '<body>' unter ```bash margin: 0; ``` die Zeile ```bash padding: 40px; ``` eingefügt werden.

Damit die Aufgaben der Gruppen auf der Startseite eingerückt unter dem Gruppennnamen angezeigt werden, muss folgender Code unten in 'style.css' hinzugefügt werden:

```bash
.grouped-task {
    margin-left: 60px;   # Einrückung der Aufgabe in einer Gruppe (Startseite)
}
```

Der Abstand zwischen den Zeilen wird durch das Einfügen weiterer Klassen und den darin enthaltenen Eigenschaften und Werten erzielt. Nach dieser Anpassung sieht der Inhalt der 'style.css' so aus:

```bash
body {
    margin: 0;
    padding: 40px;
    font-family: "Liberation Mono", monospace;
    color: #d6d6d6;
}

.home {
    background-color: #2b2b2b;
}

.task-detail {
    background-color: #353535;
}

.group {
    margin-top: 20px;
    margin-bottom: 10px;
}

.grouped-task {
    margin-left: 60px;
}

.task {
    margin-bottom: 10px;
}
```

Damit die begriffe bezüglich des Abstands besser nachvollzogen werden könne, eine Übersicht der Abstände:

- padding → Abstand innerhalb eines Elements
- margin → Abstand außerhalb eines Elements
- margin-left → Außenabstand links
- margin-top / margin-bottom → Außenabstand oben/unten

## Schriftgröße anpassen

Im nächsten Schritt wird die Schriftgröße angepasst, was in diesem Fall sehr schnell umgesetzt werden kann.

In 'style.css' muss jeweils eine Zeile in den Klassen '.home' und '.task-details' eingefügtwerden:

```bash
.home {
    background-color: #2b2b2b;
    font-size: 24px;   # Schriftgröße hinzufügen
}

.task-detail {
    background-color: #353535;
    font-size: 24px;   # Schriftgröße hinzufügen
}
```

## Farbe der Links anpassen

Im Bereich Schriftfarbe muss nur noch die Farbe der Links von dunkel Blau in Türkis geändert werden. Dafür müssen folgende Codezeilen unten in 'style.css' eingefügt werden:

```bash
a {
    color: #40e0d0;   # Farbe des Links
}
```

## Farben der Symbole festlegen

Die Symbole sind bisher in der selben Farbe, wie die Schrift. Darum werden die Symbolfarben in diesem Schritt angepasst. Dafür müssen Anpassungen in 'index.html', 'task.html' und 'style.css' vorgenommen werden. Damit dies besser nachvollzogen werden kann, hier die gesamten Codes der drei Dateien mit Kommentaren bei allen Änderungen.

Aktuelle 'index.html'-Datei:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Taskmanager</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body class="home">

    <h1>{{ name }}</h1>

    <p>Willkommen bei unserem Taskmanager!</p>

    {% set current_group = namespace(name=None) %}

    {% for task in tasks %}

    {% if task["name"] != current_group.name %}

    {% if task["name"] != None %}

    <h2 class="group">
        <span class="group-marker">♦</span> {{ task["name"] }}   # Klasse für Gruppensymbole definieren 'group-marker'
    </h2>

    {% endif %}

    {% set current_group.name = task["name"] %}

    {% endif %}

    <div class="task {% if task['name'] != None %}grouped-task{% endif %}">

        <span class="task-marker">♦</span>

        <a href="/task/{{ task['id'] }}">{{ task['title'] }}</a>

        <span class="priority">

            {% if task["priority"] == 1 %}
            <span class="priority-marker low">●</span> Niedrig   # 
            {% elif task["priority"] == 2 %}
            <span class="priority-marker medium">●</span> Mittel   # 
            {% elif task["priority"] == 3 %}
            <span class="priority-marker high">●</span> Hoch   # 
            {% endif %}

        </span>

        <span class="status">

            {% if task["status"] == "open" %}
            <span class="status-marker open">■</span> Offen    # 
            {% elif task["status"] == "in_progress" %}
            <span class="status-marker in-progress">■</span> In Bearbeitung   # 
            {% elif task["status"] == "completed" %}
            <span class="status-marker completed">■</span> Erledigt   # 
            {% endif %}

        </span>

        {% if task["deadline"] != None %}
        <span class="deadline">
            – Deadline: {{ task["deadline"] }}
        </span>
        {% endif %}

    </div>

    {% endfor %}

</body>

</html>
```

Aktuelle 'task.html'-Datei:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Aufgabe</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body class="task-detail">

    <h1>
        <span class="task-marker">♦</span> {{ task["title"] }}   # 
    </h1>

    <div class="task-info">

        <p>
            {% if task["priority"] == 1 %}
            <span class="priority-marker low">●</span> Niedrig   # wie bei 'index.html'
            {% elif task["priority"] == 2 %}
            <span class="priority-marker medium">●</span> Mittel   # 
            {% elif task["priority"] == 3 %}
            <span class="priority-marker high">●</span> Hoch   #
            {% endif %}
        </p>

        <p>
            {% if task["status"] == "open" %}
            <span class="status-marker open">■</span> Offen   # wie bei 'index.html'
            {% elif task["status"] == "in_progress" %}
            <span class="status-marker in-progress">■</span> In Bearbeitung   # 
            {% elif task["status"] == "completed" %}
            <span class="status-marker completed">■</span> Erledigt   #
            {% endif %}
        </p>

        {% if task["deadline"] != None %}
        <p>
            Deadline: {{ task["deadline"] }}
        </p>
        {% endif %}

        {% if task["name"] != None %}
        <p>
            Gruppe: {{ task["name"] }}
        </p>
        {% endif %}

        {% if task["description"] != None %}
        <p>
            Beschreibung: {{ task["description"] }}
        </p>
        {% endif %}

        {% if task["depends_on_titles"] != None %}
        <p>
            Abhängig von: {{ task["depends_on_titles"] }}
        </p>
        {% endif %}

        {% if task["dependent_titles"] != None %}
        <p>
            Wird benötigt von: {{ task["dependent_titles"] }}
        </p>
        {% endif %}

    </div>

    <p>
        <a href="/">← Zurück</a>
    </p>

</body>

</html>
```

Aktuelle 'style.css'-Datei:

```bash
body {
    margin: 0;
    padding: 40px;
    font-family: "Liberation Mono", monospace;
    color: #d6d6d6;
}

.home {
    background-color: #2b2b2b;
    font-size: 24px;
}

.task-detail {
    background-color: #353535;
    font-size: 24px;
}

.group {
    margin-top: 20px;
    margin-bottom: 10px;
}

.grouped-task {
    margin-left: 60px;
}

.group-marker {
    color: #f08080;   # Farbe des Gruppensymbols
}

.task {
    margin-bottom: 15px;
}

.task-info {
    margin-left: 60px;
}

.task-marker {
    color: #c8a2d8;   # Farbe des Aufgabensymbols
}

a {
    color: #40e0d0;
}

# Farben der Prioritäten
.low {
    color: #70c070;   # Farbe des 'Niedrig'-Symbols
}

.medium {
    color: #f0c419;   # Farbe des 'Mittel'-Symbols
}

.high {
    color: #e05a5a;   # Farbe des 'Hoch'-Symbols
}

# Farben der Statussymbole
.open {
    color: #4a90e2;   # Farbe des 'Offen'-Symbols
}

.in-progress {
    color: #ffffff;   # Farbe des 'In Bearbeitung'-Symbols
}

.completed {
    color: #ff1493;   # Farbe des 'Erledigt'-Symbols
}
```

Damit sind Abstände, Schriftgröße und Farben festgelegt. Im nächsten Abschnitt werden die Eingabemasken für die Erstellung von Aufgaben und Gruppen integriert.  