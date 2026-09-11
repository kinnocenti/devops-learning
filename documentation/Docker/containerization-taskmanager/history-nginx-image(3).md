# des Befehls ```bash docker image history nginx ``` 

An dieser Stelle wird die Ausgabe des Befehls ```bash docker image history nginx ``` eingefügt und im Weiteren erläutert. 

## Ausgabe des Befehls

Die Ausgabe wird von unten nach oben gelesen, da unten der erste Schritt angezeigt wird (die Basis) und die folgende Schritte bauen entsprechend darauf auf.

IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
5a88c9c45479   6 weeks ago   CMD ["nginx" "-g" "daemon off;"]                0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   STOPSIGNAL SIGQUIT                              0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   EXPOSE map[80/tcp:{}]                           0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   ENTRYPOINT ["/docker-entrypoint.sh"]            0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   COPY 30-tune-worker-processes.sh /docker-ent…   16.4kB    buildkit.dockerfile.v0
<missing>      6 weeks ago   COPY 20-envsubst-on-templates.sh /docker-ent…   12.3kB    buildkit.dockerfile.v0
<missing>      6 weeks ago   COPY 15-local-resolvers.envsh /docker-entryp…   12.3kB    buildkit.dockerfile.v0
<missing>      6 weeks ago   COPY 10-listen-on-ipv6-by-default.sh /docker…   12.3kB    buildkit.dockerfile.v0
<missing>      6 weeks ago   COPY docker-entrypoint.sh / # buildkit          8.19kB    buildkit.dockerfile.v0
<missing>      6 weeks ago   RUN /bin/sh -c set -x     && groupadd --syst…   87.1MB    buildkit.dockerfile.v0
<missing>      6 weeks ago   ENV DYNPKG_RELEASE=1~trixie                     0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   ENV PKG_RELEASE=1~trixie                        0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   ENV ACME_VERSION=0.4.1                          0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   ENV NJS_RELEASE=1~trixie                        0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   ENV NJS_VERSION=1.0.0                           0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   ENV NGINX_VERSION=1.31.3                        0B        buildkit.dockerfile.v0
<missing>      6 weeks ago   LABEL maintainer=NGINX Docker Maintainers <d…   0B        buildkit.dockerfile.v0
<missing>      7 weeks ago   # debian.sh --arch 'amd64' out/ 'trixie' '@1…   87.4MB    debuerreotype 0.17

## Erläuterung der Ausgabe

Was zeigt docker image history?

Sie zeigt vereinfacht, aus welchen Schichten bzw. Anweisungen das Image aufgebaut wurde. In der untersten Zeile steht, '7 weeks ago   # debian.sh --arch 'amd64' out/ 'trixie' '@1…   87.4MB', das ist die Basis des Images.

### Das Image basiert auf Debian

Ganz unten steht 'trixie'. Das ist der Codename der Debian-Version, auf der dieses Nginx-Image basiert. Das bedeutet aber nicht, dass ein vollständiger Debian-Server als VM heruntergeladen wurde. Es besteht eine Umgebung mit den benötigten User-Space-Bestandteilen. Der Linux-Kernel kommt weiterhin vom Host.

### EXPOSE 80/tcp 

'EXPOSE 80/tcp' ist keine Portweiterleitung. Im Image steht 'EXPOSE map[80/tcp:{}]'. Das bedeutet sinngemäß, dieses Image beschreibt, dass die Anwendung Port 80/TCP verwendet bzw. für diesen Port vorgesehen ist. Aber 'EXPOSE 80/tcp' bedeutet nicht Host:80 → Container:80. Die tatsächliche Weiterleitung entsteht erst durch: '-p 3000:80'. Das ist eine sehr wichtige Unterscheidung.

Also ergibt sich:

        Image:
    EXPOSE 80/tcp
          ↓
      Container:
Nginx hört auf 80/tcp
          ↓
docker run -p 3000:80
          ↓
        Host:
 3000 → Container:80

### CMD 

In der obersten Zeile steht, 'CMD ["nginx" "-g" "daemon off;"]'. Hier erklärt sich, warum der Container überhaupt Nginx ausführt. CMD legt fest, welcher Standardbefehl beim Start des Containers verwendet werden soll. Und 'daemon off;' sorgt dafür, dass Nginx im Vordergrund läuft. Das ist für Container sehr wichtig.

Denn folgendes ist nicht erwünscht:

                  Container startet
                         ↓
                   Nginx startet
                         ↓
              Nginx geht in Hintergrund
                         ↓
Container hat keinen relevanten Vordergrundprozess mehr
                         ↓
               Container beendet sich

Sondern:

     Container startet
             ↓
       Nginx startet
             ↓
Nginx bleibt im Vordergrund
             ↓
      Container läuft

Mit dem Befehl ```bash docker run nginx ``` bleibt das Terminal „besetzt“, weil Nginx im Vordergrund läuft. Mit 'docker run -d ...' wird dagegen der Container detached gestartet. Und damit kann das Modell erweitert werden.

Bisher:

  Image
    ↓
Container
    ↓
 Prozess

Jetzt wird deutlich mehr sichtbar:

   Dockerfile
       ↓
     Build
       ↓
     Layer
       ↓
     Image
       ↓
    docker run
       ↓
   Container
       ↓
CMD / ENTRYPOINT
       ↓
    Prozess

### ENTRYPOINT und CMD

In der Augabe steht ein paar Zeilen unter 'CMD ["nginx" "-g" "daemon off;"]' 'ENTRYPOINT ["/docker-entrypoint.sh"]'. Die Beiden haben unterschiedliche Aufgaben.
ENTRYPOINT legt fest, welches Programm bzw. welches Startskript beim Start des Containers ausgeführt wird.

Beim Nginx-Image:

     ENTRYPOINT
         ↓
/docker-entrypoint.sh

Das ist ein Startskript des Nginx-Images. Es kann beispielsweise vorbereitende Aufgaben erledigen und anschließend den eigentlichen Nginx-Prozess starten.

Vereinfacht:

 Container startet
        ↓
docker-entrypoint.sh
        ↓
   Vorbereitungen
        ↓
   Nginx starten

CMD hingegen gibt den Standardbefehl bzw. die Standardargumente für den Container vor. Damit wird Nginx gestartet und mit 'daemon off;' angewiesen, im Vordergrund zu bleiben. Das ist für Container wichtig, weil der laufende Hauptprozess den Lebenszyklus des Containers bestimmt.

Das vereinfachte Modell lautet daher:

 Container starten
         ↓
    ENTRYPOINT
         ↓
docker-entrypoint.sh
         ↓
        CMD
         ↓
       nginx
         ↓
    Nginx läuft
         ↓
   Container läuft

'ENTRYPOINT' definiert den Einstiegspunkt des Containers. 'CMD' definiert den standardmäßig auszuführenden Befehl bzw. die Standardargumente.