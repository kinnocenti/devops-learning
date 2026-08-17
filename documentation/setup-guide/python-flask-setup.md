# Python (.venv) und Flask Installation und Test-Flask-Anwendung

Für die Entwicklung des 'Taskmanagers' wird Python, eine virtuelle Umgebung (.venv) und Flask benötigt. In diesem Abschnitt werden die entsprechenden Installationen und die Erstellung der 'Test-Flask_Anwendung' aufgezeigt. 

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

python3 -m venv .venv   # mit .venv virtuelle Umgebung erstellen

source .venv/bin/activate   # die virtuelle Umgebung aktivieren
```

Hinweis: Wenn ```bash source .venv/bin/activate ``` ausgeführt wird, steht vor dem Prompt im Terminal '(.venv)'. Der Terminal greift dann auf die Python-Umgebung zu.

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

In VScode im Ordner 'taskmanager' eine neue Datei 'app.py' erstellen.

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
flask --app app run   # damit wird 'app.py' ausgeführt
```

Im Browser eingeben:

http://127.0.0.1:5000  

Ausgabe im Browser:

Hallo vom Taskmanager!

Hinweis: Die Warnung im Terminal muss nicht weiter beachtet werden, da sie lediglich auf die Verwendung des integrierten Servers hinweist.
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