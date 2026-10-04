# Docker Networking – Container-Kommunikation und benutzerdefiniertes Bridge-Netzwerk

## Ausgangspunkt

Nach der Untersuchung grundlegender Docker-Netzwerke wird die Container-zu-Container-Kommunikation weiter untersucht. Für die weiteren Tests sollte ein eigenes Netzwerk verwendet werden. Dadurch bleiben die Netzwerkkonfigurationen der Tests von dem bereits bestehenden 'taskmanager-net' getrennt.

Das Vorgehen folgt dabei weiterhin dem Prinzip:

Beobachtung → Vermutung → gezielter Test → Ausgabe → Schlussfolgerung

## Eigenes Testnetzwerk

Für die Netzwerktests wird ein eigenes Bridge-Netzwerk erstellt:

```bash
docker network create test-net
```

Anschließend wird die tatsächliche Konfiguration mit ```bash docker network inspect test-net``` überprüft. Das Netzwerk verwendet den Driver 'bridge' und erhält in der aktuellen Docker-Installation:

Subnet:  172.19.0.0/16
Gateway: 172.19.0.1

Damit wird die bisherige Annahme praktisch bestätigt, dass Docker bei einem neu erstellten Bridge-Netzwerk ein eigenes Subnetz verwendet.

Hinweis: Die konkrete Adresse darf nicht vorausgesetzt werden. Docker verwaltet die IP-Adressvergabe und kann abhängig von der vorhandenen Netzwerkkonfiguration ein anderes freies Subnetz verwenden.

Das neue Testnetzwerk ist damit logisch von den bereits vorhandenen Netzwerken getrennt:

Docker-Host
│
├── bridge
│   └── 172.17.0.0/16
│
├── taskmanager-net
│   └── 172.18.0.0/16
│
└── test-net
    └── 172.19.0.0/16

Die Aufteilung ist für die Tests übersichtlich, stellt aber keine allgemeingültige feste Vergabereihenfolge dar.

## nginx als HTTP-Testcontainer

Für den nächsten Test wird zunächst die Anforderung betrachtet. Es wird ein Container benötigt, der HTTP-Verbindungen entgegennimmt. Die bereits vorhandenen Images werden unter diesem Gesichtspunkt betrachtet. Bei der Untersuchung des vorhandenen nginx-Images zeigte sich in den Image-Metadaten:

"ExposedPorts": {
    "80/tcp": {}
}

Damit ist im Image hinterlegt, dass der Containerdienst Port 80 über TCP verwendet bzw. dass dieser Port als Container-Port vorgesehen ist. 

## Erster HTTP-Container

Der erste nginx-Container wurde direkt mit dem Testnetzwerk verbunden:

```bash
docker run -d --name http-test --network test-net nginx
```

Die Netzwerkkonfiguration des Containers zeigte anschließend:

Gateway:   172.19.0.1
IPAddress: 172.19.0.2

Der Container befindet sich damit im Netzwerk test-net.

Auch die aus dem Image übernommenen Metadaten sind im Container wiederzufinden:

"ExposedPorts": {
    "80/tcp": {}
}

Damit lässt sich erneut der Zusammenhang zwischen Image und daraus erzeugtem Container beobachten:

nginx Image
    │
    ├── Anwendung
    ├── Konfiguration
    └── Metadaten
           │
           ▼
      nginx Container
           │
           └── 80/tcp

Die vorhandenen Image-Metadaten sind dabei von der tatsächlichen Netzwerkerreichbarkeit zu unterscheiden.

## HTTP-Client als erweitertes Image

Für den eigentlichen Kommunikationstest wird kein zweiter nginx-Container benötigt. Ein Webserver würde lediglich einen weiteren HTTP-Dienst bereitstellen, könnte aber nicht als HTTP-Client für den Test dienen. 
Deshalb muss ein anderes Image für den zweiten Container verwedent werden. Am effizientesten ist es in diesem Fall ein bestehendes Image, wie z.B. 'HTTPie' für den HTTP-Client zu verwenden.
Stattdessen wird aber das vorhandene Alpine-Image gezielt erweitert. Damit soll gezeigt werden, dass ein bestehendes Image mit Funktionen erweitert werden kann. Dazu wird ein eigenes Dockerfile erstellt:

```bash
FROM alpine

RUN apk add --no-cache httpie   # apk add installiert das Paket httpie; --no-cache verhindert unnötige Paketindex-Daten im Image
```

Damit entsteht aus Alpine ein neues Image 'alpine-http', das zusätzlich den HTTP-Client HTTPie enthält. Ein vorhandenes Image kann also als Basis für ein eigenes, erweitertes Image verwendet werden.

Ablauf des Image-Builds:

Alpine Image
     │
     │ FROM
     ▼
Dockerfile
     │
     │ RUN apk add httpie
     ▼
neues Image
Alpine + HTTPie

Neben HTTPie existieren für solche Tests auch andere Werkzeuge wie curl oder wget.
Kommunikation über das benutzerdefinierte Netzwerk

Der HTTP-Client wird als temporärer Container im selben Netzwerk gestartet:

```bash
docker run --rm --network test-net alpine-http http http://http-test
```

Dabei wird der Containername 'http-test' als Ziel verwendet.

Die Kommunikation verläuft damit:

alpine-http
   │
   │ HTTPie
   │
   │ http://http-test
   ▼
test-net
   │
   ▼
http-test
   │
   │ nginx
   │ TCP/80
   ▼
HTTP-Antwort

Eine Veröffentlichung des nginx-Ports auf dem Docker-Host ist für diesen Test nicht erforderlich. Beide Container befinden sich im selben benutzerdefinierten Bridge-Netzwerk und können dort direkt miteinander kommunizieren.
Damit wird gleichzeitig die zuvor untersuchte Docker-DNS-Funktion praktisch genutzt: Der Containername 'http-test' dient als Zieladresse und muss nicht über die aktuell zugewiesene IP-Adresse angesprochen werden.

## Ergebnis

Der Test liefert folgende Ausgabe:

<html>
<head><title>405 Not Allowed</title></head>
<body>
<center><h1>405 Not Allowed</h1></center>
<hr><center>nginx/1.31.3</center>
</body>
</html>

Die Antwort 405 Not Allowed bedeutet in diesem Zusammenhang nicht, dass die Netzwerkverbindung fehlgeschlagen ist. Entscheidend ist, dass eine HTTP-Antwort von nginx zurückgegeben wurde.

Damit wurde praktisch nachgewiesen:

- Der HTTP-Client konnte gestartet werden.
- HTTPie konnte ausgeführt werden.
- 'http-test' konnte über seinen Container-Namen erreicht werden.
- Die Kommunikation funktionierte über test-net.
- Die HTTP-Anfrage erreichte den nginx-Webserver.
- 'nginx' erzeugte daraufhin eine HTTP-Antwort.

Damit wurde die bisherige Kommunikationskette von der Netzwerk- bis zur Anwendungsebene erweitert:

      Netzwerk
          ↓
  IP-Kommunikation
          ↓
         TCP
          ↓
         HTTP
          ↓
Webserver / Anwendung

Der HTTP-Test bildet damit den Abschluss des aktuellen Docker-Networking-Lernschritts.

## Ablauf des HTTP-Tests

Anforderung
    │
    ▼
HTTP-Client benötigt
    │
    ▼
Recherche
    │
    ├── HTTPie → fertige passende Lösung
    │
    └── für unseren Test nicht verwendet
             │
             ▼
      Alpine als Basis
             │
             ▼
      um HTTP-Client erweitern
             │
             ▼
       eigener Test-Client
             │
             │ HTTP
             ▼
          nginx