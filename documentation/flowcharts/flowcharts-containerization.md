# Ablaufdiagramme und Modelle der Containerisierung des Taskmanagers

Hier ein Überblick über Modelle und Abläufe im Bezug auf die Containerisierung des Taskmanagers. 

## Grundaufbau

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

## Unterscheidung Dockerfile, Image und Container

      Dockerfile
          │ docker build
          ▼
        Image
          │ docker run
          ▼
      Container
          │
          ▼
laufender Taskmanager

## Ablauf der Containerisierung

    Dockerfile
        │
        │ docker build
        ▼
      Image
        │
        │ docker run
        ▼
    Container
        │
        │ CMD
        ▼
      Flask
        │
        │ 0.0.0.0:5000
       ▼
Docker-Netzwerk
        │
        │ Port Mapping
        ▼
  localhost:3001
        │
        ▼
     Browser

## Ablauf nach Containerstart

 Container startet
        ↓
CMD wird ausgeführt
        ↓
flask --app app run
        ↓
 Flask lädt app.py
        ↓
 Flask lauscht auf
  0.0.0.0:5000
        ↓
 Taskmanager läuft

## Portmodell

Browser
   │
   │ localhost:3001
   ▼
┌─────────────────────────┐
│          HOST           │
│                         │
│        Port 3001        │
└────────────┬────────────┘
             │
             │ Docker Port Mapping
             ▼
┌─────────────────────────┐
│       CONTAINER         │
│                         │
│       Port 5000         │
│           │             │
│           ▼             │
│    Flask 0.0.0.0:5000   │
│           │             │
│           ▼             │
│       Taskmanager       │
└─────────────────────────┘

## Ablauf Browser → Flask

  Browser
     │
     │ localhost:3001
     ▼
    Host
     │
     │ Docker Port Mapping
     │ 3001 → 5000
     ▼
 Container
     │
     │ Netzwerkinterface
     ▼
   Flask
     │
     │ 0.0.0.0:5000
     ▼
Taskmanager

## Weg eines Docker-Befehls

      Docker-Befehl
            │
            ▼
      Docker Client
            │
            │ Docker API
            ▼
  Docker Engine / Daemon
            │
  ┌─────────┼─────────┐
  ▼         ▼         ▼
Images  Container  Netzwerke
                      │
                      ▼
                   Volumes