Ein Damespiel in Python3.
Das Programm verwendet die pygame Engine.

Mit d wird der Debug Modus aktiviert / deaktiviert. 
Mit h wird der Regeltext angezeigt. Formatierung fehlt noch.

Es wird automatisch überprüft ob pygame installiert wurde oder nicht.

https://www.python-lernen.de/pygame-tutorial.htm



Spielregeln

Das Spielbrett zu Beginn

Das Damebrett wird automatisch so platziert, dass links unten ein dunkles Feld liegt.
Der Startspieler beginnt mit den schwarzen Steinen

![Startaufstellung](https://images.brettspielnetz.de/spelregels/checkers/start.gif)

Das Ziehen der Steine

Die Steine ziehen ein Feld in diagonaler Richtung, aber nur vorwärts und nur auf freie dunkle Felder.

![Das ziehen der Steine](https://images.brettspielnetz.de/spelregels/checkers/schuiven.gif)

Schlagen

Es gilt Schlagzwang. Bei Brettspielnetz.de wird das automatisch durchgesetzt. Wenn sich eigene freie Steine bei einem Zug nicht anklicken lassen, kann das daran liegen, dass irgendwo auf dem Brett die Möglichkeit zum Schlagen besteht. Nur einer dieser Steine kann dann ausgewählt werden. Einfache Steine dürfen nur vorwärts schlagen.

![Schlagen 1](https://images.brettspielnetz.de/spelregels/checkers/slaan1.gif)

![Schlagen 2](https://images.brettspielnetz.de/spelregels/checkers/slaan2.gif)
