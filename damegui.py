# debug modus kann mit d ein und ausgeschaltet werden
# Die Ausgabe erscheint in der Konsole
# 11.12.2023
# schlagen funktioniert
# springen funktioniert
# Dame umwandeln geht noch nicht
# einfacher Computer Gegner ist noch nicht implementiert
# KI ist noch nicht implementiert
# KI soll mit minimax und alpha beta pruning implementiert werden
# KI soll mit pygame implementiert werden
# KI soll mit pygame und minimax und alpha beta pruning implementiert werden

# 12.12.2023

# verwendete KI chatgpt 3.5 turbo und chatgpt 4
# chatgpt ist irgendwann zickig
# URL fürs weitere lernen https://www.python-lernen.de/pygame.htm

# Bugs
# beim auswählen eines steines und unmöglichen zügen stürzt das programm ab
# Dame umwandeln geht noch nicht (nur Farbe ändern)

# 14.12.2023
# Dame umwandeln?
# Der Damestein wird umgewandelt, wenn er die letzte Reihe erreicht
# Damesteine können sich diagonal in alle Richtungen bewegen
# schlagen und nochmal schlagen geht mit damesteinen nicht

import pygame
import sys

class DameSpiel:
    def __init__(self):
        self.brett_groesse = 8
        self.feld_groesse = 80
        self.fenster_groesse = self.feld_groesse * self.brett_groesse
        self.farben = {1: (255, 255, 255), 0: (0, 0, 0)}
        self.steine = {}
        self.aktueller_spieler = 'W'
        self.ausgewaehlter_spielstein = None

        self.debug_mode = False

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.fenster = pygame.display.set_mode((self.fenster_groesse, self.fenster_groesse))
        pygame.display.set_caption("Damespiel")
        self.uhr = pygame.time.Clock()

        self.create_board()

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
        text = schrift.render("Spieler A", True, (23,125,122))
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

            self.zeichne_brett()
            self.debug_log()
            pygame.display.flip()
            self.uhr.tick(60)

spiel = DameSpiel()
spiel.starte_spiel()
