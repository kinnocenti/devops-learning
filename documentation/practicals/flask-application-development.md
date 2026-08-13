# Entwicklung der Flask-Anwendung

Hier werden die Entwicklungsschritte an der Flask-Anwendung zum näheren Verständnis erklärt und auf ienem Blick dargestellt.

Anmerkung: Versionierung wird regulär mit 'git commit' durchgeführt.

## Erste Test-Flask-Anwendung

Einfachste Flask-Anwendung

```bash
from flask import Flask   # Flask aus dem installierten Flask-Paket holen

app = Flask(__name__)   # Flask-Anwendung erzeugen

@app.route("/")   # wenn / aufrufen wird, soll home() ausgeführt werden
def home():   # home()-Funktion
    return "Hallo vom Taskmanager!"   # liefert Text als HTTP-Antwort

# mit folgenden Befehl ausführen
flask --app app run

# im Browser folgenden eingeben
http://127.0.0.1:5000/
```

Hinweis: Der Befehl zum Ausführen des Codes und die Eingabe der oben aufgeführten URL müssen nach jedem folgenden Code durchgeführt werden. Sie werden im Folgenden nicht wiederholt.

Zeigt folgende Abläufe an:
- Flask läuft
- integrierter Webserver läuft
- Browser kann mit Python-Anwendung kommunizieren
- der Text wird als HTTP-Anwort zurückgeliefert

Ablauf mit HTTP:

Browser
   │
   │ GET /
   ▼
Flask
   │
   │ Route "/"
   ▼
Funktion home()
   │
   │ erzeugt Antwort
   ▼
HTTP Response

## HTML anwenden

Es wird mit HTTP nicht nur Text als Inhalt übergeben, sondern HTML als Inhalt.

```bash
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """   # liefert Text als HTML-Antwort
    <!DOCTYPE html>
    <html>
        <head>
            <title>Taskmanager</title>
        </head>
        <body>
            <h1>Taskmanager</h1>   # eine Überschrift erster Ebene
            <p>Willkommen bei unserem Taskmanager!</p>   # ein Absatz
        </body>
    </html>
    """
```

Aufbau:

Browser
   ↑
   │ HTML steckt direkt in app.py
   │
Flask
   │
   └── app.py
       ├── Python
       └── HTML

## Flask und HTML voneinander trennen

Für die bessere Struktur und Verwaltung des Codes, werden Codeteile in verschiedene Dateien aufgeteilt. Der Python-Code wird vom HTML-Code strukturell getrennt.

Neuen Ordner erstellen 'templates'.
Darin die Datei 'index.html' anlegen.

Folgenden Code einfügen:

```bash
<!DOCTYPE html>
<html>
    <head>
        <title>Taskmanager</title>
    </head>
    <body>
        <h1>Taskmanager</h1>
        <p>Willkommen bei unserem Taskmanager!</p>
    </body>
</html>
```

Dann die Datei 'app.py' anpassen und den Inhalt durch folgenden Code ersetzen:

```bash
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")   # Referenzierung auf index.html 
```

Aufbau mit Templates:

Browser
   ↑
   │ HTML
   │
Flask
   │
   ├── app.py
   │   └── Python / Logik
   │
   └── templates/
       └── index.html
           └── HTML / Darstellung

Ablauf:

Browser
   │
   │ HTTP
   ▼
Flask
   │
   ├── Python
   │
   └── Template
          │
          ▼
       HTML
          │
          ▼
       Browser
          │
          ▼
       Darstellung

## Erster Schritt von 'HTML-Datei' zu 'dynamischer Webanwendung' 

In diesem Schritt wird ein statischer Wert zu einem dynamischen Wert im HTML-Template mit Hilfe von Jinja.

In app.py die letzte Zeile ändern:

```bash
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", name="Taskmanager")   # diese Zeile hat sich geändert, damit wird dem Template ein Wert mitgegeben: name = "Taskmanager"
```

In index.html die siebte Zeile ändern:

```bash
<!DOCTYPE html>
<html>

<head>
    <title>Taskmanager</title>
</head>

<body>
    <h1>{{ name }}</h1>   # diese Zeile hat sich geändert, hier wird der Wert der Template-Variable 'name' eingesetzt
    <p>Willkommen bei unserem Taskmanager!</p>
</body>

</html>
```

Mit der Template-Engine Jinja wird das statische HTML dynamisch. Statt des statischen Eintrags Taskmanager wird {{ name }} eingefügt und damit kommt Jinja zum Einsatz. Der Wert der an dieser Stelle eingesetzt wird, wird aus dem Python-Code der Datei 'app.py' geholt, eingefügt und wird per HTTP an den Browser übergeben.

Ablauf mit Jinja:

Python
   │
   │ Daten
   ▼
Jinja
   │
   │ setzt Daten in Template ein
   ▼
HTML
   │
   ▼
Browser

Gesamter Ablauf:

    SERVER

Python / Flask
      │
      │ name = "Taskmanager"
      ▼
Jinja Template Engine
      │
      │ verarbeitet
      ▼
templates/index.html
      │
      │ {{ name }}
      ▼
fertiges HTML
      │
      │ HTTP Response
      ▼

    BROWSER

      │
      │ empfängt HTML
      ▼
Browser rendert HTML
      |
      ▼
┌──────────────────┐
│ Taskmanager      │
│                  │
│ Willkommen bei   │
│ unserem          │
│ Taskmanager!     │
└──────────────────┘