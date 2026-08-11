# DBeaver Installation

Für das Taskmanager-Projekt wird eine Datenbank benötigt.

## Signaturschlüssel installieren

```bash
sudo wget -q -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/dbeaver.gpg.key
```

Hinweis: Mit dem Sinaturschlüssel wird die Paketquelle verifiziert.

## Lokalisation von DBeaver an APT weitergeben

```bash
echo "deb [signed-by=/usr/share/keyrings/dbeaver.gpg.key] https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
```

Hinweis: Neben der Lokalisation wird auch der Sinaturschlüssel übergeben.

## DBeaver installieren

```bash
sudo apt-get update   # Aktualisierung verfügbarer Paketinformationen

sudo apt-get install dbeaver-ce   # installiert DBeaver
```

## DBeaver Konfiguration

SQLite als Datenbankverbindung auswählen.

.gitignore-Datei erstellen und entsprechenden Inhalt einfügen:

```bash
touch .gitignore   # Datei erstellen

taskmanager/taskmanager.db   # Inhalt der Datei
```

Hinweis: Mit der .gitignore-Datei wird verhindert, dass die Datenbank von Git an GitHub weitergegeben wird.

## Check, ob Git die Datenbank ignoriert

```bash
git check-ignore -v taskmanager/taskmanager.db
```

Gewünschte Ausgabe:
.gitignore:1:taskmanager/taskmanager.db    taskmanager/taskmanager.db