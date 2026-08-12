# Python (.venv) und Flask Installation und Test-Flask-Anwendung

## Python installieren

```bash
sudo apt update   # Paketquellen aktualisieren

sudo apt install python3   # Python3 installieren

sudo apt install python3-pip    # Paketverwaltung für Python installieren
```

## .venv installieren

```bash
cd /Path   # den entsprechenden Pfad eingeben

python3 –version   # Version prüfen

sudo apt install python3.12-venv   # .venv installieren   

python3 -m venv .venv   # mit .venv virtuelle Umgebung erzeugen

source .venv/bin/activate   # die virtuelle Umgebung aktivieren
```

Hinweis: Wenn 'source .venv/bin/activate' ausgeführt wird, steht dann vor dem Prompt im Terminal '(.venv)'. Der Terminal greift dann auf die Python-Umgebung zu.

## Flask installieren

```bash
pip install flask   # Flask installieren
```

Hinweis: Für diesen Befehl muss sich der Terminal in .venv befinden.

## Systemstruktur

Linux Mint
   │
   ├── System-Python
   |
   └── devops-learning
        │
        └── taskmanager
             │
             ├── taskmanager-database/
             │    └── schema.sql
             │
             └── .venv/
                  ├── Python 3.12
                  ├── pip
                  └── Flask

## Test-Flask-Anwendung

In VScode im Ordner 'taskmanager' eine neue Datei erstellen 'app.py'.

Folgenden Code in 'app.py' einfügen:

```bash
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hallo vom Taskmanager!"
```

Im Terminal eingeben:

```bash
flask --app app run   # damit läuft app.py
```

Im Browser eingeben:

http://127.0.0.1:5000  

Damit wird im Browser 'Hallo vom Taskmanager!' angezeigt.

Hinweis: Die Warnung im Terminal ist kein Problem.
Nachdem 'http://127.0.0.1:5000' im Browser eingegeben wurde, sind im Terminal zwei GET-Anfragen vom Browser zu sehen.

Ablauf zum Verständnis:

Browser
   │
   │ HTTP GET /
   ▼
127.0.0.1:5000
   │
   ▼
Flask
   │
   │ erkennt: "/"
   ▼
home()
   │
   │ return
   ▼
"Hallo vom Taskmanager!"
   │
   ▼
Browser