# Git und GitHub Einrichtung

## Ziel

Einrichtung einer lokalen Git-Umgebung und Verbindung zu GitHub über SSH zur Versionsverwaltung von Lernprojekten.

## Ablauf

1. Git lokal einrichten
2. SSH-Verbindung zu GitHub herstellen
3. Repository erstellen
4. Repository lokal klonen
5. Ersten Commit erstellen
6. Änderungen nach GitHub pushen

## Lokale Git-Konfiguration

Git wurde konfiguriert.

```bash
git config --global user.name "NAME"   # Benutzernamen für Commits festlegen

git config --global user.email "MAIL"   # E-Mail-Adresse für Commits festlegen

git config --global init.defaultBranch main   # Standard-Branch 'main' für neue lokale Repositories festlegen 

git --version   # Versionsprüfung
```

## SSH-Authentifizierung 

SSH-Verbindung vom Client zu GitHub.

```bash
ssh-keygen -t ed25519 -C "email@example.com"   # SSH-Schlüssel generieren

# Enter drücken und Phassphrase vergeben, wenn gewünscht.

ls ~/.ssh   # prüfen

eval "$(ssh-agent -s)"   # SSH-Agent starten

ssh-add ~/.ssh/id_ed25519   # Schlüssel laden

cat ~/.ssh/id_ed25519.pub   # öffentlichen Schlüssel anzeigen lassen

# cat-Ausgabe kopieren und in GitHub unter 'Settings → SSH and GPG keys → New SSH key' einfügen und 'Add SSH key' anklicken. 

ssh -T git@github.com   # Verbindung testen
#Vertrauensabfrage mit 'yes' bestätigen
```

## Erstes Repository

GitHub-Repository erstellt.

```bash
mkdir -p ~/FOLDERNAME   # Ordner erstellen

cd ~/FOLDERNAME   # in Ordner wechseln

git clone git@github.com:USERNAME/FOLDERNAME.git   # erstellt lokale Kopie eines bestehenden Repositorys
```

## Erster Commit und Push

README.md-Datei erstellt und erweitert. 

```bash
git add FILENAME.md   # Änderungen für den nächsten Commit vormerken (staging).

git status   # Statusänderung checken

git commit -m "COMMENT"   # Speicherpunkt mit Kommentar erstellen

git status   # Statusänderung checken

git push   # lokalen Speicherstand an zentrales Repository übertragen
```