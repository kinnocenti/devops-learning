-- Tabelle groups anlegen:
CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


-- Tabelle tasks anlegen:
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


-- Tabelle task_dependencies anlegen:
CREATE TABLE task_dependencies (
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,
    PRIMARY KEY (task_id, depends_on_task_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id),
    CHECK (task_id <> depends_on_task_id)
);

-- Gruppen anlegen:
INSERT INTO groups (name)
VALUES
    ('Docker'),
    ('Kubernetes'),
    ('Linux');

-- Prüfen, ob Daten gespeichert wurden:
SELECT * FROM groups;

-- Aufgaben erstellen für die Testung:
INSERT INTO tasks (
    title,
    status,
    priority,
    group_id
)
VALUES
    ('Docker installieren', 'completed', 2, 1),
    ('Docker Tutorial Teil 1', 'in_progress', 2, 1),
    ('Docker Tutorial Teil 2', 'open', 3, 1),
    ('Linuxbefehlsübersicht erstellen', 'open', 1, NULL);

-- Prüfen, ob Daten gespeichert wurden:
SELECT * FROM tasks;

-- Aufgabe 'Docker Tutorial Teil 2' Deadline hinzufügen:
UPDATE tasks
SET deadline = '2026-08-12 20:00'
WHERE id = 3;

-- Prüfen, ob Deadline eingefügt wurde:
SELECT id, title, deadline
FROM tasks;

-- Aufgabenabhängigkeit erstellen:
INSERT INTO task_dependencies (
    task_id,
    depends_on_task_id
)
VALUES (
    3,
    2
);

-- Prüfen, ob Abhängigkeit angelegt wurde:
SELECT * FROM task_dependencies;

-- Neue Aufgabe anlegen für Aufgabe mit mehreren Abhängigkeiten:
INSERT INTO tasks (
    title,
    status,
    priority,
    group_id
)
VALUES (
    'Docker Compose Grundlagen',
    'open',
    2,
    1
);

-- IDs in tasks anzeigen lassen:
SELECT id, title
FROM tasks;

-- Zwei Abhängigkeiten für Docker Compose Grundlagen anlegen:
INSERT INTO task_dependencies (
    task_id,
    depends_on_task_id
)
VALUES
    (5, 2),
    (5, 3);

-- Prüfen, ob Aufgabe mit mehrehen Abhängigkeiten erstellt wurde:
SELECT * FROM task_dependencies;

-- Erster Constraint, eine bestehende Abhängigkeit soll erneut erstellt werden:
INSERT INTO task_dependencies (
    task_id,
    depends_on_task_id
)
VALUES (
    5,
    2
);

-- Zweiter Constraint, nicht vorhandene Priorität 4 vergeben bei einer neuen Aufgabe:
INSERT INTO tasks (
    title,
    status,
    priority,
    group_id
)
VALUES (
    'Test ungültige Priorität',
    'open',
    4,
    1
);

-- Abfrage der Tabelle tasks nach unerledigten Aufgaben:
SELECT id, title, status, priority, deadline, group_id
FROM tasks
WHERE status IN ('open', 'in_progress');

-- Anfrage der Tabelle tasks nach erledigten Aufgaben:
SELECT id, title, status, priority, deadline, group_id
FROM tasks
WHERE status = 'completed';

-- Abfrage der Tabelle tasks nach den Aufgaben und ihren Gruppennamen:
SELECT
    tasks.id,
    tasks.title,
    groups.name AS group_name
FROM tasks
LEFT JOIN groups
    ON tasks.group_id = groups.id;

-- Self-JOIN, Tabelle tasks wird mit sich selbst verbunden für die Abfrgae der abhängige Aufgabe und von der sie abhängt: 
SELECT
    task.title AS task,
    dependency.title AS depends_on
FROM task_dependencies
JOIN tasks AS task
    ON task_dependencies.task_id = task.id
JOIN tasks AS dependency
    ON task_dependencies.depends_on_task_id = dependency.id;












