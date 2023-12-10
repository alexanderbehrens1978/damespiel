from damegui import DameSpiel

def starte_spiel():
    # Erstelle ein neues Spiel
    game = DameSpiel()

    # Starte den Spielloop
    game.starte_spiel()

if __name__ == "__main__":
    # Starte das Spiel
    starte_spiel()
# Das Programm ist noch Buggy
# Beim beenden wird das erste Fenster geschlossen und ein zweites Fenster erscheint.

