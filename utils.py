import sys
import os

def resource_path(relative_path):
    """
    PyInstaller (.exe) ve normal Python çalıştırma için
    ortak dosya yolu çözücü
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller exe içindeyken
        base_path = sys._MEIPASS
    else:
        # Normal python çalıştırma
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
