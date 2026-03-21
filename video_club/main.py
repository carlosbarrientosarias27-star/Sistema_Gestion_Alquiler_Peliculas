import sys
import os

# Añadimos el directorio padre al path para que reconozca los paquetes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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