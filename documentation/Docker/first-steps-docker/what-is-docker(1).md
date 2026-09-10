# Was ist Docker?

Docker ist eine Plattform zur Entwicklung, Bereitstellung und Ausführung von Anwendungen in Containern. Container ermöglichen es, eine Anwendung zusammen mit ihren benötigten Abhängigkeiten in einer isolierten und reproduzierbaren Umgebung auszuführen.

Ein Container ist eine laufende Instanz eines Docker-Images. Ein Image beschreibt dabei den Ausgangszustand und die benötigten Bestandteile eines Containers und dient als Vorlage, aus der ein oder mehrere Container erstellt werden können. 
Ein einmal erstelltes Image wird dabei grundsätzlich nicht direkt verändert. Änderungen werden üblicherweise durch das Erstellen eines neuen Images bzw. neuer Image-Layer abgebildet. Im Gegensatz zu einer virtuellen Maschine enthält ein Container kein vollständiges eigenes Betriebssystem und keinen eigenen Kernel. Container nutzen den Kernel des Hostsystems und sind dadurch wesentlich ressourcenärmer und schneller zu starten als virtuelle Maschinen.

## Die grundlegenden Bestandteile von Docker

DOCKER IMAGE → Vorlage für einen Container mit Anwendung und benötigten Dateien bzw. Abhängigkeiten. Es enthält also die Dateien, Programme, Bibliotheken und Konfigurationen, die eine Anwendung innerhalb des Containers benötigt.

DOCKER CONTAINER → Laufende Instanz eines Images.

DOCKER ENGINE → Software auf dem Hostsystem, die Images und Container verwaltet und deren Ausführung ermöglicht. Sie stellt die Infrastruktur bereit.

DOCKERFILE → Bauanleitung für einen Container

DOCKER REGISTRY → Speicherort für Images, aus dem Images heruntergeladen bzw. in den Images veröffentlicht werden können. Eine bekannte öffentliche Registry ist Docker Hub.

Der grundlegende Ablauf ist:

Dockerfile
    │
    │ docker build
    ▼
Docker Image
    │
    │ docker run
    ▼
Container
    │
    ▼
Prozess

Images können lokal vorhanden sein oder bei Bedarf aus einer Registry heruntergeladen werden. Container können gestartet, gestoppt, entfernt und neu erstellt werden. Dadurch lassen sich Anwendungen reproduzierbar bereitstellen und betreiben.

Docker verwendet verschiedene Linux-Mechanismen zur Isolation und Ressourcenverwaltung. Dazu gehören unter anderem Namespaces, cgroups und Sicherheitsmechanismen wie seccomp und AppArmor.

Ein wesentlicher Vorteil von Docker ist die Reproduzierbarkeit. Die benötigte Umgebung einer Anwendung kann als Image definiert und auf unterschiedlichen Systemen wieder bereitgestellt werden. Dadurch werden Unterschiede zwischen Entwicklungs-, Test- und Produktionsumgebungen reduziert.

Docker wird unter anderem für Webanwendungen, Entwicklungs- und Testumgebungen sowie CI/CD-Pipelines eingesetzt. In Verbindung mit Kubernetes können viele Container automatisiert bereitgestellt, überwacht und verwaltet werden.

Für die Systemintegration ist Docker insbesondere relevant, weil Anwendungen standardisiert, reproduzierbar und mit geringem Ressourcenbedarf betrieben werden können. Gleichzeitig müssen Container, Images, Speicher, Netzwerke und deren Lebenszyklus administriert und überwacht werden.

Der Container bekommt eine isolierte Sicht auf Ressourcen des Hosts und verwendet den Kernel des Hostsystems. Das ist einer der entscheidenden Unterschiede zur VM.

┌──────────────────────────────┐
│          Host Linux          │
│                              │
│         Linux Kernel         │
│              ↑               │
│      ┌───────┴────────┐      │
│      │ Docker Engine  │      │
│      └───────┬────────┘      │
│              │               │
│   ┌──────────┴───────────┐   │
│   │      Container       │   │
│   │                      │   │
│   │ Flask + Python       │   │
│   │ benötigte Libraries  │   │
│   │ Dateien              │   │
│   └──────────────────────┘   │
└──────────────────────────────┘