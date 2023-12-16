# debug modus kann mit d ein und ausgeschaltet werden
# Die Ausgabe erscheint in der Konsole
# offen = r Regelwerk wird in der Konsole angezeigt 
# Regelwerk wird in einem Fenster(bereich) angezeigt
# offen = Rotenpunkt für den aktiven Spieler anzeigen
# offen = Schlagzwang
# offen = richtige Startaufstellung
# flutter Umwandlung 



import pygame
import sys

class ZweiterBildschirm:
    def __init__(self, text):
        pygame.init()
        pygame.font.init()
        self.fenster = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Zweiter Bildschirm")
        
        self.text = text
        self.font = pygame.font.SysFont('Arial', 24)
        self.text_rendered = self.font.render(self.text, True, (255, 255, 255))
              
    def anzeigen(self):
        self.fenster.blit(self.hintergrund, (0, 0)) # Hintergrund schwarz
        self.fenster.blit(self.text_rendered,(50,50))
        pygame.display.flip()
        
    def schließen(self):
        pygame.quit()
        sys.exit()

class DameSpiel:
    def __init__(self):
        self.brett_groesse = 8
        self.feld_groesse = 80
        self.fenster_groesse = self.feld_groesse * self.brett_groesse
        self.farben = {1: (255, 255, 255), 0: (0, 0, 0)}
        self.steine = {}
        self.aktueller_spieler = 'B'
        self.ausgewaehlter_spielstein = None
        self.x_breiter = 800
        self.y_höher = 800
        
        self.zweiter_bildschirm_text = ""
        
        self.debug_mode = False

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.fenster = pygame.display.set_mode((self.fenster_groesse + self.x_breiter, self.fenster_groesse + self.y_höher)) # was ist x und was is y

        pygame.display.set_caption("Damespiel")
        self.uhr = pygame.time.Clock()

        self.create_board()
        self.zweiter_bildschirm = None
        
        self.zweiter_bildschirm_anzeigen = False
        self.zweiter_bildschirm = ZweiterBildschirm("""Das Spielbrett zu Beginn

Das Damebrett wird automatisch so platziert, dass links unten ein\n
dunkles Feld liegt.\n
Der Startspieler beginnt mit den schwarzen Steinen.\n
\n
Das Ziehen der Steine\n
\n
Die Steine ziehen ein Feld in diagonaler Richtung, aber nur vorwärts und nur\n
auf freie dunkle Felder.\n
\n
Schlagen\n
\n
Es gilt Schlagzwang. Bei Brettspielnetz.de wird das automatisch durchgesetzt.\n
Wenn sich eigene freie Steine bei einem Zug nicht anklicken lassen, kann das\n
daran liegen, dass irgendwo auf dem Brett die Möglichkeit zum Schlagen besteht.\n
Nur einer dieser Steine kann dann ausgewählt werden.\n
Einfache Steine dürfen nur vorwärts schlagen.\n
\n
Wenn du die Auswahl zwischen verschiedenen Schlagmöglichkeiten hast, darfst du\n
dich frei entscheiden. Weder ein Mehrfachschlagen, noch ein Schlagen\n
mit einer Dame hat absoluten Vorrang.\n
\n
In Dame umwandeln\n
\n
Du bekommst eine Dame, wenn einer deiner Steine auf der gegnerischen\n
Grundlinie stehen bleibt, egal ob durch einen normalen Zug oder durch\n
ein Schlagen. Der Stein wird dann durch ein "D" gekennzeichnet\n
(im Brettspiel wird ein zweiter Stein darauf gestellt).\n
\n
Eine Dame kannst Du nun sowohl schräg vorwärts als auch rückwärts bewegen\n
und genauso darfst du mit ihr auch schlagen. Im Gegensatz zur internationalen\n
Damenvariante darf sich die Dame aber nur um ein Feld vorwärts oder\n
rückwärts bewegen. Beim Schlagen muss die Dame direkt vor dem gegnerischen\n
Stein stehen und muss nach dem Schlagen direkt hinter dem\n
geschlagenen Stein landen.\n
\n
Spielende\n
\n
Du hast verloren, wenn du keinen Stein mehr hast oder wenn du mit deinen\n
Steinen keinen Zug mehr machen kannst, weil deine Steine durch deinen\n
Gegner blockiert sind. Du kannst auch die Partie verloren geben durch\n
die Aktion "Aufgeben", zum Beispiel weil du so weit zurück liegst,\n
dass ein weiteres Spielen keinen Sinn mehr macht.\n
\n
Unentschieden\n
\n
Manche Partien gehen unentschieden aus. In so einem Fall kann keiner der\n
beiden Spieler mehr gewinnen, es sei denn, der andere macht einen\n
enormen Fehler. Um endlose Partien zu vermeiden, gibt es bei\n
Brettspielnetz.de drei Möglichkeiten für ein Unentschieden:\n
\n
\n
Beide Spieler sind sich darin einig geworden, oder\n
25 Züge wurden gezogen, in denen weder ein Stein geschlagen noch zur\n
Dame umgewandelt wurde (*), oder\n
eine Stellung wiederholt sich zum dritten Mal (*).\n
* Diese Punkte werden von Brettspielnetz nicht automatisch erkannt.\n
Wenn eine dieser Situationen auftritt, schickt eurem Mitspieler mit dem\n
nächsten Zug ein Remis-Angebot und schreibt in der Nachricht die Begründung\n
für euer Remisangebot mit Verweis auf die Spielregel. Sollte er/sie\n
das Remis-Angebot ohne Begründung ablehnen, müsst ihr über das Kontaktformular\n
eine Nachricht an die Admins schicken, in der ihr die Spielnummer und\n
"Dame" notiert und mitteilt, warum ihr eine Remis-Stellung seht.\n
Wenn es sich um eine Zugwiederholung handelt, müsst ihr auch die 3 Zugnummern\n
angeben, in denen sich die Stellung wiederholt - wir suchen keine komplette\n
Partie durch! Der Admin wird das dann prüfen und gegebenenfalls die Partie\n
auf unentschieden setzen. Wenn es tatsächlich Remis ist, kann es dem Gegner\n
passieren, dass er wegen Spielverzögerung verwarnt wird! In dieser Zeit\n
solltet ihr natürlich keine weiteren Züge machen! Bitte beachtet, dass es\n
sich in den Bedingungen um 25 Vollzüge handelt. Das heißt, wenn\n
beispielsweise der erste Zug die Zugnummer 41 hatte, ist das Spiel erst\n
ab dem 66. Zug remis, wenn sich bis dahin nichts getan hat.\n""")
        
        
    def toggle_debug(self, debug_mode):
        self.debug_mode = debug_mode

    def create_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    if row < 3:
                        self.steine[(row, col)] = 'B'  # Schwarze Steine
                    elif row > 4:
                        self.steine[(row, col)] = 'W'  # Weiße Steine

    def debug_log(self):
        if self.debug_mode:
            print("===== Debug-Informationen =====")
            print(f"Aktueller Spieler: {self.aktueller_spieler}")
            print(f"Ausgewählter Spielstein: {self.ausgewaehlter_spielstein}")
            print("Spielsteine auf dem Brett:")
            for pos, stein in self.steine.items():
                print(f"  Position: {pos}, Stein: {stein}")
            print("================================")

    def zeichne_brett(self):
        for row in range(self.brett_groesse):
            for col in range(self.brett_groesse):
                farbe = self.farben[(row + col) % 2]
                pygame.draw.rect(self.fenster, farbe, (col * self.feld_groesse, row * self.feld_groesse, self.feld_groesse, self.feld_groesse))
        for pos, stein in self.steine.items():
            farbe = (139, 69, 19) if stein in ['B', 'BD'] else (255, 255, 0)
            x, y = pos[1] * self.feld_groesse + self.feld_groesse // 2, pos[0] * self.feld_groesse + self.feld_groesse // 2
            pygame.draw.circle(self.fenster, farbe, (x, y), self.feld_groesse // 2 - 10)
            if 'D' in stein:  # 'D' im Inneren für Damesteine
                schrift = pygame.font.SysFont('Arial', 20, True)
                text = schrift.render('D', True, (0, 0, 0))
                text_rect = text.get_rect(center=(x, y))
                self.fenster.blit(text, text_rect)

        schrift = pygame.font.SysFont('Arial', 35, True, False)
        text = schrift.render("Spieler W", True, (23,125,122))
        self.fenster.blit(text, [self.fenster_groesse/2 - 70, self.fenster_groesse - 35])

        schrift = pygame.font.SysFont('Arial', 35, True, False)
        text = schrift.render("Spieler B", True, (55,55,55))
        self.fenster.blit(text, [250, 0]) 

    def spiel_ist_vorbei(self):
        # Prüfen, ob ein Spieler keine Steine mehr hat
        hat_weisse_steine = any(stein.startswith('W') for stein in self.steine.values())
        hat_schwarze_steine = any(stein.startswith('B') for stein in self.steine.values())
        return not hat_weisse_steine or not hat_schwarze_steine


    def on_click(self, pos):
        row, col = pos[1] // self.feld_groesse, pos[0] // self.feld_groesse
        if self.ausgewaehlter_spielstein:
            if self.is_valid_move(*self.ausgewaehlter_spielstein, row, col, self.steine[self.ausgewaehlter_spielstein]):
                self.bewege_stein(row, col)
            else:
                # Wenn der Zug nicht gültig ist, Auswahl aufheben und dem Spieler erlauben, einen anderen Stein zu wählen
                self.ausgewaehlter_spielstein = None
        elif (row, col) in self.steine and self.steine[(row, col)][0] == self.aktueller_spieler:
            self.ausgewaehlter_spielstein = (row, col)


    def is_valid_move(self, start_row, start_col, end_row, end_col, stein):
        # Standardbewegung für einfache Steine
        if stein in ['W', 'B']:
            if (end_row, end_col) in self.steine:
                return False
            if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
                return (stein == 'W' and end_row < start_row) or (stein == 'B' and end_row > start_row)
            elif abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
                mitte_row = (end_row + start_row) // 2
                mitte_col = (end_col + start_col) // 2
                return (mitte_row, mitte_col) in self.steine and self.steine[(mitte_row, mitte_col)][0] != stein

        # Bewegung für Damesteine
        elif stein in ['WD', 'BD']:
            return self.is_valid_dame_move(start_row, start_col, end_row, end_col, stein)

        return False
    
    def is_valid_dame_move(self, start_row, start_col, end_row, end_col, stein):
        if (end_row, end_col) in self.steine:
            return False

        # Prüfen, ob die Bewegung diagonal ist
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False

        direction_row = 1 if end_row > start_row else -1
        direction_col = 1 if end_col > start_col else -1
        current_row, current_col = start_row, start_col

        while (current_row != end_row) and (current_col != end_col):
            current_row += direction_row
            current_col += direction_col

            # Wenn ein Stein auf dem Weg ist, muss es ein gegnerischer Stein sein und genau einmal vorkommen
            if (current_row, current_col) in self.steine:
                if self.steine[(current_row, current_col)][0] == stein[0]:
                    return False
                if current_row + direction_row != end_row or current_col + direction_col != end_col:
                    return False

        return True

    def is_valid_move(self, start_row, start_col, end_row, end_col, stein):
        if (end_row, end_col) in self.steine:
            return False

        # Bewegung für normale Steine
        if stein in ['W', 'B']:
            # Normale Steine dürfen nur vorwärts schlagen
            if stein == 'W' and end_row >= start_row:
                return False
            if stein == 'B' and end_row <= start_row:
                return False

            if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
                return True
            elif abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
                mitte_row = (end_row + start_row) // 2
                mitte_col = (end_col + start_col) // 2
                if (mitte_row, mitte_col) in self.steine and self.steine[(mitte_row, mitte_col)][0] != stein:
                    return True
            return False

        # Bewegung für Damesteine
        elif stein in ['WD', 'BD']:
            return self.is_valid_dame_move(start_row, start_col, end_row, end_col, stein)

        return False

    def bewege_stein(self, row, col):
        if self.ausgewaehlter_spielstein and self.ausgewaehlter_spielstein in self.steine:
            ausgewaehlte_row, ausgewaehlte_col = self.ausgewaehlter_spielstein
            stein = self.steine[self.ausgewaehlter_spielstein]
            if self.is_valid_move(ausgewaehlte_row, ausgewaehlte_col, row, col, stein):
                schlagzug = abs(row - ausgewaehlte_row) == 2 and abs(col - ausgewaehlte_col) == 2
                del self.steine[self.ausgewaehlter_spielstein]
                self.steine[(row, col)] = stein

                if schlagzug:
                    mitte_row = (row + ausgewaehlte_row) // 2
                    mitte_col = (col + ausgewaehlte_col) // 2
                    del self.steine[(mitte_row, mitte_col)]

                    if 'D' in stein and self.kann_weiter_schlagen(row, col):
                        self.ausgewaehlter_spielstein = (row, col)
                    else:
                        self.wechsel_spieler()
                        self.ausgewaehlter_spielstein = None
                else:
                    self.wechsel_spieler()
                    self.ausgewaehlter_spielstein = None
        
        gegner = 'W' if self.aktueller_spieler == 'B' else 'B'
        if not self.hat_gueltige_zuege(gegner):
            self.zeige_ende_nachricht(gegner)

    def kann_weiter_schlagen(self, row, col):
        stein = self.steine.get((row, col))
        if not stein or 'D' not in stein:
            return False

        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            test_row = row + direction[0] * 2
            test_col = col + direction[1] * 2
            if 0 <= test_row < self.brett_groesse and 0 <= test_col < self.brett_groesse:
                if self.is_valid_move(row, col, test_row, test_col, stein):
                    return True
        return False

    def hat_gueltige_zuege(self, spieler):
        for pos, stein in self.steine.items():
            if stein.startswith(spieler):
                if self.kann_sich_bewegen(*pos):
                    return True
        return False

    def kann_sich_bewegen(self, row, col):
        stein = self.steine.get((row, col))
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for distanz in range(1, self.brett_groesse):
                test_row = row + direction[0] * distanz
                test_col = col + direction[1] * distanz
                if 0 <= test_row < self.brett_groesse and 0 <= test_col < self.brett_groesse:
                    if not self.is_valid_move(row, col, test_row, test_col, stein):
                        break
                    if self.is_valid_move(row, col, test_row, test_col, stein):
                        return True
        return False

    def zeige_ende_nachricht(self):
        gewinner = None
        verlierer = 'Spieler B'  # Annahme eines Standardwertes für den Verlierer
      
        if not any(stein.startswith('W') for stein in self.steine.values()):
            gewinner = 'Spieler B'
            verlierer = 'Spieler A'  # Falls Spieler A gewonnen hat
        elif not any(stein.startswith('B') for stein in self.steine.values()):
            gewinner = 'Spieler A'
            verlierer = 'Spieler B'

        if gewinner:
            nachricht = f"{gewinner} hat gewonnen! {verlierer} kann sich nicht mehr bewegen. Noch eine Runde? (Ja/Nein)"
            pygame.draw.rect(self.fenster, (0, 0, 0), (100, self.fenster_groesse // 2 - 60, self.fenster_groesse - 200, 120))
            schrift = pygame.font.SysFont('Arial', 30)
            text = schrift.render(nachricht, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.fenster_groesse // 2, self.fenster_groesse // 2))
            self.fenster.blit(text, text_rect)
            pygame.display.flip()

            self.warte_auf_antwort()


    def zeige_zweiter_bildschirm(self):
        if not self.zweiter_bildschirm_anzeigen:
            self.zweiter_bildschirm = ZweiterBildschirm(self.zweiter_bildschirm_text)
            self.zweiter_bildschirm_anzeigen = True
            self.zweiter_bildschirm_anzeigen()
        else:
            self.zweiter_bildschirm.schließen()
            self.zweiter_bildschirm_anzeigen = False

    def bewege_stein(self, row, col):
        if self.ausgewaehlter_spielstein and self.ausgewaehlter_spielstein in self.steine:
            ausgewaehlte_row, ausgewaehlte_col = self.ausgewaehlter_spielstein
            stein = self.steine[self.ausgewaehlter_spielstein]
            if self.is_valid_move(ausgewaehlte_row, ausgewaehlte_col, row, col, stein):
                if abs(row - ausgewaehlte_row) == 2 and abs(col - ausgewaehlte_col) == 2:
                    mitte_row = (row + ausgewaehlte_row) // 2
                    mitte_col = (col + ausgewaehlte_col) // 2
                    del self.steine[(mitte_row, mitte_col)]

                del self.steine[self.ausgewaehlter_spielstein]
                self.steine[(row, col)] = stein

                # Dame-Umwandlung mit 'D' im Inneren
                if stein == 'W' and row == 0:
                    self.steine[(row, col)] = 'WD'
                elif stein == 'B' and row == self.brett_groesse - 1:
                    self.steine[(row, col)] = 'BD'

                self.wechsel_spieler()
                self.ausgewaehlter_spielstein = None

    def wechsel_spieler(self):
        self.aktueller_spieler = 'W' if self.aktueller_spieler == 'B' else 'B'

    def toggle_debug(self, debug_mode):
        self.debug_mode = debug_mode

    def zeige_ende_nachricht(self):
        gewinner = None
        gewinner = 'Spieler A' if verlierer == 'B' else 'Spieler B'
        nachricht = f"{gewinner} hat gewonnen! {verlierer} kann sich nicht mehr bewegen. Noch eine Runde? (Ja/Nein)"
        if not any(stein.startswith('W') for stein in self.steine.values()):
            gewinner = 'Spieler B'
        elif not any(stein.startswith('B') for stein in self.steine.values()):
            gewinner = 'Spieler A'

        if gewinner:
            nachricht = f"{gewinner} hat gewonnen! Noch eine Runde? (Ja/Nein)"
            pygame.draw.rect(self.fenster, (0, 0, 0), (100, self.fenster_groesse // 2 - 60, self.fenster_groesse - 200, 120))
            schrift = pygame.font.SysFont('Arial', 30)
            text = schrift.render(nachricht, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.fenster_groesse // 2, self.fenster_groesse // 2))
            self.fenster.blit(text, text_rect)
            pygame.display.flip()

            self.warte_auf_antwort()

    def warte_auf_antwort(self):
            ja_button = pygame.Rect(100, self.fenster_groesse // 2 + 30, 150, 50)
            nein_button = pygame.Rect(self.fenster_groesse - 250, self.fenster_groesse // 2 + 30, 150, 50)
            pygame.draw.rect(self.fenster, (0, 255, 0), ja_button)  # Grüner Ja-Button
            pygame.draw.rect(self.fenster, (255, 0, 0), nein_button)  # Roter Nein-Button

            schrift = pygame.font.SysFont('Arial', 30)
            ja_text = schrift.render('Ja', True, (0, 0, 0))
            nein_text = schrift.render('Nein', True, (0, 0, 0))
            self.fenster.blit(ja_text, (ja_button.x + 50, ja_button.y + 10))
            self.fenster.blit(nein_text, (nein_button.x + 40, nein_button.y + 10))
            pygame.display.flip()

            warten = True
            while warten:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if ja_button.collidepoint(event.pos):
                            self.__init__()  # Spiel zurücksetzen und eine neue Runde starten
                            return
                        elif nein_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

    def starte_spiel(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.on_click(pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.toggle_debug(not self.debug_mode)
                    elif event.key == pygame.K_h:
                        if not self.zweiter_bildschirm_anzeigen:
                            self.zeige_zweiter_bildschirm()
                        else:
                            pygame.quit()
                            sys.exit()

            if self.spiel_ist_vorbei():
                self.zeige_ende_nachricht()

            self.zeichne_brett()
            self.debug_log()
            pygame.display.flip()
            self.uhr.tick(60)

spiel = DameSpiel()
spiel.starte_spiel()