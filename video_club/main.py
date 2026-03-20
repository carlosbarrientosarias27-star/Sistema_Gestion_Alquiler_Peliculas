from video_club.database.connection import Database
from video_club.ui.console import ConsoleUI


def main() -> None:
    """Punto de entrada de la aplicación."""
    db = Database()
    db.connect()
    db.create_tables()

    ui = ConsoleUI()
    ui.ejecutar()


if __name__ == "__main__":
    main()