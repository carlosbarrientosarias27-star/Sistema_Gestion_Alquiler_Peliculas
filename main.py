import sys
import os

# Añade la carpeta actual al path de búsqueda de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.init_db import init_db
from ui.menu import Menu

def main() -> None:
    init_db()
    menu = Menu()
    menu.ejecutar()

if __name__ == "__main__":
    main()