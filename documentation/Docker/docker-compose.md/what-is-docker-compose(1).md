# Docker-Compose – Grundlagen und Architekturmodell

Bevor die ersten praktischen Schritte mit Docker-Compose gemacht werden, wird zuvor erlärt, was Docker-Compose ist und wofür es verwendet wird.

## Zweck von Docker-Compose

Docker-Compose ermöglicht es, mehrere zusammengehörige Containerdienste und die zugehörigen Ressourcen zentral in einer deklarativen YAML-Konfiguration zu beschreiben und gemeinsam zu verwalten.
Statt Container, Netzwerke und Volumes ausschließlich über einzelne Docker-Befehle zu verwalten, können die benötigten Ressourcen eines Anwendungsstacks gemeinsam deklariert werden. Die Konfiguration kann unter anderem Images, Portfreigaben, Netzwerke, Volumes und Umgebungsvariablen festlegen. Docker-Compose setzt diese Beschreibung mithilfe der Docker-Engine um.
Compose vereinfacht damit die reproduzierbare Bereitstellung und Verwaltung eines zusammengehörigen Anwendungsstacks. Die erforderliche Architektur und die gewünschten Betriebsparameter müssen weiterhin bewusst festgelegt werden.
Ein erfolgreicher Start der Container bedeutet nicht automatisch, dass sämtliche Dienste betriebsbereit sind oder die Anwendung vollständig funktioniert.

Zentrale Vorteile:

- Zusammengehörige Dienste gemeinsam konfigurieren und verwalten
- Konfiguration nachvollziehbar und versionierbar ablegen
- Benötigte Netzwerke und Volumes deklarieren
- Bereitstellung und Verwaltung eines Anwendungsstacks vereinfachen

## Zentrale Begriffe

Hier werden zentrale Begriffe von Docker-Compose erläutert.

### Projekt

Ein Compose-Projekt fasst die zugehörigen Ressourcen einer Anwendung zusammen. Dazu gehören beispielsweise Services, Netzwerke und Volumes. Der Projektname dient unter anderem zur Zuordnung der von Compose verwalteten Ressourcen.

### Service

Ein Service beschreibt die gewünschte Konfiguration eines Anwendungsdienstes. Er ist weder das Image noch der Container selbst.

Mögliche Konfigurationselemente:

- image bzw. build
- ports
- volumes
- networks
- environment
- restart

Ein Service kann mit einem oder mehreren Container-Exemplaren betrieben werden.

### Image

Ein Image ist die Vorlage, auf deren Grundlage Container erstellt werden:

image → gibt das zu verwendende Image an.
build → beschreibt, wie ein Image beispielsweise anhand eines Dockerfiles erstellt 
        werden soll.

Beide Angaben können gemeinsam verwendet werden.

### Container

Ein Container ist eine konkrete Laufzeitinstanz auf Grundlage eines Images. Docker-Compose erstellt und verwaltet die Container entsprechend der Service-Konfiguration. Ein Container besitzt einen eigenen beschreibbaren Layer. Dieser ist vom Image und von eingebundenen Mounts zu unterscheiden.

### Netzwerk

Compose kann Netzwerke deklarieren und Services mit ihnen verbinden. Standardmäßig wird für ein Compose-Projekt ein eigenes Netzwerk erstellt, sofern die Netzwerkkonfiguration nicht entsprechend angepasst wird.
In einem gemeinsamen benutzerdefinierten Bridge-Netzwerk können Services in der Regel über ihre Servicenamen miteinander kommunizieren. Eine Veröffentlichung von Ports auf dem Host ist für rein interne Container-Kommunikation nicht erforderlich.

### Volume

Volumes ermöglichen die persistente Speicherung von Daten unabhängig vom Lebenszyklus eines Containers. Im Taskmanager wird die Datenbankdatei unter '/data/taskmanager.db' gespeichert. Der zugehörige Storage soll über ein Docker-Volume bereitgestellt werden.

## Deklaratives Konfigurationsmodell

Compose beschreibt den gewünschten Zustand des Anwendungsstacks in einer YAML-Konfiguration. Dabei werden nicht einfach bestehende 'docker run'-Befehle gesammelt. Stattdessen werden die gewünschten Eigenschaften der Services und ihrer Ressourcen deklariert. Compose interpretiert diese Beschreibung und verwendet die Docker-Engine, um die benötigten Ressourcen zu erstellen oder anzupassen.

## Lebenszyklus und Persistenz

Beim Stoppen eines Containers bleiben der Container und sein beschreibbarer Layer grundsätzlich erhalten. Beim Entfernen des Containers wird auch sein beschreibbarer Layer entfernt. Ein vorhandenes Image und ein separates Docker-Volume bleiben beim Löschen eines Containers grundsätzlich erhalten, sofern sie nicht unabhängig davon entfernt werden.

Ressource	                    | Container stoppen | Container entfernen
-----------------------------------------------------------------------------------
Image	                        | bleibt erhalten	| bleibt grundsätzlich erhalten
Container	                    | bleibt bestehen	| wird entfernt
Beschreibbarer Container-Layer	| bleibt erhalten	| wird entfernt
Docker Volume	                | bleibt erhalten	| bleibt grundsätzlich erhalten
Datenbankdatei im Volume	    | bleibt erhalten	| bleibt erhalten

Beim erneuten Start eines Services kann Compose vorhandene Container starten oder falls erforderlich Container neu erstellen. Das konkrete Verhalten hängt vom verwendeten Befehl und der vorhandenen Konfiguration ab.

Wichtig: Ein erfolgreicher Containerstart bedeutet nicht automatisch, dass die Anwendung vollständig betriebsbereit ist.

## Abgrenzung der Zuständigkeiten

Komponente      | Aufgabe
-------------------------------------------------------------------------------------
Docker-Compose	| Deklariert und verwaltet den zusammengehörigen Anwendungsstack
Docker-Engine	| Stellt die Container-Laufzeit und die zugehörigen Docker-Ressourcen  
                | bereit
Image	        | Liefert die Grundlage für einen Container
Container	    | Führt die Anwendung in einer isolierten Laufzeitumgebung aus
Docker-Volume	| Speichert Daten unabhängig vom Container-Lebenszyklus

Compose vereinfacht die Verwaltung des Stacks, ersetzt aber weder die Docker-Engine noch die erforderlichen Architektur- und Sicherheitsentscheidungen.

## Geplante Anwendung im Taskmanager-Projekt

Die vorhandene Anwendung besteht aus einer Flask-Anwendung und einer dateibasierten SQLite-Datenbank.

Aktuelles Zielmodell:

Anwendung      → Flask, einschließlich Templates und statischer Dateien
Anwendungscode → /app
Datenbankdatei → /data/taskmanager.db
Persistenz     → Docker-Volume
Netzwerk       → Kommunikation entsprechend den tatsächlichen Anforderungen

SQLite ist derzeit kein eigenständiger Netzwerkdienst. Die Flask-Anwendung greift direkt über Python auf die Datenbankdatei zu. Ein separater Datenbankcontainer ist deshalb für die aktuelle Architektur nicht erforderlich. Ein späterer Wechsel zu einer Datenbank wie PostgreSQL würde eine bewusste Architekturänderung darstellen.

## Weiteres Vorgehen

Die praktische Umsetzung erfolgt schrittweise anhand der vorhandenen Anwendung.

Geplant sind:

- Compose-Projekt und Service-Konfiguration erstellen
- Vorhandenes Dockerfile in die Konfiguration einbinden
- Netzwerk- und Storage-Konfiguration untersuchen
- Anwendung mit Compose starten und testen
- Container-Lifecycle und Datenpersistenz praktisch überprüfen
- Konfiguration und Testergebnisse dokumentieren

Die Praxisdokumentation hält anschließend insbesondere die tatsächlich verwendete Konfiguration, relevante Entscheidungen, ausgeführte Befehle, Testergebnisse und aufgetretene Fehler fest.