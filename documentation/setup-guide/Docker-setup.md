# Docker Installation und Testung

Im Folgenden wird die Installation und Testung von Docker vorgenommen.

## Voraussetzungen

- Linux 
- Internetverbindung
- Benutzer mit sudo-Rechten
- Keine wichtigen Docker-Daten vorhanden

## Alte Docker-Pakete entfernen

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt purge -y "$pkg"
done
```

## Prüfen, ob Docker-Daten vorhanden sind

```bash
sudo ls -la /var/lib/docker
sudo ls -la /var/lib/containerd
```

Mögliche Ausgaben:

Ausgabe Fall 1:
ls: cannot access '/var/lib/docker': No such file or directory
- Perfekt. Es existieren keine Docker-Daten. (Nächsten Schritt überspringen)

Ausgabe Fall 2:
Es werden Dateien angezeigt.
- Dann können sie entfernt werden. (Nächsten Schritt durchführen)

## Docker-Daten löschen (Ausgabe Fall 2)

```bash
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

## Paketliste aktualisieren

```bash
sudo apt update
```

## Benötigte Pakete installieren

```bash
sudo apt install -y \
ca-certificates \
curl \
gnupg
```

## Schlüsselverzeichnis anlegen

```bash
sudo install -m 0755 -d /etc/apt/keyrings
```

## Docker-GPG-Schlüssel herunterladen

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg   # Berechtigungen setzen
```
## Ubuntu-Codename prüfen

```bash
. /etc/os-release && echo "$UBUNTU_CODENAME"
```

Je nach Mint-Version erscheint zB:

noble oder jammy

## Docker-Repository hinzufügen

```bash
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$UBUNTU_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## Paketlisten erneut aktualisieren

```bash
sudo apt update
```

## Docker installieren

```bash
sudo apt install -y \
docker-ce \
docker-ce-cli \
containerd.io \
docker-buildx-plugin \
docker-compose-plugin
```

Installation von:
    • Docker Engine
    • Docker CLI
    • containerd
    • Docker Buildx
    • Docker Compose Plugin

## Prüfen, ob Docker läuft

```bash
systemctl status docker
```

Gewünschte Ausgabe:

Active: active (running)

Falls der Dienst noch nicht läuft:

```bash
sudo systemctl enable --now docker
```

## Eigenen Benutzer zur Docker-Gruppe hinzufügen

```bash
sudo usermod -aG docker $USER
```

Danach abmelden und wieder anmelden oder neu starten.

Alternativ kann für die aktuelle Sitzung die neue Gruppenmitgliedschaft geladen werden:

```bash
newgrp docker
```

## Installation überprüfen

```bash
docker --version   #  Docker-Version anzeigen  

docker info    # Informationen zur Installation
```

## Ersten Testcontainer starten

```bash
docker run hello-world
```

Wenn alles funktioniert, kommt folgende Ausgabe:

Hello from Docker!

## Docker Compose testen

```bash
docker compose version
```

Hinweis: Docker compose ohne Bindestrich.

## Einen echten Container starten

```bash
docker run -d \   # Container erzeugen
--name nginx \   # Containername vergeben
-p 8080:80 \   # Hostport:Containerport konfigurieren
nginx   # Image des Containers

docker ps    # Laufende Container anzeigen
```
http://localhost:8080   # In Browser öffnen

Standardseite von Nginx sollte angezeigt werden.

```bash
docker stop nginx   # Container beenden
docker rm nginx   # Container löschen
```