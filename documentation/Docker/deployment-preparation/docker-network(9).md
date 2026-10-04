# Docker-Netzwerke – Grundlagen, Bridge-Netzwerk und Container-Kommunikation

Nachdem Container-Dateisystem, Image-Layer, persistenter Storage und Volume-Mounts untersucht wurden, beginnt mit Docker-Networking ein weiterer zentraler Bereich des Containerbetriebs.

Bisher wurde der Taskmanager hauptsächlich aus Sicht von Anwendung, Dateisystem und Storage betrachtet. Mit Docker-Netzwerken kommt nun die Kommunikation zwischen Prozessen und Containern hinzu.

Das bisherige Modell:

Dockerfile
    ↓
  Image
    ↓
 Container
    ↓
 Anwendung

wird um die Netzwerkebene erweitert:

Docker Host
    │
    ▼
Docker Netzwerk
    │
    ├── Container A
    │
    └── Container B

Dabei ist insbesondere zu unterscheiden zwischen:

- dem Netzwerk innerhalb eines Containers
- der Kommunikation zwischen mehreren Containern
- der Kommunikation zwischen Container und Docker-Host
- der Veröffentlichung eines Container-Ports auf dem Host
- der Namensauflösung innerhalb eines Docker-Netzwerks

## Netzwerkinterfaces eines Containers

Als erster Test wurde ein interaktiver Alpine-Container gestartet mit dem folgenden Befehl:

```bash
docker run --rm -it alpine sh
```

Innerhalb des Containers wurde zunächst der Hostname abgefragt:

```bash
hostname
```

Beispielhafte Ausgabe:

fe33d37704d1

Anschließend wurden die vorhandenen Netzwerkinterfaces betrachtet:

```bash
ip addr
```

Dabei wurden insbesondere zwei Interfaces sichtbar:

1: lo:
    inet 127.0.0.1/8

2: eth0@if5:
    inet 172.17.0.2/16

Damit besitzt der Container mindestens:

lo
│
└── 127.0.0.1

und:

eth0
│
└── 172.17.0.2/16

Das Loopback-Interface 'lo' dient der Kommunikation innerhalb des eigenen Netzwerk-Namespaces. Das Interface eth0 stellt dagegen die Verbindung des Containers zum Docker-Netzwerk bereit.
Damit wurde praktisch bestätigt, dass ein Container aus Netzwerksicht nicht einfach nur „ein Prozess mit einer Portnummer“ ist. Er besitzt eine eigene Netzwerkkonfiguration mit eigenen Interfaces und eigenen IP-Adressen.

## Die Container-IP-Adresse

Im ersten Testcontainer wird folgende IPv4-Adresse festgestellt:

172.17.0.2/16

Das zugehörige Netzwerk lautet:

172.17.0.0/16

Damit liegen beispielsweise folgende Adressen innerhalb dieses Netzwerks:

172.17.0.1
172.17.0.2
172.17.0.3
...

Die konkrete Vergabe der Adressen übernimmt Docker über die Netzwerkverwaltung. Die Adresse 172.17.0.2 ist dabei die IP-Adresse des Containers innerhalb dieses Docker-Netzwerks.

## Routing innerhalb des Containers

Mit:

```bash
ip route
```

wird folgende Routingtabelle betrachtet:

default via 172.17.0.1 dev eth0
172.17.0.0/16 dev eth0 scope link src 172.17.0.2

Damit sind zwei wichtige Informationen sichtbar. Für das lokale Docker-Netzwerk 172.17.0.0/16 wird das Interface eth0 verwendet. Für Ziele, die nicht direkt in diesem Netzwerk liegen, existiert eine Default Route:

default via 172.17.0.1

Die Adresse 172.17.0.1 stellt in diesem Docker-Netzwerk das Gateway dar:

Container
172.17.0.2
    │
    │ Default Route
    ▼
172.17.0.1
    │
    ▼
Docker-Netzwerkinfrastruktur

## Praktischer Test des Gateways

Das Gateway wird mit dem folgenden Befehl direkt aus dem Container angepingt:

```bash
ping -c 3 172.17.0.1
```

Die Pakete wurden erfolgreich beantwortet:

3 packets transmitted, 3 packets received, 0% packet loss

Damit wurde praktisch bestätigt, dass der Container das Gateway innerhalb des Docker-Netzwerks erreichen kann. Anschließend wird die eigene Container-IP angepingt:

```bash
ping -c 3 172.17.0.2
```

Auch dieser Test war erfolgreich. Hierbei handelt es sich jedoch um einen wichtigen Sonderfall:

172.17.0.2
     │
     ▼
eigener Container

Der Container kommuniziert dabei mit seiner eigenen Netzwerkadresse. Die beobachteten niedrigen Laufzeiten waren daher nicht mit einer Kommunikation zu einem anderen Netzwerkgerät gleichzusetzen.

Mit:

```bash
docker network ls
```

wurden die vorhandenen Docker-Netzwerke angezeigt:

NETWORK ID     NAME      DRIVER    SCOPE
3ad10c4cc9ec   bridge    bridge    local
f9b368c2b6a7   host      host      local
7bc37d6e554c   none      null      local

Dabei fällt insbesondere das Netzwerk 'bridge' auf. Docker stellt standardmäßig mehrere Netzwerke bereit. Für die weitere Untersuchung ist insbesondere das Netzwerk 'bridge' relevant.

Der Eintrag:

NAME      bridge
DRIVER    bridge

bedeutet, dass für dieses Netzwerk der Docker-bridge-Driver verwendet wird. Der Begriff 'bridge' bezeichnet dabei sowohl den Namen des Standardnetzwerks als auch den verwendeten Netzwerk-Driver. Inhaltlich müssen diese beiden Ebenen jedoch unterschieden werden. Ein Driver beschreibt die technische Art, wie Docker das Netzwerk bereitstellt. Ein konkretes Netzwerk besitzt dagegen zusätzlich eine eigene Konfiguration.

## Netzwerkadressierung des Standard-Bridge-Netzwerks

Mit 'docker inspect' wurde die IPAM-Konfiguration des Bridge-Netzwerks untersucht.

Dabei war unter anderem sichtbar:

"IPAM": {
    "Driver": "default",
    "Config": [
        {
            "Subnet": "172.17.0.0/16",
            "Gateway": "172.17.0.1"
        }
    ]
}

Damit konnte die bereits innerhalb des Containers beobachtete Konfiguration von der Docker-Seite aus nachvollzogen werden:

Subnetz:
172.17.0.0/16

Gateway:
172.17.0.1

Damit ergibt sich:

Docker-bridge
│
├── Subnetz: 172.17.0.0/16
│
├── Gateway: 172.17.0.1
│
└── Container
       └── 172.17.0.2

Die Werte aus ```bash ip addr ``` und ```bash ip route ``` innerhalb des Containers stimmen damit mit der Netzwerkdefinition überein, die Docker für das Netzwerk bereitstellt.

## Container im Docker-Netzwerk

Die Netzwerkdefinition enthält außerdem eine Liste der aktuell angeschlossenen Container.

Beispielsweise:

"Containers": {
    "...": {
        "Name": "network-test",
        "EndpointID": "...",
        "MacAddress": "2e:c0:59:14:04:9b",
        "IPv4Address": "172.17.0.2/16"
    }
}

Hier sind mehrere Informationen über die Verbindung des Containers mit dem Docker-Netzwerk sichtbar:

- Name des Containers
- EndpointID
- MAC-Adresse
- IPv4-Adresse
- IPv6-Adresse

Damit lässt sich der Container nicht nur über seinen Namen, sondern auch über seine Netzwerkidentität innerhalb des Docker-Netzwerks nachvollziehen.

## Vergabe von IP-Adressen

Anschließend wurde ein zweiter Container in dasselbe Netzwerk aufgenommen.
Dabei erhielt der zweite Container:

172.17.0.3/16

Die Beobachtung passte damit zunächst zur erwarteten Vergabe:

network-test
    └── 172.17.0.2

network-test-2
    └── 172.17.0.3

Zuvor war bereits beobachtet worden, dass ein gelöschter Container die verwendete Adresse wieder freigeben kann. Die Vergabe von Container-IP-Adressen sollte allerdings nicht als dauerhafte Zuordnung verstanden werden.
Insbesondere sollte sich eine Anwendung nicht darauf verlassen, dass ein bestimmter Container dauerhaft dieselbe IP-Adresse besitzt. Container können gelöscht und neu erstellt werden, wodurch sich die Netzwerkidentität ändern kann.
Für die spätere Kommunikation zwischen Diensten ist deshalb die Verwendung von Docker-internen Namen innerhalb benutzerdefinierter Netzwerke wesentlich geeigneter als das Festhalten an dynamisch vergebenen Container-IP-Adressen.

## Kommunikation zwischen zwei Containern

Nachdem sich zwei Container im selben Docker-Netzwerk befinden, wird die direkte Kommunikation getestet.

Von network-test:

```bash
docker exec network-test ping -c 3 172.17.0.3
```

Von network-test-2:

```bash
docker exec network-test-2 ping -c 3 172.17.0.2
```

Beide Tests waren erfolgreich.
Damit wurde praktisch bestätigt:

network-test
172.17.0.2
      │
      │ Docker-Netzwerk
      ▼
network-test-2
172.17.0.3

Die Container können innerhalb desselben Docker-Netzwerks direkt miteinander kommunizieren. Dabei war kein Host-Port-Mapping erforderlich. Dies ist ein wichtiger Unterschied zur zuvor untersuchten Kommunikation vom Host zum Taskmanager:

Host → Container über 3001:5000

Bei der Kommunikation zwischen zwei Containern im selben Netzwerk wird dagegen direkt das Docker-Netzwerk verwendet.

## Containername und IP-Adresse

Nachdem die direkte Kommunikation über IP-Adressen funktioniert hat, ergab sich die Frage, ob Container auch über ihren Namen erreicht werden können. Diese Überlegung führt zur Untersuchung von Docker-DNS. Zunächst wird versucht, die Container über ihre Namen anzupingen. Im automatisch bereitgestellten Standardnetzwerk 'bridge' funktionierte dies jedoch nicht:

```bash
ping: bad address 'network-test'

ping: bad address 'network-test-2'
```

Damit wird ein wichtiger Unterschied sichtbar. Obwohl die Container über ihre IP-Adressen erreichbar waren, wurde der Containername im Standardnetzwerk nicht automatisch in eine IP-Adresse aufgelöst.

## Untersuchung von '/etc/resolv.conf'

Innerhalb des Containers wurde anschließend die DNS-Konfiguration betrachtet:

```bash
docker exec network-test cat /etc/resolv.conf
```

Dabei war unter anderem sichtbar:

nameserver 192.168.1.1
search router.ip

Der Container verwendet damit einen DNS-Server, der aus Sicht des Containers über die konfigurierte DNS-Konfiguration erreichbar ist. Die Untersuchung zeigte jedoch gleichzeitig, dass der bisher verwendete Standard-Bridge-Modus nicht automatisch dieselbe containerbezogene Namensauflösung bereitstellt wie ein benutzerdefiniertes Docker-Netzwerk.

## Untersuchung von '/etc/hosts'

Zusätzlich wurde:

```bash
docker exec network-test cat /etc/hosts
```

ausgeführt. Die Datei enthielt unter anderem:

127.0.0.1    localhost
::1          localhost ip6-localhost ip6-loopback
fe00::       ip6-localnet
ff00::       ip6-mcastprefix
ff02::1      ip6-allnodes
ff02::2      ip6-allrouters
172.17.0.2   396271777b88

Auffällig ist hierbei, dass der Containername 'network-test' dort nicht als Auflösungseintrag für die eigene Container-IP vorhanden war. Damit konnte die fehlende Namensauflösung über '/etc/hosts' nachvollzogen werden.

## Benutzerdefiniertes Bridge-Netzwerk

Anschließend wird ein eigenes Docker-Netzwerk für den Taskmanager verwendet. Das Netzwerk wird mit folgendem Befehl erstellt:

```bash
docker network create taskmanager-net
```

Das Netzwerk 'taskmanager-net' besitzt ebenfalls den Driver 'bridge'. Damit entstand zunächst die Frage, warum ein benutzerdefiniertes Bridge-Netzwerk Namensauflösung zwischen Containern ermöglicht, obwohl auch das Standardnetzwerk 'bridge' denselben Driver verwendet.
Der entscheidende Unterschied liegt darin, dass der bridge-Driver nicht bedeutet, dass jedes konkrete Bridge-Netzwerk exakt dieselben Docker-Funktionen und Standardeinstellungen besitzt.

Vereinfacht:

Docker-Netzwerk
│
├── Standardnetzwerk "bridge"
│     └── Driver: bridge
│
└── Benutzerdefiniertes Netzwerk "taskmanager-net"
      └── Driver: bridge

Beide Netzwerke verwenden denselben Driver. Das benutzerdefinierte Netzwerk stellt jedoch zusätzliche Docker-Funktionen bereit, insbesondere die integrierte Namensauflösung zwischen angeschlossenen Containern. Dadurch kann die Kommunikation in einem benutzerdefinierten Netzwerk über Namen erfolgen.

Vereinfacht:

dns-test-1
    │
    │ Name: dns-test-2
    ▼
Docker-DNS
    │
    ▼
IP-Adresse von dns-test-2
    │
    ▼
dns-test-2

Dies ist insbesondere für Anwendungen mit mehreren Containern wichtig. Ein Dienst muss dadurch nicht die aktuell zugewiesene IP-Adresse eines anderen Containers kennen.

## Containername statt fester IP-Adresse

Die Verwendung von Namen ist für einen mehrteiligen Anwendungsstack wesentlich sinnvoller als die direkte Verwendung dynamischer Container-IP-Adressen. Beispielsweise kann später ein Anwendungcontainer mit einem Datenbankcontainer kommunizieren:

taskmanager
     │
     │ database
     ▼
database

Der Anwendungscode muss dadurch nicht beispielsweise 172.18.0.3 als feste Datenbankadresse kennen. Stattdessen wird der Name des Dienstes verwendet. Dies ist eine wichtige Grundlage für Docker-Compose, da Compose später mehrere Dienste und deren Netzwerke gemeinsam verwalten kann.

## Benutzerdefiniertes Netzwerk und Taskmanager

Das erstellte Netzwerk 'taskmanager-net' verwendet den bridge-Driver. Die Container des Tests werden diesem Netzwerk zugeordnet und erhalten Adressen aus einem eigenen Subnetz, beispielsweise:

172.18.0.0/16

Damit besteht eine klare Trennung zum Standardnetzwerk:

Standard-bridge
172.17.0.0/16

taskmanager-net
172.18.0.0/16

Die Verwendung eines eigenen Netzwerks ermöglicht damit nicht nur eine separate IP-Adressierung, sondern auch die für mehrteilige Anwendungen wichtige Docker-interne Namensauflösung.

## localhost innerhalb eines Containers

Ein weiterer wichtiger Lernpunkt war die Bedeutung von localhost. Aus einem Container heraus wurde:

```bash
docker exec dns-test-1 ping -c 3 localhost
```

ausgeführt.

Die Ausgabe begann mit:

PING localhost (::1)

Damit wurde die IPv6-Loopback-Adresse ::1 verwendet. Bereits beim ersten Netzwerktest war innerhalb des Containers die IPv4-Loopback-Adresse (127.0.0.1) sichtbar. Beide bezeichnen aus Sicht des jeweiligen Netzwerk-Stacks das lokale System.

Im Container bedeutet localhost daher:

localhost
    │
    ▼
dieser Container

und nicht automatisch:

localhost
    │
    ▼
Docker Host

Nachweis über den Hostnamen des Containers

Zur weiteren Überprüfung wird der folgende Befehl im Container ausgeführt:

```bash
docker exec dns-test-1 hostname
```

Die Ausgabe lautete:

9c6e5b3f75dd

Anschließend wird die Containerliste betrachtet mit:

```bash
docker ps
```

Dort wird sichtbar:

CONTAINER ID   ...   NAMES
9c6e5b3f75dd   ...   dns-test-1

Der Hostname innerhalb des Containers stimmte damit mit der Container-ID überein. Damit kann die bereits anhand des Loopback-Interfaces formulierte Annahme zusätzlich praktisch überprüft werden:

dns-test-1
    │
    ├── hostname → 946e56cf75dd
    │
    └── docker ps
           └── Container ID → 946e56cf75dd

Der Zugriff auf localhost blieb damit innerhalb des Containers.

## Ausblick

Der aktuelle Taskmanager besteht bisher vereinfacht aus:

Browser
   │
   ▼
Host:3001
   │
   │ Port Publishing
   ▼
Taskmanager-Container:5000
   │
   ▼
Flask
   │
   ▼
/data
   │
   ▼
Docker Volume
taskmanager-data

Mit einer separaten Datenbank als eigenständigem Dienst würde das Modell erweitert:

                    Docker-Host
                         │
                         │ Port Publishing
                         ▼
                    Taskmanager
                    Container
                         │
                         │ taskmanager-net
                         ▼
                    Datenbank
                    Container
                         │
                         ▼
                    Daten-Volume

Die Anwendung würde die Datenbank dabei über deren Docker-interne Netzwerkadresse beziehungsweise deren Dienstnamen erreichen und nicht über einen zufällig vergebenen Container-IP-Wert.

Damit verbinden sich die bisher einzeln untersuchten Bereiche:

Container
    │
    ├── Netzwerk
    │      │
    │      └── Container-zu-Container-Kommunikation
    │
    ├── Storage
    │      │
    │      └── Docker-Volume
    │
    └── Port Publishing
           │
           └── Zugriff vom Host

Diese Kombination aus mehreren Containern, einem gemeinsamen Netzwerk, persistentem Storage und zentraler Konfiguration bildet später die Grundlage für Docker-Compose.

Das bisherige Docker-Modell auf Netzwerkebene:

                         Docker Host
                              │
             ┌────────────────┴────────────────┐
             │                                 │
             ▼                                 ▼
       Host-Dateisystem                  Docker Netzwerk
             │                           taskmanager-net
             │                                 │
             │                    ┌────────────┴────────────┐
             │                    │                         │
             ▼                    ▼                         ▼
         VScode            Taskmanager              Datenbank
                            Container                Container
                                │                         │
                                │                         │
                                └──── Container-Netz ─────┘
                                │
                                ▼
                         Docker Volume
                         taskmanager-data

Damit ist der nächste logische Lernschritt die Untersuchung mehrerer Dienste als zusammengehöriges System. Insbesondere soll zunächst die Kommunikation zwischen Anwendung und Datenbank praktisch nachvollzogen werden. Anschließend kann daraus schrittweise Docker-Compose als Werkzeug zur gemeinsamen Definition von Containern, Netzwerken, Volumes und Konfiguration entstehen.