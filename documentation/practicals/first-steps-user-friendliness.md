# Erste Schritte zur Benutzerfreundlichkeit

Im ersten Schritt werden die Statuswerte des 'Taskmanagers' benutzerfreundlicher gemacht. Es werden also erst grundlegende Umsetzungsschritte im Code gezeigt. Diese werden dabei auch aus Sicht der Systemintegration erläutert.

## Statuswerte anpassen

Die Statuswerte sind in der Datenbank in Englisch als technische Daten abgespeichert. Diese Werte sollen in der Ausgabe im Browser zukünftig auf Deutsch und damit verständlich für Benutzer*innen sein. 
Wo soll die Anpassung kodiert werden? In SQLite werden keine Anpassungen vorgenommen, die Werte werden so belassen, da sie der Datenbanklogik entsprechen. SQLite speichert also die technischen Werte. Python holt Daten aus der Datenbank und gibt diese an die Anwendung weiter. Jinja kümmert sich darum, wie diese Daten für die HTML-Oberfläche dargestellt werden. Jinja übernimmt also die Darstellungslogik und SQLite und Python die Datenlogik. Da die Anpassung der Statuswerte für die Darstellung im Browser vorgenommen wird, muss diese in der 'index.html' umgesetzt werden. 

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

Wie zu sehen haben sich die Statuswerte angepasst.

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