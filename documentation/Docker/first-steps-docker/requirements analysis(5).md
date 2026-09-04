# Anforderungsanalyse

Bevor eine Anwendung containerisiert wird, sollte zunächst geklärt werden, welche Voraussetzungen sie für ihren Betrieb benötigt. Die Dockerfile sollte anschließend genau diese Anforderungen abbilden. Ausgangspunkt ist die Frage, was benötigt die Anwendung, um unabhängig von der bisherigen lokalen Umgebung ausgeführt werden zu können? Damit wird eine Anforderungsanalyse vor der Containerisierung durchgeführt.

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

## Dateien und Anwendungscode

Welche Dateien und Verzeichnisse werden zur Laufzeit benötigt? Dazu gehören beispielsweise:

- Anwendungscode
- Konfigurationsdateien
- Templates
- statische Dateien
- weitere für die Ausführung benötigte Ressourcen

Gleichzeitig sollte geprüft werden, welche Dateien nicht benötigt werden, z.B. Entwicklungsumgebungen, temporäre Dateien oder automatisch erzeugte Cache-Dateien.

## Laufzeitumgebung

Welche Software bzw. welche Laufzeit benötigt die Anwendung, um ausgeführt werden zu können?

Beispiele:

Python
Java Runtime
Node.js
.NET Runtime

Dabei sollte insbesondere die benötigte Version betrachtet werden. Eine definierte und getestete Version erhöht die Reproduzierbarkeit der Anwendung.

## Abhängigkeiten

Welche zusätzlichen Softwarepakete oder Bibliotheken benötigt die Anwendung? Dabei wird zwischen der direkten Abhängigkeit der Anwendung und den daraus resultierenden weiteren Abhängigkeiten unterschieden.

Zum Beispiel:

Anwendung
  ↓
Flask
  ↓
weitere Flask-Abhängigkeiten

Die benötigten Abhängigkeiten sollten möglichst nachvollziehbar und reproduzierbar festgehalten werden.

## Konfiguration

Welche Einstellungen benötigt die Anwendung zur Laufzeit? Dazu können beispielsweise gehören:

Ports
Dateipfade
Umgebungsvariablen
Verbindungsinformationen
Einstellungen für externe Dienste

Dabei sollte zwischen Anwendungscode und laufzeitabhängiger Konfiguration unterschieden werden.

## Daten und Persistenz

Welche Daten benötigt die Anwendung und wie werden diese gespeichert? Hier muss insbesondere geprüft werden, ob Daten dauerhaft erhalten bleiben müssen. Dabei gilt, Anwendung und persistente Daten sollten grundsätzlich getrennt betrachtet werden.
Ein Container kann jederzeit beendet, gelöscht und neu erstellt werden. Daten, die über den Lebenszyklus eines Containers hinaus benötigt werden, sollten deshalb nicht ausschließlich im beschreibbaren Container-Dateisystem gespeichert werden. Für solche Daten kommen beispielsweise Volumes oder externe Datenspeicher zum Einsatz.

Aus der Anforderungsanalyse lässt sich anschließend ableiten, welche Bestandteile das Docker-Image benötigt:

Was benötigt die Anwendung?
       │
       ├── Dateien / Anwendungscode
       ├── Laufzeitumgebung
       ├── Abhängigkeiten
       ├── Konfiguration
       └── Daten / Persistenz
       │
       ↓
Container-Definition
       ↓
   Docker Image
       ↓
    Container
       ↓
laufende Anwendung

Die Dockerfile ist damit nicht der Ausgangspunkt der Containerisierung, sondern das Ergebnis der vorherigen Anforderungsanalyse. Zuerst wird ermittelt, was die Anwendung benötigt. Anschließend wird beschrieben, wie diese Voraussetzungen in einem Container bereitgestellt werden.

Gesamtüberblick der Anforderungsanalyse

                    TASKMANAGER
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
 Anwendungscode       Runtime         Abhängigkeiten
        │                │                │
    app.py          Python 3.12        Flask 3.1.3
 templates/
 static/
        │
        └────────────────┬────────────────┐
                         ↓
                       Daten
                         │
                  taskmanager.db
                         │
                   später Volume