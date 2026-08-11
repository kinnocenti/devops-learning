# Projektplan Taskmanager

## Warum und Ziel

Damit eine Webanwendung mit Docker bereit gestellt werden kann, wird zunächst eine Webanwendung entwickelt. Webentwicklung selbst ist nicht Ziel von DEVOPS-LEARNING, aber wird hier einmal durchgearbeitet, damit der Prozess bekannt ist. 

Im Projekt Taskmanager wird nach der Webentwicklung der Schritt hin zu Docker gemacht und die Webanwendung entsprechend bereit gestellt. Dies ist das eigentliche Ziel des Projektes.

## Projektphasen

Phase 1 – Anwendung verstehen:
Browser
   ↓
Webanwendung
   ↓
Python / Flask

Phase 2 – Docker:
Browser
   ↓
Host:8080
   ↓
Docker Container
   ↓
Flask
   ↓
Anwendung

Lerninhalte:
Dockerfile
Images
Container
Ports
docker build
docker run
Logs
Container stoppen/starten
Images und Container untersuchen
warum die Anwendung im Container etwas anders gestartet werden muss als lokal

Phase 3 – Persistenz:
Implementierung der Datenbank:

             ┌── Flask
Browser ────►│
             └── SQLite

Interessante Docker-Frage:
Was passiert mit meinen Daten, wenn ich den Container lösche?
Damit kommen wir zu Volumes.

Phase 4 – Docker Compose:
Beispielsweise:

          ┌──────────────┐
          │ Webcontainer │
Browser ─►│    Flask     │
          └──────┬───────┘
                 │
          ┌──────▼───────┐
          │ Datenbank    │
          └──────────────┘

Phase 5 – Git & GitHub:
GitHub
   ↓
CI/CD
   ↓
Docker Image bauen
   ↓
Image Registry
   ↓
Deployment

Phase 6 – Kubernetes
Kubernetes
├── Deployment
├── Pod
├── Service
└── ConfigMap / Secret

Phase 7 – IaC / DevOps / Monitoring

Danach kann beispielsweise Terraform/OpenTofu, Ansible, Prometheus/Grafana, GitHub Actions usw. an dieses Projekt angeknüpft werden.

## Aufbau des Taskmanagers

Die Hauptübersicht:
                MEINE AUFGABEN                
                                     
  📁 DOCKER                                    
                                               
  🔴 ⬜ Docker Tutorial Teil 2                 
  🔵    Docker Tutorial Teil 3                 
  🟡 ⬜ Docker Compose lernen                  
                                               
  📁 KUBERNETES                                
                                               
  🔴 ⬜ Kubernetes Grundlagen                  
                                               
  📋 OHNE GRUPPE                              
                                               
  🟡 ⬜ GitHub README aktualisieren            
                                                                                
            🗄️ ARCHIV                    

Klick auf „ARCHIV“

Wechsel zu separater Ansicht:
            ARCHIV                     
                                       
  📁 DOCKER                                    
                                              
     Docker Tutorial Teil 1                    
     Docker Grundlagen                         
                                               
  📁 KUBERNETES                                
                                               
     Kubernetes Grundlagen Teil 1              
                                               
  📋 OHNE GRUPPE                               
                                               
     GitHub README überarbeitet                
                                              
  ← Zurück zu den Aufgaben                     
                                                                             
Erledigten Aufgaben werden genauso gruppiert darstellen, wie die aktiven Aufgaben.

Klares Status-/Archiv-Konzept:

Die aktive Übersicht kennt nur zwei Zustände:
⬜ Offen
🔵 In Bearbeitung

Sobald eine Aufgabe auf Erledigt gesetzt wird:
⬜ Offen
   ↓
🔵 In Bearbeitung
   ↓
✅ Erledigt
   ↓
🗄️ Archiv

„Erledigt“ ist der Auslöser für das Archivieren, aber kein dauerhaft sichtbarer Status in der Hauptübersicht.

Die Aufgabe wird also nicht gelöscht. Sie wandert lediglich aus der aktiven Ansicht ins Archiv.

Die Aufgaben, die zu erledigen sind, sollen im Mittelpunkt stehen.

Das fachliche Modell:
Aufgabe wird erstellt
⬜ OFFEN

Aufgabe wurde begonnen
🔵 IN BEARBEITUNG

Aufgabe wurde abgeschlossen
✅ ERLEDIGT

Anwendung:
→ Aufgabe aus aktiver Übersicht entfernen
→ Aufgabe ins Archiv verschieben

Aufgabe wird technisch nicht von einem Ort (Tabelle in DB) in einen anderen verschoben.

Zudem muss eine der drei Prioritäten vergeben werden:
🔴 Hoch
🟡 Mittel
🟢 Niedrig

Beispielhafte aktive Übersicht:
📁 DOCKER

🔴 ⬜ Docker Tutorial Teil 2
🔵    Docker Tutorial Teil 3
🟢 ⬜ Docker Compose Dokumentation lesen

📁 KUBERNETES

🔴 ⬜ Kubernetes Grundlagen
🟡 ⬜ Ersten Pod erstellen

Konzept:

Aktive Übersicht:
Aufgabengruppen
Aufgaben innerhalb der Gruppen
Aufgaben ohne Gruppe
nur Offen und In Bearbeitung
Priorität sichtbar
Deadline sichtbar
Abhängigkeiten erkennbar
Archiv nur als anklickbarer Eintrag

Archiv:
alle erledigten Aufgaben
gleiche Gruppierung wie in der Hauptübersicht
Aufgaben ohne Gruppe ebenfalls separat
erledigte Aufgaben klar als archiviert erkennbar
Möglichkeit, eine Aufgabe ggf. wiederherzustellen

Aufgabenstatus:
Offen → In Bearbeitung → Erledigt/Archiv