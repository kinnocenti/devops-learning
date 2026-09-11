# Deployment

Deployment ist der Prozess, bei dem eine Webanwendung als laufender Container auf einem Server oder in einer Cloud-Umgebung bereitgestellt und gestartet wird. Im Zusammenhang mit Deployment müssen verschiedene Themen bearbeitet werden, darum wird das Projekt gedanklich in diese Bereiche aufteilen:

              TASKMANAGER
                   │
    ┌──────────────┼──────────────┐
    │              │              │
Deployment     Persistenz      Security
    │              │              │
    ▼              ▼              ▼
Erreichbar    Daten bleiben    sicherer
 betreiben      erhalten       Betrieb
    │              │              │
    └──────────────┼──────────────┘
                   │
            Docker / Linux
                   │
    ┌──────────────┼──────────────┐
    │              │              │
Netzwerk       Isolation       Prozesse

Hinweis: Da Sicherheit eine große Rolle spielt, wird Scurity im gesamten Projekt nicht aus den Augen gelassen.

## Was bedeutet sicheres Deployment?

Docker ist zunächst einmal eine Technologie zur Isolation und zum Verpacken von Anwendungen. Ein Container macht eine Anwendung nicht automatisch sicher.

Es müssen mehrere Ebenen betrachtet werden:

Internet / Benutzer
        │
        ▼
   Netzwerkzugang
        │
        ▼
      Docker
        │
        ▼
    Container
        │
        ▼
   Flask / App
        │
        ▼
    Datenbank
        │
        ▼
      Daten

Jede dieser Ebenen kann eigene Sicherheitsfragen haben.

## Die erste große Security-Frage: Was ist überhaupt erreichbar?

Aktueller Stand:

      Host
localhost:3001
       │
       ▼
Container:5000
       │
       ▼
     Flask

Hier stellt sich später die Frage, wer kann eigentlich Port 3001 erreichen? Wenn die Anwendung nur lokal laufen soll, ist beispielsweise ein anderes Binding interessant als wenn sie aus dem Internet erreichbar sein soll. Dadurch ergibt sich ein wichtiges Prinzip. Nicht alles, was technisch erreichbar ist, muss auch erreichbar sein. Das nennt man vereinfacht Minimierung der Angriffsfläche.

Wenn die PostgreSQL-Datenbank z.B. nur von der Anwendung benötigt wird, sollte sie nicht zusätzlich öffentlich im Internet erreichbar sein.

Also besser:

       Internet
          │
          ▼
Webserver / Reverse Proxy
          │
          ▼
     Taskmanager
          │
          ▼
      PostgreSQL

statt:

Internet
   │
   ├────► Taskmanager
   │
   └────► PostgreSQL

Das wird später beim Thema Docker-Netzwerke sehr interessant.

## Container-Isolation ist ein Sicherheitsmechanismus - aber keine magische Mauer

Ein Container hat keinen eigenen Kernel. Das ist wichtig für Security.

Vereinfacht:

┌───────────────────────────────┐
│              HOST             │
│                               │
│          Linux Kernel         │
│                               │
│ ┌────────────┐ ┌────────────┐ │
│ │ Container A│ │ Container B│ │
│ │            │ │            │ │
│ │ Taskmanager│ │ PostgreSQL │ │
│ └────────────┘ └────────────┘ │
└───────────────────────────────┘

Die Container bekommen durch Mechanismen wie Namespaces und cgroups eine isolierte Umgebung und Ressourcenbegrenzungen. Aber Container-Isolation ist nicht dasselbe wie eine virtuelle Maschine. Der Kernel bleibt gemeinsam.
Deshalb ist es absolut sinnvoll, später zu verstehen, was Docker tatsächlich isoliert und was nicht.

## Ein besonders wichtiger Punkt: Root

Ein Punkt sollte beim Deployment definitiv untersucht werden, unter welchem Benutzer läuft unser Flask-Prozess im Container? Beim offiziellen Python-Image ist der Ausgangspunkt grundsätzlich ein privilegierter Benutzer, sofern nichts anderes konfiguriert wird.

Das bedeutet, wenn die Anwendung einfach gestartet wird, was muss beachtet werden:

          Wer startet Flask?
                  │
                  ▼
          Welcher Benutzer?
                  │
                  ▼
Welche Rechte besitzt dieser Benutzer?

Für ein produktives Deployment ist das relevant. 

Denn es ist nicht gewünscht:

└── Flask läuft als root

sondern:

Container
└── Flask läuft als unprivilegierter Benutzer

Das ist ein klassisches Beispiel für das Least-Privilege-Prinzip. Ein Prozess soll nur die Rechte besitzen, die er tatsächlich benötigt. Das Prinzip wird beim Deployment immer wieder zu sehen sein.

## Secrets gehören nicht ins Repository

Es ist zu beachten, dass keine Secrets, wie z.B. Passwörter im Repository gespeichert werden.

Angenommen, die Anwendung benötigt irgendwann:

DATABASE_PASSWORD
SECRET_KEY

Dann wäre das hier eine schlechte Idee:

DATABASE_PASSWORD = "MeinSuperGeheimesPasswort123!"

und noch schlimmer wäre:

config.py
└── Passwort
└── Secret Key

…und anschließend wird das Ganze auf GitHub gepusht.

Darum soll der Umgang mit den folgenden Punkten erlernt werden:

- Umgebungsvariablen
- Secret Management
- .env-Dateien im lokalen Entwicklungsumfeld
- .gitignore

Dabei wird wir auch eine wichtige Unterscheidung gemacht, .env ist nicht automatisch ein sicheres Secret Management. Für lokale Entwicklung kann das sinnvoll sein. Für echtes produktives Deployment gibt es bessere Mechanismen. Diese Differenzierung wird später näher betrachtet.

## Der Container sollte möglichst wenig enthalten

Das ist ein weiterer Punkt.

Die Dockerfile führt aktuell im Build ```bash FROM python:3.12-slim-trixie ``` aus. Das ist bereits eine relativ schlanke Ausgangsbasis. Aber Security bedeutet hier nicht einfach, je kleiner das Image, desto sicherer. Sondern eher, es soll möglichst wenig unnötige Software und damit möglichst wenig unnötige Angriffsfläche im Image sein.

Später kann man sich z.B. anschauen:

Image
 ├── Python
 ├── Flask
 ├── Dependencies
 ├── unsere Anwendung
 └── ...?

und fragen, was davon wird wirklich benötigt? Das ist dann Image Hardening.

## Auch Dependencies gehören zur Security

In der Dockerfile steht:

```bash
COPY requirements.txt .
RUN pip install -r requirements.txt
```

Das funktioniert so, aber Security wirft sofort weitere Fragen auf:

- Welche Versionen installieren wir?
- Sind die Abhängigkeiten aktuell?
- Gibt es bekannte Schwachstellen?
- Sind Versionen reproduzierbar?
- Wie erkennen wir später eine verwundbare Dependency?

Das führt uns irgendwann zu Dingen wie Dependency Scanning und Vulnerability Scanning. Aber es sollte von Anfang an als Teil des Projekts betrachtet werden.

## Flask

Momentan wird gestartet mit, ```bash CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"] ```. Das ist für dieses Lernprojekt völlig okay.
Für ein echtes Production Deployment würde sich die Frage stellen, ist der Flask-Development-Server der richtige Server für den produktiven Betrieb? → Nein.

Später könnte man z.B. einen WSGI-Server, wie Gunicorn, mit einem Reverse Proxy davor, umgesetzt. Dann würde sich folgender Ablauf ergeben:

     Internet
        │
        ▼
   Reverse Proxy
        │
        │ HTTPS
        ▼
Application Server
        │
        ▼
   Taskmanager
        │
        ▼
    PostgreSQL

Und damit kommen dann auch Themen wie:

- HTTPS/TLS
- Security Headers
- Request Limits
- Logging
- Zugriffskontrolle
- Reverse Proxy
- sichere Netzwerkarchitektur

## Security wird kein Extra-Kapitel

Wie schon erwähnt wird sich Sicherheit thematisch durch das ganze Projekt ziehen, wie bei den folgenden Fragen zu sehen ist: 

- Projektbereich → Security-Frage
- Dockerfile     → Läuft der Prozess mit möglichst wenigen Rechten?
- Image          → Ist unnötige Software enthalten?
- Dependencies   → Gibt es bekannte Schwachstellen?
- Ports          → Was muss überhaupt erreichbar sein?
- Netzwerk       → Welche Container dürfen miteinander sprechen?
- Datenbank	     → Ist PostgreSQL von außen erreichbar?
- Persistenz     → Wer darf auf die Daten zugreifen?
- Secrets        → Wo liegen Passwörter und Schlüssel?
- Deployment     → Wer kann den Dienst erreichen?
- HTTPS	         → Werden Daten verschlüsselt übertragen?
- Logging	     → Können sicherheitsrelevante Ereignisse nachvollzogen werden?
- Updates	     → Wie werden Images und Dependencies aktualisiert?