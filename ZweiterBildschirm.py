# debug modus kann mit d ein und ausgeschaltet werden
# Die Ausgabe erscheint in der Konsole
# ToDo:
# Klasse, Methoden, Attribute, Variablen, Konstanten auf englisch ändern
# Kommentare auf englisch ändern
# Spielregeln richtig anzeigen
# Zugwang implementieren
# Punkte anzeigen
# jedes mal schlagen erhöht die Punkte um 1


import pygame
import sys

class ZweiterBildschirm:
    def __init__(self, text):
        pygame.init()
        pygame.font.init()
        self.fenster = pygame.display.set_mode((1400,800))
        pygame.display.set_caption("Damespiel")
        self.hintergrund = pygame.Surface(self.fenster.get_size())
        self.hintergrund = self.hintergrund.convert()
        self.hintergrund.fill((80, 80, 8)) # Schwarzer Hintergrund
        self.text = text
        self.text_lines = text.split('\n')
        self.font = pygame.font.SysFont('Arial', 12)
        self.text_rendered = self.font.render(self.text, True, (255, 255, 255))

    def anzeigen(self):
        self.fenster.blit(self.hintergrund, (0, 0)) # Hintergrund schwarz
        y_offset = 5
        for line in self.text_lines:
            rendered_line = self.font.render(line, True, (255,255,255))
            self.fenster.blit(rendered_line, (650, y_offset))
            y_offset += 30 # Abstand zwischen den Zeilen     
        pygame.display.flip()   

    def clear(self):
        SCHWARZ = (255,255,255)
        screen = pygame.display.set_mode((1400,800))
        screen.fill(SCHWARZ)
        pygame.display.flip()

    def schließen(self):
        self.fenster = None
        pygame.display.set_mode((1400,800)) # Setze die Fenstergröße zurück

