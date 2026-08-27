# Aktuelles UI-Konzept

Das UI-Konzept wird fortlaufend angepasst und auf dem aktuellen Stand gehalten.

## Design

Es wird mit Farben und Symbolen gearbeitet und einem einfachen Design. 

Grunddesign:
    • gesamte Schrift: Liberation Mono 
    • Startseite: Anthrazit 
    • Detailansicht: dunkles Grau, etwas heller als die Startseite 
    • Schriftfarbe: helles Grau, kein reines Weiß 
    • Links: gut sichtbares Türkis 
    • farbige Status- und Prioritätssymbole wie oben beschrieben 

## Darstellung der Startseite:

Kategorien werden nur angezeigt, wenn sie Daten enthalten. Wurde z.B. keine Deadline eingetragen, wird Deadline auch nicht angezeigt. Auf der Startseite werden die wichtigsten Informationen der Aufgaben angezeigt.

♦ Docker
    ♦ Docker Compose Grundlagen ● Mittel ■ Offen
    ♦ Docker Tutorial Teil 1    ● Mittel ■ In Bearbeitung Deadline: Freitag
    ♦ Docker Tutorial Teil 2    ● Hoch   ■ Offen Deadline: ...
    ♦ Docker installieren       ● Mittel ■ Erledigt

♦ Linuxbefehlsübersicht erstellen ● Niedrig ■ Offen Deadline: ...

Dabei gilt:
    • Gruppen haben eine rosa Raute 
    • Aufgaben haben eine fliederfarbene Raute 
    • gruppierte Aufgaben sind eingerückt 
    • gruppenlose Aufgaben stehen auf der Ebene der Gruppennamen 
    • für gruppenlose Aufgaben gibt es keine zusätzliche Überschrift 
    • Gruppennamen sind größer und fett 
    • Gruppennamen bleiben in der normalen Schriftfarbe und sind nicht türkis 
    • Aufgabentitel sind Links und türkis/unterstrichen 
    • nur der Aufgabentitel ist klickbar 
    • Status und Priorität sind nicht klickbar 
    • Deadlines sind nicht klickbar 
    • Abhängigkeiten werden nicht auf der Startseite angezeigt 
    • Abhängigkeiten erscheinen nur in der Detailansicht 

Statusdarstellung:
    • Offen → blaues Quadrat 
    • In Bearbeitung → weißes Quadrat 
    • Erledigt → lachsfarbenes Quadrat 

Priorität:
    • Niedrig → grüner Kreis 
    • Mittel → gelber Kreis 
    • Hoch → roter Kreis 

Die genaue grafische Umsetzung erfolgt mit CSS.

## Detailansicht

Wie auf der Statseite, werden Kategorien nur angezeigt, wenn sie Daten enthalten. Aber in der Detailansicht werden entsprechend alle vorhandenen Kategorien angezeigt, z.B. auch die Beschreibung.

Detailansicht einer Aufgabe:

♦ Docker Compose Grundlagen (-> Titel)
    ● Mittel (-> Priorität)
    ■ Offen (-> Status)
    (Deadline:)
    Gruppe: Docker (-> Gruppenname)
    (Beschreibung:)

<- Zurück