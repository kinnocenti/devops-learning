## Ablaufdiagramme zum Projekt Taskmanager

In den Dokumentationen dieses Repositories werden immer wieder Ablaufdiagramme gezeigt. Hier alle wichtigen Ablaufdiagramme, die für das Verständnis der Abläufe innerhalb des Projektes 'Taskmanager' wichtig sind.

## Der komplette Weg: Datenbank → Browser

Gesamtüberblick:

SQLite-Datenbank
    ↓
SQL-Abfrage
    ↓
sqlite3 / Connection / Cursor
    ↓
Python
    ↓
Flask
    ↓
Jinja
    ↓
HTML + CSS
    ↓
Browser
    ↓
fertige Webseite

Die Verantwortlichkeiten:

SQLite       → speichert die Daten
SQL          → bestimmt, welche Daten abgefragt werden
sqlite3      → ermöglicht Python den Zugriff auf SQLite
Python       → führt SQL aus und verarbeitet die Ergebnisse
Flask        → verarbeitet HTTP-Anfragen und steuert die Anwendung
Jinja        → setzt Python-Daten in HTML ein
HTML         → beschreibt die Struktur der Webseite
CSS          → beschreibt das Aussehen
Browser      → stellt HTML + CSS dar

## Was passiert beim Aufrufen der Startseite?

Zum Beispiel beim Aufruf von:

http://localhost:5000/

läuft es vereinfacht so:

Browser
   ↓
HTTP GET /
   ↓
Flask
   ↓
home()
   ↓
SQLite-Verbindung
   ↓
SQL SELECT
   ↓
Cursor
   ↓
fetchall()
   ↓
Python erhält Task-Daten
   ↓
render_template()
   ↓
Jinja verarbeitet die Daten
   ↓
index.html
   ↓
CSS
   ↓
Browser
   ↓
Startseite

Das ist ein schöner Ablauf, weil man hier wirklich sieht, wer wann was macht.

## Was passiert bei einer Task-Detailansicht?

Beim Aufruf beispielsweise:

/task/3

läuft es so:

Browser
   ↓
HTTP GET /task/3
   ↓
Flask
   ↓
task_detail(task_id=3)
   ↓
SQL SELECT ... WHERE tasks.id = ?
   ↓
(task_id,)
   ↓
Cursor
   ↓
fetchone()
   ↓
ein Task als Ergebnis
   ↓
render_template("task.html", task=task)
   ↓
Jinja
   ↓
task.html
   ↓
CSS
   ↓
Browser
   ↓
Detailansicht

Hier sieht man auch sehr schön den Unterschied:

Startseite → fetchall() → mehrere Tasks

Detailansicht → fetchone() → ein Task

## Der Weg beim Erstellen einer Aufgabe

Ablauf mit umgekehrten Datenfluss:

Browser
   ↓
Formular ausfüllen
   ↓
HTTP POST
   ↓
Flask-Route
   ↓
Formulardaten auslesen
   ↓
Python
   ↓
cursor.execute()
   ↓
SQL INSERT
   ↓
SQLite-Datenbank
   ↓
commit()
   ↓
Weiterleitung zur Startseite
   ↓
Flask
   ↓
SQL SELECT
   ↓
Jinja
   ↓
HTML + CSS
   ↓
Browser

Beide Richtungen:

DATEN LESEN

SQLite
  ↓
SQL SELECT
  ↓
Python / Flask
  ↓
Jinja
  ↓
HTML + CSS
  ↓
Browser

DATEN SCHREIBEN:

Browser
  ↓
HTML-Formular
  ↓
HTTP POST
  ↓
Flask / Python
  ↓
SQL INSERT
  ↓
SQLite

## Übergang zu Docker

TASKMANAGER

Browser
   ↓
HTML + CSS
   ↓
Jinja
   ↓
Flask / Python
   ↓
sqlite3
   ↓
SQLite

Das ist die Anwendung und mit Docker läuft alles innerhallb eines Docker-Containers.