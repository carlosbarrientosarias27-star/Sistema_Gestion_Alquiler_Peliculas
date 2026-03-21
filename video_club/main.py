import sys
import os

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