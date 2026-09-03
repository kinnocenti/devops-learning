# Containerisierung des Taskmanagers

Nachdem die Grundlagen für Docker geschaffen wurden, wird nun der Taskmanager containerisiert mit Docker. Es werden also alle Schritte durchlaufen, die notwendig sind, um die Webanwendung in einem Container lauffähig zu machen.

Damit wird folgender Aufbau umgesetzt.

Linux-Host
    │
    └── Docker Engine
          │
          └── Container
                │
                └── Taskmanager
                      ├── Python
                      ├── Flask
                      ├── Anwendungscode
                      └── Abhängigkeiten

Damit wirklich verstanden wird, welche Komponenten in einem Container aktiv sind und als Vorbereitung auf die Dockerfile, wurde die Ausgabe von ```bash docker inspect webserver ``` analysiert. Da dies den Rahmen dieser Datei sprengen würde, wurde die Analyse in 'analysis-docker-inspect(5).md' angespeichert.   

## Zu Anfang

Zu Anfang macht es Sinn sich zu überlegen was alles im Container benötigt wird. Dafür sollte man sich folgende Fragen stellen: 

Was braucht diese Anwendung?
    ↓
Welche Dateien?
Welche Laufzeit?
Welche Abhängigkeiten?
Welche Konfiguration?
Welche Daten?
    ↓
Docker Image
    ↓
Container

## 

