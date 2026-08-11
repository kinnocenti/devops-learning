# Datenbank Modell und Erstellung

## Datenbankmodell

┌──────────────────────┐
│       groups         │
├──────────────────────┤
│ PK id       INTEGER  │
│    name     TEXT     │
└──────────┬───────────┘
           │
           │ 1 : n
           ▼
┌────────────────────────┐
│        tasks           │
├────────────────────────┤
│ PK id          INTEGER |
│    title       TEXT    │
│    description TEXT    │
│    status      TEXT    │
│    priority    INTEGER | 
│    deadline    TEXT    │
│ FK group_id    INTEGER |
└──────────┬─────────────┘
           │
           │
           │ 1 : n
           ▼
┌────────────────────────────┐
│    task_dependencies       │
├────────────────────────────┤
│ PK,FK task_id              │
│ PK,FK depends_on_task_id   │
└────────────┬───────────────┘
             │
             │ n : 1
             │
             ▼
           tasks
        (Selbstreferenz)

Die Anwendung verwendet drei Tabellen. Die Tabelle 'groups' speichert die Aufgabengruppen. In 'tasks' werden die eigentlichen Aufgaben gespeichert. Eine Aufgabe kann optional einer Gruppe zugeordnet werden.
Die Tabelle 'task_dependencies' bildet Abhängigkeiten zwischen Aufgaben ab. Sie verwendet zwei Fremdschlüssel auf die Tabelle tasks und stellt damit eine selbstreferenzierende n:m-Beziehung zwischen Aufgaben dar. Eine Aufgabe kann dadurch von mehreren anderen Aufgaben abhängen und gleichzeitig Voraussetzung für mehrere weitere Aufgaben sein.

## SQLite-Datenbank in DBeaver anlegen

Oben links 'New Database Connection' (Datenbanksymbol mit einem Plus) anklicken.

Datenbanktyp SQLite auswählen.

Den entsprechenden Path einfügen, mit 'Open...' den entsprechenden Ordner auswählen oder mit 'Create...' neu anlegen.

Mit 'Finish' bestätigen.

## Verbindungstest

Rechtsklick auf taskmanager.db (wurde links neu angelegt) und Connect auswählen und anklicken.

Wenn der Hinweis kommt, dass mit Download der SQLite-JDBC-Treiber eingerichtet wird, auf 'Download' klicken.
Der Treiber ist notwendig für die Kommunikation zwischen DBeaver und SQLite.

Wird jetzt erneut Rechtsklick auf taskmanager.db gemacht, wird nicht mehr die Option 'Connect', sondern 'Disconnect' und weitere neue Optionen angezeigt.

## Tabellen erstellen

Rechtsklick auf taskmanager.db, 'SQL Editor' auswählen und 'Open SQL Script' anklicken.

SQL-Queries zum anlegen der Tabellen:

```bash
# Tabelle groups anlegen:
CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


# Tabelle tasks anlegen:
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK (status IN ('open', 'in_progress', 'completed')),
    priority INTEGER NOT NULL CHECK (priority IN (1, 2, 3)),
    deadline TEXT,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);


# Tabelle task_dependencies (Zwischentabelle für die mögliche Abhängigkeit zwischen Aufgaben) anlegen:
CREATE TABLE task_dependencies (
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,
    PRIMARY KEY (task_id, depends_on_task_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id),
    CHECK (task_id <> depends_on_task_id)
);
```

Die Datenbank direkt in dem Lern-Repository von VScode abspeichern.
Hier wurde die Datenbank im 'taskmanager-database'-Ordner abgespeichert. In den beiden Dateien 'taskmanager.db' (enthält die Daten) und 'schema.sql' (enthält den Aufbau der Datenbank).