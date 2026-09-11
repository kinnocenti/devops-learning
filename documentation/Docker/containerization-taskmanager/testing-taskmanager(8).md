# Testung des Taskmanagers

Nach der erfolgreichen Containerisierung des Taskmanagers wird eine Testung durchgeführt, ob alle Funktionen im Taskmanager wie gewünscht ablaufen. Mit 'curl' wurde zuvor schon der Healthcheck durchgeführt, aber zur Übung werden kleine Tests vorgenommen.

Da der Container nur gestoppt wurde, wird er mit ```bash docker start taskmanager ``` gestartet. Daraufhin kann er mit https://localhost:3001 im Browser aufgerufen werden. Zudem wird DBeaver geöffnet, um die Verbindung zwischen Taskmanager und Datenbank zu testen.

## Funktionstest der Links

Funktionieren die Links zu den einzelnen Aufgaben, funktioniert der Zurück-Link und funktionieren die Links zur Aufgaben- und Gruppenerstellung? Dafür werden alle Links durchgeklickt. 
Da alle Links funktionieren, wird die Erstellung von Aufgaben und Gruppen getestet.

## Testung der Aufgaben- und Gruppenerstellung

Damit wird überprüft, ob die Daten der erstellten Aufgabe und Gruppe in die Datenbank eingefügt werden.

### Testung der Aufgabenerstellung

Im Taskmanager wird die Aufgabe 'Testung' erstellt und sie wird einer bestehenden Gruppe ('DevOps') zugewiesen, die noch keine Aufgabe hat. Nachdem die Aufgabe erstellt wurde, wird mit 'Zurück' auf die Startseite gewechselt. Dort ist die Gruppe 'DevOps' aufgeführt und darin die Aufgabe 'Testung'.

Dann wird in DBeaver mit ```bash SELECT * FROM tasks; ``` die Tabelle der Aufgaben aufgerufen und kontrolliert, ob alle Daten der erstellten Aufgabe eingefügt wurden. Das ist der Fall.

### Testung der Gruppenerstellung

Es wird die Gruppe 'Testungen' erstellt. Dann wird in DBeaver mit ```bash SELECT * FROM groups; ``` die Tabelle der Gruppen abgefragt und die neu erstellte Gruppe 'Testungen' wurde unter id 7 abgespeichert. 

## Testung von Änderungen in der Datenbank

Es soll getestet werden, ob Änderungen in der Datenbank auch im Taskmanager angezeigt werden. Dafür wird die SQL-Abfrage ```bash UPDATE tasks SET group_id = 7 WHERE id = 7; ``` ausgeführt. Damit wird die Aufgabe Testung (id 7) in die Gruppe Testung (group_id 7) verschoben. Zuvor war sie in der Gruppe group_id 4 ('DevOps'). 
Nachdem der Browser aktuallisiert wurde, erscheint die Gruppe 'Testungen' mit der Aufgabe 'Testung'. 

## Resultat

Es konnte nachgewiesen werden, dass alle Links funktionieren, Daten vom Taskmanger in die Datenbank eingefügt werden und, dass Änderungen in der Datenbank auch im Taskmanager angezeigt werden. Die Datenbankanbindung funktioniert also.

Nach der Testung wird der Taskmanager mit ```bash docker stop taskmanager ``` beendet.

Da die Testung erfolgreich war, kommt nun der nächste große Schritt, das Deployment des Taskmanagers. Also die Bereitstellung des Taskmanager-Containers.