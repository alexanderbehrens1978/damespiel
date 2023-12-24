# Dateiname: Main.py
# -*- coding: utf-8 -*-
from DameSpiel import DameSpiel

def main():
    spiel = DameSpiel()
    spiel.zeige_zweiter_bildschirm()
    #spiel.zeichne_brett()
    spiel.starte_spiel()

if __name__ == "__main__":
    main()
