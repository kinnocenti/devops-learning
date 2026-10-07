# Webserver- und HTTP-Grundlagen

Nach Abschluss des Docker-Networking-Lernblocks wird die HTTP-Kommunikation zwischen Containern auf die Webserver-Ebene erweitert. Der Schwerpunkt liegt auf dem Zusammenhang zwischen HTTP-Request, Webserver, statischen Inhalten und Anwendung. Die bereits bekannten Grundlagen zu TCP, HTTP Request/Response und HTTPS werden dabei vorausgesetzt.Das Vorgehen folgt weiterhin dem Prinzip: Beobachtung → Vermutung → gezielter Test → Ausgabe → Schlussfolgerung.

## HTTP-Kommunikation mit nginx

Als HTTP-Server wird das bereits untersuchte nginx-Image verwendet:

```bash
docker run -d --name http-test --network test-net nginx
```

Der HTTP-Client basiert auf dem zuvor erstellten Image alpine-http, das Alpine um HTTPie erweitert.

Damit entsteht folgende Testumgebung:

test-net
│
├── http-test
│   └── nginx
│       └── TCP/80
│
└── HTTP-Client
    └── alpine-http

Für die Kommunikation wird weiterhin der Containername http-test verwendet. Eine Veröffentlichung von Port 80 auf dem Docker-Host ist für die Container-zu-Container-Kommunikation nicht erforderlich.

## Untersuchung eines DNS-Problems

Ein erster HTTP-Test mit HTTPie schlug mit einem DNS-Fehler fehl:

http: error: gaierror: [Errno -3] Try again
Couldn’t connect to a DNS server.

Statt unmittelbar von einem defekten Docker-DNS auszugehen, wurde die Namensauflösung schrittweise untersucht.

Zunächst:

```bash
docker run --rm --network test-net alpine-http \
    getent hosts http-test
```

liefert keine Ausgabe.

Die DNS-Konfiguration des Containers zeigte anschließend:

```bash
docker run --rm --network test-net alpine-http \
    cat /etc/resolv.conf
```

unter anderem:

nameserver 127.0.0.11

Damit war nachgewiesen, dass der Container den Docker-internen DNS-Resolver verwendet.Anschließend wurde der Zustand des Netzwerks untersucht:

```bash
docker network inspect test-net
```

Dabei zeigte sich:

"Containers": {}

Der zuvor verwendete nginx-Container war zu diesem Zeitpunkt nicht mehr mit dem Netzwerk verbunden bzw. lief nicht. Nach erneutem Start:

```bash
docker run -d --name http-test --network test-net nginx
```

funktionierte die Namensauflösung:

```bash
docker run --rm --network test-net alpine-http \
    getent hosts http-test
```

Ergebnis:

172.19.0.2        http-test  http-test

Damit wurde praktisch bestätigt:

http-test
    │
    ▼
Docker-DNS
    │
    ▼
172.19.0.2

Die Ursache des ursprünglichen Fehlers lag damit nicht in einer fehlenden Docker-DNS-Konfiguration, sondern darin, dass zum Zeitpunkt des Tests kein Zielcontainer im Netzwerk vorhanden war.

## HTTP-Client und verwendete Werkzeuge

Bei einem anschließenden Test mit curl trat ein anderer Fehler auf:

exec: "curl": executable file not found in $PATH

Dies war kein Netzwerkfehler. Das Image alpine-http enthält HTTPie, aber kein curl. Damit wurde erneut zwischen verschiedenen Fehler-Ebenen unterschieden:

Container starten
Netzwerk konfigurieren
Prozess starten
    └── curl vorhanden?

Für den Test wurde deshalb das vorhandene HTTPie verwendet:

```bash
docker run --rm --network test-net alpine-http \
    http -v GET http://http-test/
```

## HTTP Request und Response

Der Test lieferte unter anderem:

GET / HTTP/1.1
Host: http-test

und als Antwort:

HTTP/1.1 200 OK
Server: nginx/1.31.3
Content-Type: text/html
Content-Length: 896

Anschließend wurde die nginx-Standardseite als HTML zurückgegeben. Damit wurde die komplette Kommunikationskette praktisch bestätigt:

       Docker-DNS
            ↓
Containername → IP-Adresse
            ↓
    IP-Kommunikation
            ↓
           TCP
            ↓
        HTTP GET /
            ↓
          nginx
            ↓
     HTTP/1.1 200 OK
            ↓
      HTML-Response

Dabei wurden HTTP-Header von Headern niedrigerer Protokollebenen abgegrenzt:

HTTP
┌──────────────────────┐
│ HTTP-Header          │
│ HTTP-Body            │
└──────────────────────┘
          ↓
         TCP
          ↓
         IP
          ↓
      Ethernet

Die HTTP-Header beschreiben dabei die HTTP-Kommunikation und sind nicht mit TCP-, IP- oder Ethernet-Headern gleichzusetzen.

## nginx als Webserver

Um zu verstehen, woher die ausgelieferte HTML-Seite stammt, wurde zunächst das Dateisystem des Containers untersucht:

```bash
docker exec http-test ls -la /usr/share/nginx/html/
```

Ergebnis:

/usr/share/nginx/html/
├── 50x.html
└── index.html

Die Datei index.html besitzt eine Größe von 896 Bytes. Dies entspricht der im HTTP-Response angegebenen:

Content-Length: 896

Damit besteht ein direkter Zusammenhang zwischen der ausgelieferten Response und der Datei im nginx-Webroot.

## URL-Pfad und Dateisystempfad

Der HTTP-Request 'GET /' bedeutet nicht automatisch, dass nginx auf ein Dateisystemverzeichnis '/' zugreift. Die Zuordnung zwischen URL-Pfad und Dateisystem wird durch die nginx-Konfiguration hergestellt:

location / {
    root   /usr/share/nginx/html;
    index  index.html index.htm;
}

Für 'GET /' ergibt sich damit vereinfacht:

HTTP-Request
  GET /
    │
    ▼
location /
    │
    ▼
root /usr/share/nginx/html
    │
    ▼
index index.html
    │
    ▼
/usr/share/nginx/html/index.html
    │
    ▼
HTTP Response

Der URL-Pfad '/' und das Dateisystemverzeichnis '/usr/share/nginx/html/' sind somit nicht identisch. nginx stellt über seine Konfiguration die entsprechende Zuordnung her.

## Index-Datei

Mit 'index index.html index.htm;' ist festgelegt, welche Dateien nginx als Index-Dokument verwendet, wenn ein Verzeichnis bzw. dessen URL-Pfad angefordert wird. Da 'index.html' vorhanden ist, wird bei 'GET /' diese Datei verwendet. Die vorhandene '50x.html' wird dagegen nicht für den normalen Request 'GET /' verwendet, obwohl sie sich ebenfalls im Webroot befindet.
Damit zeigt sich das Vorhandensein einer Datei bedeutet nicht automatisch, dass sie für jeden HTTP-Request verwendet wird. Entscheidend ist die nginx-Konfiguration und der angeforderte URL-Pfad.

## nginx-Fehlerseite 50x.html

Die Datei '50x.html' wurde anschließend direkt untersucht:

```bash
docker exec http-test cat /usr/share/nginx/html/50x.html
```

Sie enthält statischen HTML-Inhalt sowie internes CSS (<style>...</style>). Die Datei ist als Fehlerseite für bestimmte HTTP-Statuscodes aus der 5xx-Klasse vorgesehen. Die entsprechende nginx-Konfiguration lautet:

error_page 500 502 503 504 /50x.html;

location = /50x.html {
    root /usr/share/nginx/html;
}

Damit wird die Funktion der Datei direkt durch die Konfiguration bestätigt:

500 / 502 / 503 / 504
        │
        ▼
    error_page
        │
        ▼
     /50x.html
        │
        ▼
/usr/share/nginx/html/50x.html
        │
        ▼
    HTML-Response


'50x.html' ist damit nicht für den normalen Aufruf von '/' zuständig, sondern für die konfigurierte Fehlerbehandlung bestimmter serverseitiger Fehler.

## Webserver und Anwendung

Damit lässt sich nginx von der bereits vorhandenen Flask-Anwendung abgrenzen. nginx kann beispielsweise statische Inhalte direkt aus dem Dateisystem ausliefern:

  HTTP Request
       ↓
     nginx
       ↓
statische Datei
       ↓
 HTTP Response

Der Taskmanager arbeitet dagegen als Anwendung:

HTTP Request
     ↓
   Flask
     ↓
Python-Anwendung
     ├── Anwendungslogik
     ├── Jinja-Templates
     └── Datenbankzugriffe
     ↓
HTTP Response

Das Verzeichnis '/app' des Taskmanager-Containers ist deshalb nicht automatisch mit dem nginx-Webroot gleichzusetzen. Die Flask-Anwendung verarbeitet Requests und erzeugt daraus Responses, während nginx im bisherigen Test statische Dateien direkt aus seinem konfigurierten Webroot ausliefert.

## Einordnung für den Taskmanager

Aus der Trennung zwischen Webserver und Anwendung ergibt sich später eine mögliche mehrstufige Architektur:

Browser
   │
   │ HTTP/HTTPS
   ▼
nginx
   │
   │ Reverse Proxy
   ▼
Flask
   │
   ▼
Datenhaltung

Dabei kann nginx als Webserver und Reverse Proxy eingesetzt werden, während Flask die eigentliche Anwendungslogik übernimmt. Die konkrete Umsetzung dieses Aufbaus wird bewusst noch nicht vorweggenommen. Sie kann später im Zusammenhang mit mehreren Containern und Docker Compose praktisch untersucht werden.

## HTTPS und TLS

HTTPS und TLS sind aus den bisherigen Grundlagen bereits bekannt. Für die spätere Systemarchitektur ist insbesondere relevant, dass TLS häufig am vorgeschalteten Webserver bzw. Reverse Proxy terminiert wird:

Client
  │
  │ HTTPS
  ▼
Webserver / Reverse Proxy
  │
  │ internes HTTP
  ▼
Anwendung

Dadurch kann der externe Zugriff verschlüsselt erfolgen, während die Kommunikation innerhalb einer kontrollierten Container- bzw. Netzwerkumgebung je nach Architektur über HTTP erfolgen kann. 

## Ergebnis des Webserver-Exkurses

Der HTTP-Test wurde von der reinen Container-Kommunikation bis zur konkreten Webserver-Konfiguration erweitert.

Damit wurde nachvollzogen:

Container-Netzwerk
       ↓
  Docker-DNS
       ↓
       IP
       ↓
      TCP
       ↓
  HTTP Request
       ↓
     nginx
       ↓
nginx-Konfiguration
       ↓
    URL-Pfad
       ↓
    Webroot
       ↓
statische Datei
       ↓
 HTTP Response

Besonders wichtig für die weitere Entwicklung des Taskmanagers ist die Unterscheidung:

nginx
→ Webserver / Reverse Proxy
→ statische Inhalte und Weiterleitung

Flask
→ Webanwendung
→ Anwendungslogik und dynamische Responses

Datenbank
→ Datenhaltung

Damit ist die notwendige Grundlage für die spätere Betrachtung mehrerer Dienste geschaffen. Der nächste größere Lernschritt ist Docker-Compose, bei dem mehrere Container, Netzwerk, Volumes und Konfiguration gemeinsam beschrieben und betrieben werden.