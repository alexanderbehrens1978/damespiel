# debug modus kann mit d ein und ausgeschaltet werden
# Die Ausgabe erscheint in der Konsole

import pygame
import sys

class DameSpiel:
    def __init__(self):
        self.brett_groesse = 8
        self.feld_groesse = 80  # Größe eines Feldes in Pixeln
        self.fenster_groesse = self.feld_groesse * self.brett_groesse
        self.farben = {1: (255, 255, 255), 0: (0, 0, 0)}  # Weiß und Schwarz
        self.steine = {}  # Speichert die Positionen der Spielsteine
        self.aktueller_spieler = 'W'  # Der Spieler, der am Zug ist
        self.ausgewaehlter_spielstein = None  # Ausgewählter Spielstein

        self.debug_mode = False  # Debug-Modus standardmäßig ausgeschaltet

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.fenster = pygame.display.set_mode((self.fenster_groesse, self.fenster_groesse))
        pygame.display.set_caption("Damespiel - created by Alexander Behrens & KI")  # Fenstertitel setzen
        self.uhr = pygame.time.Clock()

        self.create_board()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Dunkle Felder
                    if row < 3:
                        self.steine[(row, col)] = 'B'  # Schwarze Spielsteine
                    elif row > 4:
                        self.steine[(row, col)] = 'W'  # Weiße Spielsteine

    def debug_log(self, message):
        if self.debug_mode:
            print(message)

    def zeichne_brett(self):
        for row in range(self.brett_groesse):
            for col in range(self.brett_groesse):
                farbe = self.farben[(row + col) % 2]
                pygame.draw.rect(self.fenster, farbe, (col * self.feld_groesse, row * self.feld_groesse, self.feld_groesse, self.feld_groesse))

        for pos, stein in self.steine.items():
            if stein == 'B':
                farbe = (139, 69, 19)  # Braun
            elif stein == 'W':
                farbe = (255, 255, 0)  # Gelb

            pygame.draw.circle(self.fenster, farbe, (pos[1] * self.feld_groesse + self.feld_groesse // 2, pos[0] * self.feld_groesse + self.feld_groesse // 2), self.feld_groesse // 2 - 10)

        # Rote Punkte oben und unten
        if self.aktueller_spieler == 'W':
            pygame.draw.circle(self.fenster, (255, 0, 0), (self.fenster_groesse // 2, self.fenster_groesse - 20), 10)
        else:
            pygame.draw.circle(self.fenster, (255, 0, 0), (self.fenster_groesse // 2, 20), 10)

    def on_click(self, pos):
        row, col = pos[1] // self.feld_groesse, pos[0] // self.feld_groesse
        self.debug_log(f"Clicked at row: {row}, col: {col}")

        if self.ausgewaehlter_spielstein:
            self.bewege_stein(row, col)
        elif (row, col) in self.steine and self.steine[(row, col)][0] == self.aktueller_spieler:
            self.ausgewaehlter_spielstein = (row, col)

    def is_valid_move(self, start_row, start_col, end_row, end_col, stein):
        # Prüfen, ob der Zug diagonal ist und nur nach vorne
        if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
            if stein == 'W':
                return end_row < start_row  # Nur nach oben erlauben
            elif stein == 'B':
                return end_row > start_row  # Nur nach unten erlauben
        elif abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
            # Schlagzug
            mitte_row = (end_row + start_row) // 2
            mitte_col = (end_col + start_col) // 2
            if (mitte_row, mitte_col) in self.steine and self.steine[(mitte_row, mitte_col)][0] != stein:
                if stein == 'W':
                    return end_row < start_row  # Nur nach oben erlauben
                elif stein == 'B':
                    return end_row > start_row  # Nur nach unten erlauben
        return False

    def bewege_stein(self, row, col):
        if self.ausgewaehlter_spielstein and self.ausgewaehlter_spielstein in self.steine:
            ausgewaehlte_row, ausgewaehlte_col = self.ausgewaehlter_spielstein
            stein = self.steine[self.ausgewaehlter_spielstein]

            if self.is_valid_move(ausgewaehlte_row, ausgewaehlte_col, row, col, stein):
                if abs(row - ausgewaehlte_row) == 2 and abs(col - ausgewaehlte_col) == 2:
                    # Es handelt sich um einen Schlagzug, entferne den geschlagenen Stein
                    mitte_row = (row + ausgewaehlte_row) // 2
                    mitte_col = (col + ausgewaehlte_col) // 2
                    del self.steine[(mitte_row, mitte_col)]
                    self.debug_log(f"Piece captured at row: {mitte_row}, col: {mitte_col}")

                del self.steine[self.ausgewaehlter_spielstein]
                self.steine[(row, col)] = stein
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
                        # Debug-Modus ein- oder ausschalten
                        self.toggle_debug(not self.debug_mode)

            self.zeichne_brett()
            pygame.display.flip()
            self.uhr.tick(60)

spiel = DameSpiel()
spiel.starte_spiel()
