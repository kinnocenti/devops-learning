# Docker-Netzwerke – Grundlagen, Bridge-Netzwerk und Container-Kommunikation

Nachdem Container-Dateisystem, Image-Layer, persistenter Storage und Volume-Mounts untersucht wurden, beginnt mit Docker Networking ein weiterer zentraler Bereich des Containerbetriebs.

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
- der Kommunikation zwischen Container und Docker Host
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

Das Loopback-Interface lo dient der Kommunikation innerhalb des eigenen Netzwerk-Namespaces.

Das Interface eth0 stellt dagegen die Verbindung des Containers zum Docker-Netzwerk bereit.

Damit wurde praktisch bestätigt, dass ein Container aus Netzwerksicht nicht einfach nur „ein Prozess mit einer Portnummer“ ist. Er besitzt eine eigene Netzwerkkonfiguration mit eigenen Interfaces und eigenen IP-Adressen.
Die Container-IP-Adresse

Im ersten Testcontainer wurde folgende IPv4-Adresse festgestellt:

172.17.0.2/16

Die Schreibweise /16 beschreibt die Präfixlänge des Netzwerks.

Das zugehörige Netzwerk lautet:

172.17.0.0/16

Damit liegen beispielsweise folgende Adressen innerhalb dieses Netzwerks:

172.17.0.1
172.17.0.2
172.17.0.3
...

Die konkrete Vergabe der Adressen übernimmt Docker über die Netzwerkverwaltung.

Die Adresse 172.17.0.2 ist dabei die IP-Adresse des Containers innerhalb dieses Docker-Netzwerks.
Routing innerhalb des Containers

Mit:

ip route

wurde folgende Routingtabelle betrachtet:

default via 172.17.0.1 dev eth0
172.17.0.0/16 dev eth0 scope link src 172.17.0.2

Damit sind zwei wichtige Informationen sichtbar.

Für das lokale Docker-Netzwerk:

172.17.0.0/16

wird das Interface eth0 verwendet.

Für Ziele, die nicht direkt in diesem Netzwerk liegen, existiert eine Default Route:

default via 172.17.0.1

Die Adresse 172.17.0.1 stellt in diesem Docker-Netzwerk das Gateway dar.

Dabei ist wichtig, die Bezeichnung Gateway nicht mit einem physischen Heim- oder Unternehmensrouter gleichzusetzen. Das Gateway gehört hier zur Docker-Netzwerkinfrastruktur.

Der Vergleich mit einem klassischen IP-Netzwerk ist dennoch hilfreich:

Container
172.17.0.2
    │
    │ Default Route
    ▼
172.17.0.1
    │
    ▼
Docker-Netzwerkinfrastruktur

Praktischer Test des Gateways

Das Gateway wurde direkt aus dem Container angepingt:

ping -c 3 172.17.0.1

Die Pakete wurden erfolgreich beantwortet:

3 packets transmitted, 3 packets received, 0% packet loss

Damit wurde praktisch bestätigt, dass der Container das Gateway innerhalb des Docker-Netzwerks erreichen kann.

Anschließend wurde die eigene Container-IP angepingt:

ping -c 3 172.17.0.2

Auch dieser Test war erfolgreich.

Hierbei handelt es sich jedoch um einen wichtigen Sonderfall:

172.17.0.2
     │
     ▼
eigener Container

Der Container kommuniziert dabei mit seiner eigenen Netzwerkadresse.

Die beobachteten niedrigen Laufzeiten waren daher nicht mit einer Kommunikation zu einem anderen Netzwerkgerät gleichzusetzen.
TTL als zusätzliche Beobachtung

Bei den Ping-Antworten wurde unter anderem folgende Information angezeigt:

ttl=64

Ein Wert von 64 ist häufig bei Linux-Systemen als initialer TTL-Wert zu beobachten.

Der TTL-Wert ist jedoch kein eindeutiger Beweis für ein Linux-System, da der Wert konfiguriert werden kann und sich durch Routing verändern kann.

Damit eignet sich TTL als zusätzliche technische Beobachtung, sollte aber nicht isoliert zur Identifikation eines Betriebssystems verwendet werden.
Docker-Netzwerke

Mit:

docker network ls

wurden die vorhandenen Docker-Netzwerke angezeigt:

NETWORK ID     NAME      DRIVER    SCOPE
4ad19c4ca8ec   bridge    bridge    local
f9b263c236a7   host      host      local
7bc87e6e054c   none      null      local

Dabei fällt insbesondere das Netzwerk bridge auf.

Docker stellt standardmäßig mehrere Netzwerke bereit. Für die weitere Untersuchung ist insbesondere das Netzwerk bridge relevant.

Der Eintrag:

NAME      bridge
DRIVER    bridge

bedeutet, dass für dieses Netzwerk der Docker-bridge-Driver verwendet wird.

Der Begriff bridge bezeichnet dabei sowohl den Namen des Standardnetzwerks als auch den verwendeten Netzwerk-Driver. Inhaltlich müssen diese beiden Ebenen jedoch unterschieden werden.

Ein Driver beschreibt die technische Art, wie Docker das Netzwerk bereitstellt.

Ein konkretes Netzwerk besitzt dagegen zusätzlich eine eigene Konfiguration.
Netzwerkadressierung des Standard-Bridge-Netzwerks

Mit docker inspect wurde die IPAM-Konfiguration des Bridge-Netzwerks untersucht.

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

Docker bridge
│
├── Subnetz: 172.17.0.0/16
│
├── Gateway: 172.17.0.1
│
└── Container
       └── 172.17.0.2

Die Werte aus ip addr und ip route innerhalb des Containers stimmen damit mit der Netzwerkdefinition überein, die Docker für das Netzwerk bereitstellt.
Container im Docker-Netzwerk

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

    Name des Containers

    EndpointID

    MAC-Adresse

    IPv4-Adresse

    IPv6-Adresse

Damit lässt sich der Container nicht nur über seinen Namen, sondern auch über seine Netzwerkidentität innerhalb des Docker-Netzwerks nachvollziehen.
Vergabe von IP-Adressen

Anschließend wurde ein zweiter Container in dasselbe Netzwerk aufgenommen.

Dabei erhielt der zweite Container:

172.17.0.3/16

Die Beobachtung passte damit zunächst zur erwarteten Vergabe:

network-test
    └── 172.17.0.2

network-test-2
    └── 172.17.0.3

Zuvor war bereits beobachtet worden, dass ein gelöschter Container die verwendete Adresse wieder freigeben kann.

Die Vergabe von Container-IP-Adressen sollte allerdings nicht als dauerhafte Zuordnung verstanden werden.

Insbesondere sollte sich eine Anwendung nicht darauf verlassen, dass ein bestimmter Container dauerhaft dieselbe IP-Adresse besitzt. Container können gelöscht und neu erstellt werden, wodurch sich die Netzwerkidentität ändern kann.

Für die spätere Kommunikation zwischen Diensten ist deshalb die Verwendung von Docker-internen Namen innerhalb benutzerdefinierter Netzwerke wesentlich geeigneter als das Festhalten an dynamisch vergebenen Container-IP-Adressen.
Kommunikation zwischen zwei Containern

Nachdem sich zwei Container im selben Docker-Netzwerk befanden, wurde die direkte Kommunikation getestet.

Von network-test:

docker exec network-test ping -c 3 172.17.0.3

Von network-test-2:

docker exec network-test-2 ping -c 3 172.17.0.2

Beide Tests waren erfolgreich und zeigten:

3 packets transmitted
3 packets received
0% packet loss

Damit wurde praktisch bestätigt:

network-test
172.17.0.2
      │
      │ Docker-Netzwerk
      ▼
network-test-2
172.17.0.3

Die Container können innerhalb desselben Docker-Netzwerks direkt miteinander kommunizieren.

Dabei war kein Host-Port-Mapping erforderlich.

Dies ist ein wichtiger Unterschied zur zuvor untersuchten Kommunikation vom Host zum Taskmanager:

Host → Container

über:

3001:5000

Bei der Kommunikation zwischen zwei Containern im selben Netzwerk wird dagegen direkt das Docker-Netzwerk verwendet.
Containername und IP-Adresse

Nachdem die direkte Kommunikation über IP-Adressen funktioniert hatte, entstand die Frage, ob Container auch über ihren Namen erreicht werden können.

Diese Überlegung führte zur Untersuchung von Docker-DNS.

Zunächst wurde versucht, die Container über ihre Namen anzupingen. Im automatisch bereitgestellten Standardnetzwerk bridge funktionierte dies jedoch nicht:

ping: bad address 'network-test'

bzw.:

ping: bad address 'network-test-2'

Damit war ein wichtiger Unterschied sichtbar.

Obwohl die Container über ihre IP-Adressen erreichbar waren, wurde der Containername im Standardnetzwerk nicht automatisch in eine IP-Adresse aufgelöst.
Untersuchung von /etc/resolv.conf

Innerhalb des Containers wurde anschließend die DNS-Konfiguration betrachtet:

docker exec network-test cat /etc/resolv.conf

Dabei war unter anderem sichtbar:

nameserver 192.168.2.1
search speedport.ip

Der Container verwendet damit einen DNS-Server, der aus Sicht des Containers über die konfigurierte DNS-Konfiguration erreichbar ist.

Die Datei wurde von Docker erzeugt.

Die Untersuchung zeigte jedoch gleichzeitig, dass der bisher verwendete Standard-Bridge-Modus nicht automatisch dieselbe containerbezogene Namensauflösung bereitstellt wie ein benutzerdefiniertes Docker-Netzwerk.
Untersuchung von /etc/hosts

Zusätzlich wurde:

docker exec network-test cat /etc/hosts

ausgeführt.

Die Datei enthielt unter anderem:

127.0.0.1    localhost
::1          localhost ip6-localhost ip6-loopback
fe00::       ip6-localnet
ff00::       ip6-mcastprefix
ff02::1      ip6-allnodes
ff02::2      ip6-allrouters
172.17.0.2   396271777b88

Auffällig ist hierbei, dass der Containername network-test dort nicht als Auflösungseintrag für die eigene Container-IP vorhanden war.

Damit konnte die fehlende Namensauflösung über /etc/hosts nachvollzogen werden.
Benutzerdefiniertes Bridge-Netzwerk

Anschließend wurde ein eigenes Docker-Netzwerk für den Taskmanager verwendet.

Das Netzwerk taskmanager-net besitzt ebenfalls den Driver:

bridge

Damit entstand zunächst die Frage, warum ein benutzerdefiniertes Bridge-Netzwerk Namensauflösung zwischen Containern ermöglicht, obwohl auch das Standardnetzwerk bridge denselben Driver verwendet.

Der entscheidende Unterschied liegt darin, dass der bridge-Driver nicht bedeutet, dass jedes konkrete Bridge-Netzwerk exakt dieselben Docker-Funktionen und Standardeinstellungen besitzt.

Vereinfacht:

Docker-Netzwerk
│
├── Standardnetzwerk "bridge"
│     └── Driver: bridge
│
└── Benutzerdefiniertes Netzwerk "taskmanager-net"
      └── Driver: bridge

Beide Netzwerke verwenden denselben Driver.

Das benutzerdefinierte Netzwerk stellt jedoch zusätzliche Docker-Funktionen bereit, insbesondere die integrierte Namensauflösung zwischen angeschlossenen Containern.

Dadurch kann die Kommunikation in einem benutzerdefinierten Netzwerk über Namen erfolgen.

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

Dies ist insbesondere für Anwendungen mit mehreren Containern wichtig.

Ein Dienst muss dadurch nicht die aktuell zugewiesene IP-Adresse eines anderen Containers kennen.
Containername statt fester IP-Adresse

Die Verwendung von Namen ist für einen mehrteiligen Anwendungsstack wesentlich sinnvoller als die direkte Verwendung dynamischer Container-IP-Adressen.

Beispielsweise kann später ein Anwendungcontainer mit einem Datenbankcontainer kommunizieren:

taskmanager
     │
     │ database
     ▼
database

Der Anwendungscode muss dadurch nicht beispielsweise:

172.18.0.3

als feste Datenbankadresse kennen.

Stattdessen wird der Name des Dienstes verwendet.

Dies ist eine wichtige Grundlage für Docker Compose, da Compose später mehrere Dienste und deren Netzwerke gemeinsam verwalten kann.
Benutzerdefiniertes Netzwerk und Taskmanager

Das Netzwerk taskmanager-net verwendet ebenfalls den bridge-Driver.

Die Container des Tests wurden diesem Netzwerk zugeordnet und erhielten Adressen aus einem eigenen Subnetz, beispielsweise:

172.18.0.0/16

Damit besteht eine klare Trennung zum Standardnetzwerk:

Standard-bridge
172.17.0.0/16

taskmanager-net
172.18.0.0/16

Die Verwendung eines eigenen Netzwerks ermöglicht damit nicht nur eine separate IP-Adressierung, sondern auch die für mehrteilige Anwendungen wichtige Docker-interne Namensauflösung.
localhost innerhalb eines Containers

Ein weiterer wichtiger Lernpunkt war die Bedeutung von localhost.

Aus einem Container heraus wurde:

docker exec dns-test-1 ping -c 3 localhost

ausgeführt.

Die Ausgabe begann mit:

PING localhost (::1)

Damit wurde die IPv6-Loopback-Adresse:

::1

verwendet.

Bereits beim ersten Netzwerktest war innerhalb des Containers die IPv4-Loopback-Adresse sichtbar:

127.0.0.1

IPv4 und IPv6 besitzen damit jeweils eine eigene Loopback-Adresse:

IPv4:
127.0.0.1

IPv6:
::1

Beide bezeichnen aus Sicht des jeweiligen Netzwerk-Stacks das lokale System.

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

Zur weiteren Überprüfung wurde im Container:

docker exec dns-test-1 hostname

ausgeführt.

Die Ausgabe lautete:

946e56cf75dd

Anschließend wurde mit:

docker ps

die Containerliste betrachtet.

Dort war sichtbar:

CONTAINER ID   ...   NAMES
946e56cf75dd   ...   dns-test-1

Der Hostname innerhalb des Containers stimmte damit mit der Container-ID überein.

Damit konnte die bereits anhand des Loopback-Interfaces formulierte Annahme zusätzlich praktisch überprüft werden:

dns-test-1
    │
    ├── hostname → 946e56cf75dd
    │
    └── docker ps
           └── Container ID → 946e56cf75dd

Der Zugriff auf localhost blieb damit innerhalb des Containers.
localhost ist nicht dasselbe wie Port Publishing

Für das Verständnis des Docker-Netzwerks ist die Unterscheidung zwischen localhost und Port Publishing besonders wichtig.

Ein Port-Mapping wie:

-p 3001:5000

bedeutet:

Docker Host
localhost:3001
       │
       ▼
Container:5000

localhost innerhalb des Containers bedeutet dagegen:

Container
localhost:5000
       │
       ▼
derselbe Container

Das Netzwerk und die Portweiterleitung sind damit zwei unterschiedliche Mechanismen.

Ein Container kann mit anderen Containern kommunizieren, ohne dass dafür ein Host-Port veröffentlicht werden muss.
Container-zu-Container-Kommunikation ohne Port Publishing

Die bisherigen Tests zeigen:

Container A
    │
    │ Docker-Netzwerk
    ▼
Container B

Diese Kommunikation benötigt nicht zwingend:

-p HOSTPORT:CONTAINERPORT

Das Port Publishing ist primär dafür relevant, einen Dienst außerhalb des Docker-Netzwerks, beispielsweise für den Docker Host oder einen externen Client, erreichbar zu machen.

Innerhalb eines gemeinsamen Docker-Netzwerks können Container dagegen direkt über das Netzwerk miteinander kommunizieren.

Damit ergibt sich eine wichtige Unterscheidung:

Container → Container
        │
        └── Docker-Netzwerk

gegenüber:

Host → Container
        │
        └── Port Publishing

HTTP-Test und Fehlersuche

Als nächster praktischer Schritt sollte nicht mehr nur ICMP mit ping, sondern eine echte Anwendungskommunikation über TCP und HTTP untersucht werden.

Dafür wurde ein weiterer Alpine-Container im Netzwerk taskmanager-net gestartet:

docker run -d \
  --name http-test \
  --network taskmanager-net \
  alpine \
  sh -c "echo 'Hallo aus dem Container!' > /index.html && httpd -f -p 8080 -h /"

Beim ersten Versuch trat bereits auf der Shell-Ebene ein Fehler auf:

bash: !': event not found

Ursache war das Ausrufezeichen innerhalb des Befehls, das von der Bash-History-Expansion interpretiert wurde.

Trotzdem wurde ein Container angelegt.

Bei der Untersuchung mit:

docker ps -a --filter name=http-test

wurde festgestellt:

STATUS: Exited (0)

Der Container war damit nicht mehr aktiv, existierte aber weiterhin.

Dies führte zunächst zu einer wichtigen Wiederholung des Container-Lifecycle-Modells:

Container erstellt
      ↓
Hauptprozess beendet
      ↓
Container = Exited
      ↓
Container existiert weiterhin

Ein beendeter Container wird ohne --rm nicht automatisch gelöscht.
Untersuchung des fehlgeschlagenen HTTP-Containers

Nach dem erneuten Startversuch blieb der Container ebenfalls nicht aktiv.

Statt sofort einen neuen Test zu erstellen, wurde der vorhandene Container untersucht.

Mit:

docker inspect http-test --format '{{.Config.Cmd}}'

wurde die tatsächlich hinterlegte Kommandozeile überprüft:

[sh -c echo Hallo aus dem Container > /index.html && httpd -f -p 8080 -h /]

Anschließend wurde der Exit-Code untersucht:

docker inspect http-test --format '{{.State.ExitCode}}'

Ergebnis:

127

Die Logs lieferten schließlich die entscheidende Information:

docker logs http-test

Ausgabe:

sh: httpd: not found

Damit war die Ursache eindeutig.

Das verwendete Alpine-Image enthielt den Befehl httpd in dieser Umgebung nicht.

Der Container beendete deshalb seinen Hauptprozess mit Exit-Code 127.

Vereinfacht:

Container startet
      │
      ▼
sh
      │
      ├── echo ... > /index.html
      │       │
      │       └── erfolgreich
      │
      └── httpd ...
              │
              ▼
        httpd nicht vorhanden
              │
              ▼
        Exit-Code 127
              │
              ▼
        Container Exited

Damit wurde gleichzeitig erneut praktisch bestätigt, dass der Lebenszyklus eines Containers unmittelbar an den laufenden Hauptprozess gekoppelt ist.

Der HTTP-Test wurde an dieser Stelle bewusst beendet und soll mit einem geeigneten Image zu einem späteren Zeitpunkt wiederholt werden.
Bedeutung für die spätere Compose-Architektur

Die bisherigen Netzwerkuntersuchungen bilden bereits die Grundlage für den späteren Taskmanager-Stack.

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

                    Docker Host
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
    │      └── Docker Volume
    │
    └── Port Publishing
           │
           └── Zugriff vom Host

Diese Kombination aus mehreren Containern, einem gemeinsamen Netzwerk, persistentem Storage und zentraler Konfiguration bildet später die Grundlage für Docker Compose.
Ergebnis

Durch die praktische Untersuchung von Docker-Netzwerken wurde das bisherige Verständnis von Containern um die Netzwerkebene erweitert.

Dabei wurden folgende Zusammenhänge praktisch nachvollzogen:

    Ein Container besitzt eigene Netzwerkinterfaces.

    Das Loopback-Interface lo stellt unter anderem 127.0.0.1 beziehungsweise ::1 bereit.

    localhost innerhalb eines Containers bezeichnet den jeweiligen Container selbst.

    Ein Container besitzt eine eigene IP-Adresse innerhalb des Docker-Netzwerks.

    Die Routingtabelle des Containers enthält unter anderem eine Route zum Docker-Gateway.

    Das Standardnetzwerk bridge verwendet ein eigenes Subnetz, im Test 172.17.0.0/16.

    Das Gateway des Standardnetzwerks war 172.17.0.1.

    Mehrere Container können gleichzeitig an dasselbe Docker-Netzwerk angeschlossen werden.

    Container können innerhalb eines gemeinsamen Netzwerks direkt miteinander kommunizieren.

    Diese Kommunikation benötigt kein Host-Port-Mapping.

    Der bridge-Driver stellt die technische Grundlage für Bridge-Netzwerke bereit.

    Das Standardnetzwerk bridge und ein benutzerdefiniertes Bridge-Netzwerk können denselben Driver verwenden, besitzen aber nicht dieselbe funktionale Konfiguration.

    Benutzerdefinierte Bridge-Netzwerke ermöglichen die Docker-interne Namensauflösung zwischen Containern.

    Container-IP-Adressen sollten nicht als dauerhaft stabile Identität eines Dienstes betrachtet werden.

    Container-Namen beziehungsweise später Compose-Dienstnamen eignen sich besser für die Kommunikation zwischen Diensten.

    Port Publishing und Container-zu-Container-Kommunikation sind unterschiedliche Mechanismen.

    Ein beendeter Container (Exited) existiert weiterhin, sofern er nicht mit --rm gestartet oder anschließend gelöscht wurde.

    Der Lebenszyklus eines Containers hängt unmittelbar vom laufenden Hauptprozess ab.

    Ein Exit-Code 127 kann darauf hinweisen, dass ein aufgerufener Befehl nicht gefunden wurde.

    Fehler sollten anhand von docker ps, docker inspect und docker logs bis zur tatsächlichen Ursache untersucht werden.

Damit ergibt sich für die Netzwerkebene des bisherigen Docker-Modells:

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
         VS Code            Taskmanager              Datenbank
                            Container                Container
                                │                         │
                                │                         │
                                └──── Container-Netz ─────┘
                                │
                                ▼
                         Docker Volume
                         taskmanager-data

Damit ist der nächste logische Lernschritt die Untersuchung mehrerer Dienste als zusammengehöriges System. Insbesondere soll zunächst die Kommunikation zwischen Anwendung und Datenbank praktisch nachvollzogen werden. Anschließend kann daraus schrittweise Docker Compose als Werkzeug zur gemeinsamen Definition von Containern, Netzwerken, Volumes und Konfiguration entstehen.