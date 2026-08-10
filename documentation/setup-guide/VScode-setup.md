# VScode Einrichtung

Hinweis: Verwendung des offiziellen Microsoft Repository für automatische Updates

## Microsoft-Schlüssel importieren

```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg

sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg

echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list

rm packages.microsoft.gpg
```

## VScode Installation

```bash
sudo apt update
sudo apt install code
```

## VScode Konfiguration

Folgende Extensions installieren:
- Docker
- Dev Containers
- YAML
- GitLens
- Error Lens
- EditorConfig
- Kubernetes
- Markdown All in One
- Remote SSH

Weitere Konfigurationen:
- unter Auto Save 'afterDelay' aktivieren
- 'Format on Save' aktivieren

## Tipp

```bash
code –list-extensions    # Extensions auflisten lassen

code --list-extensions > vscode-extensions.txt   # Extensions in Textdatei speichern
```