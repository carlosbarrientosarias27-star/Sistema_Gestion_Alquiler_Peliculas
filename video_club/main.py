import sys
import os

# Esto permite que los archivos dentro de video_club se vean entre sí
# como 'models', 'services', etc.
directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.append(directorio_actual)

from database.init_db import init_db
from ui.menu import Menu

def main() -> None:
    """Punto de entrada de la aplicación.

    Output:
        None
    """
    init_db()
    menu = Menu()
    menu.ejecutar()


if __name__ == "__main__":
    main()