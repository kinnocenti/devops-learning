# Entwicklung der Flask-Anwendung

Hier werden die Entwicklungsschritte an der Flask-Anwendung zum näheren Verständnis erklärt.

## Erste Test-Flask-Anwendung

Einfachste Flask-Anwendung

```bash
from flask import Flask   # Flask aus dem installierten Flask-Paket holen

app = Flask(__name__)   # Flask-Anwendung erzeugen

@app.route("/")   # wenn / aufrufen wird, soll home() ausgeführt werden
def home():   # home()-Funktion
    return "Hallo vom Taskmanager!"   # liefert Text als HTTP-Antwort
```

Zeigt folgende Abläufe an:
- Flask läuft
- integrierter Webserver läuft
- Browser kann mit Python-Anwendung kommunizieren
- der Text wird als HTTP-Anwort zurückgeliefert

Ablauf:

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

Aufbau:

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