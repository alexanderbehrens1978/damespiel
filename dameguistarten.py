import subprocess
import importlib.util
import sys

def ist_pygame_installiert():
    return importlib.util.find_spec("pygame") is not None

def installiere_pygame():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        return ist_pygame_installiert()
    except Exception as e:
        print(f"Es gab ein Problem bei der Installation von Pygame: {e}")
        return False

def starte_spiel():
    from damegui import DameSpiel
    game = DameSpiel()
    game.starte_spiel()

if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print("Dieses Programm benötigt Python 3. Bitte führen Sie es mit Python 3 aus.")
        sys.exit(1)

    if not ist_pygame_installiert():
        antwort = input("Pygame ist nicht installiert. Möchten Sie es jetzt installieren? (ja/j/nein): ").lower()
        if antwort in ["ja", "j"]:
            print("Installiere Pygame...")
            if installiere_pygame():
                print("Pygame wurde erfolgreich installiert.")
            else:
                print("Die Installation von Pygame ist fehlgeschlagen.")
                print("Sie können Pygame manuell installieren, indem Sie diesen Befehl in Ihrem Terminal ausführen:\n")
                print(f"{sys.executable} -m pip install pygame")
                sys.exit(1)
        else:
            print("Pygame wird benötigt, um das Spiel zu starten. Bitte installieren Sie es manuell, indem Sie diesen Befehl in Ihrem Terminal ausführen:\n")
            print(f"{sys.executable} -m pip install pygame")
            sys.exit(1)

    # Starte das Spiel
    starte_spiel()
