import pygame
import sys
from ZweiterBildschirm import ZweiterBildschirm

class DameSpiel:
    def __init__(self):
        self.brett_groesse = 8
        self.feld_groesse = 80
        self.fenster_groesse = self.feld_groesse * self.brett_groesse
        self.steine = {}
        self.aktueller_spieler = 'B'
        self.ausgewaehlter_spielstein = None
        self.x_breiter = 600
        self.y_höher = 150
        self.rahmenbreite = 5 # Definieren der Rahmenbreite in Pixel
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
        self.zweiter_bildschirm_text = self.lade_spielregeln()

    def berechne_brett_startpunkt(self):
        brett_gesamtgroesse  = self.feld_groesse * self.brett_groesse
        brett_start_x = (self.fenster_groesse + self.x_breiter - brett_gesamtgroesse) // 2
        brett_start_y = (self.fenster_groesse + self.y_höher - brett_gesamtgroesse) // 2
        return brett_start_x, brett_start_y

    def lade_spielregeln(self):
        try:
            with open('spielregeln.txt','r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "Spielregeln konnten nicht geladen werden."

    def create_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 != 0:  # Dunkle Felder haben eine ungerade Summe von Reihe und Spalte
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
        dunkle_farbe = (0, 0, 0)  # Schwarz
        helle_farbe = (255, 255, 255)  # Weiß
        rahmenbreite = 5  # Breite des Rahmens in Pixel
        rahmenfarbe = (255, 0, 0)  # Farbe des Rahmens, hier rot

        brett_start_x, brett_start_y = self.berechne_brett_startpunkt()

        # Zeichne den Rahmen um das Brett
        pygame.draw.rect(self.fenster, rahmenfarbe, (brett_start_x - rahmenbreite, brett_start_y - rahmenbreite, self.feld_groesse * self.brett_groesse + rahmenbreite * 2, self.feld_groesse * self.brett_groesse + rahmenbreite * 2), rahmenbreite)

        for row in range(self.brett_groesse):
            for col in range(self.brett_groesse):
                if (row + col) % 2 == 0:
                    farbe = helle_farbe
                else:
                    farbe = dunkle_farbe

                pygame.draw.rect(self.fenster, farbe, (col * self.feld_groesse + brett_start_x, row * self.feld_groesse + brett_start_y, self.feld_groesse, self.feld_groesse))

        # Zeichne die Spielsteine
        for pos, stein in self.steine.items():
            farbe_stein = (139, 69, 19) if stein in ['B', 'BD'] else (255, 255, 0)
            x, y = pos[1] * self.feld_groesse + self.feld_groesse // 2 + brett_start_x, pos[0] * self.feld_groesse + self.feld_groesse // 2 + brett_start_y
            pygame.draw.circle(self.fenster, farbe_stein, (x, y), self.feld_groesse // 2 - 10)

            if 'D' in stein:
                schrift = pygame.font.SysFont('Arial', 20, True)
                text = schrift.render('D', True, (0, 0, 0))
                text_rect = text.get_rect(center=(x, y))
                self.fenster.blit(text, text_rect)

        # Zeichne den Text für Spieler W und Spieler B
        schrift = pygame.font.SysFont('Arial', 35, True, False)

        # Text für Spieler W
        text_w = schrift.render("Spieler W", True, (23, 125, 122))
        text_w_rect = text_w.get_rect(center=(self.fenster_groesse // 2 + self.x_breiter // 2, self.fenster_groesse + self.y_höher // 2 + 50))
        self.fenster.blit(text_w, text_w_rect)

        # Text für Spieler B
        text_b = schrift.render("Spieler B", True, (55, 55, 55))
        text_b_rect = text_b.get_rect(center=(self.fenster_groesse // 2 + self.x_breiter // 2, self.y_höher // 2 - 50))
        self.fenster.blit(text_b, text_b_rect)
        
        pygame.display.flip()

    def spiel_ist_vorbei(self):
        # Prüfen, ob ein Spieler keine Steine mehr hat
        hat_weisse_steine = any(stein.startswith('W') for stein in self.steine.values())
        hat_schwarze_steine = any(stein.startswith('B') for stein in self.steine.values())
        return not hat_weisse_steine or not hat_schwarze_steine

    def on_click(self, pos):
        brett_start_x, brett_start_y = self.berechne_brett_startpunkt()
        brett_gesamtgroesse = self.feld_groesse * self.brett_groesse + self.rahmenbreite * 2
        brett_start_x = (self.fenster_groesse + self.x_breiter - brett_gesamtgroesse) // 2
        brett_start_y = (self.fenster_groesse + self.y_höher - brett_gesamtgroesse) // 2

        # Berechne die Position relativ zum Brett
        pos_x = pos[0] - brett_start_x - self.rahmenbreite
        pos_y = pos[1] - brett_start_y - self.rahmenbreite

        # Überprüfe, ob der Klick innerhalb des Bretts liegt
        if 0 <= pos_x < self.feld_groesse * self.brett_groesse and 0 <= pos_y < self.feld_groesse * self.brett_groesse:
            row, col = pos_y // self.feld_groesse, pos_x // self.feld_groesse
        else:
            return
        
        if self.ausgewaehlter_spielstein:
            if self.is_valid_move(*self.ausgewaehlter_spielstein, row, col, self.steine[self.ausgewaehlter_spielstein]):
                self.bewege_stein(row, col)
            else:
                # Wenn der Zug nicht gültig ist, Auswahl aufheben und dem Spieler erlauben, einen anderen Stein zu wählen
                self.ausgewaehlter_spielstein = None
        elif (row, col) in self.steine and self.steine[(row, col)][0] == self.aktueller_spieler:
            self.ausgewaehlter_spielstein = (row, col)

    def is_valid_move(self, start_row, start_col, end_row, end_col, stein):
        if (end_row, end_col) in self.steine:
            return False

        if stein in ['W', 'B']:
            # Logik für normale Steine
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

        elif stein in ['WD', 'BD']:
            # Logik für Damesteine
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

    def bewege_stein(self, row, col):
        if self.ausgewaehlter_spielstein and self.ausgewaehlter_spielstein in self.steine:
            ausgewaehlte_row, ausgewaehlte_col = self.ausgewaehlter_spielstein
            stein = self.steine[self.ausgewaehlter_spielstein]

            if self.is_valid_move(ausgewaehlte_row, ausgewaehlte_col, row, col, stein):
                schlagzug = abs(row - ausgewaehlte_row) == 2 and abs(col - ausgewaehlte_col) == 2
                del self.steine[self.ausgewaehlter_spielstein]
                self.steine[(row, col)] = stein

                # Behandlung von Schlagzügen
                if schlagzug:
                    mitte_row = (row + ausgewaehlte_row) // 2
                    mitte_col = (col + ausgewaehlte_col) // 2
                    del self.steine[(mitte_row, mitte_col)]

                # Beförderung zur Dame
                if stein == 'W' and row == 0:
                    self.steine[(row, col)] = 'WD'  # Weiße Dame
                elif stein == 'B' and row == self.brett_groesse - 1:
                    self.steine[(row, col)] = 'BD'  # Schwarze Dame

                self.wechsel_spieler()
                self.ausgewaehlter_spielstein = None

        gegner = 'W' if self.aktueller_spieler == 'B' else 'B'
        if not self.hat_gueltige_zuege(gegner):
            self.zeige_ende_nachricht()

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

    def zeige_zweiter_bildschirm(self):
            if not self.zweiter_bildschirm_anzeigen:
                self.zweiter_bildschirm = ZweiterBildschirm(self.zweiter_bildschirm_text)
                self.zweiter_bildschirm.anzeigen()
                self.zweiter_bildschirm_anzeigen = True
            else:
                # Schließen Sie nur das Hilfefenster
                if self.zweiter_bildschirm:
                    self.zweiter_bildschirm.schließen()
                self.zweiter_bildschirm_anzeigen = False
                self.zeichne_brett() # Zeichnen Sie das Brett neu, um die Änderungen anzuzeigen

    def wechsel_spieler(self):
        self.aktueller_spieler = 'W' if self.aktueller_spieler == 'B' else 'B'

    def toggle_debug(self, debug_mode):
        self.debug_mode = debug_mode

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
                        self.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if ja_button.collidepoint(event.pos):
                            self.__init__()  # Spiel zurücksetzen und eine neue Runde starten
                            return
                        elif nein_button.collidepoint(event.pos):
                            self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()

    def starte_spiel(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.on_click(pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.toggle_debug(not self.debug_mode)
                    elif event.key == pygame.K_h:
                        self.zeige_zweiter_bildschirm()
                    elif event.key == pygame.K_q:
                        self.quit()
                    if self.spiel_ist_vorbei():
                        self.zeige_ende_nachricht()

            self.zeichne_brett()
            self.debug_log()
            pygame.display.flip()
            self.uhr.tick(60)

    def reset_spiel(self):
        self.__init__()

spiel = DameSpiel()
spiel.starte_spiel()