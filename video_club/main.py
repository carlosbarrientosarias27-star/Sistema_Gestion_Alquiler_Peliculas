import sys
import os

# Añade la carpeta actual al path de búsqueda de Python
directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.append(directorio_actual)

from database.init_db import init_db
from ui.menu import Menu

def main() -> None:
    init_db()
    menu = Menu()
    menu.ejecutar()

if __name__ == "__main__":
    main()