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

Hier wurde nicht nur 