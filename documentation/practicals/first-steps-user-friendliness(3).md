# Erste Schritte zur Benutzerfreundlichkeit

Im ersten Schritt werden die Werte aus bestimmten Spalten des 'Taskmanagers' benutzerfreundlicher gemacht. Technische Werte, wie z.B. 'in_progress', werden in eine benutzerfreundlichere Darstellung, wie 'In Bearbeitung', geändert. Es werden also erste grundlegende Umsetzungsschritte im Code gezeigt.

## Statuswerte anpassen

Die Statuswerte sind in der Datenbank in Englisch als technische Daten abgespeichert. Diese Werte sollen in der Ausgabe im Browser zukünftig auf Deutsch und damit verständlich für Benutzer*innen sein. 
Wo soll die Anpassung kodiert werden? In SQLite werden keine Anpassungen vorgenommen, die Werte werden so belassen, da sie der Datenbanklogik entsprechen. SQLite speichert also die technischen Werte. Python holt Daten aus der Datenbank und gibt diese an die Anwendung weiter. Jinja kümmert sich darum, wie diese Daten für die HTML-Oberfläche dargestellt werden. Vereinfacht übernimmt Jinja die Darstellungslogik, während SQLite und Python die Datenlogik übernehmen. Da die Anpassung der Statuswerte für die Darstellung im Browser vorgenommen wird, muss diese in der 'index.html'-Datei umgesetzt werden. 

In der Datei 'index.html' muss folgender Codeabschnitt geändert werden:

Vorher:

```bash
<ul>
    {% for task in tasks %}
    <li>
        {{ task["title"] }}
        – Status: {{ task["status"] }}
        – Priorität: {{ task["priority"] }}
    </li>
    {% endfor %}
</ul>
```

Nachher:

```bash
<ul>
    {% for task in tasks %}   # for-Schleife, damit alle Zeilen durchgegangen werden
    <li>
        {{ task["title"] }}

        – Status:
        {% if task["status"] == "open" %} 
        Offen
        {% elif task["status"] == "in_progress" %}
        In Bearbeitung
        {% elif task["status"] == "completed" %}
        Erledigt
        {% endif %}   # in dieser if-Anweisung werden die Statuswerte für die Darstellung gesetzt

        – Priorität: {{ task["priority"] }}
    </li>
    {% endfor %}
</ul>
```

Ausgabe im Browser:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Status: Erledigt – Priorität: 2
    Docker Tutorial Teil 1 – Status: In Bearbeitung – Priorität: 2
    Docker Tutorial Teil 2 – Status: Offen – Priorität: 3
    Linuxbefehlsübersicht erstellen – Status: Offen – Priorität: 1
    Docker Compose Grundlagen – Status: Offen – Priorität: 2

Wie zu sehen, haben sich die Statuswerte angepasst.

Ablauf:

SQLite
   │
   │ open / in_progress / completed
   ▼
Python / Flask
   │
   │ unverändert weitergegeben
   ▼
Jinja
   │
   │ technische Werte werden für Darstellung übersetzt
   ▼
HTML
   │
   │ Offen / In Bearbeitung / Erledigt
   ▼
Browser

## Prioritätswerte anpassen

Wie der Statuswert, wird auch der Prioritätswert für die Browserausgabe mit if-Anweisung geändert.

Der folgende Codeabschnitt muss unter den Codeblock der Statuswerte. Also auch innerhalb der for-Schleife:

```bash
        – Priorität:
        {% if task["priority"] == 1 %}   # Wenn Priorität 1 ist, dann Niedrig einsetzen
        Niedrig   
        {% elif task["priority"] == 2 %}   # elif = ansonsten wenn
        Mittel
        {% elif task["priority"] == 3 %}
        Hoch
        {% endif %}
```

Hinweis: Browserausgabe siehe nächstes Kapitel.

## Deadline integrieren und anpassen

Hier wird die Deadline eingefügt. Dabei soll zum einen die Deadline ausgegeben werden und zum anderen soll lediglich ein '–' ausgegeben werden, wenn keine Deadline eingegeben wurde. Dafür wird eine if/else-Anweisung verwedent.
Das Datums- und Uhrzeitformat, das in der Browserausgabe unten zu sehen ist, liegt einem Textfeld zugrunde. In der Planung des Taskmanagers wurde entschieden, dass Deadline ein Textfeld hat. User können also das für ihre Deadline eintragen, was sie favorisieren.

Hinweis: Was steht wo, wenn keine Deadline eingegeben wurde? In der Datenbank steht 'NULL', in Python 'None' und durch Jinja im Browser '–'.

Die folgenden Codezeilen werden entsprechend unter den Codeabschnitt der Prioritätswerte eingefügt:

```bash
       – Deadline:
        {% if task["deadline"] == None %}   # wenn Deadline None ist, dann – einfügen
        –
        {% else %}   # sonst Wert aus Spalte deadline ausgeben
        {{ task["deadline"] }}
        {% endif %}
```

Ausgabe im Browser:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Status: Erledigt – Priorität: Mittel – Deadline: –
    Docker Tutorial Teil 1 – Status: In Bearbeitung – Priorität: Mittel – Deadline: –
    Docker Tutorial Teil 2 – Status: Offen – Priorität: Hoch – Deadline: 2026-08-12 20:00
    Linuxbefehlsübersicht erstellen – Status: Offen – Priorität: Niedrig – Deadline: –
    Docker Compose Grundlagen – Status: Offen – Priorität: Mittel – Deadline: –

In der Browserausgabe ist auch ersichtlich, dass die Prioritätswerte entsprechend der Anpassungen des Codes im vorherigen Kapitel angepasst wurden.

Mit zwei weiteren SQL-Updates wurden zwei neue Deadlines eingetragen und das Resultat ist entsprechend in der folgenden Browserausgabe zu sehen.

```bash
UPDATE tasks
SET deadline = 'Freitag'
WHERE id = 2;

UPDATE tasks
SET deadline = '30.09.2026'
WHERE id = 4;
```

Browserausgabe:

Taskmanager

Willkommen bei unserem Taskmanager!

    Docker installieren – Status: Erledigt – Priorität: Mittel – Deadline: –
    Docker Tutorial Teil 1 – Status: In Bearbeitung – Priorität: Mittel – Deadline: Freitag
    Docker Tutorial Teil 2 – Status: Offen – Priorität: Hoch – Deadline: 2026-08-12 20:00
    Linuxbefehlsübersicht erstellen – Status: Offen – Priorität: Niedrig – Deadline: 30.09.2026
    Docker Compose Grundlagen – Status: Offen – Priorität: Mittel – Deadline: –

Damit alle Änderungen nochmal kontrolliert werden können, hier die komplette aktuelle Version der 'index.html'-Datei:

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

        – Deadline:
        {% if task["deadline"] == None %}
        –
        {% else %}
        {{ task["deadline"] }}
        {% endif %}
    </li>
    {% endfor %}
</ul>

</html>  
``` 